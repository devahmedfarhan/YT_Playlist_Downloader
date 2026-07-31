import re
import os
import sys
from os.path import expanduser

import yt_dlp
try:
    import imageio_ffmpeg
    FFMPEG_PATH = imageio_ffmpeg.get_ffmpeg_exe()
except Exception:
    FFMPEG_PATH = None

def getDownloadDir():
    return os.path.join(expanduser("~"), "Downloads")

def askdirectory(initDir=""):
    try:
        from PyQt4 import QtGui
        dialog = QtGui.QFileDialog()
        dialog.setFileMode(QtGui.QFileDialog.Directory)
        if initDir == "":
            initDir = getDownloadDir()
        dialog.setDirectory(initDir)
        dialog.setOption(QtGui.QFileDialog.ShowDirsOnly)
        newPath = ""
        if dialog.exec_():
            newPath = dialog.selectedFiles()[0]
            print(newPath)
        return newPath
    except Exception:
        return getDownloadDir()

def getVideoDetails(pageURL):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'js_runtimes': {'node': {}}
    }
    if FFMPEG_PATH:
        ydl_opts['ffmpeg_location'] = FFMPEG_PATH

    det = []
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(pageURL, download=False)
            title = info.get('title', 'video')
            formats = info.get('formats', [])
            for fmt in formats:
                if fmt.get('vcodec') != 'none' or fmt.get('acodec') != 'none':
                    res = fmt.get('resolution') or f"{fmt.get('height', '720')}p"
                    ext = fmt.get('ext', 'mp4')
                    filesize = fmt.get('filesize') or fmt.get('filesize_approx') or 0
                    size_mb = int(round(filesize / 1024 / 1024)) if filesize else 0
                    fname = re.sub(r'[<>:\"\/\\|\?\*]+', "_", title) + "." + ext
                    det.append({
                        'url': fmt.get('url', pageURL),
                        'title': title,
                        'ext': ext,
                        'filename': fname,
                        'resolution': str(res),
                        'size': size_mb
                    })
    except Exception as e:
        print("Error getting video details:", e)
    return det

