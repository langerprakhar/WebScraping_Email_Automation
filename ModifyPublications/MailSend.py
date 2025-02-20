import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

def send_emails_from_csv(csv_file, summaries_file, publications_file, sender_email, sender_password, subject, body_template, resume_path):
    try:
        # Load email addresses and names from the CSV file
        df = pd.read_csv(csv_file)
        if 'Email' not in df.columns or 'Name' not in df.columns:
            print("The CSV file must have 'Email' and 'Name' columns.")
            return

        email_list = df['Email'].dropna().tolist()  # Extract and clean the email column
        name_list = df['Name'].dropna().tolist()   # Extract and clean the name column

        # Load publication titles and summaries
        publications_df = pd.read_csv(publications_file)
        summaries_df = pd.read_csv(summaries_file)

        # Connect to Gmail's SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, sender_password)  # Login to Gmail

            # Iterate through each email and send the message
            for recipient_email, full_name in zip(email_list, name_list):
                # Extract the last name (assumes the second string in the name is the last name)
                name_parts = full_name.split()
                last_name = name_parts[-1] if len(name_parts) > 1 else full_name  # Use the last part or the full name

                # Get the professor's publications and summaries
                publications = publications_df[publications_df['professor_name'] == full_name]['title'].tolist()
                summaries = summaries_df[summaries_df['Abstract'].str.contains(full_name, na=False)]['Summary'].tolist()

                # Check if any publications were found
                if not publications:
                    print(f"No publications found for {full_name}")
                    continue

                # Prepare the publications and summaries section for the email
                publications_with_summary = ""
                for title, summary in zip(publications, summaries):
                    publications_with_summary += f"\n- {title}: {summary}"

                # Customize the email body using the template
                body = body_template.format(
                    LastName=last_name,
                    Publications=", ".join(publications),
                    PublicationsWithSummary=publications_with_summary,
                    Accomplishments="During my research internship under Professor Matthias Wacker at the National University of Singapore, I explored the role of phospholipids in drug formulations. By analyzing PubMed data and ranking phospholipids based on their interactions with cancer-curing drugs, I contributed to advancing targeted drug delivery mechanisms. This interdisciplinary experience reinforced my commitment to solving real-world challenges through computational approaches.\n\nBeyond this, I have developed a frog species identification app with the hope of helping identify various frog species by the scientists of the Western Ghats in India, using machine learning as part of my honours research. These projects honed my skills in Python, OpenCV, and TensorFlow while nurturing my ability to address challenges at the intersection of AI and human-centric design. My passion for human augmentation, a technique to enhance physical and cognitive abilities, aligns with my broader interest in HCI and its potential to redefine accessibility and performance."
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
csv_file_path = 'Filtered_Professors_Artificial_Intelligence1.csv'  # The file containing the email addresses and names
summaries_file_path = 'extracted_and_summarized_links.csv'  # The file containing publication summaries
publications_file_path = 'Top_Cited_Publications_With_URLs1.csv'  # The file containing the publication titles and URLs
sender_email = 'prakhar.langer@gmail.com'  # Replace with your Gmail address
sender_password = 'onpf evtj qcqy ntti'  # Replace with your Gmail app password
email_subject = "Request for Research Internship Opportunity"  # Email subject

# Email body template with placeholders for professor's last name, publications, summaries, and accomplishments
email_body_template = """
Dear Professor {LastName},

I am Prakhar Langer and I am excited to apply for a research internship under your guidance.
I hope this email finds you in the best of your health and high spirits. I am particularly intrigued by your innovative work in some of your publications that I have read:{Publications}. 
{PublicationsWithSummary}
. My technical background includes:

- Developing a frog identification model using EfficientNet for species classification, applying machine learning techniques such as convolutional neural networks (CNNs) to analyze image features for accurate species prediction.
- Conducting a phospholipid-drug association project, where I utilize Natural Language Processing (NLP) and data analytics to extract meaningful correlations from scientific databases, focusing on phospholipids' role in drug delivery.
- Gaining recognition for my computer vision projects, including object detection using OpenCV for hidden object games and implementing a fire alarm detection system using real-time video analysis.
- Presenting my frog identification idea at Buildspace, which was well-received for its innovative use of machine learning and computer vision.
- Creating various automation tools and Python-based projects, such as an Amazon clone for frontend development, and games like Blackjack and RockPaperScissors.
- Completing a cloud computing internship, where I gained hands-on experience in managing databases and cloud infrastructure.

With a strong interest in AI, machine learning, computer vision, and data analytics, I am eager to contribute to your research and expand my expertise. I look forward to the opportunity to work under your mentorship.

Thank you for considering my application. I look forward to the possibility of learning from and contributing to your innovative work.

Best Regards,
Prakhar Langer
"""

# Path to the resume
resume_path = 'C:/Users/Prakhar/Downloads/Prakhar_Langer_Resume.pdf'  # Replace with the path to your resume

# Call the function to send emails
send_emails_from_csv(csv_file_path, summaries_file_path, publications_file_path, sender_email, sender_password, email_subject, email_body_template, resume_path)
