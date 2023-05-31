import navbarMenuHandler from './navbar.js'
import itemFrameHandler from './itemFrame.js';
import previewImage from './imagePreviewer.js';
import flashMessage from './flashMessage.js';

// register every handler on DomContentLoad
document.addEventListener('DOMContentLoaded', navbarMenuHandler);
document.addEventListener('DOMContentLoaded', itemFrameHandler);
document.addEventListener('DOMContentLoaded', previewImage);
document.addEventListener('DOMContentLoaded', flashMessage);
