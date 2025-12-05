// TRUTH - Fake News Detection System Frontend

const API_BASE = '/api';

// DOM Elements
const contentInput = document.getElementById('content');
const sourceUrlInput = document.getElementById('source-url');
const authorInput = document.getElementById('author');
const analyzeBtn = document.getElementById('analyze-btn');
const extractClaimsBtn = document.getElementById('extract-claims-btn');
const loadingDiv = document.getElementById('loading');
const resultsDiv = document.getElementById('results');
const errorDiv = document.getElementById('error');
const charCount = document.getElementById('char-count');

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    analyzeBtn.addEventListener('click', analyzeContent);
    extractClaimsBtn.addEventListener('click', extractClaims);
    document.getElementById('close-results').addEventListener('click', closeResults);
    document.getElementById('close-error').addEventListener('click', closeError);
    
    // Tab switching
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', switchTab);
    });
    
    // Character count
    contentInput.addEventListener('input', updateCharCount);
});

function updateCharCount() {
    charCount.textContent = contentInput.value.length;
}

async function analyzeContent() {
    const content = contentInput.value.trim();
    
    if (!content) {
        showError('Please enter news content to analyze');
        return;
    }
    
    if (content.length < 10) {
        showError('Content must be at least 10 characters long');
        return;
    }
    
    showLoading();
    closeError();
    
    try {
        const payload = {
            content: content,
            source_url: sourceUrlInput.value || null,
            author: authorInput.value || null
        };
        
        const response = await fetch(`${API_BASE}/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Analysis failed');
        }
        
        displayResults(data.analysis);
        hideLoading();
    } catch (error) {
        console.error('Analysis error:', error);
        showError(`Analysis failed: ${error.message}`);
        hideLoading();
    }
}

async function extractClaims() {
    const content = contentInput.value.trim();
    
    if (!content) {
        showError('Please enter news content first');
        return;
    }
    
    showLoading();
    closeError();
    
    try {
        const response = await fetch(`${API_BASE}/extract-claims`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ content: content })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Claim extraction failed');
        }
        
        hideLoading();
        showInfo(`Extracted ${data.count} claims. Analyze the content to see detailed verification.`);
    } catch (error) {
        console.error('Extraction error:', error);
        showError(`Claim extraction failed: ${error.message}`);
        hideLoading();
    }
}

function displayResults(analysis) {
    const score = Math.round(analysis.overall_score * 100);
    
    // Update overall score
    document.getElementById('score-value').textContent = `${score}%`;
    document.getElementById('score-fill').style.width = `${score}%`;
    document.getElementById('recommendation').textContent = analysis.recommendation;
    
    // Content tab
    displayContentAnalysis(analysis.content_analysis);
    
    // Source tab
    displaySourceAnalysis(analysis.source_analysis);
    
    // Fact check tab
    displayFactCheck(analysis.fact_check);
    
    // Linguistic tab
    displayLinguisticAnalysis(analysis.content_analysis);
    
    // Show results
    resultsDiv.classList.remove('hidden');
    resultsDiv.scrollIntoView({ behavior: 'smooth' });
}

function displayContentAnalysis(content) {
    const container = document.getElementById('content-details');
    container.innerHTML = '';
    
    if (!content || content.error) {
        container.innerHTML = '<p>Unable to analyze content</p>';
        return;
    }
    
    const items = [
        {
            label: 'ML Prediction',
            value: content.ml_prediction ? content.ml_prediction.toUpperCase() : 'N/A',
            className: content.ml_prediction === 'real' ? 'positive' : 'negative'
        },
        {
            label: 'Confidence',
            value: `${Math.round(content.ml_confidence * 100)}%`,
            className: content.ml_confidence > 0.7 ? 'positive' : 'neutral'
        },
        {
            label: 'Sentiment',
            value: content.sentiment?.sentiment || 'N/A',
            className: 'neutral'
        },
        {
            label: 'Sensationalism Score',
            value: `${Math.round(content.sensationalism_score || 0)}%`,
            className: (content.sensationalism_score || 0) > 50 ? 'negative' : 'positive'
        },
        {
            label: 'Readability',
            value: `${Math.round(content.readability_score || 0)}%`,
            className: 'neutral'
        },
        {
            label: 'Word Count',
            value: content.text_statistics?.word_count || 'N/A',
            className: 'neutral'
        }
    ];
    
    items.forEach(item => {
        container.innerHTML += `
            <div class="detail-item">
                <div class="detail-label">${item.label}</div>
                <div class="detail-value ${item.className}">${item.value}</div>
            </div>
        `;
    });
}

function displaySourceAnalysis(source) {
    const container = document.getElementById('source-details');
    container.innerHTML = '';
    
    if (!source) {
        container.innerHTML = '<p>No source information provided</p>';
        return;
    }
    
    const credibleClass = source.credible ? 'positive' : (source.credible === false ? 'negative' : 'neutral');
    
    const items = [
        {
            label: 'URL',
            value: source.url || 'Not provided',
            className: 'neutral'
        },
        {
            label: 'Credibility',
            value: source.credible ? 'CREDIBLE' : (source.credible === false ? 'NOT CREDIBLE' : 'UNKNOWN'),
            className: credibleClass
        },
        {
            label: 'Score',
            value: `${Math.round(source.score * 100)}%`,
            className: credibleClass
        },
        {
            label: 'Reason',
            value: source.reason || 'N/A',
            className: 'neutral'
        }
    ];
    
    items.forEach(item => {
        container.innerHTML += `
            <div class="detail-item">
                <div class="detail-label">${item.label}</div>
                <div class="detail-value ${item.className}">${item.value}</div>
            </div>
        `;
    });
}

function displayFactCheck(factCheck) {
    const container = document.getElementById('fact-check-details');
    const claimsList = document.getElementById('claims-list');
    container.innerHTML = '';
    claimsList.innerHTML = '';
    
    if (!factCheck) {
        container.innerHTML = '<p>No fact-check data available</p>';
        return;
    }
    
    const scoreClass = factCheck.score >= 0.7 ? 'positive' : (factCheck.score >= 0.4 ? 'neutral' : 'negative');
    
    container.innerHTML = `
        <div class="detail-item">
            <div class="detail-label">Fact Check Score</div>
            <div class="detail-value ${scoreClass}">${Math.round(factCheck.score * 100)}%</div>
        </div>
        <div class="detail-item">
            <div class="detail-label">Claims Analyzed</div>
            <div class="detail-value">${factCheck.claims_checked || 0}</div>
        </div>
        <div class="detail-item">
            <div class="detail-label">Verified Claims</div>
            <div class="detail-value">${(factCheck.verified_claims || []).length}</div>
        </div>
    `;
    
    if (factCheck.verified_claims && factCheck.verified_claims.length > 0) {
        factCheck.verified_claims.forEach(claim => {
            const verdictClass = claim.verdict.toLowerCase();
            claimsList.innerHTML += `
                <div class="claim-item">
                    <h4>"${claim.claim}"</h4>
                    <p>${claim.explanation}</p>
                    <span class="claim-verdict ${verdictClass}">${claim.verdict}</span>
                    <div style="margin-top: 0.5rem; font-size: 0.9rem; color: var(--text-light);">
                        Confidence: ${Math.round(claim.confidence * 100)}%
                    </div>
                </div>
            `;
        });
    }
}

function displayLinguisticAnalysis(content) {
    const container = document.getElementById('linguistic-details');
    container.innerHTML = '';
    
    if (!content || !content.language_patterns) {
        container.innerHTML = '<p>Unable to analyze linguistic patterns</p>';
        return;
    }
    
    const patterns = content.language_patterns;
    
    const items = [
        {
            label: 'Exclamation Marks',
            value: patterns.exclamation_count || 0,
            className: 'neutral'
        },
        {
            label: 'Question Marks',
            value: patterns.question_count || 0,
            className: 'neutral'
        },
        {
            label: 'CAPS Usage',
            value: `${Math.round(patterns.caps_percentage || 0)}%`,
            className: (patterns.caps_percentage || 0) > 10 ? 'negative' : 'positive'
        },
        {
            label: 'Quotation Marks',
            value: patterns.quotation_count || 0,
            className: 'neutral'
        },
        {
            label: 'Source References',
            value: patterns.has_sources || 0,
            className: (patterns.has_sources || 0) > 0 ? 'positive' : 'negative'
        },
        {
            label: 'Sensational Words',
            value: patterns.sensational_words || 0,
            className: (patterns.sensational_words || 0) > 0 ? 'negative' : 'positive'
        }
    ];
    
    items.forEach(item => {
        container.innerHTML += `
            <div class="detail-item">
                <div class="detail-label">${item.label}</div>
                <div class="detail-value ${item.className}">${item.value}</div>
            </div>
        `;
    });
}

function switchTab(e) {
    const tabName = e.target.dataset.tab;
    
    // Remove active class from all tabs and buttons
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Add active class to clicked tab and button
    document.getElementById(`${tabName}-tab`).classList.add('active');
    e.target.classList.add('active');
}

function showLoading() {
    loadingDiv.classList.remove('hidden');
    resultsDiv.classList.add('hidden');
    errorDiv.classList.add('hidden');
}

function hideLoading() {
    loadingDiv.classList.add('hidden');
}

function closeResults() {
    resultsDiv.classList.add('hidden');
}

function closeError() {
    errorDiv.classList.add('hidden');
}

function showError(message) {
    document.getElementById('error-message').textContent = message;
    errorDiv.classList.remove('hidden');
}

function showInfo(message) {
    // Show as a temporary message (can be enhanced with a toast)
    alert(message);
}
