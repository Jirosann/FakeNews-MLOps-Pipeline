# Gunakan base image yang ringan (Optimasi LO 5)
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    NLTK_DATA=/usr/local/share/nltk_data

# Set folder kerja di dalam container
WORKDIR /app

# Copy daftar dependensi
COPY requirements.txt .

# Install dependensi tanpa menyimpan cache (agar image kecil)
RUN pip install --no-cache-dir -r requirements.txt

# Download data NLTK (Stopwords) agar tidak error saat running
RUN python -m nltk.downloader -d /usr/local/share/nltk_data stopwords

# Copy aset aplikasi yang dibutuhkan saja (Modularitas)
COPY app.py .
COPY pipeline_fake_news.pkl .
COPY templates/ ./templates/
COPY static/ ./static/

# Jalankan aplikasi sebagai user biasa (bukan root) demi keamanan
RUN useradd --create-home --uid 10001 appuser
USER appuser

EXPOSE 5000

# Jalankan server menggunakan Gunicorn (Standar)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "30", "app:app"]
