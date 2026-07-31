# 🚀 YDM Pro 3.0 — YouTube Playlist & Video Downloader

YDM Pro 3.0 is a modern, high-speed, dark-mode desktop application built for downloading YouTube Playlists and single videos in **4K, 2K, 1080p, 720p HD, or MP3 Audio**.

---

## 👤 Author & Developer
**Created & Developed by Dr Farhan Ahmed**

---

## 📦 Direct ZIP Download
Download the ready-to-run ZIP archive directly:
👉 **[Download YDM_Pro_3.0_Downloader.zip](https://github.com/devahmedfarhan/YT_Playlist_Downloader/raw/main/YDM_Pro_3.0_Downloader.zip)**

---

## ✨ Features

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

## 🛠️ Installation & Setup (One-time Setup)

Make sure you have **Python 3.8+** installed on your Windows machine.

Open Command Prompt or PowerShell in the project folder and run:

```powershell
pip install yt-dlp imageio-ffmpeg customtkinter
```

---

## 🚀 How to Start & Use the App (App Kaise Start Karein)

### Method 1: Graphical Desktop App (GUI)

Run the following command in Command Prompt / Terminal:

```powershell
python yListerFull.py
```

#### Step-by-Step Usage:
1. **Paste Playlist URL:** Enter any YouTube playlist link (e.g. `https://www.youtube.com/playlist?list=PLjMdlvowxr_0XqrqKSvbvcKd4562mnonS`).
2. **Choose Save Folder:** Click **`📂 Browse`** to select where to save downloaded files.
3. **Choose Format:** Select **`🎬 MP4 Video`** or **`🎵 MP3 Audio`**.
4. **Choose Quality:** Select **`🌟 Dynamic Max Quality (4K / 2K / 1080p)`** or **`720p HD`**.
5. **Click `🔍 Parse Playlist`:** Wait a few seconds until the playlist is scanned.
6. **Click `▶️ Start Batch Download`:** All videos in the playlist will download automatically one by one!

---

### Method 2: Command Line (CLI)

To parse and export playlist links via terminal:

```powershell
python ylister.py "YOUR_YOUTUBE_PLAYLIST_URL"
```

---

## 📋 Requirements
- Windows 10 / 11
- Python 3.8+
- Node.js (Installed for JS runtime decoding)
- Packages: `yt-dlp`, `imageio-ffmpeg`, `customtkinter`
