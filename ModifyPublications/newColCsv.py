import pandas as pd
import csv
from transformers import pipeline
# File path to the CSV containing abstracts
input_csv = 'updated_file_with_empty_column.csv'  # Replace with your updated CSV file path

try:
    # Read CSV while skipping rows with extra columns
    df = pd.read_csv(input_csv, on_bad_lines='skip', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')

    # Display the first few rows to check the data
    print("Data successfully loaded. Here are the first few rows:")
    print(df.head())

except Exception as e:
    print(f"An error occurred while reading the CSV: {e}")

# Load the BART summarization model from Hugging Face
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Function to summarize the text
def summarize_text(text):
    # Check if the text is empty or NaN
    if pd.isna(text) or not text.strip():
        return ""  # Return an empty string if the text is invalid
    # BART works with texts up to 1024 tokens, so we may need to truncate long texts
    if len(text) > 1024:
        text = text[:1024]  # Truncate to 1024 characters, can adjust based on use case
    summary = summarizer(text, max_length=150, min_length=50, do_sample=False)
    return summary[0]['summary_text']


df = pd.read_csv(input_csv)
# Ensure the 'Abstract' column exists before applying summarization
if 'Abstract' in df.columns:
    # Apply the summarization function to the Abstract column
    df['Abstract_Summary'] = df['Abstract'].apply(summarize_text)

    # Save the updated CSV file with summaries
    output_csv = 'summarized_abstracts.csv'  # Replace with your desired output file name
    df.to_csv(output_csv, index=False)

    print(f"Summarized abstracts saved to {output_csv}")
else:
    print("Error: 'Abstract' column not found in the input CSV.")
