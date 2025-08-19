// Removed bulk export functionality

// Find any JOSAA table on the page
function findTable() {
  const tableIds = [
    'ctl00_ContentPlaceHolder1_GridView1',
    'ctl00_ContentPlaceHolder1_gvSeatMatrix',
    'ctl00_ContentPlaceHolder1_GridView',
    'GridView1'
  ];
  
  for (let id of tableIds) {
    const table = document.getElementById(id);
    if (table && table.rows.length > 1) {
      return table;
    }
  }
  
  // Fallback: find any table with substantial data
  const tables = document.querySelectorAll('table');
  for (let table of tables) {
    if (table.rows.length > 5) {
      return table;
    }
  }
  
  return null;
}

// Listen for messages from popup
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.action === 'extractCSV') {
    const success = extractTableToCSV(null, request.selectedColumns, request.allColumns);
    sendResponse({success: success});
  } else if (request.action === 'getColumns') {
    const columns = getTableColumns();
    sendResponse({success: columns.length > 0, columns: columns});
  }
});











function sanitizeFilename(text) {
  return text.replace(/[^a-z0-9]/gi, '_').toLowerCase();
}



function getTableColumns() {
  const table = findTable();
  if (!table || table.rows.length === 0) {
    return [];
  }

  const rows = Array.from(table.rows);
  const grid = buildDataGrid(rows);
  const columns = [];
  
  // Find data row to check for space-separated values
  let dataRowIndex = -1;
  for (let i = 2; i < grid.length; i++) {
    if (grid[i] && grid[i].some(cell => /\d+\s+\d+/.test(cell))) {
      dataRowIndex = i;
      break;
    }
  }
  
  // Process each column
  for (let col = 0; col < grid[0].length; col++) {
    const headerParts = [];
    
    // Get header text from first few rows
    for (let row = 0; row < Math.min(3, grid.length); row++) {
      const text = grid[row][col];
      if (text && !headerParts.includes(text)) {
        headerParts.push(text);
      }
    }
    
    const columnName = headerParts.join(' - ') || `Column ${col + 1}`;
    
    // Check if this is the Program Total column with space-separated values
    const isProgramTotalColumn = columnName.toLowerCase().includes('program') && 
                                columnName.toLowerCase().includes('total');
    const hasSpaceSeparatedValues = dataRowIndex >= 0 && 
                                   grid[dataRowIndex][col] && 
                                   /\d+\s+\d+/.test(grid[dataRowIndex][col]);
    
    if (isProgramTotalColumn && hasSpaceSeparatedValues) {
      // Split Program Total column into Seat Capacity and Female Supernumerary
      columns.push('Seat Capacity');
      columns.push('Female Supernumerary');
    } else {
      columns.push(columnName);
    }
  }
  
  return columns;
}

function buildDataGrid(rows) {
  const maxCols = Math.max(...rows.map(row => {
    let colCount = 0;
    Array.from(row.cells).forEach(cell => {
      colCount += parseInt(cell.getAttribute('colspan') || '1');
    });
    return colCount;
  }));
  
  const grid = [];
  for (let i = 0; i < rows.length; i++) {
    grid[i] = new Array(maxCols).fill('');
  }
  
  for (let rowIndex = 0; rowIndex < rows.length; rowIndex++) {
    const row = rows[rowIndex];
    const cells = Array.from(row.cells);
    let colIndex = 0;
    
    for (let cellIndex = 0; cellIndex < cells.length; cellIndex++) {
      const cell = cells[cellIndex];
      
      while (colIndex < maxCols && grid[rowIndex][colIndex] !== '') {
        colIndex++;
      }
      
      let text = '';
      const spans = cell.querySelectorAll('span');
      if (spans.length > 0) {
        text = Array.from(spans).map(span => span.textContent.trim()).join(' ');
      } else {
        text = cell.textContent.trim();
      }
      
      const rowspan = parseInt(cell.getAttribute('rowspan') || '1');
      const colspan = parseInt(cell.getAttribute('colspan') || '1');
      
      for (let r = 0; r < rowspan; r++) {
        for (let c = 0; c < colspan; c++) {
          if (rowIndex + r < grid.length && colIndex + c < maxCols) {
            grid[rowIndex + r][colIndex + c] = text;
          }
        }
      }
      
      colIndex += colspan;
    }
  }
  
  return grid;
}

function extractTableToCSV(filename, selectedColumns, allColumns) {
  const table = findTable();
  if (!table) {
    return false;
  }

  const rows = Array.from(table.rows);
  const originalGrid = buildDataGrid(rows);
  
  // Find which columns are Program Total columns that need to be split
  const columnsToSplit = [];
  for (let col = 0; col < originalGrid[0].length; col++) {
    // Check header for Program Total column
    const headerParts = [];
    for (let row = 0; row < Math.min(3, originalGrid.length); row++) {
      const text = originalGrid[row][col];
      if (text && !headerParts.includes(text)) {
        headerParts.push(text);
      }
    }
    const columnName = headerParts.join(' - ').toLowerCase();
    const isProgramTotalColumn = columnName.includes('program') && columnName.includes('total');
    
    // Check if this column has space-separated values in data rows
    let hasSpaceSeparatedValues = false;
    for (let row = 2; row < originalGrid.length; row++) {
      if (originalGrid[row][col] && /\d+\s+\d+/.test(originalGrid[row][col])) {
        hasSpaceSeparatedValues = true;
        break;
      }
    }
    
    columnsToSplit[col] = isProgramTotalColumn && hasSpaceSeparatedValues;
  }
  
  // Process grid to split Program Total columns
  const processedGrid = originalGrid.map((row, rowIndex) => {
    const newRow = [];
    
    for (let col = 0; col < row.length; col++) {
      const cellValue = row[col] || '';
      
      if (columnsToSplit[col]) {
        // This is a Program Total column - split the space-separated values
        if (/\d+\s+\d+/.test(cellValue)) {
          const values = cellValue.trim().split(/\s+/);
          const seat = values[0] || '0';
          const female = values[1] || '0';
          newRow.push(seat);
          newRow.push(female);
        } else {
          // For header rows
          if (rowIndex < 3) {
            newRow.push('Seat Capacity');
            newRow.push('Female Supernumerary');
          } else {
            newRow.push('0');
            newRow.push('0');
          }
        }
      } else {
        newRow.push(cellValue);
      }
    }
    
    return newRow;
  });
  
  // Convert grid to CSV
  let csvData;
  if (selectedColumns && !allColumns) {
    csvData = processedGrid.map(row => {
      return selectedColumns.map(colIndex => {
        const text = (row[colIndex] || '').replace(/\s+/g, ' ').replace(/"/g, '""');
        return `"${text}"`;
      }).join(',');
    }).join('\n');
  } else {
    csvData = processedGrid.map(row => {
      return row.map(cell => {
        const text = (cell || '').replace(/\s+/g, ' ').replace(/"/g, '""');
        return `"${text}"`;
      }).join(',');
    }).join('\n');
  }

  downloadCSV(csvData, filename);
  return true;
}

function downloadCSV(csvData, filename) {
  const blob = new Blob([csvData], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  const url = URL.createObjectURL(blob);
  
  link.setAttribute('href', url);
  link.setAttribute('download', filename || `josaa_table_${new Date().toISOString().slice(0,10)}.csv`);
  link.style.visibility = 'hidden';
  
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

