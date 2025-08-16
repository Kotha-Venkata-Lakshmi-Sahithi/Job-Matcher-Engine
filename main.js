// Main JavaScript file for the Job Recommendation Engine

document.addEventListener('DOMContentLoaded', function() {
    // Initialize form validation and interactions
    initializeFormValidation();
    initializeInteractiveElements();
});

function initializeFormValidation() {
    const form = document.getElementById('preferencesForm');
    if (!form) return;
    
    form.addEventListener('submit', function(e) {
        const checkedInputs = form.querySelectorAll('input[type="checkbox"]:checked');
        
        if (checkedInputs.length === 0) {
            e.preventDefault();
            showAlert('Please select at least one preference to get job recommendations.', 'warning');
            return false;
        }
        
        // Show loading state
        const submitBtn = form.querySelector('button[type="submit"]');
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Finding Your Jobs...';
        }
    });
}

function initializeInteractiveElements() {
    // Add hover effects to job cards
    const jobCards = document.querySelectorAll('.card');
    jobCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.classList.add('shadow-lg');
            this.style.transform = 'translateY(-2px)';
            this.style.transition = 'all 0.3s ease';
        });
        
        card.addEventListener('mouseleave', function() {
            this.classList.remove('shadow-lg');
            this.style.transform = 'translateY(0)';
        });
    });
    
    // Add click handlers for preference sections
    const sectionHeaders = document.querySelectorAll('.form-label.fw-semibold');
    sectionHeaders.forEach(header => {
        header.style.cursor = 'pointer';
        header.addEventListener('click', function() {
            const section = this.closest('.mb-4');
            const checkboxes = section.querySelectorAll('input[type="checkbox"]');
            const allChecked = Array.from(checkboxes).every(cb => cb.checked);
            
            checkboxes.forEach(cb => {
                cb.checked = !allChecked;
            });
        });
    });
}

function showAlert(message, type = 'info') {
    const alertContainer = document.createElement('div');
    alertContainer.className = `alert alert-${type} alert-dismissible fade show`;
    alertContainer.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    container.insertBefore(alertContainer, container.firstChild);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        if (alertContainer.parentNode) {
            alertContainer.remove();
        }
    }, 5000);
}

// Utility functions for job recommendations page
function filterJobs(filterType, filterValue) {
    const jobCards = document.querySelectorAll('[data-job-card]');
    
    jobCards.forEach(card => {
        const jobData = JSON.parse(card.dataset.jobData);
        let shouldShow = true;
        
        switch(filterType) {
            case 'minScore':
                shouldShow = jobData.match_score >= parseInt(filterValue);
                break;
            case 'location':
                shouldShow = filterValue === 'all' || jobData.location.toLowerCase().includes(filterValue.toLowerCase());
                break;
            case 'salary':
                const minSalary = parseInt(filterValue);
                shouldShow = !minSalary || (jobData.salary_range && jobData.salary_range[0] >= minSalary);
                break;
        }
        
        card.style.display = shouldShow ? 'block' : 'none';
    });
}

// Search functionality
function searchJobs(query) {
    const jobCards = document.querySelectorAll('[data-job-card]');
    const lowercaseQuery = query.toLowerCase();
    
    jobCards.forEach(card => {
        const jobData = JSON.parse(card.dataset.jobData);
        const searchText = `${jobData.job_title} ${jobData.company} ${jobData.location}`.toLowerCase();
        
        const shouldShow = searchText.includes(lowercaseQuery);
        card.style.display = shouldShow ? 'block' : 'none';
    });
}

// Copy job link functionality
function copyJobLink(jobId) {
    const url = `${window.location.origin}/job/${jobId}`;
    navigator.clipboard.writeText(url).then(() => {
        showAlert('Job link copied to clipboard!', 'success');
    }).catch(() => {
        showAlert('Failed to copy link', 'error');
    });
}

// Export recommendations as JSON
function exportRecommendations() {
    const recommendations = window.jobData || [];
    const dataStr = JSON.stringify(recommendations, null, 2);
    const dataBlob = new Blob([dataStr], {type: 'application/json'});
    
    const link = document.createElement('a');
    link.href = URL.createObjectURL(dataBlob);
    link.download = 'job_recommendations.json';
    link.click();
    
    showAlert('Recommendations exported successfully!', 'success');
}

// Progressive enhancement for form inputs
document.querySelectorAll('input[type="number"]').forEach(input => {
    input.addEventListener('input', function() {
        // Format salary input with commas
        if (this.name === 'min_salary' && this.value) {
            const numValue = parseInt(this.value.replace(/,/g, ''));
            if (!isNaN(numValue)) {
                this.dataset.value = numValue;
            }
        }
    });
});

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + Enter to submit form
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        const form = document.getElementById('preferencesForm');
        if (form) {
            form.submit();
        }
    }
    
    // Escape to close modals
    if (e.key === 'Escape') {
        const openModal = document.querySelector('.modal.show');
        if (openModal) {
            const modal = bootstrap.Modal.getInstance(openModal);
            if (modal) {
                modal.hide();
            }
        }
    }
});
