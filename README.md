# Personal Portfolio - CSGE602022

Repositori ini merupakan karya pribadi untuk keperluan tugas mata kuliah wajib yaitu pemrograman berbasis platform (PBP) di Universitas Indonesia, portofolio ini secara berkala dalam satu semester akan terus di update 

## Informasi Mahasiswa
- **Nama** : Adriana Ainurrahmah Damanik
- **NPM** : 2506656375
- **Kelas** : PBP E

## Cara Menjalankan Proyek Secara Lokal
1. Pastikan Anda memiliki Python (versi 3.10+) yang sudah ter-install, karena Django REST Framework 3.18 membutuhkan minimal Python 3.10.
2. Buat dan aktifkan *virtual environment*:
   ```bash
   python -m venv env
   source env/bin/activate  # Untuk Mac / Linux
   # env\Scripts\activate   # ini command jika anda menggunakan windows
   ```
3. Install semua *dependencies* (termasuk `djangorestframework` sejak Tutorial 7):
   ```bash
   pip install -r requirements.txt
   ```
4. Jalankan migrasi database:
   ```bash
   python manage.py migrate
   ```
5. (Opsional) Buat akun pemilik portofolio, lalu buat grup `Editor` lewat `/admin/` jika ingin mencoba peran Editor:
   ```bash
   python manage.py createsuperuser
   ```
6. Jalankan server pengembangan lokal:
   ```bash
   python manage.py runserver
   ```
7. Buka `http://localhost:8000/` di browser Anda. Browsable API bisa dibuka di `http://localhost:8000/api/v1/experience/` dan `http://localhost:8000/api/v1/projects/`.
8. Jalankan seluruh test:
   ```bash
   python manage.py test main
   ```

jika anda hanya inign melihat hasil protofolio atau hasil compile dari kode yang sudah say abuat anda bisa membuka di [https://adriana-ainurrahmah-myportofolio.pws.cs.ui.ac.id/](https://adriana-ainurrahmah-myportofolio.pws.cs.ui.ac.id/)

## Progres Mingguan
| Minggu | Topik | Yang dikerjakan |
|:---|:---|:---|
| Tugas 1 | HTML & CSS | Halaman profil statis, skills, dan deploy ke PWS |
| Tugas 2 | MVT Django | Model `Experience`, halaman Experience, dan unit test |
| Tugas 3 | Form & Data Delivery | Form tambah/edit/hapus dengan `ModelForm` serta endpoint JSON dan XML |
| Tugas 4 | Autentikasi & Otorisasi | Login, register, cookie `last_login`, peran Editor, dan fitur star |
| Tugas 5 | JavaScript & AJAX | Halaman Experience berbasis Fetch API, pencarian debounce, modal, toast, dan proteksi XSS |
| Tugas 6 | Django REST Framework | API `/api/v1/experience/` dengan serializer, permission empat peran, edit lewat `PATCH`, dan test API |

---
## Tugas 1

**1. Penggunaan elemen semantik HTML5**
Ya, saya menggunakan elemen semantik HTML5 seperti `<section>` untuk membagi bagian 'Profile', 'About Me', dan 'Skills' di `index.html`, serta `<article>` untuk kartu About Me yang berisi nama, NPM, dan program studi. Kartu proyek dan pengalaman di halaman Projects dan Experience juga dirender sebagai `<article>`. Penggunaan elemen ini sangat membantu dalam menyusun static web karena memberikan struktur logika yang jelas tanpa harus bergantung pada banyak tag `<div>` yang membingungkan.

> **Catatan revisi (feedback Tugas 1):** sebelumnya README menyebut `<article>` padahal `index.html` belum memakainya, dan NPM belum tampil di halaman. Keduanya sudah diperbaiki dengan menambahkan bagian About Me berbentuk `<article>` yang menampilkan NPM.

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

### AI Disclosure
Dalam pengerjaan Tugas 2 ini, saya memanfaatkan AI sebagai teman diskusi untuk memahami alur dasar arsitektur MVT di Django:
- **Cara saya menggunakan AI:** Saya berdiskusi dengan AI untuk memahami bagaimana pemetaan routing URL bekerja dari level proyek (`portofolio/urls.py`) ke level aplikasi (`main/urls.py`), serta bagaimana cara meneruskan *QuerySet* dari fungsi view ke dalam template context menggunakan dictionary agar bisa di-looping menggunakan `{% for %}`.
- **Koreksi dan penyesuaian mandiri:** Contoh kode awal dari AI sering kali menggunakan nama model dan field yang generik atau field bawaan tutorial. Saya secara mandiri merancang dan menyesuaikan field pada model portofolio saya sendiri (seperti atribut `role` dan `link` pada `Project`). Selain itu, saya mengatur penulisan sintaks URL patterns secara manual agar sesuai konvensi namespace Django (`app_name = "main"`), serta memastikan konfigurasi `settings.py` (terutama `TEMPLATES` dan `INSTALLED_APPS`) terpasang dengan benar.


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

### AI Disclosure & Analisis Kritis
- **Alat yang digunakan:** Dalam pengerjaan Tugas 3, saya menggunakan AI (LLM) sebagai mitra diskusi konseptual untuk memahami alur kerja `ModelForm` Django, mekanisme pre-populate form untuk edit data menggunakan parameter `instance`, serta proses serialisasi dan deserialisasi JSON pada Django.
- **Strategi Prompting:** Saya menggunakan strategi prompting berbasis masalah spesifik, seperti: *"Bagaimana memisahkan alur update dan create di Django view dengan ModelForm yang sama?"* dan *"Bagaimana format serializers.deserialize menghasilkan objek Python yang bisa dikirim ke context template?"*.
- **Keterbatasan AI & Perbaikan Manual Mandiri:**
  1. **Kode Generik vs Model Nyata:** Kode yang disarankan AI sering kali menggunakan field dummy generik atau contoh Burhan dari modul. Saya secara manual mengoreksi dan mengaitkan field form dengan model portofolio saya sendiri (`title`, `role`, `description`, `link` pada `Project` serta `title`, `category`, `description`, `thumbnail`, `ended_at` pada `Experience`).
  2. **Styling & Desain:** AI cenderung menghasilkan elemen visual yang kaku (*AI slop* seperti badge status bertumpuk dan kontras warna yang kurang pas di atas background gambar ocean). Saya melakukan perbaikan manual pada CSS dengan menambahkan dark overlay gradient agar keterbacaan tipografi tetap kontras dan mempertahankan estetika personal portofolio.
  3. **Penyesuaian Test Suite:** Saya menulis dan menyesuaikan unit test mandiri di `main/tests.py` hingga seluruh 18 test kasus berhasil dilewati (100% OK) untuk memastikan tidak ada regresi pada endpoint maupun view.

---
## Tugas 4

Di tugas 4 ini, saya melanjutkan proyek portofolio dengan menerapkan sistem autentikasi, session, cookie `last_login`, dan pembagian peran (hak akses) pengguna. Di sini saya juga menambahkan satu peran baru yaitu **Editor** dengan memanfaatkan fitur `Group` bawaan dari Django.

### 1. Hak Akses Tiap Peran Pengguna
Agar data portofolio tetap aman dan tidak sembarangan diubah oleh orang lain, saya membatasi hak akses pengguna baik dari sisi server (view) maupun dari antarmuka template:

| Peran Pengguna | Melihat Portofolio | Kasih / Batal Star | Edit Data | Tambah / Hapus Data |
|:---|:---:|:---:|:---:|:---:|
| **Pengunjung (Belum Login)** | Bisa | Nggak bisa (diarahkan ke login) | Nggak bisa (diarahkan ke login) | Nggak bisa (diarahkan ke login) |
| **Pengguna Biasa** | Bisa | Bisa | Nggak bisa (403 Forbidden) | Nggak bisa (403 Forbidden) |
| **Editor (Grup 'Editor')** | Bisa | Bisa | Bisa | Nggak bisa (403 Forbidden) |
| **Pemilik Portofolio (Superuser)** | Bisa | Bisa | Bisa | Bisa |

### 2. Penerapan Peran Editor dan Fitur Star
- **Grup Editor:** Saya membuat grup baru bernama `Editor` lewat Django Admin. Di bagian view, saya membuat fungsi pembantu `is_editor_or_admin(user)` untuk mengecek apakah user yang sedang login adalah superuser atau tergabung dalam grup `Editor`. Kalau pengguna masuk ke grup ini, mereka bisa membuka halaman edit dan mengubah data proyek atau pengalaman, tapi kalau mereka coba-coba menambah atau menghapus data, server bakal langsung memunculkan error `403 Forbidden`.
- **Fitur Star:** Saya menambahkan field `starred_by = models.ManyToManyField(User, ...)` pada model `Project` dan `Experience`. Pengguna yang sudah login bisa menekan tombol star untuk memberi apresiasi atau membatalkannya (toggle). Setiap user hanya bisa memberi satu star per proyek atau pengalaman.
- **Keamanan Data JSON:** Pada endpoint `/api/projects/` dan `/api/experience/`, saya menambahkan opsi `use_natural_foreign_keys=True` pada serializer Django supaya data yang tampil adalah username pemberi star, bukan id angka dari database yang bersifat privat.

### AI Disclosure
Dalam pengerjaan tugas 4 ini, saya menggunakan AI sebagai teman diskusi dan mencari referensi ketika mengalami kendala:
- **Cara saya menggunakan AI:** Saya bertanya ke AI bagaimana cara mengecek keanggotaan grup Django pada fungsi view (`request.user.groups.filter(...)`) dan bagaimana membuat tampilan halaman login serta register menjadi pas satu layar tanpa scrollbar.
- **Koreksi dan penyesuaian mandiri:** AI sempat menyarankan untuk hanya menyembunyikan tombol edit dan delete di template saja. Tapi saya tahu kalau cuma disembunyikan di HTML, orang lain masih bisa mengakses linknya langsung lewat URL. Jadi saya secara manual menambahkan proteksi server-side dengan `raise PermissionDenied` di setiap fungsi view (create, edit, delete). Selain itu, saya juga menyesuaikan padding CSS sendiri agar tampilannya tetap enak dilihat di laptop maupun HP, serta menulis unit test tambahan di `tests.py` sampai semuanya berhasil lolos.

---
## Tugas 5

### 1. Pengertian Debouncing dan Pentingnya pada Fitur Pencarian AJAX
**Debouncing** adalah teknik pemrograman untuk membatasi frekuensi pemanggilan suatu fungsi dengan cara menunda eksekusinya sampai tidak ada lagi event baru yang dipicu selama rentang waktu tertentu (misalnya jeda 300 milidetik). Jika sebelum waktu tunggu tersebut habis pengguna memicu event kembali (misalnya menekan tombol huruf berikutnya), maka timer yang sedang berjalan akan dibatalkan (`clearTimeout`) dan timer baru akan dimulai kembali dari nol.

Teknik ini sangat penting diterapkan pada fitur pencarian berbasis AJAX karena beberapa alasan utama:
- **Mencegah Beban Berlebih pada Server dan Pemborosan Bandwidth:** Ketika pengguna mengetik kata kunci pada kolom pencarian (event `input`), pencarian tanpa debouncing akan mengirimkan permintaan HTTP ke server untuk setiap penekanan tombol. Sebagai contoh, mengetik kata "Software" akan memicu 8 kali *request* berturut-turut. Dengan debouncing, browser hanya akan mengirimkan satu permintaan ke server setelah pengguna benar-benar berhenti mengetik sejenak.
- **Menghindari Masalah Race Condition:** Karena pemanggilan AJAX bersifat asinkron, waktu tiba respons dari server tidak dapat dijamin berurutan. Tanpa debouncing, respons dari permintaan pertama (misalnya untuk huruf "S") bisa saja tiba lebih lambat dibandingkan respons dari permintaan kata lengkap ("Software"). Hal ini berpotensi menimpa data terbaru dengan data lama yang sudah tidak relevan (*stale data*). Debouncing bersama dengan pembatalan request lama lewat `AbortController` menjamin antarmuka web selalu menampilkan data yang akurat sesuai kata kunci terakhir pengguna.

### 2. Fungsi Penggunaan `await` saat Menggunakan `fetch()` dan Akibat jika Tidak Digunakan
Fungsi `fetch()` adalah fungsi bawaan browser (Web API) yang bersifat asinkron dan selalu mengembalikan sebuah objek `Promise` yang merepresentasikan proses permintaan jaringan yang sedang berlangsung. Keyword `await` hanya dapat digunakan di dalam `async function` dan berfungsi untuk menunda (*pause*) eksekusi baris kode berikutnya hingga `Promise` dari `fetch()` selesai diproses (*resolved*) serta menghasilkan objek `Response` yang sebenarnya. Dengan menggunakan `await`, kode asinkron dapat ditulis dengan struktur yang bersih, berurutan, dan mudah dibaca tanpa harus membuat rantai callback bertingkat (`.then()`).

**Apa yang terjadi jika kita tidak menggunakan `await`:**
Jika kita memanggil `const response = fetch(url)` tanpa keyword `await`, variabel `response` tidak akan berisi objek hasil dari server, melainkan hanya akan menampung objek `Promise <pending>`. Jika baris kode selanjutnya mencoba mengakses properti dari objek tersebut (seperti mengecek `response.ok` atau menjalankan `response.json()`), operasi tersebut akan gagal atau mengembalikan error/Promise lain yang belum selesai. Akibatnya, alur eksekusi akan terus berjalan sebelum data dari server berhasil diunduh, menyebabkan data yang ingin diproses bernilai `undefined`, antarmuka gagal merender kartu data, atau bahkan aplikasi mengalami error (*crash*) di sisi browser pengguna.

### 3. Serangan XSS (Cross-Site Scripting) dan Mengapa Data via AJAX/JavaScript Lebih Rentan daripada Template Django
**Cross-Site Scripting (XSS)** adalah jenis serangan keamanan siber di mana penyerang berhasil menyisipkan kode skrip berbahaya (umumnya JavaScript) ke dalam aplikasi web yang kemudian dieksekusi oleh browser pengguna lain yang mengunjungi halaman tersebut. Pada jenis *Stored XSS*, kode berbahaya tersebut disimpan ke dalam database (misalnya diselipkan pada nama proyek atau deskripsi pengalaman) sehingga akan selalu dieksekusi setiap kali data tersebut diambil dan ditampilkan ke antarmuka pengguna. Jika berhasil, penyerang dapat mencuri cookie sensitif pengguna (seperti session id atau token CSRF), menjalankan perintah tidak sah atas nama pengguna, maupun merusak tampilan website.

**Mengapa data yang ditampilkan melalui AJAX/JavaScript lebih rentan:**
- **Auto-Escaping pada Template Django:** Saat kita merender data langsung menggunakan template engine Django (misalnya dengan sintaks `{{ experience.title }}`), Django secara otomatis menerapkan mekanisme *auto-escaping*. Karakter-karakter khusus HTML seperti `<`, `>`, `&`, `"`, dan `'` akan diubah secara otomatis menjadi karakter entitas aman (`&lt;`, `&gt;`, `&quot;`, dll.). Dengan begitu, teks seperti `<script>alert(1)</script>` akan ditampilkan murni sebagai teks biasa oleh browser, bukan dieksekusi sebagai tag elemen HTML.
- **Ketiadaan Proteksi Otomatis saat Beralih ke AJAX:** Ketika data diambil lewat AJAX dalam format JSON lalu dirakit ke antarmuka menggunakan JavaScript (misalnya lewat properti `innerHTML` atau template literal), peran template engine Django berakhir di pembuatan JSON. Browser tidak memiliki fitur auto-escaping bawaan saat menyisipkan string ke dalam `innerHTML`. Jika nilai teks dari JSON langsung digabungkan ke elemen HTML tanpa disanitasi, browser akan menganggap tag berbahaya tersebut sebagai elemen HTML/JS sungguhan dan langsung menjalankannya. Oleh sebab itu, rendering via JavaScript menuntut penanganan keamanan manual yang ketat, baik melalui fungsi sanitasi sisi klien seperti `escapeHtml()` sebelum data disuntikkan ke DOM, maupun pembersihan tag berbahaya di sisi server menggunakan `strip_tags()` pada method `clean_<field>` di Django `ModelForm`.

### AI Disclosure & Analisis Kritis
- **Alat yang Digunakan:** Saya menggunakan bantuan AI (LLM) sebagai mitra diskusi konseptual untuk mendalami mekanisme `AbortController` pada Fetch API, integrasi header `X-CSRFToken` pada pengiriman data multipart form via AJAX, serta pemanfaatan Popover API untuk modal interaktif tanpa dependensi pustaka luar.
- **Strategi Prompting:** Saya menerapkan prompting berbasis skenario konkret, seperti: *"Bagaimana cara menghentikan fetch request sebelumnya yang belum selesai saat pengguna masih mengetik pencarian?"* dan *"Bagaimana format response JsonResponse manual di Django agar menyertakan relasi ManyToMany untuk informasi star?"*.
- **Analisis Kritis Keterbatasan AI & Perbaikan Mandiri Mahasiswa:**
  1. **Celah XSS pada Boilerplate AI:** Kode contoh yang sering diberikan oleh AI langsung menyematkan variabel JSON ke dalam `innerHTML` tanpa proses escaping. Menyadari risiko celah XSS ini, saya secara manual membuat fungsi `escapeHtml()` di JavaScript untuk menyaring kelima karakter sensitif HTML pada seluruh teks yang dirender, serta menambahkan validasi `strip_tags()` dan penolakan input kosong di method `clean_title()` pada `ExperienceForm`.
  2. **Pengabaian Otorisasi Server-Side:** AI sering kali hanya menyarankan untuk menyembunyikan modal tambah data di template HTML bagi non-admin. Saya memahami bahwa hal tersebut tidak aman karena endpoint POST tetap bisa ditembak langsung via HTTP request. Oleh karena itu, saya mengimplementasikan pengecekan hak akses tegas di sisi server pada fungsi view `create_experience_ajax` dengan mengembalikan status `403 Forbidden` jika pengguna bukan superuser.
  3. **Inovasi Fitur Ekstra (Rubrik 4):** Di luar materi dasar tutorial, saya berinisiatif merancang dan menambahkan fitur filter kategori interaktif (*category filter pills*) pada halaman Experience sehingga pengguna dapat memfilter pengalaman (Internship, Research, Full-Time, Freelance, dll.) secara instan tanpa memuat ulang halaman.
  4. **Verifikasi Test Suite Mandiri:** Saya memperluas cakupan unit test di `main/tests.py` hingga mencapai 32 pengujian menyeluruh (mencakup pengujian respons JSON, otorisasi peran, validasi error 400, dan pembersihan XSS) dengan status kelulusan 100% OK.




---
## Tugas 6

Di tugas 6 ini, saya menerapkan pola Django REST Framework dari Tutorial 7 ke bagian **Experience** yang saya kerjakan sejak Tugas 2 sampai Tugas 5. Halaman Experience sekarang sepenuhnya memakai API `/api/v1/experience/` untuk menampilkan, mencari, memfilter, menambah, mengubah, memberi star, dan menghapus data tanpa reload.

### Ringkasan Implementasi
- **Serializer (`main/serializers.py`):** `ExperienceSerializer` dengan daftar `fields` eksplisit. Field hasil perhitungan (`category_display`, `is_ongoing`, `star_count`, `is_starred`, `starred_by_names`) bersifat read-only, jadi klien tidak bisa memalsukan jumlah star. Input `title` dan `description` dibersihkan dengan `strip_tags` di `validate_title` dan `validate_description`, lalu ditolak kalau hasilnya kosong. Data akun seperti email dan password tidak pernah ikut dikirim, hanya username pemberi star.
- **Permission (`main/permissions.py`):** `IsPortfolioOwnerOrEditorOrReadOnly` dipasang di endpoint daftar dan detail, sedangkan endpoint star memakai `IsAuthenticated` dan selalu memakai `request.user`.
- **API View (`main/api_views.py`):** `experience_list`, `experience_detail`, dan `experience_star` berbasis fungsi dengan `@api_view` dan `SessionAuthentication`. Pencarian dari Tugas 5 dipindah ke parameter `?title=`, ditambah filter `?category=`.
- **Halaman (`templates/experience.html`):** semua operasi tulis lewat satu fungsi `writeExperience()` yang mengirim JSON dan header `X-CSRFToken`. Error `400` dan `403` dari API ditampilkan di toast lengkap dengan nama field-nya. Setiap teks tetap di-escape dengan `escapeHtml()`.
- **Fitur tambahan:** modal yang sama dipakai untuk tambah dan edit (`PATCH`) sehingga Editor bisa mengubah data langsung dari halaman; star, edit, dan hapus memperbarui kartu yang bersangkutan saja tanpa memuat ulang seluruh daftar; jumlah hasil pencarian ditampilkan; tombol "Coba Lagi" saat data gagal dimuat; dan input tanggal selesai memakai date picker.

### Endpoint API Experience
| Method | Endpoint | Tindakan | Siapa yang boleh |
|:---|:---|:---|:---|
| GET | `/api/v1/experience/?title=...&category=...` | Daftar, pencarian, dan filter | Semua pengunjung |
| POST | `/api/v1/experience/` | Tambah pengalaman | Pemilik |
| GET | `/api/v1/experience/<uuid>/` | Detail | Semua pengunjung |
| PUT / PATCH | `/api/v1/experience/<uuid>/` | Ubah pengalaman | Editor dan pemilik |
| DELETE | `/api/v1/experience/<uuid>/` | Hapus pengalaman | Pemilik |
| POST | `/api/v1/experience/<uuid>/star/` | Beri / batalkan star | Pengguna login |

View HTML lama (`edit_experience`, `delete_experience`, dan `create_experience`) sudah konsisten dengan aturan ini: Editor hanya bisa mengedit, sedangkan tambah dan hapus hanya untuk superuser.

### Pengujian
Test API ada di `main/tests_api.py` (kelas `ExperienceAPITest`) dan mencakup keempat peran: pengunjung dan pengguna biasa ditolak saat menulis, Editor boleh `PUT`/`PATCH` tapi ditolak saat `POST`/`DELETE`, dan pemilik bisa membuat, mengubah, serta menghapus data. Test penolakan juga memeriksa isi database, bukan hanya status HTTP. Selain itu ada test validasi (judul kosong, payload `<img onerror>`, kategori tidak valid, URL `javascript:`, tanggal salah), star (termasuk penolakan pengunjung dan `GET` yang menghasilkan 405), field read-only, dan CSRF dengan `APIClient(enforce_csrf_checks=True)` serta `.login()`.

```bash
python manage.py test main
```

### Tugas 6

1. **REST, mengapa JSON saja belum cukup, serta perbedaan PUT dan PATCH**

   **REST (Representational State Transfer)** adalah gaya arsitektur untuk merancang web API, bukan library atau format data. Dalam REST, data diperlakukan sebagai *resource* yang punya alamat sendiri (misalnya `/api/v1/experience/` untuk kumpulan pengalaman dan `/api/v1/experience/<uuid>/` untuk satu pengalaman), tindakan dinyatakan lewat HTTP method (`GET` membaca, `POST` membuat, `PUT`/`PATCH` mengubah, `DELETE` menghapus), klien dan server bertukar *representasi* data, dan setiap request membawa informasi yang dibutuhkan server.

   Mengembalikan JSON saja belum cukup untuk disebut RESTful karena JSON hanya format datanya. Endpoint lama saya di Tugas 5, misalnya `POST /experience/add-ajax/`, memang membalas JSON, tapi tindakannya ditulis di URL (`add-ajax`), hapus dilakukan lewat `POST /experience/<id>/delete/`, dan kode status tidak selalu mengikuti konvensi. API seperti itu lebih mirip kumpulan fungsi jarak jauh. API baru saya memakai satu URL per resource dan membiarkan HTTP method serta status code (`200`, `201`, `204`, `400`, `403`, `404`, `405`) yang menjelaskan apa yang terjadi.

   **PUT vs PATCH:**
   - `PUT` mengirim representasi pengganti yang lengkap. Semua field wajib harus dikirim, kalau tidak hasilnya `400`. Cocok dipakai ketika klien memang memegang seluruh data, misalnya form edit yang mengirim ulang judul, kategori, deskripsi, thumbnail, dan tanggal sekaligus.
   - `PATCH` hanya mengirim field yang ingin diubah (`partial=True` di serializer), field lain tetap. Cocok untuk perubahan kecil, misalnya menandai pengalaman sudah selesai dengan mengirim `{"ended_at": "2026-01-31"}` saja. Modal edit di halaman Experience saya memakai `PATCH`.

2. **Peran serializer dan keuntungannya dibandingkan JsonResponse manual**

   Serializer di DRF bekerja dua arah. Saat **serialization** (misalnya `GET`), serializer mengubah objek model menjadi tipe data Python yang siap dirender jadi JSON. Saat **deserialization** (`POST`/`PUT`/`PATCH`), serializer memvalidasi `request.data` lalu menghasilkan `validated_data` yang siap disimpan lewat `.save()`.

   Keuntungannya dibandingkan merakit dictionary sendiri dengan `JsonResponse` seperti di Tugas 5:
   - **Satu kontrak data untuk baca dan tulis.** Di Tugas 5 saya merakit dictionary dalam perulangan untuk output, lalu memakai `ExperienceForm` dan `form.errors.get_json_data()` untuk input. Sekarang daftar field, validasi, dan bentuk output ada di satu kelas.
   - **Validasi otomatis dari model.** `ModelSerializer` membaca model sehingga `category` otomatis dicek terhadap pilihan yang ada, `thumbnail` dicek sebagai URL, dan field wajib langsung ditolak. Aturan tambahan cukup ditulis di `validate_<field>`.
   - **Field read-only dan hasil perhitungan lebih aman.** `SerializerMethodField` dan `read_only_fields` membuat `star_count` atau `id` tidak bisa diisi klien, tanpa perlu `if` manual.
   - **Error dan status konsisten.** `is_valid(raise_exception=True)` otomatis membalas `400` dengan error per field, dan `Response` mengurus format serta Browsable API.
   - **Lebih sedikit kode berulang.** Pola yang sama bisa dipakai lagi untuk Projects dan Experience tanpa menulis ulang perulangan dictionary.

3. **Autentikasi vs otorisasi di DRF dan mengapa permission harus dicek di server**

   **Autentikasi** menjawab "siapa kamu?". Di DRF, *authentication class* seperti `SessionAuthentication` membaca cookie session dan mengisi `request.user`. Kalau tidak ada session, pengguna tetap diperlakukan sebagai anonim. **Otorisasi** menjawab "apa yang boleh kamu lakukan?". Di DRF ini diputuskan oleh *permission class*, misalnya `IsPortfolioOwnerOrEditorOrReadOnly` yang mengizinkan semua orang membaca, Editor melakukan `PUT`/`PATCH`, dan hanya superuser yang boleh `POST`/`DELETE`. Permission dicek sebelum isi view dijalankan, jadi request yang ditolak tidak pernah menyentuh database.

   Menyembunyikan tombol di template hanya mengatur tampilan, bukan keamanan. Siapa pun tetap bisa mengirim request langsung ke `/api/v1/experience/<uuid>/` lewat Console browser, `curl`, atau Postman tanpa pernah melihat tombolnya. Kalau server tidak memeriksa izin, request itu akan diproses. Karena itu aturan akses harus ada di server, dan tombol yang disembunyikan hanya untuk kenyamanan pengguna. Saya membuktikan ini di test `test_editor_cannot_create_or_delete`, yang mengirim `POST` dan `DELETE` langsung sebagai Editor lalu memastikan database tidak berubah.

4. **Mengapa CSRF tetap diperlukan dengan SessionAuthentication dan mengapa force_authenticate tidak cukup**

   `SessionAuthentication` mengenali pengguna dari cookie session, dan browser selalu mengirim cookie itu secara otomatis ke domain kita, termasuk ketika request dipicu oleh situs lain. Tanpa token CSRF, situs jahat bisa membuat halaman yang diam-diam mengirim `POST` atau `DELETE` ke API saya memakai session korban yang sedang login, misalnya menghapus pengalaman kalau korbannya superuser. Token CSRF mencegah ini karena nilainya harus dibaca dari cookie `csrftoken` milik origin kita lalu dikirim ulang lewat header `X-CSRFToken`, dan situs lain tidak bisa membaca cookie tersebut. Karena itu DRF memeriksa CSRF untuk setiap request yang mengubah data dari pengguna yang terautentikasi lewat session.

   `force_authenticate` langsung menempelkan user ke request dan melewati proses autentikasi session sepenuhnya, termasuk pemeriksaan CSRF. Test seperti itu berguna untuk menguji permission, tapi akan tetap lulus walaupun perlindungan CSRF rusak atau dimatikan. Untuk membuktikan CSRF benar-benar berjalan, saya memakai `APIClient(enforce_csrf_checks=True)` dan `.login()` yang membuat session sungguhan. Test `test_session_write_without_csrf_is_rejected` dan `test_star_without_csrf_is_rejected` memastikan request tanpa token ditolak `403` dan database tidak berubah, sedangkan `test_session_write_with_csrf_from_page_succeeds` mengambil token dari halaman Experience lalu membuktikan `PATCH` dengan header `X-CSRFToken` berhasil.

#### AI Disclosure & Analisis Kritis
- **Alat yang digunakan:** Claude (lewat Claude Code) sebagai asisten pemrograman untuk Tutorial 7 dan Tugas 6.
- **Bagian yang dibantu AI:** penyesuaian `ProjectSerializer`, API view, dan test Tutorial 7 ke field model saya; pembuatan `ExperienceSerializer`, API view, dan URL Experience; penulisan ulang script halaman Experience (modal tambah/edit, star, hapus, toast error); test `ExperienceAPITest`; serta draf jawaban README ini.
- **Strategi prompting:** saya memberikan teks tutorial dan soal tugas secara utuh, lalu meminta AI menganalisis repositori saya dulu dan membuat rencana sebelum menulis kode. Saya juga meminta perubahan dipecah menjadi beberapa commit dengan format conventional commits di branch fitur terpisah.
- **Keterbatasan AI dan hal yang diperiksa:**
  1. **Contoh tutorial tidak cocok dengan model saya.** Tutorial memakai field `tech_stack`, `project_url`, dan `project_image_url`, sedangkan model `Project` saya memakai `role` dan `link`. Kode tutorial tidak bisa langsung disalin, sehingga serializer, script, dan test harus disesuaikan tanpa mengubah model.
  2. **Format tanggal.** Input tanggal kosong dari form dikirim sebagai string kosong dan ditolak DRF dengan `400`. Masalah ini ditemukan saat mencoba API secara langsung, lalu diperbaiki dengan mengirim `null` untuk tanggal kosong.
  3. **Versi dependency.** DRF 3.18 membutuhkan Django 5.2 dan Python 3.10, sedangkan `requirements.txt` masih menulis `django~=5.0`, jadi versinya disamakan ke `django~=5.2`.
  4. **Memastikan test benar-benar menguji izin.** Permission sempat diubah sementara agar Editor boleh membuat dan menghapus data, dan test Editor gagal seperti yang diharapkan. Setelah itu permission dikembalikan seperti semula.
  5. **Uji manual di browser.** Halaman Experience dan Projects dicoba untuk keempat peran (pengunjung, pengguna biasa, Editor, dan pemilik), termasuk input XSS dan request `POST` dari Editor yang harus ditolak `403`.
