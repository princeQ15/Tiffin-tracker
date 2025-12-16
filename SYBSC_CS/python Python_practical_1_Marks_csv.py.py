import pandas as pd

import os

script_dir = os.path.dirname(os.path.abspath(__file__))
marks_path = os.path.join(script_dir, "marks.csv")

df = pd.read_csv(marks_path)

print("First few rows of the dataset:")
print(df.head(10))

print("\nData type of columns:")
print(df.dtypes)

df = df.fillna(0) 
print("\nMissing values handled.")

df = df.drop_duplicates()
print("\nDuplicates removed.")

df = df.rename(columns={
    'columns~1': 'Sql Marks',
    'location': 'Address',
    'sql_marks': 'Set Marks',
    'excel_marks': 'Excel Marks'
})
print("\nColumns renamed successfully.")

for col in df.select_dtypes(include='float').columns:
    df[col] = df[col].astype(int)
print("\nData types changed successfully.")

columns_to_drop = ['Remarks', 'Address']
df = df.drop(columns=[col for col in columns_to_drop if col in df.columns])
print("\nFinal Cleaned DataFrame:")
print(df.head())
print("\nUpdated Data Types:")
print(df.dtypes)