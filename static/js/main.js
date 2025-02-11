// Form submission handler
async function submitPatientForm(event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);

    try {
        const response = await fetch('/api/patients', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (result.success) {
            showAlert('success', 'Patient added successfully');
            form.reset();
            searchPatients('');
        } else {
            showAlert('danger', result.message);
        }
    } catch (error) {
        showAlert('danger', 'Error adding patient');
    }
}

// Search functionality
async function searchPatients(query) {
    try {
        const response = await fetch(`/api/patients/search?query=${encodeURIComponent(query)}`);
        const patients = await response.json();
        displaySearchResults(patients);
    } catch (error) {
        showAlert('danger', 'Error searching patients');
    }
}

// Display search results
function displaySearchResults(patients) {
    const resultsContainer = document.getElementById('searchResults');

    if (patients.length === 0) {
        resultsContainer.innerHTML = '<p class="text-muted">No patients found</p>';
        return;
    }

    const html = patients.map(patient => `
        <div class="card mb-3">
            <div class="card-body">
                <h5 class="card-title">${patient.name}</h5>
                <h6 class="card-subtitle mb-2 text-muted">ID: ${patient.patient_id}</h6>
                <p class="card-text">
                    Age: ${patient.age}<br>
                    Location: ${patient.location}<br>
                    Date: ${patient.date}
                </p>
                ${patient.ocr_text ? `
                    <div class="mt-3">
                        <h6>Extracted Text from Document:</h6>
                        <p class="text-muted">${patient.ocr_text}</p>
                    </div>
                ` : ''}
            </div>
        </div>
    `).join('');

    resultsContainer.innerHTML = html;
}

// OCR document processing
async function processDocument(event) {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    showLoading(true);

    try {
        const response = await fetch('/api/ocr', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (result.success) {
            document.getElementById('ocrResult').value = result.text;
        } else {
            showAlert('danger', result.message);
        }
    } catch (error) {
        showAlert('danger', 'Error processing document');
    } finally {
        showLoading(false);
    }
}

// Utility functions
function showAlert(type, message) {
    const alertContainer = document.getElementById('alertContainer');
    alertContainer.innerHTML = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
}

function showLoading(show) {
    const loader = document.getElementById('loader');
    loader.style.display = show ? 'block' : 'none';
}

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('patientForm').addEventListener('submit', submitPatientForm);
    document.getElementById('searchInput').addEventListener('input', (e) => searchPatients(e.target.value));
    document.getElementById('documentUpload').addEventListener('change', processDocument);
});