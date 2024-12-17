import smtplib

def send_mail(recipient_email, subject, vname, vid, vkey):

    body=f"""
    Dear {vname},

    I am sending you this email to provide you with the VID and VKey for your account.

    VID: {vid}
    VKey: {vkey}

    Please keep this information safe and secure.

    Sincerely,
    Zust
    """
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('pranaykarbele11@gmail.com', 'kfegljhuqqcqvhfw')

    # Send the email
    server.sendmail('pranaykarbele11@gmail.com', recipient_email, f'Subject: {subject}\n\n{body}')

    server.quit()
    return True