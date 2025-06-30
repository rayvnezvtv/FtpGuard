# network_scanner.py

import platform
import subprocess
import socket
from concurrent.futures import ThreadPoolExecutor
from logger import log_action, log_error

def get_local_ip_prefix():
    """Retourne le préfixe réseau local automatiquement."""
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        prefix = ".".join(local_ip.split(".")[:3]) + "."
        return prefix
    except Exception as e:
        log_error(f"get_local_ip_prefix failed: {e}")
        return "192.168.1."  # fallback par défaut

def ping_host(ip):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    try:
        result = subprocess.run(["ping", param, "1", ip], stdout=subprocess.DEVNULL)
        if result.returncode == 0:
            log_action("PING_OK", ip)
            return ip
    except Exception as e:
        log_error(f"ping_host failed for {ip}: {e}")
    return None

def port_scan(ip, ports=[21, 22, 80, 443]):
    open_ports = []
    for port in ports:
        try:
            with socket.create_connection((ip, port), timeout=1):
                open_ports.append(port)
        except:
            continue
    if open_ports:
        log_action("OPEN_PORTS", f"{ip}: {open_ports}")
    return open_ports

def scan_network(portscan=False):
    """Scan automatique du réseau local de la machine."""
    base_ip = get_local_ip_prefix()
    print(f"🔍 Scan réseau automatique sur {base_ip}0/24...")

    active_hosts = []
    try:
        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(ping_host, f"{base_ip}{i}") for i in range(1, 255)]
            for future in futures:
                result = future.result()
                if result:
                    active_hosts.append(result)

        print(f"✅ {len(active_hosts)} hôtes actifs détectés.")

        if portscan:
            print("🎯 Scan de ports en cours...")
            for ip in active_hosts:
                ports = port_scan(ip)
                if ports:
                    print(f"{ip} ➜ ports ouverts : {ports}")

    except Exception as e:
        log_error(f"scan_network failed: {e}")

    return active_hosts
