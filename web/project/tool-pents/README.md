# Tools
Repository ini berisi script otomatis untuk menginstall seluruh *essential tools* untuk Reconnaissance, Web Vulnerability Scanning, dan Network Scanning pada Kali Linux/Ubuntu.
## 🚀 Cara Install

Cukup jalankan satu perintah berikut di terminal:

```bash
git clone https://github.com/mnytc-git/Tools.git
cd Tools
chmod +x install.sh
sudo ./install.sh
```
```bash
amass enum -d microsoft.com
finalrecon --full --url [https://target.com](https://target.com)
subfinder -d target.com -silent | httpx -status-code -mc 200
nmap -p 80 --script http-vhosts --script-args http-vhosts.domainname=target.com target.com
naabu -host target.com
# UDP Scan
sudo nmap -sU -sV --version-intensity 5 -p 53,123,161,500 target.com
whatweb -a 3 [https://target.com](https://target.com)
# Menggunakan Dirsearch (jika diinstall manual di folder tools)
python3 tools/dirsearch/dirsearch.py -u [https://target.com](https://target.com) -e php,js,conf,bak,zip,sql,.env
wafw00f [https://target.com](https://target.com) -a
ffuf -u http://TARGET_IP/FUZZ -w /usr/share/wordlists/dirb/common.txt -e .php,.html,.txt -mc 200,301,302 -ac -c
nuclei -u [https://target.com](https://target.com)
nikto -h [https://target.com](https://target.com)
zaproxy -cmd -quickurl [https://target.com](https://target.com) -quickout laporan-scan.html
wapiti -u [http://testphp.vulnweb.com/](http://testphp.vulnweb.com/)
wpscan --url [https://target-wordpress.com](https://target-wordpress.com)
joomscan -u [https://target-joomla.com](https://target-joomla.com)
nuclei -u [https://target-sharepoint.com](https://target-sharepoint.com) -tags sharepoint
sqlmap -u "[http://target.com/page.php?id=1](http://target.com/page.php?id=1)" --dbs
python3 tools/XSStrike/xsstrike.py -u "[http://target.com/search.php?q=test](http://target.com/search.php?q=test)"
dalfox url [http://testphp.vulnweb.com/listproducts.php?cat=1](http://testphp.vulnweb.com/listproducts.php?cat=1)
sniper -t <target.com>
sniper -t <target.com> -m stealth
subfinder -d target.com -silent | nuclei -t takeovers/ -o hasil_scan.txt
hydra -l user -P /usr/share/wordlists/rockyou.txt ssh://target_ip
testssl.sh target.com
```
### Catatan Penting
* **Sn1per**: Di dalam script `install.sh`, saya hanya melakukan `git clone` untuk Sn1per. Sn1per memiliki script instalasinya sendiri yang sangat masif dan sering meminta input user. Setelah script saya selesai, Anda perlu masuk ke folder Sn1per dan menginstalnya secara manual (instruksi sudah saya echo di akhir script).
* **Path**: Beberapa tool Go (seperti `nuclei`, `subfinder`) membutuhkan path Go yang benar. Script sudah mencoba menambahkannya ke `.bashrc`, tapi mungkin perlu restart terminal setelah install.
