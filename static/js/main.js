// Global variables
let selectedSkills = [];

// DOM elements
const skillInput = document.getElementById('skillInput');
const skillTags = document.getElementById('skillTags');
const skillsHidden = document.getElementById('skills');
const form = document.getElementById('recommendationForm');
const submitBtn = document.getElementById('submitBtn');
const spinner = document.getElementById('spinner');
const resultsSection = document.getElementById('resultsSection');
const recommendationCards = document.getElementById('recommendationCards');
const loadingOverlay = document.getElementById('loadingOverlay');
const errorModal = document.getElementById('errorModal');
const errorMessage = document.getElementById('errorMessage');

// Initialize the app
document.addEventListener('DOMContentLoaded', function() {
    initializeSkillInput();
    initializeSkillSuggestions();
    initializeForm();
    initializeLanguageSelector();
});

// Skills management
function initializeSkillInput() {
    if (!skillInput) return;
    
    skillInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            addSkill(this.value.trim());
            this.value = '';
        }
    });

    skillInput.addEventListener('blur', function() {
        if (this.value.trim()) {
            addSkill(this.value.trim());
            this.value = '';
        }
    });
}

function initializeSkillSuggestions() {
    const suggestions = document.querySelectorAll('.skill-suggestion');
    suggestions.forEach(suggestion => {
        suggestion.addEventListener('click', function() {
            const skill = this.getAttribute('data-skill');
            addSkill(skill);
        });
    });
}

function addSkill(skill) {
    if (!skill || selectedSkills.includes(skill)) return;
    
    selectedSkills.push(skill);
    updateSkillTags();
    updateSkillsHidden();
}

function removeSkill(skill) {
    selectedSkills = selectedSkills.filter(s => s !== skill);
    updateSkillTags();
    updateSkillsHidden();
}

function updateSkillTags() {
    if (!skillTags) return;
    
    skillTags.innerHTML = selectedSkills.map(skill => `
        <div class="skill-tag fade-in-up">
            <span>${skill}</span>
            <button type="button" class="remove-skill" onclick="removeSkill('${skill}')">&times;</button>
        </div>
    `).join('');
}

function updateSkillsHidden() {
    if (skillsHidden) {
        skillsHidden.value = JSON.stringify(selectedSkills);
    }
}

// Form handling
function initializeForm() {
    if (!form) return;
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        handleFormSubmit();
    });
}

async function handleFormSubmit() {
    // Validate form
    if (!validateForm()) return;
    
    // Show loading state
    setLoadingState(true);
    
    // Collect form data
    const formData = collectFormData();
    
    try {
        // Make API request
        const response = await fetch('/api/recommendations', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to get recommendations');
        }
        
        // Display results
        displayRecommendations(data.recommendations);
        
    } catch (error) {
        console.error('Error:', error);
        showError(error.message || 'Failed to get recommendations. Please try again.');
    } finally {
        setLoadingState(false);
    }
}

function validateForm() {
    const education = document.getElementById('education').value;
    const sector = document.getElementById('sector').value;
    const location = document.getElementById('location').value;
    
    if (!education) {
        showError('Please select your education background');
        return false;
    }
    
    if (!sector) {
        showError('Please select your preferred sector');
        return false;
    }
    
    if (!location) {
        showError('Please select your preferred location');
        return false;
    }
    
    if (selectedSkills.length === 0) {
        showError('Please add at least one skill');
        return false;
    }
    
    return true;
}

function collectFormData() {
    return {
        education: document.getElementById('education').value,
        skills: selectedSkills,
        sector: document.getElementById('sector').value,
        location: document.getElementById('location').value
    };
}

function setLoadingState(loading) {
    if (loading) {
        submitBtn.disabled = true;
        submitBtn.querySelector('span') && (submitBtn.querySelector('span').textContent = 'Finding Matches...');
        spinner.classList.add('active');
        loadingOverlay.classList.remove('hidden');
    } else {
        submitBtn.disabled = false;
        submitBtn.querySelector('span') && (submitBtn.querySelector('span').textContent = 'Get My Recommendations');
        spinner.classList.remove('active');
        loadingOverlay.classList.add('hidden');
    }
}

// Results display
function displayRecommendations(recommendations) {
    if (!recommendationCards || !resultsSection) return;
    
    // Update results subtitle
    const resultsSubtitle = document.getElementById('resultsSubtitle');
    if (resultsSubtitle) {
        resultsSubtitle.textContent = `We found ${recommendations.length} perfect matches for you!`;
    }
    
    // Generate cards HTML
    recommendationCards.innerHTML = recommendations.map((internship, index) => 
        createRecommendationCard(internship, index)
    ).join('');
    
    // Show results section with animation
    resultsSection.classList.remove('hidden');
    resultsSection.scrollIntoView({ behavior: 'smooth' });
    
    // Add staggered animation to cards
    const cards = recommendationCards.querySelectorAll('.recommendation-card');
    cards.forEach((card, index) => {
        setTimeout(() => {
            card.classList.add('fade-in-up');
        }, index * 150);
    });
}

function createRecommendationCard(internship, index) {
    const matchScore = calculateDisplayScore(internship.match_score || 0);
    const stars = generateStars(internship.rating || 0);
    
    return `
        <div class="recommendation-card" style="animation-delay: ${index * 0.1}s">
            <div class="card-header">
                <div>
                    <h3 class="card-title">${internship.title}</h3>
                    <p class="card-company">${internship.company}</p>
                </div>
                <div class="card-match">${matchScore}% Match</div>
            </div>
            
            <div class="card-details">
                <div class="card-detail">
                    <i class="fas fa-industry"></i>
                    <span>${internship.sector}</span>
                </div>
                <div class="card-detail">
                    <i class="fas fa-map-marker-alt"></i>
                    <span>${internship.location}</span>
                </div>
                <div class="card-detail">
                    <i class="fas fa-clock"></i>
                    <span>${internship.duration}</span>
                </div>
                <div class="card-detail">
                    <i class="fas fa-rupee-sign"></i>
                    <span>${internship.stipend}</span>
                </div>
            </div>
            
            <div class="card-description">
                ${internship.description}
            </div>
            
            <div class="card-skills">
                <h4>Skills Required:</h4>
                <div class="skill-chips">
                    ${internship.skills_required.map(skill => 
                        `<span class="skill-chip">${skill}</span>`
                    ).join('')}
                </div>
            </div>
            
            <div class="card-footer">
                <div class="card-rating">
                    <span class="rating-stars">${stars}</span>
                    <span>${internship.rating}/5</span>
                </div>
                <div class="card-opportunities">
                    ${internship.opportunities} positions
                </div>
            </div>
        </div>
    `;
}

function calculateDisplayScore(score) {
    // Convert internal score to percentage (0-100)
    const percentage = Math.min(Math.max(Math.round((score / 15) * 100), 60), 99);
    return percentage;
}

function generateStars(rating) {
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 >= 0.5;
    let stars = '';
    
    for (let i = 0; i < fullStars; i++) {
        stars += '★';
    }
    
    if (hasHalfStar) {
        stars += '☆';
    }
    
    for (let i = fullStars + (hasHalfStar ? 1 : 0); i < 5; i++) {
        stars += '☆';
    }
    
    return stars;
}

// Error handling
function showError(message) {
    if (errorMessage && errorModal) {
        errorMessage.textContent = message;
        errorModal.classList.remove('hidden');
    } else {
        alert(message);
    }
}

function closeModal() {
    if (errorModal) {
        errorModal.classList.add('hidden');
    }
}

// Language selector (basic structure for future implementation)
function initializeLanguageSelector() {
    const languageSelect = document.getElementById('languageSelect');
    if (languageSelect) {
        languageSelect.addEventListener('change', function() {
            // Future: Implement language switching
            console.log('Language switched to:', this.value);
        });
    }
}

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Close modal when clicking outside
document.addEventListener('click', function(e) {
    if (e.target === errorModal) {
        closeModal();
    }
});

// Close modal on escape key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && !errorModal.classList.contains('hidden')) {
        closeModal();
    }
});

// Smooth scroll polyfill for older browsers
if (!window.CSS || !CSS.supports('scroll-behavior', 'smooth')) {
    const smoothScrollPolyfill = document.createElement('script');
    smoothScrollPolyfill.src = 'https://cdn.jsdelivr.net/gh/iamdustan/smoothscroll@1.4.10/src/smoothscroll.js';
    document.head.appendChild(smoothScrollPolyfill);
}

// Performance optimization: Lazy load animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('fade-in-up');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Observe elements for animation when they come into view
document.addEventListener('DOMContentLoaded', function() {
    const animatableElements = document.querySelectorAll('.form-group, .hero');
    animatableElements.forEach(el => observer.observe(el));
});