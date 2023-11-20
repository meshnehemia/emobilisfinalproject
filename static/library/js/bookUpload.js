let imagedropArea = document.getElementById('imageDropArea');
let imageInput = document.querySelector(`input[name="${'image'}"]`);
let filedropArea = document.getElementById('bookDropArea');
let bookInput = document.querySelector(`input[name="${'book'}"]`);
let selectedImage = '';

function handleFiles(files, type) {
    if (files.length > 0) {
        if (type === 'image') {
            selectedImage = files[0];
            imageInput.files = files;
            imagedropArea.style.backgroundImage = `url('${URL.createObjectURL(selectedImage)}')`;
            if (bookInput.files && bookInput.files.length > 0) {
                filedropArea.style.backgroundImage = `url('${URL.createObjectURL(selectedImage)}')`;
            }
        } else {
            bookInput.files = files;
            if (imageInput.files && imageInput.files.length > 0) {
                imagedropArea.style.backgroundImage = `url('${URL.createObjectURL(imageInput.files[0])}')`;
                filedropArea.style.backgroundImage = `url('${URL.createObjectURL(selectedImage)}')`;
            }
        }

        alert(`Selected ${type} file: ${imageInput}, Size: ${fileInput} bytes`);
    }
}


function setupDropArea(area, file, type) {
    area.addEventListener('dragenter', function (e) {
        e.preventDefault();
        area.classList.add('drag-over');
    });

    area.addEventListener('dragover', function (e) {
        e.preventDefault();
    });

    area.addEventListener('dragleave', function () {
        area.classList.remove('drag-over');
    });

    area.addEventListener('drop', function (e) {
        e.preventDefault();
        area.classList.remove('drag-over');
        let files = e.dataTransfer.files;
        handleFiles(files, type);
    });

    area.addEventListener('click', function () {
        file.click();
    });

    file.addEventListener('change', function () {
        let files = file.files;
        handleFiles(files, type);
    });
}

setupDropArea(imagedropArea, imageInput, 'image');
setupDropArea(filedropArea, bookInput, 'file');