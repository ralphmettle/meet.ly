var debug = true;

document.getElementById('user_search-form').addEventListener('submit', async function (event) {
    event.preventDefault()

    const search_result = await searchUser();
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