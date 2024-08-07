var debug = true;

document.getElementById('prompt-submit').addEventListener('click', async function () {
    const response = await submitPrompt();

    if (response) {
        const keywords = response.join(', ');

        if (debug) {
            if (keywords) {
                alert(`Prompt submitted successfully! Keywords are: [${keywords}]`);
            }
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

    const response = await get_response.json();
    
    if (debug) {
        console.log(response);
    }

    return response;
}
