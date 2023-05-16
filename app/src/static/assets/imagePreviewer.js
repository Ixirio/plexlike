const previewImage = () => {
    const imageInput = document.querySelector('[data-image-input]');
    const imagePreview = document.querySelector('[data-image-preview]');

    imageInput.addEventListener('change', () => {
        const reader = new FileReader();
        reader.onload = () => {
            imagePreview.src = reader.result;
        };
        if (imageInput.files.length === 1) {
            imagePreview.parentElement.classList.add('mb-4');
            reader.readAsDataURL(imageInput.files[0]);
        }
    });
}

export default previewImage;
