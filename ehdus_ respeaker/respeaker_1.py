import time 
# time 모듈: 프로그램 실행을 지연(sleep)하는 기능을 제공하는 표준 라이브러리.
from pixel_ring import pixel_ring
# pixel_ring 모듈: Seeed ReSpeaker 마이크 모듈 등의 LED 링을 제어하는 라이브러리


if __name__ == '__main__':
# Python 프로그램이 직접 실행될 때만 실행되도록 하는 코드.다른 모듈에서 import 하면 실행되지 않음.
    pixel_ring.change_pattern('echo')


    # def change_pattern(self, pattern):
    # if pattern == 'echo':
    #     self.pattern = Echo(show=self.show)
    # else:
    #     self.pattern = GoogleHome(show=self.show)
    
    # self: 현재 객체(클래스 인스턴스).
    # pattern: 패턴을 지정하는 문자열(예: 'echo', 그 외 다른 패턴).
    # change_pattern은 pattern이 'echo'일 경우: self.pattern을 Echo 클래스의 인스턴스로 설정. 
    # Echo(show=self.show): Echo 패턴 객체를 생성하면서 show 함수를 전달. 
    # self.show: LED의 색상을 업데이트하는 함수(아마도 show(self, data) 함수).

    



    # LED의 패턴을 'echo' 모드로 변경함.
    # 'echo' 패턴이 정확히 무엇을 의미하는지는 라이브러리의 문서를 확인해야 함.
    while True:
    # LED의 상태를 반복적으로 변경하는 무한 루프.
        try:
        # KeyboardInterrupt(Ctrl+C 입력)으로 프로그램을 종료할 수 있도록 예외 처리를 포함함.
            pixel_ring.wakeup()
            # wakeup(): LED를 "깨어있는" 상태로 변경. (일반적으로 밝게 빛나거나 특정 애니메이션을 보여줌)
            time.sleep(3)
            pixel_ring.think()
            # think(): LED가 "생각하는" 상태로 변경. (보통 AI 스피커가 명령을 처리하는 동안 보여지는 패턴)
            time.sleep(3)
            pixel_ring.speak()
            # speak(): LED가 "말하는" 상태로 변경. (보통 음성을 출력할 때 보여지는 패턴)
            time.sleep(6)
            pixel_ring.off()
            # off(): LED를 끔.
            time.sleep(3)
        except KeyboardInterrupt:
        # 사용자가 Ctrl+C를 입력하면 KeyboardInterrupt 예외가 발생.
            break


    pixel_ring.off()
    # 루프가 끝난 후 최종적으로 LED를 끔
    time.sleep(1)
