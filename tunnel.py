daemon=True),
                threading.Thread(target=start_receiver, args=(session,), daemon=True),
                threading.Thread(target=connection_monitor, args=(REMOTE_TUNNEL_IP,), daemon=True)
            ]
            
            for t in threads:
                t.start()
            
            # Не даем программе закрыться
            while True:
                time.sleep(1)
                
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n[!] Выход...")
    except Exception as e:
        print(Fore.RED + f"[ОШИБКА]: {e}")