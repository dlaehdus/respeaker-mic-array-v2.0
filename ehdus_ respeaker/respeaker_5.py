import pyaudio 
# pyaudio: 오디오 입력(녹음) 및 출력(재생)을 다룰 수 있는 라이브러리
import wave
# wave: WAV 파일을 읽고 쓰는 라이브러리
import numpy as np
# numpy: 오디오 데이터를 배열로 변환하고 처리하는 라이브러리

# 오디오 설정
RESPEAKER_RATE = 16000
# RESPEAKER_RATE = 16000: 16,000Hz(16kHz) 로 샘플링 (일반적인 음성 녹음에 적절)
RESPEAKER_CHANNELS = 4
# RESPEAKER_CHANNELS = 4: ReSpeaker 4 Mic Array는 4개의 마이크(채널) 를 지원
RESPEAKER_WIDTH = 2
# RESPEAKER_WIDTH = 2: 16비트(2바이트) 크기의 샘플을 사용
CHUNK = 1024
# CHUNK = 1024: 오디오 데이터를 1024개 샘플씩 읽음
RECORD_SECONDS = 15
# RECORD_SECONDS = 15: 15초 동안 녹음
WAVE_OUTPUT_FILENAME = "output.wav" 
# WAVE_OUTPUT_FILENAME = "output.wav": 녹음된 WAV 파일 저장 경로


p = pyaudio.PyAudio()
# p = pyaudio.PyAudio(): PyAudio 객체 생성 (오디오 장치를 다루기 위해 필요)
device_index = None
# device_index = None: ReSpeaker 장치의 인덱스를 저장할 변수를 초기화

for i in range(p.get_device_count()):
    dev = p.get_device_info_by_index(i)
    if "ReSpeaker" in dev["name"]:
        device_index = i
        print(f"ReSpeaker 장치 찾음: index {device_index}")
        break

if device_index is None:
    print("ReSpeaker 장치를 찾을 수 없습니다.")
    p.terminate()
    exit()

try:
    # 오디오 스트림 열기
    stream = p.open(
        rate=RESPEAKER_RATE,
        format=p.get_format_from_width(RESPEAKER_WIDTH),
        channels=RESPEAKER_CHANNELS,
        input=True,
        input_device_index=device_index,
    )

    print("* Recording...")

    frames = []

    for _ in range(int(RESPEAKER_RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        # 4채널 중 첫 번째 채널만 추출
        a = np.frombuffer(data, dtype=np.int16)[0::4]  
        frames.append(a.tobytes())

    print("* Done recording")

    # 스트림 정리
    stream.stop_stream()
    stream.close()
    p.terminate()

    # WAV 파일 저장
    with wave.open(WAVE_OUTPUT_FILENAME, "wb") as wf:
        wf.setnchannels(1)  # 1채널로 저장
        wf.setsampwidth(p.get_sample_size(p.get_format_from_width(RESPEAKER_WIDTH)))
        wf.setframerate(RESPEAKER_RATE)
        wf.writeframes(b"".join(frames))

    print(f"녹음 완료! {WAVE_OUTPUT_FILENAME} 저장됨")

except Exception as e:
    print(f"오류 발생: {e}")
    p.terminate()
