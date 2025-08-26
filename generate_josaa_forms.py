import pandas as pd

# Read the CSV files
df_2024 = pd.read_csv('Josaa2024.csv')
df_2025 = pd.read_csv('Josaa2025.csv')

# Clean column names
df_2024.columns = ['Institute Name', 'Program Name', 'Seat Capacity', 'Female Supernumerary', 'Total']
df_2025.columns = ['Institute Name', 'Program Name', 'Seat Capacity', 'Female Supernumerary', 'Total']

# Remove any rows with empty or invalid data
df_2024 = df_2024.dropna(subset=['Institute Name', 'Program Name'])
df_2025 = df_2025.dropna(subset=['Institute Name', 'Program Name'])

# Convert numeric columns to numeric, replacing any non-numeric values with 0
for col in ['Seat Capacity', 'Female Supernumerary', 'Total']:
    df_2024[col] = pd.to_numeric(df_2024[col], errors='coerce').fillna(0)
    df_2025[col] = pd.to_numeric(df_2025[col], errors='coerce').fillna(0)

# Form 1: College-wise aggregated data
college_2024 = df_2024.groupby('Institute Name').agg({
    'Seat Capacity': 'sum',
    'Female Supernumerary': 'sum',
    'Total': 'sum'
}).reset_index()

college_2025 = df_2025.groupby('Institute Name').agg({
    'Seat Capacity': 'sum',
    'Female Supernumerary': 'sum',
    'Total': 'sum'
}).reset_index()

# Merge college data - keep all institutes from both years
form1 = pd.merge(college_2024, college_2025, on='Institute Name', how='outer', suffixes=('_2024', '_2025')).fillna(0)
form1['Difference'] = form1['Total_2025'] - form1['Total_2024']

# Rename columns for Form 1
form1.columns = ['Institute Name', '2024-25 Seat Capacity', '2024-25 Female Supernumerary', '2024-25 Total',
                 '2025-26 Seat Capacity', '2025-26 Female Supernumerary', '2025-26 Total', 'Difference']

# Form 2: Program-wise detailed data
form2_2024 = df_2024.copy()
form2_2025 = df_2025.copy()

# Merge program data - keep all programs from both years
form2 = pd.merge(form2_2024, form2_2025, on=['Institute Name', 'Program Name'], how='outer', suffixes=('_2024', '_2025')).fillna(0)
form2['Difference'] = form2['Total_2025'] - form2['Total_2024']

# Rename columns for Form 2
form2.columns = ['Institute Name', 'Program Name', '2024-25 Seat Capacity', '2024-25 Female Supernumerary', '2024-25 Total',
                 '2025-26 Seat Capacity', '2025-26 Female Supernumerary', '2025-26 Total', 'Difference']

# Form 3: Program-wise aggregated data
program_2024 = df_2024.groupby('Program Name').agg({
    'Seat Capacity': 'sum',
    'Female Supernumerary': 'sum',
    'Total': 'sum'
}).reset_index()

program_2025 = df_2025.groupby('Program Name').agg({
    'Seat Capacity': 'sum',
    'Female Supernumerary': 'sum',
    'Total': 'sum'
}).reset_index()

# Merge program data - keep all programs from both years
form3 = pd.merge(program_2024, program_2025, on='Program Name', how='outer', suffixes=('_2024', '_2025')).fillna(0)
form3['Difference'] = form3['Total_2025'] - form3['Total_2024']

# Rename columns for Form 3
form3.columns = ['Program Name', '2024-25 Seat Capacity', '2024-25 Female Supernumerary', '2024-25 Total',
                 '2025-26 Seat Capacity', '2025-26 Female Supernumerary', '2025-26 Total', 'Difference']

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
print(f"Total Colleges in 2024: {len(college_2024)}")
print(f"Total Colleges in 2025: {len(college_2025)}")
print(f"Total Programs in 2024: {len(df_2024)}")
print(f"Total Programs in 2025: {len(df_2025)}")
print(f"Unique Programs in 2024: {df_2024['Program Name'].nunique()}")
print(f"Unique Programs in 2025: {df_2025['Program Name'].nunique()}")