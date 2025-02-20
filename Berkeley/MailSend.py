import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import requests  # Assuming Gemini uses HTTP APIs

# Load sensitive credentials from environment variables
GEMINI_API_KEY = os.getenv('AIzaSyDyPR7lj-MLO6oa86IcSs0kY71pnne4zwU')
SMTP_PASSWORD = os.getenv('qzze cdqv mgzm bsyx')
SMTP_EMAIL = os.getenv('codingguru3999@gmail.com')

def generate_elaboration_gemini(title):
    try:
        url = "https://api.google.com/gemini/v1/generate"  # Replace with the actual Google Gemini endpoint
        headers = {
            "Authorization": f"Bearer {GEMINI_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "prompt": f"Provide a brief summary of the research publication titled: {title}. If no summary is available, return exactly 'NOT FOUND'."
        }
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an error for bad responses

        summary = response.json().get("content", "").strip()
        return f"**{title}**: {summary}" if summary and summary != "NOT FOUND" else ""
    except Exception as e:
        print(f"Error generating elaboration for title: {title} - {e}")
        return ""  # Skip if an error occurs



# The rest of the email-sending logic remains mostly the same
def send_emails_from_csv(csv_file, publications_file, sender_email, sender_password, subject, body_template, resume_path):
    try:
        # Load email addresses and names from the CSV file
        df = pd.read_csv(csv_file)
        if 'Email' not in df.columns or 'Name' not in df.columns:
            print("The CSV file must have 'Email' and 'Name' columns.")
            return

        email_list = df['Email'].dropna().tolist()  # Extract and clean the email column
        name_list = df['Name'].dropna().tolist()   # Extract and clean the name column

        # Load publication titles
        publications_df = pd.read_csv(publications_file)

        # Connect to Gmail's SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, sender_password)  # Login to Gmail

            # Iterate through each email and send the message
            for recipient_email, full_name in zip(email_list, name_list):
                # Extract the last name (assumes the second string in the name is the last name)
                name_parts = full_name.split()
                last_name = name_parts[-1] if len(name_parts) > 1 else full_name  # Use the last part or the full name

                # Get the professor's publications
                publications = publications_df[publications_df['Name'] == full_name]['title'].tolist()

                # Check if any publications were found
                if not publications:
                    print(f"No publications found for {full_name}")
                    continue

                # Prepare the publications section for the email, including elaborations
                elaborations = []
                for title in publications:
                    elaboration = generate_elaboration_gemini(title)  # Get the elaboration using Gemini
                    elaborations.append(f"Title: {title}\nElaboration: {elaboration}\n")

                # Combine all the elaborations
                publications_list = "\n\n".join(elaborations)

                # Customize the email body using the template
                body = body_template.format(
                    LastName=last_name,
                    Publications=publications_list
                )

                # Create the email
                message = MIMEMultipart()
                message['From'] = sender_email
                message['To'] = recipient_email
                message['Subject'] = subject
                message.attach(MIMEText(body, 'plain', 'utf-8'))

                # Attach the resume file
                if os.path.exists(resume_path):
                    with open(resume_path, 'rb') as resume_file:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(resume_file.read())
                        encoders.encode_base64(part)  # Encode the file in base64
                        part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(resume_path)}"')
                        message.attach(part)

                # Send the email
                server.sendmail(sender_email, recipient_email, message.as_string())
                print(f"Email sent to {recipient_email}")

        print("All emails sent successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
csv_file_path = 'Filtered_Professors_Artificial_Intelligence1.csv'  # Email CSV file
publications_file_path = 'Top_Cited_Publications_With_URLs1.csv'  # Publications CSV file
email_subject = "Request for Research Internship Opportunity"  # Email subject

email_body_template = """
Dear Professor {LastName},

I am Prakhar Langer and I am excited to apply for a research internship under your guidance.
I hope this email finds you in the best of your health and high spirits. I am particularly intrigued by your work in these publications: {Publications}.
My technical background includes:
- Successfully participated in and completed a submission to Zama.ai's bounty program. My project focused on implementing invisible watermarking using Fully Homomorphic Encryption (FHE), demonstrating its potential for secure and privacy-preserving digital watermarking.
- Developing a frog identification model using EfficientNet for species classification, applying machine learning techniques such as convolutional neural networks (CNNs) to analyze image features for accurate species prediction.
- Conducting a phospholipid-drug association project, where I utilize Natural Language Processing (NLP) and data analytics to extract meaningful correlations from scientific databases, focusing on phospholipids' role in drug delivery.
- Gaining recognition for my computer vision projects, including object detection using OpenCV for hidden object games and implementing a fire alarm detection system using real-time video analysis.
- Presenting my frog identification idea at Buildspace, which was well-received and sparked discussions on the intersection of AI and ecological conservation.
- Developing projects using cloud technologies, particularly Azure, as part of my internship at Anunta Tech, where I gained hands-on experience in cloud computing and enhanced my skills in managing large datasets and deploying scalable solutions.

I believe my research experience and technical expertise would allow me to contribute meaningfully to your ongoing work. I am eager to collaborate with you and contribute to impactful research in your lab.

Please find my resume attached for further details on my background. I look forward to the opportunity to discuss how I can contribute to your research team.

Best regards,  
Prakhar Langer
"""
send_emails_from_csv(
    csv_file_path, 
    publications_file_path, 
    SMTP_EMAIL, 
    SMTP_PASSWORD, 
    email_subject, 
    email_body_template, 
    r"C:\Users\Prakhar\Downloads\Prakhar-Langer_Resume.pdf")
