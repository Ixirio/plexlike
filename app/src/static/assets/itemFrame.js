// Ajax method to get data from the API
async function getItemData(url, target) {
    $.ajax({
        method: 'GET',
        url: url,
        success: (result) => {
            target.innerHTML = result
        }
    });
}

// Method to open the itemFrame and get the data from API
async function openItemFrame(itemFrame, item) {
    itemFrame.classList.remove('hidden');

    await getItemData(item.dataset.itemRoute, itemFrame.querySelector('[data-item-frame-body]'));
}

// Item frame Handler
const itemFrameHandler = async () => {

    const itemFrame = document.querySelector('[data-item-frame]');

    // add event to open item frame
    document.querySelectorAll('[data-item]').forEach((item) => {
        item.addEventListener('click', (element) => {
            if (!('itemActionIgnore' in element.target.dataset)) {
                openItemFrame(itemFrame, item);
            }
        });
    });

    // close the item frame and remove data from it 
    itemFrame.querySelector('[data-item-frame-close-button]').addEventListener('click', () => {
        itemFrame.classList.add('hidden');
        itemFrame.querySelector('[data-item-frame-body]').innerHTML = '';
    });
}

export default itemFrameHandler;
