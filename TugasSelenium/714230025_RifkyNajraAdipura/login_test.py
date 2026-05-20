import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# Membuka Chrome
driver = webdriver.Chrome()

# Membuka website login
driver.get("https://sentisynced.irc-enter.tech/login.php")

# Tunggu halaman terbuka
time.sleep(2)

# Input email
driver.find_element(By.ID, "email").send_keys("SuperAdmin@sentisynced.com")

# Input password
driver.find_element(By.ID, "password").send_keys("SuperAdmin123")

# Klik tombol login
driver.find_element(By.CLASS_NAME, "btn-login").click()

# Tunggu proses login
time.sleep(5)

# Validasi login berhasil
current_url = driver.current_url

if "dashboard" in current_url.lower():
    print("LOGIN BERHASIL")
else:
    print("LOGIN GAGAL")

# Tutup browser
driver.quit()