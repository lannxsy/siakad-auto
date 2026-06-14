"""
conftest.py - Konfigurasi global untuk pytest + Selenium
SIAKAD Testing Suite
"""

import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# ============================================================
# KONFIGURASI — sesuaikan BASE_URL dengan environment Anda
# ============================================================
BASE_URL = "http://localhost/siakad_testing\webakademik"   # ganti jika beda

# Kredensial disesuaikan dengan data di tabel `akun` pada 11732.sql
# induk=1, password='guru', level='guru'
GURU_INDUK = "1"
GURU_PASSWORD = "guru"

# induk=2000, password='murid', level='siswa'
SISWA_INDUK = "2000"
SISWA_PASSWORD = "murid"

IMPLICIT_WAIT = 5                           # detik tunggu elemen


@pytest.fixture(scope="session")
def driver():
    """
    Membuat instance ChromeDriver satu kali per sesi pengujian.
    Headless mode aktif secara default (untuk CI/CD).
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1280,900")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-popup-blocking")

    # Gunakan webdriver-manager (tidak perlu chromedriver_binary)
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium.webdriver.chrome.service import Service
        service = Service(ChromeDriverManager().install())
        drv = webdriver.Chrome(service=service, options=chrome_options)
    except Exception:
        # Fallback: ChromeDriver sudah ada di PATH
        drv = webdriver.Chrome(options=chrome_options)

    drv.implicitly_wait(IMPLICIT_WAIT)
    yield drv
    drv.quit()


@pytest.fixture(autouse=True)
def reset_session(driver):
    """Kembali ke halaman logout sebelum setiap test agar sesi bersih.
    Logout ada di admin/logout.php (bukan /logout.php).
    """
    driver.get(f"{BASE_URL}/admin/logout.php")
    time.sleep(0.5)
