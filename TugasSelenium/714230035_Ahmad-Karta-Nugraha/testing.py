import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 15)

driver.get("https://moms-care-ten.vercel.app/index.html")
driver.maximize_window()

print("Halaman login:", driver.title)

# Klik ke halaman daftar
daftar_link = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'Daftar')]"))
)
daftar_link.click()

time.sleep(2)

email_baru = "ahmadtest999@gmail.com"
password_baru = "ibu123"

# Isi form daftar
wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Nama Ibu']"))
).send_keys("Ahmad Karta")

driver.find_element(By.CSS_SELECTOR, "input[type='email']").send_keys(email_baru)
driver.find_element(By.CSS_SELECTOR, "input[type='password']").send_keys(password_baru)
driver.find_element(By.CSS_SELECTOR, "input[type='date']").send_keys("2000-01-01")

# Klik daftar akun
btn_daftar = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'Daftar Akun')]"))
)
btn_daftar.click()

time.sleep(3)

# Balik ke login
login_link = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'Masuk ke Akun')]"))
)
login_link.click()

time.sleep(2)

# Login akun
email_login = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
)
email_login.clear()
email_login.send_keys(email_baru)

password_login = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
password_login.clear()
password_login.send_keys(password_baru)

# Submit login
password_login.send_keys(Keys.ENTER)

time.sleep(5)

print("URL akhir:", driver.current_url)
print("Judul akhir:", driver.title)
print("Pengujian daftar akun lalu login selesai")

time.sleep(3)
driver.quit()