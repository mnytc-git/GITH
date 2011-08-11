import logging
import os
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
import hashlib
import json
from pathlib import Path
import shutil

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

# --- DEPENDENSI WAJIB ---
try:
    import internetarchive as ia
except ImportError:
    logging.error("❌ Library 'internetarchive' belum terpasang.")
    sys.exit(1)

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.action_chains import ActionChains
except ImportError:
    logging.error("Selenium belum terpasang.")
    sys.exit(1)

try:
    from webdriver_manager.chrome import ChromeDriverManager
except ImportError:
    ChromeDriverManager = None

# --- TARGET TUNGGAL & KONFIGURASI DRIVE ---
ROOM_URL = "https://www.watchparty.me/watch/fantastic-receipt-move"
MAX_FILE_SIZE_GB = 15.0
SEARCH_DIR = '/content/drive/MyDrive/'
MIN_MOVIE_SIZE_MB = 50.0  

# =========================================================================
# 👑 KUNCI RAHASIA KRIPTOGRAFI, GHOST MEMORY & DATABASE LINK
# =========================================================================
SECRET_SALT = "MNYTC_GHOST_PROTOCOL_"
GHOST_MEMORY = set() 
IA_PASSWORD = "6@EgrCFJRdynJqG"
DATABASE_FILE = Path('/content/drive/MyDrive/MNYTC_DATABASE_LINKS.txt')
ACCOUNT_STATE_FILE = Path('/content/drive/MyDrive/mnytc_account_state.txt')
IP_HISTORY_FILE = Path('/content/drive/MyDrive/MNYTC_IP_HISTORY.json')

# =========================================================================
# 👑 THE DATABASE BYPASS READER
# =========================================================================
def check_if_already_uploaded(slug_name: str) -> str | None:
    if not DATABASE_FILE.exists():
        return None
    try:
        with open(DATABASE_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if slug_name in line:
                    parts = line.strip().split(' | ')
                    if len(parts) >= 4:
                        return parts[3].strip() 
    except Exception as e:
        logging.error(f"Gagal membaca database Drive: {e}")
    return None

# =========================================================================
# 👑 THE IP LEDGER: RADAR & PRE-EMPTIVE KAMIKAZE
# =========================================================================
COOLDOWN_HOURS = 12
COOLDOWN_SECONDS = COOLDOWN_HOURS * 3600

def get_current_ip():
    try:
        return subprocess.check_output(["curl", "-s", "--max-time", "5", "https://api.ipify.org"]).decode().strip()
    except:
        return "Unknown"

def load_ip_history():
    if IP_HISTORY_FILE.exists():
        try:
            with open(IP_HISTORY_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_ip_history(history_dict):
    try:
        with open(IP_HISTORY_FILE, 'w') as f:
            json.dump(history_dict, f, indent=4)
    except Exception as e:
        logging.error(f"Gagal menyimpan histori IP: {e}")

def trigger_kernel_panic(reason: str):
    print("\n" + "💥"*40)
    print(f"🚨 [AUTO-DELETE RUNTIME DIINISIASI]")
    print(f"{reason}")
    print("Memerintahkan Server Google Colab untuk menghancurkan Virtual Machine ini.")
    print("Layar ini akan terputus dalam 3 detik...")
    print("💥"*40 + "\n")
    time.sleep(3)
    
    try:
        from google.colab import runtime
        runtime.unassign() 
    except Exception as e:
        logging.warning("Jalur API Colab terblokir. Menggunakan Eksekusi OS tingkat akar...")
        os.system("kill -9 -1")
        sys.exit(0)

def verify_ip_status_and_enforce():
    ip = get_current_ip()
    print("\n" + "="*80)
    print("🌐 [NETWORK RADAR - ANALISIS IP & COOLDOWN]")
    print(f"   ► IP Native Colab : {ip}")
    
    if ip == "Unknown":
        print("   ► Status : Gagal mengecek IP, mengaktifkan mode bypass.")
        print("="*80 + "\n")
        return ip
        
    history = load_ip_history()
    if ip in history:
        last_used = history[ip]
        elapsed = time.time() - last_used
        
        if elapsed < COOLDOWN_SECONDS:
            remaining = COOLDOWN_SECONDS - elapsed
            hours = int(remaining // 3600)
            minutes = int((remaining % 3600) // 60)
            last_used_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_used))
            
            print(f"   ► Status : ⚠️ IP KOTOR! IP ini belum di-refresh oleh Archive.org.")
            print(f"   ► Terakhir Dipakai : {last_used_str}")
            print(f"   ► Sisa Waktu Pembersihan : {hours} Jam {minutes} Menit")
            print("="*80)
            
            # 👑 THE PRE-EMPTIVE KAMIKAZE (LEDAKKAN JIKA IP KOTOR)
            trigger_kernel_panic("IP YANG DIBERIKAN GOOGLE ADALAH IP KOTOR (BEKAS)!")
        else:
            print(f"   ► Status : ✅ IP BERSIH (Masa pendinginan {COOLDOWN_HOURS} jam telah terlewati).")
    else:
        print("   ► Status : ✨ IP BARU (Belum pernah tercatat di Database Drive Anda).")
        
    print("="*80 + "\n")
    return ip

def mark_ip_as_used(ip):
    if ip and ip != "Unknown":
        history = load_ip_history()
        history[ip] = time.time()
        save_ip_history(history)
        logging.info(f"📝 [IP LEDGER] Alamat IP {ip} telah dikunci selama {COOLDOWN_HOURS} jam ke depan.")

# =========================================================================
# 👑 DATABASE LOGGER
# =========================================================================
def log_success_upload(original_name, slug_name, cf_link, archive_link):
    try:
        is_new = not DATABASE_FILE.exists()
        with open(DATABASE_FILE, 'a', encoding='utf-8') as f:
            if is_new:
                f.write("Waktu Upload | Nama Asli | Judul Bersih | Link Cloudflare Premium | Link Rahasia Archive\n")
            waktu = time.strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"{waktu} | {original_name} | {slug_name} | {cf_link} | {archive_link}\n")
    except Exception as e:
        logging.error(f"⚠️ Gagal mencatat log ke Google Drive: {e}")

# =========================================================================
# 👑 PERSISTENT ACCOUNT QUEUE (MURNI ROUND-ROBIN)
# =========================================================================
def get_next_account() -> str:
    default_accounts = [
        "4qimfhr5v@mozmail.com", "uk0db6tar@mozmail.com", "ai6i9xoo0@mozmail.com",
        "fm5xggfvd@mozmail.com", "rykywrpqo@mozmail.com", "remvw7098@mozmail.com",
        "z43vmsef9@mozmail.com", "aet5gsshv@mozmail.com", "fz2j67v84@mozmail.com",
        "yam9hg1yw@mozmail.com"
    ]
    accounts = default_accounts.copy()
    if ACCOUNT_STATE_FILE.exists():
        with open(ACCOUNT_STATE_FILE, 'r') as f:
            saved_accounts = [line.strip() for line in f.readlines() if line.strip()]
        if len(saved_accounts) == len(default_accounts):
            accounts = saved_accounts
            
    active_account = accounts.pop(0)
    accounts.append(active_account)
    
    with open(ACCOUNT_STATE_FILE, 'w') as f:
        for acc in accounts:
            f.write(f"{acc}\n")
    return active_account

# =========================================================================
# 👑 SETUP SELENIUM CHROME
# =========================================================================
def find_chrome_binary():
    candidates = ['google-chrome', 'google-chrome-stable', 'chromium', 'chromium-browser', '/usr/bin/google-chrome', '/opt/google/chrome/chrome']
    for candidate in candidates:
        which_result = shutil.which(candidate)
        if which_result and os.path.exists(which_result): return which_result
    return None

def build_driver(proxy_server=None):
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--mute-audio')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-extensions')
    options.add_argument('--js-flags=--max-old-space-size=1024') 
    options.add_argument('--blink-settings=imagesEnabled=false') 
    prefs = {"profile.default_content_setting_values.webrtc_multiple_routes_enable": 0, "webrtc.ip_handling_policy": "disable_non_proxied_udp"}
    options.add_experimental_option("prefs", prefs)
    options.add_argument('--disable-webrtc')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    chrome_path = find_chrome_binary()
    if chrome_path: options.binary_location = chrome_path

    try: driver_path = ChromeDriverManager().install()
    except Exception: driver_path = shutil.which('chromedriver')
    if not driver_path: raise FileNotFoundError('chromedriver tidak ditemukan.')

    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': '''Object.defineProperty(navigator, 'webdriver', { get: () => undefined });'''
    })
    driver.set_script_timeout(600)
    driver.implicitly_wait(10)
    return driver

def check_google_drive() -> bool:
    if not Path('/content/drive').exists():
        logging.error('Google Drive belum dimount. Mount terlebih dahulu.')
        return False
    return True

# =========================================================================
# 👑 THE SMART SLUGIFIER
# =========================================================================
def sanitize_movie_title(original_name: str) -> str:
    name = original_name
    name = re.sub(r'(?i)^(lk21.*?de-|lk21-?)', '', name)
    name = re.sub(r'(?i)-?(1080p|720p|480p|360p|web-dl|bluray|hdrip|brrip|cam)', '', name)
    name = re.sub(r'\s*\(\d{1,2}\)\s*(?=\.mp4$)', '', name) 
    name = name.replace('.mp4', '')
    name = re.sub(r'[^a-zA-Z0-9]+', '-', name)
    name = name.strip('-').lower()
    return name + '.mp4'

# =========================================================================
# 👑 THE DIRECTORY SCRAPER RADAR
# =========================================================================
def check_file_ready_direct(bucket_code: str, physical_file_name: str, max_wait_minutes=10) -> bool:
    logging.info(f"\n📡 [DIRECTORY SCRAPER PING] Mengintip langsung ke halaman direktori Archive.org...")
    target_url = f"https://archive.org/download/{bucket_code}/"
    start_time = time.time()
    max_wait_seconds = max_wait_minutes * 60

    while time.time() - start_time < max_wait_seconds:
        try:
            req = urllib.request.Request(target_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            with urllib.request.urlopen(req, timeout=10) as response:
                html_content = response.read().decode('utf-8')
                if physical_file_name in html_content:
                    print("\n")
                    return True
        except urllib.error.HTTPError: pass
        except Exception: pass
            
        elapsed = int(time.time() - start_time)
        sys.stdout.write(f"\r⚡ Menunggu direktori memunculkan nama file... ({elapsed} detik berlalu) ")
        sys.stdout.flush()
        time.sleep(3) 
        
    print("\n")
    return False

# =========================================================================
# 👑 INTI UTAMA: THE S3 HTTPS cURL ENGINE (100% NATIVE MURNI)
# =========================================================================
def upload_archive_s3_curl(original_drive_path: Path, clean_title_with_ext: str, bucket_code: str, active_account: str) -> str | int | None:
    logging.info(f"\n🚀 [INTERNET ARCHIVE S3] Mengeksekusi Upload MURNI dari Google Drive...")
    
    physical_file_name = f"{bucket_code}.mp4" 
    identifier = bucket_code 
    
    try:
        ia.configure(active_account, IA_PASSWORD)
        session = ia.get_session()
        access_key = session.access_key
        secret_key = session.secret_key
        if not access_key: return None
    except: return None

    s3_url = f"https://s3.us.archive.org/{identifier}/{physical_file_name}"
    
    curl_command = [
        "curl", "--progress-bar", "-w", "\n%{http_code}", "--http1.1", 
        "-T", str(original_drive_path), s3_url,
        "-H", f"authorization: LOW {access_key}:{secret_key}",
        "-H", "x-amz-auto-make-bucket: 1",
        "-H", "x-archive-queue-derive: 0", 
        "-H", f"x-archive-meta-title: {bucket_code}", 
        "-H", "x-archive-meta-mediatype: data", 
        "-H", "x-archive-meta-collection: opensource_media",
        "-H", "x-archive-meta-subject: tmp", 
        "-H", "x-archive-meta-description: null",
        "-H", "Expect:", 
        "--tcp-nodelay", "--tcp-fastopen", "--connect-timeout", "60", "--max-time", "14400",             
        "--retry", "5", "--retry-delay", "5", "--retry-all-errors"               
    ]
    
    logging.info("⏳ Web Socket S3 terbuka! Mengalirkan data dengan kecepatan Colab Native...")
    logging.info("⚡ MENAMPILKAN LIVE PROGRESS BAR:\n")
    
    try:
        result = subprocess.run(curl_command, stdout=subprocess.PIPE, stderr=sys.stdout, text=True)
        http_code = "000"
        if result.stdout.strip():
            http_code = result.stdout.strip().split('\n')[-1]
            
        if http_code in ["200", "201", "202"]:
            # 👑 DOMAIN BARU: MENGGUNAKAN DEVS.SURF! 👑
            masked_link = f"https://git.mnytc.eu/{urllib.parse.quote(clean_title_with_ext)}"
            archive_direct_link = f"https://archive.org/details/{identifier}"
            
            logging.info(f"✅ Transmisi S3 Selesai! (HTTP Code: {http_code})")
            logging.info(f"🕵️‍♂️ [SECRET ARCHIVE LINK] {archive_direct_link}")
            
            is_ready = check_file_ready_direct(bucket_code, physical_file_name, max_wait_minutes=10)
            if is_ready: logging.info("✅ RADAR HIJAU! File telah terlihat di direktori publik Archive. Jalan!")
            else: logging.warning("⚠️ Radar Timeout! Memaksa jalan...")
                
            time.sleep(3) 
            logging.info(f"🎭 [CLOUDFLARE ROOT URL] Tautan Premium disiapkan: {urllib.parse.unquote(masked_link)}")
            return masked_link
        
        elif http_code in ["403", "429"]:
            print("\n")
            logging.error(f"❌ Transmisi ditolak oleh server Archive.org (Limit IP Tercapai / File Collision)! (HTTP Code: {http_code})")
            return int(http_code)
            
        else:
            print("\n")
            logging.error(f"❌ Transmisi terputus karena masalah jaringan! (HTTP Code: {http_code})")
            return None
            
    except Exception as e:
        print("\n")
        logging.error(f"❌ Kesalahan Kritis OS saat menjalankan cURL: {e}")
        return None

# =========================================================================================
# 👑 THE ATOMIC WATCHPARTY INJECTOR
# =========================================================================================
def play_on_watchparty(video_link: str, room_url: str):
    logging.info('\n🤖 [AUTO-PLAY] Menghubungkan ke WatchParty Room via Stealth Browser...')
    driver = None
    try:
        driver = build_driver() 
        driver.get(room_url)
        wait = WebDriverWait(driver, 20)
        
        logging.info('🔍 Mencari kolom input URL Mantine UI...')
        input_selector = "input[placeholder*='Enter video file URL']"
        
        logging.info('🧹 Mengaktifkan "Phantom Keystrokes" untuk membypass React.js...')
        
        for attempt in range(5):
            try:
                input_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, input_selector)))
                wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, input_selector)))
                
                driver.execute_script("arguments[0].scrollIntoView();", input_box)
                input_box.click()
                time.sleep(1) 
                
                actions = ActionChains(driver)
                actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL)
                actions.send_keys(Keys.BACKSPACE)
                actions.send_keys(video_link)
                actions.send_keys(Keys.ENTER)
                actions.perform()
                
                logging.info('💥 Tautan & ENTER Ditembakkan Secara Atomik via OS Keyboard!')
                time.sleep(2) 
                
                ActionChains(driver).send_keys(Keys.ENTER).perform()
                logging.info('🎬 SUKSES! Video diputar di WatchParty. Bot keluar dari room...')
                break 
                
            except Exception as e:
                logging.warning(f"⚠️ Terjadi rintangan DOM. Menangkap fokus ulang (Percobaan {attempt+1}/5)...")
                time.sleep(2)
                
        time.sleep(3) 

    except Exception as exc:
        logging.error('❌ Gagal memutar video di WatchParty (Error Browser): %s', exc)
    finally:
        if driver: driver.quit()

# --- LOGIKA TINGKAT TINGGI: FUZZY ANTI-GHOST SWEEPER ---
def wait_for_new_movie(search_dir: str) -> Path:
    print(f"\n📡 SNIPER MODE AKTIF: Memantau folder Google Drive secara Real-Time...")
    while True:
        valid_movies = []
        for root, _, files in os.walk(search_dir):
            for file in files:
                if file.lower().endswith('.mp4'):
                    path = Path(root) / file
                    file_slug = sanitize_movie_title(file)
                    if file_slug in GHOST_MEMORY:
                        try:
                            logging.info(f"👻 [FUZZY ANTI-GHOST] Mendeteksi kloningan: {file}. Menghancurkan seketika!")
                            with open(path, 'wb') as f: f.truncate(0); f.flush(); os.fsync(f.fileno()) 
                            path.unlink()
                        except: pass
                        continue 
                    try:
                        size_mb = path.stat().st_size / (1024 * 1024)
                        if size_mb < MIN_MOVIE_SIZE_MB:
                            with open(path, 'wb') as f: f.truncate(0); f.flush(); os.fsync(f.fileno()) 
                            path.unlink()
                            continue 
                        if size_mb <= (MAX_FILE_SIZE_GB * 1024): valid_movies.append(path)
                    except: pass
        if valid_movies:
            newest_movie = sorted(valid_movies, key=lambda f: f.stat().st_mtime, reverse=True)[0]
            print(f"\n🔔 FILM BARU TERDETEKSI: {newest_movie.name} ({newest_movie.stat().st_size / (1024*1024):.2f} MB)")
            last_size = -1
            while True:
                time.sleep(3)
                try:
                    current_size = newest_movie.stat().st_size
                    if current_size == last_size and current_size > 0: break
                    last_size = current_size
                except: pass
            print("✅ File stabil dan siap dieksekusi!\n")
            return newest_movie
        time.sleep(5)

def main():
    if not check_google_drive(): sys.exit(1)

    # 👑 THE IP LEDGER CHECK: Pengecekan Kritis Saat Bot Menyala!
    current_ip = verify_ip_status_and_enforce()

    print("\n" + "="*80)
    print("🚀 ARCHIVE.ORG PREMIUM ROOT CDN BOT (CUSTOM DOMAIN & KERNEL PANIC EDITION)")
    print("   (DB Bypass -> Pre-Emptive Kill -> Fail-Safe -> Cloud Sync -> Harakiri)")
    print("="*80)
    
    while True:
        try:
            original_file_path = wait_for_new_movie(SEARCH_DIR)
            original_name = original_file_path.name 
            clean_title_with_ext = sanitize_movie_title(original_name)
            clean_title = clean_title_with_ext.replace('.mp4', '')
            file_path = original_file_path.with_name(clean_title_with_ext)
            
            try: original_file_path.rename(file_path)
            except: file_path = original_file_path; clean_title = file_path.stem
            
            hash_input = SECRET_SALT + clean_title
            bucket_code = hashlib.sha256(hash_input.encode('utf-8')).hexdigest()[:10]
            
            # 👑 THE DATABASE BYPASS (HANCURKAN FILE GANDA TANPA HARAKIRI)
            existing_link = check_if_already_uploaded(clean_title_with_ext)
            
            if existing_link:
                print("\n" + "🌟"*40)
                print(f"✅ [DATABASE HIT] Film ini sudah pernah diupload ke Archive.org!")
                print(f"⏩ Membatalkan Upload S3 untuk menghemat Bandwidth dan IP...")
                print(f"📥 Mengambil Tautan Lama Anda: {existing_link}")
                print("🌟"*40 + "\n")
                
                GHOST_MEMORY.add(clean_title_with_ext)
                play_on_watchparty(existing_link, ROOM_URL)
                
                try:
                    print(f'\n🗑️ Memulai penghapusan permanen tingkat OS (FSync Shredder)...')
                    with open(file_path, 'wb') as f: f.truncate(0); f.flush(); os.fsync(f.fileno()) 
                    file_path.unlink()
                    print('✅ File ganda di Drive dihancurkan total (0 Byte).')
                    # Jeda sinkronisasi untuk file bypass (opsional tapi aman)
                    print("⏳ Menunggu 5 detik sinkronisasi Cloud Drive...")
                    time.sleep(5)
                except: pass

                # JANGAN HARAKIRI! Karena IP Colab sama sekali tidak terpakai.
                print("\n" + "="*80)
                print("🔄 Skip selesai! Lanjut menyapu file berikutnya di Drive...")
                print("="*80)
                continue 
            
            active_account = get_next_account()
            print(f"🎭 [SMART LOAD BALANCER] Mengambil akun antrean: {active_account}")
            
            # 👑 UPLOAD MURNI
            link = upload_archive_s3_curl(file_path, clean_title_with_ext, bucket_code, active_account)
            
            if isinstance(link, str):
                # 👑 JIKA SUKSES MUTLAK
                unquoted_link = urllib.parse.unquote(link)
                print('\n🎉 UNGGAHAN TITAN BERHASIL!')
                print(f'📥 Tautan WatchParty Anda: {unquoted_link}')
                
                archive_secret_link = f"https://archive.org/details/{bucket_code}"
                log_success_upload(original_name, clean_title_with_ext, unquoted_link, archive_secret_link)
                logging.info(f"📝 [DATABASE] Film dicatat ke {DATABASE_FILE.name}")
                
                GHOST_MEMORY.add(clean_title_with_ext)
                play_on_watchparty(link, ROOM_URL)
                
                # Mengunci IP karena sudah dipakai untuk 1 upload sukses
                mark_ip_as_used(current_ip)
                
                # 👑 FAIL-SAFE SHREDDER
                try:
                    print(f'\n🗑️ Memulai penghapusan permanen tingkat OS (FSync Shredder)...')
                    with open(file_path, 'wb') as f: f.truncate(0); f.flush(); os.fsync(f.fileno()) 
                    file_path.unlink()
                    print('✅ File di Drive dihancurkan total (0 Byte).')
                except: pass

                # 👑 CLOUD SYNC DELAY (MENCEGAH FILE NYANGKUT DI DRIVE)
                print("⏳ Menunggu 15 detik agar Server Google Drive mensinkronisasi penghapusan ini ke Cloud...")
                time.sleep(15)

                # 👑 THE HYPERVISOR KAMIKAZE (OS-LEVEL HARAKIRI) SETELAH SUKSES
                trigger_kernel_panic("TUGAS SELESAI MUTLAK (SATU PELURU, SATU NYAWA)")

            elif link in [403, 429]:
                # 👑 JIKA TERKENA LIMIT 403 
                mark_ip_as_used(current_ip)
                # 👑 LEDAKKAN SERVER KARENA IP SUDAH KOTOR 
                trigger_kernel_panic("LIMIT IP ARCHIVE TERCAPAI (403/429)!")
                
            else:
                print('\n❌ Gagal memproses file ke Archive.org S3 karena gangguan jaringan.')
                print('⚠️ FILE AMAN DI DRIVE! Bot akan melakukan Auto-Retry dalam 5 detik...')
                print("\n" + "-"*80)
                time.sleep(5)
            
        except KeyboardInterrupt: sys.exit(0)
        except Exception as e: time.sleep(5)

if __name__ == '__main__':
    main()
