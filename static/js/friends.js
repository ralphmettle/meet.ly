let debug = true;

document.getElementById('user_search-form').addEventListener('submit', async function (event) {
    event.preventDefault()

    const search_result = await searchUser();
    let display_result = await displayUsers(search_result, 'search-result', true);
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
async function displayUsers(user_list, container_id, addFriend) {
    const container = document.getElementById(container_id);
    container.innerHTML = '';
    container.hidden = false;

    if (!user_list || user_list.length === 0) {
        container.innerHTML = 'No users found.';
        return;
    }

    user_list.forEach(function (user) {
        let userCard = document.createElement('div');
        userCard.className = 'user-card';
        userCard.id = 'user-card';

        let profilePicture = user.profile_picture;

        if (!profilePicture) {
            profilePicture = 'static/images/profile_pictures/profile-picture_default.png';
        } else {
            profilePicture = `static/images/profile_pictures/${profilePicture}`;
        }

        if (addFriend === true) {
            userCard.innerHTML = `
                <img src="${profilePicture}" id="profile-picture" alt="Profile Picture">
                <div class="user_info-container" id="user-info">
                    <h3>@${user.username}</h3>
                    <p>${user.firstname} ${user.lastname}</p>
                </div>
                <button class="btn btn-primary">Add Friend</button>
            `;

            container.appendChild(userCard);
        } else {
            userCard.innerHTML = `
                <img src="${profilePicture}" id="profile-picture" alt="Profile Picture">
                <div class="user_info-container" id="user-info">
                    <h3>@${user.username}</h3>
                    <p>${user.firstname} ${user.lastname}</p>
                </div>
            `;

            container.appendChild(userCard);
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
    let display_result = await displayUsers(friends_list, 'friends-list', false);

    if (debug) {
        console.log(display_result);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    loadFriendsList();
});