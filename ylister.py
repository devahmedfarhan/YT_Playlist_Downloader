
# coding: utf-8
# Name: ylister.py
# Description: Parse URLs in Youtube Playlist using yt-dlp

import re
import sys
import time
import yt_dlp

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

def listParser(list_url):
    items, l = crawl(list_url)
    print(f"Found {l} videos. Please hold on...")
    with open("temp.html", "w", encoding="utf-8") as fHTML:
        for i, item in enumerate(items):
            fHTML.write(f"<a href='{item['url']}'>{item['title']}</a><br>\n")
            print(f"Done: {(i+1)*100/l:.2f} % - {item['title']}")
        
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('USAGE: python ylister.py YOUTUBE_URL')
        sys.exit(1)
    url = sys.argv[1]
    if 'http' not in url:
        url = 'http://' + url
    listParser(url)





