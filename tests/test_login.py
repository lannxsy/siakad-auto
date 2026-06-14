"""
test_login.py — Skenario Pengujian Fitur Login SIAKAD
=====================================================

Fitur yang diuji:
  - Login Guru berhasil
  - Login Siswa berhasil
  - Login dengan password salah
  - Login dengan No. Induk salah
  - Login dengan field kosong
  - Logout berhasil

Referensi source code:
  login.php  → form POST ke member.php
  member.php → validasi dari tabel `akun`, redirect ke admin/guru.php atau admin/siswa.php
"""

import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conftest import BASE_URL, GURU_INDUK, GURU_PASSWORD, SISWA_INDUK, SISWA_PASSWORD


# ─────────────────────────────────────────────────────────────
# Helper
# ─────────────────────────────────────────────────────────────

def buka_login(driver):
    driver.get(f"{BASE_URL}/login.php")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "induk"))
    )


def isi_form_login(driver, induk, password, level="guru"):
    """Isi form login dan klik tombol Login."""
    radio = driver.find_element(By.CSS_SELECTOR, f'input[name="level"][value="{level}"]')
    radio.click()

    field_induk = driver.find_element(By.NAME, "induk")
    field_induk.clear()
    field_induk.send_keys(induk)

    field_password = driver.find_element(By.NAME, "password")
    field_password.clear()
    field_password.send_keys(password)

    driver.find_element(By.CSS_SELECTOR, 'input[type="submit"][value="Login"]').click()
    time.sleep(2)  # tunggu redirect atau alert


def tangkap_alert(driver, timeout=4):
    """Tangkap teks alert JS jika ada, lalu dismiss."""
    try:
        alert = WebDriverWait(driver, timeout).until(EC.alert_is_present())
        teks = alert.text
        alert.accept()
        return teks
    except Exception:
        return None


# ─────────────────────────────────────────────────────────────
# Test Cases
# ─────────────────────────────────────────────────────────────

class TestLogin:

    # TC-LOGIN-01
    def test_login_guru_berhasil(self, driver):
        """
        TC-LOGIN-01: Login sebagai Guru dengan kredensial valid.
        Expected: diarahkan ke admin/guru.php dan terlihat menu Beranda.
        """
        buka_login(driver)
        isi_form_login(driver, GURU_INDUK, GURU_PASSWORD, level="guru")

        WebDriverWait(driver, 10).until(EC.url_contains("guru.php"))
        assert "guru.php" in driver.current_url, (
            f"TC-LOGIN-01 GAGAL: URL seharusnya mengandung 'guru.php', "
            f"tapi URL saat ini: {driver.current_url}"
        )
        assert "Beranda" in driver.page_source, "TC-LOGIN-01 GAGAL: Menu Beranda tidak ditemukan."

    # TC-LOGIN-02
    def test_login_siswa_berhasil(self, driver):
        """
        TC-LOGIN-02: Login sebagai Siswa dengan kredensial valid.
        Expected: diarahkan ke admin/siswa.php.
        """
        buka_login(driver)
        isi_form_login(driver, SISWA_INDUK, SISWA_PASSWORD, level="siswa")

        WebDriverWait(driver, 10).until(EC.url_contains("siswa.php"))
        assert "siswa.php" in driver.current_url, (
            f"TC-LOGIN-02 GAGAL: URL seharusnya 'siswa.php', "
            f"tapi: {driver.current_url}"
        )

    # TC-LOGIN-03
    def test_login_password_salah(self, driver):
        """
        TC-LOGIN-03: Login dengan password yang salah.
        Expected: muncul alert 'No. Induk/Password/Status Salah' dan kembali ke login.php.
        """
        buka_login(driver)
        isi_form_login(driver, GURU_INDUK, "passwordsalah", level="guru")

        alert_text = tangkap_alert(driver)
        assert alert_text is not None, "TC-LOGIN-03 GAGAL: Alert tidak muncul."
        assert "Salah" in alert_text, (
            f"TC-LOGIN-03 GAGAL: Pesan alert tidak sesuai. Alert: '{alert_text}'"
        )
        WebDriverWait(driver, 5).until(EC.url_contains("login.php"))
        assert "login.php" in driver.current_url

    # TC-LOGIN-04
    def test_login_induk_salah(self, driver):
        """
        TC-LOGIN-04: Login dengan No. Induk yang tidak terdaftar.
        Expected: muncul alert error.
        """
        buka_login(driver)
        isi_form_login(driver, "99999999", GURU_PASSWORD, level="guru")

        alert_text = tangkap_alert(driver)
        assert alert_text is not None, "TC-LOGIN-04 GAGAL: Alert tidak muncul."
        assert "Salah" in alert_text, (
            f"TC-LOGIN-04 GAGAL: Pesan alert tidak sesuai. Alert: '{alert_text}'"
        )

    # TC-LOGIN-05
    def test_login_field_kosong(self, driver):
        """
        TC-LOGIN-05: Login tanpa mengisi No. Induk maupun Password.
        Expected: browser memblokir submit (HTML5 required) atau tetap di login.php.
        """
        buka_login(driver)
        # Langsung klik submit tanpa isi field
        driver.find_element(By.CSS_SELECTOR, 'input[type="submit"][value="Login"]').click()
        time.sleep(1)

        # HTML5 'required' memblokir submit — tetap di login.php atau member.php
        # Kita pastikan TIDAK redirect ke guru.php / siswa.php
        assert "guru.php" not in driver.current_url and "siswa.php" not in driver.current_url, (
            "TC-LOGIN-05 GAGAL: Form terkirim meski field kosong."
        )

    # TC-LOGIN-06
    def test_logout_berhasil(self, driver):
        """
        TC-LOGIN-06: Logout dari sesi guru yang aktif.
        Expected: sesi dihancurkan dan diarahkan kembali ke index.php.
        """
        buka_login(driver)
        isi_form_login(driver, GURU_INDUK, GURU_PASSWORD, level="guru")
        WebDriverWait(driver, 10).until(EC.url_contains("guru.php"))

        # Klik link Keluar
        driver.find_element(By.LINK_TEXT, "Keluar").click()
        try:
            alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
            alert.accept()
        except Exception:
            pass  # headless kadang tidak menampilkan confirm dialog

        time.sleep(1.5)
        assert "guru.php" not in driver.current_url, (
            "TC-LOGIN-06 GAGAL: Pengguna masih di halaman guru setelah logout."
        )

    # TC-LOGIN-07
    def test_akses_tanpa_login_redirect(self, driver):
        """
        TC-LOGIN-07: Akses langsung ke halaman admin tanpa login.
        Expected: muncul alert 'Anda Harus Login' dan di-redirect ke login.php.
        """
        driver.get(f"{BASE_URL}/admin/guru.php")
        time.sleep(1.5)

        alert_text = tangkap_alert(driver)
        redirected = "login.php" in driver.current_url or "index.php" in driver.current_url
        assert redirected or (alert_text and ("Login" in alert_text or "Guru" in alert_text)), (
            "TC-LOGIN-07 GAGAL: Halaman admin bisa diakses tanpa login."
        )
