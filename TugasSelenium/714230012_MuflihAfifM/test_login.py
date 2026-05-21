import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class TestLoginManualPDFSuit(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Setup browser dan konfigurasi laporan sebelum tes berjalan"""
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.maximize_window()
        cls.base_url = "https://pdfmulbi.github.io" # Diarahkan ke github pages live milikmu
        cls.wait = WebDriverWait(cls.driver, 10)
        
        # Variabel penampung hasil laporan
        cls.status_test = "FAILED"
        cls.detail_log = "Pengujian dihentikan sebelum user sukses berpindah halaman."

    @classmethod
    def tearDownClass(cls):
        """Tutup browser dan generate laporan setelah testing selesai"""
        print("-> Menutup browser otomatis.")
        cls.driver.quit()
        
        # ==================================================
        # PROSES OTOMATISASI GENERATE FILE LAPORAN (.TXT & .PDF)
        # ==================================================
        # 1. Cetak Laporan Teks (.txt)
        with open("laporan_testing.txt", "w") as txt_file:
            txt_file.write("==================================================\n")
            txt_file.write("          LAPORAN PENGUJIAN UNITTEST-MANUAL       \n")
            txt_file.write("==================================================\n")
            txt_file.write(f"Modul Fitur   : Form Otentikasi Login (PDF Suit)\n")
            txt_file.write(f"Metode Input  : User Manual Input (Unittest Class)\n")
            txt_file.write(f"Status Akhir  : {cls.status_test}\n")
            txt_file.write(f"Detail Log    : {cls.detail_log}\n")
            txt_file.write("==================================================\n")
        print("-> Berhasil mencetak berkas: 'laporan_testing.txt'")

        # 2. Cetak Laporan PDF (.pdf)
        c = canvas.Canvas("laporan_testing.pdf", pagesize=letter)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, 750, "LAPORAN HASIL TESTING - FORM LOGIN")
        c.setLineWidth(1)
        c.line(50, 740, 550, 740)
        
        c.setFont("Helvetica", 11)
        c.drawString(50, 700, f"Metode Uji       : Unittest Framework + Manual Input Driver")
        c.drawString(50, 680, f"Waktu Eksekusi   : {time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        if cls.status_test == "PASSED":
            c.setFillColorRGB(0, 0.5, 0) # Warna Hijau
        else:
            c.setFillColorRGB(0.8, 0, 0) # Warna Merah
            
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, 640, f"STATUS KELULUSAN : {cls.status_test}")
        
        c.setFillColorRGB(0, 0, 0)
        c.setFont("Helvetica", 10)
        c.drawString(50, 600, "Bukti Riwayat Jalur Kerja:")
        c.drawString(50, 580, cls.detail_log[:120]) 
        c.save()
        print("-> Berhasil mencetak berkas: 'laporan_testing.pdf'")

    def test_01_manual_login_flow(self):
        """Test login menahan otomatisasi untuk input manual"""
        driver = self.driver
        print("\n==================================================")
        print("-> Membuka halaman login PDF Suit...")
        driver.get(f"{self.base_url}/login.html")
        
        # Tunggu sampai kolom input email terdeteksi (Gaya kodingan temanmu)
        self.wait.until(EC.presence_of_element_located((By.NAME, "email")))
        
        print("\n[ROBOT DI-PAUSE] Unittest mendeteksi form siap!")
        print("--> SILAKAN KETIK EMAIL & PASSWORD MANUAL DI CHROME... <--")
        print("--> LALU KLIK TOMBOL LOGIN DI WEB... <--")
        
        # Robot memantau perpindahan halaman secara live selama maksimal 60 detik
        waktu_mulai = time.time()
        success = False
        
        while time.time() - waktu_mulai < 60:
            url_sekarang = driver.current_url
            if "login.html" not in url_sekarang:
                success = True
                break
            time.sleep(1)
            
        # Validasi Assert ala Unittest Framework
        if success:
            TestLoginManualPDFSuit.status_test = "PASSED"
            TestLoginManualPDFSuit.detail_log = f"User sukses login manual. URL berubah ke: {driver.current_url}"
            print("\n✓ TEST LOGIN BERHASIL ✅")
        else:
            TestLoginManualPDFSuit.status_test = "FAILED"
            TestLoginManualPDFSuit.detail_log = "Waktu tunggu input manual habis (Timeout 60 detik)."
            print("\n⚠ TEST LOGIN GAGAL / TIMEOUT ❌")
            self.fail("Gagal karena user tidak melakukan login hingga batas waktu habis.")

        print("-> Menahan tampilan akhir selama 5 detik...")
        time.sleep(5)
        print("==================================================")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("SELENIUM MANU-AUTOMATION TEST FOR PDF SUIT")
    print("="*60 + "\n")
    
    # Jalankan unittest suite
    unittest.main(verbosity=2)