// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const alertContainer = document.getElementById('alertContainer');
const resultsContainer = document.getElementById('resultsContainer');

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    setupUploadArea();
});

function setupUploadArea() {
    // Click to upload
    uploadArea.addEventListener('click', () => {
        fileInput.click();
    });

    // File input change
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            uploadFile(e.target.files[0]);
        }
    });

    // Drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            uploadFile(files[0]);
        }
    });
}

function uploadFile(file) {
    if (!file.name.toLowerCase().endsWith('.csv')) {
        showAlert('Lütfen .csv dosyası seçin!', 'danger');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    showAlert('Dosya yükleniyor...', 'info');

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showAlert(data.message, 'success');
            analyzeData();
        } else {
            showAlert(data.message, 'danger');
        }
    })
    .catch(error => {
        showAlert('Dosya yükleme hatası: ' + error.message, 'danger');
    });
}

function analyzeData() {
    showAlert('Veriler analiz ediliyor...', 'info');

    fetch('/analyze')
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showAlert('Analiz tamamlandı!', 'success');
            displayResults(data.data);
        } else {
            showAlert(data.message, 'danger');
        }
    })
    .catch(error => {
        showAlert('Analiz hatası: ' + error.message, 'danger');
    });
}

function displayResults(data) {
    resultsContainer.style.display = 'block';
    resultsContainer.classList.add('fade-in');

    // Özet istatistikleri göster
    displaySummaryStats(data.summary);
    
    // Case süre analizini göster
    displayCaseDurationAnalysis(data.case_durations);
    
    // Aktivite frekanslarını göster
    displayActivityFrequency(data.activity_frequency);
    
    // Geçiş analizini göster
    displayTransitionAnalysis(data.transitions);
    
    // Grafikleri göster
    displayCharts(data.charts);
    
    // Case süre tablosunu göster
    displayCaseDurationTable(data.case_durations.data);
}

function displaySummaryStats(summary) {
    const container = document.getElementById('summaryStats');
    container.innerHTML = `
        <div class="col-md-3">
            <div class="stat-card">
                <h3>${summary.total_cases}</h3>
                <p>Toplam Case</p>
            </div>
        </div>
        <div class="col-md-3">
            <div class="stat-card">
                <h3>${summary.total_activities}</h3>
                <p>Toplam Aktivite</p>
            </div>
        </div>
        <div class="col-md-3">
            <div class="stat-card">
                <h3>${summary.unique_activities}</h3>
                <p>Benzersiz Aktivite</p>
            </div>
        </div>
        <div class="col-md-3">
            <div class="stat-card">
                <h3>${Math.round((new Date(summary.date_range.end) - new Date(summary.date_range.start)) / (1000 * 60 * 60 * 24))}</h3>
                <p>Gün Aralığı</p>
            </div>
        </div>
    `;
}

function displayCaseDurationAnalysis(caseData) {
    const container = document.getElementById('caseDurationStats');
    container.innerHTML = `
        <div class="row">
            <div class="col-md-4">
                <div class="text-center">
                    <h6>Ortalama Süre</h6>
                    <h4 class="text-primary">${Math.round(caseData.avg_duration)} dk</h4>
                </div>
            </div>
            <div class="col-md-4">
                <div class="text-center">
                    <h6>Minimum Süre</h6>
                    <h4 class="text-success">${Math.round(caseData.min_duration)} dk</h4>
                </div>
            </div>
            <div class="col-md-4">
                <div class="text-center">
                    <h6>Maksimum Süre</h6>
                    <h4 class="text-danger">${Math.round(caseData.max_duration)} dk</h4>
                </div>
            </div>
        </div>
    `;
}

function displayActivityFrequency(activityData) {
    const container = document.getElementById('activityStats');
    const activities = Object.entries(activityData.data).slice(0, 5);
    
    let html = '<h6>En Sık Aktiviteler</h6>';
    activities.forEach(([activity, count], index) => {
        html += `
            <div class="d-flex justify-content-between align-items-center mb-2">
                <span>${activity}</span>
                <span class="badge bg-primary">${count}</span>
            </div>
        `;
    });
    
    container.innerHTML = html;
}

function displayTransitionAnalysis(transitionData) {
    const container = document.getElementById('transitionsList');
    const transitions = Object.entries(transitionData.data).slice(0, 10);
    
    let html = '';
    transitions.forEach(([transition, count]) => {
        html += `
            <div class="transition-item">
                <div class="d-flex justify-content-between">
                    <span>${transition}</span>
                    <span class="transition-count">${count}</span>
                </div>
            </div>
        `;
    });
    
    container.innerHTML = html;
}

function displayCharts(charts) {
    // Aktivite grafiği
    document.getElementById('activityChart').innerHTML = charts.activity_chart;
    
    // Süre dağılım grafiği
    document.getElementById('durationChart').innerHTML = charts.duration_chart;
    
    // Süreç akış diyagramı
    document.getElementById('processFlow').innerHTML = charts.process_flow;
}

function displayCaseDurationTable(caseData) {
    const tbody = document.querySelector('#caseDurationTable tbody');
    tbody.innerHTML = '';
    
    caseData.forEach(row => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${row['Case ID']}</td>
            <td>${Math.round(row['Total Duration (minutes)'])}</td>
        `;
        tbody.appendChild(tr);
    });
}

function downloadSample() {
    fetch('/download_sample')
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showAlert(data.message, 'success');
        } else {
            showAlert(data.message, 'danger');
        }
    })
    .catch(error => {
        showAlert('Örnek dosya indirme hatası: ' + error.message, 'danger');
    });
}

function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    alertContainer.innerHTML = '';
    alertContainer.appendChild(alertDiv);
    
    // Auto dismiss after 5 seconds for success messages
    if (type === 'success') {
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }
}
