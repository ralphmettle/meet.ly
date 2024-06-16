document.addEventListener('DOMContentLoaded', function() {
  const emailInput = document.getElementById('email');
  const registerButton = document.querySelector('button[type="submit"]');
  const errorBanner = document.getElementById('error-banner');

  function validateEmail(email) {
      const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return re.test(String(email).toLowerCase());
  }

  function toggleErrorBanner(show) {
    if (show) {
        errorBanner.classList.add('fade-in');
        errorBanner.style.display = 'block';
        setTimeout(() => {
            errorBanner.classList.remove('fade-in');
            errorBanner.classList.add('fade-out');
            setTimeout(() => {
                errorBanner.style.display = 'none';
                errorBanner.classList.remove('fade-out');
            }, 500); // Duration of fade-out animation
        }, 5000); // Display error banner for 5 seconds
    } else {
        errorBanner.style.display = 'none';
        errorBanner.classList.remove('fade-in', 'fade-out');
    }
}

  registerButton.addEventListener('click', function(event) {
      const isValidEmail = validateEmail(emailInput.value);
      if (!isValidEmail) {
          event.preventDefault(); // Prevent form submission
          toggleErrorBanner(true); // Show error banner
      }
  });

  // Hide the error banner initially on email input change
  emailInput.addEventListener('input', function() {
      toggleErrorBanner(false);
  });
});