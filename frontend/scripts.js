const uploadForm = document.getElementById('uploadForm');
const imgInput = document.getElementById('imgInput');
const previewDiv = document.getElementById('preview');
const resultDiv = document.getElementById('result');

imgInput.addEventListener('change', function() {
    previewDiv.innerHTML = '';
    resultDiv.textContent = '';
    const file = imgInput.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const imgTag = document.createElement("img");
            imgTag.src = e.target.result;
            previewDiv.appendChild(imgTag);
        }
        reader.readAsDataURL(file);
    }
});

uploadForm.addEventListener('submit', function(e) {
    e.preventDefault();
    resultDiv.textContent = 'Predicting...';

    const file = imgInput.files[0];
    if (!file) {
        resultDiv.textContent = "Please select an image file!";
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    fetch('http://localhost:5000/predict', {
        method: 'POST',
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        if (data.prediction) {
            resultDiv.innerHTML = `
            <b>Landmark:</b> ${data.prediction}<br>
            <b>Confidence:</b> ${(data.confidence*100).toFixed(2)}%
            `;
        } else if (data.error) {
            resultDiv.textContent = "Error: " + data.error;
        } else {
            resultDiv.textContent = "Unexpected response.";
        }
    })
    .catch(err => {
        resultDiv.textContent = "Server error: " + err;
    });
});
