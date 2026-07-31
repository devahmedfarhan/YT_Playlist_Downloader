# 🚀 YDM Pro 3.0 — YouTube Playlist & Video Downloader

YDM Pro 3.0 is a standalone, modern, high-speed dark-mode Windows desktop application (`YDM_Pro_3.0.exe`) built for downloading YouTube Playlists and single videos in **4K, 2K, 1080p, 720p HD, or MP3 Audio**.

---

## 👤 Author & Developer
**Created & Developed by Dr Farhan Ahmed**

---

## ⚡ Direct Executable Download (No Terminal / CMD Required!)

You do **NOT** need to open command prompt or install any Python packages! Simply download the package and double-click **`YDM_Pro_3.0.exe`** to open the GUI directly:

👉 **[Download YDM_Pro_3.0_Downloader.zip (Includes YDM_Pro_3.0.exe)](https://github.com/devahmedfarhan/YT_Playlist_Downloader/raw/main/YDM_Pro_3.0_Downloader.zip)**

---

## ✨ Key Features

- ⚡ **Standalone Windows Executable (`YDM_Pro_3.0.exe`):** Double-click to open UI directly — zero terminal setup required!
- 🌟 **Dynamic Max Quality (4K / 2K / 1080p / HD):** Automatically fetches the highest resolution available for every single video in a playlist.
- 🔄 **Automatic Full Playlist Batch Downloading:** Downloads the entire playlist sequentially from start to finish without pausing.
- 🎬 **Multi-Format Support:**
  - 🎥 **MP4 Video** (.mp4 - Default)
  - 🎵 **MP3 Audio** (.mp3 - Extract High-Quality Audio)
  - 📹 **MKV Video** (.mkv)
  - 🌐 **WEBM Video** (.webm)
  - 🔊 **M4A Audio** (.m4a)
- 🎨 **Modern Dark-Mode UI:** CustomTkinter interface with rounded cards, progress bars, and real-time status banners.
- 🛡️ **Anti-403 Forbidden Engine:** Built-in retries (`yt-dlp` + `imageio-ffmpeg`) for smooth uninterrupted downloads.
- 🚀 **Optional IDM Queue:** Support for Internet Download Manager (IDM) if desired, but **IDM is NOT required**.

---

## 🚀 How to Start & Use the App (App Kaise Start Karein)

### Option 1: Double-Click EXE (Recommended for Everyone)
1. Download & Extract **`YDM_Pro_3.0_Downloader.zip`**.
2. Double-click **`YDM_Pro_3.0.exe`**.
3. Paste Playlist URL -> Select Format/Quality -> Click **`Start Batch Download`**!

---

### Option 2: Run from Python Source (For Developers)

If running from Python source:

```powershell
pip install yt-dlp imageio-ffmpeg customtkinter
python yListerFull.py
```
