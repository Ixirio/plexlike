const navbarMenuHandler = () => {

    const selectorsList = [
        '.navbar-burger',
        '.navbar-close',
        '.navbar-backdrop'
    ]

    const menu = document.querySelector('.navbar-menu');

    selectorsList.forEach((selector) => {
        document.querySelector(selector).addEventListener('click', () => {
            menu.classList.toggle('hidden');
        });
    });
}

export default navbarMenuHandler;
