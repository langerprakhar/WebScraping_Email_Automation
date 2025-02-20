import smtplib
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

def send_emails_from_csv(csv_file, sender_email, sender_password, subject, body_template, resume_path):
    """
    Reads email addresses and names from a CSV file and sends a personalized email with an attachment.

    Parameters:
    - csv_file: Path to the CSV file containing email addresses and names
    - sender_email: Sender's Gmail address
    - sender_password: Sender's Gmail password (consider using an app password)
    - subject: Email subject
    - body_template: Email body template with placeholders for the professor's last name
    - resume_path: Path to the resume file to be attached
    """
    try:
        # Load email addresses and names from the CSV file
        df = pd.read_csv(csv_file)
        if 'Email' not in df.columns or 'Name' not in df.columns:
            print("The CSV file must have 'Email' and 'Name' columns.")
            return

        email_list = df['Email'].dropna().tolist()  # Extract and clean the email column
        name_list = df['Name'].dropna().tolist()   # Extract and clean the name column

        # Connect to Gmail's SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, sender_password)  # Login to Gmail

            # Iterate through each email and send the message
            for recipient_email, full_name in zip(email_list, name_list):
                # Extract the last name (assumes the second string in the name is the last name)
                name_parts = full_name.split()
                last_name = name_parts[1] if len(name_parts) > 1 else "Professor"

                # Customize the email body
                body = body_template.replace("{LastName}", last_name)

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
csv_file_path = 'columbia_matchedProfs.csv'  # The file containing the email addresses and names
sender_email = 'prakhar.langer@gmail.com'  # Replace with your Gmail address
sender_password = 'onpf evtj qcqy ntti'  # Replace with your Gmail app password
email_subject = "Request for Research Internship Opportunity"  # Email subject
email_body_template = """
Dear Professor {LastName},

I am Prakhar Langer, and I am excited to apply for a research internship under your guidance. My technical background includes:

- Developing a frog identification model using EfficientNet for species classification, applying machine learning techniques such as convolutional neural networks (CNNs) to analyze image features for accurate species prediction.
- Conducting a phospholipid-drug association project, where I utilize Natural Language Processing (NLP) and data analytics to extract meaningful correlations from scientific databases, focusing on phospholipids' role in drug delivery.
- Gaining recognition for my computer vision projects, including object detection using OpenCV for hidden object games and implementing a fire alarm detection system using real-time video analysis.
- Presenting my frog identification idea at Buildspace, which was well-received for its innovative use of machine learning and computer vision.
- Creating various automation tools and Python-based projects, such as an Amazon clone for frontend development, and games like Blackjack and RockPaperScissors.
- Completing a cloud computing internship, where I gained hands-on experience in managing databases and cloud infrastructure.

With a strong interest in AI, machine learning, computer vision, and data analytics, I am eager to contribute to your research and expand my expertise. I look forward to the opportunity to work under your mentorship.

Thank you for considering my application.

Sincerely,
Prakhar Langer
"""  # Replace with your email body template
resume_path = 'C:/Users/Prakhar/Downloads/Prakhar_Langer_Resume.pdf'  # Replace with the path to your resume

# Call the function to send emails
send_emails_from_csv(csv_file_path, sender_email, sender_password, email_subject, email_body_template, resume_path)
