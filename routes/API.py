import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import matplotlib.pyplot as plt
import numpy as np
import pickle
import sys

modelParam_List = [208,352,896,272,336,528,288,336,272,336,256,304,304,288,352,1968,224,240,288,192,240]
Lenght_List = [37,60,150, 47, 58, 88, 48, 56, 46, 58, 43, 51, 51, 48, 61, 330, 38, 42, 50, 33, 41]
pathName = "/www/IntelliPenService/routes/model"

num_classes = 3
num_layers = 2
learning_rate = 0.001
output_channel = 4  # 卷积层输出的信道数
sequence_length = 4
input_size = 12  # 卷积层输入数据的维度
hidden_size = 8 * output_channel * 56//4 + 1  # LSTM层输入数据的维度，另外LSTM输出的大小取为输入的2倍
kernel_length = 5
EPOCH = 100
batch_size = 5


def sample(data_1d, x_length = 25):
    length = len(data_1d)   #传入数据长度，eg. 15
    x_list1 = np.array(range(length)) / length  #划分区间，eg, 14个区间
    diff = x_list1[1] - x_list1[0]
    result_list = np.array(range(x_length)) / x_length
    
    result = np.zeros(x_length)
    result[0] = data_1d[0];
    result[-1] = data_1d[-1]   #保证首尾衔接
    
    for i in range(x_length):
        if i == 0:
            pass
        elif i == x_length - 1:
            pass
        else:
            temp = result_list[i]                            #返回的某个x点坐标， 非边缘点
            ceiling = findCeiling(temp, x_list1)             #上区间
            floor = ceiling - 1                              #下区间
            
            x1 = x_list1[floor];    y1 = data_1d[floor]
            x2 = x_list1[ceiling];  y2 = data_1d[ceiling]

            k = (y2 - y1) / diff    #斜率

            result_i = y1 + k *(temp - x1)
            
            result[i] = result_i
    
    return result

def getNormalize(data_1d):
    Max  = max(data_1d)
    Min = min(data_1d)
    diff = Max - Min
    if diff == 0:
        diff == 1e-5
    
    result = []
    for x in data_1d:
        temp = x - Min
        result.append(temp / diff)
    return np.array(result)

def findCeiling(x , interval_list):   #找到一个有序列表中，第一个比x大的数的索引
    for i in range(len(interval_list)):
        if interval_list[i] > x:
            return i
    else:
        return len(interval_list) - 1

def plot(num_str, csv_name):
    data = pd.read_csv(csv_name).iloc[:, 2:14]
    data = np.array(data)
    F1 = data[:, -3]
    F2 = data[:, -2]
    F3 = data[:, -1]
    
    ave = np.load('/www/IntelliPenService/routes/aveList_' + str(num_str) + '.npy')
    ave1_List = ave[0]
    ave2_List = ave[1]
    ave3_List = ave[2]
    
    x = np.array(range(25)) / 25
    
    #plot class1
    plt.subplot(3, 1, 1)
    plt.plot(x, getNormalize(ave1_List), label="Standard")
    plt.plot(x, sample(getNormalize(F1)), label="yours")
    plt.legend(loc='upper left')
    
    #plot class2
    plt.subplot(3, 1, 2)
    plt.plot(x, getNormalize(ave2_List), label="Standard")
    plt.plot(x, sample(getNormalize(F2)), label="yours")
    plt.legend(loc='upper left')
	
    #plot class3
    plt.subplot(3, 1, 3)
    plt.plot(x, getNormalize(ave3_List), label="Standard")
    plt.plot(x, sample(getNormalize(F3)), label="yours")
    plt.legend(loc='upper left')
    
    #改存储路径
    plt.savefig('/www/IntelliPenService/routes/'+num_str+'.png')
#     plt.show()
plot(sys.argv[1], sys.argv[2])
class CNN_1d(nn.Module):
    def __init__(self, num_classes = 3):
        super(CNN_1d, self).__init__()
        self.conv1 = nn.Sequential(nn.Conv1d(in_channels = 1, out_channels = output_channel, kernel_size = kernel_length,
                                             stride = 1, padding = (kernel_length-1)//2,))  # 卷积层1
        self.conv2 = nn.Sequential(nn.Conv1d(in_channels = output_channel, out_channels = 2*output_channel, kernel_size = kernel_length,
                                             stride = 1, padding = (kernel_length-1)//2,))  # 卷积层2
        self.conv3 = nn.Sequential(nn.Conv1d(in_channels = 2*output_channel, out_channels = 4*output_channel, kernel_size = kernel_length,
                                             stride = 1, padding = (kernel_length-1)//2,))  # 卷积层3
        self.conv4 = nn.Sequential(nn.Conv1d(in_channels = 4*output_channel, out_channels = 4*output_channel , kernel_size = kernel_length,
                                             stride = 1, padding = (kernel_length-1)//2,))  # 卷积层4
        self.conv5 = nn.Sequential(nn.Conv1d(in_channels = 4*output_channel, out_channels = 4*output_channel , kernel_size = kernel_length,
                                             stride = 1, padding = (kernel_length-1)//2,))  # 卷积层5
        self.conv6 = nn.Sequential(nn.Conv1d(in_channels = 4*output_channel, out_channels = 2*output_channel , kernel_size = kernel_length,
                                             stride = 1, padding = (kernel_length-1)//2,))  # 卷积层6
        self.dp = nn.Dropout(0.45)

        self.fc = nn.Linear(272, 3)
    
    def forward(self, x):
        conv1_output = self.conv1(x)                                          #444
        conv1_output = self.dp(conv1_output)
        conv2_output = self.conv2(F.max_pool1d(F.relu(conv1_output), 2))      #222
        conv2_output = self.dp(conv2_output)
        conv3_output = self.conv3(F.max_pool1d(F.relu(conv2_output), 2))      #111
        conv3_output = self.dp(conv3_output)
        conv4_output = self.conv4(F.max_pool1d(F.relu(conv3_output), 2))      #56
        conv4_output = self.dp(conv4_output)
        conv5_output = self.conv4(F.max_pool1d(F.relu(conv4_output), 2))      #28
        conv5_output = self.dp(conv5_output)
        conv6_output = self.conv4(F.max_pool1d(F.relu(conv5_output), 2))      #14
        
        out = conv6_output.view(conv6_output.size(0), -1)
        return self.fc(out)

def getScore(num_str, csv_name):
    cnn = CNN_1d()
    cnn.dp = nn.Dropout(0)
    #loading the model parameters
    fileName = pathName + num_str + '.pkl'    #eg: pathName = home/Model_, num_str = '12
                                              #fileName = home/Model_12.pkl
    #adopting the model params
    fc_number = modelParam_List[int(num_str)]
    cnn.fc = nn.Linear(in_features=fc_number, out_features=3, bias=True)
    
    state_dict2 = torch.load(fileName)
    cnn.load_state_dict(state_dict2)
    
    
    #preparing the data
    data = pd.read_csv(csv_name).iloc[:, 2:14]
    data = np.array(data)
    max_length = Lenght_List[int(num_str)]
    
    #短补长截
    x = data.shape[0] ;  y = data.shape[1]
    if (x > max_length):
        data = data[:max_length, :] 
    else:
        pass
    
    num_samples = 1
    feature_dim = 12
    padding_dataSet = np.zeros([num_samples, max_length * feature_dim])    #eg. 99 x 444
    
    for idx, seq in enumerate(data):
        padding_dataSet[:, idx * len(seq) :idx * len(seq) + len(seq)] = seq
    
    data_Tensor = torch.from_numpy(padding_dataSet)
    data_Tensor = Variable(data_Tensor).float()
    x = data_Tensor.shape[0];  y = data_Tensor.shape[1]
    data_Tensor = data_Tensor.view(1, x, y)
    data_Tensor = data_Tensor.permute(1, 0, 2)
#     data_Tensor = torch.from_numpy(data)
#     data_Tensor = Variable(data_Tensor).float()
#     x = data_Tensor.shape[0];  y = data_Tensor.shape[1]
#     data_Tensor = data_Tensor.view(1, x, y)
    
    result = cnn(data_Tensor)
    result = torch.argmax(result).detach().numpy().tolist()
    return result
	
print(getScore(sys.argv[1],sys.argv[2]))
