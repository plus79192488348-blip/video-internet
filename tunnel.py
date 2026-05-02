import os
import sys
import threading
import time
from scapy.all import Ether, IP, UDP, Raw, sendp, sniff
from colorama import init, Fore

# --- НАСТРОЙКИ ---
# Имя твоей реальной карты (из Сетевых подключений)
PHYSICAL_IFACE = "Ethernet 2" 
# Твой реальный IP адрес (для теста на одном ПК)
REMOTE_PHYSICAL_IP = "127.0.0.1" 

TUNNEL_IP = "10.0.0.1"
REMOTE_TUNNEL_IP = "10.0.0.2"
VIDEO_PORT = 5004
ADAPTER_NAME = "VideoTunnel"
MTU_VALUE = 1400

init(autoreset=True)

def setup_system():
    """Настройка виртуального адаптера через команды Windows"""
    print(Fore.CYAN + f"[*] Настройка сети {ADAPTER_NAME}...")
    time.sleep(3)
    
    # Мы используем \" чтобы Windows понимала имена с пробелами
    cmd_ip = f'netsh interface ipv4 set address name=\"{ADAPTER_NAME}\" static {TUNNEL_IP} 255.255.255.0'
    cmd_mtu = f'netsh interface ipv4 set subinterface \"{ADAPTER_NAME}\" mtu={MTU_VALUE} store=persistent'
    
    res1 = os.system(cmd_ip)
    res2 = os.system(cmd_mtu)
    
    if res1 == 0 and res2 == 0:
        print(Fore.GREEN + f"[+] Сеть настроена успешно! IP: {TUNNEL_IP}")
    else:
        print(Fore.RED + "[-] Ошибка при настройке. Запусти от АДМИНИСТРАТОРА!")

def start_sender():
    """Поток для отправки данных (заглушка)"""
    print(Fore.WHITE + "[SENDER] Поток отправки готов.")
    while True:
        time.sleep(1)

def start_receiver():
    """Поток для приема данных через видео-порт"""
    print(Fore.WHITE + "[RECEIVER] Поток приема слушает порт 5004.")
    try:
        sniff(iface=PHYSICAL_IFACE, filter=f"udp port {VIDEO_PORT}", prn=lambda x: print(Fore.MAGENTA + "[!] Поймали видео-фрейм!"), store=0)
    except Exception as e:
        print(Fore.RED + f"[!] Ошибка захвата на {PHYSICAL_IFACE}: {e}")

if __name__ == "__main__":
    print(Fore.YELLOW + "=== ПОЛНОЦЕННЫЙ ВИДЕО-ТУННЕЛЬ ЗАПУЩЕН ===")
    
    # Запускаем логику в разных потоках
    t1 = threading.Thread(target=start_sender, daemon=True)
    t2 = threading.Thread(target=start_receiver, daemon=True)
    t1.start()
    t2.start()
    
    # Пытаемся настроить систему
    setup_system()
    
    print(Fore.YELLOW + "\nПрограмма работает. Нажми Ctrl+C для выхода.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(Fore.RED + "Выход из программы...")
