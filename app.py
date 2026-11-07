from flask import Flask, request, render_template, jsonify
import pickle
import re
import string
import nltk
from nltk.corpus import stopwords

app = Flask(__name__)

# Batasi ukuran request (100 KB) agar server tidak bisa dibanjiri payload besar
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024
MAX_TEXT_LENGTH = 20000  # Batas jumlah karakter teks berita

# Load Pipeline (TF-IDF + Model)
model = None
try:
    with open('pipeline_fake_news.pkl', 'rb') as f:
        model = pickle.load(f)
except FileNotFoundError:
    app.logger.error("File pipeline_fake_news.pkl tidak ditemukan!")

# Pastikan stopwords tersedia (sudah di-download saat docker build)
try:
    stop_words = set(stopwords.words('english'))
except LookupError:
    nltk.download('stopwords', quiet=True)
    stop_words = set(stopwords.words('english'))


WORD_RE = re.compile(r'\w+')
DIGIT_RE = re.compile(r'\d')
PUNCT_RE = re.compile('[%s]' % re.escape(string.punctuation))


def remove_bracketed(text):
    """Menghapus teks dalam kurung kotak, misal "[VIDEO]".

    Hasilnya sama dengan re.sub(r'\\[.*?\\]', '', text), tetapi berjalan
    dalam waktu linear sehingga aman dari serangan ReDoS (input "[[[[...").
    """
    lines = []
    for line in text.split('\n'):
        parts, pos = [], 0
        while True:
            start = line.find('[', pos)
            if start == -1:
                break
            end = line.find(']', start + 1)
            if end == -1:
                break
            parts.append(line[pos:start])
            pos = end + 1
        parts.append(line[pos:])
        lines.append(''.join(parts))
    return '\n'.join(lines)


def remove_words_with_digits(text):
    """Menghapus kata yang mengandung angka, misal "covid19".

    Hasilnya sama dengan re.sub(r'\\w*\\d\\w*', '', text), tetapi tanpa
    backtracking sehingga aman dari serangan ReDoS (input "aaaa...").
    """
    return WORD_RE.sub(lambda m: '' if DIGIT_RE.search(m.group()) else m.group(), text)


def clean_text(text):
    text = text.lower()
    text = remove_bracketed(text)  # Menghapus teks dalam kurung kotak
    text = PUNCT_RE.sub('', text)  # Menghapus tanda baca
    text = remove_words_with_digits(text)  # Menghapus angka

    # Deteksi Stopwords
    text = " ".join([word for word in text.split() if word not in stop_words])

    return text


@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Referrer-Policy'] = 'no-referrer'
    return response


@app.errorhandler(413)
def payload_too_large(_error):
    return jsonify({'status': 'error', 'message': 'Ukuran data terlalu besar!'}), 413


@app.route('/')
def home():
    # Menampilkan UI
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'status': 'error', 'message': 'Model belum tersedia.'}), 503

    data = request.get_json(silent=True)
    input_data = data.get('text') if isinstance(data, dict) else None

    if not isinstance(input_data, str) or not input_data.strip():
        return jsonify({'status': 'error', 'message': 'Teks tidak boleh kosong!'}), 400
    if len(input_data) > MAX_TEXT_LENGTH:
        return jsonify({'status': 'error',
                        'message': f'Teks maksimal {MAX_TEXT_LENGTH} karakter!'}), 400

    try:
        cleaned_data = clean_text(input_data)
        prediction = model.predict([cleaned_data])[0]

        # Ambil probabilitas persentase
        probabilities = model.predict_proba([cleaned_data])[0]
        confidence_score = max(probabilities) * 100

        result = "Real News" if prediction == 1 else "Fake News"

        return jsonify({
            'status': 'success',
            'prediction': result,
            'confidence': f"{confidence_score:.2f}%",
            'text_length': len(input_data)
        })
    except Exception:
        # Detail error hanya dicatat di log server, tidak dikirim ke client
        app.logger.exception("Gagal melakukan prediksi")
        return jsonify({'status': 'error', 'message': 'Terjadi kesalahan internal.'}), 500
