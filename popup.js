document.addEventListener('DOMContentLoaded', function() {
  const quickCsvBtn = document.getElementById('quickCsvBtn');
  const selectColumnsBtn = document.getElementById('selectColumnsBtn');
  const downloadSelectedBtn = document.getElementById('downloadSelectedBtn');
  const cancelBtn = document.getElementById('cancelBtn');
  const columnSection = document.getElementById('columnSection');
  const columnOptions = document.getElementById('columnOptions');
  const status = document.getElementById('status');

  let tableColumns = [];

  function showStatus(message, type = 'info') {
    status.textContent = message;
    status.className = `status ${type}`;
    status.style.display = 'block';
  }

  quickCsvBtn.addEventListener('click', function() {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
      chrome.tabs.sendMessage(tabs[0].id, {action: 'extractCSV', allColumns: true}, function(response) {
        if (response && response.success) {
          showStatus('CSV downloaded successfully!', 'success');
        } else {
          showStatus('No table found on this page', 'error');
        }
      });
    });
  });

  selectColumnsBtn.addEventListener('click', function() {
    showStatus('Analyzing table columns...', 'info');
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
      chrome.tabs.sendMessage(tabs[0].id, {action: 'getColumns'}, function(response) {
        if (response && response.success) {
          tableColumns = response.columns;
          displayColumns(response.columns);
          columnSection.style.display = 'block';
          showStatus('Select columns and click Download Selected', 'info');
        } else {
          showStatus('No table found on this page', 'error');
        }
      });
    });
  });

  function displayColumns(columns) {
    columnOptions.innerHTML = '';
    
    columns.forEach((column, index) => {
      const columnDiv = document.createElement('div');
      columnDiv.className = 'column-item';
      columnDiv.innerHTML = `
        <input type="checkbox" id="col_${index}" data-index="${index}">
        <label for="col_${index}">${column}</label>
      `;
      columnOptions.appendChild(columnDiv);
    });
  }

  window.toggleAllColumns = function() {
    const checkboxes = document.querySelectorAll('#columnOptions input[type="checkbox"]');
    const allChecked = Array.from(checkboxes).every(cb => cb.checked);
    checkboxes.forEach(cb => cb.checked = !allChecked);
  };

  downloadSelectedBtn.addEventListener('click', function() {
    const selectedColumns = [];
    const checkboxes = document.querySelectorAll('#columnOptions input[type="checkbox"]:checked');
    
    checkboxes.forEach(cb => {
      selectedColumns.push(parseInt(cb.dataset.index));
    });

    if (selectedColumns.length === 0) {
      showStatus('Please select at least one column', 'error');
      return;
    }

    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
      chrome.tabs.sendMessage(tabs[0].id, {
        action: 'extractCSV',
        selectedColumns: selectedColumns
      }, function(response) {
        if (response && response.success) {
          showStatus(`CSV downloaded with ${selectedColumns.length} columns!`, 'success');
          columnSection.style.display = 'none';
        } else {
          showStatus('Download failed', 'error');
        }
      });
    });
  });

  cancelBtn.addEventListener('click', function() {
    columnSection.style.display = 'none';
    showStatus('', 'info');
  });
});