let debug = true;

document.getElementById('user_search-form').addEventListener('submit', async function (event) {
    event.preventDefault()

    const search_result = await searchUser();
    let display_result = await displayUsers(search_result, 'search-result');
});

async function searchUser() {
    const username = document.getElementById('user_search-input').value;

    if (!username) {
        alert('No username was entered, please enter a username.');
        return;
    }

    const get_response = await fetch('/process-search-user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username }),
    });

    const search_result = await get_response.json();
    
    if (debug) {
        console.log(search_result);
    }

    return search_result;
}

// Function incomplete; no relevant route or logic
async function displayUsers(user_list, container_id) {
    const container = document.getElementById(container_id);
    container.innerHTML = '';
    container.hidden = false;

    if (!user_list || user_list.length === 0) {
        container.innerHTML = 'No users found.';
        return;
    }

    user_list.forEach(function (user) {
        
        let profilePicture = user.profile_picture;

        if (!profilePicture) {
            profilePicture = 'static/images/profile_pictures/profile-picture_default.png';
        } else {
            profilePicture = `static/images/profile_pictures/${profilePicture}`;
        }

        if (container_id === 'search-result') {
            let userCard = document.createElement('div');
            userCard.className = 'user-card';
            userCard.id = 'user-card';

            userCard.innerHTML = `
                <img src="${profilePicture}" id="profile-picture" alt="Profile Picture">
                <div class="user_info-container" id="user-info">
                    <h3>@${user.username}</h3>
                    <p>${user.firstname} ${user.lastname}</p>
                </div>
                <button class="btn btn-primary" id=${user.username}>Add Friend</button>
            `;

            container.appendChild(userCard);
            addSendRequestListeners(`${user.username}`);
        } else if (container_id === 'friends-list') {
            let friendCard = document.createElement('div');
            friendCard.className = 'friend-card';
            friendCard.id = 'friend-card';

            friendCard.innerHTML = `
                <img src="${profilePicture}" id="profile-picture" alt="Profile Picture">
                <div class="friend_info-container" id="user-info">
                    <h3>@${user.username}</h3>
                    <p>${user.firstname} ${user.lastname}</p>
                </div>
            `;

            container.appendChild(friendCard);
        } else if (container_id === 'friend-requests-list-display') {
            let friendRequestCard = document.createElement('div');
            friendRequestCard.className = 'friend-request-card';
            friendRequestCard.id = 'friend-request-card';

            friendRequestCard.innerHTML = `
                <img src="${profilePicture}" id="profile-picture" alt="Profile Picture">
                <div class="friend_request_info-container" id="user-info">
                    <h3>@${user.username}</h3>
                    <p>${user.firstname} ${user.lastname}</p>
                </div>
                <button class="btn btn-accept" id="accept-button" data-user=${user.username}>Accept</button>
                <button class="btn btn-decline" id="decline-button" data-user=${user.username}>Decline</button>
            `;

            container.appendChild(friendRequestCard);
            addFriendRequestListneners();
        }
    });
}

async function getFriends() {
    const get_response = await fetch('/process-get-friends', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    });

    const friends_list = await get_response.json();

    if (debug) {
        console.log(friends_list);
    }

    return friends_list;
}

async function loadFriendsList() {
    const friends_list = await getFriends();
    let display_result = await displayUsers(friends_list, 'friends-list');

    if (debug) {
        console.log(display_result);
    }
}

function addSendRequestListeners(username) {
    const button = document.getElementById(username);

    button.addEventListener('click', async function (event) {
        event.preventDefault();

        const username = event.target.id;

        if (debug) {
            console.log(username);
        }
        
        const add_response = await fetch('/process-send-friend-request', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username }),
        });

        const add_result = await add_response.json();

        if (debug) {
            console.log(add_result);
        }
    });
}

function addFriendRequestListneners() {
    const accept_button = document.getElementById('accept-button');
    const decline_button = document.getElementById('decline-button');

    accept_button.addEventListener('click', async function (event) {
        event.preventDefault();

        const username = event.target.dataset.user;

        if (debug) {
            console.log(username);
        }

        const accept_response = await fetch('/process-accept-friend-request', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username }),
        });

        const accept_result = await accept_response.json();

        if (debug) {
            console.log(accept_result);
        }
    });

    decline_button.addEventListener('click', async function (event) {
        event.preventDefault();

        const username = event.target.dataset.user;

        if (debug) {
            console.log(username);
        }

        const decline_response = await fetch('/process-decline-friend-request', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username }),
        });

        const decline_result = await decline_response.json();

        if (debug) {
            console.log(decline_result);
        }
    });
}

async function countRequests() {
    const count_response = await fetch('/process-count-friend-requests', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    });

    const response = await count_response.json();

    if (debug) {
        console.log(response);
    }

    return response;
}

const friendRequestCounter = document.getElementById('friend-request-counter');

async function loadFriendRequestCount() {
    const countRequest = await countRequests();
    let count = countRequest.count;
    
    if (count === 0) {
        friendRequestCounter.innerHTML = 'No new friend requests';
    } else {
        friendRequestCounter.hidden = false
        friendRequestCounter.innerHTML = `${count} friend request(s)`;
        friendRequestCounter.addEventListener('click', async function() {
            document.getElementById('friend-requests-list').style.display = 'block';
            let friendRequests = await getFriendRequests();
            displayUsers(friendRequests, 'friend-requests-list-display');
        });
    }  
}

async function getFriendRequests() {
    const get_response = await fetch('/process-get-friend-requests', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    });

    const friend_requests = await get_response.json();

    if (debug) {
        console.log(friend_requests);
    }

    return friend_requests;
}

document.addEventListener('DOMContentLoaded', function() {
    loadFriendsList();
    loadFriendRequestCount();
});
