let currentChatId = null;
let currentUserId = null;
let latestMessageId = null;

const setHeaderImage = () => {
    const pageElement = document.querySelector('#self-image');
    let imageElement = document.createElement('img') // <img />
    imageElement.classList.add('icon-img'); // <img class="icon-img" />
    imageElement.setAttribute("src", "`images/${mockAPI.myInfo.icon}`") // <img class="icon-img" src="images/pup1.jpg"/>
    imageElement.setAttribute("alt", "Puppy Icon Image for " + mockAPI.myInfo.myName)
    pageElement.appendChild(imageElement)
    console.log(imageElement)
}

// last message
let lastSeenMessage = document.querySelectorAll('.mssg-time')

// Last message in DB
//let lastMessage = fetch(`/api/chats${currentChatId}/messages?user_id=${currentUserId}`, {
//    method: 'GET'}).then(result =>result.json()).created_at

// retrieveMessages(currentChatId, currentUserId)
setInterval( ()=> {
    retrieveMessages(currentChatId, currentUserId, latestMessageId) // retrieve all messages larger than the latestMessageId
},2000);


// Makes a GET request to retrieve the last message for a user. Turns it into JSON then adds messages to body.
const retrieveMessages = (chat_id, user_id, greater_than_message_id = null) => {
    console.log(greater_than_message_id)
    if(chat_id === null || user_id === null) { // Error handling if not chat_id or user_id is selected 
        return;
    }
    let url = `/api/chats/${chat_id}/messages?user_id=${user_id}`
    if(greater_than_message_id !== null) { // greater_than_message_id assures that only messages larger than the current message get retrieved
        url += '&greater_than_message_id=' + greater_than_message_id; // Append greater_than_message_id parameter if parameter is not null
    }
    fetch(url, { // Get the last message 
        method: 'GET'
    }).then(result => result.json())
       .then(data => {
           console.log(data.map((m) => m.id)) 
           const ids = data.map((m) => m.id) // List comprehension - returns an array of ids
           if(ids.length > 0) { // If there are messages
                latestMessageId = Math.max(...ids) // Return the largest id
           }
           addMessages(data) // Add the last message into the displayed messages
        })
}

    
// Assigns a variable to all elements with the classname convo
    const conversationElements = document.getElementsByClassName("convo");

// Creates a function that registers each click and returns the chat and user id

    const convoClick = (event) => {
        const clicked = event.currentTarget; // clicked chat
        console.log(clicked.dataset)
        const dataAttributes = clicked.dataset
        const chat_id = dataAttributes.chat_id // current chat_id
        document.querySelector('#sndr-chat_id').value = chat_id; // setting the sndr-chat_id to the current chat_id
        currentChatId = chat_id // Reassign the current ChatId to the the clicked chat_id
        currentUserId = dataAttributes.user_id // Setting the current user_id
        let activeConversation = document.querySelector('.active')
        console.log(activeConversation)
        if (activeConversation !== null) { // if the active conversation is not null
            activeConversation.classList.remove('active') // Remove the class active
        } 
        clicked.classList.add('active') // Add the class active
        deleteMessages() // Delete all message in main-chat-wrap
        retrieveMessages(dataAttributes.chat_id, dataAttributes.user_id); // Retrieve messages
    }
    for(let i = 0; i < conversationElements.length; i++) {
        conversationElements[i].addEventListener('click', convoClick, false)
    }

    const createMessage = (message) => {
        let msgWrap = document.createElement('div');
        msgWrap.classList.add('message-wrap');
        let msgOut = document.createElement('div');
        const urlParams = new URLSearchParams(window.location.search)
        const myParam = urlParams.get('user_id');
        if (myParam == message.sender_id) {
            msgOut.classList.add('message', 'out')
        } else {
            msgOut.classList.add('message', 'in')
        }
        let msgP = document.createElement('p');
        msgP.classList.add('mssg');
        msgP.innerHTML = message.content
        let msgTime = document.createElement('p');
        msgTime.classList.add('mssg-time');
        msgTime.innerHTML = message.created_at;
        msgOut.appendChild(msgP)
        msgOut.appendChild(msgTime)
        msgWrap.appendChild(msgOut);
        let pageElement = document.querySelector('#main-chat-wrap')
        pageElement.appendChild(msgWrap)
    }

    const deleteMessages = () => {
        document.querySelector('#main-chat-wrap').innerHTML = ''
    }

    const addMessages = (messages) => {
        for (let message of messages) {
            createMessage(message)
            }
        
        }

    const submitNewMessage = () => {
        //formContent = '{"content": ' + '"' + document.getElementById("new-message").value + '"}'
        //console.log(formContent)

        const urlParams = new URLSearchParams(window.location.search) // Gets URL parameters
        const myParam = urlParams.get('user_id'); // Gets user_id
        const activeConversation = document.querySelector('.active').dataset.chat_id
        console.log(activeConversation)
        const postUrl = `/api/chats/${activeConversation}/messages?user_id=${myParam}`
    
        fetch(postUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                content: document.getElementById("new-message").value
            }),
    })

        .then(res => res.json())
        .then(data => {
            createMessage(data)
            document.querySelector('#new-message').value = '';
            document.querySelector(`div.convo[data-chat_id="${activeConversation}"] p.mssg`).innerHTML = data.body
        })
    }