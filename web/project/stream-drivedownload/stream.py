#!/usr/bin/env python3
"""
ULTIMATE AUTO-STREAMING BOT (DRIVEDOWNLOADER EXCLUSIVE CORE)
Sniper Auto-Detect -> Drivedownloader API -> Extract 1080p Hotlink -> Stealth WatchParty -> Memory Quarantine (No File Deletion)
"""

import logging
import os
import re
import shutil
import subprocess
import sys
import time
import random
import json
import urllib.parse
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.keys import Keys
except ImportError:
    logging.error("Selenium belum terpasang. Pastikan Setup Environment berhasil.")
    sys.exit(1)

try:
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except:
    pass

try:
    import requests
except ImportError:
    requests = None

try:
    from webdriver_manager.chrome import ChromeDriverManager
except ImportError:
    ChromeDriverManager = None

# --- TARGET TUNGGAL DRIVEDOWNLOADER ---
DRIVE_API_URL = "https://drivedownloader.com/api/drive"
# Prefix server streaming langsung berdasarkan penemuan DevTools
STREAM_PREFIX = "https://fx5jl.drivedownloader.com/?video_id="
ROOM_URL = "https://www.watchparty.me/watch/fantastic-receipt-move"

MAX_FILE_SIZE_GB = 15.0
SEARCH_DIR = '/content/drive/MyDrive/'
MIN_MOVIE_SIZE_MB = 50.0  


def find_chrome_binary():
    candidates = [
        'google-chrome', 'google-chrome-stable', 'chromium', 'chromium-browser',
        '/usr/bin/google-chrome', '/usr/bin/google-chrome-stable', '/usr/bin/chromium',
        '/usr/bin/chromium-browser', '/snap/bin/chromium', '/opt/google/chrome/chrome',
    ]
    for candidate in candidates:
        which_result = shutil.which(candidate)
        if which_result and os.path.exists(which_result):
            return which_result
    for candidate in candidates:
        if os.path.exists(candidate) and os.path.isfile(candidate):
            return candidate
    return None

def build_driver(proxy_server=None):
    options = Options()
    
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--mute-audio')
    options.add_argument('--window-size=1920,1080')
    
    # --- LOGIKA TINGKAT TINGGI: WEBRTC LEAK KILLER ---
    prefs = {
        "profile.default_content_setting_values.webrtc_multiple_routes_enable": 0,
        "webrtc.ip_handling_policy": "disable_non_proxied_udp",
        "webrtc.multiple_routes_enabled": False,
        "webrtc.nonproxied_udp_enabled": False
    }
    options.add_experimental_option("prefs", prefs)
    options.add_argument('--disable-webrtc')

    if proxy_server:
        options.add_argument(f'--proxy-server=http://{proxy_server}')
        logging.info(f"🛡️ Menjalankan Browser dengan IP Proxy Publik: {proxy_server}")

    # --- LOGIKA TINGKAT TINGGI: STEALTH MODE ANTI-BOT ---
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    chrome_path = find_chrome_binary()
    if chrome_path:
        options.binary_location = chrome_path

    try:
        driver_path = ChromeDriverManager().install()
    except Exception:
        driver_path = shutil.which('chromedriver')

    if not driver_path:
        raise FileNotFoundError('chromedriver tidak ditemukan.')

    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    
    # --- LOGIKA TINGKAT TINGGI: BIOMETRIC & HARDWARE SPOOFING (CDP) ---
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': '''
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
            Object.defineProperty(navigator, 'languages', { get: () => ['id-ID', 'id', 'en-US', 'en'] });
            window.chrome = { runtime: {} };
            
            const getParameter = WebGLRenderingContext.prototype.getParameter;
            WebGLRenderingContext.prototype.getParameter = function(parameter) {
                if (parameter === 37445) return 'Intel Inc.';
                if (parameter === 37446) return 'Intel(R) Iris(R) Xe Graphics';
                return getParameter.apply(this, arguments);
            };
        '''
    })

    driver.set_script_timeout(600)
    driver.implicitly_wait(10)
    
    return driver

def check_google_drive() -> bool:
    if not Path('/content/drive').exists():
        logging.error('Google Drive belum dimount. Mount terlebih dahulu.')
        return False
    return True

def get_safe_proxy(exclude_list):
    if requests is None:
        return None
    logging.info('🔄 [ANTI-BLOKIR] Mencari daftar IP Proxy Elite dari server global...')
    api_url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=5000&country=all&ssl=yes&anonymity=elite"
    try:
        res = requests.get(api_url, timeout=10)
        proxies = res.text.strip().split('\r\n')
        if not proxies or not proxies[0]:
            return None
            
        valid_proxies = [p for p in proxies if p not in exclude_list and len(p.split(':')) == 2]
        random.shuffle(valid_proxies)
        
        logging.info(f'✅ Mendapatkan {len(valid_proxies)} IP Proxy baru. Menguji koneksi...')
        
        for proxy in valid_proxies[:15]: 
            try:
                proxies_dict = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
                test = requests.get("https://drivedownloader.com", proxies=proxies_dict, timeout=5)
                if test.status_code == 200:
                    logging.info(f'✅ IP Aman Ditemukan dan Valid: {proxy}')
                    return proxy
            except:
                continue
    except Exception as e:
        logging.error(f"Gagal mengambil proxy: {e}")
    return None

# =========================================================================================
# --- INTI UTAMA: DRIVEDOWNLOADER API & HOTLINK GENERATOR ---
# =========================================================================================
def process_drivedownloader_api(file_path: str, proxy_ip=None, is_proxy=False) -> str | None:
    logging.info(f'🚀 [CORE API] Menghubungkan file ke Drivedownloader Gateway ({DRIVE_API_URL})...')
    
    file_name = Path(file_path).name
    # Mengamankan nama file agar aman dimasukkan ke dalam URL (URL Encoding)
    encoded_filename = urllib.parse.quote(file_name)
    
    curl_command = [
        "curl", "-s", "-X", "POST", DRIVE_API_URL,
        "-F", f"file=@{file_path}",
        "-H", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "-H", "Referer: https://drivedownloader.com/",
        "--ipv4",                          
        "--connect-timeout", "15",         
        "--speed-time", "20",              
        "--speed-limit", "50000"          
    ]
    
    if is_proxy:
        curl_command.extend(["--max-time", "900"])
    else:
        curl_command.extend(["--max-time", "7200"])
        
    if proxy_ip:
        curl_command.extend(["-x", f"http://{proxy_ip}"])
        logging.info(f'🛡️ Menembus blokir menggunakan Proxy: {proxy_ip}')
        
    logging.info('Proses Gateway sedang berjalan, mendeteksi Video ID...')
    
    try:
        result = subprocess.run(curl_command, capture_output=True, text=True, timeout=7250)
        raw_output = result.stdout.strip()
        
        if not raw_output or any(err in raw_output.lower() for err in ["502 bad gateway", "503 service", "504 gateway", "521 web server", "522 connection"]):
            return "PROXY_DEAD" if proxy_ip else "SERVER_DOWN"
            
        if "403 forbidden" in raw_output.lower() or "<html" in raw_output.lower():
            return "403_BLOCKED"
            
        # --- LOGIKA TINGKAT DEWA: EKSTRAKSI & PERAKITAN HOTLINK 1080P ---
        video_id = None
        
        # Sapu Jagat 1: Mencari parameter video_id resmi di respon JSON/HTML
        match_id = re.search(r'"(?:video_id|id|file_id|fileId)"\s*:\s*"([a-zA-Z0-9_-]{25,35})"', raw_output)
        if match_id:
            video_id = match_id.group(1)
            
        # Sapu Jagat 2: Mencari langsung URL yang dikembalikan
        match_url = re.search(r'(https://[a-zA-Z0-9_-]+\.drivedownloader\.com/\?video_id=[a-zA-Z0-9_-]+)', raw_output)
        if match_url and not video_id:
            raw_url = match_url.group(1)
            video_id_match = re.search(r'video_id=([a-zA-Z0-9_-]+)', raw_url)
            if video_id_match:
                video_id = video_id_match.group(1)
            
        # Sapu Jagat 3: Ekstraksi Paksa Google Drive ID (33 karakter standar)
        match_any_id = re.search(r'([a-zA-Z0-9_-]{28,35})', raw_output)
        if match_any_id and not video_id:
            video_id = match_any_id.group(1)

        if video_id:
            # Merakit Hotlink Super persis seperti penelusuran DevTools Anda
            hotlink = f"{STREAM_PREFIX}{video_id}&location=SIN&quality=1080&action=download_direct&filename={encoded_filename}"
            logging.info(f"✅ Drivedownloader Berhasil! Merakit Direct Hotlink 1080p: {hotlink[:70]}...")
            return hotlink

        logging.error(f"❌ Drivedownloader menolak/gagal memproses. Respons: {raw_output[:150]}")
        return None
            
    except subprocess.TimeoutExpired:
        return "PROXY_DEAD"
    except Exception as exc:
        logging.error(f'Kesalahan kritis saat eksekusi Drivedownloader: {exc}')
        
    return None

def execute_drivedownloader_pipeline(file_path: str) -> str | None:
    """Manajer Kaskade khusus untuk Drivedownloader"""
    file_size_mb = Path(file_path).stat().st_size / (1024 * 1024)
    
    # 1. Coba koneksi langsung tanpa proxy (Tercepat)
    link = process_drivedownloader_api(file_path, proxy_ip=None, is_proxy=False)
    
    if link == "SERVER_DOWN":
        logging.error("🚨 API Drivedownloader sedang MATI TOTAL / MAINTENANCE.")
        return None
        
    if link == "403_BLOCKED":
        logging.warning("⚠️ Drivedownloader memblokir IP Datacenter Google Colab kita.")
        
        # SMART SIZE BYPASS: Mencegah proxy nyangkut pada file di atas 250MB
        if file_size_mb > 250:
            logging.error(f"🛑 File ini berukuran Raksasa ({file_size_mb:.2f} MB).")
            logging.error("⚡ Menggunakan Proxy Publik gratis untuk ukuran sebesar ini akan menyebabkan Stuck/Macet.")
            logging.error("⚠️ Operasi Drivedownloader DIBATALKAN untuk mencegah Colab hang.")
            return None
            
        logging.warning("Mengaktifkan Proxy Rotator untuk mencoba menembus blokir...")
        used_proxies = set()
        
        for attempt in range(3): 
            logging.info(f"\n🔄 --- MENGAKTIFKAN PROXY DRIVEDOWNLOADER KE-{attempt + 1} ---")
            safe_proxy = get_safe_proxy(exclude_list=used_proxies)
            if not safe_proxy: break
            used_proxies.add(safe_proxy) 
            
            proxy_link = process_drivedownloader_api(file_path, proxy_ip=safe_proxy, is_proxy=True)
            
            if proxy_link == "SERVER_DOWN":
                logging.error("🚨 Proxy membuktikan Server Drivedownloader MATI TOTAL!")
                return None
            if proxy_link and proxy_link not in ["403_BLOCKED", "SERVER_DOWN", "PROXY_DEAD"]:
                return proxy_link
                
        logging.error("❌ Seluruh Proxy gagal menembus perlindungan Drivedownloader.")
        return None
        
    elif link and link not in ["PROXY_DEAD"]:
        return link
        
    return None

def play_on_watchparty(video_link: str, room_url: str):
    logging.info('\n🤖 [AUTO-PLAY] Menghubungkan ke WatchParty Room via Stealth Browser...')
    driver = None
    try:
        driver = build_driver() 
        driver.get(room_url)
        wait = WebDriverWait(driver, 20)

        logging.info('🔍 Mencari kolom input URL...')
        input_selector = "input[placeholder*='Enter video file URL']"
        input_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, input_selector)))
        
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, input_selector)))

        logging.info('🧹 Membersihkan kolom input (React Bypass)...')
        input_box.send_keys(Keys.CONTROL, 'a')
        input_box.send_keys(Keys.BACKSPACE)
        time.sleep(0.5)

        logging.info('🔗 Memasukkan tautan Drivedownloader dan menekan ENTER...')
        input_box.send_keys(video_link)
        time.sleep(0.5)
        input_box.send_keys(Keys.ENTER)

        logging.info('🎬 SUKSES! Video 1080p diputar di WatchParty. Bot keluar dari room...')
        time.sleep(3) 

    except Exception as exc:
        logging.error('Gagal memutar video di WatchParty: %s', exc)
    finally:
        if driver:
            driver.quit()

# --- LOGIKA TINGKAT TINGGI: AUTO DETECTOR (NO-DELETE MEMORY) ---
def wait_for_new_movie(search_dir: str, processed_files: set) -> Path:
    print(f"\n📡 SNIPER MODE AKTIF: Memantau folder Google Drive secara Real-Time...")
    print(f"   (Mengabaikan video < {MIN_MOVIE_SIZE_MB} MB dan {len(processed_files)} file yang sudah tayang di WatchParty)")
    
    while True:
        valid_movies = []
        for root, _, files in os.walk(search_dir):
            for file in files:
                # LOGIKA PENTING: Hanya memproses file yang belum ada di 'processed_files' memory
                if file.lower().endswith('.mp4') and file not in processed_files:
                    path = Path(root) / file
                    try:
                        size_mb = path.stat().st_size / (1024 * 1024)
                        if size_mb > MIN_MOVIE_SIZE_MB and size_mb <= (MAX_FILE_SIZE_GB * 1024):
                            valid_movies.append(path)
                    except:
                        pass
        
        if valid_movies:
            newest_movie = sorted(valid_movies, key=lambda f: f.stat().st_mtime, reverse=True)[0]
            
            print(f"\n🔔 FILM BARU TERDETEKSI: {newest_movie.name} ({newest_movie.stat().st_size / (1024*1024):.2f} MB)")
            print("   Memastikan proses Save/Download ke Google Drive selesai 100%...")
            
            last_size = -1
            while True:
                time.sleep(3)
                try:
                    current_size = newest_movie.stat().st_size
                    if current_size == last_size and current_size > 0:
                        break
                    last_size = current_size
                except Exception as e:
                    pass
                
            print("✅ File sudah stabil di Drive dan siap dikonversi ke Hotlink!\n")
            return newest_movie
            
        time.sleep(5)

def main():
    if not check_google_drive():
        sys.exit(1)

    print("\n" + "="*65)
    print("🚀 DRIVEDOWNLOADER EXCLUSIVE BOT (WATCHPARTY DAEMON)")
    print("   (Drive -> Drivedownloader API 1080p -> WatchParty)")
    print("="*65)
    
    # Memori untuk menyimpan nama file yang sudah diproses agar tidak diulang (Karena file TIDAK dihapus)
    processed_memory = set()
    
    # SIKLUS TAK TERBATAS (ALWAYS-ON DAEMON)
    while True:
        try:
            # 1. Tunggu dan deteksi film baru otomatis (Mengabaikan file yang ada di memori)
            file_path = wait_for_new_movie(SEARCH_DIR, processed_memory)
            
            # 2. Eksekusi API Drivedownloader
            link = execute_drivedownloader_pipeline(str(file_path))
            
            # WatchParty mendukung link mp4 mentah atau proxy URL seperti fx5jl.drivedownloader...
            if link and ('drivedownloader' in link or 'video_id=' in link):
                print('\n🎉 KONVERSI BERHASIL (Mendapatkan Tautan Direct Stream 1080p)!')
                print(f'📥 Tautan Stream: {link}')
                
                # 3. Putar di WatchParty
                play_on_watchparty(link, ROOM_URL)
                
                # 4. MEMASUKKAN KE MEMORI (TIDAK ADA PENGHAPUSAN FILE)
                print(f'\n🛡️ Sistem Keamanan Aktif: File "{file_path.name}" DIBIARKAN utuh di Google Drive.')
                print('   (Menghapus file ini akan menyebabkan link Drivedownloader di WatchParty mati seketika).')
                
                # Masukkan ke memori agar Sniper Mode mengabaikannya di pemindaian berikutnya
                processed_memory.add(file_path.name)
                print('✅ File masuk ke dalam memori. Siklus eksekusi selesai dengan sempurna!')
                
            else:
                print('\n❌ Gagal memproses file ke Drivedownloader.')
                print('⚠️ File akan dimasukkan ke Karantina agar bot tidak macet berulang-ulang.')
                processed_memory.add(file_path.name)
                
            print("\n" + "-"*65)
            print("🔄 Kembali ke Mode Pemantauan (Menunggu film baru masuk ke Drive)...")
            
        except KeyboardInterrupt:
            print("\n🛑 Bot dihentikan secara manual oleh pengguna.")
            sys.exit(0)
        except Exception as e:
            logging.error(f"Terjadi kesalahan pada siklus utama: {e}")
            time.sleep(5)

if __name__ == '__main__':
    main()
