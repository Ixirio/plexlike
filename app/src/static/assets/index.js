import navbarMenuHandler from './navbar.js'
import itemFrameHandler from './itemFrame.js';
import changeImage from './imagePicker.js';

document.addEventListener('DOMContentLoaded', navbarMenuHandler);
document.addEventListener('DOMContentLoaded', itemFrameHandler);

document.addEventListener('DOMContentLoaded', () => {

    console.log(document.querySelector('[data-image-input]').files)
    const imageInput = document.querySelector('[data-image-input]')
    imageInput.addEventListener('change', () => {
        console.log(imageInput.files)

        $('[data-image-preview]').attr('src', )

    });
    
});
