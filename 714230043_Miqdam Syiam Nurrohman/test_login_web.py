"""
=============================================================
 PENGUJIAN SELENIUM WEBDRIVER - LOGIN VIA HALAMAN WEB
 Aplikasi: DompetKu (Catatan Keuangan Pribadi)
 Tester  : Miqdam Syiam Nurrohman (714230043)
=============================================================

Deskripsi:
    Script ini menguji fungsi Login pada halaman web login_page.html
    menggunakan Selenium WebDriver. Halaman web terhubung ke backend
    API DompetKu yang sudah di-hosting di Vercel.

Test Cases:
    1. Login berhasil dengan username & password valid
    2. Login gagal - username salah
    3. Login gagal - password salah
    4. Login gagal - field kosong (validasi client-side)
"""

import time
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# ===================== KONFIGURASI =====================
# Credential akun test yang sudah terdaftar di database
USERNAME_VALID = "Maiys"
PASSWORD_VALID = "Maiys0311"

# Path ke halaman login HTML
LOGIN_PAGE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "login_page.html")
LOGIN_PAGE_URL = "file:///" + LOGIN_PAGE_PATH.replace("\\", "/")

# Waktu tunggu maksimal untuk response API (detik)
WAIT_TIMEOUT = 15


# ===================== HELPER FUNCTIONS =====================
def setup_driver():
    """Inisialisasi Chrome WebDriver menggunakan webdriver-manager."""
    options = webdriver.ChromeOptions()
    # Uncomment baris di bawah jika ingin menjalankan tanpa GUI (headless)
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(5)
    return driver


def clear_and_type(element, text):
    """Hapus isi field lalu ketik teks baru."""
    element.clear()
    element.send_keys(text)


def wait_for_result(driver, timeout=WAIT_TIMEOUT):
    """Tunggu sampai elemen result-message muncul (visible)."""
    try:
        result_el = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.ID, "result-message"))
        )
        return result_el
    except Exception:
        return None


def reset_form(driver):
    """Reset form dan pesan hasil sebelum test berikutnya."""
    driver.get(LOGIN_PAGE_URL)
    time.sleep(1)


# ===================== TEST CASES =====================
def test_login_berhasil(driver):
    """
    TEST CASE 1: Login Berhasil
    - Input: username valid, password valid
    - Expected: Muncul pesan "Login berhasil" dengan warna hijau (class success)
    """
    print("\n" + "=" * 60)
    print("TEST CASE 1: Login Berhasil")
    print("=" * 60)

    reset_form(driver)

    # Isi form
    username_input = driver.find_element(By.ID, "username")
    password_input = driver.find_element(By.ID, "password")

    clear_and_type(username_input, USERNAME_VALID)
    clear_and_type(password_input, PASSWORD_VALID)

    print(f"  Input Username : {USERNAME_VALID}")
    print(f"  Input Password : {PASSWORD_VALID}")

    # Klik tombol login
    btn_login = driver.find_element(By.ID, "btn-login")
    btn_login.click()

    # Tunggu hasil
    result_el = wait_for_result(driver)

    if result_el is None:
        print("  ❌ GAGAL - Pesan hasil tidak muncul (timeout)")
        return False

    result_text = result_el.text
    result_class = result_el.get_attribute("class")

    print(f"  Hasil          : {result_text}")
    print(f"  Class CSS      : {result_class}")

    if "success" in result_class and "Login berhasil" in result_text:
        print("  ✅ PASSED - Login berhasil dengan credential valid")
        return True
    else:
        print("  ❌ FAILED - Expected pesan sukses, tapi dapat:", result_text)
        return False


def test_login_username_salah(driver):
    """
    TEST CASE 2: Login Gagal - Username Salah
    - Input: username salah, password valid
    - Expected: Muncul pesan error (class error)
    """
    print("\n" + "=" * 60)
    print("TEST CASE 2: Login Gagal - Username Salah")
    print("=" * 60)

    reset_form(driver)

    username_salah = "username_tidak_ada_12345"

    username_input = driver.find_element(By.ID, "username")
    password_input = driver.find_element(By.ID, "password")

    clear_and_type(username_input, username_salah)
    clear_and_type(password_input, PASSWORD_VALID)

    print(f"  Input Username : {username_salah}")
    print(f"  Input Password : {PASSWORD_VALID}")

    btn_login = driver.find_element(By.ID, "btn-login")
    btn_login.click()

    result_el = wait_for_result(driver)

    if result_el is None:
        print("  ❌ GAGAL - Pesan hasil tidak muncul (timeout)")
        return False

    result_text = result_el.text
    result_class = result_el.get_attribute("class")

    print(f"  Hasil          : {result_text}")
    print(f"  Class CSS      : {result_class}")

    if "error" in result_class:
        print("  ✅ PASSED - Login ditolak untuk username salah")
        return True
    else:
        print("  ❌ FAILED - Expected pesan error, tapi dapat:", result_text)
        return False


def test_login_password_salah(driver):
    """
    TEST CASE 3: Login Gagal - Password Salah
    - Input: username valid, password salah
    - Expected: Muncul pesan error (class error)
    """
    print("\n" + "=" * 60)
    print("TEST CASE 3: Login Gagal - Password Salah")
    print("=" * 60)

    reset_form(driver)

    password_salah = "password_salah_123"

    username_input = driver.find_element(By.ID, "username")
    password_input = driver.find_element(By.ID, "password")

    clear_and_type(username_input, USERNAME_VALID)
    clear_and_type(password_input, password_salah)

    print(f"  Input Username : {USERNAME_VALID}")
    print(f"  Input Password : {password_salah}")

    btn_login = driver.find_element(By.ID, "btn-login")
    btn_login.click()

    result_el = wait_for_result(driver)

    if result_el is None:
        print("  ❌ GAGAL - Pesan hasil tidak muncul (timeout)")
        return False

    result_text = result_el.text
    result_class = result_el.get_attribute("class")

    print(f"  Hasil          : {result_text}")
    print(f"  Class CSS      : {result_class}")

    if "error" in result_class:
        print("  ✅ PASSED - Login ditolak untuk password salah")
        return True
    else:
        print("  ❌ FAILED - Expected pesan error, tapi dapat:", result_text)
        return False


def test_login_field_kosong(driver):
    """
    TEST CASE 4: Login Gagal - Field Kosong
    - Input: username kosong, password kosong
    - Expected: Muncul pesan validasi error (class error)
    """
    print("\n" + "=" * 60)
    print("TEST CASE 4: Login Gagal - Field Kosong")
    print("=" * 60)

    reset_form(driver)

    username_input = driver.find_element(By.ID, "username")
    password_input = driver.find_element(By.ID, "password")

    # Biarkan kosong
    username_input.clear()
    password_input.clear()

    print("  Input Username : (kosong)")
    print("  Input Password : (kosong)")

    btn_login = driver.find_element(By.ID, "btn-login")
    btn_login.click()

    # Untuk validasi client-side, pesan muncul langsung tanpa menunggu API
    time.sleep(1)

    result_el = driver.find_element(By.ID, "result-message")
    result_text = result_el.text
    result_class = result_el.get_attribute("class")

    print(f"  Hasil          : {result_text}")
    print(f"  Class CSS      : {result_class}")

    # Cek juga validasi per-field
    username_error = driver.find_element(By.ID, "username-error")
    password_error = driver.find_element(By.ID, "password-error")

    username_error_visible = "show" in username_error.get_attribute("class")
    password_error_visible = "show" in password_error.get_attribute("class")

    print(f"  Username Error : {'Tampil' if username_error_visible else 'Tidak tampil'}")
    print(f"  Password Error : {'Tampil' if password_error_visible else 'Tidak tampil'}")

    if "error" in result_class and username_error_visible and password_error_visible:
        print("  ✅ PASSED - Validasi field kosong berfungsi")
        return True
    else:
        print("  ❌ FAILED - Validasi field kosong tidak berfungsi dengan benar")
        return False


# ===================== MAIN =====================
def main():
    print("╔" + "═" * 58 + "╗")
    print("║  PENGUJIAN SELENIUM - LOGIN WEB (DompetKu)              ║")
    print("║  Tester: Miqdam Syiam Nurrohman (714230043)             ║")
    print("╚" + "═" * 58 + "╝")
    print(f"\nHalaman Login: {LOGIN_PAGE_URL}")

    driver = None
    results = []

    try:
        # Setup WebDriver
        print("\n🔧 Menginisialisasi Chrome WebDriver...")
        driver = setup_driver()
        print("✅ WebDriver berhasil diinisialisasi\n")

        # Jalankan semua test case
        results.append(("TC-01: Login Berhasil", test_login_berhasil(driver)))
        results.append(("TC-02: Login Username Salah", test_login_username_salah(driver)))
        results.append(("TC-03: Login Password Salah", test_login_password_salah(driver)))
        results.append(("TC-04: Login Field Kosong", test_login_field_kosong(driver)))

    except Exception as e:
        print(f"\n💥 Error tidak terduga: {e}")
    finally:
        # Tampilkan ringkasan
        print("\n" + "=" * 60)
        print("📊 RINGKASAN HASIL PENGUJIAN")
        print("=" * 60)

        passed = 0
        failed = 0
        for name, result in results:
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"  {status} - {name}")
            if result:
                passed += 1
            else:
                failed += 1

        total = passed + failed
        print(f"\n  Total: {total} | Passed: {passed} | Failed: {failed}")
        print("=" * 60)

        # Tunggu sebentar agar user bisa melihat hasil
        time.sleep(3)

        # Tutup browser
        if driver:
            driver.quit()
            print("\n🔒 Browser ditutup.")


if __name__ == "__main__":
    main()
