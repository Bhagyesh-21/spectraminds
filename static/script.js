function showProgress() {
    document.getElementById('submitBtn').disabled = true;
    document.getElementById('progress').style.display = 'block';
}

const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('fileInput');
const previewContainer = document.getElementById('preview-container');

dropZone.addEventListener('click', () => fileInput.click());

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('dragover');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('dragover');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
    fileInput.files = e.dataTransfer.files;
    showPreviews(e.dataTransfer.files);
});

fileInput.addEventListener('change', () => {
    showPreviews(fileInput.files);
});

function showPreviews(files) {
    previewContainer.innerHTML = '';
    const previews = [];
    Array.from(files).forEach(file => {
        if (file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = (e) => {
                previews.push({ name: file.name, src: e.target.result });
                const div = document.createElement('div');
                div.classList.add('preview');
                div.innerHTML = `<img src="${e.target.result}" alt="${file.name}"><p><strong>${file.name}</strong></p>`;
                previewContainer.appendChild(div);
                localStorage.setItem('imagePreviews', JSON.stringify(previews));
            };
            reader.readAsDataURL(file);
        }
    });
}

window.addEventListener('DOMContentLoaded', () => {
    const saved = localStorage.getItem('imagePreviews');
    if (saved) {
        const previews = JSON.parse(saved);
        previews.forEach(({ name, src }) => {
            const div = document.createElement('div');
            div.classList.add('preview');
            div.innerHTML = `<img src="${src}" alt="${name}"><p><strong>${name}</strong></p>`;
            previewContainer.appendChild(div);
        });
        localStorage.removeItem('imagePreviews');
    }
});


function showProgress() {
    const progress = document.getElementById("progress");
    const bar = document.getElementById("progress-bar");
    const submitBtn = document.getElementById("submitBtn");

    progress.style.display = "block";
    submitBtn.disabled = true;

    let width = 0;
    const interval = setInterval(() => {
        if (width >= 100) {
            clearInterval(interval);
        } else {
            width += 1;
            bar.style.width = width + "%";
        }
    }, 300); // Adjust speed as needed
}

    window.addEventListener("DOMContentLoaded", function () {
        const resultsSection = document.getElementById("results");
        const progress = document.getElementById("progress");
        const submitBtn = document.getElementById("submitBtn");
    });
