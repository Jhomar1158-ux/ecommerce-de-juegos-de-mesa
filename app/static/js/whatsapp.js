window.onload = function() {
    const chatButton = document.getElementById('chat-start-btn');
    const chatBox = document.getElementsByClassName('chat-box-container')[0]
    const chatBoxCloseBtn = document.getElementById('cb-close-btn');
    let isChatActive = false;


    chatBoxCloseBtn.addEventListener('click', handleChatClick)
    chatButton.addEventListener('click', handleChatClick)

    function handleChatClick(){
        console.log('start handle')
        console.log(isChatActive);
        isChatActive = !isChatActive
        if(isChatActive){
            chatBox.classList.add('appear-up')
        } else {
            chatBox.classList.remove('appear-up')
        }
        console.log(isChatActive);
    }

};