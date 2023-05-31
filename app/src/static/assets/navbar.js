// navBar menu handler
const navbarMenuHandler = () => {

    const selectorsList = [
        '.navbar-burger',
        '.navbar-close',
        '.navbar-backdrop'
    ]

    const menu = document.querySelector('.navbar-menu');

    // add event to hide or show navbar on mobile version
    selectorsList.forEach((selector) => {
        document.querySelector(selector).addEventListener('click', () => {
            menu.classList.toggle('hidden');
        });
    });
}

export default navbarMenuHandler;
