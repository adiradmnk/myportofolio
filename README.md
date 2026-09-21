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

---
## Tugas 3

### 1. Mengapa menggunakan ModelForm pada Django alih-alih membuat form HTML secara manual, serta alasan penambahan `{% csrf_token %}`
- **Alasan menggunakan ModelForm:**
  ModelForm merupakan fitur bawaan Django yang secara otomatis menghasilkan form berdasarkan skema model database yang sudah didefinisikan. Jika membuat form HTML manual, kita harus menulis setiap tag input secara berulang, mengurus sanitasi dan pemetaan data `request.POST` satu per satu ke objek model, serta mengimplementasikan validasi secara manual. Dengan ModelForm, validasi tipe data (seperti URL, teks, panjang karakter), pembuatan elemen input yang sesuai, hingga fungsi penyimpanan langsung (`form.save()`) ditangani secara otomatis, bersih, dan meminimalisir redundansi kode serta potensi bug.
- **Pentingnya `{% csrf_token %}`:**
  Tag `{% csrf_token %}` wajib ditambahkan pada setiap form dengan metode POST untuk melindungi aplikasi web dari serangan *Cross-Site Request Forgery* (CSRF). CSRF adalah serangan di mana situs jahat memanfaatkan sesi login atau kredensial pengguna yang tersimpan di browser untuk mengirimkan permintaan tidak sah (seperti mengubah atau menghapus data) ke server aplikasi kita tanpa disadari pengguna. Token CSRF bekerja sebagai kunci rahasia unik sekali pakai yang dibuat oleh server dan diverifikasi kecocokannya saat form dikirimkan kembali; jika token tidak cocok atau tidak ada, Django akan menolak permintaan tersebut.

### 2. Mengapa JSON lebih disukai dibandingkan XML dalam pengembangan aplikasi web modern
- **Ukuran lebih ringkas dan efisien:** JSON menggunakan sintaks key-value dengan kurung kurawal yang minimalis, sedangkan XML membutuhkan tag pembuka dan penutup (`<tag></tag>`) untuk setiap data sehingga ukuran payload XML jauh lebih besar dan boros bandwidth.
- **Parsing langsung dan integrasi alami:** Format data JSON diturunkan langsung dari objek JavaScript. Di sisi client (browser), JSON dapat di-parse secara instan menjadi objek native menggunakan fungsi bawaan `JSON.parse()` atau otomatis oleh library/API seperti `fetch().json()`. Sebaliknya, XML memerlukan *DOM parser* yang lebih berat dan kompleks untuk membaca hierarki tagnya.
- **Struktur data yang fleksibel:** JSON secara langsung merepresentasikan tipe data standar seperti string, number, boolean, array, dan null tanpa memerlukan skema definisi tipe yang rumit seperti XML Schema (XSD). Hal ini membuat JSON menjadi format standar *de facto* untuk arsitektur RESTful API modern.

### 3. Alur pengembalian data portofolio dalam bentuk JSON dan mengapa perlu serialization
- **Alur kerja view JSON:**
  1. Klien mengirim permintaan HTTP GET ke endpoint API (misal `/api/projects/` atau `/api/experience/`).
  2. URL resolver Django mengarahkan permintaan ke fungsi view terkait (misal `get_projects_json`).
  3. View melakukan query ke database melalui model ORM (misal `Project.objects.all()`), yang menghasilkan *QuerySet* berisi objek-objek model Python.
  4. Objek model tersebut diteruskan ke serializer bawaan Django (`serializers.serialize("json", ...)`).
  5. Serializer mengubah objek Python menjadi string terformat JSON.
  6. View mengembalikan data tersebut ke klien dalam bentuk `HttpResponse` dengan header `content_type="application/json"`.
- **Mengapa perlu proses serialization:**
  Objek model Django (*QuerySet* atau instance class Python) adalah objek internal yang tersimpan di memori runtime Python dan tidak dapat dikirim secara langsung melalui protokol HTTP. Protokol HTTP hanya dapat mengirimkan teks atau byte stream. Oleh karena itu, diperlukan proses **serialization**, yaitu konversi dari struktur data internal Python (objek model dengan relasi dan atributnya) menjadi format representasi teks standar (seperti JSON) yang dapat dipahami dan diproses oleh berbagai sistem, bahasa pemrograman, atau perangkat client di sisi frontend.

### AI Disclosure
Pada pengerjaan Tugas 3 ini, saya menggunakan AI sebagai asisten diskusi dan referensi teknis dalam memahami konsep implementasi `ModelForm`, mekanisme update data dengan parameter `instance`, serta alur serialisasi dan deserialisasi data menggunakan Django Serializer. Saya tetap membaca alur kode secara mandiri, menyesuaikan setiap field model dan form agar selaras dengan data portofolio saya sendiri, serta melakukan pengujian langsung di lingkungan lokal untuk memastikan fungsionalitas CRUD dan API berjalan dengan baik.
