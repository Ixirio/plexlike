// Flash message handler
const flashMessage = () => {

    // Get flash messages from dom element
    const flashMessagesOptions = JSON.parse($('[data-flash-message]').get(0).dataset.flashMessageOptions);

    // Check that we have at least one message
    if (flashMessagesOptions.messages.length === 0) return;

    // Create toasts for each messages
    flashMessagesOptions.messages.forEach((message) => {
        $.toast({ text: message[1], icon: message[0] })
    });
}

export default flashMessage;
