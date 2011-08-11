# 🛡️ Secure Enclave Colab Workspace (Builder)

Skrip `co.py` adalah sebuah *builder* (pembuat) *payload* yang dirancang untuk mengubah Google Colab menjadi *Virtual Workspace* dengan tingkat keamanan militer (Forensic Diagnostic Mode + Glass Box Engine). Skrip ini akan mengenkripsi *source code* utama menggunakan `cryptography.fernet` dan menghasilkan *payload* yang siap dieksekusi dengan aman.

## ✨ Fitur Utama (Virtual Workspace)

Jika *payload* utama (`kode_asli`) dieksekusi, sistem akan membangun lingkungan dengan fitur berikut:

- 🔐 **Military-Grade Storage Encryption**: Membuat partisi penyimpanan terenkripsi (`TERMINAL_VAULT.enc`) di Google Drive menggunakan AES-256-CBC.
- 🔄 **Atomic Auto-Save**: Menyimpan status *workspace* (direktori `/workspace`) secara otomatis setiap 60 detik ke Google Drive untuk mencegah kehilangan data.
- 🛡️ **Layer 7 & 9 Kernel Hardening**: Mencegah *profiling* sistem, mematikan IPv6, mengatur *swappiness* ke 0, dan mitigasi *copyfail* tingkat kernel.
- 🌐 **Dynamic Routing (Tor + Privoxy)**: Mengamankan seluruh lalu lintas jaringan (*apt*, *curl*, *go*, dll.) dengan merutekannya secara paksa melalui jaringan anonim Tor (SOCKS5).
- 💻 **Secure Web Terminal**: Menyediakan antarmuka terminal interaktif melalui web (`ttyd`) dengan otentikasi kata sandi ganda.
- 📁 **Secure Web File Manager**: Menyediakan antarmuka manajemen file berbasis GUI (`filebrowser`) untuk mempermudah *upload/download* data ke dalam *enclave*.
- 📦 **Universal Persistence**: Direktori kerja terisolasi yang mendukung *cache* persisten untuk lingkungan Go, NPM, Rust, dan Pipx.

## 📋 Prasyarat

- Akun Google Colab (direkomendasikan menggunakan Google Drive yang terhubung).
- Library Python: `cryptography` (untuk proses enkripsi *payload*).

```bash
pip install cryptography
