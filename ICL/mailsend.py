import smtplib
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import time

def send_emails(publications_file, faculty_file, sender_email, sender_password, subject, body_template, resume_path):
    try:
        # Load and clean data
        publications_df = pd.read_csv(publications_file)
        faculty_df = pd.read_csv(faculty_file)

        # Strip spaces from column headers
        publications_df.columns = publications_df.columns.str.strip()
        faculty_df.columns = faculty_df.columns.str.strip()

        # Merge data on professor name
        merged_df = publications_df.merge(
            faculty_df[['Name', 'Email', 'Research Area']].drop_duplicates(),
            left_on='professor', right_on='Name', how='left', validate="many_to_one"
        )

        # Check for missing emails
        if merged_df['Email'].isnull().any():
            print("Warning: Some professors in the publications file do not have corresponding emails.")

        # Group publications by professor
        grouped = merged_df.groupby('professor')

        # Connect to SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)

            for professor, group in grouped:
                professor_email = group['Email'].iloc[0]
                if pd.isna(professor_email):
                    print(f"Skipping professor {professor} as no email is available.")
                    continue

                # Extract last name
                last_name = professor.split()[-1]

                # Prepare research areas
                research_area = group['Research Area'].iloc[0]

                # Prepare top publications
                top_publications = '\n'.join([f"- {title}" for title in group['title'].head(3)])

                # Customize email body
                body = body_template.format(LastName=last_name, ResearchArea=research_area, TopPublications=top_publications)

                # Create email
                message = MIMEMultipart()
                message['From'] = sender_email
                message['To'] = professor_email
                message['Subject'] = subject
                message.attach(MIMEText(body, 'plain', 'utf-8'))

                # Attach resume
                if os.path.exists(resume_path):
                    with open(resume_path, 'rb') as resume_file:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(resume_file.read())
                        encoders.encode_base64(part)
                        part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(resume_path)}"')
                        message.attach(part)
                else:
                    print(f"Resume file not found at {resume_path}. Skipping attachment.")
                    continue

                # Send email
                server.sendmail(sender_email, professor_email, message.as_string())
                print(f"Email sent to {professor_email}")

                # Pause to avoid spam detection
                time.sleep(2)

        print("All emails sent successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")

publications_file_path = 'ICLProfessors_Publications.csv'
faculty_file_path = 'faculty_data.csv'
sender_email = 'prakhar.langer@gmail.com'
sender_password = 'onpf evtj qcqy ntti'
email_subject = "Request for Research Internship Opportunity"
email_body_template = """

Dear Professor {LastName},

I have been following your research closely, and I am highly impressed by your contributions in {ResearchArea}. Your publications that I was particularly intrigued by are:

{TopPublications}

I am currently pursuing a B.Tech (Hons) in Computer Science at Manipal Institute Of Technology and have developed a strong foundation in machine learning, cloud computing, and data analytics.

My Research Background includes:
- Serving as a research intern under Professor Matthias Wacker at the National University of Singapore, where I explored the role of phospholipids in drug formulations. I analyzed PubMed data and ranked phospholipids based on their interactions with cancer-curing drugs, contributing to the advancement of targeted drug delivery mechanisms. This interdisciplinary experience reinforced my commitment to solving real-world challenges through computational approaches.

My Technical Background includes:
- Developing a frog identification model using EfficientNet for species classification, applying machine learning techniques such as convolutional neural networks (CNNs) to analyze image features for accurate species prediction.
- Conducting a phospholipid-drug association project, utilizing Natural Language Processing (NLP) and data analytics to extract meaningful correlations from scientific databases, with a focus on phospholipids' role in drug delivery.
- Gaining recognition for my computer vision projects, including object detection using OpenCV for hidden object games and implementing a fire alarm detection system using real-time video analysis.
- Presenting my frog identification idea at Buildspace, which was well-received and sparked discussions on the intersection of AI and ecological conservation.
- Developing projects using cloud technologies, particularly Azure, as part of my internship at Anunta Tech, where I gained hands-on experience in cloud computing, enhancing my skills in managing large datasets and deploying scalable solutions.

I would greatly appreciate the opportunity to discuss how I can contribute to your research and gain invaluable experience under your mentorship. Thank you for considering my application.

Sincerely,  
Prakhar Langer
"""
resume_path = r"C:\Users\Prakhar\Downloads\Prakhar's_Resume.pdf"

# Call the function
send_emails(publications_file_path, faculty_file_path, sender_email, sender_password, email_subject, email_body_template, resume_path)
