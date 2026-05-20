"""
=============================================================
 PENGUJIAN SELENIUM WEBDRIVER - API BACKEND LANGSUNG
 Aplikasi: DompetKu (Catatan Keuangan Pribadi)
 Tester  : Miqdam Syiam Nurrohman (714230043)
=============================================================

Deskripsi:
    Script ini menguji API backend DompetKu secara langsung
    menggunakan Selenium WebDriver. Selenium membuka browser dan
    mengeksekusi JavaScript fetch() untuk memanggil API endpoint.
    Hasil response ditampilkan di halaman browser.

Test Cases:
    1. Login API - berhasil (POST /api/auth/login)
    2. Login API - gagal, credential salah (POST /api/auth/login)
    3. Health Check API (GET /health)
    4. Get Categories API (GET /api/categories)
"""

import time
import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# ===================== KONFIGURASI =====================
API_BASE_URL = "https://dompetku-mu.vercel.app"
USERNAME_VALID = "test123"
PASSWORD_VALID = "test123"
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


def create_test_page(driver):
    """
    Buat halaman HTML kosong di browser untuk menampilkan hasil test.
    Kita perlu halaman dengan origin yang sama agar bisa execute JavaScript.
    """
    # Buka halaman about:blank terlebih dahulu
    driver.get("about:blank")
    time.sleep(1)

    # Inject HTML untuk menampilkan hasil test
    driver.execute_script("""
        document.title = 'DompetKu API Test Results';
        document.body.innerHTML = `
            <div style="font-family: 'Segoe UI', sans-serif; max-width: 800px; margin: 40px auto; padding: 20px;">
                <h1 style="color: #667eea; text-align: center;">🧪 DompetKu API Test Results</h1>
                <p style="text-align: center; color: #888;">Pengujian Selenium WebDriver - API Backend</p>
                <hr style="border: 1px solid #eee; margin: 20px 0;">
                <div id="test-results"></div>
            </div>
        `;
    """)
    time.sleep(0.5)


def execute_api_call(driver, method, endpoint, body=None):
    """
    Eksekusi API call menggunakan JavaScript fetch() di browser.
    Mengembalikan dict dengan status, data, dan error.
    """
    fetch_options = {
        "method": method,
        "headers": {"Content-Type": "application/json"},
    }

    if body is not None:
        body_json = json.dumps(body)
        js_script = f"""
            var callback = arguments[arguments.length - 1];
            fetch('{API_BASE_URL}{endpoint}', {{
                method: '{method}',
                headers: {{'Content-Type': 'application/json'}},
                body: '{body_json}'
            }})
            .then(function(response) {{
                return response.json().then(function(data) {{
                    callback({{
                        'status': response.status,
                        'ok': response.ok,
                        'data': data
                    }});
                }});
            }})
            .catch(function(error) {{
                callback({{
                    'status': 0,
                    'ok': false,
                    'data': {{'error': error.message}}
                }});
            }});
        """
    else:
        js_script = f"""
            var callback = arguments[arguments.length - 1];
            fetch('{API_BASE_URL}{endpoint}', {{
                method: '{method}',
                headers: {{'Content-Type': 'application/json'}}
            }})
            .then(function(response) {{
                return response.json().then(function(data) {{
                    callback({{
                        'status': response.status,
                        'ok': response.ok,
                        'data': data
                    }});
                }});
            }})
            .catch(function(error) {{
                callback({{
                    'status': 0,
                    'ok': false,
                    'data': {{'error': error.message}}
                }});
            }});
        """

    try:
        driver.set_script_timeout(WAIT_TIMEOUT)
        result = driver.execute_async_script(js_script)
        return result
    except Exception as e:
        return {"status": 0, "ok": False, "data": {"error": str(e)}}


def append_result_to_page(driver, test_name, passed, details):
    """Tambahkan hasil test ke halaman browser."""
    status_color = "#28a745" if passed else "#dc3545"
    status_text = "✅ PASSED" if passed else "❌ FAILED"
    details_escaped = details.replace("'", "\\'").replace("\n", "<br>")

    driver.execute_script(f"""
        var resultsDiv = document.getElementById('test-results');
        var testDiv = document.createElement('div');
        testDiv.style.cssText = 'background: #f8f9fa; border-radius: 10px; padding: 16px; margin-bottom: 12px; border-left: 4px solid {status_color};';
        testDiv.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <strong style="color: #333;">{test_name}</strong>
                <span style="color: {status_color}; font-weight: bold;">{status_text}</span>
            </div>
            <div style="color: #666; font-size: 13px; margin-top: 8px;">{details_escaped}</div>
        `;
        resultsDiv.appendChild(testDiv);
    """)


# ===================== TEST CASES =====================
def test_api_login_berhasil(driver):
    """
    TEST CASE 1: Login API - Berhasil
    - Endpoint : POST /api/auth/login
    - Input    : username & password valid
    - Expected : Status 200, response berisi token dan user data
    """
    print("\n" + "=" * 60)
    print("TEST CASE 1: Login API - Berhasil")
    print("=" * 60)

    body = {"username": USERNAME_VALID, "password": PASSWORD_VALID}
    print(f"  Endpoint : POST /api/auth/login")
    print(f"  Body     : {json.dumps(body)}")

    result = execute_api_call(driver, "POST", "/api/auth/login", body)

    status = result.get("status", 0)
    data = result.get("data", {})

    print(f"  Status   : {status}")
    print(f"  Response : {json.dumps(data, indent=2)}")

    passed = (
        status == 200
        and "token" in data
        and "user" in data
    )

    details = f"Status: {status} | Token: {'Ada' if 'token' in data else 'Tidak ada'} | User: {data.get('user', {}).get('nama', 'N/A')}"

    if passed:
        print("  ✅ PASSED - Login API berhasil, token diterima")
    else:
        print("  ❌ FAILED - Login API tidak mengembalikan response yang diharapkan")

    append_result_to_page(driver, "TC-01: Login API Berhasil", passed, details)
    return passed


def test_api_login_gagal(driver):
    """
    TEST CASE 2: Login API - Gagal (Credential Salah)
    - Endpoint : POST /api/auth/login
    - Input    : username salah, password salah
    - Expected : Status 401, response berisi error message
    """
    print("\n" + "=" * 60)
    print("TEST CASE 2: Login API - Gagal (Credential Salah)")
    print("=" * 60)

    body = {"username": "akun_tidak_ada_xyz", "password": "salah_password"}
    print(f"  Endpoint : POST /api/auth/login")
    print(f"  Body     : {json.dumps(body)}")

    result = execute_api_call(driver, "POST", "/api/auth/login", body)

    status = result.get("status", 0)
    data = result.get("data", {})

    print(f"  Status   : {status}")
    print(f"  Response : {json.dumps(data, indent=2)}")

    passed = (
        status == 401
        and "error" in data
    )

    details = f"Status: {status} | Error: {data.get('error', 'N/A')}"

    if passed:
        print("  ✅ PASSED - API menolak credential salah dengan status 401")
    else:
        print("  ❌ FAILED - Expected status 401 dengan error message")

    append_result_to_page(driver, "TC-02: Login API Gagal (Credential Salah)", passed, details)
    return passed


def test_api_health_check(driver):
    """
    TEST CASE 3: Health Check API
    - Endpoint : GET /health
    - Expected : Status 200, API berjalan
    """
    print("\n" + "=" * 60)
    print("TEST CASE 3: Health Check API")
    print("=" * 60)

    print(f"  Endpoint : GET /health")

    result = execute_api_call(driver, "GET", "/health")

    status = result.get("status", 0)
    data = result.get("data", {})

    print(f"  Status   : {status}")
    print(f"  Response : {json.dumps(data, indent=2)}")

    passed = status == 200

    details = f"Status: {status} | Response: {json.dumps(data)}"

    if passed:
        print("  ✅ PASSED - Health check API berjalan (status 200)")
    else:
        print("  ❌ FAILED - Health check API tidak merespons dengan benar")

    append_result_to_page(driver, "TC-03: Health Check API", passed, details)
    return passed


def test_api_get_categories(driver):
    """
    TEST CASE 4: Get Categories API
    - Endpoint : GET /api/categories
    - Expected : Status 200, response berisi list kategori
    """
    print("\n" + "=" * 60)
    print("TEST CASE 4: Get Categories API")
    print("=" * 60)

    print(f"  Endpoint : GET /api/categories")

    result = execute_api_call(driver, "GET", "/api/categories")

    status = result.get("status", 0)
    data = result.get("data", {})

    print(f"  Status   : {status}")
    print(f"  Response : {json.dumps(data, indent=2)}")

    categories = data.get("categories", [])

    passed = (
        status == 200
        and isinstance(categories, list)
        and len(categories) > 0
    )

    details = f"Status: {status} | Jumlah Kategori: {len(categories)} | Kategori: {', '.join(categories) if categories else 'N/A'}"

    if passed:
        print(f"  ✅ PASSED - Berhasil mendapatkan {len(categories)} kategori")
    else:
        print("  ❌ FAILED - Tidak berhasil mendapatkan daftar kategori")

    append_result_to_page(driver, "TC-04: Get Categories API", passed, details)
    return passed


# ===================== MAIN =====================
def main():
    print("╔" + "═" * 58 + "╗")
    print("║  PENGUJIAN SELENIUM - API BACKEND (DompetKu)            ║")
    print("║  Tester: Miqdam Syiam Nurrohman (714230043)             ║")
    print("╚" + "═" * 58 + "╝")
    print(f"\nAPI Base URL: {API_BASE_URL}")

    driver = None
    results = []

    try:
        # Setup WebDriver
        print("\n🔧 Menginisialisasi Chrome WebDriver...")
        driver = setup_driver()
        print("✅ WebDriver berhasil diinisialisasi\n")

        # Buat halaman test di browser
        create_test_page(driver)

        # Jalankan semua test case
        results.append(("TC-01: Login API Berhasil", test_api_login_berhasil(driver)))
        results.append(("TC-02: Login API Gagal", test_api_login_gagal(driver)))
        results.append(("TC-03: Health Check API", test_api_health_check(driver)))
        results.append(("TC-04: Get Categories API", test_api_get_categories(driver)))

    except Exception as e:
        print(f"\n💥 Error tidak terduga: {e}")
    finally:
        # Tampilkan ringkasan di console
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

        # Tambahkan summary ke browser juga
        if driver:
            try:
                driver.execute_script(f"""
                    var resultsDiv = document.getElementById('test-results');
                    var summaryDiv = document.createElement('div');
                    summaryDiv.style.cssText = 'background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 10px; padding: 20px; margin-top: 20px; color: white; text-align: center;';
                    summaryDiv.innerHTML = `
                        <h3 style="margin: 0 0 8px 0;">📊 Ringkasan</h3>
                        <p style="margin: 0; font-size: 18px;">Total: {total} | ✅ Passed: {passed} | ❌ Failed: {failed}</p>
                    `;
                    resultsDiv.appendChild(summaryDiv);
                """)
            except Exception:
                pass

        # Tunggu agar user bisa melihat hasil di browser
        print("\n⏳ Browser tetap terbuka 10 detik agar bisa melihat hasil...")
        time.sleep(10)

        # Tutup browser
        if driver:
            driver.quit()
            print("🔒 Browser ditutup.")


if __name__ == "__main__":
    main()
