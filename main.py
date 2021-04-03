from bs4 import BeautifulSoup
import requests
import pandas
import datetime

# Item to be searched for and replacing spaces with '+' for url
object = input("Enter the Item you want to search: ")
object = object.replace(' ','+')

# No of pages to be parsed
pages = int(input("Number of pages you want to parse: "))

# if you need data in excel?
fg = input("Do you want data to be saved in a file (y/n) :")

# For storing values to export to excel
title_list = []
price_list = []
misc_list = []
heading_misc = 'Misc'

for i in range(1,pages+1):

    try:
        # using requests and Bs4 to parse html using lxml
        html_text = requests.get('https://www.flipkart.com/search?q='+object+'&sort=popularity&page='+str(i)).text
        soup = BeautifulSoup(html_text,'lxml')
    except:
        print("Error Occured!!")
        exit(1)

    # finding the main list of items
    item_list = soup.find_all('div',class_='_1AtVbE col-12-12')

    for item in item_list:

        div = item.find('div',class_='_13oc-S')
        
        if(div is not None):    
            if(div.find('div',class_='_4rR01T') is not None):
                
                # Finding the respective values
                
                title = div.find('div',class_='_4rR01T').text
                title_list.append(title)
                
                price = div.find('div',class_='_30jeq3 _1_WHN1').text
                price_list.append(price)
                
                rating = div.find('div',class_='_3LWZlK').text
                misc_list.append(rating)
                heading_misc = 'Rating' 

                # Printing extracted values
                print(title,' : ',price,'    Rating:',rating)
                print() 
            
            else:
                
                item_list2 = div.find_all('div',class_='_1xHGtK _373qXS')   
                
                for item2 in item_list2:    
                    
                    # Finding the respective values
                    
                    title = item2.find('div',class_='_2WkVRV').text
                    title_list.append(title)
                    
                    price = div.find('div',class_='_30jeq3').text
                    price_list.append(price)
                    
                    cat = div.find('a',class_='IRpwTa').text
                    misc_list.append(cat)
                    heading_misc = 'Category'   
                    
                    # Printing extracted values
                    print(title,' : ',price,"    Category :",cat)
                    print()


if(fg == 'y' or fg == 'Y'): 
    
    # To add timestamp to file name to avoid ambiguities
    def timeStamped(fname, fmt='%Y-%m-%d-%H-%M-%S_{fname}'):
        return datetime.datetime.now().strftime(fmt).format(fname=fname)

    df = pandas.DataFrame( {
                'Title' : title_list ,
                'Price' : price_list ,
                heading_misc : misc_list
                } )

    file_name = timeStamped(object+'.xlsx')
    df.to_excel(file_name)
