import os
import sys
import shutil
import subprocess
from pathlib import Path

try:
    import yt_dlp
except ImportError:
    print('Install dependency: py -m pip install -U yt-dlp')
    input('Press Enter to exit...')
    raise SystemExit(1)

os.system('')
CYAN='\033[96m'; WHITE='\033[97m'; DIM='\033[90m'; GREEN='\033[92m'; RED='\033[91m'; RESET='\033[0m'; BOLD='\033[1m'

LOGO = r'''
███╗   ██╗██╗  ██╗ ██████╗ ███╗   ███╗
████╗  ██║██║  ██║██╔═══██╗████╗ ████║
██╔██╗ ██║███████║██║   ██║██╔████╔██║
██║╚██╗██║██╔══██║██║▄▄ ██║██║╚██╔╝██║
██║ ╚████║██║  ██║╚██████╔╝██║ ╚═╝ ██║
╚═╝  ╚═══╝╚═╝  ╚═╝ ╚══▀▀═╝ ╚═╝     ╚═╝'''

def desktop_path():
    home = Path.home()
    candidates = [home/'Desktop', home/'OneDrive'/'Desktop']
    for p in candidates:
        if p.is_dir(): return p
    if os.name == 'nt':
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders') as k:
                raw = winreg.QueryValueEx(k, 'Desktop')[0]
                p = Path(os.path.expandvars(raw))
                if p.is_dir(): return p
        except OSError: pass
    p = home/'Desktop'; p.mkdir(parents=True, exist_ok=True); return p

def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(CYAN+BOLD+LOGO+RESET)
    print(CYAN+'╔'+'═'*61+'╗')
    print('║'+WHITE+'  NHQM  /  MEDIA DOWNLOADER  /  ROOT CONSOLE'.ljust(61)+CYAN+'║')
    print('╠'+'═'*61+'╣')
    print('║'+DIM+'  [01] MP3  - Best available audio'.ljust(61)+CYAN+'║')
    print('║'+DIM+'  [02] MP4  - Full HD up to 1080p'.ljust(61)+CYAN+'║')
    print('╚'+'═'*61+'╝'+RESET)

def prompt(message):
    return input(f'\n{CYAN}<Root>@NHQM{RESET} {WHITE}{message}{RESET} ').strip()

def main():
    while True:
        banner()
        print(f'\n{DIM}  Save directory: {desktop_path()}{RESET}')
        url=prompt('Paste URL >')
        if url.lower() in ('q','quit','exit'): break
        if not url.startswith(('https://','http://')):
            print(RED+'[ERROR] Enter a valid URL.'+RESET); input('Press Enter...'); continue
        mode=prompt('Select [1] MP3 / [2] MP4 >')
        if mode not in ('1','2'):
            print(RED+'[ERROR] Choose 1 or 2.'+RESET); input('Press Enter...'); continue
        if not shutil.which('ffmpeg'):
            print(RED+'[ERROR] FFmpeg not found in PATH.'+RESET)
            print('Install: winget install --id Gyan.FFmpeg -e')
            input('Press Enter...'); continue
        folder=desktop_path()
        opts={
            'outtmpl': str(folder/'%(title).180B [%(id)s].%(ext)s'),
            'noplaylist': True,
            'windowsfilenames': True,
            'quiet': False,
            'no_warnings': False,
        }
        if mode=='1':
            opts.update({'format':'bestaudio/best','postprocessors':[{'key':'FFmpegExtractAudio','preferredcodec':'mp3','preferredquality':'192'}]})
        else:
            opts.update({'format':'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=1080]+bestaudio/best[height<=1080]','merge_output_format':'mp4','postprocessors':[{'key':'FFmpegVideoRemuxer','preferedformat':'mp4'}]})
        print(f'\n{CYAN}[NHQM] Starting download...{RESET}\n')
        try:
            with yt_dlp.YoutubeDL(opts) as ydl: ydl.download([url])
            print(f'\n{GREEN}[SUCCESS] Saved to: {folder}{RESET}')
        except Exception as e:
            print(f'\n{RED}[ERROR] {e}{RESET}')
        again=prompt('Download another? [Y/N] >').lower()
        if again not in ('y','yes',''): break

if __name__=='__main__':
    try: main()
    except KeyboardInterrupt: print('\n'+DIM+'[NHQM] Exiting...'+RESET)
