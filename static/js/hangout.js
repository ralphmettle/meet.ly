var debug = true;
let placeImages = [];
let currentIndex = 0;

document.getElementById('prompt-submit').addEventListener('click', async function () {
    const prompt_response = await submitPrompt();

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
            await getPlacePhoto(placeId, placeName);
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
        body: JSON.stringify({ keywords }),
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
    return new Promise((resolve) => {
        service.getDetails({ placeId: placeId }, (place, status) => {
            if (status === google.maps.places.PlacesServiceStatus.OK) {
                if (place.reviews && place.reviews.length > 0) {
                    place.reviews.slice(0, 5).forEach(review => {
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

async function getPlacePhoto(placeId, placeName) {
    const service = new google.maps.places.PlacesService(document.createElement('div'));
    // Wait for the photos to be retrieved before running the next functions
    return new Promise((resolve) => {
        service.getDetails({ placeId: placeId }, (place, status) => {
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

                    // Append elements to the container
                    containerDiv.appendChild(imgElement);
                    containerDiv.appendChild(labelElement);
                    containerDiv.appendChild(addressElement);
                    
                    // Display the clicked place on the page to be selected for the hangout
                    containerDiv.addEventListener('click', async () => {
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
                        document.getElementById('place_address').textContent = placeAddress;
                        document.getElementById('place_review_summary').textContent = summaryText;
                        document.getElementById('place_maps_link').href = `https://www.google.com/maps/place/?q=place_id:${placeId}`;                        
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
    const hangoutName = document.getElementById('hangout_name').value;
    const placeId = document.getElementById('place_image').dataset.placeId;
    const placeName = document.getElementById('place_name').textContent;
    const placeAddress = document.getElementById('place_address').textContent;
    const placeReviewSummary = document.getElementById('place_review_summary').textContent;
    const placePhotoUrl = document.getElementById('place_image').src;
    const placeMapsLink = document.getElementById('place_maps_link').href;

    const add_response = await fetch('/add-hangout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ hangoutName, placeId, placeName, placeAddress, placeReviewSummary, placePhotoUrl, placeMapsLink }),
    });

    const response = await add_response.json();

    if (debug) {
        console.log(response);
    }

    return response;
}

