import pandas as pd

# Try reading the CSV file with a few different methods
try:
    # Attempt to read CSV with utf-8 encoding
    df = pd.read_csv('oxford_faculty.csv', encoding='utf-8-sig')

    # Remove parentheses from the 'Email' column
    df['Email'] = df['Email'].str.replace(r'[()]', '', regex=True)

    # Save the cleaned data to a new CSV file
    df.to_csv('oxford_faculty_cleaned.csv', index=False)
    print("Email column cleaned and data saved to 'oxford_faculty_cleaned.csv'")

except Exception as e:
    print(f"An error occurred: {e}")
