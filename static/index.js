async function checkNews() {
    const text = document.getElementById('newsInput').value;
    const resultBox = document.getElementById('resultBox');
    const predictionResult = document.getElementById('predictionResult');

    if (!text.trim()) {
        alert("Masukkan teks beritanya!");
        return;
    }

    try {
        // Kirim data ke Flask API /predict
        const response = await fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: text })
        });

        const data = await response.json();

        if (data.status === 'success') {
            resultBox.classList.remove('hidden');

            // innerText (bukan innerHTML) agar aman dari XSS
            predictionResult.innerText = `${data.prediction} (${data.confidence})`;

            // Styling dinamis (Hijau untuk Real, Merah untuk Fake)
            if (data.prediction === "Real News") {
                resultBox.className = "mt-6 p-4 rounded-xl bg-green-100 text-green-800 border border-green-200 transition-all";
            } else {
                resultBox.className = "mt-6 p-4 rounded-xl bg-red-100 text-red-800 border border-red-200 transition-all";
            }
        } else {
            alert(data.message || "Terjadi kesalahan. Silakan coba lagi.");
        }
    } catch (error) {
        alert("Terjadi kesalahan sistem! Silakan coba lagi.");
        console.error(error);
    }
}
