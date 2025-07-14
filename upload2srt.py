# 1.上傳檔案 到 GCS(google雲端儲存:gs://your-storage)
# 2.處理 google雲端儲存中的檔案，辨識出 文字結果
import os
import sys
import subprocess
from google.cloud import speech_v1p1beta1 as speech

# --- 上傳功能 ---
def upload_to_gcs(file_path):
    """使用 gsutil 將檔案上傳到 Google Cloud Storage。"""
    if not file_path:
        print("錯誤：請提供檔案名稱。")
        return False

    bucket_name = "your-storage"# 替換為你的 GCS(google雲端儲存:gs://your-storage)
    destination_blob_name = os.path.basename(file_path) # 確保只使用檔名

    command_str = f'gsutil cp "{file_path}" gs://{bucket_name}/{destination_blob_name}'

    try:
        print(f"正在執行上傳指令: {command_str}")
        # 使用 shell=True，讓子進程可以找到在 shell 環境變數 PATH 中的 gsutil
        # capture_output=True 和 text=True 可以捕獲輸出，方便偵錯
        result = subprocess.run(command_str, check=True, shell=True, capture_output=True, text=True)
        print(f"成功將 '{file_path}' 上傳到 'gs://{bucket_name}/{destination_blob_name}'")
        return True
    except subprocess.CalledProcessError as e:
        print(f"上傳失敗，錯誤碼: {e.returncode}")
        print(f"錯誤訊息: {e.stderr}")
        return False
    except Exception as e:
        print(f"發生未預期的錯誤: {e}")
        return False

# --- 語音轉文字與SRT生成功能 ---
def speech_to_srt(gcs_uri, output_filename):
    """對 GCS 上的音檔執行語音辨識並生成 SRT 檔案。"""
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(uri=gcs_uri)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
        language_code="zh-TW",
        enable_automatic_punctuation=True,
        enable_word_time_offsets=True
    )

    print("辨識中，請稍候...")
    operation = client.long_running_recognize(config=config, audio=audio)
    try:
        response = operation.result(timeout=5400) # 90分鐘超時
    except Exception as e:
        print(f"語音辨識失敗: {e}")
        return

    def format_timestamp(seconds):
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        ms = int((seconds - int(seconds)) * 1000)
        return f"{h:02}:{m:02}:{s:02},{ms:03}"

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

# --- 主程式 ---
if __name__ == "__main__":
    # 檢查命令列參數
    if len(sys.argv) < 2:
        print("用法: python upload2srt.py <本地flac檔名>")
        print("範例: python upload2srt.py my_audio.flac")
        sys.exit(1)

    local_file_path = sys.argv[1]
    
    # 設定 Google Cloud 憑證
    # 請確保 'your-key.json' 檔案與此腳本在同一個目錄下
    if not os.path.exists("your-key.json"):# 替換為你的金鑰檔案
        print("錯誤: 找不到 'your-key.json' 憑證檔案。")
        sys.exit(1)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "your-key.json"

    # --- 步驟 1: 上傳檔案到 GCS ---
    print(f"--- 步驟 1: 上傳檔案 '{local_file_path}' 到 GCS(google雲端儲存) ---")
    if not upload_to_gcs(local_file_path):
        print("檔案上傳失敗，中止執行。")
        sys.exit(1)

    # --- 步驟 2: 執行語音辨識並生成 SRT ---
    print(f"\n--- 步驟 2: 執行語音辨識 ---")
    file_name_only = os.path.basename(local_file_path)
    gcs_uri_for_speech = f"gs://your-storage/{file_name_only}"# 替換為你的 GCS(google雲端儲存:gs://your-storage)
    output_srt_filename = os.path.splitext(file_name_only)[0] + ".srt"
    
    speech_to_srt(gcs_uri_for_speech, output_srt_filename)