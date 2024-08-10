let debug = true;

document.getElementById('user_search-form').addEventListener('submit', async function (event) {
    event.preventDefault()

    const search_result = await searchUser();
    let display_result = await displayUsers(search_result);
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
async function displayUsers(search_result) {
    const searchResultContainer = document.getElementById('search-result');
    searchResultContainer.innerHTML = '';
    searchResultContainer.hidden = false;

    if (!search_result || search_result.length === 0) {
        searchResultContainer.innerHTML = 'No users found.';
        return;
    }

    search_result.forEach(function (user) {
        let userCard = document.createElement('div');
        userCard.className = 'user-card';
        userCard.id = 'user-card';

        let profilePicture = user.profile_picture;

        if (!profilePicture) {
            profilePicture = 'static/images/profile_pictures/profile-picture_default.png';
        } else {
            profilePicture = `static/images/profile_pictures/${profilePicture}`;
        }

        userCard.innerHTML = `
            <img src="${profilePicture}" id="profile-picture" alt="Profile Picture">
            <div class="user_info-container" id="user-info">
                <h3>@${user.username}</h3>
                <p>${user.firstname} ${user.lastname}</p>
            </div>
            <button class="btn btn-primary">Add Friend</button>
        `;

        searchResultContainer.appendChild(userCard);
    });
}