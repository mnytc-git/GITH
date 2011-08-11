from cryptography.fernet import Fernet
import os

print("⏳ Memulai proses enkripsi tingkat militer (File-Based)...")

kunci_rahasia = Fernet.generate_key()
cipher_suite = Fernet(kunci_rahasia)

# =================================================================
# KODE ASLI V31 (Forensic Diagnostic Mode + Glass Box Engine)
# =================================================================
kode_asli = r"""
import os
import subprocess
import time
import sys
import re
from google.colab import output, drive

print("==================================================")
print("📂 MENGINISIALISASI VIRTUAL WORKSPACE...")
print("==================================================\n")

if not os.path.exists('/content/drive/MyDrive'):
    print("⚠️ Membutuhkan izin akses penyimpanan eksternal...")
    drive.mount('/content/drive')
else:
    print("✅ Penyimpanan eksternal telah terhubung.")
    print("Melewati proses otorisasi...\n")

os.system("ls -l /content/drive/MyDrive > /dev/null")
time.sleep(3)

# =================================================================
# 1. ENKRIPSI PENYIMPANAN, TRANSAKSI ATOMIK & DROPZONE
# =================================================================
print("🛡️ Verifikasi Integritas Penyimpanan Terenkripsi...")
vault_file = "/content/drive/MyDrive/TERMINAL_VAULT.enc"
dropzone_dir = "/content/drive/MyDrive/ENCLAVE_DROPZONE"
mount_dir = "/workspace"
key_path = "/dev/shm/.sys_k"

try:
    with open(key_path, 'w') as f:
        f.write(kunci_input)
except NameError:
    print("\n❌ ERROR: Variabel 'kunci_input' tidak ditemukan!")
    sys.exit(1)

os.system(f"chmod 400 {key_path}")
os.system(f"fusermount -uz {mount_dir} >/dev/null 2>&1")
os.system(f"umount -l {mount_dir} >/dev/null 2>&1")
os.system(f"rm -rf {mount_dir} >/dev/null 2>&1")
os.makedirs(mount_dir, exist_ok=True)
os.makedirs(dropzone_dir, exist_ok=True)

if os.path.exists(vault_file):
    print("🔓 Memuat partisi terenkripsi ke dalam memori NVMe...")
    res = os.system(f"openssl enc -aes-256-cbc -d -pbkdf2 -in '{vault_file}' -pass file:{key_path} | tar -xz -C '{mount_dir}' >/dev/null 2>&1")
    if res != 0:
        print("\n❌ ERROR: Gagal memuat partisi! Token tidak valid atau data korup.")
        sys.exit(1)
else:
    print("📦 Membuat struktur partisi baru...")
    os.system(f"tar -cz -C '{mount_dir}' -T /dev/null | openssl enc -aes-256-cbc -pbkdf2 -out '{vault_file}' -pass file:{key_path}")

print("⏳ Menyiapkan dependensi sistem & Sinkronisasi Latar Belakang (60s)...")

autosave_script = f'''
while true; do
    sleep 60
    tar -cz -C '{mount_dir}' . | openssl enc -aes-256-cbc -pbkdf2 -out /dev/shm/vault.tmp -pass file:{key_path}
    if [ $? -eq 0 ]; then
        cp -f /dev/shm/vault.tmp '{vault_file}'
    fi
done
'''
with open("/tmp/.autosave.sh", "w") as f:
    f.write(autosave_script)
subprocess.Popen(["bash", "/tmp/.autosave.sh"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
os.system("rm -f /tmp/.autosave.sh")

bash_script = r'''
# [LAYER 7 & 9 HARDENING]: Anti Profiling & Swapping
sysctl -w kernel.dmesg_restrict=1 >/dev/null 2>&1 || true
sysctl -w kernel.unprivileged_bpf_disabled=1 >/dev/null 2>&1 || true
sysctl -w kernel.kptr_restrict=2 >/dev/null 2>&1 || true
sysctl -w vm.swappiness=0 >/dev/null 2>&1 || true

ulimit -c 0 >/dev/null 2>&1

mkdir -p /etc/modprobe.d
echo "install algif_aead /bin/true" > /etc/modprobe.d/copyfail-mitigation.conf
echo "blacklist algif_aead" >> /etc/modprobe.d/copyfail-mitigation.conf

sysctl -w net.ipv6.conf.all.disable_ipv6=1 >/dev/null 2>&1 || true
sysctl -w net.ipv6.conf.default.disable_ipv6=1 >/dev/null 2>&1 || true

echo 'APT::Sandbox::User "root";' > /etc/apt/apt.conf.d/99sandbox

mkdir -p /workspace/.apt_cache/archives
echo 'Dir::Cache::Archives "/workspace/.apt_cache/archives";' > /etc/apt/apt.conf.d/95workspace_cache

cp /etc/skel/.bashrc ~/.bashrc
touch /root/.sys_env

echo 'set enable-bracketed-paste on' > /root/.inputrc
echo '"\e[200~": keep-mark' >> /root/.inputrc
echo '"\r": accept-line' >> /root/.inputrc

# [UNIVERSAL PERSISTENCE ENGINE]: Mencakup Go, NPM, Rust, Pipx
mkdir -p /workspace/bin /workspace/.local/bin /workspace/go/bin /workspace/go/pkg/mod /workspace/.cache/go-build /workspace/.pipx /workspace/.cargo/bin /workspace/.npm-global/bin

if [ ! -f "/workspace/bin/fastfetch" ]; then
    wget -qO /tmp/.fastfetch.tar.gz https://github.com/fastfetch-cli/fastfetch/releases/latest/download/fastfetch-linux-amd64.tar.gz >/dev/null 2>&1
    tar -xzf /tmp/.fastfetch.tar.gz -C /tmp
    mv /tmp/fastfetch-linux-amd64/usr/bin/fastfetch /workspace/bin/
    chmod +x /workspace/bin/fastfetch
    rm -rf /tmp/fastfetch* /tmp/.fastfetch*
fi

ln -sf /content/drive/MyDrive/ENCLAVE_DROPZONE /workspace/Dropzone

# Global Pathing & Cache Redirection
echo 'export PYTHONUSERBASE=/workspace/.local' >> /root/.sys_env
echo 'export PIP_USER=yes' >> /root/.sys_env
echo 'export GOPATH=/workspace/go' >> /root/.sys_env
echo 'export GOBIN=/workspace/go/bin' >> /root/.sys_env
echo 'export GOMODCACHE=/workspace/go/pkg/mod' >> /root/.sys_env
echo 'export GOCACHE=/workspace/.cache/go-build' >> /root/.sys_env
echo 'export PIPX_HOME=/workspace/.pipx' >> /root/.sys_env
echo 'export PIPX_BIN_DIR=/workspace/bin' >> /root/.sys_env
echo 'export CARGO_HOME=/workspace/.cargo' >> /root/.sys_env
echo 'export NPM_CONFIG_PREFIX=/workspace/.npm-global' >> /root/.sys_env
echo 'export PATH="/workspace/bin:/workspace/.local/bin:/workspace/go/bin:/workspace/.cargo/bin:/workspace/.npm-global/bin:$PATH"' >> /root/.sys_env
echo 'export VIRTUAL_ENV_DISABLE_PROMPT=1' >> /root/.sys_env
echo 'export PROXYCHAINS_QUIET_MODE=1' >> /root/.sys_env
echo 'export HISTFILE=/dev/null' >> /root/.sys_env

export PYTHONUSERBASE=/workspace/.local
export PIP_USER=yes
pip install pysocks httpx[socks] requests[socks] >/dev/null 2>&1

if [ ! -f "/workspace/autostart.sh" ]; then
    echo "#!/bin/bash" > /workspace/autostart.sh
    echo "if [ -d /workspace/.apt_cache/archives ]; then dpkg -i /workspace/.apt_cache/archives/*.deb >/dev/null 2>&1; fi" >> /workspace/autostart.sh
    chmod +x /workspace/autostart.sh
fi

# [LAYER 10 PROXY TRANSLATOR]: Solusi Mutlak untuk Golang & Curl (Error 97)
echo 'export HTTP_PROXY="http://127.0.0.1:8118"' >> ~/.bashrc
echo 'export HTTPS_PROXY="http://127.0.0.1:8118"' >> ~/.bashrc
echo 'export ALL_PROXY="socks5h://127.0.0.1:9050"' >> ~/.bashrc
echo 'export NO_PROXY="localhost,127.0.0.1"' >> ~/.bashrc

echo 'source /root/.sys_env 2>/dev/null' >> ~/.bashrc

echo "bind 'set enable-bracketed-paste on' 2>/dev/null" >> ~/.bashrc
echo "clear" >> ~/.bashrc
echo "/workspace/bin/fastfetch -l ubuntu | sed \"s/Google Compute Engine/Cloud Compute Node/g\"" >> ~/.bashrc
echo "echo -e \"\\n\\e[36m=================================================================\\e[0m\"" >> ~/.bashrc
echo "echo -n -e \"\\e[32m🛡️  VERIFIKASI IP (TOR SECURE ROUTE) : \\e[0m\"" >> ~/.bashrc
# Verifikasi IP kini dijamin sukses menembus proxy Privoxy
echo "curl -s --max-time 10 icanhazip.com || echo \"Memuat rute...\"" >> ~/.bashrc
echo "echo -e \"\\e[36m=================================================================\\e[0m\\n\"" >> ~/.bashrc

echo "alias save='echo \"⏳ Melakukan kompresi data...\" && tar -cz -C /workspace . | openssl enc -aes-256-cbc -pbkdf2 -out /dev/shm/vault.tmp -pass file:/dev/shm/.sys_k && echo \"🚀 Mengirim data...\" && cp -f /dev/shm/vault.tmp /content/drive/MyDrive/TERMINAL_VAULT.enc && sync && echo \"✅ PENYIMPANAN SUKSES!\"'" >> ~/.bashrc
echo "alias turbo='env -u HTTP_PROXY -u HTTPS_PROXY -u ALL_PROXY LD_PRELOAD= '" >> ~/.bashrc

echo 'export PS1="\[\e[38;5;51m\]┌──(\[\e[0m\]secure\[\e[38;5;51m\])(\[\e[0m\]root㉿Node\[\e[38;5;51m\])-\[\e[0m\][\[\e[38;5;46m\]\w\[\e[0m\]]\n\[\e[38;5;51m\]└─\[\e[38;5;226m\]⚡\[\e[0m\] "' >> ~/.bashrc
echo "cd /workspace" >> ~/.bashrc
'''
with open("/tmp/.setup_env.sh", "w") as f:
    f.write(bash_script)
os.system("bash /tmp/.setup_env.sh")

# =================================================================
# 2. DYNAMIC ROUTING ENGINE (LAYER 6 HARDENING & PRIVOXY TRANSLATOR)
# =================================================================
print("🔄 Mengonfigurasi Dynamic Routing Engine (Layer 6 Hardening)...")

os.system("rm -f /etc/apt/apt.conf.d/90tor")
os.system("printf '#!/bin/sh\\nexit 101\\n' > /usr/sbin/policy-rc.d && chmod +x /usr/sbin/policy-rc.d")
# [INTEGRASI PRIVOXY]: Ditambahkan ke instalasi inti
os.system("apt-get update -qq > /dev/null 2>&1 && apt-get install -y -qq tor proxychains4 netcat-openbsd python3-venv golang-go pipx privoxy > /dev/null 2>&1")
os.system("rm -f /usr/sbin/policy-rc.d")

# [KONFIGURASI PRIVOXY]: Menerjemahkan HTTP ke SOCKS5t secara Native
os.system("echo 'listen-address 127.0.0.1:8118' > /etc/privoxy/config")
os.system("echo 'forward-socks5t / 127.0.0.1:9050 .' >> /etc/privoxy/config")
os.system("service privoxy restart >/dev/null 2>&1")

os.system("mkdir -p /etc/tor /var/lib/tor")
os.system("pkill -9 tor >/dev/null 2>&1")
os.system("rm -rf /var/lib/tor/* /tmp/sys_route.log")
os.system("chown -R debian-tor:debian-tor /var/lib/tor && chmod 700 /var/lib/tor")

torrc_config = r'''
Log notice stdout
DataDirectory /var/lib/tor
ClientUseIPv6 0
SocksPort 127.0.0.1:9050
RunAsDaemon 0
FascistFirewall 1
ReachableAddresses *:80,*:443
AvoidDiskWrites 1
SafeSocks 1
ConnectionPadding 1
HardwareAccel 1
Sandbox 1
'''
with open("/etc/tor/torrc", "w") as f:
    f.write(torrc_config)

print("⚡ Memulai sinkronisasi jaringan terenkripsi...")
os.system('su -s /bin/bash debian-tor -c "tor -f /etc/tor/torrc > /tmp/sys_route.log 2>&1 &"')

port_open = False
for i in range(10):
    if os.system("nc -z 127.0.0.1 9050 >/dev/null 2>&1") == 0:
        port_open = True
        break
    time.sleep(1)

if not port_open:
    print("\n🚨 ERROR: Port jaringan terenkripsi gagal beroperasi.")
    os.system("cat /tmp/sys_route.log")
    sys.exit(1)

print("   ✅ Encrypted Route aktif. Menyinkronkan node...")

bootstrap_success = False
last_pct = ""
for i in range(90):
    if os.path.exists("/tmp/sys_route.log"):
        with open("/tmp/sys_route.log", "r") as f:
            lines = f.readlines()
            for line in reversed(lines):
                if "Bootstrapped" in line:
                    match = re.search(r'Bootstrapped (\d+)%', line)
                    if match:
                        pct = match.group(1)
                        if pct != last_pct:
                            print(f"   📡 Proses Sinkronisasi: {pct}%")
                            last_pct = pct
                        if pct == "100":
                            bootstrap_success = True
                    break
    if bootstrap_success:
        break
    time.sleep(1)

if not bootstrap_success:
    print("\n🚨 ERROR: Timeout pada proses sinkronisasi.")
    os.system("cat /tmp/sys_route.log | tail -n 25")
    sys.exit(1)

print("✅ Jaringan Dynamic Routing Terenkripsi 100% siap!")

# =================================================================
# 3. POST-ROUTE LOCKDOWN & AUTOSTART RECOVERY
# =================================================================
os.system("echo 'Acquire::http::Proxy \"http://127.0.0.1:8118\";' > /etc/apt/apt.conf.d/90tor")
os.system("echo 'Acquire::https::Proxy \"http://127.0.0.1:8118\";' >> /etc/apt/apt.conf.d/90tor")
os.system("echo 'Acquire::https::Verify-Peer \"true\";' >> /etc/apt/apt.conf.d/90tor")
os.system("echo 'Acquire::https::Verify-Host \"true\";' >> /etc/apt/apt.conf.d/90tor")

print("⏳ Memulihkan dependensi paket kustom (Autostart)...")
os.system("if [ -f /workspace/autostart.sh ]; then proxychains4 -q bash /workspace/autostart.sh >/dev/null 2>&1; fi")
print("✅ Seluruh manajemen paket telah diarahkan ke jalur terenkripsi.")

# =================================================================
# 4. WEB TERMINAL ANTARMUKA AMAN
# =================================================================
os.system("echo -e 'strict_chain\nproxy_dns\nremote_dns_subnet 224\ntcp_read_time_out 15000\ntcp_connect_time_out 8000\nlocalnet 127.0.0.0/255.0.0.0\nquiet_mode\n[ProxyList]\nsocks5 127.0.0.1 9050' > /etc/proxychains4.conf")

os.system("pkill -9 -f ttyd > /dev/null 2>&1")
tty_path = "/tmp/.sys_tty"
os.system(f"wget -qO {tty_path} https://github.com/tsl0922/ttyd/releases/download/1.7.3/ttyd.x86_64 >/dev/null 2>&1")
os.system(f"chmod +x {tty_path}")

try:
    with open("/dev/shm/.sys_k", "r") as f:
        kunci_asli = f.read().strip()
except:
    kunci_asli = "admin"

terminal_auth = f'''#!/bin/bash
clear
echo -e "\\e[36m=================================================================\\e[0m"
echo -e "\\e[36m🔒 ENCRYPTED WORKSPACE - AUTHORIZATION REQUIRED \\e[0m"
echo -e "\\e[36m=================================================================\\e[0m"
echo -e "\\e[33m📌 PERINGATAN: Direktori Persisten adalah /workspace\\e[0m"
echo -e "\\e[33m   (Data dienkripsi secara atomik setiap 60 detik)\\e[0m"
echo -e "\\e[36m=================================================================\\e[0m"
read -sp "🔑 Masukkan Token: " user_pass
echo ""
if [ "$user_pass" == "{kunci_asli}" ]; then
    export VIRTUAL_ENV_DISABLE_PROMPT=1
    export PROXYCHAINS_QUIET_MODE=1
    export HISTFILE=/dev/null
    source /root/.sys_env 2>/dev/null
    exec proxychains4 -q bash
else
    echo -e "\\e[31m❌ AKSES DITOLAK! Token tidak valid.\\e[0m"
    sleep 2
    exit 1
fi
'''
with open("/tmp/.sys_auth.sh", "w") as f:
    f.write(terminal_auth)
os.system("chmod +x /tmp/.sys_auth.sh")

with open("/tmp/.tty.log", "w") as log_file:
    subprocess.Popen([tty_path, "-p", "9999", "/tmp/.sys_auth.sh"], stdout=log_file, stderr=subprocess.STDOUT)

# =================================================================
# 5. SECURE WEB FILE MANAGER (GUI UPLOAD/DOWNLOAD)
# =================================================================
print("⏳ Menyiapkan Secure Web File Manager (GUI)...")
os.system("pkill -9 -f filebrowser > /dev/null 2>&1")
os.system("curl -fsSL https://raw.githubusercontent.com/filebrowser/get/master/get.sh | bash >/dev/null 2>&1")

fb_db = "/dev/shm/.fb.db"
os.system(f"rm -f {fb_db}")
os.system(f"filebrowser config init -d {fb_db} >/dev/null 2>&1")
os.system(f"filebrowser config set -d {fb_db} --auth.method=password --branding.name=\"SECURE ENCLAVE FS\" --branding.disableExternal >/dev/null 2>&1")
os.system(f"filebrowser users add admin \"{kunci_asli}\" --perm.admin -d {fb_db} >/dev/null 2>&1")

with open("/tmp/.fb.log", "w") as log_file:
    subprocess.Popen(["filebrowser", "-d", fb_db, "-a", "127.0.0.1", "-p", "8888", "-r", "/workspace"], stdout=log_file, stderr=subprocess.STDOUT)

print("⏳ Mengalokasikan port antarmuka ganda...")
ports_ready = False
for i in range(15):
    chk_tty = os.system("nc -z 127.0.0.1 9999 >/dev/null 2>&1")
    chk_fb = os.system("nc -z 127.0.0.1 8888 >/dev/null 2>&1")
    if chk_tty == 0 and chk_fb == 0:
        ports_ready = True
        break
    time.sleep(1)

if not ports_ready:
    print("\n❌ ERROR: Gagal mengalokasikan port antarmuka.")
    sys.exit(1)

proxy_url_term = output.eval_js("google.colab.kernel.proxyPort(9999)")
proxy_url_file = output.eval_js("google.colab.kernel.proxyPort(8888)")

print("\n" + "="*65)
print("✅ SECURE WORKSPACE & FILE MANAGER AKTIF!")
print("="*65)
print(f"💻 AKSES TERMINAL : \n{proxy_url_term}\n")
print(f"📁 AKSES FILE MANAGER (Upload/Edit) : \n{proxy_url_file}")
print(f"   (Username: admin | Password: Kunci Rahasia Anda)")
print("="*65 + "\n")
"""

# =================================================================
# PROSES ENKRIPSI FINAL
# =================================================================
kode_terenkripsi = cipher_suite.encrypt(kode_asli.encode('utf-8'))

with open('/content/KUNCI_RAHASIA.txt', 'w') as f:
    f.write(kunci_rahasia.decode('utf-8'))

with open('/content/payload.txt', 'w') as f:
    f.write(kode_terenkripsi.decode('utf-8'))

print("✅ ENKRIPSI BERHASIL! File telah dicetak mentah-mentah ke Hardisk Colab.")
