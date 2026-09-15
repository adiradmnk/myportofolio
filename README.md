# Personal Portfolio - CSGE602022

Repositori ini merupakan karya pribadi untuk keperluan tugas mata kuliah wajib yaitu pemrograman berbasis platform (PBP) di Universitas Indonesia, portofolio ini secara berkala dalam satu semester akan terus di update 

## Informasi Mahasiswa
- **Nama** : Adriana Ainurrahmah Damanik
- **NPM** : 2506656375
- **Kelas** : PBP E

## Cara Menjalankan Proyek Secara Lokal
1. Pastikan Anda memiliki Python (versi 3.9+) yang sudah ter-install. (hal ini dikarenakan agar keperluan dependensi aja)
2. Buat dan aktifkan *virtual environment*:
   ```bash
   python -m venv env
   source env/bin/activate  # Untuk Mac
   # env\Scripts\activate   # ini command jika anda menggunakan windows
   ```
3. Install semua *dependencies*:
   ```bash
   pip install -r requirements.txt # ini merupakan command yang dipakai untuk menginstall smeua packages yang diperlukan guna agar jalannya program dapat berjalan sesuai dengan kebutuhannya
   ```
4. Jalankan server pengembangan lokal:
   ```bash
   python manage.py runserver # ini merupakan command untuk menjalankan server
   ```
5. Buka `http://localhost:8000/` di browser Anda. (untuk melihat hasil kode di browser)

jika anda hanya inign melihat hasil protofolio atau hasil compile dari kode yang sudah say abuat anda bisa membuka di [https://](https://adriana-ainurrahmah-myportofolio.pws.cs.ui.ac.id/)

---
## Tugas 1

**1. Penggunaan elemen semantik HTML5**
Ya, saya menggunakan elemen semantik HTML5 seperti `<section>` untuk membagi bagian 'Skills' dan 'Projects', serta `<article>` untuk masing-masing kartu proyek individual. Penggunaan elemen ini sangat membantu dalam menyusun static web karena memberikan struktur logika yang jelas tanpa harus bergantung pada banyak tag `<div>` yang membingungkan 

**2. Tantangan Responsive Layout**
Tantangan utamanya adalah mengelola hierarki informasi ketika ukuran layar menyusut ke mobile. Saya harus mengevaluasi ukuran elemen agar tidak saling berdempetan atau overflow. Solusinya, saya memprioritaskan pemisahan grid pada desktop sehingga otomatis berubah menjadi tumpukan vertikal pada layar mobile.

**3. Batasan Static Web & Rencana Dinamis**
Batasan utama dari static web murni adalah semua informasi harus dihardcode langsung ke dalam file HTML. Ini membuat pembaruan konten (misal menambah proyek baru atau memperbarui bio) menjadi tidak efisien karena harus mengedit kode sumber dan melakukan deployment ulang. Berdasarkan batasan tersebut, fungsionalitas dinamis yang paling ingin saya tambahkan di iterasi selanjutnya adalah arsitektur MVT (Model-View-Template) dengan database. Tujuannya agar saya bisa memisahkan konten (data project, skill) dari struktur tampilan.

### AI Disclosure
Walaupun saya mengetik secara menual untuk setiap baris kode, saya tetap menggunakan ai untuk memandu saya dalam proses pembuatan setiap komponen dan cara penyusunan kode yang rapih dan bekerja dengan baik. Disini saya menggunakan ai pertama untuk brainstorming ide bagaimana layout dan isi ide desain dari portofolio yang akan saya buat, setelah konsep dari desian dan isi sudah saya tentukan, maka selanjutnya saya meminta ai untuk menjelaskan kepada saya bertahap bagaimana mewujudkan setiap bagian dari konsep yang sudah saya tentukan sebelumnya, untuk komponen komponen yang ada pada web saya, saya tidak membuatnya dnegan ai tapi saya mengambilnya dari open source library atau dari web open source.

---
## Tugas 2

**1. Alur Request pada MVT Django**
Ketika pengguna membuka halaman `/projects/`, permintaan pertama kali diterima oleh `portofolio/urls.py` (proyek) yang kemudian meneruskannya ke `main/urls.py` (aplikasi). Di sana, URL dicocokkan dengan rute yang memanggil fungsi view `show_projects`. View ini lalu berkomunikasi dengan model `Project` untuk mengambil seluruh data proyek dari database (`Project.objects.all()`). Setelah mendapatkan data, view akan memasukkannya ke dalam sebuah variabel *context* dan meneruskannya ke template `projects.html`. Template kemudian memproses data dinamis tersebut (menggunakan perulangan `{% for %}`) menjadi halaman HTML statis utuh yang akhirnya dikirim kembali ke browser pengguna.

**2. Keuntungan Menyimpan Data di Model**
Menyimpan data di model (database) memisahkan logika tampilan dari logika data. Dampak positifnya sangat besar terhadap pemeliharaan aplikasi: jika saya ingin menambahkan proyek baru atau mengedit deskripsi, saya tidak perlu lagi membongkar dan mengedit file HTML (yang rawan merusak tata letak kode). Saya cukup memperbarui data di database dan template akan secara otomatis menampilkan versi terbarunya, membuat skalabilitas aplikasi jauh lebih baik.

**3. Perbedaan makemigrations dan migrate**
- `makemigrations` bertugas melacak setiap perubahan struktur yang kita lakukan pada class Model di Python dan merumuskannya menjadi sebuah file skema instruksi (file migrasi).
- `migrate` bertugas mengeksekusi instruksi dari file migrasi tersebut secara langsung ke dalam sistem database (menjalankan perintah SQL di balik layar).
Contoh: Jika saya menambahkan atribut baru `link = models.URLField()` di dalam model `Project`, saya harus menjalankan `makemigrations` agar Django tahu ada kolom baru yang ingin ditambahkan, lalu dilanjutkan dengan `migrate` agar kolom `link` tersebut benar-benar ditambahkan ke tabel pada file `db.sqlite3`.
