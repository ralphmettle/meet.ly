var debug = true;

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

    const geocode_response = await getPlaceGeocode(process_response);

    if (geocode_response) {
        if (debug) {
            alert('Geocode completed successfully!');
        }
    }
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

async function getPlaceGeocode(place_data) {
    if (!place_data) {
        alert('No place data was found, please enter a prompt.');
        return;
    }

    const geocode_response = await fetch('/process-place-geocode', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ place_data }),
    });

    const response = await geocode_response.json();

    if (debug) {
        console.log(response);
    }

    return response;

}