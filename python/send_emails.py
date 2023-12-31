import smtplib
import random

def send_email(subject, body):
    from_email = "<FROM@EMAIL.COM>"
    to_email = "<TO@EMAIL.COM>"
    password = "<APP_PASSWORD>"

    msg = f"From: {from_email}\nTo: {to_email}\nSubject: {subject}\n\n{body}"

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg)
        server.quit()
        print(f"Email sent with subject: {subject}")
    except Exception as e:
        print(f"Failed to send email: {e}")


subjects_and_bodies = {
    'negative': {
        'subjects': ["Bad News", "Oops!", "Sorry..."],
        'bodies': ["Something went wrong", "We regret to inform you...", "Unfortunately, we cannot proceed."]
    },
    'positive': {
        'subjects': ["Great News!", "Congratulations!", "Good to Go!"],
        'bodies': ["Everything is perfect", "You've achieved something great!", "We're happy to announce..."]
    },
    'neutral': {
        'subjects': ["Update", "Information", "Details"],
        'bodies': ["Here's an update", "This is an informational message.", "Here are the details."]
    }
}

types = ['negative', 'positive', 'neutral']

for _ in range(100):
    email_type = random.choice(types)
    subject = random.choice(subjects_and_bodies[email_type]['subjects'])
    body = random.choice(subjects_and_bodies[email_type]['bodies'])

    send_email(subject, body)
