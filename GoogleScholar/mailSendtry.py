import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import google.generativeai as genai

# Load sensitive credentials from environment variables
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")  # previously hardcoded; rotate exposed credential
SMTP_EMAIL = 'prakhar.langer@gmail.com'  # Your email
SMTP_PASSWORD = os.environ.get("OUTREACH_LEGACY_SMTP_PASSWORD")  # previously hardcoded; rotate exposed credential

# Configure Google Generative AI
genai.configure(api_key=GEMINI_API_KEY)

# Function to generate an elaboration using Google Generative AI
def generate_elaboration_gemini(title):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(f"Provide a brief summary of the research publication titled: {title} in less than 80 words")
        return response.text.strip()
    except Exception as e:
        print(f"Error generating elaboration for title: {title} - {e}")
        return "No elaboration available"

# Email sending function
def send_emails_from_csv(csv_file, publications_file, sender_email, sender_password, subject, body_template, resume_path):
    raise RuntimeError("Legacy SMTP send path disabled; use reviewed Outlook Drafts workflow instead.")
    try:
        # Load email addresses and names from the CSV file
        df = pd.read_csv(csv_file)
        if 'Email' not in df.columns or 'Name' not in df.columns:
            print("The CSV file must have 'Email' and 'Name' columns.")
            return

        email_list = df['Email'].dropna().tolist()
        name_list = df['Name'].dropna().tolist()

        # Load publication titles
        publications_df = pd.read_csv(publications_file)

        # Connect to Gmail's SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)

            # Iterate through each email and send the message
            for recipient_email, full_name in zip(email_list, name_list):
                name_parts = full_name.split()
                last_name = name_parts[-1] if len(name_parts) > 1 else full_name

                publications = publications_df[publications_df['professor_name'] == full_name]['title'].tolist()

                if not publications:
                    print(f"No publications found for {full_name}")
                    continue

                elaborations = []
                for title in publications:
                    elaboration = generate_elaboration_gemini(title)
                    elaborations.append(f"Title: {title}\nElaboration: {elaboration}\n")

                publications_list = "\n\n".join(elaborations)

                body = body_template.format(
                    LastName=last_name,
                    Publications=publications_list
                )

                message = MIMEMultipart()
                message['From'] = sender_email
                message['To'] = recipient_email
                message['Subject'] = subject
                message.attach(MIMEText(body, 'plain', 'utf-8'))

                if os.path.exists(resume_path):
                    with open(resume_path, 'rb') as resume_file:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(resume_file.read())
                        encoders.encode_base64(part)
                        part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(resume_path)}"')
                        message.attach(part)

                server.sendmail(sender_email, recipient_email, message.as_string())
                print(f"Email sent to {recipient_email}")

        print("All emails sent successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
csv_file_path = 'Filtered_Professors_Artificial_Intelligence.csv'
publications_file_path = 'Top_Cited_Publications_With_URLs.csv'
email_subject = "Request for Research Internship Opportunity"

email_body_template = """
Dear Professor {LastName},

I am Prakhar Langer and I am excited to apply for a research internship under your guidance.

{Publications}

My Research Background includes:
I have served as a research intern under Professor Matthias Wacker at the National University of Singapore, 
I explored the role of phospholipids in drug formulations. By analyzing PubMed data and ranking phospholipids based on their interactions with 
cancer-curing drugs, I contributed to advancing targeted drug delivery mechanisms. This interdisciplinary experience reinforced my commitment 
to solving real-world challenges through computational approaches.

My technical background includes:
- Developing a frog identification model using EfficientNet for species classification, applying machine learning techniques such as convolutional neural networks (CNNs) to analyze image features for accurate species prediction.
- Conducting a phospholipid-drug association project, where I utilize Natural Language Processing (NLP) and data analytics to extract meaningful correlations from scientific databases, focusing on phospholipids' role in drug delivery.
- Gaining recognition for my computer vision projects, including object detection using OpenCV for hidden object games and implementing a fire alarm detection system using real-time video analysis.
- Presenting my frog identification idea at Buildspace, which was well-received and sparked discussions on the intersection of AI and ecological conservation.
- Developing projects using cloud technologies, particularly Azure, as part of my internship at Anunta Tech, where I gained hands-on experience in cloud computing and enhanced my skills in managing large datasets and deploying scalable solutions.

I am looking forward to contributing to your ongoing research projects and gaining invaluable experience under your mentorship.

Sincerely,
Prakhar Langer
"""

send_emails_from_csv(csv_file_path, publications_file_path, SMTP_EMAIL, SMTP_PASSWORD, email_subject, email_body_template, r"C:\Users\Prakhar\Desktop\Python Projects\Resume.pdf")
