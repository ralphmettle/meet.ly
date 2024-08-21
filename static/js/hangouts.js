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
    container.innerHTML = '';
    if (hangouts.length === 0) {
        container.textContent = 'No hangouts found. Create one!';
        return;
    } else {
        for (const hangout of hangouts) {
            const hangoutDiv = document.createElement('div');
            hangoutDiv.className = hangout.name;

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

            container.appendChild(hangoutDiv);

            const attendees = await checkAttendees(hangout);
            displayAttendees(attendeesDiv, attendees);
        }
    }
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

getHangouts();