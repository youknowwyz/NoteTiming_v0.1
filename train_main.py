import torch
from torch import nn
import re
import collections
import os
import numpy as np
import dataset
import model
from torch import nn, optim

if __name__ == '__main__':

    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    model_test = model.Model()
    model_test.double()
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model_test.parameters(), lr=0.002)

    epochs = 280

    train_iter, val_iter = dataset.get_my_data()
    train_losses = []
    test_losses = []
    len_data = len(train_iter)
    len_val = len(val_iter)
    step = 0
    print_step = 20
    print("len of train is：", len_data)
    print("len of val is:", len_val)



    for e in range(epochs):
        running_loss = 0
        for batch_num ,batch in enumerate(train_iter):
            #print("batch_num:", batch_num)
            #print("batch:", batch[0])
            step += 1
            #for batch in train_iter:

            data = batch[0]
            target = batch[1]
            target = target.long()

            optimizer.zero_grad()
            log_ps = model_test(data)
            loss = criterion(log_ps, target)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
        #print(running_loss)
        else:
            val_loss = 0
            accuracy = 0
            model_test.eval()
            print("########################################################################")
            with torch.no_grad():
                for batch_num_v, batch in enumerate(val_iter):

                    data = batch[0]
                    target = batch[1]
                    target = target.long()

                    log_ps = model_test(data)
                    val_loss += criterion(log_ps, target)

                    ps = torch.exp(log_ps)
                    #print(ps)
                    top_p, top_class = ps.topk(1, dim=1)
                    print(top_p)
                    # print(top_p)
                    print(top_class)
                    print(target)
                    equals = top_class == target.view(*top_class.shape)
                    accuracy += torch.mean(equals.type(torch.FloatTensor))
            model_test.train()

            train_losses.append(running_loss / len_data)
            test_losses.append(val_loss / len_data)

            print("Epoch: {}/{}.. ".format(e + 1, epochs),
                  "Training Loss: {:.3f}.. ".format(running_loss / len_data),
                  "Val Loss: {:.3f}.. ".format(val_loss / len_val),
                  "Val Accuracy: {:.3f}".format(accuracy / len_val))

            running_loss = 0


        if e % 70 == 0 and e > 0:
            torch.save(model_test.state_dict(), 'checkpoints/checkpoint.pth')