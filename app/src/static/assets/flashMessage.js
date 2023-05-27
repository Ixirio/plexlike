const flashMessage = () => {

    const $flashMessageContainer = $('[data-flash-message]');
    const flashMessagesOptions = JSON.parse($flashMessageContainer.get(0).dataset.flashMessageOptions);

    if (flashMessagesOptions.messages.length > 0) {
        flashMessagesOptions.messages.forEach((message) => {
            $.toast({
                text: message[1],
                icon: message[0]
            })
        });
    }
}

export default flashMessage;
