# 서버
from socket import *

serverPort = 1234
serverSocket = socket(AF_INET, SOCK_DGRAM)

serverSocket.bind(('0.0.0.0', serverPort)) # 서버 포트 번호(1234)를 소켓에 할당.

print('ready to receive')

cnt = 0
data = []
while True:
    message, clientAddress = serverSocket.recvfrom(1024) # 받을 때까지 블록킹.
    cnt += 1
    modifiedData = message.decode()#.split(' ')[1]

    # 마지막 패킷
    if ',' not in modifiedData:
        if cnt == int(modifiedData) and int(modifiedData) <= 80:
            ### csv로 저장하는 코드.
            print('# 저장하였습니다')
        else:
            print('# 저장실패')
        # 리스트 비우기
        data = []
    # 리스트에 누적 
    else:
       
    # print(clientAddress, ': recv data = ' + str(modifiedData))
    #### 받은 데이터 리스트로 누적하고, 최종 리스트를 .csv에 append ####
    # 그리고, 마지막에 받는 토탈 데이터 (len == 1인 데이터)랑 최종 리스트 길이랑 다르면 loss난 거로 간주하고, 저장안함.


