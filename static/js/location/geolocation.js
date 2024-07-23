function toggleButton() {
    var lat = document.getElementById("latitude");
    var long = document.getElementById("longitude");
    var toggleButton = document.getElementById("toggle_view");

    if (lat.type === "hidden") {
        lat.type = "text";
        long.type = "text";
        toggleButton.textContent = "Hide coordinates";
    } else {
        lat.type = "hidden";
        long.type = "hidden";
        toggleButton.textContent = "Show coordinates";
    }
}

function showPosition(position) {
    document.getElementById("latitude").value = position.coords.latitude;
    document.getElementById("longitude").value = position.coords.longitude;
}

function getLocation(event) {
    event.preventDefault();
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    } else {
        alert("Geolocation is not supported by this browser. Please input your location manually..");
    }
}