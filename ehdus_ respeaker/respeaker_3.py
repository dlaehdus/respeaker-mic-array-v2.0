from tuning import Tuning
import usb.core
import usb.util
import time

dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)


if dev:
    Mic_tuning = Tuning(dev)
    print (Mic_tuning.is_voice())
    # USB 장치를 찾았을 경우, Tuning 객체를 생성하여 Mic_tuning 변수에 저장.
    # 이를 통해 마이크의 음성 감지 기능을 사용할 수 있음.
    while True:
        try:
            print (Mic_tuning.is_voice())
            # Mic_tuning.is_voice()는 마이크가 음성을 감지했는지 여부를 반환.
            # True: 음성이 감지됨.
            # False: 음성이 감지되지 않음.
            # 프로그램 시작 시 현재 상태를 한 번 출력.
            time.sleep(1)
        except KeyboardInterrupt:
            break


# 이 코드는 ReSpeaker 4-Mic Array를 사용하여 음성이 감지되었는지 확인하는 코드입니다.
# 기본적으로 소리가 감지되면 True, 소리가 없으면 False를 반환합니다.
# 조용한 환경에서는 False가 계속 출력됨.
# 사람이 말하면 True로 변경됨.
# True가 유지되는 동안 마이크가 계속 음성을 감지하고 있음.