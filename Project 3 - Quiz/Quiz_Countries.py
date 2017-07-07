# Given the variable countries defined as:

#             Name    Capital  Populations (millions)
countries = [['China','Beijing',1350],
             ['India','Delhi',1210],
             ['Romania','Bucharest',21],
             ['United States','Washington',307]]

# Write code to print out the capital of India
# by accessing the list

def find_capital(country):
    count = 0
    while(count < len(countries)):
        if((countries[count][0]) == country):
            print (countries[count][1])
            count = count + 1
            break
        else:
            count = count +1

find_capital('India')