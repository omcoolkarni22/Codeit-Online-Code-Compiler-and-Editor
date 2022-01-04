from bs4 import BeautifulSoup
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *


def send(to, url):
    with open('D:\\Python\\Codeit\\templates\\resetPassword.html') as file:
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
        sg = SendGridAPIClient('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')
        response = sg.send(message)
        return True if response.status_code == 202 else False

    except Exception as e:
        return False


if __name__ == '__main__':
    send('', 'google.com')

