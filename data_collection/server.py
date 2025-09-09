# 서버
from socket import *
import numpy as np
import os

serverPort = 1234
serverSocket = socket(AF_INET, SOCK_DGRAM)

serverSocket.bind(('0.0.0.0', serverPort)) # 서버 포트 번호(1234)를 소켓에 할당.

print('ready to receive')

cnt = 0
data = []
MAX_LEN = 80
FEATURES_LEN = 6

while True:
    message, clientAddress = serverSocket.recvfrom(1024) # 받을 때까지 블록킹.
    cnt += 1
    receivedData = message.decode()

    # 마지막 패킷
    if ',' not in receivedData:
        total_packets = int(receivedData)

        if cnt != total_packets:
            print('# 저장실패 - 패킷 loss')
        elif total_packets <= MAX_LEN:
            print('# 저장실패 - 최대 입력 초과')
        else:
            ### csv로 저장하는 코드 *
            seq = np.array(data, dtype=np.float32)

            padded = np.zeros((MAX_LEN, FEATURES_LEN), dtype=np.float32)
            

            print('# 저장성공')
            
        # 리스트 비우고, 다시 루프
        data = []
        cnt = 0
        continue
    # 리스트에 누적 
    else:
        datas = receivedData.split(',')
        data.append(datas)

    #### 받은 데이터 리스트로 누적하고, 최종 리스트를 .csv에 append ####


