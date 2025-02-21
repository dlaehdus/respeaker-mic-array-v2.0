from tuning import Tuning
import usb.core
import usb.util
import time
import os
import sys
import cv2
import numpy as np

# 리눅스에서는 USB 장치 접근을 위해 루트 권한이 필요합니다.
# 현재 스크립트가 루트 권한으로 실행되지 않았다면, sudo를 이용해 재실행합니다.
if os.getuid() != 0:
    os.execvp("sudo", ["sudo", "-E", "python3"] + sys.argv)
    sys.exit()

# USB 장치 찾기 (예: ReSpeaker와 같은 장치)
dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)

if dev:
    Mic_tuning = Tuning(dev)

    # OpenCV 윈도우 생성
    window_name = 'Direction Indicator'
    cv2.namedWindow(window_name)

    # 이미지 크기와 중심 좌표 설정
    width, height = 640, 480
    center_x, center_y = width // 2, height // 2

    angle = 0
    dot_positions = []
    dot_display_time = 2  # 점이 표시되는 시간 (초)
    fade_duration = 1     # 점이 사라지기 전 페이드 아웃 시간 (초)

    while True:
        try:
            # 음성 감지 및 방향 추정
            VAD = Mic_tuning.is_voice()
            DOA = Mic_tuning.direction
            angle = DOA

            # 검은색 배경 이미지 생성
            img = np.zeros((height, width, 3), dtype=np.uint8)
            # 중심을 기준으로 반지름이 200인 원 그리기
            radius = 200
            cv2.circle(img, (center_x, center_y), radius, (0, 255, 0), 2)
            overlay = img.copy()

            if VAD == 1:
                print(DOA)
                # 현재 각도에 따른 끝점 좌표 계산
                end_x = int(center_x + radius * np.cos(np.radians(angle)))
                end_y = int(center_y - radius * np.sin(np.radians(angle)))
                # 점의 위치와 표시 시작 시간을 저장
                dot_positions.append(((end_x, end_y), time.time()))

            current_time = time.time()
            
            # 저장된 각 점들을 그리며 페이드 효과 적용
            for (pos, start_time) in dot_positions:
                elapsed_time = current_time - start_time
                if elapsed_time <= dot_display_time + fade_duration:
                    # 표시 시간 동안은 완전 불투명, 이후 서서히 사라지게 함
                    alpha = 1.0 if elapsed_time <= dot_display_time else 1.0 - (elapsed_time - dot_display_time) / fade_duration
                    cv2.circle(overlay, pos, 10, (0, 0, 255), -1)
                    cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)

            # 표시 시간이 지난 점들은 목록에서 제거
            dot_positions = [(pos, start_time) for (pos, start_time) in dot_positions if current_time - start_time <= dot_display_time + fade_duration]

            # 현재 각도 정보를 텍스트로 출력
            cv2.putText(img, f'Angle: {angle} degrees', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            # 이미지 창에 결과 출력
            cv2.imshow(window_name, img)

            # 'q' 키를 누르면 종료 (100ms마다 키 입력 확인)
            key = cv2.waitKey(100) & 0xFF
            if key == ord('q'):
                break
        except KeyboardInterrupt:
            break

    cv2.destroyAllWindows()
