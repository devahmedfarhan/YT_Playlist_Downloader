# coding: utf-8

import re
import os
import sys
import subprocess 
from threading import Thread
import time 

import yt_dlp
try:
    import imageio_ffmpeg
    FFMPEG_PATH = imageio_ffmpeg.get_ffmpeg_exe()
except Exception:
    FFMPEG_PATH = None

try:
    import customtkinter as ctk
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
    HAS_CTK = True
except Exception:
    HAS_CTK = False
    import tkinter as tk
    from tkinter import ttk

FORMAT_OPTIONS = [
    "🎬 MP4 Video (.mp4)",
    "🎵 MP3 Audio (.mp3)",
    "📹 MKV Video (.mkv)",
    "🌐 WEBM Video (.webm)",
    "🔊 M4A Audio (.m4a)"
]

QUALITY_OPTIONS = [
    "🌟 Dynamic Max Quality (4K / 2K / 1080p)",
    "🎬 2160p 4K Ultra HD",
    "📺 1440p 2K QHD",
    "🖥️ 1080p Full HD",
    "📱 720p HD",
    "⚡ 480p SD",
    "⚡ 360p SD"
]

QUALITY_HEIGHT_MAP = {
    "🌟 Dynamic Max Quality (4K / 2K / 1080p)": 99999,
    "🎬 2160p 4K Ultra HD": 2160,
    "📺 1440p 2K QHD": 1440,
    "🖥️ 1080p Full HD": 1080,
    "📱 720p HD": 720,
    "⚡ 480p SD": 480,
    "⚡ 360p SD": 360
}

def crawl(url):
    ydl_opts = {
        'extract_flat': True,
        'skip_download': True,
        'quiet': True,
        'no_warnings': True,
        'js_runtimes': {'node': {}}
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        entries = info.get('entries', [])
        final_url = []
        for entry in entries:
            if entry:
                vid_id = entry.get('id')
                vid_title = entry.get('title', 'Video')
                v_url = entry.get('url') or f"https://www.youtube.com/watch?v={vid_id}"
                final_url.append({'url': v_url, 'title': vid_title, 'id': vid_id})
        return final_url, len(final_url)

# Global State
parsed_videos = []
is_downloading = False

if HAS_CTK:
    class YDMProApp(ctk.CTk):
        def __init__(self):
            super().__init__()

            self.title("YDM Pro 3.0 — Modern YouTube Playlist & Video Downloader")
            self.geometry("900 x 680")
            self.minsize(800, 600)

            # Header Frame
            self.header_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="#1E1E2E")
            self.header_frame.pack(fill="x", padx=20, pady=(15, 10))

            self.title_label = ctk.CTkLabel(
                self.header_frame, 
                text="🚀 YDM Pro 3.0", 
                font=ctk.CTkFont(size=24, weight="bold"),
                text_color="#89B4FA"
            )
            self.title_label.pack(anchor="w", padx=20, pady=(15, 2))

            self.subtitle_label = ctk.CTkLabel(
                self.header_frame, 
                text="High-Speed Batch YouTube Playlist & Video Downloader | 4K, 2K, 1080p & MP3", 
                font=ctk.CTkFont(size=12),
                text_color="#A6ADC8"
            )
            self.subtitle_label.pack(anchor="w", padx=20, pady=(0, 15))

            # Main Content Scrollable / Scroll Frame
            self.main_card = ctk.CTkFrame(self, corner_radius=15, fg_color="#181825")
            self.main_card.pack(fill="both", expand=True, padx=20, pady=10)

            # Section 1: Inputs Card
            self.inputs_frame = ctk.CTkFrame(self.main_card, corner_radius=10, fg_color="#1E1E2E")
            self.inputs_frame.pack(fill="x", padx=15, pady=15)

            # Playlist URL Row
            self.url_label = ctk.CTkLabel(self.inputs_frame, text="Playlist / Video URL:", font=ctk.CTkFont(weight="bold"))
            self.url_label.grid(row=0, column=0, sticky="w", padx=15, pady=(15, 5))
            
            self.url_entry = ctk.CTkEntry(
                self.inputs_frame, 
                placeholder_text="Paste YouTube Playlist URL here (e.g., https://www.youtube.com/playlist?list=...)", 
                height=38,
                corner_radius=8
            )
            self.url_entry.grid(row=0, column=1, columnspan=2, sticky="ew", padx=(0, 15), pady=(15, 5))

            # Save Path Row
            self.path_label = ctk.CTkLabel(self.inputs_frame, text="Save Folder:", font=ctk.CTkFont(weight="bold"))
            self.path_label.grid(row=1, column=0, sticky="w", padx=15, pady=(5, 15))

            default_save = os.path.join(os.path.expanduser("~"), "Downloads")
            self.path_entry = ctk.CTkEntry(self.inputs_frame, height=38, corner_radius=8)
            self.path_entry.insert(0, default_save)
            self.path_entry.grid(row=1, column=1, sticky="ew", padx=(0, 10), pady=(5, 15))

            self.browse_btn = ctk.CTkButton(
                self.inputs_frame, 
                text="📂 Browse", 
                width=110, 
                height=38, 
                corner_radius=8,
                fg_color="#313244",
                hover_color="#45475A",
                command=self.browse_folder
            )
            self.browse_btn.grid(row=1, column=2, sticky="e", padx=(0, 15), pady=(5, 15))

            self.inputs_frame.columnconfigure(1, weight=1)

            # Section 2: Options Card
            self.options_frame = ctk.CTkFrame(self.main_card, corner_radius=10, fg_color="#1E1E2E")
            self.options_frame.pack(fill="x", padx=15, pady=(0, 15))

            # Format Dropdown
            self.format_label = ctk.CTkLabel(self.options_frame, text="Format:", font=ctk.CTkFont(weight="bold"))
            self.format_label.grid(row=0, column=0, sticky="w", padx=15, pady=12)

            self.format_menu = ctk.CTkOptionMenu(
                self.options_frame, 
                values=FORMAT_OPTIONS,
                height=35,
                corner_radius=8,
                fg_color="#313244",
                button_color="#45475A",
                button_hover_color="#585B70"
            )
            self.format_menu.grid(row=0, column=1, sticky="w", padx=10, pady=12)

            # Quality Dropdown
            self.quality_label = ctk.CTkLabel(self.options_frame, text="Quality:", font=ctk.CTkFont(weight="bold"))
            self.quality_label.grid(row=0, column=2, sticky="w", padx=(20, 10), pady=12)

            self.quality_menu = ctk.CTkOptionMenu(
                self.options_frame, 
                values=QUALITY_OPTIONS,
                height=35,
                corner_radius=8,
                fg_color="#313244",
                button_color="#45475A",
                button_hover_color="#585B70"
            )
            self.quality_menu.grid(row=0, column=3, sticky="w", padx=10, pady=12)

            # IDM Toggle
            self.idm_chk = ctk.CTkCheckBox(
                self.options_frame, 
                text="Use IDM Queue (Optional)", 
                font=ctk.CTkFont(size=12),
                corner_radius=6
            )
            self.idm_chk.grid(row=0, column=4, sticky="e", padx=15, pady=12)

            self.options_frame.columnconfigure(4, weight=1)

            # Section 3: Action Buttons
            self.actions_frame = ctk.CTkFrame(self.main_card, corner_radius=10, fg_color="transparent")
            self.actions_frame.pack(fill="x", padx=15, pady=(0, 10))

            self.parse_btn = ctk.CTkButton(
                self.actions_frame, 
                text="🔍 Parse Playlist", 
                height=42, 
                corner_radius=10,
                font=ctk.CTkFont(size=14, weight="bold"),
                fg_color="#A6E3A1",
                text_color="#11111B",
                hover_color="#94E2D5",
                command=self.start_parse
            )
            self.parse_btn.pack(side="left", expand=True, fill="x", padx=(0, 5))

            self.download_btn = ctk.CTkButton(
                self.actions_frame, 
                text="▶️ Start Batch Download", 
                height=42, 
                corner_radius=10,
                font=ctk.CTkFont(size=14, weight="bold"),
                fg_color="#89B4FA",
                text_color="#11111B",
                hover_color="#B4BEFE",
                command=self.start_download
            )
            self.download_btn.pack(side="left", expand=True, fill="x", padx=5)

            self.stop_btn = ctk.CTkButton(
                self.actions_frame, 
                text="⏹️ Stop", 
                height=42, 
                corner_radius=10,
                font=ctk.CTkFont(size=14, weight="bold"),
                fg_color="#F38BA8",
                text_color="#11111B",
                hover_color="#EBA0AC",
                command=self.stop_download
            )
            self.stop_btn.pack(side="left", expand=True, fill="x", padx=(5, 0))

            # Section 4: Progress Bars & Status Dashboard
            self.dash_frame = ctk.CTkFrame(self.main_card, corner_radius=10, fg_color="#1E1E2E")
            self.dash_frame.pack(fill="x", padx=15, pady=10)

            # Parse Progress
            self.parse_prog_label = ctk.CTkLabel(self.dash_frame, text="Parse Progress:", font=ctk.CTkFont(size=12))
            self.parse_prog_label.pack(anchor="w", padx=15, pady=(12, 2))
            
            self.parse_bar = ctk.CTkProgressBar(self.dash_frame, height=10, corner_radius=5, progress_color="#A6E3A1")
            self.parse_bar.pack(fill="x", padx=15, pady=(0, 10))
            self.parse_bar.set(0)

            # Download Progress
            self.dl_prog_label = ctk.CTkLabel(self.dash_frame, text="Download Progress:", font=ctk.CTkFont(size=12))
            self.dl_prog_label.pack(anchor="w", padx=15, pady=(2, 2))
            
            self.dl_bar = ctk.CTkProgressBar(self.dash_frame, height=12, corner_radius=6, progress_color="#89B4FA")
            self.dl_bar.pack(fill="x", padx=15, pady=(0, 15))
            self.dl_bar.set(0)

            # Status Banner Badge
            self.status_badge = ctk.CTkFrame(self.main_card, corner_radius=8, fg_color="#313244")
            self.status_badge.pack(fill="x", padx=15, pady=(0, 15))

            self.status_label = ctk.CTkLabel(
                self.status_badge, 
                text="⚡ Ready. Paste a Playlist URL and click 'Parse Playlist'.", 
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color="#89B4FA"
            )
            self.status_label.pack(padx=15, pady=10)

        def browse_folder(self):
            folder = ctk.filedialog.askdirectory(initialdir=self.path_entry.get())
            if folder:
                self.path_entry.delete(0, "end")
                self.path_entry.insert(0, folder)

        def update_status(self, text, color="#89B4FA"):
            self.status_label.configure(text=text, text_color=color)

        def start_parse(self):
            url = self.url_entry.get().strip()
            if not url:
                self.update_status("⚠️ Please enter a valid YouTube Playlist URL!", "#F38BA8")
                return
            t = Thread(target=self.run_parse_thread, args=[url])
            t.daemon = True
            t.start()

        def run_parse_thread(self, url):
            global parsed_videos
            try:
                self.update_status("🔍 Parsing playlist videos using yt-dlp... Please wait.", "#FAB387")
                self.parse_bar.set(0.1)
                items, count = crawl(url)
                parsed_videos = items
                self.parse_bar.set(1.0)
                self.update_status(f"🎉 Parsing Complete! Found {count} videos in playlist. Click 'Start Batch Download'.", "#A6E3A1")
            except Exception as e:
                self.parse_bar.set(0)
                self.update_status(f"❌ Error parsing playlist: {str(e)}", "#F38BA8")

        def start_download(self):
            global is_downloading
            if is_downloading:
                self.update_status("⚠️ Download is already running!", "#FAB387")
                return

            if not parsed_videos:
                self.update_status("⚠️ No videos parsed yet! Please click 'Parse Playlist' first.", "#F38BA8")
                return

            target_dir = self.path_entry.get().strip()
            if not os.path.exists(target_dir):
                try:
                    os.makedirs(target_dir)
                except Exception as e:
                    self.update_status(f"❌ Invalid save path: {e}", "#F38BA8")
                    return

            fmt_choice = self.format_menu.get()
            q_choice = self.quality_menu.get()
            use_idm = bool(self.idm_chk.get())

            t = Thread(target=self.run_download_thread, args=[parsed_videos, target_dir, fmt_choice, q_choice, use_idm])
            t.daemon = True
            t.start()

        def run_download_thread(self, videos, target_dir, format_choice, quality_choice, use_idm):
            global is_downloading
            is_downloading = True
            total = len(videos)

            max_h = QUALITY_HEIGHT_MAP.get(quality_choice, 99999)

            if "MP3" in format_choice:
                fmt_str = "bestaudio/best"
                post_processors = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
                merge_fmt = None
            elif "M4A" in format_choice:
                fmt_str = "bestaudio[ext=m4a]/bestaudio/best"
                post_processors = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'm4a',
                }]
                merge_fmt = None
            elif "MKV" in format_choice:
                fmt_str = "bestvideo+bestaudio/best" if max_h >= 99999 else f"bestvideo[height<={max_h}]+bestaudio/best[height<={max_h}]"
                post_processors = []
                merge_fmt = "mkv"
            elif "WEBM" in format_choice:
                fmt_str = "bestvideo+bestaudio/best" if max_h >= 99999 else f"bestvideo[height<={max_h}][ext=webm]+bestaudio[ext=webm]/best[height<={max_h}][ext=webm]/best[height<={max_h}]"
                post_processors = []
                merge_fmt = "webm"
            else:  # Default MP4
                fmt_str = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" if max_h >= 99999 else f"bestvideo[height<={max_h}][ext=mp4]+bestaudio[ext=m4a]/best[height<={max_h}][ext=mp4]/best[height<={max_h}]"
                post_processors = []
                merge_fmt = "mp4"

            ydl_opts = {
                'format': fmt_str,
                'quiet': True,
                'no_warnings': True,
                'js_runtimes': {'node': {}},
                'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
                'retries': 10,
                'fragment_retries': 10,
                'file_access_retries': 10,
            }
            if FFMPEG_PATH:
                ydl_opts['ffmpeg_location'] = FFMPEG_PATH

            if post_processors:
                ydl_opts['postprocessors'] = post_processors

            if merge_fmt:
                ydl_opts['merge_output_format'] = merge_fmt

            idm_path = r"C:\Program Files (x86)\Internet Download Manager\IDMan.exe"
            has_idm = os.path.exists(idm_path)

            for idx, video in enumerate(videos):
                if not is_downloading:
                    self.update_status("🛑 Download stopped by user.", "#F38BA8")
                    break

                current_num = idx + 1
                video_title = video['title']
                self.update_status(f"⬇️ Downloading [{current_num}/{total}]: {video_title}", "#89B4FA")
                self.dl_bar.set((current_num - 1) / total)

                clean_title = re.sub(r'[<>:\"\/\\|\?\*]+', '_', video_title)

                if use_idm and has_idm:
                    fname = f"{clean_title}.mp4"
                    comm = f'"{idm_path}" /n /d "{video["url"]}" /p "{target_dir}" /f "{fname}"'
                    subprocess.Popen(comm)
                    time.sleep(0.5)
                else:
                    item_opts = dict(ydl_opts)
                    item_opts['outtmpl'] = os.path.join(target_dir, f"{clean_title}.%(ext)s")
                    try:
                        with yt_dlp.YoutubeDL(item_opts) as ydl:
                            ydl.download([video['url']])
                    except Exception as e:
                        print(f"Error downloading {video_title}: {e}")
                        if has_idm:
                            fname = f"{clean_title}.mp4"
                            comm = f'"{idm_path}" /n /d "{video["url"]}" /p "{target_dir}" /f "{fname}"'
                            subprocess.Popen(comm)

                self.dl_bar.set(current_num / total)

            if is_downloading:
                self.update_status(f"🎉 Success! All {total} items downloaded in {format_choice.split()[0]} format.", "#A6E3A1")
            is_downloading = False

        def stop_download(self):
            global is_downloading
            is_downloading = False
            self.update_status("🛑 Stopping download...", "#F38BA8")

    if __name__ == "__main__":
        app = YDMProApp()
        app.mainloop()

else:
    # Standard Tkinter Fallback if CustomTkinter unavailable
    print("CustomTkinter unavailable, using standard Tkinter fallback.")
