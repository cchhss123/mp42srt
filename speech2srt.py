# 處理 google雲端儲存中的檔案，辨識出 文字結果
from google.cloud import speech_v1p1beta1 as speech
import os
import sys

# 使用 service account JSON 檔案登入
# 登入 Google Cloud 主控台 >> 選取[所建立的專案] >> 建立服務帳戶(授予此服務帳戶專案的存取權[腳色:Cloud Speech 管理員])
# >> 回到 「服務帳戶」 頁面，您會看到剛才建立的服務帳戶。點擊該服務帳戶的電子郵件地址。點擊 「金鑰」 分頁。 「建立新的金鑰」。選擇 「JSON」 作為金鑰類型。
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "your-key.json"  # 替換為你的金鑰檔案

client = speech.SpeechClient()

# gsutil mb -l asia-east1 gs://and-speech/
# gsutil cp test.flac gs://and-speech/test.flac
# 從命令列參數獲取檔案名稱
if len(sys.argv) < 2:
    print("用法: python speech2srt.py <file-name>")
    print("範例: python speech2srt.py test.flac")
    sys.exit(1)
    
fileName = sys.argv[1]
gcs_uri = f"gs://your-storage/{fileName}"  # 替換為你的 GCS(google雲端儲存:gs://your-storage)

audio = speech.RecognitionAudio(uri=gcs_uri)

config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
    # sample_rate_hertz=16000,# 註解不設定 sample_rate_hertz，讓 API 自動偵測
    # audio_channel_count=2,   # 註解不設定，預設值為 1
    language_code="zh-TW",   # 根據您的語音語言調整
    enable_automatic_punctuation=True,
    enable_word_time_offsets=True  # 啟用單詞時間偏移，以獲取時間戳
)

operation = client.long_running_recognize(config=config, audio=audio)
print("辨識中，請稍候...")
# response = operation.result(timeout=600)
response = operation.result(timeout=5400)#如檔案較大，轉換時間建議30分鐘或更大，程式才不會time-out,目前設定90分鐘

def format_timestamp(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

output_filename = os.path.splitext(fileName)[0] + ".srt"
with open(output_filename, "w", encoding="utf-8") as srt_file:
    index = 1
    for result in response.results:
        alternative = result.alternatives[0]
        if not alternative.words:
            continue

        start_time = alternative.words[0].start_time.total_seconds()
        end_time = alternative.words[-1].end_time.total_seconds()
        text = alternative.transcript.strip()

        srt_file.write(f"{index}\n")
        srt_file.write(f"{format_timestamp(start_time)} --> {format_timestamp(end_time)}\n")
        srt_file.write(f"{text}\n\n")

        index += 1

print(f"完成！已輸出字幕檔 {output_filename}")

