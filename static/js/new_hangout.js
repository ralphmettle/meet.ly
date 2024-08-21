var debug = true;
let placeImages = [];
let currentIndex = 0;
let coordinateCentroid = {};

document.getElementById('prompt-submit').addEventListener('click', async function () {
    const prompt_response = await submitPrompt();

    if (invitee_list.length === 0) {
        alert('No friends were invited, please invite a friend first.');
        return;
    }
    if (prompt_response) {
        const keywords = prompt_response.join(', ');

        if (debug) {
            if (keywords) {
                alert(`Prompt submitted successfully! Keywords are: [${keywords}]`);
            }
        }
    }

    const search_response = await searchPrompt(prompt_response);

    if (search_response) {
        if (debug) {
            alert('Search completed successfully!');
        }
    }

    const process_response = await processSearch(search_response);

    if (process_response) {
        if (debug) {
            alert('Processing completed successfully!');
        }
    }

    placeImages = [];
    for (const placeName in process_response) {
        if (process_response.hasOwnProperty(placeName)) {
            const placeId = process_response[placeName][0];  // The first entry is the Place ID
            await loadPlaceAsHangout(placeId, placeName);
        }
    }

    showPlaceImages();
});

async function submitPrompt() {
    const prompt = document.getElementById('prompt').value;

    if (!prompt) {
        alert('No prompt was entered, please enter a prompt.');
        return;
    }

    const get_response = await fetch('/process-hangout-prompt', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ prompt }),
    });

    const keywords = await get_response.json();
    
    if (debug) {
        console.log(keywords);
    }

    return keywords;
}

const friendSearchInput = document.getElementById('invitee-input');

document.getElementById('invitee-input-form').addEventListener('submit', function (event) {
    event.preventDefault();
});

async function searchFriends(search) {
    const search_response = await fetch('/process-search-friends', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ search }),
    });

    const response = await search_response.json();

    if (debug) {
        console.log(response);
    }

    return response;
}

let invitee_list = [];

async function displayUsers(user_list) {
    const container = document.getElementById('invitee-search');
    container.innerHTML = '';

    if (user_list.length === 0) {
        container.innerHTML = 'No results.';
        return;
    }

    user_list.forEach(function (user) {
        const profilePicture = `../static/images/profile_pictures/${user.profile_picture}` ||
        '../static/images/profile_pictures/profile-picture_default.png';

        const inviteeCard = document.createElement('div');
        inviteeCard.className = 'invitee-card';
        inviteeCard.id = `${user.username}`;

        inviteeCard.innerHTML = `
            <img src="${profilePicture}" id="profile-picture" alt="Profile Picture">
            <div class="search_card-container" id="user-info">
                <h3>@${user.username}</h3>
                <p>${user.firstname} ${user.lastname}</p>
            </div>
            <button class="btn btn-invite" id="invite-button" data-user="${user.username}">Invite</button>
        `;

        container.appendChild(inviteeCard);

        inviteeCard.querySelector('#invite-button').addEventListener('click', async function () {
            const username = inviteeCard.id;

            if (!invitee_list.includes(username)) {
                invitee_list.push(username);
                alert(`${username} has been added to the invite list.`);
                displayInvited();
                console.log(invitee_list);

                coordinateCentroid = await getCentralCoordinates();
                console.log(coordinateCentroid);
            } else {
                alert(`${username} is already on the invite list.`);
                console.log(invitee_list);
            }
        });
    });
}

async function displayInvited() {
    const invitedContainer = document.getElementById('invited-list');
    invitedContainer.innerHTML = '';

    if (invitee_list.length === 0) {
        invitedContainer.innerHTML = 'Invite a friend!';
        return;
    }

    invitee_list.forEach(function (username) {
        const invitedCard = document.createElement('div');
        invitedCard.className = 'invited-card';
        invitedCard.id = `${username}`;
        
        const profilePicture = `../static/images/profile_pictures/${username}.jpg` ||
        `../static/images/profile_pictures/${username}.png` ||
        '../static/images/profile_pictures/profile-picture_default.png';

        invitedCard.innerHTML = `
            <img src="${profilePicture}" id="profile-picture" alt="Profile Picture">
            <h3>@${username}</h3>
            <button class="btn btn-invited" id="remove-button" data-user="${username}">Remove</button>
        `;
        invitedCard.querySelector('#remove-button').addEventListener('click', async function () {
            invitee_list = invitee_list.filter(user => user !== username);
            displayInvited();
            console.log(invitee_list);

            coordinateCentroid = await getCentralCoordinates();
            console.log(coordinateCentroid);
        });

        invitedContainer.appendChild(invitedCard);
    });
}

friendSearchInput.addEventListener('input', async function () {
    const search_response = await searchFriends(friendSearchInput.value);
    displayUsers(search_response);
});

async function getCentralCoordinates() {
    const central_coordinates = await fetch('/process-get-central-coordinates', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ invitee_list }),
    });

    const response = await central_coordinates.json();

    if (debug) {
        console.log(response);
    }

    return response;
}

async function searchPrompt(keywords) {
    if (!keywords) {
        alert('No keywords were found, please enter a prompt.');
        return;
    }

    const search_response = await fetch('/process-hangout-search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ keywords, coordinateCentroid }),
    });

    const response = await search_response.json();

    if (debug) {
        console.log(response);
    }

    return response;
}

async function processSearch(results) {

    if (!results) {
        alert('No results were found, please enter a prompt.');
        return;
    }

    const search_response = await fetch('/process-place-info', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ results }),
    });

    const response = await search_response.json();

    if (debug) {
        console.log(response);
    }

    return response;
}

async function getReviews(placeId) {
    const service = new google.maps.places.PlacesService(document.createElement('div'));
    const reviews = [];

    // Wait for the reviews to be retrieved before running the next functions
    return new Promise(function(resolve) {
        service.getDetails({ placeId: placeId }, function(place, status) {
            if (status === google.maps.places.PlacesServiceStatus.OK) {
                if (place.reviews && place.reviews.length > 0) {
                    place.reviews.slice(0, 5).forEach(function(review) {
                        reviews.push({text: review.text});
                    });
                }
                resolve(reviews);
                

                if (debug) {
                    console.log(reviews);
                }
            } else {
                console.error(`Place details request for ${placeId} failed.`);
                resolve();
            }
        });
    });
}

async function getReviewSummary(placeId) {
    const reviews = await getReviews(placeId);

    if (!reviews || reviews.length === 0) {
        alert('No reviews were found, please try again.');
        return;
    }

    const review_response = await fetch('/process-review-summary', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ reviews: reviews }),
    });

    const response = await review_response.json();

    if (debug) {
        console.log(response);
    }

    return response;
}

async function loadPlaceAsHangout(placeId, placeName) {
    const service = new google.maps.places.PlacesService(document.createElement('div'));
    
    return new Promise(function(resolve) {
        service.getDetails({ placeId: placeId }, function(place, status) {
            if (status === google.maps.places.PlacesServiceStatus.OK) {
                if (place.photos && place.photos.length > 0) {
                    const photoUrl = place.photos[0].getUrl({ maxWidth: 400 });
                    const placeAddress = place.formatted_address;
                    console.log(`Photo for ${placeName}: ${photoUrl}`);

                    // Get the photo and the image name and save them to a list object
                    const imgElement = document.createElement('img');
                    imgElement.src = photoUrl;
                    imgElement.alt = placeName;
                    
                    const labelElement = document.createElement('p');
                    labelElement.textContent = placeName;

                    const addressElement = document.createElement('p');
                    addressElement.textContent = placeAddress;
                    
                    // Get the place details for each place and add then to the dataset for each div element in the container
                    const containerDiv = document.createElement('div');
                    containerDiv.className = 'place-item';
                    containerDiv.dataset.placeName = placeName;
                    containerDiv.dataset.placeId = placeId;
                    containerDiv.dataset.address = placeAddress;
                    containerDiv.dataset.lat = place.geometry.location.lat();
                    containerDiv.dataset.lng = place.geometry.location.lng();
                    containerDiv.dataset.photoUrl = photoUrl;

                    containerDiv.appendChild(imgElement);
                    containerDiv.appendChild(labelElement);
                    containerDiv.appendChild(addressElement);
                    
                    // Display the clicked place on the page to be selected for the hangout
                    containerDiv.addEventListener('click', async function() {
                        const placeName = containerDiv.dataset.placeName;
                        const placeId = containerDiv.dataset.placeId;
                        const placeAddress = containerDiv.dataset.address;
                        const latitude = containerDiv.dataset.lat;
                        const longitude = containerDiv.dataset.lng;
                        console.log(`Place Name: ${placeName}, Place ID: ${placeId}, Address: ${placeAddress}, Latitude: ${latitude}, Longitude: ${longitude}`);
                        
                        const reviewSummary = JSON.parse(await getReviewSummary(placeId));
                        console.log(`reviewSummary JSON object: ${reviewSummary}`);
                        const summaryText = reviewSummary.summary;
                        console.log(`Review Summary for ${placeName}: ${summaryText}`);

                        document.getElementById('place_image').src = photoUrl;
                        document.getElementById('place_name').textContent = placeName;
                        document.getElementById('place_id').textContent = placeId;
                        document.getElementById('place_address').textContent = placeAddress;
                        document.getElementById('place_latitude').textContent = latitude;
                        document.getElementById('place_longitude').textContent = longitude;
                        document.getElementById('place_review_summary').textContent = summaryText;
                        document.getElementById('hangout_datetime').value = new Date().toISOString().slice(0, 16);
                        document.getElementById('place_maps_link').href = `https://www.google.com/maps/place/?q=place_id:${placeId}`;
                        showPlaceDetails();                      
                    });

                    placeImages.push({ containerDiv });

                } else {
                    console.error(`No photos available for ${placeName}.`);
                }
            } else {
                console.error(`Place details request for ${placeName} failed.`);
            }
            resolve();
        });
    });
}

document.getElementById('prompt-submit').addEventListener('click', function() {
    document.getElementById('prev-images').style.display = 'inline-block';
    document.getElementById('next-images').style.display = 'inline-block';
});

function showPlaceDetails() {
    document.getElementById('place_overlay-container').style.display = 'block';
}

function showPlaceImages() {
    const placeImageContainer = document.getElementById('place_image-container');
    placeImageContainer.style.display = 'block';
    placeImageContainer.innerHTML = '';

    for (let i = 0; i < 3 && (currentIndex + i) < placeImages.length; i++) {
        const counter = placeImages[currentIndex + i];
        placeImageContainer.appendChild(counter.containerDiv);

    }
}

document.getElementById('prev-images').addEventListener('click', function () {
    currentIndex -= 3;
    if (currentIndex < 0) {
        currentIndex = 0;
    }
    showPlaceImages();
});

document.getElementById('next-images').addEventListener('click', function () {
    currentIndex += 3;
    if (currentIndex >= placeImages.length) {
        currentIndex = 0;
    }
    showPlaceImages();
});

async function addHangout() {
    let hangoutName = document.getElementById('hangout_name').textContent;
    let placeId = document.getElementById('place_id').textContent;
    let placeName = document.getElementById('place_name').textContent;
    let placeAddress = document.getElementById('place_address').textContent;
    let placeLatitude = document.getElementById('place_latitude').textContent;
    let placeLongitude = document.getElementById('place_longitude').textContent;
    let placeReviewSummary = document.getElementById('place_review_summary').textContent;
    let placePhotoUrl = document.getElementById('place_image').src;
    let placeDateTime = new Date(document.getElementById('hangout_datetime').value).toISOString().slice(0, 19).replace('T', ' ');  // Formatting for database/backend conversion
    let placeMapsLink = document.getElementById('place_maps_link').href;

    console.log(JSON.stringify({ hangoutName, placeId, placeName, placeAddress, placeLatitude, placeLongitude, placeReviewSummary, placePhotoUrl, placeDateTime, placeMapsLink, invitee_list }))
    
    if (invitee_list.length === 0) {
        alert('No friends were invited, please invite a friend.');
        return;
    } else if (hangoutName === 'Hangout Name (Edit me!)') {
        alert('Please name your hangout!');
        return;
    } else {
        const add_response = await fetch('/process-add-hangout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ hangoutName, placeId, placeName, placeAddress, placeLatitude, placeLongitude, placeReviewSummary, placePhotoUrl, placeDateTime, placeMapsLink, invitee_list }),
        });

        const response = await add_response.json();

        if (debug) {
            console.log(response);
        }

        alert('Hangout added successfully!');
        window.location.href = '/hangouts';
    }
}

document.getElementById('confirm_hangout-button').addEventListener('click', async function () {
    const hangout_response = await addHangout();

    if (hangout_response) {
        if (debug) {
            alert('Hangout added successfully!');
        }
    }
});

