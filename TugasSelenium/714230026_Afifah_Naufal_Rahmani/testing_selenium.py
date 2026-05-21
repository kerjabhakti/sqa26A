from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# membuka browser chrome
driver = webdriver.Chrome()

# membuka website
driver.get("https://rapat-in.vercel.app/")

# fullscreen browser
driver.maximize_window()

# tunggu 3 detik
time.sleep(3)

# menampilkan title website
print("Judul Website :", driver.title)

# contoh klik tombol login
try:
    tombol_login = driver.find_element(By.TAG_NAME, "button")
    tombol_login.click()

    print("Tombol berhasil diklik")

except:
    print("Tombol login tidak ditemukan")

# tunggu sebentar
time.sleep(5)

# tutup browser
driver.quit()