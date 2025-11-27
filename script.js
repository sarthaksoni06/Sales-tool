document.addEventListener('DOMContentLoaded', () => {
    
    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId !== '#') {
                document.querySelector(targetId).scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Simple Form Submission Handling (Simulating Waitlist Sign-up)
    const form = document.querySelector('.early-access-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const emailInput = form.querySelector('input[type="email"]');
            const submitButton = form.querySelector('.btn-primary');
            const smallText = document.querySelector('.small-text');

            if (emailInput.value) {
                // Simulate an API call delay
                submitButton.textContent = 'Submitting...';
                submitButton.disabled = true;

                setTimeout(() => {
                    alert(`Thank you for signing up with ${emailInput.value}! You've been added to the early access list.`);
                    
                    emailInput.value = ''; // Clear the input
                    smallText.textContent = 'Success! Check your inbox for updates.';
                    smallText.style.color = var(--secondary-color); // Optional: change color to green

                    submitButton.textContent = 'Join the Waitlist Today';
                    submitButton.disabled = false;
                }, 1500); // 1.5 second delay
            }
        });
    }
});
