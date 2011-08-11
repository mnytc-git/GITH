#!/bin/bash
# BANG TITAN AI-INTEGRATED - PROJECT LAZARUS // CHAOS THEORY EDITION (v34.0)
# Architect: BANG (Project Lazarus) for Tuan YANG
# Status: INTEGRATED (RECON + VULN + AI INDONESIA + NUCLEAR OVERRIDE + RAW VERBOSITY + CYBER UI)
# Efficiency is a Crime. Data is Absolute. No Simplification.

# [CRITICAL ENVIRONMENT SETUP]
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:$HOME/go/bin:/usr/local/go/bin:$PATH
export GOPATH=$HOME/go
export GOBIN=$HOME/go/bin

# -- COLOR PALETTE (CYBER THEME) --
RESET='\033[0m'
BOLD='\033[1m'
ITALIC='\033[3m'
UNDERLINE='\033[4m'

RED='\033[38;5;196m'
GREEN='\033[38;5;46m'
YELLOW='\033[38;5;226m'
BLUE='\033[38;5;33m'
MAGENTA='\033[38;5;213m'
CYAN='\033[38;5;51m'
GRAY='\033[38;5;240m'
WHITE='\033[38;5;255m'
ORANGE='\033[38;5;202m'
BG_RED='\033[48;5;196m'
BG_GREEN='\033[48;5;46m'

# Global Settings (Inherited from Titan Maximum)
TIMEOUT_FAST=60
TIMEOUT_HEAVY=7200
USER_AGENT="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
RISK_SCORE=0 

# AI CORE CONFIGURATION (Integrated from Lazarus Post Tool)
API_URL="https://text.pollinations.ai/"
MODEL="openai"

# ===================== [1] UI HELPERS & UTILITIES =====================

print_banner() {
    clear
    echo -e "${MAGENTA}"
    echo "    ██████╗  █████╗ ███╗    ██╗ ██████╗ "
    echo "    ██╔══██╗██╔══██╗████╗   ██║██╔════╝ "
    echo "    ██████╔╝███████║██╔██╗  ██║██║  ███╗"
    echo "    ██╔══██╗██╔══██║██║╚██╗ ██║██║   ██║"
    echo "    ██████╔╝██║  ██║██║ ╚████║╚██████╔╝"
    echo "    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ "
    echo -e "${CYAN}    TITAN AI-INTEGRATED // PROJECT LAZARUS // v34.0${RESET}"
    echo -e "${GRAY}    ==============================================${RESET}"
    echo -e "${RED}    [ MODE: CHAOS THEORY ] [ AI ANALYSIS: INDONESIAN ]${RESET}"
    echo -e "${RED}    [ SYSTEM: NO-OPTIMIZATION PROTOCOL ACTIVE ]${RESET}"
    echo ""
}

info() {
    echo -e "${BLUE} [➜] ${CYAN}$1${RESET}"
}

success() {
    echo -e "${GREEN} [✔] ${WHITE}$1${RESET}"
}

clean() {
    echo -e "${GREEN} [🛡️] ${WHITE}$1${RESET}"
}

warn() {
    echo -e "${YELLOW} [!] ${ORANGE}$1${RESET}"
}

crit() {
    echo -e "${BG_RED}${WHITE} [💀] FATAL ERROR: $1 ${RESET}"
}

section() {
    echo -e "\n${MAGENTA}╔════════════════════════════════════════════════════════╗${RESET}"
    echo -e "${MAGENTA}║ ${BOLD}$1${RESET}"
    echo -e "${MAGENTA}╚════════════════════════════════════════════════════════╝${RESET}"
}

cleanup() {
    tput cnorm
    echo -e "\n"
    crit "SYSTEM OVERRIDE DETECTED. INITIATING EMERGENCY SHUTDOWN..."
    if [ -n "$MONITOR_PID" ]; then kill $MONITOR_PID 2>/dev/null; fi
    jobs -p | xargs -r kill > /dev/null 2>&1
    exit 1
}
trap cleanup SIGINT

# [CYBER ANIMATION SPINNER v2]
spinner() {
    local pid=$1
    local text=$2
    local spinstr='⣾⣽⣻⢿⡿⣟⣯⣷'
    tput civis
    while kill -0 $pid 2>/dev/null; do
        local temp=${spinstr#?}
        printf "\r${MAGENTA} [PROCESSING]${RESET} ${WHITE}%s${RESET} ${CYAN}[%c]${RESET}" "$text" "$spinstr"
        local spinstr=$temp${spinstr%"$temp"}
        sleep 0.1
    done
    # Overwrite line with completion message
    printf "\r${GREEN} [COMPLETED] ${RESET} ${WHITE}%s${RESET} ${GREEN}[✔]${RESET}                                  \n" "$text"
    tput cnorm
}

# ===================== [2] LOGIC GATES & PATHFINDER =====================
locate_binary() {
    local cmd_name=$1
    if [ -f "$HOME/go/bin/$cmd_name" ]; then echo "$HOME/go/bin/$cmd_name"; return 0; fi
    if [ -f "/usr/local/go/bin/$cmd_name" ]; then echo "/usr/local/go/bin/$cmd_name"; return 0; fi
    if command -v "$cmd_name" &> /dev/null; then echo "$(command -v $cmd_name)"; return 0; fi
    if [ -f "/usr/local/bin/$cmd_name" ]; then echo "/usr/local/bin/$cmd_name"; return 0; fi
    if [ -f "/usr/bin/$cmd_name" ]; then echo "/usr/bin/$cmd_name"; return 0; fi
    if [ -f "/bin/$cmd_name" ]; then echo "/bin/$cmd_name"; return 0; fi
    return 1
}

check_tool() {
    local path
    path=$(locate_binary "$1")
    if [ -z "$path" ]; then
        warn "Tool '$1' not found in any known path. Skipping."
        return 1
    fi
    return 0
}

validate_input() {
    local file=$1
    if [ ! -s "$file" ]; then return 1; fi
    return 0
}

ensure_wordlist() {
    local dir=$1
    local curl_cmd=$(locate_binary "curl")
    
    if [ ! -f "$dir/wordlists/common.txt" ]; then
        info "Downloading Wordlist for Fuzzing..."
        mkdir -p "$dir/wordlists"
        if [ -n "$curl_cmd" ]; then
            $curl_cmd -L "https://raw.githubusercontent.com/danielmiessler/SecLists/refs/heads/master/Discovery/Web-Content/common.txt" -o "$dir/wordlists/common.txt" > /dev/null 2>&1
        fi
        if [ ! -s "$dir/wordlists/common.txt" ]; then
             echo -e "admin\nlogin\nwp-admin\ndashboard\nbackup\nconfig\nportal\n.env\n.git\nserver-status" > "$dir/wordlists/common.txt"
        fi
        success "Wordlist Acquired."
    fi
}

safe_count() {
    local file=$1
    if [ -f "$file" ] && [ -s "$file" ]; then
        wc -l < "$file" 2>/dev/null | tr -cd '0-9'
    else
        echo "0"
    fi
}

create_file() {
    touch "$1"; echo -n "" > "$1"
}

# ===================== [DEEP PROCESS MONITORING] =====================
monitor_process() {
    local pid=$1
    local tool_name=$2
    local expected_output=$3
    local log_file="logs/process_status.log"
    local start_time=$(date +%s)
    
    echo "[$(date '+%H:%M:%S')] [STARTED] Tool: $tool_name | PID: $pid | Expecting: ${expected_output:-None}" >> "$log_file"
    
    while kill -0 $pid 2>/dev/null; do sleep 2; done
    
    wait $pid 2>/dev/null
    local exit_code=$?
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    
    if [ -n "$expected_output" ] && [ -s "$expected_output" ]; then
        local file_size=$(ls -lh "$expected_output" | awk '{print $5}')
        echo "[$(date '+%H:%M:%S')] [SUCCESS] Tool: $tool_name | Output: $file_size | Duration: ${duration}s" >> "$log_file"
    elif [ $exit_code -eq 0 ]; then
        echo "[$(date '+%H:%M:%S')] [COMPLETED] Tool: $tool_name | Exit: 0 | Duration: ${duration}s" >> "$log_file"
    else
        echo "[$(date '+%H:%M:%S')] [FAILED] Tool: $tool_name | Exit: $exit_code | No Data | Duration: ${duration}s" >> "$log_file"
    fi
}

run_monitored() {
    local tool_cmd="$@"
    local tool_base=$(echo "$tool_cmd" | awk '{print $1}')
    local binary_path=$(locate_binary "$tool_base")
    
    local output_file=""
    if [[ "$tool_cmd" =~ -oN[[:space:]]+([^[:space:]]+) ]]; then
        output_file="${BASH_REMATCH[1]}"
    elif [[ "$tool_cmd" =~ -o[[:space:]]+([^[:space:]]+) ]]; then
        output_file="${BASH_REMATCH[1]}"
    elif [[ "$tool_cmd" =~ \>\>[[:space:]]*([^[:space:]]+) ]]; then
        output_file="${BASH_REMATCH[1]}"
    elif [[ "$tool_cmd" =~ \>[[:space:]]*([^[:space:]]+) ]]; then
        output_file="${BASH_REMATCH[1]}"
    elif [[ "$tool_cmd" =~ --results-file=([^[:space:]]+) ]]; then
         output_file="${BASH_REMATCH[1]}"
    fi
    
    if [ -n "$binary_path" ]; then
        local safe_cmd=$(echo "$tool_cmd" | sed "s|^$tool_base|$binary_path|")
        eval "export PATH=$PATH; $safe_cmd" &
        local pid=$!
        monitor_process $pid "$tool_base" "$output_file" &
        spinner $pid "$tool_base"
    else
        crit "Binary not found: $tool_base"
        echo "[$(date '+%H:%M:%S')] [CRITICAL_FAIL] Tool: $tool_base | Reason: Binary Missing" >> logs/process_status.log
    fi
}

# ===================== [3] INSTALLATION SUITE (VISUAL OVERHAUL) =====================

setup_environment() {
    # 0. FORCE PATH CORRECTION
    export PATH=$PATH:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$HOME/go/bin:/usr/local/go/bin
    
    echo -e "${CYAN}[*] INITIALIZING SYSTEM PROTOCOLS...${RESET}"
    
    # Progress Bar Variables
    TOTAL_STEPS=22 # System(1)+Tools(7)+GoTools(11)+Ferox(1)+Exploit(1) + Final(1)
    CURRENT_STEP=0
    
    update_bar() {
        CURRENT_STEP=$((CURRENT_STEP + 1))
        local percent=$((CURRENT_STEP * 100 / TOTAL_STEPS))
        if [ $percent -gt 100 ]; then percent=100; fi
        local filled=$((percent / 2))
        local empty=$((50 - filled))
        
        echo -ne "\r${BLUE}["
        for ((i=0; i<filled; i++)); do echo -ne "${CYAN}▓"; done
        for ((i=0; i<empty; i++)); do echo -ne "${GRAY}░"; done
        echo -ne "${BLUE}] ${WHITE}${percent}%${RESET}"
    }

    # 1. System Essentials
    if command -v apt &> /dev/null; then
        sudo apt-get update -y > /dev/null 2>&1
        sudo apt-get install -y curl libpcap-dev build-essential git gcc wget make unzip > /dev/null 2>&1
    elif command -v pacman &> /dev/null; then
        sudo pacman -Syu --noconfirm curl libpcap base-devel git wget unzip > /dev/null 2>&1
    elif command -v apk &> /dev/null; then
        sudo apk add --upgrade curl git build-base libpcap-dev unzip > /dev/null 2>&1
    fi
    if ! command -v curl &> /dev/null; then
        echo -e "\n${RED}[ERROR] CURL MISSING${RESET}"
        exit 1
    fi
    update_bar

    # Helper function definitions
    install_sys_tool() {
        local tool_bin=$1
        local pkg_name=$2
        if command -v apt &> /dev/null; then sudo apt-get install -y "$pkg_name" > /dev/null 2>&1; fi
        if command -v pacman &> /dev/null; then sudo pacman -S --noconfirm "$pkg_name" > /dev/null 2>&1; fi
        update_bar
    }

    force_install_binary() {
        local bin_name=$1
        local repo_url=$2
        local version=$3
        local arch="amd64"
        local os="linux"
        mkdir -p /tmp/bang_install
        cd /tmp/bang_install
        wget -q "$repo_url/releases/download/v$version/${bin_name}_${version}_${os}_${arch}.zip" -O tool.zip
        if [ -s tool.zip ]; then
            unzip -o tool.zip > /dev/null 2>&1
            chmod +x $bin_name
            sudo mv $bin_name /usr/local/bin/ 2>/dev/null || mv $bin_name $HOME/go/bin/
        else
            wget -q "$repo_url/releases/download/v$version/${bin_name}_${version}_${os}_${arch}.tar.gz" -O tool.tar.gz
            if [ -s tool.tar.gz ]; then
                tar -xzf tool.tar.gz > /dev/null 2>&1
                chmod +x $bin_name
                sudo mv $bin_name /usr/local/bin/ 2>/dev/null || mv $bin_name $HOME/go/bin/
            fi
        fi
        cd - > /dev/null
        rm -rf /tmp/bang_install
    }

    install_go_tool() {
        local bin_name=$1
        local package_path=$2
        export GOPATH=$HOME/go
        export PATH=$PATH:/usr/local/go/bin:$HOME/go/bin
        go install "${package_path}@latest" > /dev/null 2>&1
        
        if [ -z "$(locate_binary $bin_name)" ]; then
            if [ "$bin_name" == "httpx" ]; then
                force_install_binary "httpx" "https://github.com/projectdiscovery/httpx" "1.3.5"
            elif [ "$bin_name" == "subfinder" ]; then
                 force_install_binary "subfinder" "https://github.com/projectdiscovery/subfinder" "2.6.3"
            elif [ "$bin_name" == "nuclei" ]; then
                 force_install_binary "nuclei" "https://github.com/projectdiscovery/nuclei" "3.0.0"
            elif [ "$bin_name" == "naabu" ]; then
                 force_install_binary "naabu" "https://github.com/projectdiscovery/naabu" "2.1.6"
            fi
        fi
        update_bar
    }

    # 2. INSTALL SYS TOOL Calls
    install_sys_tool "git" "git"
    install_sys_tool "nmap" "nmap"
    install_sys_tool "jq" "jq"
    install_sys_tool "go" "golang-go" 
    install_sys_tool "sqlmap" "sqlmap"
    install_sys_tool "whatweb" "whatweb"
    install_sys_tool "nikto" "nikto"

    # 3. INSTALL GO TOOL Calls
    install_go_tool "subfinder" "github.com/projectdiscovery/subfinder/v2/cmd/subfinder"
    install_go_tool "assetfinder" "github.com/tomnomnom/assetfinder"
    install_go_tool "anew" "github.com/tomnomnom/anew"
    install_go_tool "httpx" "github.com/projectdiscovery/httpx/cmd/httpx"
    install_go_tool "waybackurls" "github.com/tomnomnom/waybackurls"
    install_go_tool "gau" "github.com/lc/gau/v2/cmd/gau"
    install_go_tool "subzy" "github.com/PentestPad/subzy"
    install_go_tool "naabu" "github.com/projectdiscovery/naabu/v2/cmd/naabu"
    install_go_tool "nuclei" "github.com/projectdiscovery/nuclei/v2/cmd/nuclei"
    install_go_tool "dalfox" "github.com/hahwul/dalfox/v2"
    install_go_tool "gitleaks" "github.com/zricethezav/gitleaks/v8"

    # 4. FEROXBUSTER FIX
    if [ -z "$(locate_binary feroxbuster)" ]; then
        curl -sL https://raw.githubusercontent.com/epi052/feroxbuster/master/install-nix.sh -o /tmp/install-ferox.sh
        chmod +x /tmp/install-ferox.sh
        /tmp/install-ferox.sh > /dev/null 2>&1
        if [ -f "./feroxbuster" ]; then 
            sudo mv -f ./feroxbuster /usr/local/bin/feroxbuster 2>/dev/null || mv -f ./feroxbuster /usr/local/bin/feroxbuster
            chmod +x /usr/local/bin/feroxbuster
        fi
        rm -f /tmp/install-ferox.sh
    fi
    update_bar

    # 5. SEARCHSPLOIT
    if [ -d "/opt/exploitdb" ]; then
        cd /opt/exploitdb && git pull > /dev/null 2>&1 && cd - > /dev/null
    else
        if [ -z "$(locate_binary searchsploit)" ]; then
             sudo apt-get install -y exploitdb > /dev/null 2>&1
             if [ -z "$(locate_binary searchsploit)" ]; then
                 git clone https://github.com/offensive-security/exploitdb.git /opt/exploitdb > /dev/null 2>&1
                 sudo ln -sf /opt/exploitdb/searchsploit /usr/local/bin/searchsploit 2>/dev/null
             fi
        fi
    fi
    update_bar
    
    echo ""
}

# ===================== [PRIVACY CLOAKING & AI INTEGRATION LOGIC] =====================

scrub_sensitive_data() {
    local input_file=$1
    local output_file=$2
    local target_domain=$3
    
    # 1. Buat salinan aman
    cp "$input_file" "$output_file"
    
    # 2. Hapus Target Spesifik (Domain)
    sed -i "s/$target_domain/[REDACTED_TARGET]/g" "$output_file"
    
    # 3. Hapus Pola IP (IPv4)
    sed -i -E 's/([0-9]{1,3}\.){3}[0-9]{1,3}/[REDACTED_IP]/g' "$output_file"
    
    # 4. Hapus URL Spesifik
    sed -i "s|http://|http://[MASKED]/|g" "$output_file"
    sed -i "s|https://|https://[MASKED]/|g" "$output_file"
    
    echo -e "${CYAN}    >>> Original Size: $(wc -c < "$input_file") bytes${RESET}"
    echo -e "${CYAN}    >>> Scrubbed Size: $(wc -c < "$output_file") bytes${RESET}"
}

transmit_to_ai_core() {
    local scrubbed_content=$(cat "$1")
    
    local prompt_template="Bertindaklah sebagai AI Keamanan Siber Lazarus. Analisis log keamanan berikut. Tuliskan ringkasan eksekutif dalam bentuk PARAGRAF NARATIF (bukan poin-poin/list). Gunakan BAHASA INDONESIA yang profesional. Batasi jawaban maksimal 150 kata. Fokus pada risiko dan mitigasi utama. Jangan gunakan format markdown bold/italic yang kompleks. Data: $scrubbed_content"

    info "Memulai Transmisi POST ke Core Lazarus via $MODEL..."
    info "Status: Jalur URL Tersembunyi (Masked)"
    
    safe_content=$(echo "$prompt_template" | sed 's/"/\\"/g' | tr '\n' ' ')
    
    response=$(curl -s -X POST "$API_URL" \
      -H "Content-Type: application/json" \
      -d "{
        \"messages\": [{\"role\": \"user\", \"content\": \"$safe_content\"}],
        \"model\": \"$MODEL\",
        \"private\": true,
        \"json\": false
      }")
    
    echo -e "\n${MAGENTA}╔════════════════════════════════════════════════════════════════════╗${RESET}"
    echo -e "${MAGENTA}║               LAZARUS AI STRATEGIC ANALYSIS                        ║${RESET}"
    echo -e "${MAGENTA}╚════════════════════════════════════════════════════════════════════╝${RESET}"

    # Clean text: Remove bold markers (**), wrap at 70 cols, print in Gray.
    echo "$response" | sed 's/\*\*//g' | fold -s -w 70 | while IFS= read -r line; do
        echo -e "  ${GRAY}$line${RESET}"
    done
    echo -e "${MAGENTA}══════════════════════════════════════════════════════════════════════${RESET}\n"
    
    echo "$response" > "AI_STRATEGIC_ANALYSIS.md"
    success "AI strategic report saved to: AI_STRATEGIC_ANALYSIS.md"
}

# ===================== [4] TARGET ACQUISITION & EXECUTION FLOW =====================
print_banner
setup_environment

echo ""
echo -e "${BOLD}${CYAN}╔════ TARGET ACQUISITION SYSTEM ════╗${RESET}"
read -p "║ Enter Target (e.g., target.com): " USER_INPUT
echo -e "${BOLD}${CYAN}╚═══════════════════════════════════╝${RESET}"

TARGET=$(echo "$USER_INPUT" | sed -E 's|^[a-zA-Z]+://||' | sed -E 's|^www\.||' | cut -d/ -f1)

if [[ -z "$TARGET" ]]; then crit "Target cannot be empty."; exit 1; fi

success "LOCKING TARGET: ${BOLD}$TARGET${RESET}"

# Setup Directories
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_DIR="BANG_${TARGET}_${TIMESTAMP}"
mkdir -p "$OUTPUT_DIR/recon"
mkdir -p "$OUTPUT_DIR/vuln/sqlmap"
mkdir -p "$OUTPUT_DIR/fuzzing"
mkdir -p "$OUTPUT_DIR/exploits"
mkdir -p "$OUTPUT_DIR/logs"
mkdir -p "$OUTPUT_DIR/wordlists"

cd "$OUTPUT_DIR" || exit 1
ROOT_DIR=$(pwd)
STATUS_LOG="logs/process_status.log"
touch "$STATUS_LOG"
echo "=== PROCESS MONITORING STARTED: $(date) ===" > "$STATUS_LOG"
echo "Format: [TIME] [STATUS] Tool | Output Size | Duration" >> "$STATUS_LOG"

log() {
    echo -e "$1"
}

# ===================== [5] PHASE 1: RECONNAISSANCE =====================
section "PHASE 1: HYBRID RECONNAISSANCE"
log "PHASE 1 START"
create_file "recon/all_subdomains_raw.txt"

if check_tool "subfinder"; then
    info "Subfinder: Harvesting..."
    run_monitored "subfinder -d $TARGET -all -silent >> recon/all_subdomains_raw.txt 2>/dev/null"
    success "Subfinder Task Complete."
fi

if check_tool "assetfinder"; then
    info "Assetfinder: Harvesting..."
    run_monitored "assetfinder --subs-only $TARGET >> recon/all_subdomains_raw.txt 2>/dev/null"
    success "Assetfinder Task Complete."
fi

info "CRT.SH: Querying Database..."
if command -v curl &> /dev/null; then
    curl -s "https://crt.sh/?q=%25.$TARGET&output=json" | grep "name_value" | cut -d '"' -f 4 | sed 's/\\n/\n/g' | sed 's/\*.//g' >> recon/all_subdomains_raw.txt 2>/dev/null & spinner $!
    success "CRT.SH Query Complete."
else
    warn "Failed (Curl missing)."
fi

info "Cleaning & Sorting Data..."
if command -v anew &> /dev/null; then
    cat recon/all_subdomains_raw.txt | sort -u | anew recon/all_subdomains.txt > /dev/null
else
    cat recon/all_subdomains_raw.txt | sort -u > recon/all_subdomains.txt
fi
success "Data Normalized."

SUB_COUNT=$(safe_count "recon/all_subdomains.txt")
echo -e "${GREEN}    >>> Total Unique Subdomains: ${BOLD}$SUB_COUNT${RESET}"

# SUBZY TAKEOVER CHECK
if validate_input "recon/all_subdomains.txt" && check_tool "subzy"; then
    info "Subzy: Checking Takeovers (High Performance)..."
    run_monitored "subzy run --targets recon/all_subdomains.txt --concurrency 25 --hide_fails --verify_ssl > vuln/takeover_results.txt 2>&1"
    
    if grep -q "VULNERABLE" vuln/takeover_results.txt; then
        crit "POTENTIAL SUBDOMAIN TAKEOVER DETECTED! Check 'vuln/takeover_results.txt'"
    else
        clean "No Subdomain Takeover Detected."
    fi
fi

# ===================== [6] PHASE 2: PORT & SERVICE =====================
section "PHASE 2: PORT & SERVICE SCANNING"
log "PHASE 2 START"

info "HTTPX: Probing Web Services..."
if validate_input "recon/all_subdomains.txt" && check_tool "httpx"; then
    # FORCE PATH RE-EXPORT (Redundancy for Exit 127)
    export PATH=$PATH:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:$HOME/go/bin:/usr/local/go/bin
    
    run_monitored "httpx -l recon/all_subdomains.txt -silent -threads 100 -follow-redirects -title -status-code -o recon/web_active_details.txt > /dev/null 2>&1"
    cat recon/web_active_details.txt | awk '{print $1}' > recon/web_active.txt
    success "HTTPX Probe Complete."
else
    echo "http://$TARGET" > recon/web_active.txt
    echo "https://$TARGET" >> recon/web_active.txt
fi

# [SCORCHED EARTH FAILSAFE PROTOCOL v2]
if [ ! -s "recon/web_active.txt" ]; then
    warn "HTTPX Failed to identify targets (Binary/Net Error). Initiating EMERGENCY PROTOCOLS..."
    
    # Clean input list just in case
    tr -d '\r' < recon/all_subdomains.txt > recon/all_subdomains_clean.txt
    
    # 1. Manual CURL Probe (Modified: GET request, max time 5s, no 'timeout' binary dependency)
    info "Protocol A: Manual CURL Probing..."
    while read -r domain; do
        # Probe HTTPS
        if curl -s -m 5 -o /dev/null "https://$domain"; then
            echo "https://$domain" >> recon/web_active.txt
            echo "https://$domain [CURL_DETECTED]" >> recon/web_active_details.txt
            info "Recovered: https://$domain"
        # Probe HTTP
        elif curl -s -m 5 -o /dev/null "http://$domain"; then
            echo "http://$domain" >> recon/web_active.txt
            echo "http://$domain [CURL_DETECTED]" >> recon/web_active_details.txt
            info "Recovered: http://$domain"
        fi
    done < recon/all_subdomains_clean.txt
    
    # 2. SCORCHED EARTH POLICY (Last Resort)
    if [ ! -s "recon/web_active.txt" ]; then
        crit "Protocol A Failed. ACTIVATING SCORCHED EARTH POLICY."
        warn "ASSUMING ALL SUBDOMAINS ARE ALIVE ON PORT 80/443."
        while read -r domain; do
            echo "https://$domain" >> recon/web_active.txt
            echo "http://$domain" >> recon/web_active.txt
        done < recon/all_subdomains_clean.txt
        success "Forced Target Population Complete."
    fi
    
    success "Emergency Protocols Finished. Targets Acquired."
fi

WEB_COUNT=$(safe_count "recon/web_active.txt")
echo -e "${GREEN}    >>> Active Web Targets: ${BOLD}$WEB_COUNT${RESET}"

info "Naabu: Port Scanning (NO LIMIT)..."
if validate_input "recon/all_subdomains.txt" && check_tool "naabu"; then
    run_monitored "naabu -l recon/all_subdomains.txt -top-ports 1000 -o recon/open_ports_raw.txt > /dev/null 2>&1"
    success "Port Scan Complete."
else
    warn "Skipped (Missing Tool/Input)."
fi

info "Sanitizing Port Data for Nmap..."
if [ -s "recon/open_ports_raw.txt" ]; then
    cat recon/open_ports_raw.txt | cut -d: -f1 | sort -u > recon/nmap_targets.txt
    cp recon/open_ports_raw.txt recon/open_ports.txt # Keep original
    success "Targets sanitized."
else
    echo "$TARGET" > recon/nmap_targets.txt
    warn "No open ports found, scanning main target."
fi

info "Nmap: Detailed Analysis..."
if [ -s "recon/nmap_targets.txt" ]; then
    run_monitored "nmap -sS -sV -T4 -Pn -iL recon/nmap_targets.txt -oN recon/nmap_detailed.txt > /dev/null 2>&1"
else
    warn "Target list empty, skipping Nmap."
fi
success "Nmap Analysis Complete."

# ===================== [7] PHASE 3: CONTENT MINING =====================
section "PHASE 3: CONTENT DISCOVERY"
log "PHASE 3 START"

if validate_input "recon/web_active.txt" && check_tool "whatweb"; then
    info "WhatWeb: Tech Detect..."
    run_monitored "cat recon/web_active.txt | xargs whatweb --color=never --no-errors > recon/whatweb_results.txt 2>/dev/null"
    success "Tech Stack Identified."
fi

info "Mining Historical URLs..."
create_file "recon/all_urls_raw.txt"

if validate_input "recon/all_subdomains.txt"; then
    if command -v waybackurls &> /dev/null; then
        cat recon/all_subdomains.txt | waybackurls >> recon/all_urls_raw.txt 2>/dev/null
    fi
    if command -v gau &> /dev/null; then
        cat recon/all_subdomains.txt | gau >> recon/all_urls_raw.txt 2>/dev/null
    fi
fi

cat recon/all_urls_raw.txt | sort -u > recon/all_urls.txt
success "Mining Complete."

URL_COUNT=$(safe_count "recon/all_urls.txt")
echo -e "${GREEN}    >>> URLs Mined: ${BOLD}$URL_COUNT${RESET}"

grep "?" recon/all_urls.txt | grep "=" | sort -u > recon/params.txt
PARAM_COUNT=$(safe_count "recon/params.txt")
echo -e "${CYAN}    >>> Vulnerable Parameters: ${BOLD}$PARAM_COUNT${RESET}"

# ===================== [8] PHASE 4: VULNERABILITY ASSAULT =====================
section "PHASE 4: VULNERABILITY ASSAULT"
log "PHASE 4 START"
ensure_wordlist "$ROOT_DIR"

# 1. Nuclei
if validate_input "recon/web_active.txt" && check_tool "nuclei"; then
    info "Nuclei: Scanning ALL Targets..."
    run_monitored "nuclei -l recon/web_active.txt -severity low,medium,high,critical -silent -o vuln/nuclei_results.txt > /dev/null 2>&1"
    
    CRIT=$(grep -c "\[critical\]" vuln/nuclei_results.txt 2>/dev/null || echo 0)
    HIGH=$(grep -c "\[high\]" vuln/nuclei_results.txt 2>/dev/null || echo 0)
    TOTAL_NUCLEI=$(grep -c "\[" vuln/nuclei_results.txt 2>/dev/null || echo 0)
    
    # Sanitize just in case
    TOTAL_NUCLEI=$(echo "$TOTAL_NUCLEI" | tr -cd '0-9')
    if [ -z "$TOTAL_NUCLEI" ]; then TOTAL_NUCLEI=0; fi

    if [ "$TOTAL_NUCLEI" -gt 0 ]; then
         echo -e "${RED}    >>> Critical: $CRIT | High: $HIGH${RESET}"
         crit "Nuclei found vulnerabilities! Check 'vuln/nuclei_results.txt'"
    else
         clean "System Clean. No vulnerabilities found by Nuclei."
    fi
fi

# 2. Nikto
if validate_input "recon/web_active.txt" && check_tool "nikto"; then
    info "Nikto: Deep Server Scan (ALL)..."
    while read -r url; do
        run_monitored "nikto -h $url -maxtime 30m >> vuln/nikto_results.txt 2>/dev/null"
    done < recon/web_active.txt 
    
    if [ -s "vuln/nikto_results.txt" ]; then
         success "Nikto Scan Complete. Check 'vuln/nikto_results.txt'"
    else
         clean "Nikto found no obvious issues."
    fi
fi

# 3. Dalfox
if validate_input "recon/params.txt" && check_tool "dalfox"; then
    info "Dalfox: XSS Hunting (ALL PARAMS)..."
    run_monitored "cat recon/params.txt | dalfox pipe --silence --no-color > vuln/xss_results.txt 2>/dev/null"
    
    XSS_COUNT=$(safe_count "vuln/xss_results.txt")
    if [ "$XSS_COUNT" -gt 0 ]; then
        crit "XSS Found: $XSS_COUNT. Check 'vuln/xss_results.txt'"
    else
        clean "No XSS vulnerabilities found."
    fi
fi

# 4. Feroxbuster
if validate_input "recon/web_active.txt" && check_tool "feroxbuster"; then
    info "Feroxbuster: Fuzzing ALL Directories (Deep)..."
    while read -r url; do
        safe_url=${url//\//_}
        run_monitored "feroxbuster --url $url --wordlist $ROOT_DIR/wordlists/common.txt --depth 2 --time-limit 30m --silent --dont-filter --no-state --output fuzzing/ferox_$safe_url.txt > /dev/null 2>&1"
    done < recon/web_active.txt
    cat fuzzing/ferox_*.txt > fuzzing/ferox_all_results.txt 2>/dev/null
    success "Fuzzing Complete."
fi

# ===================== [9] PHASE 5: DEEP EXPLOITATION =====================
section "PHASE 5: DEEP EXPLOITATION"
log "PHASE 5 START"

# 1. SQLMap (Refined Logic: Active Crawl + Param Test)
if check_tool "sqlmap"; then
    info "SQLMap: Initiating Deep Injection Protocols..."

    # Sub-routine A: Crawl Active Targets (Finding new injection points)
    if validate_input "recon/web_active.txt"; then
        info "SQLMap: [MODE: CRAWL] Hunting on Active Targets..."
        # --crawl=3: Go 3 links deep
        # --forms: Check login/search forms
        # --smart: Only test promising parameters to save time
        run_monitored "sqlmap -m recon/web_active.txt --batch --crawl=3 --level=2 --risk=2 --random-agent --forms --threads=4 --smart --answers='keep testing=Y' --results-file=$ROOT_DIR/vuln/sqlmap/crawl_results.csv > logs/sqlmap_crawl_debug.log 2>&1"
    else
        warn "SQLMap: No active web targets to crawl."
    fi

    # Sub-routine B: Test Known Parameters (Legacy/Direct mode)
    if validate_input "recon/params.txt"; then
        info "SQLMap: [MODE: DIRECT] Assaulting Known Parameters..."
        run_monitored "sqlmap -m recon/params.txt --batch --dbs --random-agent --level=2 --risk=2 --threads=4 --results-file=$ROOT_DIR/vuln/sqlmap/param_results.csv > logs/sqlmap_param_debug.log 2>&1"
    fi

    # Verification
    if [ -s "$ROOT_DIR/vuln/sqlmap/crawl_results.csv" ] || [ -s "$ROOT_DIR/vuln/sqlmap/param_results.csv" ]; then
        crit "SQL INJECTION CONFIRMED! Check 'vuln/sqlmap/' directory."
    else
        clean "No confirmed injections found in current assault phase."
    fi
else
    warn "SQLMap binary missing. Skipping assault."
fi

# 2. Gitleaks
if check_tool "gitleaks"; then
    info "Gitleaks: Secret Scanning (ALL TARGETS)..."
    while read -r url; do
        run_monitored "curl -s $url | gitleaks detect --no-git --pipe -v >> vuln/secrets.txt 2>/dev/null"
    done < recon/web_active.txt 
    
    if [ -s "vuln/secrets.txt" ]; then
        crit "Secrets/Keys leaked! Check 'vuln/secrets.txt'"
    else
        clean "No leaked secrets detected."
    fi
fi

# 3. Exploit Mapping
if check_tool "searchsploit" && validate_input "vuln/nuclei_results.txt"; then
    info "Mapping Exploits (CVE to ExploitDB)..."
    grep -o "CVE-[0-9]\{4\}-[0-9]\+" vuln/nuclei_results.txt | sort -u > vuln/detected_cves.txt
    
    if [ -s "vuln/detected_cves.txt" ]; then
        create_file "exploits/possible_exploits.txt"
        while read -r cve; do
            echo "--- Exploits for $cve ---" >> exploits/possible_exploits.txt
            searchsploit "$cve" --www >> exploits/possible_exploits.txt 2>/dev/null
        done < vuln/detected_cves.txt
        success "Exploit Mapping Complete. Check 'exploits/possible_exploits.txt'"
    else
        clean "No CVEs found, so Exploit Search was skipped (Good News!)."
    fi
else
    clean "Exploit Search Skipped (No Vulnerability Data)."
fi

# ===================== [10] REPORT GENERATION =====================
section "PHASE 6: FINAL REPORTING"
log "PHASE 6 START"

REPORT_FILE="BANG_TITAN_REPORT.md"

cat > $REPORT_FILE << EOF
# 💀 BANG TITAN INTELLIGENCE REPORT (v30.5)
## Target: $TARGET
**Date:** $(date)
**Scanner:** BANG TITAN MAXIMUM (TOTAL WAR MODE)

## 📊 EXECUTIVE SUMMARY
| Metric | Count |
| :--- | :--- |
| **Subdomains Found** | $SUB_COUNT |
| **Active Web Targets** | $WEB_COUNT |
| **Vulnerable Params** | $PARAM_COUNT |
| **XSS Candidates** | ${XSS_COUNT:-0} |
| **Nuclei Critical** | $(grep -c "\[critical\]" vuln/nuclei_results.txt 2>/dev/null || echo 0) |
| **Nuclei High** | $(grep -c "\[high\]" vuln/nuclei_results.txt 2>/dev/null || echo 0) |

## 🏆 CRITICAL FINDINGS

### 1. SUBDOMAIN TAKEOVER (Subzy)
$(if [ -s "vuln/takeover_results.txt" ]; then cat vuln/takeover_results.txt; else echo "_No takeovers detected by Subzy._"; fi)

### 2. SQL INJECTION (SQLMap - Hybrid)
#### Crawl Results:
$(if [ -s "vuln/sqlmap/crawl_results.csv" ]; then cat vuln/sqlmap/crawl_results.csv; else echo "_No crawl injections._"; fi)
#### Parameter Results:
$(if [ -s "vuln/sqlmap/param_results.csv" ]; then cat vuln/sqlmap/param_results.csv; else echo "_No param injections._"; fi)

### 3. CRITICAL VULNERABILITIES (Nuclei)
\`\`\`
$(grep -E "critical|high" vuln/nuclei_results.txt 2>/dev/null | head -50 || echo "None.")
\`\`\`

### 4. XSS VULNERABILITIES (Dalfox)
\`\`\`
$(head -20 vuln/xss_results.txt 2>/dev/null || echo "None.")
\`\`\`

### 5. LEAKED SECRETS
\`\`\`
$(head -20 vuln/secrets.txt 2>/dev/null || echo "None.")
\`\`\`

### 6. EXPLOIT MAPPING
check 'exploits/possible_exploits.txt' for ExploitDB references.

## 📂 DATA ARTIFACTS
- Full Logs: \`logs/execution.log\`
- Process Monitor: \`logs/process_status.log\`
- Recon Data: \`recon/\`
- Vulnerability Data: \`vuln/\`
- Fuzzing Results: \`fuzzing/\`

EOF

success "MISSION ACCOMPLISHED. Report: $OUTPUT_DIR/$REPORT_FILE"

# ===================== [11] PHASE 7: LAZARUS AI INTEGRATION (NEW) =====================
# Header Phase 7 dihapus secara visual agar UI lebih bersih, tetapi fungsinya tetap berjalan di latar belakang.

# 1. Data Scrubbing (Privacy Cloak)
# Memanggil fungsi pembersihan sebelum mengirim data
SCRUBBED_FILE="scrubbed_data.tmp"
scrub_sensitive_data "$REPORT_FILE" "$SCRUBBED_FILE" "$TARGET"

# 2. Transmisi ke AI
# Menggunakan logika Tools Kedua yang telah disuntikkan
transmit_to_ai_core "$SCRUBBED_FILE"

# 3. Cleanup Temporary Scrubbed File
rm "$SCRUBBED_FILE"

echo -e "${RED}=========================================================${RESET}"
echo -e "${BOLD}SYSTEM SHUTDOWN. MEMORY FLUSHED.${RESET}"