// ImagePreviewer handler
const previewImage = () => {
    const imageInput = document.querySelector('[data-image-input]');
    const imagePreview = document.querySelector('[data-image-preview]');

    if (imageInput === null) return;

    // Add a listener to preview image when the image input is fullfilled
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
