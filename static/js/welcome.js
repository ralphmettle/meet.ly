const debugMode = false;

const debugElement = document.getElementById("debug_mode");

if (debugMode) {
    debugElement.style.display = "block"
} else {
    debugElement.style.display = "none"
}

function toggleDebugButton() {
    var lat = document.getElementById("latitude");
    var long = document.getElementById("longitude");
    var toggleDebugButton = document.getElementById("debug_coords");

    if (lat.type === "hidden") {
        lat.type = "text";
        long.type = "text";
        toggleDebugButton.textContent = "Hide coordinates";
    } else {
        lat.type = "hidden";
        long.type = "hidden";
        toggleDebugButton.textContent = "Show coordinates";
    }
}

function validateCoordinates(value) {
    parseFloat(value);
    return !isNaN(value) && value <= 90 && value >= -90;
}

/* Populate the hidden latitude and longitude fields with data obtained from Geolocation API or Places API
   Required for form submission */
function getCoordinates(position) {
    const lat = position.coords.latitude;
    const long = position.coords.longitude;
    const geolocationButton = document.querySelector(".geolocation-container button");

    if (validateCoordinates(lat) && validateCoordinates(long)) {
        document.getElementById("latitude").value = lat;
        document.getElementById("longitude").value = long;
        console.log(`Latitude: ${lat}, Longitude: ${long}`);
    } else {
        alert("Invalid coordinates. Please try again or input your location manually.");
    }

    geolocationButton.classList.remove("loading");
    geolocationButton.disabled = false;
    toggleAlertBanner(true);
}

/* Get user location via Geolocation API */
function getLocation(event) {
    event.preventDefault();
    const geolocationButton = document.querySelector(".geolocation-container button");
    geolocationButton.classList.add("loading");
    geolocationButton.disabled = true;

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(getCoordinates);
    } else {
        alert("Geolocation is not supported by this browser. Please input your location manually.");
        geolocationButton.classList.remove("loading");
        geolocationButton.disabled = false;
    }
}

/* Functions to show and hide the alert banner upon successful retreival of location info */
function toggleAlertBanner(bool) {
    const alertBanner = document.getElementById("alert-banner");

    if (bool) {
        showAlertBanner(alertBanner);
    } else {
        hideAlertBanner(alertBanner);
    }
}

function showAlertBanner(alertBanner) {
    alertBanner.classList.add("fade-in");
    alertBanner.style.display = "block";

    setTimeout(function () {
        alertBanner.classList.remove("fade-in");
        alertBanner.classList.add("fade-out");

        setTimeout(function () {
            alertBanner.classList.remove("fade-out");
            alertBanner.style.display = "none";
        }, 500);
    }, 3000);
}

function hideAlertBanner(alertBanner) {
    alertBanner.style.display = "none";
    alertBanner.classList.remove("fade-in", "fade-out");
}

/* Functions for Google Places API location autocomplete */
let autocomplete;

function initAutocomplete() {
    autocomplete = new google.maps.places.Autocomplete(
        document.getElementById("location_autocomplete"),
        {
            types: ["geocode"],
            componentRestrictions: { "country": ["gb"] },
            fields: ["geometry"]
        }
    );

    autocomplete.addListener("place_changed", getLocationInfo);
}

function getLocationInfo() {
    var place = autocomplete.getPlace();
    document.getElementById("latitude").value = place.geometry.location.lat();
    document.getElementById("longitude").value = place.geometry.location.lng();
}

/* Functions to handle profile picture upload and removal */
function newProfilePicture() {
    const profilePicture = document.getElementById("profile-picture");
    const profilePictureContainer = document.querySelector(".profile_picture-container img");

    const reader = new FileReader();
    reader.onload = function (event) {
        profilePictureContainer.src = event.target.result;
    }
    reader.readAsDataURL(profilePicture.files[0]);
}

function removeProfilePicture() {
    const profilePicture = document.getElementById("profile-picture");
    const profilePictureContainer = document.querySelector(".profile_picture-container img");

    profilePicture.value = "";
    profilePictureContainer.src = profilePictureContainer.dataset.default;
}