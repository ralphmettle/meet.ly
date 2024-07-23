/* Check if the input is an email address or a username */
document.addEventListener('DOMContentLoaded', function () {
    const inputField = document.getElementById('username');

    function inputChecker() {
        /* Regex to check if the input is an email address */
        const isEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(inputField.value);
        if (isEmail) {
            inputField.setAttribute('name', 'email');
        } else {
            inputField.setAttribute('name', 'username');
        }
    }

    inputField.addEventListener('input', inputChecker);

    /* Check the input type on page load */
    inputChecker();
});