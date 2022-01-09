from bs4 import BeautifulSoup
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
import os


def send(to, url):
    with open(os.getcwd() + '\\templates\\resetPassword.html') as file:
        txt = file.read()
        soup = BeautifulSoup(txt, 'html.parser')

    main = soup.find('a')
    main['href'] = url
    # print(soup)

    message = Mail(
        from_email='kulkarniom88@gmail.com',
        to_emails=to,
        subject='Code-It Password Reset Link',
        html_content=str(soup)
    )
    try:
        sg = SendGridAPIClient(os.environ.get('SEND_GRID_API'))
        response = sg.send(message)
        return True if response.status_code == 202 else False

    except Exception as e:
        return False


if __name__ == '__main__':
    send('', 'google.com')
