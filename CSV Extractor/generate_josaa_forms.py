import pandas as pd
import glob
import re
import os

# Dynamically find the two recent years starting with Josaa
files = glob.glob('Josaa*.csv')

def extract_year(filename):
    match = re.search(r'Josaa(\d+)\.csv', os.path.basename(filename))
    return int(match.group(1)) if match else 0

files = sorted(files, key=extract_year, reverse=True)
if len(files) < 2:
    print("Need at least two Josaa CSV files.")
    exit()

recent_file = files[0]
prev_file = files[1]

year_recent = extract_year(recent_file)
year_prev = extract_year(prev_file)

# Read the CSV files
df_recent = pd.read_csv(recent_file)
df_prev = pd.read_csv(prev_file)

def process_dataframe(df):
    # Check for rows whether consecutive pairs are same for multiple rows for better validation
    if len(df) > 5:
        match_count = 0
        for i in range(0, 6, 2):
            if list(df.iloc[i]) == list(df.iloc[i+1]):
                match_count += 1
        
        # If consecutive rows repeat, remove alternate rows starting from 2nd row (index 1) but don't remove the last row
        if match_count >= 2:
            last_row = df.iloc[[-1]]
            df_cleaned = df.iloc[::2]
            
            # If length is even, the last row was at an odd index and thus was dropped. Restore it.
            if len(df) % 2 == 0:
                df = pd.concat([df_cleaned, last_row], ignore_index=True)
            else:
                df = df_cleaned.reset_index(drop=True)

    # Check columns & Total column handling
    if len(df.columns) >= 5:
        df.columns = ['Institute Name', 'Program Name', 'Seat Capacity', 'Female Supernumerary', 'Total'][:len(df.columns)]
    else:
        df.columns = ['Institute Name', 'Program Name', 'Seat Capacity', 'Female Supernumerary']

    # Remove any rows with empty or invalid data
    df = df.dropna(subset=['Institute Name', 'Program Name'])

    # Convert numeric columns to numeric, replacing any non-numeric values with 0
    for col in ['Seat Capacity', 'Female Supernumerary']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    # Calculate Total if it doesn't exist
    if 'Total' not in df.columns:
        df['Total'] = df['Seat Capacity'] + df['Female Supernumerary']
    else:
        df['Total'] = pd.to_numeric(df['Total'], errors='coerce').fillna(0)

    return df

df_prev = process_dataframe(df_prev)
df_recent = process_dataframe(df_recent)

# Save the modifications back to the original Josaa CSV files
df_prev.to_csv(prev_file, index=False)
df_recent.to_csv(recent_file, index=False)

# Form 1: College-wise aggregated data
college_prev = df_prev.groupby('Institute Name').agg({
    'Seat Capacity': 'sum',
    'Female Supernumerary': 'sum',
    'Total': 'sum'
}).reset_index()

college_recent = df_recent.groupby('Institute Name').agg({
    'Seat Capacity': 'sum',
    'Female Supernumerary': 'sum',
    'Total': 'sum'
}).reset_index()

# Merge college data - keep all institutes from both years
form1 = pd.merge(college_prev, college_recent, on='Institute Name', how='outer', suffixes=(f'_{year_prev}', f'_{year_recent}')).fillna(0)
form1['Difference'] = form1[f'Total_{year_recent}'] - form1[f'Total_{year_prev}']

# Rename columns for Form 1
form1.columns = ['Institute Name', 
                 f'{year_prev-1}-{year_prev-2000} Seat Capacity', f'{year_prev-1}-{year_prev-2000} Female Supernumerary', f'{year_prev-1}-{year_prev-2000} Total',
                 f'{year_recent-1}-{year_recent-2000} Seat Capacity', f'{year_recent-1}-{year_recent-2000} Female Supernumerary', f'{year_recent-1}-{year_recent-2000} Total', 
                 'Difference']

# Form 2: Program-wise detailed data
form2_prev = df_prev.copy()
form2_recent = df_recent.copy()

# Merge program data - keep all programs from both years
form2 = pd.merge(form2_prev, form2_recent, on=['Institute Name', 'Program Name'], how='outer', suffixes=(f'_{year_prev}', f'_{year_recent}')).fillna(0)
form2['Difference'] = form2[f'Total_{year_recent}'] - form2[f'Total_{year_prev}']

# Rename columns for Form 2
form2.columns = ['Institute Name', 'Program Name', 
                 f'{year_prev-1}-{year_prev-2000} Seat Capacity', f'{year_prev-1}-{year_prev-2000} Female Supernumerary', f'{year_prev-1}-{year_prev-2000} Total',
                 f'{year_recent-1}-{year_recent-2000} Seat Capacity', f'{year_recent-1}-{year_recent-2000} Female Supernumerary', f'{year_recent-1}-{year_recent-2000} Total', 
                 'Difference']

# Form 3: Program-wise aggregated data
program_prev = df_prev.groupby('Program Name').agg({
    'Seat Capacity': 'sum',
    'Female Supernumerary': 'sum',
    'Total': 'sum'
}).reset_index()

program_recent = df_recent.groupby('Program Name').agg({
    'Seat Capacity': 'sum',
    'Female Supernumerary': 'sum',
    'Total': 'sum'
}).reset_index()

# Merge program data - keep all programs from both years
form3 = pd.merge(program_prev, program_recent, on='Program Name', how='outer', suffixes=(f'_{year_prev}', f'_{year_recent}')).fillna(0)
form3['Difference'] = form3[f'Total_{year_recent}'] - form3[f'Total_{year_prev}']

# Rename columns for Form 3
form3.columns = ['Program Name', 
                 f'{year_prev-1}-{year_prev-2000} Seat Capacity', f'{year_prev-1}-{year_prev-2000} Female Supernumerary', f'{year_prev-1}-{year_prev-2000} Total',
                 f'{year_recent-1}-{year_recent-2000} Seat Capacity', f'{year_recent-1}-{year_recent-2000} Female Supernumerary', f'{year_recent-1}-{year_recent-2000} Total', 
                 'Difference']

# Save to CSV files
form1.to_csv('josaa_form1_college_wise.csv', index=False)
form2.to_csv('josaa_form2_program_wise_detailed.csv', index=False)
form3.to_csv('josaa_form3_program_wise_aggregated.csv', index=False)

print("Generated CSV files:")
print("1. josaa_form1_college_wise.csv - College-wise aggregated data")
print("2. josaa_form2_program_wise_detailed.csv - Program-wise detailed data")
print("3. josaa_form3_program_wise_aggregated.csv - Program-wise aggregated data")

# Display summary statistics
print(f"\nSummary Statistics:")
print(f"Total Colleges in {year_prev}: {len(college_prev)}")
print(f"Total Colleges in {year_recent}: {len(college_recent)}")
print(f"Total Programs in {year_prev}: {len(df_prev)}")
print(f"Total Programs in {year_recent}: {len(df_recent)}")
print(f"Unique Programs in {year_prev}: {df_prev['Program Name'].nunique()}")
print(f"Unique Programs in {year_recent}: {df_recent['Program Name'].nunique()}")