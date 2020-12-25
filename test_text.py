from bs4 import BeautifulSoup

m = '<div class="attr-list">SSP Operators<br/><a href="/hwdb/user/combo/24194">Сбитнева В.С.</a><br/></div>'
soup = BeautifulSoup(m, 'html.parser')
l = soup.a.get_text()
print(l == True)
print(l == False)
print(l)
print(soup.get_text())