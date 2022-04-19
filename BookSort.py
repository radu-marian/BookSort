from bs4 import BeautifulSoup
import webbrowser
import requests

class Book:
	def __init__(self, name, rating, no_ratings):
		self.name = name
		self.rating = rating
		self.no_ratings = no_ratings
	def getName(self):
		return self.name
	def getRating(self):
		return self.rating
	def getNoRatings(self):
		return self.no_ratings
	def getNoRatingsNum(self):
		return float(self.no_ratings.replace(",", ""))
	def printInfo(self):
		print(self.name, " -- ", self.rating, " -- ", self.no_ratings)

html_text = requests.get('https://www.goodreads.com/list/show/6.Best_Books_of_the_20th_Century').text
soup = BeautifulSoup(html_text, 'lxml')

names = [];

names_raw = soup.find_all(itemprop="name")
for name in names_raw:
	names.append(name.string)

rating_and_number = soup.find_all(class_="minirating", recursive = True)

rating = [];
number = [];
books = [];
i = 0

for line in rating_and_number:
	line = line.text
	if line[0] == "r":
		number.append(line[34:].split(" ", 1)[0])
		rating.append(line[16:20:1])
	else:
		number.append(line.split(" ")[5])
		rating.append(line.split(" ")[1])
	books.append(Book(names[i], rating[i], number[i]))
	i = i + 1


books.sort(key=Book.getRating, reverse = True)


f_rating = open("rating.html", "w")

html_content_rating = """<HTML>
<TITLE>ver</TITLE>
<BODY>
<DIV>
<TABLE BORDER="1px" STYLE="float:left">
<TR>
<SMALL>
<TH>Name</TH>
<TH>Rating (KEY)</TH>
<TH>No. ratings</TH>
</TR>
</SMALL>\n"""

for book in books:
	part = "<TR>\n<TH><SMALL>" + book.getName() + "</SMALL></TH>\n<TH>" + book.getRating() + "</TH>\n<TH>"
	part += book.getNoRatings() + "</TH>\n</TR>\n";
	html_content_rating += part



html_content_rating += """</TABLE>
<TABLE BORDER="1px" STYLE="float:right">
<TR>
<SMALL>
<TH>Name</TH>
<TH>Rating</TH>
<TH>No. ratings(KEY)</TH>
</TR>
</SMALL>\n"""

books.sort(key=Book.getNoRatingsNum, reverse=True)

for book in books:
        part = "<TR>\n<TH><SMALL>" + book.getName() + "</SMALL></TH>\n<TH>" + book.getRating() + "</TH>\n<TH>"
        part += book.getNoRatings() + "</TH>\n</TR>\n";
        html_content_rating += part


html_content_rating += """</TABLE>
</DIV>
</BODY>
</HTML>"""

f_rating.write(html_content_rating)
f_rating.close()

webbrowser.open_new_tab("rating.html")
