from socket import *
import time
import random
import numpy as np

serverName = 'localhost'
serverPort = 1234
clientSocket = socket(AF_INET, SOCK_DGRAM) # AF, PF 내부적 차이 없음 / DGRAM: 비연결형.

len_ = 79

for i in range(len_):
    list = []
    while len(list) != 6:
        list.append(format(random.random() * 10, "4.2f"))
    message = np.array2string(np.array(list))
    message = message.replace(' ', ',').replace('\'', '')
    clientSocket.sendto(message.encode(), (serverName,serverPort)) # 메시지 바이트로 변환해서(encode) 보내야 함.
    print('send ' + str(message))
    # time.sleep(0.2)

clientSocket.sendto((str(len_)).encode(), (serverName,serverPort))

clientSocket.close()