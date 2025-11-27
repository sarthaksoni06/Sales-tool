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
    // --- New Form Handling for AI Prediction Demo ---
const demoForm = document.getElementById('lead-demo-form');
const outputCategory = document.getElementById('output-category');
const outputProbability = document.getElementById('output-probability');
const outputRecommendation = document.getElementById('output-recommendation');
const API_URL = 'http://127.0.0.1:5000/predict_lead'; // Matches the Flask URL/Port

if (demoForm) {
    demoForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // 1. Gather form data
        const formData = new FormData(demoForm);
        const leadData = {};
        formData.forEach((value, key) => {
            // Ensure data is sent as numbers
            leadData[key] = parseInt(value, 10);
        });

        // 2. Update UI for loading state
        outputCategory.textContent = 'Analyzing lead data...';
        outputProbability.textContent = '';
        outputRecommendation.textContent = 'Please wait...';
        const submitButton = demoForm.querySelector('button[type="submit"]');
        submitButton.textContent = 'Processing...';
        submitButton.disabled = true;

        // 3. Send data to the Flask API
        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(leadData),
            });

            const result = await response.json();

            // 4. Handle API response
            if (result.success && result.prediction) {
                const pred = result.prediction;
                outputCategory.textContent = pred.category;
                outputProbability.textContent = `Conversion Probability: ${pred.conversion_probability}%`;
                outputRecommendation.innerHTML = `**Next Step:** ${pred.recommendation}`;
            } else {
                outputCategory.textContent = 'Prediction Error!';
                outputRecommendation.textContent = result.error || 'Could not get prediction from server.';
                outputProbability.textContent = '';
            }

        } catch (error) {
            console.error('API Call Failed:', error);
            outputCategory.textContent = 'Connection Error';
            outputRecommendation.textContent = 'Could not connect to the local API. Ensure `app.py` is running.';
        } finally {
            // Reset button state
            submitButton.textContent = 'Get AI Recommendation';
            submitButton.disabled = false;
        }
    });
}
// --- END New Form Handling ---

// The existing simple email sign-up form handling is still needed if you kept that form.
// You should ensure that the original email form submission handler (for the Hero section)
// is also present in this script.
