// static/js/script.js
var dropArea = document.getElementById('drop-area');
var fileInput = document.getElementById('file-input');
var filePreview = document.getElementById('file-preview');

dropArea.addEventListener('dragover', function(e) {
    e.preventDefault();
    dropArea.classList.add('highlight');
});

dropArea.addEventListener('dragleave', function() {
    dropArea.classList.remove('highlight');
});

dropArea.addEventListener('drop', function(e) {
    e.preventDefault();
    dropArea.classList.remove('highlight');

    var files = e.dataTransfer.files;
    fileInput.files = files;

    // Отображение выбранного файла
    displayFile(files[0]);
});

fileInput.addEventListener('change', function() {
    var files = fileInput.files;

    // Отображение выбранного файла
    displayFile(files[0]);
});

function displayFile(file) {
    if (file) {
        var fileType = getFileExtension(file.name);
        var iconName = getIconName(fileType);
        var fileName = file.name;

        filePreview.innerHTML = `
            <p>Выбранный файл:</p>
            <p>${iconName} ${fileName}</p>
        `;
    } else {
        filePreview.innerHTML = '';
    }

}

function getFileExtension(fileName) {
    return fileName.split('.').pop().toLowerCase();
}

function getIconName(fileType) {
    switch (fileType) {
        case 'jpg':
        case 'jpeg':
        case 'png':
        case 'gif':
            return '📷 Изображение';
        case 'pdf':
            return '<img src="/static/img/office_icons/pdf.png" alt="PDF Icon"> PDF';
        case 'xlsx':
            return '<img src="/static/img/office_icons/xlsx.png" alt="Excel Icon"> Excel';
        case 'docx':
            return '<img src="/static/img/office_icons/docx.png" alt="Word Icon"> Word';
        default:
            return '📄 Другой файл';
    }
}
