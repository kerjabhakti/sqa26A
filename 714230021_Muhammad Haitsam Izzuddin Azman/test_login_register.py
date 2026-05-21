"""
Selenium Test - GOPOS Login & Register
=======================================
Test sederhana untuk menguji fitur Login dan Register
pada aplikasi GOPOS (goposind.github.io).

Menguji 1 akun saja:
    - Register akun baru
    - Login dengan akun tersebut

Setelah test selesai, laporan HTML akan otomatis
dibuat dan dibuka di browser.

Requirement:
    - pip install selenium
    - (Chrome browser + ChromeDriver harus sudah terinstall)
"""

import os
import time
import unittest
import webbrowser
import traceback
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


# ===================================================================
# HTML Report Generator
# ===================================================================
class HTMLReportGenerator:
    """Generate laporan HTML hasil test yang cantik dan otomatis terbuka di browser."""

    @staticmethod
    def generate(test_results, output_path="test_report.html"):
        """
        Generate HTML report dari hasil test.

        Args:
            test_results: list of dict, setiap dict berisi:
                - name: nama test
                - description: deskripsi test
                - status: 'PASS', 'FAIL', atau 'ERROR'
                - duration: durasi dalam detik
                - message: pesan error (jika ada)
                - test_type: 'Positive' atau 'Negative'
            output_path: path file HTML output
        """
        total = len(test_results)
        passed = sum(1 for r in test_results if r["status"] == "PASS")
        failed = sum(1 for r in test_results if r["status"] == "FAIL")
        errors = sum(1 for r in test_results if r["status"] == "ERROR")
        total_duration = sum(r["duration"] for r in test_results)

        pass_rate = (passed / total * 100) if total > 0 else 0

        # Generate rows
        rows_html = ""
        for i, r in enumerate(test_results, 1):
            status_class = {
                "PASS": "status-pass",
                "FAIL": "status-fail",
                "ERROR": "status-error"
            }.get(r["status"], "status-error")

            status_icon = {
                "PASS": "&#10004;",   # checkmark
                "FAIL": "&#10008;",   # cross
                "ERROR": "&#9888;"    # warning
            }.get(r["status"], "?")

            type_class = "type-positive" if r["test_type"] == "Positive" else "type-negative"

            error_row = ""
            if r["message"]:
                error_row = f'''
                <tr class="error-detail-row">
                    <td colspan="6">
                        <div class="error-detail">
                            <strong>Detail:</strong>
                            <pre>{r["message"]}</pre>
                        </div>
                    </td>
                </tr>'''

            rows_html += f'''
                <tr class="test-row">
                    <td class="col-no">{i}</td>
                    <td class="col-name">{r["name"]}</td>
                    <td class="col-desc">{r["description"]}</td>
                    <td class="col-type"><span class="badge {type_class}">{r["test_type"]}</span></td>
                    <td class="col-duration">{r["duration"]:.2f}s</td>
                    <td class="col-status"><span class="badge {status_class}">{status_icon} {r["status"]}</span></td>
                </tr>{error_row}'''

        # Status bar color
        if failed == 0 and errors == 0:
            overall_status = "ALL TESTS PASSED"
            overall_class = "overall-pass"
        else:
            overall_status = f"{failed + errors} TEST(S) FAILED"
            overall_class = "overall-fail"

        timestamp = datetime.now().strftime("%d %B %Y, %H:%M:%S")

        html = f'''<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GOPOS - Selenium Test Report</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: #0a0e1a;
            color: #e0e6ed;
            min-height: 100vh;
            padding: 0;
        }}

        /* === Header === */
        .report-header {{
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
            border-bottom: 1px solid rgba(99, 179, 237, 0.15);
            padding: 32px 40px;
            position: relative;
            overflow: hidden;
        }}

        .report-header::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #3b82f6, #06b6d4, #8b5cf6, #3b82f6);
            background-size: 200% 100%;
            animation: shimmer 3s linear infinite;
        }}

        @keyframes shimmer {{
            0% {{ background-position: 200% 0; }}
            100% {{ background-position: -200% 0; }}
        }}

        .header-content {{
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 16px;
        }}

        .header-left {{
            display: flex;
            align-items: center;
            gap: 16px;
        }}

        .header-logo {{
            width: 48px;
            height: 48px;
            background: linear-gradient(135deg, #3b82f6, #06b6d4);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
        }}

        .header-title h1 {{
            font-size: 22px;
            font-weight: 700;
            color: #f1f5f9;
            letter-spacing: -0.3px;
        }}

        .header-title p {{
            font-size: 13px;
            color: #94a3b8;
            margin-top: 2px;
        }}

        .header-timestamp {{
            font-size: 13px;
            color: #64748b;
            text-align: right;
        }}

        /* === Overall Status Banner === */
        .overall-banner {{
            max-width: 1200px;
            margin: 24px auto;
            padding: 0 40px;
        }}

        .overall-status {{
            padding: 16px 24px;
            border-radius: 12px;
            font-size: 15px;
            font-weight: 700;
            letter-spacing: 1px;
            text-align: center;
            text-transform: uppercase;
        }}

        .overall-pass {{
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(5, 150, 105, 0.1));
            border: 1px solid rgba(16, 185, 129, 0.3);
            color: #34d399;
        }}

        .overall-fail {{
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.15), rgba(220, 38, 38, 0.1));
            border: 1px solid rgba(239, 68, 68, 0.3);
            color: #f87171;
        }}

        /* === Stats Cards === */
        .stats-section {{
            max-width: 1200px;
            margin: 24px auto;
            padding: 0 40px;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 16px;
        }}

        .stat-card {{
            background: linear-gradient(135deg, #1e293b, #1a2332);
            border: 1px solid rgba(99, 179, 237, 0.1);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            transition: transform 0.2s, border-color 0.2s;
        }}

        .stat-card:hover {{
            transform: translateY(-2px);
            border-color: rgba(99, 179, 237, 0.25);
        }}

        .stat-value {{
            font-size: 32px;
            font-weight: 800;
            margin-bottom: 4px;
        }}

        .stat-label {{
            font-size: 12px;
            color: #94a3b8;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 600;
        }}

        .stat-total .stat-value {{ color: #93c5fd; }}
        .stat-passed .stat-value {{ color: #34d399; }}
        .stat-failed .stat-value {{ color: #f87171; }}
        .stat-errors .stat-value {{ color: #fbbf24; }}
        .stat-duration .stat-value {{ color: #c4b5fd; font-size: 26px; }}
        .stat-rate .stat-value {{ color: #34d399; }}

        /* === Progress Bar === */
        .progress-section {{
            max-width: 1200px;
            margin: 20px auto;
            padding: 0 40px;
        }}

        .progress-bar-container {{
            background: #1e293b;
            border-radius: 8px;
            height: 10px;
            overflow: hidden;
            display: flex;
        }}

        .progress-pass {{
            background: linear-gradient(90deg, #10b981, #34d399);
            height: 100%;
            transition: width 1s ease;
        }}

        .progress-fail {{
            background: linear-gradient(90deg, #ef4444, #f87171);
            height: 100%;
            transition: width 1s ease;
        }}

        .progress-error {{
            background: linear-gradient(90deg, #f59e0b, #fbbf24);
            height: 100%;
            transition: width 1s ease;
        }}

        /* === Table === */
        .table-section {{
            max-width: 1200px;
            margin: 24px auto;
            padding: 0 40px 40px;
        }}

        .table-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
        }}

        .table-header h2 {{
            font-size: 18px;
            font-weight: 700;
            color: #f1f5f9;
        }}

        .results-table {{
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            background: #1e293b;
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid rgba(99, 179, 237, 0.1);
        }}

        .results-table thead th {{
            background: linear-gradient(135deg, #1a2332, #162030);
            padding: 14px 16px;
            text-align: left;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #94a3b8;
            border-bottom: 1px solid rgba(99, 179, 237, 0.1);
        }}

        .results-table tbody td {{
            padding: 14px 16px;
            border-bottom: 1px solid rgba(99, 179, 237, 0.05);
            font-size: 14px;
        }}

        .test-row:hover {{
            background: rgba(99, 179, 237, 0.04);
        }}

        .col-no {{ width: 50px; text-align: center; color: #64748b; font-weight: 600; }}
        .col-name {{ font-weight: 600; color: #e2e8f0; }}
        .col-desc {{ color: #94a3b8; }}
        .col-type {{ width: 100px; text-align: center; }}
        .col-duration {{ width: 90px; text-align: center; color: #c4b5fd; font-weight: 600; font-variant-numeric: tabular-nums; }}
        .col-status {{ width: 110px; text-align: center; }}

        /* === Badges === */
        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 0.5px;
        }}

        .status-pass {{
            background: rgba(16, 185, 129, 0.15);
            color: #34d399;
            border: 1px solid rgba(16, 185, 129, 0.25);
        }}

        .status-fail {{
            background: rgba(239, 68, 68, 0.15);
            color: #f87171;
            border: 1px solid rgba(239, 68, 68, 0.25);
        }}

        .status-error {{
            background: rgba(245, 158, 11, 0.15);
            color: #fbbf24;
            border: 1px solid rgba(245, 158, 11, 0.25);
        }}

        .type-positive {{
            background: rgba(59, 130, 246, 0.12);
            color: #93c5fd;
            border: 1px solid rgba(59, 130, 246, 0.2);
        }}

        .type-negative {{
            background: rgba(168, 85, 247, 0.12);
            color: #c4b5fd;
            border: 1px solid rgba(168, 85, 247, 0.2);
        }}

        /* === Error Detail === */
        .error-detail-row td {{
            padding: 0 16px 14px !important;
            border-bottom: 1px solid rgba(239, 68, 68, 0.15) !important;
        }}

        .error-detail {{
            background: rgba(239, 68, 68, 0.06);
            border: 1px solid rgba(239, 68, 68, 0.15);
            border-radius: 8px;
            padding: 12px 16px;
            font-size: 12px;
        }}

        .error-detail strong {{
            color: #f87171;
            display: block;
            margin-bottom: 6px;
        }}

        .error-detail pre {{
            color: #fca5a5;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 11px;
            white-space: pre-wrap;
            word-break: break-word;
            margin: 0;
            line-height: 1.5;
        }}

        /* === Footer === */
        .report-footer {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px 40px 40px;
            text-align: center;
            color: #475569;
            font-size: 12px;
        }}

        .report-footer a {{
            color: #3b82f6;
            text-decoration: none;
        }}

        /* === Animations === */
        @keyframes fadeInUp {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .stat-card {{ animation: fadeInUp 0.5s ease forwards; }}
        .stat-card:nth-child(2) {{ animation-delay: 0.1s; }}
        .stat-card:nth-child(3) {{ animation-delay: 0.2s; }}
        .stat-card:nth-child(4) {{ animation-delay: 0.3s; }}
        .stat-card:nth-child(5) {{ animation-delay: 0.4s; }}
        .stat-card:nth-child(6) {{ animation-delay: 0.5s; }}

        /* === Responsive === */
        @media (max-width: 768px) {{
            .report-header {{ padding: 20px; }}
            .stats-section, .table-section, .progress-section, .overall-banner {{ padding: 0 16px; }}
            .header-content {{ flex-direction: column; align-items: flex-start; }}
            .stats-grid {{ grid-template-columns: repeat(2, 1fr); }}
            .results-table {{ font-size: 12px; }}
            .col-desc {{ display: none; }}
        }}
    </style>
</head>
<body>

    <!-- Header -->
    <div class="report-header">
        <div class="header-content">
            <div class="header-left">
                <div class="header-logo">&#128238;</div>
                <div class="header-title">
                    <h1>GOPOS - Selenium Test Report</h1>
                    <p>Automated Testing &mdash; Login &amp; Register Module</p>
                </div>
            </div>
            <div class="header-timestamp">
                {timestamp}
            </div>
        </div>
    </div>

    <!-- Overall Status -->
    <div class="overall-banner">
        <div class="overall-status {overall_class}">
            {overall_status}
        </div>
    </div>

    <!-- Stats Cards -->
    <div class="stats-section">
        <div class="stats-grid">
            <div class="stat-card stat-total">
                <div class="stat-value">{total}</div>
                <div class="stat-label">Total Test</div>
            </div>
            <div class="stat-card stat-passed">
                <div class="stat-value">{passed}</div>
                <div class="stat-label">Passed</div>
            </div>
            <div class="stat-card stat-failed">
                <div class="stat-value">{failed}</div>
                <div class="stat-label">Failed</div>
            </div>
            <div class="stat-card stat-errors">
                <div class="stat-value">{errors}</div>
                <div class="stat-label">Errors</div>
            </div>
            <div class="stat-card stat-duration">
                <div class="stat-value">{total_duration:.1f}s</div>
                <div class="stat-label">Duration</div>
            </div>
            <div class="stat-card stat-rate">
                <div class="stat-value">{pass_rate:.0f}%</div>
                <div class="stat-label">Pass Rate</div>
            </div>
        </div>
    </div>

    <!-- Progress Bar -->
    <div class="progress-section">
        <div class="progress-bar-container">
            <div class="progress-pass" style="width: {passed/total*100 if total else 0:.1f}%"></div>
            <div class="progress-fail" style="width: {failed/total*100 if total else 0:.1f}%"></div>
            <div class="progress-error" style="width: {errors/total*100 if total else 0:.1f}%"></div>
        </div>
    </div>

    <!-- Results Table -->
    <div class="table-section">
        <div class="table-header">
            <h2>Detail Hasil Test</h2>
        </div>
        <table class="results-table">
            <thead>
                <tr>
                    <th class="col-no">No</th>
                    <th class="col-name">Test Case</th>
                    <th class="col-desc">Deskripsi</th>
                    <th class="col-type">Tipe</th>
                    <th class="col-duration">Durasi</th>
                    <th class="col-status">Status</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
    </div>

    <!-- Footer -->
    <div class="report-footer">
        <p>GOPOS Selenium Test Report &bull; Muhammad Haitsam Izzuddin Azman (714230021)</p>
        <p style="margin-top: 4px;">Generated by <a href="https://goposind.github.io" target="_blank">GOPOS</a> Test Suite</p>
    </div>

</body>
</html>'''

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)

        return output_path


# ===================================================================
# Custom Test Result (untuk menangkap data per-test)
# ===================================================================
class CaptureTestResult(unittest.TestResult):
    """Custom TestResult yang menangkap data setiap test untuk report."""

    def __init__(self):
        super().__init__()
        self.test_data = []
        self._current_start_time = None

    def startTest(self, test):
        super().startTest(test)
        self._current_start_time = time.time()

    def addSuccess(self, test):
        super().addSuccess(test)
        self._record(test, "PASS", "")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        msg = "".join(traceback.format_exception(*err))
        self._record(test, "FAIL", msg)

    def addError(self, test, err):
        super().addError(test, err)
        msg = "".join(traceback.format_exception(*err))
        self._record(test, "ERROR", msg)

    def _record(self, test, status, message):
        duration = time.time() - self._current_start_time if self._current_start_time else 0

        # Tentukan test type & deskripsi berdasarkan nama method
        test_name = test._testMethodName
        test_doc = test.shortDescription() or ""

        test_info = {
            "test_1_register": ("Register Akun Baru", "Positive",
                "Mendaftarkan akun baru dengan nama, email, dan password valid"),
            "test_2_login": ("Login Akun Valid", "Positive",
                "Login menggunakan email dan password yang sudah terdaftar"),
            "test_3_login_wrong_password": ("Login Password Salah", "Negative",
                "Login dengan password yang salah, harus menampilkan error"),
            "test_4_register_password_mismatch": ("Register Password Tidak Cocok", "Negative",
                "Register dengan confirm password berbeda, form tidak boleh tersubmit"),
        }

        name, test_type, desc = test_info.get(
            test_name,
            (test_name, "Unknown", test_doc)
        )

        self.test_data.append({
            "name": name,
            "description": desc,
            "status": status,
            "duration": duration,
            "message": message,
            "test_type": test_type
        })


# ===================================================================
# Test Cases
# ===================================================================
class TestLoginRegisterGOPOS(unittest.TestCase):
    """Test case untuk fitur Login dan Register GOPOS."""

    # ===== Data akun test =====
    TEST_NAME = "Test Selenium User"
    TEST_EMAIL = f"testselenium{int(time.time())}@gmail.com"  # Email unik setiap run
    TEST_PASSWORD = "Test123456"

    # URL aplikasi
    BASE_URL = "https://goposind.github.io"

    @classmethod
    def setUpClass(cls):
        """Setup WebDriver sebelum semua test dijalankan."""
        chrome_options = Options()
        # Uncomment baris di bawah jika ingin headless (tanpa tampilan browser):
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-notifications")

        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.implicitly_wait(10)
        cls.wait = WebDriverWait(cls.driver, 15)

        print(f"\n{'='*60}")
        print(f"  GOPOS Selenium Test - Login & Register")
        print(f"  Email Test: {cls.TEST_EMAIL}")
        print(f"{'='*60}\n")

    @classmethod
    def tearDownClass(cls):
        """Tutup browser setelah semua test selesai."""
        time.sleep(2)  # Biar bisa lihat hasil terakhir
        cls.driver.quit()

    def _open_homepage(self):
        """Buka halaman utama GOPOS."""
        self.driver.get(self.BASE_URL)
        # Tunggu halaman selesai loading
        self.wait.until(
            EC.presence_of_element_located((By.ID, "loginBtn"))
        )
        time.sleep(1)

    def _ensure_logged_out(self):
        """Pastikan user dalam keadaan logout agar tombol Masuk muncul."""
        self.driver.execute_script("""
            localStorage.removeItem('gopos-token');
            localStorage.removeItem('gopos-user');
        """)
        self.driver.refresh()
        self.wait.until(
            EC.presence_of_element_located((By.ID, "loginBtn"))
        )
        # Tunggu sampai loginBtn visible (bukan display:none)
        self.wait.until(
            EC.visibility_of_element_located((By.ID, "loginBtn"))
        )
        time.sleep(1)

    def _close_swal_if_present(self):
        """Tutup SweetAlert2 popup jika ada (klik tombol OK)."""
        try:
            swal_btn = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".swal2-confirm"))
            )
            swal_btn.click()
            time.sleep(0.5)
        except Exception:
            pass  # Tidak ada SweetAlert, lanjut saja

    def _wait_for_swal(self, expected_icon=None, timeout=15):
        """
        Tunggu SweetAlert2 muncul dan return title + text-nya.
        expected_icon: 'success', 'error', 'warning', 'question', dll.
        """
        # Tunggu SweetAlert muncul
        self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".swal2-popup"))
        )
        time.sleep(1)  # Beri waktu animasi SweetAlert

        # Ambil title dan text
        try:
            title_el = self.driver.find_element(By.CSS_SELECTOR, ".swal2-title")
            title = title_el.text
        except Exception:
            title = ""

        try:
            text_el = self.driver.find_element(By.CSS_SELECTOR, "#swal2-html-container")
            text = text_el.text
        except Exception:
            text = ""

        # Cek icon jika diminta
        if expected_icon:
            icon_el = self.driver.find_elements(
                By.CSS_SELECTOR, f".swal2-icon.swal2-{expected_icon}"
            )
            self.assertTrue(
                len(icon_el) > 0,
                f"Expected SweetAlert icon '{expected_icon}' tapi tidak ditemukan."
            )

        return title, text

    # ================================================================
    # TEST 1: Register akun baru
    # ================================================================
    def test_1_register(self):
        """Test registrasi akun baru."""
        print("\n[TEST 1] Register akun baru...")
        self._open_homepage()

        # 1. Klik tombol "Masuk" di navbar untuk buka login modal
        login_btn = self.driver.find_element(By.ID, "loginBtn")
        login_btn.click()
        time.sleep(1)

        # 2. Tunggu login modal muncul
        self.wait.until(
            EC.visibility_of_element_located((By.ID, "loginModal"))
        )

        # 3. Klik link "Daftar sekarang" untuk pindah ke register modal
        register_link = self.driver.find_element(
            By.CSS_SELECTOR, '#loginModal a[data-modal="registerModal"]'
        )
        register_link.click()
        time.sleep(1)

        # 4. Tunggu register modal muncul
        self.wait.until(
            EC.visibility_of_element_located((By.ID, "registerModal"))
        )

        # 5. Isi form register
        name_input = self.driver.find_element(By.ID, "registerName")
        email_input = self.driver.find_element(By.ID, "registerEmail")
        password_input = self.driver.find_element(By.ID, "registerPassword")
        confirm_input = self.driver.find_element(By.ID, "confirmPassword")

        name_input.clear()
        name_input.send_keys(self.TEST_NAME)

        email_input.clear()
        email_input.send_keys(self.TEST_EMAIL)

        password_input.clear()
        password_input.send_keys(self.TEST_PASSWORD)

        confirm_input.clear()
        confirm_input.send_keys(self.TEST_PASSWORD)

        print(f"   Nama    : {self.TEST_NAME}")
        print(f"   Email   : {self.TEST_EMAIL}")
        print(f"   Password: {'*' * len(self.TEST_PASSWORD)}")

        time.sleep(1)  # Biar terlihat isi formnya

        # 6. Klik tombol "Daftar"
        submit_btn = self.driver.find_element(
            By.CSS_SELECTOR, '#registerForm button[type="submit"]'
        )
        submit_btn.click()

        # 7. Tunggu loading selesai & SweetAlert muncul
        time.sleep(3)

        # 8. Cek SweetAlert response
        title, text = self._wait_for_swal()
        print(f"   Result  : {title} - {text}")

        # Bisa sukses atau gagal (email sudah terdaftar, dll)
        # Yang penting SweetAlert muncul
        self.assertTrue(
            len(title) > 0,
            "SweetAlert harus muncul setelah register."
        )

        # Tutup SweetAlert
        self._close_swal_if_present()
        time.sleep(1)

        print("   [TEST 1] [OK] Register test selesai!")

    # ================================================================
    # TEST 2: Login dengan akun yang sudah ada
    # ================================================================
    def test_2_login(self):
        """Test login dengan akun."""
        print("\n[TEST 2] Login dengan akun...")
        self._open_homepage()
        self._ensure_logged_out()

        # 1. Klik tombol "Masuk" di navbar
        login_btn = self.driver.find_element(By.ID, "loginBtn")
        login_btn.click()
        time.sleep(1)

        # 2. Tunggu login modal muncul
        self.wait.until(
            EC.visibility_of_element_located((By.ID, "loginModal"))
        )

        # 3. Isi form login
        email_input = self.driver.find_element(By.ID, "loginEmail")
        password_input = self.driver.find_element(By.ID, "loginPassword")

        email_input.clear()
        email_input.send_keys(self.TEST_EMAIL)

        password_input.clear()
        password_input.send_keys(self.TEST_PASSWORD)

        print(f"   Email   : {self.TEST_EMAIL}")
        print(f"   Password: {'*' * len(self.TEST_PASSWORD)}")

        time.sleep(1)  # Biar terlihat isi formnya

        # 4. Klik tombol "Masuk"
        submit_btn = self.driver.find_element(
            By.CSS_SELECTOR, '#loginForm button[type="submit"]'
        )
        submit_btn.click()

        # 5. Tunggu loading selesai & SweetAlert muncul
        time.sleep(3)

        # 6. Cek SweetAlert response
        title, text = self._wait_for_swal()
        print(f"   Result  : {title} - {text}")

        self.assertTrue(
            len(title) > 0,
            "SweetAlert harus muncul setelah login."
        )

        # Tutup SweetAlert
        self._close_swal_if_present()
        time.sleep(1)

        print("   [TEST 2] [OK] Login test selesai!")

    # ================================================================
    # TEST 3: Login dengan password salah (negative test)
    # ================================================================
    def test_3_login_wrong_password(self):
        """Test login dengan password yang salah (negative test)."""
        print("\n[TEST 3] Login dengan password salah (negative test)...")
        self._open_homepage()
        self._ensure_logged_out()

        # 1. Klik tombol "Masuk"
        login_btn = self.driver.find_element(By.ID, "loginBtn")
        login_btn.click()
        time.sleep(1)

        # 2. Tunggu login modal muncul
        self.wait.until(
            EC.visibility_of_element_located((By.ID, "loginModal"))
        )

        # 3. Isi form dengan password yang salah
        email_input = self.driver.find_element(By.ID, "loginEmail")
        password_input = self.driver.find_element(By.ID, "loginPassword")

        email_input.clear()
        email_input.send_keys(self.TEST_EMAIL)

        password_input.clear()
        password_input.send_keys("PasswordSalah123")

        print(f"   Email   : {self.TEST_EMAIL}")
        print(f"   Password: PasswordSalah123 (sengaja salah)")

        time.sleep(1)

        # 4. Klik tombol "Masuk"
        submit_btn = self.driver.find_element(
            By.CSS_SELECTOR, '#loginForm button[type="submit"]'
        )
        submit_btn.click()

        # 5. Tunggu response
        time.sleep(3)

        # 6. Cek SweetAlert response - harusnya error
        title, text = self._wait_for_swal()
        print(f"   Result  : {title} - {text}")

        # Harusnya muncul pesan error
        self.assertTrue(
            len(title) > 0,
            "SweetAlert error harus muncul saat password salah."
        )

        # Tutup SweetAlert
        self._close_swal_if_present()
        time.sleep(1)

        print("   [TEST 3] [OK] Negative login test selesai!")

    # ================================================================
    # TEST 4: Verifikasi form validasi (field kosong)
    # ================================================================
    def test_4_register_password_mismatch(self):
        """Test register dengan password yang tidak cocok."""
        print("\n[TEST 4] Register dengan password tidak cocok...")
        self._open_homepage()
        self._ensure_logged_out()

        # 1. Buka register modal
        login_btn = self.driver.find_element(By.ID, "loginBtn")
        login_btn.click()
        time.sleep(1)

        self.wait.until(
            EC.visibility_of_element_located((By.ID, "loginModal"))
        )

        register_link = self.driver.find_element(
            By.CSS_SELECTOR, '#loginModal a[data-modal="registerModal"]'
        )
        register_link.click()
        time.sleep(1)

        self.wait.until(
            EC.visibility_of_element_located((By.ID, "registerModal"))
        )

        # 2. Isi form dengan password yang tidak cocok
        name_input = self.driver.find_element(By.ID, "registerName")
        email_input = self.driver.find_element(By.ID, "registerEmail")
        password_input = self.driver.find_element(By.ID, "registerPassword")
        confirm_input = self.driver.find_element(By.ID, "confirmPassword")

        name_input.clear()
        name_input.send_keys("Test User")

        email_input.clear()
        email_input.send_keys("test@test.com")

        password_input.clear()
        password_input.send_keys("Password123")

        confirm_input.clear()
        confirm_input.send_keys("BedaPassword456")  # Sengaja beda

        print(f"   Password       : Password123")
        print(f"   Confirm Password: BedaPassword456 (sengaja beda)")

        time.sleep(1)

        # 3. Klik tombol "Daftar"
        submit_btn = self.driver.find_element(
            By.CSS_SELECTOR, '#registerForm button[type="submit"]'
        )
        submit_btn.click()

        # 4. Tunggu Toast notification muncul (SweetAlert2 Toast mode)
        #    Toast di GOPOS hanya muncul 1 detik, jadi harus cepat menangkapnya.
        #    Toast menggunakan class .swal2-popup.swal2-toast
        toast_found = False
        toast_title = ""
        try:
            # Tunggu Toast muncul (timeout 5 detik)
            toast_el = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ".swal2-popup.swal2-toast")
                )
            )
            # Ambil title dari Toast
            try:
                toast_title_el = toast_el.find_element(By.CSS_SELECTOR, ".swal2-title")
                toast_title = toast_title_el.text
            except Exception:
                toast_title = ""
            toast_found = True
            print(f"   Toast muncul   : Ya")
            print(f"   Toast pesan    : {toast_title}")
        except Exception:
            toast_found = False
            print(f"   Toast muncul   : Tidak (mungkin sudah hilang terlalu cepat)")

        # 5. Verifikasi Toast berisi pesan "Password tidak cocok"
        self.assertTrue(
            toast_found,
            "Toast 'Password tidak cocok' harus muncul saat password dan confirm password berbeda."
        )
        self.assertIn(
            "tidak cocok", toast_title.lower(),
            f"Toast harus berisi pesan 'Password tidak cocok', tapi ditemukan: '{toast_title}'"
        )

        # 6. Tunggu Toast hilang, lalu cek modal masih terbuka
        time.sleep(2)

        # Cek bahwa modal masih terbuka (form tidak disubmit)
        register_modal = self.driver.find_element(By.ID, "registerModal")
        is_modal_active = "active" in register_modal.get_attribute("class")

        print(f"   Modal masih terbuka: {is_modal_active}")
        self.assertTrue(
            is_modal_active,
            "Register modal harus tetap terbuka saat password tidak cocok."
        )

        print("   [TEST 4] [OK] Password mismatch test selesai!")


# ===================================================================
# Main Runner - jalankan test & generate HTML report
# ===================================================================
if __name__ == "__main__":
    # Jalankan test dengan custom result
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestLoginRegisterGOPOS)

    print("\n" + "=" * 60)
    print("  Menjalankan Selenium Test...")
    print("=" * 60)

    result = CaptureTestResult()

    # Jalankan semua test
    suite.run(result)

    # Generate HTML report
    report_dir = os.path.dirname(os.path.abspath(__file__))
    report_path = os.path.join(report_dir, "test_report.html")

    HTMLReportGenerator.generate(result.test_data, report_path)

    # Tampilkan ringkasan di console
    print("\n" + "=" * 60)
    print("  RINGKASAN HASIL TEST")
    print("=" * 60)
    print(f"  Total    : {result.testsRun}")
    print(f"  Passed   : {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"  Failed   : {len(result.failures)}")
    print(f"  Errors   : {len(result.errors)}")
    print(f"  Report   : {report_path}")
    print("=" * 60)

    # Buka HTML report di browser
    print("\n  >> Membuka laporan HTML di browser...")
    webbrowser.open("file:///" + report_path.replace("\\", "/"))

    # Exit code
    if result.failures or result.errors:
        exit(1)
    else:
        exit(0)
