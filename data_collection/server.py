# 서버
from socket import *
import numpy as np
import os

serverPort = 1234
serverSocket = socket(AF_INET, SOCK_DGRAM)

serverSocket.bind(('0.0.0.0', serverPort)) # 서버 포트 번호(1234)를 소켓에 할당.

SAVE_DIR = "data"
os.makedirs(SAVE_DIR, exist_ok=True) # exist_ok=True: 없으면 생성, 있으면 넘어감

LABELS = {
    0: 'up',
    1: 'down',
    # 추가 예정
}

cnt = 0
data = []

MAX_LEN = 80
FEATURES_LEN = 6

CUR_LABLE_ID = 0 # 제스처 바뀔때마다 바꿔서 돌리기

print('ready to receive')

while True:
    message, clientAddress = serverSocket.recvfrom(1024) # 받을 때까지 블록킹.
    cnt += 1
    receivedData = message.decode()

    # 마지막 패킷
    if ',' not in receivedData:
        total_packets = int(receivedData)

        if cnt != total_packets:
            print('# 저장실패 - 패킷 loss')
        elif total_packets > MAX_LEN:
            print('# 저장실패 - 최대 입력 초과')
        else:
            ### 가공 후 저장
            seq = np.array(data, dtype=np.float32)

            # 패딩 (뒤에 남는쪽을 0으로 채움)
            padded = np.zeros((MAX_LEN, FEATURES_LEN), dtype=np.float32)
            padded[:len(seq), :] = seq 

            # 레이블 열 추가
            y = np.full((1,), CUR_LABLE_ID, dtype=np.int32)
            
            # 저장
            label = LABELS[CUR_LABLE_ID] 
            filename = os.path.join(SAVE_DIR, f"record_{label}.npz")

            if os.path.exists(filename):
                old = np.load(filename)
                X_old, y_old = old["X"], old["y"]
                X_new = np.concatenate([X_old, padded], axis=0)
                y_new = np.concatenate([y_old, [CUR_LABLE_ID]], axis=0)
            else:
                X_new = padded
                y_new = np.array([CUR_LABLE_ID], dtype=np.int32)

            np.savez(filename, X=X_new, y=y_new)
            print(f"# 저장성공 → {filename} (누적: {X_new.shape[0]}개)")
            
        # 리스트 비우고, 다시 루프
        data = []
        cnt = 0
        continue

    # 리스트에 누적 
    else:
        datas = receivedData.split(',')
        if len(datas) == FEATURES_LEN:
            values = list(map(float, datas))
            data.append(values)


