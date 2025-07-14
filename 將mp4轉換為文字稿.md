# 1.本機安裝 VLC 軟體，將mp4 轉換為 flac 音訊檔格式
	1.https://www.videolan.org/vlc/index.zh_TW.html 點[下載VLC]，下載完成後，安裝 [VLC撥放器]，
	
	2.打開VLC，點擊頂部菜單的「媒體」選項，然後選擇「轉換/儲存」，「開啟媒體」視窗中，點擊「+加入...」按鈕，選擇要轉換的 mp4 檔案。
	
	3.檔案添加完成後，點擊視窗下方的「轉換/儲存」按鈕，跳出[]視窗，點擊「設定檔」下拉選單，選擇「Audio - FLAC」作為輸出格式(下拉選單右邊有的[板手工具圖示按鈕]，按下後，選[音訊編解碼器]頁籤，建議可設定 聲道數:1，取樣率:22050。產生的檔案較小，之後轉換時間較短)。
	
	4.下方[目的檔案:]旁的「瀏覽」按鈕按下，選擇FLAC檔案的儲存位置，預設應該會跳出原來mp4檔案名(例如[test.mp4])，需設定副檔名.flac(例如[test.flac]，不然會覆蓋原來mp4檔案，或重新命名為新的檔名也可)，命名完成後，按[存檔]。 
	
	5.點擊下方「開始」按鈕，VLC 將開始轉換mp4檔案為 FLAC 格式。	


# 2.申請 Google Cloud 試用 (可用gmail帳號申請Google Cloud服務) 


# 3.本機安裝 gcloud CLI (Google Cloud SDK Shell)，並執行
	以下連結可下載安裝
	https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe


# 4.進入Google Cloud SDK Shell，輸入以下指令 >> 登入帳戶
		```
		gcloud auth login
		```
		(會跳出頁面 選擇 google 帳號)

# 5.在Google Cloud SDK Shell中，先切換到 放flac檔案的資料夾，方便以下步驟的指令操作
		指令範例(舉例 放[flac檔案的資料夾] 在 [D:\_speech>]): 
		```
			d:
			D:\>cd _speech
			D:\_speech>
		```

# 6. 設定專案 
		```
		gcloud config set project and-speech
		```
		(瀏覽器打開：https://console.cloud.google.com/cloud-resource-manager，可察看或建立 專案[and-speech](專案名稱可自訂) )


# 7. 建立 雲端儲存桶（如果還沒有）
		```
		gsutil mb -l asia-east1 gs://and-speech/(儲存桶名稱可自訂)
		```


# 8. 執行[上傳音訊檔&辨識語音轉文字]，會將步驟1所產生的flac檔，上傳到 雲端儲存桶 並 開始轉換文字，產生字幕檔
		```
		python upload2srt.py {flac檔名}
		```
		(例如: python upload2srt.py test.flac)

		備註:
		 	1.執行以上指令，需在 flac檔案的目錄中，如尚未切換目錄，可參考 步驟5 進行目錄切換，以上指令執行時，需等待一段時間，依據 flac 檔案大小，可能 10 分鐘到 1小時 左右，才能執行完畢。

			2.執行完畢，會在資料夾中產生 .srt 檔案(例如:test.srt)，這個檔案可複製到與原本的影片檔(例如[電學2-1.mp4])同一資料夾，與mp4放在一起後，用vlc撥放器播放mp4影片時，會自動套用字幕。
			
			3.[.srt]檔案，可以當作[文字檔案]開啟，直接看影片逐字稿。(若無法開啟，可另存 .txt 檔名後，再開啟)

 			4. Python 程式 使用 service account JSON 檔案登入:
				- 登入 Google Cloud 主控台 >> 選取[所建立的專案] >> 建立服務帳戶(授予此服務帳戶專案的存取權[腳色:Cloud Speech 管理員])
				- >> 回到 「服務帳戶」 頁面，您會看到剛才建立的服務帳戶。點擊該服務帳戶的電子郵件地址。點擊 「金鑰」 分頁。 「建立新的金鑰」。選擇 「JSON」 作為金鑰類型。





