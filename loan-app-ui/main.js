// AWS API Gateway endpoint
const DEPLOYED_URL = 'https://ih938ywix9.execute-api.us-east-1.amazonaws.com';
const API_URL = `${DEPLOYED_URL}/process_loan_applications`;

const loanForm = document.getElementById('loanForm');
const submitBtn = document.getElementById('submitBtn');
const resultModal = document.getElementById('resultModal');
const resultTitle = document.getElementById('resultTitle');
const resultMessage = document.getElementById('resultMessage');
const statusIcon = document.getElementById('statusIcon');
const resultBreakdown = document.getElementById('resultBreakdown');

loanForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // UI State: Loading
    submitBtn.disabled = true;
    submitBtn.classList.add('btn-loading');
    showModal('Analyzing Data...', 'Our ML model is evaluating the risk profile for this application.', 'processing');

    // Collect Data
    const formData = new FormData(loanForm);
    const data = {};
    formData.forEach((value, key) => {
        // Convert numbers
        if (value && !isNaN(value) && key !== 'Gender' && key !== 'Marital_Status' && key !== 'Education_Level' && key !== 'Employment_Type' && key !== 'Employer_Category' && key !== 'Loan_Purpose') {
            data[key] = parseFloat(value);
        } else {
            data[key] = value || null;
        }
    });

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify([data]) // API expects a list
        });

        if (!response.ok) throw new Error('Network response was not ok');

        const result = await response.json();
        const prediction = result.results[0].prediction;
        
        displayResult(prediction);
    } catch (error) {
        console.error('Error:', error);
        displayResult('Error');
    } finally {
        submitBtn.disabled = false;
        submitBtn.classList.remove('btn-loading');
    }
});

function showModal(title, message, statusClass) {
    resultTitle.textContent = title;
    resultMessage.textContent = message;
    statusIcon.className = 'status-icon ' + statusClass;
    resultModal.classList.add('active');
    resultBreakdown.innerHTML = '';
}

function displayResult(prediction) {
    if (prediction === 'Approved') {
        resultTitle.textContent = 'Application Approved';
        resultMessage.textContent = 'Congratulations! The risk analysis indicates a high probability of successful repayment.';
        statusIcon.className = 'status-icon approved';
        
        resultBreakdown.innerHTML = `
            <div style="color: #4ade80; font-weight: 600; margin-bottom: 0.5rem;">Risk Profile: Low</div>
            <p style="font-size: 0.9rem; color: #94a3b8;">The internal logistic regression model has verified the creditworthiness based on the 22 provided attributes.</p>
        `;
    } else if (prediction === 'Rejected') {
        resultTitle.textContent = 'Application Rejected';
        resultMessage.textContent = 'The automated analysis has flagged this application as high risk based on the current financial metrics.';
        statusIcon.className = 'status-icon rejected';
        
        resultBreakdown.innerHTML = `
            <div style="color: #f87171; font-weight: 600; margin-bottom: 0.5rem;">Risk Profile: High</div>
            <p style="font-size: 0.9rem; color: #94a3b8;">Common reasons include low debt-to-income ratio alignment or insufficient credit history duration. Please review the financial attributes.</p>
        `;
    } else {
        resultTitle.textContent = 'System Error';
        resultMessage.textContent = 'Unable to connect to the AWS prediction engine. Please check your network connection or try again later.';
        statusIcon.className = 'status-icon rejected';
    }
}

function closeModal() {
    resultModal.classList.remove('active');
}
