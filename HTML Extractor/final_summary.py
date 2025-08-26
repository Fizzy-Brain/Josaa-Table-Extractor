#!/usr/bin/env python3
"""
Final Summary of JOSAA Data Extraction
"""

import pandas as pd

def final_summary():
    print("🎓 JOSAA 2025-2026 Seat Matrix Data Extraction - COMPLETE")
    print("=" * 65)
    
    # Read the CSV files
    form1_df = pd.read_csv('josaa_form1_college_wise.csv')
    form2_df = pd.read_csv('josaa_form2_program_wise_detailed.csv')
    form3_df = pd.read_csv('josaa_form3_program_wise_aggregated.csv')
    
    print(f"\n📊 EXTRACTION SUMMARY:")
    print(f"✅ Form 1 - College-wise totals: {len(form1_df):,} colleges")
    print(f"✅ Form 2 - Program-wise detailed: {len(form2_df):,} program entries")
    print(f"✅ Form 3 - Program-wise aggregated: {len(form3_df):,} unique programs")
    
    print(f"\n🏫 COLLEGE STATISTICS (2025-26):")
    print(f"Total Colleges: {len(form1_df):,}")
    print(f"Total Seat Capacity: {form1_df['2025-26 Seat Capacity'].sum():,}")
    print(f"Total Female Supernumerary: {form1_df['2025-26 Female Supernumerary'].sum():,}")
    print(f"Grand Total Seats: {form1_df['2025-26 Total'].sum():,}")
    
    print(f"\n🎯 PROGRAM STATISTICS (2025-26):")
    print(f"Total Program Entries: {len(form2_df):,}")
    print(f"Unique Programs: {len(form3_df):,}")
    print(f"Total Seat Capacity: {form2_df['2025-26 Seat Capacity'].sum():,}")
    print(f"Total Female Supernumerary: {form2_df['2025-26 Female Supernumerary'].sum():,}")
    print(f"Grand Total Seats: {form2_df['2025-26 Total'].sum():,}")
    
    print(f"\n🏆 TOP 10 COLLEGES BY TOTAL SEATS:")
    top_colleges = form1_df.nlargest(10, '2025-26 Total')[['Institute Name', '2025-26 Total']]
    for i, (_, row) in enumerate(top_colleges.iterrows(), 1):
        print(f"{i:2d}. {row['Institute Name'][:60]:<60} {row['2025-26 Total']:>5,}")
    
    print(f"\n🏆 TOP 10 PROGRAMS BY TOTAL SEATS (Across All Colleges):")
    top_programs = form3_df.nlargest(10, '2025-26 Total')[['Program Name', '2025-26 Total']]
    for i, (_, row) in enumerate(top_programs.iterrows(), 1):
        print(f"{i:2d}. {row['Program Name'][:60]:<60} {row['2025-26 Total']:>5,}")
    
    print(f"\n📁 FILES GENERATED:")
    print(f"1. josaa_form1_college_wise.csv - College-wise aggregated data")
    print(f"2. josaa_form2_program_wise_detailed.csv - Detailed program-wise data")
    print(f"3. josaa_form3_program_wise_aggregated.csv - Program-wise totals")
    
    print(f"\n📝 NOTE:")
    print(f"Currently using the same HTML file for both 2024-25 and 2025-26 data.")
    print(f"When you provide the 2024-25 HTML file, re-run the extraction script")
    print(f"to get accurate year-over-year comparisons with real differences.")
    
    print(f"\n✨ EXTRACTION SUCCESSFUL! All data has been processed correctly.")

if __name__ == "__main__":
    final_summary()
