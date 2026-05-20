import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Jalankan Chrome
driver = webdriver.Chrome()

# Buka website Edlink
driver.get("https://edlink.id/login")

# Perbesar window
driver.maximize_window()

# Tunggu halaman termuat
wait = WebDriverWait(driver, 20)

# Cari input email
email_input = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, '//input[@type="email"]')
    )
)

# Cari input password
password_input = driver.find_element(
    By.XPATH,
    '//input[@type="password"]'
)

# Isi email
email_input.send_keys("indahdivagracia@gmail.com")

# Isi password
password_input.send_keys("714230039")

# Tekan ENTER
password_input.send_keys(Keys.ENTER)

# Tunggu beberapa detik
time.sleep(10)

# Print title halaman
print("Judul halaman:", driver.title)

# Jangan ditutup dulu
input("Tekan ENTER untuk menutup browser...")

driver.quit()