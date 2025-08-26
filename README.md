# JOSAA Table Extractor Extension

A Chrome extension designed to extract JOSAA (Joint Seat Allocation Authority) admission data tables from the official JOSAA website and convert them to CSV format for analysis.

## 🚀 Features

- **Smart Table Detection**: Automatically detects JOSAA tables on official JOSAA websites
- **Column Selection**: Choose specific columns to export or download all data
- **CSV Export**: Clean, formatted CSV output with proper data handling
- **Program Total Splitting**: Automatically splits "Program Total" columns into "Seat Capacity" and "Female Supernumerary"
- **Data Processing**: Handles complex table structures with merged cells and multiple headers

## 📋 Prerequisites

- Google Chrome browser
- Access to JOSAA official websites (josaa.nic.in, josaa.admissions.nic.in)
- Python 3.x (for data analysis scripts)
- pandas library (for Python scripts)

## 🛠️ Installation & Setup

### Step 1: Download the Extension Files

1. Clone or download this repository to your local machine
2. Navigate to the project folder: `Josaa Extension`

### Step 2: Install the Chrome Extension

1. Open Google Chrome
2. Navigate to `chrome://extensions/`
3. Enable "Developer mode" (toggle in top-right corner)
4. Click "Load unpacked"
5. Select the `Ext` folder from the project directory
6. The extension should now appear in your extensions list

### Step 3: Pin the Extension (Recommended)

1. Click the puzzle piece icon (Extensions) in Chrome toolbar
2. Find "JOSAA Table Extractor" and click the pin icon
3. The extension icon will now be visible in your toolbar

## 📖 Usage Instructions

### ⚠️ IMPORTANT: Wait for Page Loading

**Always ensure the JOSAA webpage has completely loaded before using the extension. Wait for all tables and data to appear on the page before attempting to download.**

### Basic Usage

1. **Navigate to JOSAA Website**
   - Go to any JOSAA official page with data tables
   - Supported sites: `josaa.nic.in`, `josaa.admissions.nic.in`

2. **Wait for Complete Loading**
   - ⚠️ **CRITICAL**: Wait until the page fully loads and all table data is visible
   - Look for the complete table with all rows populated
   - Do not proceed if you see loading indicators or partial data

3. **Open Extension**
   - Click the JOSAA Table Extractor icon in your Chrome toolbar
   - The extension popup will appear

4. **Choose Download Option**
   - **Quick Download**: Downloads all columns immediately
   - **Select Columns**: Choose specific columns to download

### Quick Download (All Columns)

1. Click "Quick Download (All Columns)"
2. The CSV file will be automatically downloaded to your default Downloads folder
3. File naming: `josaa_table_YYYY-MM-DD.csv`

### Selective Column Download

1. Click "Select Columns & Download"
2. Wait for column analysis to complete
3. Check/uncheck desired columns
4. Use "Select All / None" to toggle all columns
5. Click "Download Selected"
6. The CSV file will be downloaded with only selected columns

## 📊 Data Processing Scripts

### Python Analysis Tools

The project includes Python scripts for advanced data analysis:

#### `generate_josaa_forms.py`

Processes JOSAA data to create three analytical reports:

**Prerequisites:**
```bash
pip install pandas
```

**Usage:**
1. Ensure you have `Josaa2024.csv` and `Josaa2025.csv` in the project directory
2. Run the script:
   ```bash
   python generate_josaa_forms.py
   ```

**Generated Reports:**
- `josaa_form1_college_wise.csv` - College-wise aggregated data comparison
- `josaa_form2_program_wise_detailed.csv` - Detailed program-wise data
- `josaa_form3_program_wise_aggregated.csv` - Program-wise aggregated comparison

## 🔧 Technical Details

### Supported Websites
- `*://josaa.nic.in/*`
- `*://josaa.admissions.nic.in/*`
- `*://*.josaa.nic.in/*`
- `*://*.nic.in/*josaa*`

### Table Detection
The extension automatically detects tables using:
- Specific JOSAA table IDs
- GridView controls
- Fallback detection for tables with substantial data (>5 rows)

### Data Processing Features
- **Merged Cell Handling**: Properly processes tables with rowspan/colspan
- **Multi-header Support**: Combines multiple header rows into meaningful column names
- **Numeric Data**: Automatically detects and formats numeric values
- **Text Cleaning**: Removes extra whitespace and formats text properly

## 🚨 Important Notes

### Critical Usage Guidelines

1. **⚠️ Page Loading**: Always wait for complete page loading before using the extension
2. **Table Visibility**: Ensure all table data is visible on screen
3. **Network Connection**: Maintain stable internet connection during data extraction
4. **Browser Compatibility**: Only tested with Google Chrome

### Troubleshooting

**"No table found on this page"**
- Ensure you're on a JOSAA website with data tables
- Wait for the page to completely load
- Refresh the page and try again

**Download Issues**
- Check if downloads are blocked in Chrome settings
- Ensure sufficient disk space
- Try using "Quick Download" if selective download fails

**Extension Not Working**
- Refresh the JOSAA webpage
- Disable and re-enable the extension
- Check if the extension is properly loaded in `chrome://extensions/`

## 📁 Project Structure

```
Josaa Extension/
├── Ext/                          # Chrome Extension Files
│   ├── manifest.json            # Extension configuration
│   ├── content.js              # Main extraction logic
│   ├── popup.html              # Extension interface
│   ├── popup.js                # Interface functionality
│   └── styles.css              # Extension styling
├── generate_josaa_forms.py      # Data analysis script
├── Josaa2024.csv               # Sample 2024 data
├── Josaa2025.csv               # Sample 2025 data
├── josaa_form1_college_wise.csv # Generated report 1
├── josaa_form2_program_wise_detailed.csv # Generated report 2
├── josaa_form3_program_wise_aggregated.csv # Generated report 3
└── README.md                   # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly with JOSAA websites
5. Submit a pull request

## 📄 License

This project is for educational and research purposes. Please respect JOSAA website terms of service when using this extension.

## ⚠️ Disclaimer

This extension is not officially affiliated with JOSAA or NIC. Use responsibly and in accordance with the website's terms of service. Always verify downloaded data accuracy against the original source.