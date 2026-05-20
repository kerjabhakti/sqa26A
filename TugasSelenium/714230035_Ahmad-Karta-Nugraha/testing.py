import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# Inisialisasi WebDriver
driver = webdriver.Chrome()

# Membuka project web lokal
driver.get("http://127.0.0.1:8000")

# Maksimalkan browser
driver.maximize_window()

# Tunggu halaman load
time.sleep(3)

# Ambil judul halaman
page_title = driver.title
print("Judul halaman:", page_title)

# Validasi halaman berhasil dibuka
assert page_title != "", "Halaman gagal dibuka"

# Contoh cari elemen body
body = driver.find_element(By.TAG_NAME, "body")
assert body is not None

print("Pengujian Selenium berhasil")

# Tunggu sebentar
time.sleep(5)

# Tutup browser
driver.quit()