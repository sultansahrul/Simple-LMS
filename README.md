# Simple LMS - Progress 1: Docker & Django Foundation

**Nama:** Sultan Sahrul Abdullah  
**Mata Kuliah:** Pemrograman Sisi Server

Proyek ini adalah implementasi tahap awal (Progress 1) untuk membangun Simple LMS. Fokus utama pada tahapan ini adalah melakukan setup *environment development* menggunakan Docker, konfigurasi Django, dan menghubungkannya dengan database PostgreSQL.

---

## 🚀 Cara Menjalankan Project

1. Pastikan Docker Desktop sudah menyala.
2. Clone repository ini dan buka terminal di dalam direktori project.
3. Buat file `.env` di direktori utama, lalu copy isi dari `.env.example` ke dalamnya.
4. Jalankan perintah ini untuk melakukan build dan menjalankan container:
   ```bash
   docker compose up -d --build
   ```
5. Lakukan migrasi database untuk membuat tabel bawaan Django di PostgreSQL:
   ```bash
   docker compose exec web python manage.py migrate
   ```
6. Buka browser dan akses aplikasi di: **http://localhost:8000**

---

## ⚙️ Environment Variables Explanation

Konfigurasi koneksi dan pengaturan rahasia disimpan dalam file `.env`. Berikut adalah detail fungsinya:

* `POSTGRES_DB`: Nama database PostgreSQL yang dibuat (contoh: lms_db).
* `POSTGRES_USER`: Username untuk autentikasi ke database.
* `POSTGRES_PASSWORD`: Password untuk user database.
* `DB_HOST`: Host dari database. Diisi `db` (sesuai nama service di docker-compose) agar Django bisa terhubung via internal network Docker.
* `DB_PORT`: Port PostgreSQL (5432).
* `SECRET_KEY`: Kunci enkripsi utama yang digunakan oleh Django untuk keamanan session dan *cryptographic signing*.
* `DEBUG`: Diset `True` untuk menampilkan detail log/error selama proses development.

---

## 📸 Dokumentasi

### Screenshot Django Welcome Page
![Django Welcome Page](img/django-welcome.png)