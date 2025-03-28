import sys
import time
import random
import multiprocessing
import os
from colorama import Fore, Style
from itertools import cycle

def fake_download(file_size=3.67 * 1024, chunk_size=1024 * 50):
    spinner = cycle(["|", "/", "-", "\\"])
    downloaded = 0
    speed = random.randint(300, 1200)  # Kecepatan awal antara 300 KB/s - 1200 KB/s
    last_speed_change = time.time()

    while downloaded < file_size:
        if time.time() - last_speed_change > 2:  # Ganti kecepatan setiap 2 detik
            speed = random.randint(300, 1200)
            last_speed_change = time.time()

        time.sleep(chunk_size / (speed * 1024))  # Simulasi kecepatan download
        downloaded += chunk_size
        downloaded = min(downloaded, file_size)  # Pastikan tidak lebih dari total file
        percent = (downloaded / file_size) * 100
        sys.stdout.write(
            f"\rDownloading: {percent:.1f}% [{next(spinner)}] {downloaded // (1024 * 1024)}MB/{file_size // (1024 * 1024)}MB "
            f"({speed} KB/s)"
        )
        sys.stdout.flush()

    sys.stdout.write("\r\033[K")
    print("\033[1;32m✅ Download Completed!\033[0m")
    time.sleep(1)
    os.system('clear')

def loading_animation(durasi, jumlah_proses):
    frames = [".  ", ".. ", "..."]
    start_time = time.time()
    warning_shown = False  # Flag untuk peringatan

    while time.time() - start_time < durasi:
        if not warning_shown:
            sys.stdout.write("\033[32mRunning" + frames[int(time.time() * 3) % len(frames)] + "\r")
            sys.stdout.flush()
        
        time.sleep(0.3)

        try:
            running_procs = int(os.popen("pgrep -c .").read().strip())
        except ValueError:
            running_procs = 0

        if running_procs > jumlah_proses > 80 and not warning_shown:  # melebihi limit
            sys.stdout.write("\033[K")  # clear line
            sys.stdout.flush()
            print("\n\033[1;31m⚠️  WARNING: CPU usage is high (>80%)\033[0m")
            warning_shown = True

    sys.stdout.write("\033[K")
    print("\033[1;32m✔️ Done!\033[0m")

def cpu_test(durasi):
    start_time = time.time()
    while time.time() - start_time < durasi:
        for _ in range(10**6):  # Jangan dibesarkan angkanya (semakin besar semakin lama)
            pass
        time.sleep(0.01)

if __name__ == "__main__":
    print("Downloading Asset")
    fake_download()

    jumlah_core = multiprocessing.cpu_count() // 2  # Jika ingin extreme hapus "// 2"

    while True:
        try:
            os.system('figlet Cpu Test | lolcat')
            print(Fore.RED + Style.BRIGHT + "Made by ModderGabut24\n")
            print("Github: https://github.com/ModderGabut\n" + Fore.RESET)
            durasi = int(input(Fore.GREEN + Style.BRIGHT + "Masukkan durasi (detik): "))
            if durasi <= 0:
                raise ValueError
            break
        except ValueError:
            print("Masukkan angka yang valid untuk durasi!")

    while True:
        try:
            jumlah_proses = int(input(f"Masukkan jumlah proses (max {jumlah_core * 40}): "))
            if jumlah_proses <= 0 or jumlah_proses > jumlah_core * 40:
                raise ValueError
            break
        except ValueError:
            print(f"Masukkan jumlah antara 1 dan {jumlah_core * 40}!")

    print(f"\nMenjalankan {jumlah_proses} proses selama {durasi} detik...\n")

    loading_thread = multiprocessing.Process(target=loading_animation, args=(durasi, jumlah_proses))
    loading_thread.start()

    proses = []
    for _ in range(jumlah_proses):
        p = multiprocessing.Process(target=cpu_test, args=(durasi,))
        p.start()
        proses.append(p)

    for p in proses:
        p.join()

    loading_thread.join()
