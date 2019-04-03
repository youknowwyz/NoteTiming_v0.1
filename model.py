import torch
from torch import nn
import torch.nn.functional as F

class Model(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(29, 256)
        self.fc2 = nn.Linear(256, 64)
        self.fc3 = nn.Linear(64, 32)
        self.fc4 = nn.Linear(32, 30)

        self.dropout1 = nn.Dropout(p=0.81)
        self.dropout2 = nn.Dropout(p=0.9)
        self.dropout3 = nn.Dropout(p=0.9)
        self.dropout4 = nn.Dropout(p=0.81)

    def forward(self, input):


        # res = self.dropout1(input)
        # res = self.dropout2(F.relu(self.fc1(res)))
        # res = self.dropout3(F.relu(self.fc2(res)))
        # res = self.dropout4(F.relu(self.fc3(res)))
        # res = self.fc4(res)
        res = self.dropout1(F.relu(self.fc1(input)))
        res = self.dropout2(F.relu(self.fc2(res)))
        res = self.dropout3(F.relu(self.fc3(res)))
        res = self.dropout4(F.relu(self.fc4(res)))
        # res = self.fc4(res)
        # print("res_shape_is:", res.shape)
        #res = res.view(-1, 1)
        return res