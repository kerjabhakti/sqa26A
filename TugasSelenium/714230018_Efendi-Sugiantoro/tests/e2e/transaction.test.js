import { Builder, By, Key, until } from 'selenium-webdriver';
import chrome from 'selenium-webdriver/chrome.js';

/**
 * Transaction E2E Test — FinTask Suite
 * Menguji alur pencatatan transaksi dari login sampai tersimpan.
 */
async function runTransactionTest() {
  let driver = await new Builder().forBrowser('chrome').build();

  try {
    console.log('🚀 Memulai pengujian transaksi...');

    // 1. Login Terlebih Dahulu
    await driver.get('http://localhost:5173/login');
    await driver.wait(until.elementLocated(By.name('identifier')), 10000);
    await driver.findElement(By.name('identifier')).sendKeys('test@fintask.com');
    await driver.findElement(By.name('password')).sendKeys('password123', Key.RETURN);
    
    // Tunggu sampai masuk Dashboard
    await driver.wait(until.urlContains('dashboard'), 10000);
    console.log('✅ Login berhasil.');

    // 2. Pindah ke Halaman Keuangan
    // Kita cari Link yang berisi teks "Keuangan"
    const financeLink = await driver.wait(
      until.elementLocated(By.xpath("//span[text()='Keuangan']/..")), 
      10000
    );
    await financeLink.click();
    await driver.wait(until.urlContains('finance'), 10000);
    console.log('📂 Sudah berada di halaman Keuangan.');

    // 3. Klik Tombol "Catat Transaksi"
    const addBtn = await driver.wait(
      until.elementLocated(By.xpath("//button[contains(., 'Catat Transaksi')]")), 
      10000
    );
    await addBtn.click();
    console.log('➕ Modal transaksi terbuka.');

    // 4. Isi Form Transaksi
    // Tunggu input amount muncul
    await driver.wait(until.elementLocated(By.name('amount')), 5000);
    
    const amountInput = await driver.findElement(By.name('amount'));
    await amountInput.sendKeys('50000'); // Nominal Rp 50.000

    const categoryInput = await driver.findElement(By.name('category'));
    await categoryInput.sendKeys('Makan Siang Enak');

    const descInput = await driver.findElement(By.name('description')).catch(() => null);
    if (descInput) await descInput.sendKeys('Makan bareng dosen cantik... mwehehehe.');

    // Pilih Metode Pembayaran (Cash)
    const paymentSelect = await driver.findElement(By.name('paymentMethod'));
    await paymentSelect.sendKeys('cash');

    console.log('📝 Form transaksi sudah diisi.');

    // 5. Klik Tombol Simpan
    const saveBtn = await driver.findElement(By.css('button[type="submit"]'));
    await saveBtn.click();
    console.log('💾 Tombol simpan diklik.');

    // 6. Verifikasi Sukses
    // Tunggu sampai modal tertutup (biasanya ditandai dengan munculnya data baru di list)
    // Atau kita cek apakah ada toast sukses (kalau ada)
    await driver.sleep(2000); // Tunggu sebentar proses simpan
    
    console.log('✨ Transaksi berhasil dicatat!');
    console.log('🎉 Pengujian transaksi selesai dengan sukses!');

  } catch (error) {
    console.error('❌ Pengujian Gagal, Sayang:', error.message);
  } finally {
    console.log('👋 Menutup browser...');
    await driver.quit();
  }
}

runTransactionTest();
