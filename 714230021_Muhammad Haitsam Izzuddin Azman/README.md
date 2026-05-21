# 🧪 Selenium Test - GOPOS Login & Register

Test otomatis menggunakan **Selenium WebDriver** untuk menguji fitur **Login** dan **Register** pada aplikasi [GOPOS](https://goposind.github.io) (GO-LANG POS ASSISTANT).

---

## 📋 Daftar Test Case

| No | Test Case | Tipe | Deskripsi |
|----|-----------|------|-----------|
| 1 | `test_1_register` | ✅ Positive | Register akun baru dengan data valid |
| 2 | `test_2_login` | ✅ Positive | Login dengan akun yang baru didaftarkan |
| 3 | `test_3_login_wrong_password` | ❌ Negative | Login dengan password yang salah |
| 4 | `test_4_register_password_mismatch` | ❌ Negative | Register dengan confirm password berbeda |

---

## ⚙️ Prasyarat (Prerequisites)

1. **Python 3.8+** — Pastikan Python sudah terinstall
   ```bash
   python --version
   ```

2. **Google Chrome** — Browser Chrome terbaru

3. **ChromeDriver** — Otomatis dikelola oleh Selenium 4.x (tidak perlu download manual)

---

## 🚀 Cara Instalasi

1. **Clone repository** (jika belum):
   ```bash
   git clone <repository-url>
   cd 714230021_Muhammad\ Haitsam\ Izzuddin\ Azman
   ```

2. **Install Selenium**:
   ```bash
   pip install selenium
   ```

---

## ▶️ Cara Menjalankan Test

### Jalankan semua test:
```bash
python test_login_register.py
```

### Jalankan dengan pytest (opsional):
```bash
pip install pytest
pytest test_login_register.py -v
```

---

## 📊 Laporan Hasil Test (HTML Report)

Setelah test selesai dijalankan, **laporan HTML akan otomatis dibuat dan dibuka di browser**.

File report disimpan di:
```
test_report.html
```

Report menampilkan:
- ✅ Status setiap test case (PASS / FAIL / ERROR)
- ⏱️ Durasi eksekusi setiap test
- 📝 Detail error jika ada test yang gagal
- 📈 Ringkasan total test

---

## 📁 Struktur File

```
714230021_Muhammad Haitsam Izzuddin Azman/
├── test_login_register.py    # File test Selenium utama
├── test_report.html          # Laporan hasil test (auto-generated)
├── README.md                 # Dokumentasi ini
├── backend-gopos/            # Backend API (Go-Lang)
└── goposind.github.io/       # Frontend Web App
```

---

## 🔧 Konfigurasi

Beberapa konfigurasi yang bisa diubah di dalam `test_login_register.py`:

| Variabel | Default | Keterangan |
|----------|---------|------------|
| `BASE_URL` | `https://goposind.github.io` | URL aplikasi yang ditest |
| `TEST_NAME` | `Test Selenium User` | Nama user untuk register |
| `TEST_PASSWORD` | `Test123456` | Password untuk test |
| `TEST_EMAIL` | Auto-generated (unik) | Email unik setiap kali run |

### Mode Headless (tanpa tampilan browser):
Uncomment baris berikut di dalam file test:
```python
chrome_options.add_argument("--headless")
```

---

## 📌 Catatan Penting

- Setiap kali test dijalankan, **email baru akan di-generate** secara otomatis menggunakan timestamp, sehingga tidak ada konflik email duplikat.
- Test berjalan secara **berurutan** (test 1 → 2 → 3 → 4).
- Pastikan **koneksi internet aktif** karena test mengakses website live.
- Browser Chrome akan **terbuka otomatis** saat test berjalan dan **tertutup otomatis** setelah selesai.

---

## 👤 Author

**Muhammad Haitsam Izzuddin Azman** — 714230021  
Tugas Software Quality Assurance
