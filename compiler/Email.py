from bs4 import BeautifulSoup

with open('../templates/resetPassword.html') as file:
    txt = file.read()
    soup = BeautifulSoup(txt, 'html.parser')

main = soup.find('a')
main['href'] = 'google.com'
print(main.prettify())

