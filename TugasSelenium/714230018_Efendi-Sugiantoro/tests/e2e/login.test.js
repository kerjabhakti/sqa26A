import { Builder, By, Key, until } from 'selenium-webdriver';
import chrome from 'selenium-webdriver/chrome.js';

/**
 * Login E2E Test — FinTask Suite
 * Memastikan alur login manual (password) berjalan dengan mulus.
 */
async function runLoginTest() {
  // Setup Chrome Options (Opsional: tambahkan --headless kalau mau tanpa jendela browser)
  let options = new chrome.Options();
  
  // 1. Inisialisasi Driver
  let driver = await new Builder()
    .forBrowser('chrome')
    .setChromeOptions(options)
    .build();

  try {
    console.log('🚀 Memulai pengujian login...');

    // 2. Navigasi ke Halaman Login (Pastikan app kamu jalan di port 5173!)
    await driver.get('http://localhost:5173/login');

    // 3. Tunggu sampai input 'identifier' muncul (maksimal 10 detik)
    await driver.wait(until.elementLocated(By.name('identifier')), 10000);

    // 4. Masukkan Username/Email
    // (Gunakan data test yang ada di database kamu ya!)
    const identifierInput = await driver.findElement(By.name('identifier'));
    await identifierInput.sendKeys('test@fintask.com'); 
    console.log('✅ Input identifier diisi.');

    // 5. Masukkan Password
    const passwordInput = await driver.findElement(By.name('password'));
    await passwordInput.sendKeys('password123');
    console.log('✅ Input password diisi.');

    // 6. Klik tombol Submit
    const submitButton = await driver.findElement(By.css('button[type="submit"]'));
    await submitButton.click();
    console.log('🖱️ Tombol login diklik.');

    // 7. Verifikasi apakah kita berhasil masuk ke Dashboard
    // Kita tunggu sampai URL-nya berubah mengandung kata 'dashboard'
    await driver.wait(until.urlContains('dashboard'), 10000);
    
    const currentUrl = await driver.getCurrentUrl();
    console.log(`✨ Sukses! Sekarang berada di: ${currentUrl}`);
    console.log('🎉 Pengujian login berhasil diselesaikan tanpa hambatan!');

  } catch (error) {
    console.error('❌ Pengujian Gagal, Sayang:', error.message);
  } finally {
    // 8. Tutup browser biar nggak berat
    console.log('👋 Menutup browser...');
    await driver.quit();
  }
}

// Jalankan test-nya
runLoginTest();
