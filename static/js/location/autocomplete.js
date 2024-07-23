let autocomplete;

function initAutocomplete() {
    autocomplete = new google.maps.places.Autocomplete(
        document.getElementById('location_autocomplete'),
        { 
            types: ['geocode'],
            componentRestrictions: {'country': ['gb']},
            fields: ['geometry']
        }
    );
}