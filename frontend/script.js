// Global variables
let radarCharts = {};

// Initialize Lucide icons
document.addEventListener('DOMContentLoaded', () => {
    lucide.createIcons();
    initializeDashboard();
});

async function analyze() {
    const depsInput = document.getElementById("deps").value.trim();
    const resultsSection = document.getElementById("results");
    const analyzeBtn = document.getElementById("analyze-btn");
    
    if (!depsInput) {
        showError("Please enter at least one dependency to analyze");
        return;
    }
    
    // Clear previous results
    resultsSection.innerHTML = "";
    
    // Set loading state
    analyzeBtn.classList.add("loading");
    analyzeBtn.disabled = true;
    
    try {
        const response = await fetch("http://127.0.0.1:8000/analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ 
                dependencies: depsInput.split("\n").filter(dep => dep.trim()) 
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();
        
        if (!data.dependencies || data.dependencies.length === 0) {
            showError("No dependency data received from server");
            return;
        }
        
        // Render security cards with radar charts
        data.dependencies.forEach((dep, index) => {
            setTimeout(() => {
                const card = createSecurityCard(dep);
                resultsSection.appendChild(card);
                // Initialize radar chart after card is added
                setTimeout(() => createRadarChart(dep), 100);
            }, index * 150);
        });
        
    } catch (error) {
        console.error("Analysis error:", error);
        showError(`Analysis failed: ${error.message}. Please check if backend server is running.`);
    } finally {
        // Reset loading state
        analyzeBtn.classList.remove("loading");
        analyzeBtn.disabled = false;
    }
}

function createSecurityCard(dep) {
    const card = document.createElement("div");
    card.className = `security-card ${dep.status.toLowerCase().replace(" ", "-")}-risk`;
    
    // Determine risk level class
    const riskLevel = getRiskLevel(dep.risk_score);
    
    card.innerHTML = `
        <div class="card-header">
            <h3 class="package-name">${dep.package.toUpperCase()}</h3>
            <span class="status-badge ${riskLevel}">${dep.status}</span>
        </div>
        
        <div class="radar-chart-container">
            <canvas id="radar-${dep.package}" width="200" height="200"></canvas>
        </div>
        
        <div class="risk-meter">
            <div class="risk-meter-label">Risk Assessment</div>
            <div class="risk-bar">
                <div class="risk-fill ${riskLevel}" style="width: 0%"></div>
            </div>
            <div class="risk-score">${dep.risk_score}/100</div>
        </div>
        
        <div class="metrics-grid">
            <div class="metric-item">
                <i data-lucide="star" class="metric-icon"></i>
                <div class="metric-info">
                    <div class="metric-label">Stars</div>
                    <div class="metric-value">${formatNumber(dep.details.stars)}</div>
                </div>
            </div>
            <div class="metric-item">
                <i data-lucide="bug" class="metric-icon"></i>
                <div class="metric-info">
                    <div class="metric-label">CVE Count</div>
                    <div class="metric-value">${dep.details.cve_count}</div>
                </div>
            </div>
            <div class="metric-item">
                <i data-lucide="shield-alert" class="metric-icon"></i>
                <div class="metric-info">
                    <div class="metric-label">Avg CVSS</div>
                    <div class="metric-value">${dep.details.avg_cvss.toFixed(1)}</div>
                </div>
            </div>
            <div class="metric-item">
                <i data-lucide="clock" class="metric-icon"></i>
                <div class="metric-info">
                    <div class="metric-label">Last Updated</div>
                    <div class="metric-value">${formatDays(dep.details.last_updated_days)}</div>
                </div>
            </div>
        </div>
    `;
    
    // Animate risk bar after card is added to DOM
    setTimeout(() => {
        const riskFill = card.querySelector('.risk-fill');
        if (riskFill) {
            riskFill.style.width = `${Math.min(100, Math.max(0, dep.risk_score))}%`;
        }
        // Reinitialize Lucide icons for the new card
        lucide.createIcons();
    }, 100);
    
    return card;
}

function createRadarChart(dep) {
    const canvas = document.getElementById(`radar-${dep.package}`);
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    // Normalize values for radar chart (0-100 scale)
    const maxStars = 100000;
    const maxCves = 50;
    const maxCVSS = 10;
    const maxIssues = 5000;
    const maxDays = 365;
    
    const normalizedStars = Math.min(100, (dep.details.stars / maxStars) * 100);
    const normalizedCves = Math.min(100, (dep.details.cve_count / maxCves) * 100);
    const normalizedCVSS = Math.min(100, (dep.details.avg_cvss / maxCVSS) * 100);
    const normalizedIssues = Math.min(100, (dep.details.open_issues / maxIssues) * 100);
    const normalizedRecency = Math.max(0, 100 - (dep.details.last_updated_days / maxDays) * 100);
    
    // Destroy existing chart if it exists
    if (radarCharts[dep.package]) {
        radarCharts[dep.package].destroy();
    }
    
    radarCharts[dep.package] = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: ['Stars', 'CVEs', 'CVSS', 'Issues', 'Recency'],
            datasets: [{
                label: dep.package.toUpperCase(),
                data: [normalizedStars, normalizedCves, normalizedCVSS, normalizedIssues, normalizedRecency],
                backgroundColor: getRiskLevel(dep.risk_score) === 'high' ? 'rgba(244, 63, 94, 0.2)' :
                             getRiskLevel(dep.risk_score) === 'medium' ? 'rgba(245, 158, 11, 0.2)' :
                             'rgba(16, 185, 129, 0.2)',
                borderColor: getRiskLevel(dep.risk_score) === 'high' ? '#f43f5e' :
                           getRiskLevel(dep.risk_score) === 'medium' ? '#f59e0b' :
                           '#10b981',
                borderWidth: 2,
                pointBackgroundColor: getRiskLevel(dep.risk_score) === 'high' ? '#f43f5e' :
                                  getRiskLevel(dep.risk_score) === 'medium' ? '#f59e0b' :
                                  '#10b981',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: getRiskLevel(dep.risk_score) === 'high' ? '#f43f5e' :
                                       getRiskLevel(dep.risk_score) === 'medium' ? '#f59e0b' :
                                       '#10b981'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        stepSize: 20,
                        color: '#94a3b8',
                        backdropColor: 'transparent'
                    },
                    grid: {
                        color: 'rgba(148, 163, 184, 0.1)'
                    },
                    pointLabels: {
                        color: '#f1f5f9',
                        font: {
                            size: 10,
                            family: 'Inter'
                        }
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(15, 23, 42, 0.9)',
                    titleColor: '#f1f5f9',
                    bodyColor: '#94a3b8',
                    borderColor: 'rgba(255, 255, 255, 0.1)',
                    borderWidth: 1
                }
            }
        }
    });
}

function initializeDashboard() {
    const depsTextarea = document.getElementById('deps');

    // 🔥 AUTO EXPAND LOGIC
    const autoResize = () => {
        depsTextarea.style.height = 'auto';
        depsTextarea.style.height = depsTextarea.scrollHeight + 'px';
    };

    // Run once (for default values)
    autoResize();

    // Run on input
    depsTextarea.addEventListener('input', autoResize);

    // Keyboard shortcut (already present)
    depsTextarea.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            e.preventDefault();
            analyze();
        }
    });

    // Default example text
    if (!depsTextarea.value) {
        depsTextarea.value = "numpy\npandas\nrequests\nflask";
        autoResize(); // adjust height after setting default
    }
}

function getRiskLevel(score) {
    if (score < 30) return "low";
    if (score < 70) return "medium";
    return "high";
}

function formatNumber(num) {
    if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
    if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
    return num.toString();
}

function formatDays(days) {
    if (days === 0) return "Today";
    if (days === 1) return "Yesterday";
    if (days < 7) return `${days} days ago`;
    if (days < 30) return `${Math.floor(days / 7)} weeks ago`;
    if (days < 365) return `${Math.floor(days / 30)} months ago`;
    return `${Math.floor(days / 365)} years ago`;
}

function showError(message) {
    const toastContainer = document.getElementById("toast-container");
    
    // Remove existing toasts
    const existingToasts = toastContainer.querySelectorAll('.error-toast');
    existingToasts.forEach(toast => toast.remove());
    
    const toast = document.createElement("div");
    toast.className = "error-toast";
    toast.innerHTML = `
        <i data-lucide="alert-triangle" class="toast-icon"></i>
        <span class="toast-message">${message}</span>
    `;
    
    toastContainer.appendChild(toast);
    
    // Reinitialize Lucide icons
    lucide.createIcons();
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        toast.style.animation = "slideInRight 0.3s ease-out reverse";
        setTimeout(() => toast.remove(), 300);
    }, 5000);
    
    // Allow manual dismissal
    toast.addEventListener('click', () => {
        toast.style.animation = "slideInRight 0.3s ease-out reverse";
        setTimeout(() => toast.remove(), 300);
    });
}