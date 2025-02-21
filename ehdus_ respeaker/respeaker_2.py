from tuning import Tuning
# tuning 모듈에서 Tuning 클래스를 가져옴 → Mic Array (마이크 배열) 관련 설정을 제어하기 위해 사용됨.
import usb.core
import usb.util
# usb.core 및 usb.util을 가져옴 → USB 장치 검색 및 제어를 위해 필요.
import time
# time 라이브러리는 딜레이(대기 시간) 처리를 위해 사용됨


dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)
# usb.core.find() 함수를 사용하여 특정 USB 장치를 검색함
# 터미널에 lsusb를 치면 나옴
# idVendor=0x2886, idProduct=0x0018
# Vendor ID (제조사 ID): 0x2886
# Product ID (제품 ID): 0x0018
# ReSpeaker 4-Mic Array 장치를 찾는 코드.
# 만약 dev가 None이면 해당 USB 장치를 찾지 못한 것.

if dev:
    Mic_tuning = Tuning(dev)
    # dev가 None이 아니라면 (즉, 장치를 찾았으면) Tuning 객체를 생성하여 Mic_tuning 변수에 저장.
    # Tuning(dev): ReSpeaker 4-Mic Array의 방향 감지를 담당하는 객체를 생성.
    print (Mic_tuning.direction)
    # Mic_tuning.direction → 마이크가 감지한 소리의 **방향(각도)**을 출력.
    while True:
        try:
            print (Mic_tuning.direction)
            time.sleep(1)
            # 무한 루프를 실행하여 1초마다 계속 마이크의 방향 값을 출력함.
            # Mic_tuning.direction: 소리가 오는 방향(0~360도)을 반환함.
            # time.sleep(1): 1초 동안 대기 후 다시 방향을 출력.
        except KeyboardInterrupt:
            break

# 전체 코드 동작 과정
# ReSpeaker 4-Mic Array USB 장치를 찾음.
# 찾은 경우 Tuning 객체를 생성하여 마이크의 소리 방향 감지 기능을 활성화.
# 현재 감지된 소리 방향(각도)를 출력.
# 무한 루프를 실행하여 1초마다 소리 방향을 계속 출력.
# 사용자가 CTRL + C를 입력하면 루프를 종료하고 프로그램 종료.