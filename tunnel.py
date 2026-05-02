import os
import sys
import ctypes
import threading
import subprocess
import time
from scapy.all import Ether, IP, UDP, Raw, sendp, sniff
from colorama import init, Fore

# --- НАСТРОЙКИ ---
PHYSICAL_IFACE = "Ethernet"
REMOTE_PHYSICAL_IP = "192.168.1.50"
TUNNEL_IP = "10.0.0.1"
REMOTE_TUNNEL_IP = "10.0.0.2"
VIDEO_PORT = 5004
ADAPTER_NAME = "VideoTunnel"
MTU_VALUE = 1400

init(autoreset=True)

def setup_system(ip, adapter):
    print(Fore.CYAN + f"[*] Настройка адаптера {adapter}...")
    time.sleep(5)
    os.system(f'netsh interface ipv4 set address name="{adapter}" static {ip} 255.255.255.0')
    os.system(f'netsh interface ipv4 set subinterface "{adapter}" mtu={MTU_VALUE} store=persistent')
    print(Fore.GREEN + f"[+] Готово! IP: {ip}")

# ВНИМАНИЕ: Здесь мы грузим DLL напрямую без лишних библиотек
def load_wintun():
    dll_path = os.path.abspath("wintun.dll")
    if not os.path.exists(dll_path):
        print(Fore.RED + "[-] Ошибка: wintun.dll не найден!")
        return None
    return ctypes.WinDLL(dll_path)

if __name__ == "__main__":
    print(Fore.YELLOW + "=== VIDEO-TUNNEL (NO-LIB VERSION) ===")
    wintun_lib = load_wintun()
    if wintun_lib:
        print(Fore.GREEN + "[+] Драйвер Wintun подгружен напрямую.")
        # Тут просто заглушка для теста сборки
        print(Fore.WHITE + "Запуск настройки сети...")
        setup_system(TUNNEL_IP, ADAPTER_NAME)
        while True:
            time.sleep(1)
