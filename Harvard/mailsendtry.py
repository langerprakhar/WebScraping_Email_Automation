import smtplib
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

def send_emails_from_csv(publications_file, professors_file, sender_email, sender_password, subject, body_template, resume_path):
    try:
        # Load publications data from CSV file
        publications_df = pd.read_csv(publications_file)
        
        # Load professors data from CSV file
        professors_df = pd.read_csv(professors_file)
        
        if 'title' not in publications_df.columns or 'professor' not in publications_df.columns:
            print("The publications CSV file must have 'title' and 'professor' columns.")
            return
        
        # Check if the 'professor', 'email', 'research_area' columns exist in the publications DataFrame
        if 'professor' not in publications_df.columns or 'email' not in publications_df.columns or 'research_area' not in publications_df.columns:
            print("The publications CSV file must have 'professor', 'email', and 'research_area' columns.")
            return
        
        # Merge publications with professor data to get their email
        merged_df = publications_df.merge(professors_df[['professor', 'email']], on='professor', how='left')

        # Group by professor and sort publications
        grouped = merged_df.groupby('professor')

        # Connect to Gmail's SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, sender_password)  # Login to Gmail

            # Iterate through each professor and send the message
            for professor, group in grouped:
                # Get the professor's research area
                research_area = group['research_area'].iloc[0]
                
                # Format the top publications into a string (only titles)
                top_publications_str = '\n'.join([f"{row['title']}" for _, row in group.iterrows()])

                # Get the professor's email
                professor_email = group['email'].iloc[0]

                # Customize the email body with the research area and publications
                body = body_template.replace("{Research Areas}", research_area)  # Replace the research areas
                body = body.replace("{Top Publications}", top_publications_str)  # Replace the publications

                # Create the email
                message = MIMEMultipart()
                message['From'] = sender_email
                message['To'] = professor_email
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
                server.sendmail(sender_email, professor_email, message.as_string())
                print(f"Email sent to {professor_email}")

        print("All emails sent successfully!")

        # Append the email column to the publications CSV file
        publications_df['email'] = merged_df['email']
        publications_df.to_csv(publications_file, index=False)
        print(f"Emails have been appended to {publications_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
publications_file_path = 'HarvardProfessors_Publications1.csv'  # The file containing publications data
professors_file_path = 'HarvardProfessors1.csv'  # The file containing professors' emails
sender_email = 'prakhar.langer@gmail.com'  # Replace with your Gmail address
sender_password = 'onpf evtj qcqy ntti'  # Replace with your Gmail app password
email_subject = "Request for Research Internship Opportunity"  # Email subject
email_body_template = """
Dear Professor {LastName},

I have been following your research closely, and I am highly impressed by your contributions in {Research Areas}. Your publications that I was particularly intrigued by are:

{Top Publications}

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
"""  # Replace with your email body template
resume_path = 'C:/Users/Prakhar/Downloads/Prakhar_Langer_Resume.pdf'  # Replace with the path to your resume

# Call the function to send emails
send_emails_from_csv(publications_file_path, professors_file_path, sender_email, sender_password, email_subject, email_body_template, resume_path)
