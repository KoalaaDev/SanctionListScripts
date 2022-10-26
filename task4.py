import scrapeutils
import dbutils
import PyPDF2

scrapeutils.GetPDF("https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32014R0833&from=EN")
from PyPDF2 import PdfReader

reader = PdfReader("EU Sanction list.pdf")
page = reader.pages[-1] #last page
#extract the list of names
names = page.extractText().split("\n")[2:-1]
print(names)




