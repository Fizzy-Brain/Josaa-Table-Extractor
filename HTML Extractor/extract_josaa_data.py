#!/usr/bin/env python3
"""
JOSAA Seat Matrix Data Extractor
Extracts institute, program, and seat capacity data from JOSAA HTML files
Creates three different CSV formats for analysis
"""

import re
import csv
import pandas as pd
from bs4 import BeautifulSoup
from collections import defaultdict

def extract_josaa_data(html_file_path):
    """Extract seat matrix data from JOSAA HTML file"""
    
    with open(html_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # Find all institute spans
    institute_spans = soup.find_all('span', {'id': 'lblnm'})
    institutes = [span.get_text(strip=True) for span in institute_spans]
    
    # Find all program spans
    program_spans = soup.find_all('span', {'id': 'lblAcademicProgram'})
    programs = [span.get_text(strip=True) for span in program_spans]
    
    # Find all seat capacity spans
    seat_spans = soup.find_all('span', {'id': 'lblProgramTotal'})
    seats = [int(span.get_text(strip=True)) for span in seat_spans]
    
    # Find all female supernumerary spans
    female_spans = soup.find_all('span', {'id': 'lblFemaleSeats'})
    female_seats = [int(span.get_text(strip=True)) for span in female_spans]
    
    data = []
    
    # Since all arrays should have the same length, zip them together
    if len(institutes) == len(programs) == len(seats) == len(female_seats):
        for i in range(len(institutes)):
            data.append({
                'institute_name': institutes[i],
                'program_name': programs[i],
                'seat_capacity': seats[i],
                'female_supernumerary': female_seats[i],
                'total_seats': seats[i] + female_seats[i]
            })
    else:
        print(f"Data length mismatch: institutes={len(institutes)}, programs={len(programs)}, seats={len(seats)}, female={len(female_seats)}")
    
    return data

def create_form1_csv(data_2024, data_2025, output_file):
    """Form 1: College-wise totals"""
    
    # Aggregate by institute for 2024-25
    institute_totals_2024 = defaultdict(lambda: {'seat_capacity': 0, 'female_supernumerary': 0})
    for row in data_2024:
        inst = row['institute_name']
        institute_totals_2024[inst]['seat_capacity'] += row['seat_capacity']
        institute_totals_2024[inst]['female_supernumerary'] += row['female_supernumerary']
    
    # Aggregate by institute for 2025-26
    institute_totals_2025 = defaultdict(lambda: {'seat_capacity': 0, 'female_supernumerary': 0})
    for row in data_2025:
        inst = row['institute_name']
        institute_totals_2025[inst]['seat_capacity'] += row['seat_capacity']
        institute_totals_2025[inst]['female_supernumerary'] += row['female_supernumerary']
    
    # Get all unique institutes
    all_institutes = set(institute_totals_2024.keys()) | set(institute_totals_2025.keys())
    
    form1_data = []
    for institute in sorted(all_institutes):
        data_2024_inst = institute_totals_2024[institute]
        data_2025_inst = institute_totals_2025[institute]
        
        total_2024 = data_2024_inst['seat_capacity'] + data_2024_inst['female_supernumerary']
        total_2025 = data_2025_inst['seat_capacity'] + data_2025_inst['female_supernumerary']
        difference = total_2025 - total_2024
        
        form1_data.append({
            'Institute Name': institute,
            '2024-25 Seat Capacity': data_2024_inst['seat_capacity'],
            '2024-25 Female Supernumerary': data_2024_inst['female_supernumerary'],
            '2024-25 Total': total_2024,
            '2025-26 Seat Capacity': data_2025_inst['seat_capacity'],
            '2025-26 Female Supernumerary': data_2025_inst['female_supernumerary'],
            '2025-26 Total': total_2025,
            'Difference (2025-26 minus 2024-25)': f"{'+' if difference > 0 else ''}{difference}"
        })
    
    # Write to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Institute Name', '2024-25 Seat Capacity', '2024-25 Female Supernumerary', 
                     '2024-25 Total', '2025-26 Seat Capacity', '2025-26 Female Supernumerary', 
                     '2025-26 Total', 'Difference (2025-26 minus 2024-25)']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(form1_data)
    
    print(f"Form 1 CSV created: {output_file}")

def create_form2_csv(data_2024, data_2025, output_file):
    """Form 2: Program-wise details as given"""
    
    # Create dictionaries for easy lookup
    data_2024_dict = {}
    for row in data_2024:
        key = (row['institute_name'], row['program_name'])
        data_2024_dict[key] = row
    
    data_2025_dict = {}
    for row in data_2025:
        key = (row['institute_name'], row['program_name'])
        data_2025_dict[key] = row
    
    # Get all unique combinations
    all_combinations = set(data_2024_dict.keys()) | set(data_2025_dict.keys())
    
    form2_data = []
    for institute, program in sorted(all_combinations):
        data_2024_row = data_2024_dict.get((institute, program), {'seat_capacity': 0, 'female_supernumerary': 0, 'total_seats': 0})
        data_2025_row = data_2025_dict.get((institute, program), {'seat_capacity': 0, 'female_supernumerary': 0, 'total_seats': 0})
        
        difference = data_2025_row['total_seats'] - data_2024_row['total_seats']
        
        form2_data.append({
            'Institute Name': institute,
            'Program Name': program,
            '2024-25 Seat Capacity': data_2024_row['seat_capacity'],
            '2024-25 Female Supernumerary': data_2024_row['female_supernumerary'],
            '2024-25 Total': data_2024_row['total_seats'],
            '2025-26 Seat Capacity': data_2025_row['seat_capacity'],
            '2025-26 Female Supernumerary': data_2025_row['female_supernumerary'],
            '2025-26 Total': data_2025_row['total_seats'],
            'Difference (2025-26 minus 2024-25)': f"{'+' if difference > 0 else ''}{difference}"
        })
    
    # Write to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Institute Name', 'Program Name', '2024-25 Seat Capacity', 
                     '2024-25 Female Supernumerary', '2024-25 Total', '2025-26 Seat Capacity', 
                     '2025-26 Female Supernumerary', '2025-26 Total', 
                     'Difference (2025-26 minus 2024-25)']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(form2_data)
    
    print(f"Form 2 CSV created: {output_file}")

def create_form3_csv(data_2024, data_2025, output_file):
    """Form 3: Program-wise totals across all colleges"""
    
    # Aggregate by program for 2024-25
    program_totals_2024 = defaultdict(lambda: {'seat_capacity': 0, 'female_supernumerary': 0})
    for row in data_2024:
        prog = row['program_name']
        program_totals_2024[prog]['seat_capacity'] += row['seat_capacity']
        program_totals_2024[prog]['female_supernumerary'] += row['female_supernumerary']
    
    # Aggregate by program for 2025-26
    program_totals_2025 = defaultdict(lambda: {'seat_capacity': 0, 'female_supernumerary': 0})
    for row in data_2025:
        prog = row['program_name']
        program_totals_2025[prog]['seat_capacity'] += row['seat_capacity']
        program_totals_2025[prog]['female_supernumerary'] += row['female_supernumerary']
    
    # Get all unique programs
    all_programs = set(program_totals_2024.keys()) | set(program_totals_2025.keys())
    
    form3_data = []
    for program in sorted(all_programs):
        data_2024_prog = program_totals_2024[program]
        data_2025_prog = program_totals_2025[program]
        
        total_2024 = data_2024_prog['seat_capacity'] + data_2024_prog['female_supernumerary']
        total_2025 = data_2025_prog['seat_capacity'] + data_2025_prog['female_supernumerary']
        difference = total_2025 - total_2024
        
        form3_data.append({
            'Program Name': program,
            '2024-25 Seat Capacity': data_2024_prog['seat_capacity'],
            '2024-25 Female Supernumerary': data_2024_prog['female_supernumerary'],
            '2024-25 Total': total_2024,
            '2025-26 Seat Capacity': data_2025_prog['seat_capacity'],
            '2025-26 Female Supernumerary': data_2025_prog['female_supernumerary'],
            '2025-26 Total': total_2025,
            'Difference (2025-26 minus 2024-25)': f"{'+' if difference > 0 else ''}{difference}"
        })
    
    # Write to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Program Name', '2024-25 Seat Capacity', '2024-25 Female Supernumerary', 
                     '2024-25 Total', '2025-26 Seat Capacity', '2025-26 Female Supernumerary', 
                     '2025-26 Total', 'Difference (2025-26 minus 2024-25)']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(form3_data)
    
    print(f"Form 3 CSV created: {output_file}")

def main():
    # File paths
    html_file_2025 = 'Josaa2025.html'
    html_file_2024 = 'Josaa2025.html'
    
    print("Extracting data from HTML files...")
    
    # Extract data
    data_2024 = extract_josaa_data(html_file_2024)
    data_2025 = extract_josaa_data(html_file_2025)
    
    print(f"Extracted {len(data_2024)} records for 2024-25")
    print(f"Extracted {len(data_2025)} records for 2025-26")
    
    # Create the three CSV forms
    create_form1_csv(data_2024, data_2025, 'josaa_form1_college_wise.csv')
    create_form2_csv(data_2024, data_2025, 'josaa_form2_program_wise_detailed.csv')
    create_form3_csv(data_2024, data_2025, 'josaa_form3_program_wise_aggregated.csv')
    
    print("\nAll CSV files have been created successfully!")
    print("- josaa_form1_college_wise.csv: College-wise totals")
    print("- josaa_form2_program_wise_detailed.csv: Detailed program-wise data")
    print("- josaa_form3_program_wise_aggregated.csv: Program-wise aggregated across all colleges")

if __name__ == "__main__":
    main()
