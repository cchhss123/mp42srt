# 上傳檔案 到 GCS(google雲端儲存:gs://your-storage)
import sys
import subprocess


def upload_to_gcs(file_path):
    """
    Uploads a file to Google Cloud Storage using gsutil.

    Args:
        file_path (str): The path to the file to upload.
    """
    if not file_path:
        print("錯誤：請提供檔案名稱。")
        print("用法: python upload_to_gcs.py <flac檔名>")
        return

    bucket_name = "your-storage"# 替換為你的 GCS(google雲端儲存:gs://your-storage)
    destination_blob_name = file_path

    # 將指令組合成一個字串，並在檔案路徑加上引號以處理包含空格的檔名
    command_str = f'gsutil cp "{file_path}" gs://{bucket_name}/{destination_blob_name}'

    try:
        print(f"正在執行指令: {command_str}")
        # 使用 shell=True，讓子進程可以找到在 shell 環境變數 PATH 中的 gsutil
        subprocess.run(command_str, check=True, shell=True)
        print(f"成功將 '{file_path}' 上傳到 'gs://{bucket_name}/{destination_blob_name}'")
    except FileNotFoundError:
        print("錯誤: 'gsutil' 指令未找到。請確認 Google Cloud SDK 已安裝並在您的 PATH 中。")
    except subprocess.CalledProcessError as e:
        print(f"上傳失敗，錯誤碼: {e.returncode}")
        print(f"錯誤訊息: {e.stderr}")
    except Exception as e:
        print(f"發生未預期的錯誤: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python upload_to_gcs.py <flac檔名>")
    else:
        flac_file_name = sys.argv[1]
        upload_to_gcs(flac_file_name)