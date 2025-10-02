import requests
import os
import random
import re
import threading
import urllib.request
import argparse
import sys
import socks
import socket
from colorama import Fore, Back, Style, init
from time import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import json

init(autoreset=True)

# User agents for downloading and checking proxies
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15",
]

output_file = 'proxy.txt'
checked_output_file = 'proxy_checked.txt' # New file for checked proxies

os.system('cls' if os.name == 'nt' else 'clear')

# Display banner
print(f"{Fore.CYAN}{Style.BRIGHT}┌──────────────────────────────────────────────┐")
print(f"{Fore.CYAN}{Style.BRIGHT}│           Proxy Scraper by xAI               │")
print(f"{Fore.CYAN}{Style.BRIGHT}│  Collect HTTP, HTTPS, SOCKS4, SOCKS5 Proxies  │")
print(f"{Fore.CYAN}{Style.BRIGHT}└──────────────────────────────────────────────┘{Style.RESET_ALL}")

# Delete existing files
for file_to_delete in [output_file, checked_output_file]:
    if os.path.isfile(file_to_delete):
        os.remove(file_to_delete)
        print(f"{Fore.RED}Deleted existing '{file_to_delete}'.{Style.RESET_ALL}")

print(f"{Fore.YELLOW}Starting proxy download...{Style.RESET_ALL}")

# Number of worker threads for concurrent downloading
num_workers = 50 # Increased workers for faster download

# Combined and deduplicated proxy URLs (HTTP, HTTPS, SOCKS4, SOCKS5)
proxy_urls = list(set([
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=1000&country=all",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://www.proxy-list.download/api/v1/get?type=http",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
    "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/http/http.txt",
    "https://advanced.name/freeproxy/688992cc37a4f",
    "https://raw.githubusercontent.com/prxchk/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/proxylist-to/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/yuceltoluyag/GoodProxy/main/raw.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/https.txt",
    "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/http_proxies.txt",
    "https://raw.githubusercontent.com/opsxcq/proxy-list/master/list.txt",
    "https://api.openproxylist.xyz/http.txt",
    "https://api.proxyscrape.com/v2/?request=displayproxies",
    "https://api.proxyscrape.com/?request=displayproxies&proxytype=http",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
    "https://www.proxydocker.com/en/proxylist/download?email=noshare&country=all&city=all&port=all&type=all&anonymity=all&state=all&need=all",
    "https://proxyspace.pro/http.txt",
    "https://proxy-spider.com/api/proxies.example.txt",
    "https://cdn.jsdelivr.net/gh/aslisk/proxyhttps/https.txt",
    "https://cdn.jsdelivr.net/gh/hendrikbgr/Free-Proxy-Repo/proxy_list.txt",
    "https://cdn.jsdelivr.net/gh/prxchk/proxy-list/http.txt",
    "https://cdn.jsdelivr.net/gh/jetkai/proxy-list/online-proxies/txt/proxies-http.txt",
    "https://cdn.jsdelivr.net/gh/mmpx12/proxy-list/https.txt",
    "https://cdn.jsdelivr.net/gh/ShiftyTR/Proxy-List/https.txt",
    "https://cdn.jsdelivr.net/gh/sunny9577/proxy-scraper/proxies.txt",
    "http://rootjazz.com/proxies/proxies.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies.txt",
    "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=anonymous",
    "http://free-proxy.cz/en/web-proxylist/",
    "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/http/data.txt",
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&country=all",
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=79990&country=all",
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=7990&country=all",
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=79999&country=all",
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=7991&country=all",
    "https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/http.txt",
    "https://raw.githubusercontent.com/SevenworksDev/proxy-list/refs/heads/main/proxies/http.txt",
    "https://raw.githubusercontent.com/SevenworksDev/proxy-list/refs/heads/main/proxies/https.txt",
    "https://raw.githubusercontent.com/r00tee/Proxy-List/main/Https.txt",
    "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/http.txt",
    "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/https.txt",
    "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/https_proxies.txt",
    "https://sunny9577.github.io/proxy-scraper/proxies.txt",
    "https://sunny9577.github.io/proxy-scraper/generated/http_proxies.txt",
    "https://raw.githubusercontent.com/saisuiu/Lionkings-Http-Proxys-Proxies/main/free.txt",
    "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/https.txt",
    "https://raw.githubusercontent.com/tuanminpay/live-proxy/master/http.txt",
    "https://raw.githubusercontent.com/casals-ar/proxy-list/main/http",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/http.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/https.txt",
    "https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/http.txt",
    "http://atomintersoft.com/proxy_list_port_80",
    "http://atomintersoft.com/proxy_list_domain_org",
    "http://atomintersoft.com/proxy_list_port_3128",
    "http://browse.feedreader.com/c/Proxy_Server_List-1/449196258",
    "http://free-ssh.blogspot.com/feeds/posts/default",
    "http://browse.feedreader.com/c/Proxy_Server_List-1/449196259",
    "http://atomintersoft.com/transparent_proxy_list",
    "http://atomintersoft.com/anonymous_proxy_list",
    "http://atomintersoft.com/high_anonymity_elite_proxy_list",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http",
    "https://openproxylist.xyz/http.txt",
    "https://proxyspace.pro/https.txt",
    "https://raw.githubusercontent.com/almroot/proxylist/master/list.txt",
    "https://raw.githubusercontent.com/hanwayTech/free-proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/hanwayTech/free-proxy-list/main/https.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-https.txt",
    "https://spys.me/proxy.txt",
    "http://hack-hack.chat.ru/proxy/p4.txt",
    "https://github.com/themiralay/Proxy-List-World/raw/master/data.txt",
    "https://raw.githubusercontent.com/Tsprnay/Proxy-lists/master/proxies/all.txt",
    "https://github.com/TuanMinPay/live-proxy/raw/master/all.txt",
    "https://github.com/andigwandi/free-proxy/raw/main/proxy_list.txt",
    "https://github.com/MrMarble/proxy-list/raw/main/all.txt",
    "http://vipprox.blogspot.com/2013_06_01_archive.html",
    "http://vipprox.blogspot.com/2013/05/us-proxy-servers-74_24.html",
    "http://vipprox.blogspot.com/p/blog-page_7.html",
    "http://vipprox.blogspot.com/2013/05/us-proxy-servers-199_20.html",
    "http://vipprox.blogspot.com/2013_02_01_archive.html",
    "http://vipprox.blogspot.com/2013_03_01_archive.html",
    "http://sockproxy.blogspot.com/2013/04/11-04-13-socks-45.html",
    "http://proxyfirenet.blogspot.com/",
    "http://proxydb.net/",
    "http://olaf4snow.com/public/proxy.txt",
    "http://rammstein.narod.ru/proxy.html",
    "http://greenrain.bos.ru/R_Stuff/Proxy.htm",
    "http://inav.chat.ru/ftp/proxy.txt",
    "http://atomintersoft.com/products/alive-proxy/proxy-list/3128",
    "http://atomintersoft.com/products/alive-proxy/proxy-list/com",
    "http://atomintersoft.com/products/alive-proxy/proxy-list/high-anonymity/",
    "http://atomintersoft.com/proxy_list_domain_com",
    "http://atomintersoft.com/proxy_list_domain_edu",
    "http://atomintersoft.com/proxy_list_domain_net",
    "http://atomintersoft.com/proxy_list_port_8000",
    "http://atomintersoft.com/proxy_list_port_81",
    "http://hack-hack.chat.ru/proxy/allproxy.txt",
    "http://hack-hack.chat.ru/proxy/anon.txt",
    "http://hack-hack.chat.ru/proxy/p1.txt",
    "http://hack-hack.chat.ru/proxy/p2.txt",
    "http://hack-hack.chat.ru/proxy/p3.txt",
    "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/https/https.txt",
    "https://api.proxyscrape.com/?request=displayproxies&proxytype=socks5",
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=10000&country=all&simplified=true",
    "https://proxyspace.pro/socks5.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
    "http://atomintersoft.com/products/alive-proxy/socks5-list",
    "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks4.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/socks5.txt",
    "https://raw.githubusercontent.com/prxchk/proxy-list/main/socks5.txt",
    "https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/socks5.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks5.txt",
    "https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/SOCKS5.txt",
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks4",
    "https://api.proxyscrape.com/?request=displayproxies&proxytype=socks4&country=all",
    "https://api.openproxylist.xyz/socks4.txt",
    "https://proxyspace.pro/socks4.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks4.txt",
    "https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/SOCKS4.txt",
    "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks4.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/socks4.txt",
    "https://raw.githubusercontent.com/prxchk/proxy-list/main/socks4.txt",
    "https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/socks4.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt",
    "https://raw.githubusercontent.com/BreakingTechFr/Proxy_Free/main/proxies/http.txt",
    "https://raw.githubusercontent.com/BreakingTechFr/Proxy_Free/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/BreakingTechFr/Proxy_Free/main/proxies/socks5.txt",
    "https://sunny9577.github.io/proxy-scraper/generated/socks4_proxies.txt",
    "https://sunny9577.github.io/proxy-scraper/generated/socks5_proxies.txt",
    "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/socks4/socks4.txt",
    "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/socks5/socks5.txt",
    "https://raw.githubusercontent.com/Firdoxx/proxy-list/main/https",
    "https://raw.githubusercontent.com/Firdoxx/proxy-list/main/http",
    "https://raw.githubusercontent.com/Jakee8718/Free-Proxies/main/proxy/-http%20and%20https.txt",
    "https://raw.githubusercontent.com/Tsprnay/Proxy-lists/master/proxies/http.txt",
    "https://raw.githubusercontent.com/Tsprnay/Proxy-lists/master/proxies/https.txt",
    "https://raw.githubusercontent.com/a2u/free-proxy-list/master/free-proxy-list.txt",
    "https://raw.githubusercontent.com/mishakorzik/Free-Proxy/main/proxy.txt",
    "https://slims-sf.com/Htewarukofdcn/proxy.txt",
    "https://slims-sf.com/Htewarukofdcn/https.txt",
    "https://slims-sf.com/Htewarukofdcn/http.txt",
    "https://www.proxy-list.download/api/v1/get?type=socks5",
    "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc&protocols=http,https,socks4,socks5",
    "https://api.openproxylist.xyz/https.txt",
    "https://www.proxy-list.download/api/v1/get?type=https",
    "https://www.proxy-list.download/api/v1/get?type=socks4",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
    # Added some more sources
    "https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt",
    "https://raw.githubusercontent.com/saisuiu/Lionkings-Http-Proxys-Proxies/main/cnfree.txt",
    "https://raw.githubusercontent.com/saisuiu/Lionkings-Http-Proxys-Proxies/main/free.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/all.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/socks4.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/http.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/https.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/socks5.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_anonymous/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_anonymous/socks4.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_anonymous/socks5.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_geolocation/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_geolocation/socks4.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_geolocation/socks5.txt",
    "https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt",
    "https://raw.githubusercontent.com/yemixzy/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/yemixzy/proxy-list/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/yemixzy/proxy-list/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/all.txt",
    "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/socks4.txt",
    "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/socks5.txt",
    "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/http/http.txt",
    "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/https/https.txt",
    "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/socks4/socks4.txt",
    "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/socks5/socks5.txt",
    "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/socks4_proxies.txt",
    "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/socks5_proxies.txt",
    "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/http_proxies.txt",
    "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/https_proxies.txt",
    "https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/http.txt",
    "https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/https.txt",
    "https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/socks4.txt",
    "https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/socks5.txt",
    "https://raw.githubusercontent.com/prxchk/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/prxchk/proxy-list/main/socks4.txt",
    "https://raw.githubusercontent.com/prxchk/proxy-list/main/socks5.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt",
    "https://raw.githubusercontent.com/hendrikbgr/Free-Proxy-Repo/master/proxy_list.txt",
    "https://raw.githubusercontent.com/aslisk/proxyhttps/main/https.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-https.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks4.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks5.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/https.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks4.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks5.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/https.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
    "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt",
    "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/generated/http_proxies.txt",
    "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/generated/socks4_proxies.txt",
    "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/generated/socks5_proxies.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_anonymous/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_anonymous/socks4.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_anonymous/socks5.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_geolocation/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_geolocation/socks4.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_geolocation/socks5.txt",
    "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/http.txt",
    "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/https.txt",
    "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/SevenworksDev/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/SevenworksDev/proxy-list/main/proxies/https.txt",
    "https://raw.githubusercontent.com/SevenworksDev/proxy-list/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/SevenworksDev/proxy-list/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/r00tee/Proxy-List/main/Http.txt",
    "https://raw.githubusercontent.com/r00tee/Proxy-List/main/Https.txt",
    "https://raw.githubusercontent.com/r00tee/Proxy-List/main/Socks4.txt",
    "https://raw.githubusercontent.com/r00tee/Proxy-List/main/Socks5.txt",
    "https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/HTTP.txt",
    "https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/HTTPS.txt",
    "https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/SOCKS4.txt",
    "https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/SOCKS5.txt",
    "https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/socks4.txt",
    "https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/socks5.txt",
    "https://raw.githubusercontent.com/hanwayTech/free-proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/hanwayTech/free-proxy-list/main/https.txt",
    "https://raw.githubusercontent.com/hanwayTech/free-proxy-list/main/socks4.txt",
    "https://raw.githubusercontent.com/hanwayTech/free-proxy-list/main/socks5.txt",
    "https://raw.githubusercontent.com/tuanminpay/live-proxy/master/http.txt",
    "https://raw.githubusercontent.com/tuanminpay/live-proxy/master/socks4.txt",
    "https://raw.githubusercontent.com/tuanminpay/live-proxy/master/socks5.txt",
    "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/http.txt",
    "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/https.txt",
    "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/socks4.txt",
    "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/socks5.txt",
    "https://raw.githubusercontent.com/saisuiu/Lionkings-Http-Proxys-Proxies/main/free.txt",
    "https://raw.githubusercontent.com/saisuiu/Lionkings-Http-Proxys-Proxies/main/cnfree.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/all.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/http.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/https.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/socks4.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/socks5.txt",
    "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/all.txt",
    "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/http_proxies.txt",
    "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/https_proxies.txt",
    "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/socks4_proxies.txt",
    "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/socks5_proxies.txt",
    "https://raw.githubusercontent.com/almroot/proxylist/master/list.txt",
    "https://raw.githubusercontent.com/opsxcq/proxy-list/master/list.txt",
    "https://raw.githubusercontent.com/a2u/free-proxy-list/master/free-proxy-list.txt",
    "https://raw.githubusercontent.com/mishakorzik/Free-Proxy/main/proxy.txt",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
    "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/all.txt",
    "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/socks4.txt",
    "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/socks5.txt",
    "https://raw.githubusercontent.com/yemixzy/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/yemixzy/proxy-list/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/yemixzy/proxy-list/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt",
    "https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/http/data.txt",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/socks4/data.txt",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/socks5/data.txt",
    "https://raw.githubusercontent.com/casals-ar/proxy-list/main/http",
    "https://raw.githubusercontent.com/casals-ar/proxy-list/main/https",
    "https://raw.githubusercontent.com/casals-ar/proxy-list/main/socks4",
    "https://raw.githubusercontent.com/casals-ar/proxy-list/main/socks5",
    "https://raw.githubusercontent.com/Firdoxx/proxy-list/main/http",
    "https://raw.githubusercontent.com/Firdoxx/proxy-list/main/https",
    "https://raw.githubusercontent.com/Firdoxx/proxy-list/main/socks4",
    "https://raw.githubusercontent.com/Firdoxx/proxy-list/main/socks5",
    "https://raw.githubusercontent.com/Jakee8718/Free-Proxies/main/proxy/-http%20and%20https.txt",
    "https://raw.githubusercontent.com/Jakee8718/Free-Proxies/main/proxy/-socks4.txt",
    "https://raw.githubusercontent.com/Jakee8718/Free-Proxies/main/proxy/-socks5.txt",
    "https://raw.githubusercontent.com/Tsprnay/Proxy-lists/master/proxies/all.txt",
    "https://raw.githubusercontent.com/Tsprnay/Proxy-lists/master/proxies/http.txt",
    "https://raw.githubusercontent.com/Tsprnay/Proxy-lists/master/proxies/https.txt",
    "https://raw.githubusercontent.com/Tsprnay/Proxy-lists/master/proxies/socks4.txt",
    "https://raw.githubusercontent.com/Tsprnay/Proxy-lists/master/proxies/socks5.txt",
    "https://raw.githubusercontent.com/BreakingTechFr/Proxy_Free/main/proxies/http.txt",
    "https://raw.githubusercontent.com/BreakingTechFr/Proxy_Free/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/BreakingTechFr/Proxy_Free/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/http.txt",
    "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/https.txt",
    "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks4.txt",
    "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks5.txt",
    "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/andigwandi/free-proxy/main/proxy_list.txt",
    "https://raw.githubusercontent.com/MrMarble/proxy-list/main/all.txt",
    "https://raw.githubusercontent.com/themiralay/Proxy-List-World/master/data.txt",
    "https://raw.githubusercontent.com/TuanMinPay/live-proxy/master/all.txt",
    # Adding more specific API calls for variety
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=elite",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=anonymous",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=https&timeout=10000&country=all&ssl=all&anonymity=elite",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=https&timeout=10000&country=all&ssl=all&anonymity=anonymous",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=10000&country=all",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=10000&country=all",
    "https://www.proxy-list.download/api/v1/get?type=http&anon=elite",
    "https://www.proxy-list.download/api/v1/get?type=http&anon=anonymous",
    "https://www.proxy-list.download/api/v1/get?type=https&anon=elite",
    "https://www.proxy-list.download/api/v1/get?type=https&anon=anonymous",
    "https://www.proxy-list.download/api/v1/get?type=socks4",
    "https://www.proxy-list.download/api/v1/get?type=socks5",
    "https://api.openproxylist.xyz/http.txt",
    "https://api.openproxylist.xyz/https.txt",
    "https://api.openproxylist.xyz/socks4.txt",
    "https://api.openproxylist.xyz/socks5.txt",
    "https://openproxylist.xyz/http.txt",
    "https://openproxylist.xyz/https.txt",
    "https://openproxylist.xyz/socks4.txt",
    "https://openproxylist.xyz/socks5.txt",
    # Adding more sources from different providers
    "https://raw.githubusercontent.com/proxylist-to/proxy-list/main/https.txt", # Might be 404, handled
    "https://raw.githubusercontent.com/proxylist-to/proxy-list/main/socks4.txt",
    "https://raw.githubusercontent.com/proxylist-to/proxy-list/main/socks5.txt",
    "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
    "https://raw.githubusercontent.com/manuGMG/proxy-365/main/SOCKS5.txt",
    "https://raw.githubusercontent.com/manuGMG/proxy-365/main/SOCKS4.txt",
    "https://raw.githubusercontent.com/manuGMG/proxy-365/main/HTTP.txt",
    "https://raw.githubusercontent.com/manuGMG/proxy-365/main/HTTPS.txt",
    "https://raw.githubusercontent.com/BlackSnowDot/proxylist-update-every-minute/main/http.txt",
    "https://raw.githubusercontent.com/BlackSnowDot/proxylist-update-every-minute/main/socks4.txt",
    "https://raw.githubusercontent.com/BlackSnowDot/proxylist-update-every-minute/main/socks5.txt",
    "https://raw.githubusercontent.com/BlackSnowDot/proxylist-update-every-minute/main/https.txt",
    "https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/http.txt",
    "https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/socks4.txt",
    "https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/socks5.txt",
    "https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/https.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/ALL_RAW.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTP_RAW.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
    # Adding some less common but potentially useful sources
    "https://raw.githubusercontent.com/uptimerbot/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/uptimerbot/proxy-list/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/uptimerbot/proxy-list/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/uptimerbot/proxy-list/main/proxies/https.txt",
    "https://raw.githubusercontent.com/uptimerbot/proxy-list/main/proxies_anonymous/http.txt",
    "https://raw.githubusercontent.com/uptimerbot/proxy-list/main/proxies_anonymous/socks4.txt",
    "https://raw.githubusercontent.com/uptimerbot/proxy-list/main/proxies_anonymous/socks5.txt",
    "https://raw.githubusercontent.com/uptimerbot/proxy-list/main/proxies_geolocation/http.txt",
    "https://raw.githubusercontent.com/uptimerbot/proxy-list/main/proxies_geolocation/socks4.txt",
    "https://raw.githubusercontent.com/uptimerbot/proxy-list/main/proxies_geolocation/socks5.txt", # Might be 404, handled
    # Adding more sources from proxy-list.download with different parameters
    "https://www.proxy-list.download/api/v1/get?type=http&country=US",
    "https://www.proxy-list.download/api/v1/get?type=https&country=US",
    "https://www.proxy-list.download/api/v1/get?type=socks4&country=US",
    "https://www.proxy-list.download/api/v1/get?type=socks5&country=US",
    "https://www.proxy-list.download/api/v1/get?type=http&country=CN",
    "https://www.proxy-list.download/api/v1/get?type=https&country=CN", # Might be 429, handled
    "https://www.proxy-list.download/api/v1/get?type=socks4&country=CN",
    "https://www.proxy-list.download/api/v1/get?type=socks5&country=CN",
    "https://www.proxy-list.download/api/v1/get?type=http&country=RU",
    "https://www.proxy-list.download/api/v1/get?type=https&country=RU",
    "https://www.proxy-list.download/api/v1/get?type=socks4&country=RU",
    "https://www.proxy-list.download/api/v1/get?type=socks5&country=RU",
    # Adding more sources from proxyscrape with different parameters
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=5000&country=US&ssl=all&anonymity=all",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=https&timeout=5000&country=US&ssl=all&anonymity=all",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=5000&country=US",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=5000&country=US",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=5000&country=CN&ssl=all&anonymity=all",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=https&timeout=5000&country=CN&ssl=all&anonymity=all",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=5000&country=CN",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=5000&country=CN",
    # Adding more sources from geonode with different parameters
    "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc&protocols=http",
    "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc&protocols=https",
    "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc&protocols=socks4",
    "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc&protocols=socks5",
    "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc&protocols=http,https",
    "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc&protocols=socks4,socks5",
    "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc&protocols=http,https,socks4,socks5&anonymityLevel=elite",
    "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc&protocols=http,https,socks4,socks5&anonymityLevel=anonymous",
    "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc&protocols=http,https,socks4,socks5&anonymityLevel=transparent",
    # Adding more sources from proxy-scraper with different parameters
    "https://sunny9577.github.io/proxy-scraper/proxies.txt",
    "https://sunny9577.github.io/proxy-scraper/generated/http_proxies.txt",
    "https://sunny9577.github.io/proxy-scraper/generated/https_proxies.txt",
    "https://sunny9577.github.io/proxy-scraper/generated/socks4_proxies.txt",
    "https://sunny9577.github.io/proxy-scraper/generated/socks5_proxies.txt",
    # Adding more sources from proxy-list-to with different parameters
    "https://raw.githubusercontent.com/proxylist-to/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/proxylist-to/proxy-list/main/https.txt", # Might be 404
    "https://raw.githubusercontent.com/proxylist-to/proxy-list/main/socks4.txt",
    "https://raw.githubusercontent.com/proxylist-to/proxy-list/main/socks5.txt",
    # Adding more sources from proxy4parsing with different parameters
    "https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/https.txt",
    "https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/socks4.txt",
    "https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/socks5.txt",
    # Adding more sources from jetkai with different parameters
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-https.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks4.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks5.txt",
    # Adding more sources from mmpx12 with different parameters
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/https.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks4.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks5.txt",
    # Adding more sources from ShiftyTR with different parameters
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt",
    # Adding more sources from TheSpeedX with different parameters
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/https.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
    # Adding more sources from sunny9577 with different parameters
    "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt",
    "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/generated/http_proxies.txt",
    "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/generated/https_proxies.txt",
    "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/generated/socks4_proxies.txt",
    "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/generated/socks5_proxies.txt",
    # Adding more sources from monosans with different parameters
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/https.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_anonymous/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_anonymous/https.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_anonymous/socks4.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_anonymous/socks5.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_geolocation/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_geolocation/https.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_geolocation/socks4.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_geolocation/socks5.txt",
    # Adding more sources from ErcinDedeoglu with different parameters
    "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/http.txt",
    "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/https.txt",
    "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/socks5.txt",
    # Adding more sources from SevenworksDev with different parameters
    "https://raw.githubusercontent.com/SevenworksDev/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/SevenworksDev/proxy-list/main/proxies/https.txt",
    "https://raw.githubusercontent.com/SevenworksDev/proxy-list/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/SevenworksDev/proxy-list/main/proxies/socks5.txt",
    # Adding more sources from r00tee with different parameters
    "https://raw.githubusercontent.com/r00tee/Proxy-List/main/Http.txt",
    "https://raw.githubusercontent.com/r00tee/Proxy-List/main/Https.txt",
    "https://raw.githubusercontent.com/r00tee/Proxy-List/main/Socks4.txt",
    "https://raw.githubusercontent.com/r00tee/Proxy-List/main/Socks5.txt",
    # Adding more sources from B4RC0DE-TM with different parameters
    "https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/HTTP.txt",
    "https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/HTTPS.txt",
    "https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/SOCKS4.txt",
    "https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/SOCKS5.txt",
    # Adding more sources from hanwayTech with different parameters
    "https://raw.githubusercontent.com/hanwayTech/free-proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/hanwayTech/free-proxy-list/main/https.txt",
    "https://raw.githubusercontent.com/hanwayTech/free-proxy-list/main/socks4.txt",
    "https://raw.githubusercontent.com/hanwayTech/free-proxy-list/main/socks5.txt",
    # Adding more sources from tuanminpay with different parameters
    "https://raw.githubusercontent.com/tuanminpay/live-proxy/master/http.txt",
    "https://raw.githubusercontent.com/tuanminpay/live-proxy/master/socks4.txt",
    "https://raw.githubusercontent.com/tuanminpay/live-proxy/master/socks5.txt",
    # Adding more sources from vakhov with different parameters
    "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/http.txt",
    "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/https.txt",
    "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/socks4.txt",
    "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/socks5.txt",
    # Adding more sources from saisuiu with different parameters
    "https://raw.githubusercontent.com/saisuiu/Lionkings-Http-Proxys-Proxies/main/free.txt",
    "https://raw.githubusercontent.com/saisuiu/Lionkings-Http-Proxys-Proxies/main/cnfree.txt",
    # Adding more sources from Zaeem20 with different parameters
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/all.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/http.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/https.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/socks4.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/socks5.txt",
    # Adding more sources from Anonym0usWork1221 with different parameters
    "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/all.txt",
    "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/http_proxies.txt",
    "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/https_proxies.txt",
    "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/socks4_proxies.txt",
    "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/socks5_proxies.txt",
    # Adding more sources from almroot with different parameters
    "https://raw.githubusercontent.com/almroot/proxylist/master/list.txt",
    # Adding more sources from opsxcq with different parameters
    "https://raw.githubusercontent.com/opsxcq/proxy-list/master/list.txt",
    # Adding more sources from a2u with different parameters
    "https://raw.githubusercontent.com/a2u/free-proxy-list/master/free-proxy-list.txt",
    # Adding more sources from mishakorzik with different parameters
    "https://raw.githubusercontent.com/mishakorzik/Free-Proxy/main/proxy.txt",
    # Adding more sources from clarketm with different parameters
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
    # Adding more sources from zevtyardt with different parameters
    "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/all.txt",
    "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/socks4.txt",
    "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/socks5.txt",
    # Adding more sources from yemixzy with different parameters
    "https://raw.githubusercontent.com/yemixzy/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/yemixzy/proxy-list/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/yemixzy/proxy-list/main/proxies/socks5.txt",
    # Adding more sources from mertguvencli with different parameters
    "https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt",
    # Adding more sources from UptimerBot with different parameters
    "https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/socks5.txt",
    # Adding more sources from proxifly with different parameters
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/http/data.txt",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/socks4/data.txt",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/socks5/data.txt",
    # Adding more sources from casals-ar with different parameters
    "https://raw.githubusercontent.com/casals-ar/proxy-list/main/http",
    "https://raw.githubusercontent.com/casals-ar/proxy-list/main/https",
    "https://raw.githubusercontent.com/casals-ar/proxy-list/main/socks4",
    "https://raw.githubusercontent.com/casals-ar/proxy-list/main/socks5",
    # Adding more sources from Firdoxx with different parameters
    "https://raw.githubusercontent.com/Firdoxx/proxy-list/main/http",
    "https://raw.githubusercontent.com/Firdoxx/proxy-list/main/https",
    "https://raw.githubusercontent.com/Firdoxx/proxy-list/main/socks4",
    "https://raw.githubusercontent.com/Firdoxx/proxy-list/main/socks5",
    # Adding more sources from Jakee8718 with different parameters
    "https://raw.githubusercontent.com/Jakee8718/Free-Proxies/main/proxy/-http%20and%20https.txt",
    "https://raw.githubusercontent.com/Jakee8718/Free-Proxies/main/proxy/-socks4.txt",
    "https://raw.githubusercontent.com/Jakee8718/Free-Proxies/main/proxy/-socks5.txt",
    # Adding more sources from Tsprnay with different parameters
    "https://raw.githubusercontent.com/Tsprnay/Proxy-lists/master/proxies/all.txt",
    "https://raw.githubusercontent.com/Tsprnay/Proxy-lists/master/proxies/http.txt",
    "https://raw.githubusercontent.com/Tsprnay/Proxy-lists/master/proxies/https.txt",
    "https://raw.githubusercontent.com/Tsprnay/Proxy-lists/master/proxies/socks4.txt",
    "https://raw.githubusercontent.com/Tsprnay/Proxy-lists/master/proxies/socks5.txt",
    # Adding more sources from BreakingTechFr with different parameters
    "https://raw.githubusercontent.com/BreakingTechFr/Proxy_Free/main/proxies/http.txt",
    "https://raw.githubusercontent.com/BreakingTechFr/Proxy_Free/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/BreakingTechFr/Proxy_Free/main/proxies/socks5.txt",
    # Adding more sources from MuRongPIG with different parameters
    "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/http.txt",
    "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/https.txt",
    "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks4.txt",
    "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks5.txt",
    # Adding more sources from rdavydov with different parameters
    "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/socks5.txt",
    # Adding more sources from andigwandi with different parameters
    "https://raw.githubusercontent.com/andigwandi/free-proxy/main/proxy_list.txt",
    # Adding more sources from MrMarble with different parameters
    "https://raw.githubusercontent.com/MrMarble/proxy-list/main/all.txt",
    # Adding more sources from themiralay with different parameters
    "https://raw.githubusercontent.com/themiralay/Proxy-List-World/master/data.txt",
    # Adding more sources from TuanMinPay with different parameters
    "https://raw.githubusercontent.com/TuanMinPay/live-proxy/master/all.txt",
    # Adding more sources from hookzof with different parameters
    "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
    # Adding more sources from manuGMG with different parameters
    "https://raw.githubusercontent.com/manuGMG/proxy-365/main/SOCKS5.txt",
    "https://raw.githubusercontent.com/manuGMG/proxy-365/main/SOCKS4.txt",
    "https://raw.githubusercontent.com/manuGMG/proxy-365/main/HTTP.txt",
    "https://raw.githubusercontent.com/manuGMG/proxy-365/main/HTTPS.txt",
    # Adding more sources from BlackSnowDot with different parameters
    "https://raw.githubusercontent.com/BlackSnowDot/proxylist-update-every-minute/main/http.txt",
    "https://raw.githubusercontent.com/BlackSnowDot/proxylist-update-every-minute/main/socks4.txt",
    "https://raw.githubusercontent.com/BlackSnowDot/proxylist-update-every-minute/main/socks5.txt",
    "https://raw.githubusercontent.com/BlackSnowDot/proxylist-update-every-minute/main/https.txt",
    # Adding more sources from saschazesiger with different parameters
    "https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/http.txt",
    "https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/socks4.txt",
    "https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/socks5.txt",
    "https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/https.txt",
    # Adding more sources from roosterkid with different parameters
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/ALL_RAW.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTP_RAW.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
    # Adding more sources from uptimerbot with different parameters
    "https://raw.githubusercontent.com/uptimerbot/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/uptimerbot/proxy-list/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/uptimerbot/proxy-list/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/uptimerbot/proxy-list/main/proxies/https.txt",
    "https://raw.githubusercontent.com/uptimerbot/proxy-list/main/proxies_anonymous/http.txt",
    "https://raw.githubusercontent.com/uptimerbot/proxy-list/main/proxies_anonymous/socks4.txt",
    "https://raw.githubusercontent.com/uptimerbot/proxy-list/main/proxies_anonymous/socks5.txt",
    "https://raw.githubusercontent.com/uptimerbot/proxy-list/main/proxies_geolocation/http.txt",
    "https://raw.githubusercontent.com/uptimerbot/proxy-list/main/proxies_geolocation/socks4.txt",
    "https://raw.githubusercontent.com/uptimerbot/proxy-list/main/proxies_geolocation/socks5.txt", # Might be 404

]))

# Thread lock for safe file writing
file_lock = threading.Lock()

# Global variables for progress tracking
total_urls = len(proxy_urls)
current_download = 0
success_count = 0
lock = threading.Lock()

# Global set to store unique proxies during download
unique_proxies = set()

def download_and_save_proxies(url, output_file, user_agents, unique_proxies_set):
    global current_download, success_count
    try:
        headers = {'User-Agent': random.choice(user_agents)}
        response = requests.get(url, timeout=15, headers=headers) # Increased timeout slightly
        with lock:
            current_download += 1
            current = current_download
        if response.status_code == 200:
            # Handle JSON response for geonode API
            if "geonode.com" in url and url.endswith("protocols=http,https,socks4,socks5"):
                try:
                    data = response.json()
                    proxies = [f"{item['ip']}:{item['port']}" for item in data.get('data', [])]
                    proxy_text = '\n'.join(proxies)
                except json.JSONDecodeError as e:
                    print(f"{Fore.RED}[{current}/{total_urls}] Failed: {Fore.WHITE}{url} (JSON Error: {str(e)}){Style.RESET_ALL}")
                    return False
            else:
                proxy_text = response.text

            # Deduplicate proxies before writing
            new_proxies = set()
            for line in proxy_text.strip().splitlines():
                line = line.strip()
                if line and re.match(r"\d{1,3}(?:\.\d{1,3}){3}(?::\d{1,5})?$", line):
                    new_proxies.add(line)

            # Add only new unique proxies to the global set and file
            unique_count = 0
            with file_lock:
                with open(output_file, 'a') as file:
                    for proxy in new_proxies:
                        if proxy not in unique_proxies_set:
                            unique_proxies_set.add(proxy)
                            file.write(proxy + '\n')
                            unique_count += 1

            print(f"{Fore.GREEN}[{current}/{total_urls}] Collected: {Fore.WHITE}{url} ({Fore.YELLOW}{unique_count} new{Fore.WHITE}){Style.RESET_ALL}")
            with lock:
                success_count += 1
            return True
        else:
            # Handle specific HTTP status codes for better UI
            status_color = Fore.RED
            if response.status_code == 404:
                status_color = Fore.MAGENTA
            elif response.status_code == 429:
                status_color = Fore.YELLOW
            print(f"{Fore.RED}[{current}/{total_urls}] Failed: {Fore.WHITE}{url} ({status_color}Status: {response.status_code}{Fore.RED}){Style.RESET_ALL}")
            return False
    except requests.exceptions.RequestException as e: # More specific exception handling
        with lock:
            current_download += 1 # Ensure counter is updated even on failure
        error_type = type(e).__name__
        if isinstance(e, requests.exceptions.Timeout):
            error_msg = "Timeout"
        elif isinstance(e, requests.exceptions.ConnectionError):
            error_msg = "Connection Error"
        else:
            error_msg = str(e)
        print(f"{Fore.RED}[{current_download}/{total_urls}] Failed: {Fore.WHITE}{url} ({Fore.CYAN}{error_type}: {error_msg}{Fore.RED}){Style.RESET_ALL}")
        return False
    except Exception as e: # Catch any other unexpected errors
        with lock:
            current_download += 1
        print(f"{Fore.RED}[{current_download}/{total_urls}] Failed: {Fore.WHITE}{url} ({Fore.CYAN}Unexpected Error: {str(e)}{Fore.RED}){Style.RESET_ALL}")
        return False

# Download proxies using a thread pool
print(f"{Fore.CYAN}Downloading from {total_urls} sources with {num_workers} workers...{Style.RESET_ALL}")

with ThreadPoolExecutor(max_workers=num_workers) as executor:
    # Submit all tasks
    future_to_url = {executor.submit(download_and_save_proxies, url, output_file, user_agents, unique_proxies): url for url in proxy_urls}
    # Wait for all tasks to complete (optional, as executor context manager handles this)
    for future in as_completed(future_to_url):
        url = future_to_url[future]
        try:
            future.result() # This will re-raise any exceptions caught in the thread
        except Exception as e:
            print(f"{Fore.RED}Exception occurred while processing {url}: {e}{Style.RESET_ALL}")

# Print download summary
print(f"\n{Fore.CYAN}Download Summary:{Style.RESET_ALL}")
print(f"{Fore.GREEN}Successful: {success_count} sources{Style.RESET_ALL}")
print(f"{Fore.RED}Failed: {total_urls - success_count} sources{Style.RESET_ALL}")

# Count proxies in the output file
try:
    with open(output_file, 'r') as ceki:
        jumlh = sum(1 for line in ceki if line.strip())
except FileNotFoundError:
    jumlh = 0

print(f"\n{Fore.CYAN}Total Unique Proxies Downloaded: {Fore.YELLOW}{jumlh}{Style.RESET_ALL}")

# --- Proxy Checking Section ---
class Proxy:
    def __init__(self, method, proxy):
        if method.lower() not in ["http", "https", "socks4", "socks5"]:
            raise NotImplementedError("Only HTTP, HTTPS, SOCKS4, and SOCKS5 are supported")
        self.method = method.lower()
        self.proxy = proxy
        # More robust IP:Port parsing
        match = re.match(r"(\d{1,3}(?:\.\d{1,3}){3}):(\d{1,5})", proxy)
        if match:
            self.ip, self.port = match.groups()
        else:
            # Handle cases where parsing might fail unexpectedly, though is_valid should catch most
            self.ip, self.port = proxy.split(":") if ":" in proxy else (proxy, "80")

    def is_valid(self):
        return re.match(r"\d{1,3}(?:\.\d{1,3}){3}(?::\d{1,5})?$", self.proxy)

    def check(self, site, timeout, user_agent):
        try:
            if self.method in ["http", "https"]:
                url = self.method + "://" + self.proxy
                proxy_support = urllib.request.ProxyHandler({self.method: url})
                opener = urllib.request.build_opener(proxy_support)
                urllib.request.install_opener(opener)
                req = urllib.request.Request(self.method + "://" + site)
                req.add_header("User-Agent", user_agent)
                start_time = time()
                urllib.request.urlopen(req, timeout=timeout)
                end_time = time()
                time_taken = end_time - start_time
                return True, time_taken, None
            elif self.method in ["socks4", "socks5"]:
                socks.set_default_proxy(
                    socks.SOCKS4 if self.method == "socks4" else socks.SOCKS5,
                    self.ip,
                    int(self.port)
                )
                # Store original socket
                original_socket = socket.socket
                socket.socket = socks.socksocket
                req = urllib.request.Request("http://" + site)
                req.add_header("User-Agent", user_agent)
                start_time = time()
                urllib.request.urlopen(req, timeout=timeout)
                end_time = time()
                time_taken = end_time - start_time
                # Restore original socket
                socket.socket = original_socket
                return True, time_taken, None
        except Exception as e:
            # Restore original socket in case of error for SOCKS
            if self.method in ["socks4", "socks5"]:
                socket.socket = socket.socket if 'original_socket' not in locals() else original_socket
            return False, 0, e

    def __str__(self):
        return self.proxy

def verbose_print(verbose, message):
    if verbose:
        print(message)

def check(file, timeout, method, site, verbose, random_user_agent, output_file):
    proxies = []
    seen_proxies = set() # Set to track duplicates within the input file
    duplicate_count = 0
    try:
        with open(file, "r") as f:
            for line in f:
                line = line.strip()
                if line and line not in seen_proxies: # Check for duplicates within the file
                    seen_proxies.add(line)
                    try:
                        proxies.append(Proxy(method, line))
                    except NotImplementedError as e:
                        verbose_print(verbose, f"{Fore.RED}Skipping invalid proxy format or method '{line}': {e}{Style.RESET_ALL}")
                elif line in seen_proxies:
                    duplicate_count += 1
    except FileNotFoundError:
        print(f"{Fore.RED}Error: File '{file}' not found.{Style.RESET_ALL}")
        return

    if duplicate_count > 0:
        print(f"{Fore.YELLOW}Removed {duplicate_count} duplicate proxies from input.{Style.RESET_ALL}")

    print(f"\n{Fore.GREEN}Checking {Fore.YELLOW}{len(proxies)} {Fore.GREEN}proxies...{Style.RESET_ALL}")
    proxies = list(filter(lambda x: x.is_valid(), proxies))
    if len(proxies) < len(seen_proxies):
        print(f"{Fore.YELLOW}Filtered out {(len(seen_proxies) - len(proxies))} invalid proxy formats.{Style.RESET_ALL}")

    valid_proxies = []
    user_agent = random.choice(user_agents)
    checked_count = 0
    lock = threading.Lock()

    def check_proxy(proxy, user_agent, valid_proxies_list, verbose):
        nonlocal checked_count
        new_user_agent = user_agent if not random_user_agent else random.choice(user_agents)
        valid, time_taken, error = proxy.check(site, timeout, new_user_agent)
        with lock:
            checked_count += 1
            progress = f"[{checked_count}/{len(proxies)}]"
        message = {
            True: f"{Fore.GREEN}{progress} {proxy} is valid, took {time_taken:.2f} seconds{Style.RESET_ALL}",
            False: f"{Fore.RED}{progress} {proxy} is invalid: {repr(error)}{Style.RESET_ALL}",
        }[valid]
        verbose_print(verbose, message)
        if valid:
            valid_proxies_list.append(proxy)

    threads = []
    for proxy in proxies:
        t = threading.Thread(target=check_proxy, args=(proxy, user_agent, valid_proxies, verbose))
        threads.append(t)
        t.start() # Start thread immediately

    for t in threads:
        t.join()

    # Deduplicate valid proxies before writing to the final file
    unique_valid_proxies = []
    seen_valid = set()
    for proxy in valid_proxies:
        proxy_str = str(proxy)
        if proxy_str not in seen_valid:
            seen_valid.add(proxy_str)
            unique_valid_proxies.append(proxy)

    with open(output_file, "w") as f: # Write to the new checked file
        for proxy in unique_valid_proxies:
            f.write(str(proxy) + "\n")

    print(f"\n{Fore.GREEN}Found {Fore.YELLOW}{len(unique_valid_proxies)} {Fore.GREEN}valid and unique proxies{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Saved to '{output_file}'{Style.RESET_ALL}")

# --- Main Execution Flow ---
print(f"{Fore.CYAN}Check proxies now? {Fore.WHITE}({Fore.GREEN}Y{Fore.WHITE}/{Fore.RED}N{Fore.WHITE}): ", end="")
choice = input().strip().lower()
if choice == 'y':
    parser = argparse.ArgumentParser(description="Proxy Scraper and Checker")
    parser.add_argument("-t", "--timeout", type=int, default=20, help="Dismiss the proxy after this many seconds")
    parser.add_argument("-p", "--proxy", default="http", help="Check HTTPS, HTTP, SOCKS4, or SOCKS5 proxies")
    parser.add_argument("-s", "--site", default="https://google.com", help="Check with specific website (e.g., https://google.com)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Increase output verbosity")
    parser.add_argument("-r", "--random-agent", action="store_true", help="Use a random user agent per proxy")
    args = parser.parse_args()

    # Pass the new output file name to the check function
    check(file=output_file, timeout=args.timeout, method=args.proxy, site=args.site, verbose=args.verbose, random_user_agent=args.random_agent, output_file=checked_output_file)
    print(f"\n{Fore.YELLOW}Thank you for using Proxy Scraper! Valid proxies are in '{checked_output_file}'.{Style.RESET_ALL}")
    sys.exit(0)
else:
    print(f"\n{Fore.YELLOW}Thank you for using Proxy Scraper! Downloaded proxies are in '{output_file}'.{Style.RESET_ALL}")
