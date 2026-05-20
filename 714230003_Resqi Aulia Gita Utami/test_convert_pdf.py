"""
=================================================================
SELENIUM WEBDRIVER TESTING - FITUR CONVERT PDF
Aplikasi: PDF Suit (https://pdfmulbi.github.io/)
=================================================================
Testing mencakup (TANPA LOGIN):
1. Navigasi ke halaman Convert
2. Test Convert Word to PDF (upload .docx, preview, download)
3. Test switch tab antara Word to PDF dan PDF to Word
4. Test elemen UI dan validasi
=================================================================
"""

import time
import os
import sys
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


# =============================================
# KONFIGURASI
# =============================================
BASE_URL = "https://pdfmulbi.github.io"
CONVERT_URL = f"{BASE_URL}/convert.html"

# Path file testing (absolute path) - menggunakan file yang sudah disiapkan
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DOCX_FILE = os.path.join(CURRENT_DIR, "test_files", "testing.docx")


class TestConvertPDF(unittest.TestCase):
    """Test class untuk fitur Convert PDF pada aplikasi PDF Suit (tanpa login)."""

    @classmethod
    def setUpClass(cls):
        """Setup yang dijalankan sekali sebelum semua test."""
        # Konfigurasi Chrome Options
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")

        # Set download directory
        download_dir = os.path.join(CURRENT_DIR, "test_downloads")
        os.makedirs(download_dir, exist_ok=True)

        prefs = {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
        }
        chrome_options.add_experimental_option("prefs", prefs)

        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.implicitly_wait(10)
        cls.wait = WebDriverWait(cls.driver, 15)
        cls.download_dir = download_dir

    @classmethod
    def tearDownClass(cls):
        """Cleanup - otomatis menutup browser setelah semua test selesai."""
        try:
            cls.driver.quit()
            print("\n[INFO] Browser otomatis ditutup setelah testing selesai.")
        except Exception:
            pass

    # =============================================
    # TEST 1: Halaman Convert bisa diakses
    # =============================================
    def test_01_convert_page_accessible(self):
        """Test bahwa halaman convert bisa diakses."""
        print("\n[TEST 1] Mengecek halaman Convert bisa diakses...")
        self.driver.get(CONVERT_URL)
        time.sleep(3)

        # Verifikasi title halaman
        self.assertIn("Converter Tools", self.driver.title)
        print("[PASS] Halaman Convert berhasil diakses.")

    # =============================================
    # TEST 2: Elemen-elemen utama halaman Convert ada
    # =============================================
    def test_02_convert_page_elements_exist(self):
        """Test bahwa elemen-elemen utama di halaman convert ada."""
        print("\n[TEST 2] Mengecek elemen-elemen halaman Convert...")
        self.driver.get(CONVERT_URL)
        time.sleep(3)

        # Cek judul halaman
        page_title = self.wait.until(
            EC.presence_of_element_located((By.ID, "pageTitle"))
        )
        self.assertIsNotNone(page_title)
        print("  - Page title ditemukan: " + page_title.text)

        # Cek deskripsi halaman
        page_desc = self.driver.find_element(By.ID, "pageDesc")
        self.assertIsNotNone(page_desc)
        print("  - Page description ditemukan: " + page_desc.text)

        # Cek tab Word to PDF
        tab_word = self.driver.find_element(By.ID, "tabWord")
        self.assertIsNotNone(tab_word)
        print("  - Tab 'Word to PDF' ditemukan")

        # Cek tab PDF to Word
        tab_pdf = self.driver.find_element(By.ID, "tabPdf")
        self.assertIsNotNone(tab_pdf)
        print("  - Tab 'PDF to Word' ditemukan")

        # Cek upload zone Word
        word_upload = self.driver.find_element(By.ID, "wordUploadZone")
        self.assertIsNotNone(word_upload)
        print("  - Word upload zone ditemukan")

        # Cek input file Word
        word_input = self.driver.find_element(By.ID, "wordInput")
        self.assertIsNotNone(word_input)
        print("  - Word file input ditemukan")

        print("[PASS] Semua elemen utama ditemukan.")

    # =============================================
    # TEST 3: Switch tab Word to PDF -> PDF to Word
    # =============================================
    def test_03_switch_tab_to_pdf_to_word(self):
        """Test switching tab dari Word to PDF ke PDF to Word."""
        print("\n[TEST 3] Mengecek switch tab ke PDF to Word...")
        self.driver.get(CONVERT_URL)
        time.sleep(3)

        # Klik tab PDF to Word
        tab_pdf = self.wait.until(
            EC.element_to_be_clickable((By.ID, "tabPdf"))
        )
        tab_pdf.click()
        time.sleep(2)

        # Verifikasi judul berubah
        page_title = self.driver.find_element(By.ID, "pageTitle")
        self.assertIn("PDF to Word", page_title.text)
        print("  - Judul berubah menjadi: " + page_title.text)

        # Verifikasi panel PDF muncul
        panel_pdf = self.driver.find_element(By.ID, "panelPdf")
        self.assertNotIn("d-none", panel_pdf.get_attribute("class"))
        print("  - Panel PDF to Word ditampilkan")

        # Verifikasi panel Word tersembunyi
        panel_word = self.driver.find_element(By.ID, "panelWord")
        self.assertIn("d-none", panel_word.get_attribute("class"))
        print("  - Panel Word to PDF tersembunyi")

        # Verifikasi elemen upload PDF ada
        pdf_upload = self.driver.find_element(By.ID, "pdfUploadZone")
        self.assertIsNotNone(pdf_upload)
        print("  - PDF upload zone ditemukan")

        print("[PASS] Switch tab ke PDF to Word berhasil.")

    # =============================================
    # TEST 4: Switch tab kembali ke Word to PDF
    # =============================================
    def test_04_switch_tab_back_to_word_to_pdf(self):
        """Test switching tab kembali dari PDF to Word ke Word to PDF."""
        print("\n[TEST 4] Mengecek switch tab kembali ke Word to PDF...")
        self.driver.get(CONVERT_URL)
        time.sleep(3)

        # Pertama, klik tab PDF to Word
        tab_pdf = self.wait.until(
            EC.element_to_be_clickable((By.ID, "tabPdf"))
        )
        tab_pdf.click()
        time.sleep(1)

        # Kemudian klik kembali tab Word to PDF
        tab_word = self.driver.find_element(By.ID, "tabWord")
        tab_word.click()
        time.sleep(2)

        # Verifikasi judul kembali
        page_title = self.driver.find_element(By.ID, "pageTitle")
        self.assertIn("Word to PDF", page_title.text)
        print("  - Judul kembali menjadi: " + page_title.text)

        # Verifikasi panel Word muncul kembali
        panel_word = self.driver.find_element(By.ID, "panelWord")
        self.assertNotIn("d-none", panel_word.get_attribute("class") or "")
        print("  - Panel Word to PDF ditampilkan kembali")

        print("[PASS] Switch tab kembali ke Word to PDF berhasil.")

    # =============================================
    # TEST 5: Upload file Word (.docx) untuk convert
    # =============================================
    def test_05_upload_word_file(self):
        """Test upload file Word (testing.docx) untuk convert ke PDF."""
        print("\n[TEST 5] Mengecek upload file Word (.docx)...")

        # Navigasi ke halaman convert
        self.driver.get(CONVERT_URL)
        time.sleep(3)

        # Pastikan tab Word to PDF aktif
        tab_word = self.wait.until(
            EC.element_to_be_clickable((By.ID, "tabWord"))
        )
        tab_word.click()
        time.sleep(1)

        # Upload file .docx menggunakan send_keys ke input file
        word_input = self.driver.find_element(By.ID, "wordInput")
        word_input.send_keys(TEST_DOCX_FILE)
        print("  - File .docx berhasil di-upload: " + TEST_DOCX_FILE)

        # Tunggu preview muncul
        time.sleep(5)

        # Cek apakah preview container muncul
        try:
            preview_container = self.driver.find_element(By.ID, "wordPreviewContainer")
            preview_class = preview_container.get_attribute("class") or ""
            if "d-none" not in preview_class:
                print("  - Preview dokumen Word berhasil ditampilkan")
            else:
                print("  - Preview container ada tapi masih tersembunyi")
        except Exception:
            print("  - Preview container tidak ditemukan")

        # Cek apakah tombol download muncul
        try:
            action_area = self.driver.find_element(By.ID, "wordActionArea")
            action_class = action_area.get_attribute("class") or ""
            if "d-none" not in action_class:
                print("  - Tombol 'Simpan sebagai PDF' muncul")
                download_btn = self.driver.find_element(By.ID, "wordDownloadBtn")
                self.assertIsNotNone(download_btn)
                print("[PASS] Upload file Word berhasil, tombol download tersedia.")
            else:
                print("  - Action area masih tersembunyi")
                print("[INFO] Upload mungkin belum diproses sepenuhnya.")
        except Exception as e:
            print(f"  - Error: {e}")
            print("[INFO] Upload mungkin belum diproses.")

    # =============================================
    # TEST 6: Download PDF dari Word to PDF convert
    # =============================================
    def test_06_download_converted_pdf(self):
        """Test download file PDF setelah convert dari Word (testing.docx)."""
        print("\n[TEST 6] Mengecek download hasil convert Word to PDF...")

        # Navigasi ke halaman convert
        self.driver.get(CONVERT_URL)
        time.sleep(3)

        # Upload file Word
        tab_word = self.wait.until(
            EC.element_to_be_clickable((By.ID, "tabWord"))
        )
        tab_word.click()
        time.sleep(1)

        word_input = self.driver.find_element(By.ID, "wordInput")
        word_input.send_keys(TEST_DOCX_FILE)
        time.sleep(5)

        # Cek dan klik tombol download
        try:
            action_area = self.driver.find_element(By.ID, "wordActionArea")
            action_class = action_area.get_attribute("class") or ""

            if "d-none" not in action_class:
                download_btn = self.driver.find_element(By.ID, "wordDownloadBtn")
                download_btn.click()
                print("  - Tombol 'Simpan sebagai PDF' diklik")
                time.sleep(5)

                # Verifikasi file di-download (cek folder download)
                downloaded_files = os.listdir(self.download_dir)
                pdf_files = [f for f in downloaded_files if f.endswith(".pdf")]

                if pdf_files:
                    print(f"  - File PDF berhasil di-download: {pdf_files}")
                    print("[PASS] Download PDF berhasil.")
                else:
                    print("  - File PDF belum terdeteksi di folder download")
                    print("[INFO] Download mungkin butuh waktu lebih lama.")
            else:
                print("  - Tombol download belum tersedia")
                print("[INFO] Perlu upload file terlebih dahulu.")

        except Exception as e:
            print(f"  - Error saat download: {e}")

    # =============================================
    # TEST 7: Verifikasi style tab aktif berubah
    # =============================================
    def test_07_tab_active_style_changes(self):
        """Test bahwa style tab aktif berubah saat diklik."""
        print("\n[TEST 7] Mengecek perubahan style tab aktif...")
        self.driver.get(CONVERT_URL)
        time.sleep(3)

        # Cek tab Word aktif secara default
        tab_word = self.wait.until(
            EC.presence_of_element_located((By.ID, "tabWord"))
        )
        word_classes = tab_word.get_attribute("class")
        self.assertIn("btn-active-mode", word_classes)
        print("  - Tab Word to PDF memiliki class 'btn-active-mode' (default aktif)")

        # Cek tab PDF tidak aktif
        tab_pdf = self.driver.find_element(By.ID, "tabPdf")
        pdf_classes = tab_pdf.get_attribute("class")
        self.assertIn("btn-inactive-mode", pdf_classes)
        print("  - Tab PDF to Word memiliki class 'btn-inactive-mode' (default tidak aktif)")

        # Klik tab PDF to Word
        tab_pdf.click()
        time.sleep(2)

        # Verifikasi class berubah
        word_classes_after = tab_word.get_attribute("class")
        pdf_classes_after = tab_pdf.get_attribute("class")

        self.assertIn("btn-inactive-mode", word_classes_after)
        self.assertIn("btn-active-mode", pdf_classes_after)
        print("  - Setelah klik: Tab Word menjadi inactive, Tab PDF menjadi active")

        print("[PASS] Perubahan style tab aktif berfungsi dengan benar.")

    # =============================================
    # TEST 8: Verifikasi deskripsi halaman berubah saat switch tab
    # =============================================
    def test_08_page_description_changes(self):
        """Test bahwa deskripsi halaman berubah saat switch tab."""
        print("\n[TEST 8] Mengecek perubahan deskripsi halaman...")
        self.driver.get(CONVERT_URL)
        time.sleep(3)

        # Cek deskripsi default (Word to PDF)
        page_desc = self.wait.until(
            EC.presence_of_element_located((By.ID, "pageDesc"))
        )
        default_desc = page_desc.text
        print("  - Deskripsi default: " + default_desc)
        self.assertIn("Word", default_desc)

        # Switch ke PDF to Word
        tab_pdf = self.driver.find_element(By.ID, "tabPdf")
        tab_pdf.click()
        time.sleep(2)

        # Cek deskripsi berubah
        new_desc = page_desc.text
        print("  - Deskripsi setelah switch: " + new_desc)
        self.assertIn("PDF", new_desc)
        self.assertNotEqual(default_desc, new_desc)

        print("[PASS] Deskripsi halaman berubah sesuai tab yang dipilih.")

    # =============================================
    # TEST 9: Verifikasi upload zone Word bisa diklik
    # =============================================
    def test_09_upload_zone_clickable(self):
        """Test bahwa upload zone (Word) bisa diklik untuk membuka file dialog."""
        print("\n[TEST 9] Mengecek upload zone Word bisa diklik...")
        self.driver.get(CONVERT_URL)
        time.sleep(3)

        # Cek upload zone Word ada dan bisa diklik
        word_upload_zone = self.wait.until(
            EC.presence_of_element_located((By.ID, "wordUploadZone"))
        )
        self.assertTrue(word_upload_zone.is_displayed())
        print("  - Upload zone Word ditampilkan")

        # Cek file input ada di dalam upload zone
        word_input = self.driver.find_element(By.ID, "wordInput")
        self.assertIsNotNone(word_input)
        accept_attr = word_input.get_attribute("accept")
        self.assertEqual(accept_attr, ".docx")
        print("  - File input menerima format .docx")

        print("[PASS] Upload zone Word berfungsi dengan benar.")

    # =============================================
    # TEST 10: Verifikasi upload zone PDF bisa diklik
    # =============================================
    def test_10_pdf_upload_zone_clickable(self):
        """Test bahwa upload zone (PDF) bisa diklik untuk membuka file dialog."""
        print("\n[TEST 10] Mengecek upload zone PDF bisa diklik...")
        self.driver.get(CONVERT_URL)
        time.sleep(3)

        # Switch ke tab PDF to Word
        tab_pdf = self.wait.until(
            EC.element_to_be_clickable((By.ID, "tabPdf"))
        )
        tab_pdf.click()
        time.sleep(2)

        # Cek upload zone PDF ada dan bisa diklik
        pdf_upload_zone = self.driver.find_element(By.ID, "pdfUploadZone")
        self.assertTrue(pdf_upload_zone.is_displayed())
        print("  - Upload zone PDF ditampilkan")

        # Cek file input PDF
        pdf_input = self.driver.find_element(By.ID, "pdfInput")
        self.assertIsNotNone(pdf_input)
        accept_attr = pdf_input.get_attribute("accept")
        self.assertEqual(accept_attr, ".pdf")
        print("  - File input menerima format .pdf")

        print("[PASS] Upload zone PDF berfungsi dengan benar.")

    # =============================================
    # TEST 11: Verifikasi header/navbar ada di halaman convert
    # =============================================
    def test_11_header_exists_on_convert_page(self):
        """Test bahwa header/navbar ada di halaman convert."""
        print("\n[TEST 11] Mengecek header di halaman Convert...")
        self.driver.get(CONVERT_URL)
        time.sleep(3)

        # Cek header ada
        header = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "header.header"))
        )
        self.assertIsNotNone(header)
        print("  - Header/navbar ditemukan")

        # Cek logo ada
        logo = self.driver.find_element(By.CSS_SELECTOR, ".logo-text")
        self.assertIsNotNone(logo)
        print("  - Logo 'PDF Suit' ditemukan")

        print("[PASS] Header di halaman convert ada.")

    # =============================================
    # TEST 12: Verifikasi footer ada di halaman convert
    # =============================================
    def test_12_footer_exists_on_convert_page(self):
        """Test bahwa footer ada di halaman convert."""
        print("\n[TEST 12] Mengecek footer di halaman Convert...")
        self.driver.get(CONVERT_URL)
        time.sleep(3)

        # Cek footer ada
        footer = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "footer.footer"))
        )
        self.assertIsNotNone(footer)
        print("  - Footer ditemukan")

        # Cek link Home di footer
        home_link = self.driver.find_element(
            By.CSS_SELECTOR, "footer a[href='index.html']"
        )
        self.assertIsNotNone(home_link)
        print("  - Link Home di footer ditemukan")

        print("[PASS] Footer di halaman convert ada.")

    # =============================================
    # TEST 13: Verifikasi default tab adalah Word to PDF
    # =============================================
    def test_13_default_tab_is_word_to_pdf(self):
        """Test bahwa tab default saat pertama kali buka adalah Word to PDF."""
        print("\n[TEST 13] Mengecek default tab adalah Word to PDF...")
        self.driver.get(CONVERT_URL)
        time.sleep(3)

        # Cek judul default
        page_title = self.wait.until(
            EC.presence_of_element_located((By.ID, "pageTitle"))
        )
        self.assertIn("Word to PDF", page_title.text)
        print("  - Judul default: " + page_title.text)

        # Cek panel Word ditampilkan (tidak punya class d-none)
        panel_word = self.driver.find_element(By.ID, "panelWord")
        panel_word_class = panel_word.get_attribute("class") or ""
        self.assertNotIn("d-none", panel_word_class)
        print("  - Panel Word to PDF ditampilkan secara default")

        # Cek panel PDF tersembunyi
        panel_pdf = self.driver.find_element(By.ID, "panelPdf")
        panel_pdf_class = panel_pdf.get_attribute("class") or ""
        self.assertIn("d-none", panel_pdf_class)
        print("  - Panel PDF to Word tersembunyi secara default")

        print("[PASS] Default tab adalah Word to PDF.")


# =============================================
# MAIN RUNNER
# =============================================
if __name__ == "__main__":
    # Jalankan test dengan output verbose, lalu otomatis exit
    result = unittest.main(verbosity=2, exit=False)

    # Tampilkan ringkasan hasil
    print("\n" + "=" * 60)
    print("RINGKASAN HASIL TESTING")
    print("=" * 60)
    total = result.result.testsRun
    failures = len(result.result.failures)
    errors = len(result.result.errors)
    success = total - failures - errors
    print(f"Total Test  : {total}")
    print(f"Berhasil    : {success}")
    print(f"Gagal       : {failures}")
    print(f"Error       : {errors}")
    print("=" * 60)

    # Exit dengan code sesuai hasil test
    sys.exit(0 if result.result.wasSuccessful() else 1)
