async function getHangouts() {
    const fetch_hangouts = await fetch('/process-get-hangouts', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
    });

    const data = await fetch_hangouts.json();
    console.log('Data:', data);

    if (data && data.hangouts_list) {
        displayHangouts(data.hangouts_list);
    } else {
        console.error('Error fetching hangouts:', data);
    }
}

async function checkAttendees(hangout) {
    const fetch_attendees = await fetch('/process-get-hangout-attendees', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'hangout_id': hangout.hangout_id})
    });

    const data = await fetch_attendees.json();
    console.log('Attendees:', data);

    if (data) {
        console.log('Success');
        return data;
    } else {
        console.error('Error fetching attendees:', data);
    }
}


async function displayHangouts(hangouts) {
    const container = document.getElementById('hangout_feed');
    const pendingContainer = document.getElementById('pending_hangout_feed');
    container.innerHTML = '';
    pendingContainer.innerHTML = '';

    const pendingHangouts = hangouts.filter(hangout => hangout.status === 'PENDING');
    const acceptedHangouts = hangouts.filter(hangout => hangout.status === 'ACCEPTED');

    if (pendingHangouts.length === 0) {
        pendingContainer.textContent = 'No pending invitations.';
    } else {
        for (const hangout of pendingHangouts) {
            const hangoutDiv = createHangoutDiv(hangout);
            const responseDiv = createResponseButtons(hangout);
            hangoutDiv.appendChild(responseDiv);
            pendingContainer.appendChild(hangoutDiv);
            const attendees = await checkAttendees(hangout);
            displayAttendees(hangoutDiv.querySelector('.attendees'), attendees);
        }
    }

    if (acceptedHangouts.length === 0) {
        container.textContent = 'No accepted hangouts found.';
    } else {
        for (const hangout of acceptedHangouts) {
            const hangoutDiv = createHangoutDiv(hangout);
            container.appendChild(hangoutDiv);
            const attendees = await checkAttendees(hangout);
            displayAttendees(hangoutDiv.querySelector('.attendees'), attendees);
        }
    }
}

function createHangoutDiv(hangout) {
    const hangoutDiv = document.createElement('div');
    hangoutDiv.className = 'hangout-box';
    hangoutDiv.id = hangout.name;

    const photo = document.createElement('img');
    photo.src = hangout.place_photo_url;
    photo.alt = hangout.place_name;
    hangoutDiv.appendChild(photo);

    const title = document.createElement('h2');
    const link = document.createElement('a');
    link.textContent = hangout.name;
    link.href = `/hangouts/${hangout.hangout_id}`;
    title.appendChild(link);
    hangoutDiv.appendChild(title);

    const address = document.createElement('h3');
    address.textContent = hangout.place_address;
    hangoutDiv.appendChild(address);
    
    const reviewSummary = document.createElement('p');
    reviewSummary.textContent = hangout.place_review_summary;
    hangoutDiv.appendChild(reviewSummary);

    const placeLink = document.createElement('a');
    placeLink.href = hangout.place_maps_link;
    placeLink.textContent = 'View on Google Maps';
    placeLink.target = '_blank';
    hangoutDiv.appendChild(placeLink);

    const attendeesDiv = document.createElement('div');
    attendeesDiv.className = 'attendees';
    attendeesDiv.textContent = 'Getting attendees...';
    hangoutDiv.appendChild(attendeesDiv);

    return hangoutDiv;
}

async function displayAttendees(container, attendees) {
    container.innerHTML = '';
    attendees.forEach(attendee => {
        const attendeeDiv = document.createElement('div');
        attendeeDiv.className = 'attendee';

        const photo = document.createElement('img');
        photo.src = `../static/images/profile_pictures/${attendee.profile_picture}` || '../static/images/profile_pictures/profile-picture_default.png';
        photo.alt = attendee.username;
        attendeeDiv.appendChild(photo);

        const name = document.createElement('h3');
        name.textContent = `@${attendee.username}`;
        attendeeDiv.appendChild(name);

        const status = document.createElement('p');
        status.textContent = attendee.status.charAt(0).toUpperCase() + attendee.status.slice(1);
        attendeeDiv.appendChild(status);

        container.appendChild(attendeeDiv);
    });
}

function createResponseButtons(hangout) {
    const responseDiv = document.createElement('div');
    responseDiv.className = 'invitation-response';

    const acceptButton = document.createElement('button');
    acceptButton.textContent = 'Accept';
    acceptButton.onclick = () => respondToInvitation(hangout.hangout_id, 'accept');

    const rejectButton = document.createElement('button');
    rejectButton.textContent = 'Reject';
    rejectButton.onclick = () => respondToInvitation(hangout.hangout_id, 'reject');

    responseDiv.appendChild(acceptButton);
    responseDiv.appendChild(rejectButton);

    return responseDiv;
}

async function respondToInvitation(hangoutId, response) {
    const res = await fetch('/process-respond-hangout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ hangout_id: hangoutId, response: response })
    });

    const data = await res.json();
    if (res.ok) {
        alert(data.message);
        getHangouts();
    } else {
        alert('Error: ' + data.message);
    }
}

getHangouts();