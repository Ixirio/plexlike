async function getItemData(url, target) {
    $.ajax({
        method: 'GET',
        url: url,
        success: (result) => {
            target.innerHTML = result
        }
    });
}

async function openItemFrame(itemFrame, item) {

    itemFrame.classList.remove('hidden');

    console.log()
   

    closeFrameSelectors.forEach((selector) => {
        itemFrame.querySelector(selector).addEventListener('click', () => {
            itemFrame.classList.add('hidden');
        });
    });
    await getItemData(item.dataset.itemRoute, itemFrame.querySelector('[data-item-frame-body]'));

}

const closeFrameSelectors = [
    '[data-item-frame-close-button]',
    '[data-item-frame-backdrop]'
]

const itemFrameHandler = async () => {

    const itemFrame = document.querySelector('[data-item-frame]');

    document.querySelectorAll('[data-item]').forEach((item) => {
        item.addEventListener('click', () => {
            openItemFrame(itemFrame, item);
        });
    });

    closeFrameSelectors.forEach((selector) => {
        itemFrame.querySelector(selector).addEventListener('click', () => {
            itemFrame.classList.add('hidden');
            itemFrame.querySelector('[data-item-frame-body]').innerHTML = '';
        });
    });
}

export default itemFrameHandler;
