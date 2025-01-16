import time
import subprocess
import re

# Hatalı girişleri izlemek için log dosyasının yolu
log_file = "/var/log/auth.log"

# Hatalı giriş sayısı
failed_attempts = 0

# Hatalı girişten sonra sistemin kapanacağı limit
max_failed_attempts = 3

# Root kullanıcısı için şifre hatalı girişlerini izleme
def check_failed_logins():
    global failed_attempts
    with open(log_file, "r") as f:
        logs = f.readlines()
    
    # Hatalı girişleri tespit et
    for line in logs:
        if "sshd" in line and "Failed password" in line and "root" in line:
            failed_attempts += 1

# Sistemi kapatma fonksiyonu
def shutdown_system():
    print("Too many failed login attempts. Shutting down the system.")
    subprocess.call(["shutdown", "-h", "now"])

# Ana fonksiyon
def main():
    global failed_attempts
    
    while True:
        # Log dosyasını her 10 saniyede bir kontrol et
        check_failed_logins()
        
        if failed_attempts >= max_failed_attempts:
            shutdown_system()
            break
        
        # Kontrol aralığını ayarla (10 saniye)
        time.sleep(10)

if __name__ == "__main__":
    main()
