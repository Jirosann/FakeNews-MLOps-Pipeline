# 🛡️ Fake News Detection System: End-to-End MLOps Pipeline

[![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/framework-Flask-lightgrey.svg)](https://flask.palletsprojects.com/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Proyek ini adalah sistem deteksi berita palsu (*Fake News*) yang dibangun dengan pendekatan **MLOps** (Machine Learning Operations). Sistem ini mencakup seluruh siklus  pengembangan, mulai dari riset data,preprocessing data, pelatihan model, hingga pengembangan Web Service yang dikontainerisasi menggunakan Docker.

---

## 🏗️ Software Architecture
Proyek ini mengadopsi arsitektur yang kohesif dengan pemisahan tanggung jawab (*Separation of Concerns*) yang jelas:

1.  **Research Layer (`/Jupyter`)**: Berisi eksperimen data, pra-pemrosesan NLP, dan pelatihan model.
2.  **Logic Layer (`app.py`)**: Web service berbasis Flask yang menangani permintaan inferensi secara real-time.
3.  **UI Layer (`/templates`)**: Antarmuka pengguna yang responsif menggunakan Tailwind CSS.
4.  **Infrastruktur Layer (`Dockerfile` & `docker-compose.yml`)**: Abstraksi lingkungan menggunakan Docker untuk memastikan skalabilitas dan portabilitas.

---

## 🔬 Modeling & Algorithm
Model dilatih menggunakan **ISOT Dataset** (internasional) dengan alur kerja sebagai berikut:

### 1. Preprocessing (NLP)
Teks dibersihkan melalui fungsi `clean_text` yang mencakup:
* **Case Folding**: Mengubah teks ke lowercase.
* **Noise Removal**: Menghapus angka, tanda baca, dan teks dalam kurung.
* **Stopwords Removal**: Menggunakan `nltk.corpus.stopwords` bahasa Inggris untuk membuang kata-kata umum yang tidak bermakna.

### 2. Feature Extraction
Menggunakan **TF-IDF Vectorizer** untuk mengubah teks menjadi representasi vektor numerik. Algoritma ini memberikan bobot tinggi pada kata-kata unik yang menjadi ciri khas berita palsu vs asli.

### 3. Classification Model
Menggunakan **Logistic Regression** dengan fungsi aktivasi Sigmoid:
$$P(y=1|x) = \frac{1}{1 + e^{-z}}$$
Model ini menghasilkan akurasi sebesar **98.58%** pada data pengujian.

---

## 🐳 Web Service Deployment
Aplikasi ini sepenuhnya dikontainerisasi menggunakan **Docker** untuk menjamin lingkungan yang *reproducible* dan *optimized*.

### Kenapa Docker?
* **Isolasi Environment**: Mengunci versi Python (3.11-slim) dan library agar identik di semua komputer.
* **Production Ready**: Menggunakan **Gunicorn** sebagai WSGI HTTP Server untuk stabilitas tinggi.
* **Automated Setup**: Docker secara otomatis mengunduh dependensi NLTK saat proses *build*.

## 🚀 Cara Penggunaan (Installation & Running)

```bash
git clone https://github.com/Jirosann/FakeNews-MLOps-Pipeline.git
cd FakeNews-MLOps-Pipeline
```

1.  Jalankan perintah berikut di terminal:
    ```bash
    docker compose up --build
    ```
    
2.  Tunggu hingga proses *build* selesai. Aplikasi akan tersedia dan dapat diakses melalui browser pada:
    **[http://localhost:5000](http://localhost:5000)**

---

## 📊 Academic Fulfillment (Kriteria Evaluasi)

Proyek ini disusun dengan memenuhi standar industri dan akademik untuk mata kuliah Machine_Learning terkait:

1.  **Detail & Terstruktur (LO 4):** Dokumentasi ini secara gamblang menjelaskan landasan teori algoritma (Sigmoid, TF-IDF) serta implementasi praktisnya (NLTK, Pickle).
2.  **Struktur Deployment Jelas (LO 3 & LO 5):** Mendemonstrasikan pemahaman mendalam mengenai struktur *deployment*, pemisahan layer arsitektur (*software architecture*), dan alur kontainerisasi.
3.  **Reproducible (LO 5):** Menyediakan instruksi eksekusi *"Single Command"* (`docker compose up`) yang menjamin aplikasi dapat dijalankan oleh evaluator/dosen di lingkungan mana pun tanpa *dependency error*.
4.  **Profesionalitas:** Menerapkan *badges*, penggunaan sintaks LaTeX untuk perumusan model, serta pemisahan logika aplikasi dengan antarmuka.

---

## 🛠️ Tech Stack
* **Language**: Python 3.11
* **ML Libraries**: Scikit-Learn, Pandas, NLTK
* **Web Framework**: Flask
* **Server**: Gunicorn
* **Frontend**: HTML5 & Tailwind CSS
* **DevOps**: Docker & Docker Compose

---
### Struktur Folder
```text
FakeNews-MLOps-Pipeline/
├── Jupyter/                    # Area Riset (Eksperimen)
│   └── AOL_ML_FakeNews_Research.ipynb
├── templates/                  # Frontend UI
│   └── index.html
├── static/                     # JavaScript Frontend
│   └── index.js
├── app.py                      # Flask API & Logic
├── Dockerfile                  # Blueprint Container
├── docker-compose.yml          # Orkestrasi Service
├── pipeline_fake_news.pkl      # Saved Model (Pickle)
├── requirements.txt            # Daftar Dependensi
└── README.md                   # Dokumentasi Teknis
```

> **Catatan:** Dataset `Fake.csv` dan `True.csv` (ISOT Dataset) tidak disertakan di repository karena ukurannya besar. Unduh dataset tersebut dan letakkan di folder `Jupyter/` jika ingin menjalankan ulang notebook riset.

## 🔒 Keamanan
* Container berjalan sebagai user non-root dengan filesystem read-only.
* Port hanya dibuka untuk `localhost` (`127.0.0.1:5000`).
* Ukuran request dan panjang teks dibatasi, dan detail error internal tidak dikirim ke client.
* File rahasia (`.env`, key, kredensial) dikecualikan lewat `.gitignore` dan `.dockerignore`.
