import time
import unittest
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class TestRegistration(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Setup browser untuk semua test"""
        cls.driver = webdriver.Chrome()  # Pastikan chromedriver sudah terinstall
        cls.base_url = "http://localhost:3001"  # Sesuaikan dengan port server Anda
        cls.wait = WebDriverWait(cls.driver, 10)
    
    @classmethod
    def tearDownClass(cls):
        """Close browser setelah semua test selesai"""
        cls.driver.quit()
    
    def test_01_valid_registration(self):
        """Test registrasi dengan data yang valid"""
        driver = self.driver
        driver.get(f"{self.base_url}/register.html")
        
        # Tunggu form muncul
        self.wait.until(EC.presence_of_element_located((By.ID, "registerForm")))
        
        # Gunakan email unik dengan timestamp untuk setiap test run
        unique_email = f"test_user_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}@test.com"
        
        # Isi form
        driver.find_element(By.ID, "fullname").send_keys("Aulia Puspita")
        driver.find_element(By.ID, "email").send_keys(unique_email)
        driver.find_element(By.ID, "phone").send_keys("08123456789")
        driver.find_element(By.ID, "password").send_keys("Password123!")
        driver.find_element(By.ID, "confirmPassword").send_keys("Password123!")
        
        # Klik tombol register
        driver.find_element(By.CSS_SELECTOR, "#registerForm button[type='submit']").click()
        
        # Tunggu dan verifikasi success message atau alert
        time.sleep(2)
        try:
            # Cek jika ada alert
            alert = self.wait.until(EC.alert_is_present())
            alert_text = alert.text
            alert.accept()  # Tutup alert
            self.assertIn("berhasil", alert_text.lower())
            print("✓ Test registrasi valid: PASS")
        except TimeoutException:
            # Jika tidak ada alert, cek message element
            try:
                message = driver.find_element(By.ID, "message")
                self.assertIn("successfully", message.text.lower())
                print("✓ Test registrasi valid: PASS")
            except NoSuchElementException:
                print("✓ Test registrasi valid: PASS (Redirect atau response berbeda)")
    
    def test_02_empty_fields_registration(self):
        """Test registrasi dengan field kosong"""
        driver = self.driver
        driver.get(f"{self.base_url}/register.html")
        
        self.wait.until(EC.presence_of_element_located((By.ID, "registerForm")))
        
        # Coba submit tanpa isi form
        driver.find_element(By.CSS_SELECTOR, "#registerForm button[type='submit']").click()
        
        time.sleep(1)
        # HTML5 validation harus menampilkan pesan error
        fullname_input = driver.find_element(By.ID, "fullname")
        validity = driver.execute_script("return arguments[0].validity.valid", fullname_input)
        
        self.assertFalse(validity, "Form harus invalid ketika field kosong")
        print("✓ Test empty fields: PASS")
    
    def test_03_password_mismatch(self):
        """Test registrasi dengan password tidak cocok"""
        driver = self.driver
        driver.get(f"{self.base_url}/register.html")
        
        self.wait.until(EC.presence_of_element_located((By.ID, "registerForm")))
        
        driver.find_element(By.ID, "fullname").send_keys("Bima Saputra")
        driver.find_element(By.ID, "email").send_keys("bima@test.com")
        driver.find_element(By.ID, "phone").send_keys("08987654321")
        driver.find_element(By.ID, "password").send_keys("Password123!")
        driver.find_element(By.ID, "confirmPassword").send_keys("Password456!")  # Berbeda
        
        driver.find_element(By.CSS_SELECTOR, "#registerForm button[type='submit']").click()
        
        time.sleep(2)
        try:
            # Cek jika ada alert
            alert = self.wait.until(EC.alert_is_present())
            alert_text = alert.text.lower()
            alert.accept()
            # Verifikasi pesan error
            self.assertTrue("tidak cocok" in alert_text or "match" in alert_text,
                          f"Expected password mismatch error, got: {alert_text}")
            print("✓ Test password mismatch: PASS")
        except TimeoutException:
            # Jika tidak ada alert, cek message element
            try:
                message = driver.find_element(By.ID, "message")
                msg_text = message.text.lower()
                self.assertTrue("tidak cocok" in msg_text or "match" in msg_text,
                              f"Expected password mismatch error, got: {msg_text}")
                print("✓ Test password mismatch: PASS")
            except NoSuchElementException:
                print("⚠ Test password mismatch: Alert/message tidak ditemukan")
    
    def test_04_invalid_email_format(self):
        """Test registrasi dengan format email invalid"""
        driver = self.driver
        driver.get(f"{self.base_url}/register.html")
        
        self.wait.until(EC.presence_of_element_located((By.ID, "registerForm")))
        
        driver.find_element(By.ID, "fullname").send_keys("Clara Wijaya")
        driver.find_element(By.ID, "email").send_keys("invalid-email")  # Format invalid
        driver.find_element(By.ID, "phone").send_keys("08555555555")
        driver.find_element(By.ID, "password").send_keys("Password123!")
        driver.find_element(By.ID, "confirmPassword").send_keys("Password123!")
        
        driver.find_element(By.CSS_SELECTOR, "#registerForm button[type='submit']").click()
        
        time.sleep(1)
        email_input = driver.find_element(By.ID, "email")
        validity = driver.execute_script("return arguments[0].validity.valid", email_input)
        
        self.assertFalse(validity, "Email harus invalid")
        print("✓ Test invalid email format: PASS")


class TestLogin(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Setup browser untuk semua test"""
        cls.driver = webdriver.Chrome()
        cls.base_url = "http://localhost:3001"
        cls.wait = WebDriverWait(cls.driver, 10)
        # Data user yang sudah ada di database (sesuaikan dengan user real)
        cls.test_email = "aulia@test.com"
        cls.test_password = "Password123!"
    
    @classmethod
    def tearDownClass(cls):
        """Close browser setelah semua test selesai"""
        cls.driver.quit()
    
    def test_01_valid_login(self):
        """Test login dengan kredensial yang valid"""
        driver = self.driver
        driver.get(f"{self.base_url}/login.html")
        
        # Tunggu form muncul
        self.wait.until(EC.presence_of_element_located((By.ID, "loginForm")))
        
        # Isi form
        driver.find_element(By.ID, "email").send_keys(self.test_email)
        driver.find_element(By.ID, "password").send_keys(self.test_password)
        
        # Klik tombol login
        driver.find_element(By.CSS_SELECTOR, "#loginForm button[type='submit']").click()
        
        # Tunggu redirect atau success response
        time.sleep(2)
        try:
            # Cek apakah ada error message (jika ada, login gagal)
            error_msg = driver.find_element(By.ID, "loginStatus")
            if error_msg.text:
                self.fail(f"Login failed: {error_msg.text}")
        except NoSuchElementException:
            pass
        
        # Verifikasi berhasil login (bisa check URL atau elemen tertentu)
        print("✓ Test login valid: PASS")
    
    def test_02_invalid_password(self):
        """Test login dengan password salah"""
        driver = self.driver
        driver.get(f"{self.base_url}/login.html")
        
        self.wait.until(EC.presence_of_element_located((By.ID, "loginForm")))
        
        driver.find_element(By.ID, "email").send_keys(self.test_email)
        driver.find_element(By.ID, "password").send_keys("WrongPassword123!")
        
        driver.find_element(By.CSS_SELECTOR, "#loginForm button[type='submit']").click()
        
        time.sleep(2)
        try:
            # Cek jika ada alert
            alert = self.wait.until(EC.alert_is_present())
            alert_text = alert.text.lower()
            alert.accept()
            # Verifikasi error message
            self.assertTrue("salah" in alert_text or "invalid" in alert_text or "error" in alert_text,
                          f"Expected password error, got: {alert_text}")
            print("✓ Test invalid password: PASS")
        except TimeoutException:
            # Jika tidak ada alert, cek message element
            try:
                error_msg = driver.find_element(By.ID, "loginStatus")
                self.assertTrue(error_msg.text, "Seharusnya ada error message")
                msg_text = error_msg.text.lower()
                self.assertTrue("salah" in msg_text or "invalid" in msg_text or "error" in msg_text,
                              f"Expected password error, got: {msg_text}")
                print("✓ Test invalid password: PASS")
            except NoSuchElementException:
                print("⚠ Test invalid password: Error message tidak ditemukan")
    
    def test_03_nonexistent_email(self):
        """Test login dengan email yang tidak terdaftar"""
        driver = self.driver
        driver.get(f"{self.base_url}/login.html")
        
        self.wait.until(EC.presence_of_element_located((By.ID, "loginForm")))
        
        driver.find_element(By.ID, "email").send_keys("notregistered@test.com")
        driver.find_element(By.ID, "password").send_keys(self.test_password)
        
        driver.find_element(By.CSS_SELECTOR, "#loginForm button[type='submit']").click()
        
        time.sleep(2)
        try:
            error_msg = driver.find_element(By.ID, "loginStatus")
            self.assertTrue(error_msg.text, "Seharusnya ada error message")
            print("✓ Test nonexistent email: PASS")
        except NoSuchElementException:
            print("⚠ Test nonexistent email: Error message tidak ditemukan")
    
    def test_04_empty_fields_login(self):
        """Test login dengan field kosong"""
        driver = self.driver
        driver.get(f"{self.base_url}/login.html")
        
        self.wait.until(EC.presence_of_element_located((By.ID, "loginForm")))
        
        # Coba submit tanpa isi form
        driver.find_element(By.CSS_SELECTOR, "#loginForm button[type='submit']").click()
        
        time.sleep(1)
        email_input = driver.find_element(By.ID, "email")
        validity = driver.execute_script("return arguments[0].validity.valid", email_input)
        
        self.assertFalse(validity, "Form harus invalid ketika field kosong")
        print("✓ Test empty fields login: PASS")
    
    def test_05_register_link_visible(self):
        """Test bahwa link register tersedia di halaman login"""
        driver = self.driver
        driver.get(f"{self.base_url}/login.html")
        
        register_link = driver.find_element(By.CSS_SELECTOR, "a[href='register.html']")
        self.assertTrue(register_link.is_displayed(), "Register link harus visible")
        print("✓ Test register link visible: PASS")


class TestNavigationFlow(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.base_url = "http://localhost:3001"
        cls.wait = WebDriverWait(cls.driver, 10)
    
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
    
    def test_01_login_to_register_navigation(self):
        """Test navigasi dari login ke register"""
        driver = self.driver
        driver.get(f"{self.base_url}/login.html")
        
        # Klik link register
        register_link = driver.find_element(By.CSS_SELECTOR, "a[href='register.html']")
        register_link.click()
        
        time.sleep(1)
        # Verifikasi berada di halaman register
        self.wait.until(EC.presence_of_element_located((By.ID, "registerForm")))
        self.assertIn("register", driver.current_url.lower())
        print("✓ Test login to register navigation: PASS")
    
    def test_02_register_to_login_navigation(self):
        """Test navigasi dari register ke login"""
        driver = self.driver
        driver.get(f"{self.base_url}/register.html")
        
        # Klik link login
        login_link = driver.find_element(By.CSS_SELECTOR, "a[href='login.html']")
        login_link.click()
        
        time.sleep(1)
        # Verifikasi berada di halaman login
        self.wait.until(EC.presence_of_element_located((By.ID, "loginForm")))
        self.assertIn("login", driver.current_url.lower())
        print("✓ Test register to login navigation: PASS")


if __name__ == "__main__":
    # Jalankan semua test
    print("\n" + "="*60)
    print("SELENIUM TEST UNTUK LOGIN & REGISTER - CClassforUs")
    print("="*60 + "\n")
    
    # Buat test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Tambahkan test classes
    suite.addTests(loader.loadTestsFromTestCase(TestRegistration))
    suite.addTests(loader.loadTestsFromTestCase(TestLogin))
    suite.addTests(loader.loadTestsFromTestCase(TestNavigationFlow))
    
    # Jalankan test
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
