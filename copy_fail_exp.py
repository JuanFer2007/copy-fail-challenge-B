import socket
print("[+] Ejecutando exploit en Python (MicroPython)...")
try:
    # Intento de apertura de socket crudo para el ataque
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    print("[+] Socket abierto. El kernel parcheado deberia bloquear valores lmax invalidos.")
except Exception as e:
    print("[-] El sistema bloqueo la operacion o falta soporte de socket:", e)
print("[+] Prueba finalizada.")
