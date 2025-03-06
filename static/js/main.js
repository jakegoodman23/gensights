document.addEventListener('DOMContentLoaded', function () {
  // DOM Elements
  const customerContainer = document.querySelector('.customer-container');
  const customerSelect = document.getElementById('customerSelect');
  const loadCustomerBtn = document.getElementById('loadCustomerBtn');
  const selectionContent = document.querySelector('.selection-content');
  const loadingContainer = document.querySelector('.loading-container');
  const progressBar = document.getElementById('progressBar');
  const uploadStatus = document.getElementById('uploadStatus');
  const errorToast = document.getElementById('errorToast');
  const successToast = document.getElementById('successToast');
  const errorMessage = document.getElementById('errorMessage');
  const successMessage = document.getElementById('successMessage');

  // Add Marked.js library for markdown rendering
  const markedScript = document.createElement('script');
  markedScript.src = 'https://cdn.jsdelivr.net/npm/marked/marked.min.js';
  document.head.appendChild(markedScript);

  // Handle analyze customer data button click
  loadCustomerBtn.addEventListener('click', function () {
    const selectedCustomer = customerSelect.value;

    if (!selectedCustomer) {
      showError('Please select a customer');
      return;
    }

    loadCustomerData(selectedCustomer);
  });

  // Load the sample data for the selected customer
  function loadCustomerData(customerId) {
    // Show progress UI
    selectionContent.style.display = 'none';
    loadingContainer.style.display = 'block';

    // Update progress status
    uploadStatus.textContent = 'Loading customer data...';

    // Simulate loading progress
    let progress = 0;
    const progressInterval = setInterval(() => {
      progress += 5;
      progressBar.style.width = `${Math.min(progress, 100)}%`;

      if (progress >= 100) {
        clearInterval(progressInterval);

        // After simulated loading, fetch sample data and directly start analysis
        startAnalysisWithCustomerData(customerId);
      }
    }, 50);
  }

  // Fetch sample data and start analysis directly
  function startAnalysisWithCustomerData(customerId) {
    fetch('/use_sample_data', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ customer_id: customerId }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          const customerName =
            customerSelect.options[customerSelect.selectedIndex].text;
          showSuccess(`Loaded data for ${customerName}`);

          // Start analysis immediately instead of showing file info
          startAnalysis();
        } else {
          resetSelectionUI();
          showError(data.error || 'An error occurred');
        }
      })
      .catch((error) => {
        resetSelectionUI();
        showError('Network error: ' + error.message);
      });
  }

  // Function to start the analysis process
  function startAnalysis() {
    // Create a modal to show the analysis is in progress
    const modal = document.createElement('div');
    modal.className = 'analysis-modal';
    modal.innerHTML = `
        <div class="analysis-modal-content">
            <h2><i class="fas fa-robot"></i> Analyzing Data</h2>
            <p>Please wait while we process your data and generate insights. This may take a minute or two.</p>
            <div class="analysis-progress">
                <div class="analysis-progress-bar"></div>
            </div>
            <p class="analysis-steps">
                <span class="step active">Processing data</span>
                <span class="step">Generating insights</span>
                <span class="step">Creating PDF report</span>
            </p>
        </div>
    `;
    document.body.appendChild(modal);

    // Simulate progress for better UX
    const progressBar = modal.querySelector('.analysis-progress-bar');
    const steps = modal.querySelectorAll('.step');
    let progress = 0;

    const progressInterval = setInterval(() => {
      progress += 1;
      progressBar.style.width = `${Math.min(progress, 95)}%`;

      // Update steps
      if (progress > 30 && progress <= 60) {
        steps[0].classList.remove('active');
        steps[1].classList.add('active');
      } else if (progress > 60) {
        steps[1].classList.remove('active');
        steps[2].classList.add('active');
      }

      if (progress >= 95) {
        clearInterval(progressInterval);
      }
    }, 300);

    // Send the analysis request
    fetch('/analyze', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then((response) => response.json())
      .then((data) => {
        // Clear the progress interval
        clearInterval(progressInterval);

        // Remove the modal
        document.body.removeChild(modal);

        if (data.success) {
          // Create a results modal
          const resultsModal = document.createElement('div');
          resultsModal.className = 'results-modal';
          resultsModal.innerHTML = `
                <div class="results-modal-content">
                    <span class="close-modal">&times;</span>
                    <h2>Analysis Results</h2>
                    <div class="results-tabs">
                        <button class="tab-btn active" data-tab="insights">Insights</button>
                        <button class="tab-btn" data-tab="download">Download Report</button>
                    </div>
                    <div class="tab-content active" id="insights-tab">
                        <div class="insights-content"></div>
                    </div>
                    <div class="tab-content" id="download-tab">
                        <p>Your executive summary report is ready for download.</p>
                        <a href="/download/${data.pdf_path}" class="download-btn" target="_blank">
                            <i class="fas fa-file-pdf"></i> Download PDF Report
                        </a>
                    </div>
                </div>
            `;
          document.body.appendChild(resultsModal);

          // Render markdown content using Marked.js
          const insightsContainer =
            resultsModal.querySelector('.insights-content');

          // Wait for Marked.js to load if it's not already loaded
          if (typeof marked === 'undefined') {
            markedScript.onload = function () {
              insightsContainer.innerHTML = marked.parse(data.insights);
            };
          } else {
            insightsContainer.innerHTML = marked.parse(data.insights);
          }

          // Add event listeners for the modal
          const closeBtn = resultsModal.querySelector('.close-modal');
          closeBtn.addEventListener('click', () => {
            document.body.removeChild(resultsModal);
          });

          // Tab functionality
          const tabBtns = resultsModal.querySelectorAll('.tab-btn');
          const tabContents = resultsModal.querySelectorAll('.tab-content');

          tabBtns.forEach((btn) => {
            btn.addEventListener('click', () => {
              // Remove active class from all buttons and contents
              tabBtns.forEach((b) => b.classList.remove('active'));
              tabContents.forEach((c) => c.classList.remove('active'));

              // Add active class to clicked button and corresponding content
              btn.classList.add('active');
              const tabId = btn.getAttribute('data-tab');
              document.getElementById(`${tabId}-tab`).classList.add('active');
            });
          });

          // Show success message
          showSuccess('Analysis completed successfully!');
        } else {
          showError(data.error || 'An error occurred during analysis');
        }
      })
      .catch((error) => {
        // Clear the progress interval
        clearInterval(progressInterval);

        // Remove the modal
        document.body.removeChild(modal);

        showError('Error during analysis: ' + error.message);
      });
  }

  // Reset the selection UI
  function resetSelectionUI() {
    selectionContent.style.display = 'block';
    loadingContainer.style.display = 'none';
    progressBar.style.width = '0%';
    uploadStatus.textContent = 'Loading...';
    customerSelect.value = '';
    customerContainer.style.display = 'block';
  }

  // Toast functions
  function showError(message) {
    errorMessage.textContent = message;
    errorToast.classList.add('show');

    setTimeout(() => {
      errorToast.classList.remove('show');
    }, 5000);
  }

  function showSuccess(message) {
    successMessage.textContent = message;
    successToast.classList.add('show');

    setTimeout(() => {
      successToast.classList.remove('show');
    }, 5000);
  }

  // Close toast buttons
  document.querySelectorAll('.toast-close').forEach((button) => {
    button.addEventListener('click', function () {
      this.closest('.toast').classList.remove('show');
    });
  });

  // Add a sample data link
  const featuresSection = document.querySelector('.features-section');
  const sampleLink = document.createElement('div');
  sampleLink.className = 'sample-data-link';
  sampleLink.innerHTML = `
      <p>Don't have data to test with? <a href="/sample_csv">Download our sample CSV</a></p>
  `;
  featuresSection.appendChild(sampleLink);
});
