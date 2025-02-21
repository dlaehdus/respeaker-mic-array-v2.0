import pyaudio
import wave
import numpy as np

# 오디오 설정
RESPEAKER_RATE = 16000
RESPEAKER_CHANNELS = 4  # 4채널 오디오
RESPEAKER_WIDTH = 2  # 16비트 (2바이트)
CHUNK = 1024
RECORD_SECONDS = 15  # 녹음할 시간
WAVE_OUTPUT_FILENAME = "output_mixed.wav"  # 저장할 파일

# 장치 찾기
p = pyaudio.PyAudio()
device_index = None

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
        audio_data = np.frombuffer(data, dtype=np.int16)  
        
        # 4채널을 평균 내어 1채널로 변환
        mixed_data = np.mean(audio_data.reshape(-1, 4), axis=1).astype(np.int16)
        
        frames.append(mixed_data.tobytes())

    print("* Done recording")

    # 스트림 정리
    stream.stop_stream()
    stream.close()
    p.terminate()

    # WAV 파일 저장
    with wave.open(WAVE_OUTPUT_FILENAME, "wb") as wf:
        wf.setnchannels(1)  # 1채널 (모노)로 저장
        wf.setsampwidth(p.get_sample_size(p.get_format_from_width(RESPEAKER_WIDTH)))
        wf.setframerate(RESPEAKER_RATE)
        wf.writeframes(b"".join(frames))

    print(f"녹음 완료! {WAVE_OUTPUT_FILENAME} 저장됨")

except Exception as e:
    print(f"오류 발생: {e}")
    p.terminate()
