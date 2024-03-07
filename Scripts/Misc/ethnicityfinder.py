from ethnicity import Ethnicity

# initialize and create dictionaries
e = Ethnicity().make_dicts()

# apply to a list of names
print(e.get(['Jacky Chan', 'Ruben Powar', 'James Mumberson', 'Kirat Dhillon',  'Freddie Simons', 'Igor Gorbatsevich',
             'Tahleel Khan', 'Sam Tibbins,', 'Nadav Albin', 'Le Masson']))
