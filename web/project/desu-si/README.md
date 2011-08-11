# 🚀 Ultimate Auto-Streaming Bot (API Sniper Edition)

Sebuah bot otomatisasi tingkat tinggi (Daemon/Sniper Edition) yang dirancang untuk mendeteksi film baru di Google Drive, mengunggahnya secara efisien, dan memutarnya langsung ke WatchParty secara otomatis. Skrip ini dibangun dengan berbagai fitur *stealth* dan optimasi memori.

## ✨ Fitur Utama

- 📡 **Auto-Detect Movie (Sniper Mode)**: Memantau folder Google Drive secara *real-time* dan hanya mengeksekusi file video (`.mp4`) yang memenuhi syarat ukuran minimum (default: > 50MB) dan sudah selesai diunduh 100%.
- ⚡ **Zero-RAM cURL Upload**: Menggunakan eksekusi cURL native untuk proses unggah ke API Backend (`desu.si`). Mencegah kebocoran memori (RAM) dibandingkan menggunakan *library* *requests* biasa untuk file besar.
- 🛡️ **Smart Proxy Rotator**: Dilengkapi dengan sistem *auto-scrape* IP Proxy Elite global. Jika server menolak IP (403 Forbidden/Cloudflare), bot otomatis merotasi proxy hingga unggahan berhasil.
- 🕵️ **WebRTC Killer & Stealth Mode**: Menggunakan konfigurasi Selenium tingkat tinggi dengan *Biometric & Hardware Spoofing (CDP)* untuk mematikan WebRTC dan memanipulasi *fingerprint* browser agar tidak terdeteksi sebagai bot.
- 🎬 **Stealth WatchParty**: Mengambil *Direct Download Link* dari respons JSON dan secara otomatis memasukkannya ke *room* WatchParty yang telah ditentukan.
- 🗑️ **Zero-Byte Shredding**: Menghancurkan file asli di Google Drive menjadi 0 byte lalu menghapusnya secara permanen (Bypass Google Drive Trash) setelah berhasil diputar, sehingga menghemat kapasitas penyimpanan Drive Anda.

## 📋 Prasyarat Sistem

Pastikan lingkungan Anda memenuhi persyaratan berikut sebelum menjalankan bot:
1. **Sistem Operasi**: Linux / Google Colab (direkomendasikan karena menggunakan `/content/drive`).
2. **Google Drive**: Harus sudah ter-*mount* di sistem.
3. **Browser**: Google Chrome atau Chromium terinstal di sistem.
4. **Dependensi Sistem**: `curl` harus terinstal.
5. **Python 3.x** dengan modul-modul berikut:

```bash
pip install selenium webdriver-manager requests urllib3
