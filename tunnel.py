import os
import sys
import threading
import time
from scapy.all import Ether, IP, UDP, Raw, sendp, sniff
from colorama import init, Fore

# --- НАСТРОЙКИ ---
PHYSICAL_IFACE = "Ethernet 2"       # Проверь имя своей карты в "Сетевых подключениях"
REMOTE_PHYSICAL_IP = "192.168.1.50" # IP второго компа
TUNNEL_IP = "10.0.0.1"             # Твой IP в туннеле
REMOTE_TUNNEL_IP = "10.0.0.2"      # IP соседа в туннеле
VIDEO_PORT = 5004
ADAPTER_NAME = "VideoTunnel"
MTU_VALUE = 1400

init(autoreset=True)

def setup_system():
    print(Fore.CYAN + f"[*] Настройка сети {ADAPTER_NAME}...")
    # Команды настройки (выполнятся только если запущен драйвер)
    os.system(f'netsh interface ipv4 set address name="{ADAPTER_NAME}" static {TUNNEL_IP} 255.255.255.0')
    os.system(f'netsh interface ipv4 set subinterface "{ADAPTER_NAME}" mtu={MTU_VALUE} store=persistent')

def start_sender():
    print(Fore.WHITE + "[SENDER] Поток отправки активен.")
    # Тут будет логика перехвата, пока просто заглушка для теста
    while True:
        time.sleep(1)

def start_receiver():
    print(Fore.WHITE + "[RECEIVER] Поток приема активен.")
    sniff(iface=PHYSICAL_IFACE, filter=f"udp port {VIDEO_PORT}", prn=lambda x: None, store=0)

if __name__ == "__main__":
    print(Fore.GREEN + "=== ПОЛНОЦЕННЫЙ ВИДЕО-ТУННЕЛЬ ЗАПУЩЕН ===")
    
    # Запускаем потоки
    t1 = threading.Thread(target=start_sender, daemon=True)
    t2 = threading.Thread(target=start_receiver, daemon=True)
    t1.start()
    t2.start()
    
    setup_system()
    
    print(Fore.YELLOW + "\nНажми Ctrl+C для выхода. Окно больше не закроется само!")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Выход...")
