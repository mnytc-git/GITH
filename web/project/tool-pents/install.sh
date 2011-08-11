#!/bin/bash

# Cek apakah dijalankan sebagai root
if [ "$EUID" -ne 0 ]
  then echo "❌ Mohon jalankan script ini sebagai root: sudo ./install.sh"
  exit
fi

echo "============================================="
echo "   AUTO INSTALLER: RECON & PENTEST TOOLS     "
echo "============================================="

# 1. Update System & Install Dependencies Dasar
echo "[+] Mengupdate Repository & System..."
apt update && apt upgrade -y
echo "[+] Menginstall Dependencies (Git, Python, Go, Pip)..."
apt install -y git python3 python3-pip golang wget curl

# Setup Go Environment (Penting untuk Nuclei, Dalfox, dll)
echo "[+] Mengkonfigurasi Go Environment..."
export PATH=$PATH:$(go env GOPATH)/bin
echo 'export PATH=$PATH:$(go env GOPATH)/bin' >> ~/.bashrc

# Buat folder khusus untuk tools manual
mkdir -p tools

# ---------------------------------------------
# 2. INSTALL VIA APT (Kali Repository)
# ---------------------------------------------
echo "[+] Menginstall Tools via APT (Standard Repo)..."
# Menggabungkan install dalam satu perintah agar lebih cepat
apt install -y \
    amass \
    finalrecon \
    subfinder \
    httpx-toolkit \
    nmap \
    naabu \
    whatweb \
    nikto \
    wafw00f \
    ffuf \
    zaproxy \
    sqlmap \
    wpscan \
    joomscan \
    hydra \
    testssl.sh \
    wapiti \
    subjack \
    exploitdb \
    whois \
    iputils-ping

# Catatan: exploitdb adalah paket yang berisi searchsploit

# ---------------------------------------------
# 3. INSTALL VIA GO (Golang)
# ---------------------------------------------
echo "[+] Menginstall Tools via Go (Latest Versions)..."

# Kiterunner (API Scanner)
go install github.com/assetnote/kiterunner/cmd/kr@latest

# Nuclei (Vulnerability Scanner)
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
# Update template nuclei agar siap pakai
~/go/bin/nuclei -update-templates

# Dalfox (XSS Handler)
go install github.com/hahwul/dalfox/v2@latest

# ---------------------------------------------
# 4. INSTALL VIA GIT CLONE & PYTHON
# ---------------------------------------------
echo "[+] Menginstall Tools Manual (Git Clone)..."
cd tools

# CloudFail
if [ ! -d "CloudFail" ]; then
    echo " -> Installing CloudFail..."
    git clone https://github.com/m0rtem/CloudFail.git
    cd CloudFail
    pip3 install -r requirements.txt --break-system-packages 2>/dev/null || pip3 install -r requirements.txt
    cd ..
fi

# XSStrike
if [ ! -d "XSStrike" ]; then
    echo " -> Installing XSStrike..."
    git clone https://github.com/s0md3v/XSStrike.git
    cd XSStrike
    pip3 install -r requirements.txt --break-system-packages 2>/dev/null || pip3 install -r requirements.txt
    cd ..
fi

# Sn1per
if [ ! -d "Sn1per" ]; then
    echo " -> Downloading Sn1per..."
    git clone https://github.com/1N3/Sn1per.git
    # Sn1per butuh install manual interaktif, kita skip eksekusi otomatisnya
fi

cd ..

echo "============================================="
echo "           ✅ INSTALASI SELESAI!             "
echo "============================================="
echo "Catatan Penting:"
echo "1. Jalankan 'source ~/.bashrc' agar command Go (nuclei/kr) terbaca."
echo "2. Untuk Sn1per, masuk ke folder 'tools/Sn1per' dan jalankan 'sudo bash install.sh' secara manual."
