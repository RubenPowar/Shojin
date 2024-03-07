# Import docx NOT python-docx 
import docx
import pandas as pd
from docxtpl import DocxTemplate



doc = docx.Document('/Users/ruben/PycharmProjects/Shojin/files/Logs/Templates/TableTemp.docx')
doc2 = DocxTemplate('/Users/ruben/PycharmProjects/Shojin/files/Logs/Templates/TableTemp.docx')

# Table data in a form of list 
data = (
    (1, 'Geek 1'),
    (2, 'Geek 2'),
    (3, 'Geek 3')
)


# Creating a table object 
table = doc.add_table(rows=1, cols=2)

# Adding heading in the 1st row of the table 
row = table.rows[0].cells
row[0].text = 'Id'
row[1].text = 'Name'

# Adding data from the list to the table 
for id, name in data:
    # Adding a row and then adding data in it.
    row = table.add_row().cells
    # Converting id to string as table can only take string input 
    row[0].text = str(id)
    row[1].text = name



my_context = {'table': data}
doc2.render(my_context)
doc2.save('/Users/ruben/PycharmProjects/Shojin/WordTestFiles/gfg1.docx')

# Now save the document to a location 
doc.save('/Users/ruben/PycharmProjects/Shojin/WordTestFiles/gfg2.docx')
