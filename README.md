# 🧪 Pengujian Otomatis SIAKAD dengan Selenium + CI/CD GitHub Actions

> **Judul Tugas:** Pengujian Otomatis Sistem Informasi Akademik (SIAKAD) Berbasis Web dengan CI/CD GitHub Actions

---

## 📋 Daftar Isi
1. [Analisis Fitur yang Diuji](#1-analisis-fitur-yang-diuji)
2. [Skenario & Test Case](#2-skenario--test-case)
3. [Struktur Folder Project](#3-struktur-folder-project)
4. [Langkah Menjalankan Lokal](#4-langkah-menjalankan-lokal)
5. [Penjelasan CI/CD GitHub Actions](#5-penjelasan-cicd-github-actions)
6. [Cara Membaca Laporan Pengujian](#6-cara-membaca-laporan-pengujian)

---

## 1. Analisis Fitur yang Diuji

Berdasarkan analisis source code SIAKAD (`webakademik/`), fitur-fitur berikut **paling cocok** untuk diuji dengan Selenium:

| No | Fitur              | File Utama                          | Alasan Dipilih |
|----|--------------------|-------------------------------------|----------------|
| 1  | **Login / Logout** | `login.php`, `member.php`           | Entry point utama, ada validasi session & alert JS |
| 2  | **Data Siswa**     | `tambahsiswa.php`, `lihatsiswa.php` | CRUD dengan validasi NIS numerik, file upload |
| 3  | **Nilai Siswa**    | `nilaisiswa.php`                    | Validasi angka, proteksi duplikat, 5 mata pelajaran |

---

## 2. Skenario & Test Case

### 🔐 Fitur Login (`test_login.py`)

| ID Test       | Skenario                          | Input                         | Expected Result                              |
|---------------|-----------------------------------|-------------------------------|----------------------------------------------|
| TC-LOGIN-01   | Login Guru berhasil               | Induk & password benar, Guru  | Redirect ke `admin/guru.php`                 |
| TC-LOGIN-02   | Login Siswa berhasil              | Induk & password benar, Siswa | Redirect ke `admin/siswa.php`                |
| TC-LOGIN-03   | Login password salah              | Password salah                | Alert "No. Induk/Password/Status Salah"      |
| TC-LOGIN-04   | Login No. Induk tidak terdaftar   | Induk tidak ada               | Alert error, tetap di `login.php`            |
| TC-LOGIN-05   | Login field kosong                | Semua field kosong            | Form tidak terkirim (HTML5 `required`)       |
| TC-LOGIN-06   | Logout berhasil                   | Klik "Keluar"                 | Sesi dihapus, redirect ke halaman awal       |
| TC-LOGIN-07   | Akses admin tanpa login           | URL langsung `admin/guru.php` | Alert + redirect ke `login.php`              |

### 👩‍🎓 Fitur Data Siswa (`test_data_siswa.py`)

| ID Test        | Skenario                          | Input                        | Expected Result                             |
|----------------|-----------------------------------|------------------------------|---------------------------------------------|
| TC-SISWA-01    | Tambah siswa valid                | Semua field terisi benar     | Alert "Data Berhasil Ditambahkan"           |
| TC-SISWA-02    | Tambah siswa NIS huruf            | NIS = "ABCDE"                | Alert "NIS Harus Berupa Angka"              |
| TC-SISWA-03    | Lihat daftar siswa                | Akses `lihatsiswa.php`       | Halaman terbuka dengan daftar siswa         |
| TC-SISWA-04    | Cari siswa berdasarkan NIS        | Keyword = NIS                | Hasil pencarian menampilkan siswa           |
| TC-SISWA-05    | Akses tambah siswa tanpa login    | Tanpa sesi                   | Alert + redirect ke `login.php`             |
| TC-SISWA-06    | Submit form dengan NIS kosong     | NIS kosong                   | Validasi browser / server menolak           |

### 📊 Fitur Nilai Siswa (`test_nilai_siswa.py`)

| ID Test        | Skenario                         | Input                           | Expected Result                                   |
|----------------|----------------------------------|---------------------------------|---------------------------------------------------|
| TC-NILAI-01    | Buka halaman nilai NIS valid     | `?nis=9901`                     | Halaman "Tambah Nilai Siswa" terbuka              |
| TC-NILAI-02    | Tambah nilai valid               | Semua nilai angka 0–100         | Alert "Nilai Berhasil Ditambahkan"                |
| TC-NILAI-03    | Tambah nilai bukan angka         | `uh1="A+"`, `uts="ok"`         | Alert "Nilai Harus Berupa Angka"                  |
| TC-NILAI-04    | Nilai duplikat (mapel sama)      | Mapel + NIS sama, submit 2×     | Alert "Nilai ... Pernah Ditambahkan"              |
| TC-NILAI-05    | NIS tidak ada di database        | `?nis=00000`                    | Alert "NIS Tidak Ada" + redirect                  |
| TC-NILAI-06    | Akses halaman nilai tanpa login  | Tanpa sesi                      | Alert + redirect ke `login.php`                   |

---

## 3. Struktur Folder Project

```
siakad_testing/               ← Root project pengujian
│
├── .github/
│   └── workflows/
│       └── test.yml          ← GitHub Actions CI/CD workflow
│
├── tests/
│   ├── conftest.py           ← Konfigurasi global & fixture driver
│   ├── test_login.py         ← Test Case Login & Logout (TC-LOGIN-01~07)
│   ├── test_data_siswa.py    ← Test Case Data Siswa (TC-SISWA-01~06)
│   └── test_nilai_siswa.py   ← Test Case Nilai Siswa (TC-NILAI-01~06)
│
├── reports/                  ← Laporan hasil test (di-generate otomatis)
│   ├── laporan_pengujian.html
│   └── output_log.txt
│
├── pytest.ini                ← Konfigurasi pytest
├── requirements.txt          ← Daftar dependensi Python
└── README.md                 ← Dokumentasi ini
```

> **Catatan:** Folder `webakademik/` (source code PHP SIAKAD) harus berada satu level dengan folder `tests/` di root repository agar GitHub Actions bisa mengaksesnya.

---

## 4. Langkah Menjalankan Lokal

### Prasyarat
- Python 3.8+
- Google Chrome (terbaru)
- XAMPP / LAMP / Laragon (PHP + MySQL)
- SIAKAD berjalan di `http://localhost/webakademik`

### Langkah-langkah

```bash
# 1. Clone atau masuk ke folder project testing
cd siakad_testing

# 2. Buat virtual environment Python (disarankan)
python -m venv venv

# Aktivasi (Windows)
venv\Scripts\activate

# Aktivasi (Mac/Linux)
source venv/bin/activate

# 3. Install dependensi
pip install -r requirements.txt

# 4. Pastikan SIAKAD sudah berjalan
#    - Jalankan XAMPP / Laragon
#    - Import database siakad.sql ke MySQL
#    - Akses http://localhost/webakademik/ di browser → harus tampil halaman awal

# 5. Sesuaikan konfigurasi di tests/conftest.py
#    BASE_URL      = "http://localhost/webakademik"
#    GURU_INDUK    = "guru01"   ← sesuaikan dengan akun di DB Anda
#    GURU_PASSWORD = "123456"   ← sesuaikan

# 6. Jalankan semua test
pytest

# Atau dengan laporan HTML
pytest --html=reports/laporan_pengujian.html --self-contained-html

# Jalankan satu file saja
pytest tests/test_login.py -v

# Jalankan satu test case tertentu
pytest tests/test_login.py::TestLogin::test_login_guru_berhasil -v

# Mode tidak headless (agar bisa lihat browser)
# Edit conftest.py, hapus baris: chrome_options.add_argument("--headless")
```

---

## 5. Penjelasan CI/CD GitHub Actions

### Cara Kerja

```
Developer push kode ke GitHub
         │
         ▼
GitHub Actions mendeteksi event push
         │
         ▼
Runner Ubuntu disiapkan secara otomatis
         │
    ┌────┴────────────────────────┐
    │ Langkah Otomatis:           │
    │ 1. Checkout kode            │
    │ 2. Install PHP + Apache     │
    │ 3. Deploy SIAKAD ke Apache  │
    │ 4. Jalankan MySQL Service   │
    │ 5. Import database          │
    │ 6. Seed data akun testing   │
    │ 7. Install Python & library │
    │ 8. Install Chrome           │
    │ 9. Jalankan pytest          │
    │10. Upload laporan HTML      │
    └─────────────────────────────┘
         │
         ▼
  ✅ PASS / ❌ FAIL
  (notifikasi di GitHub)
```

### File Workflow: `.github/workflows/test.yml`

```
Trigger (on:)        → push ke main/master ATAU pull request
Job (selenium-test)  → berjalan di ubuntu-latest
Service (mysql)      → container MySQL 8.0 otomatis disiapkan
Steps                → 10 langkah dari setup hingga laporan
Artifact             → laporan HTML disimpan 30 hari
```

### Cara Setup di Repository GitHub

```bash
# 1. Pastikan struktur repository seperti ini:
your-repo/
  ├── webakademik/          ← source code PHP SIAKAD
  ├── siakad.sql            ← file dump database
  ├── tests/                ← folder test Selenium
  ├── .github/workflows/    ← file workflow CI/CD
  ├── pytest.ini
  └── requirements.txt

# 2. Push ke GitHub
git add .
git commit -m "feat: tambah pengujian otomatis Selenium"
git push origin main

# 3. Buka tab Actions di GitHub → lihat workflow berjalan otomatis
# 4. Setelah selesai → tab Actions → pilih run → Download Artifacts
#    untuk melihat laporan HTML pengujian
```

---

## 6. Cara Membaca Laporan Pengujian

Setelah test selesai, buka file `reports/laporan_pengujian.html` di browser.

| Ikon | Arti |
|------|------|
| ✅ PASSED | Test case berhasil, sistem berfungsi sesuai ekspektasi |
| ❌ FAILED | Test case gagal, ada bug atau konfigurasi salah |
| ⚠️ SKIPPED | Test dilewati (biasanya karena data prasyarat tidak ada) |
| ⏱️ Duration | Waktu eksekusi per test case |

---

## Teknologi yang Digunakan

| Teknologi | Versi | Fungsi |
|-----------|-------|--------|
| Python | 3.11 | Bahasa pemrograman test |
| Selenium | 4.18 | Otomasi browser Chrome |
| pytest | 8.1 | Test runner & pelaporan |
| pytest-html | 4.1 | Generate laporan HTML |
| webdriver-manager | 4.0 | Auto-download ChromeDriver |
| GitHub Actions | — | Platform CI/CD |
| Ubuntu | latest | OS runner CI/CD |
| MySQL | 8.0 | Database (service container) |
| Apache + PHP | 8.1 | Web server SIAKAD |
