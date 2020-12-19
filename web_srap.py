import requests
from bs4 import BeautifulSoup
import math
from requests.compat import quote_plus
import re

print("\n\t\t\t Code With Harry \n\n")
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", 
               "Accept-Encoding":"gzip, deflate", 
               "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 
               "DNT":"1","Connection":"close", 
               "Upgrade-Insecure-Requests":"1"
               }
# Get the input from the user.
search_item = input("Enter your query here. to get its content.\n")
print("\n\nYou searched for:", search_item)
    
# Initializing an empty list.
final_items = []

# Get the url request to extract the number of results for the query.
r = requests.get(f'https://codewithharry.com/search/?query={quote_plus(search_item)}', headers=headers)
data = r.text
soup = BeautifulSoup(data, features="html.parser")
num_srch = soup.find('h1').text

# Function to split the text from H1 tag and store in the list.
def Convert(string): 
    li = list(string.split(" ")) 
    return li
numsrch = Convert(num_srch)

# Extracting process
if len(search_item) > 3:
    result_num = numsrch[35]
    result_num = result_num.replace('(', '')
    result_num = int(result_num)
    result_num = result_num / 10
    result_num = math.ceil(result_num)
    warning_error = "Everything's alright."
    end_page = result_num + 1
    for i in range(1, end_page):
        r = requests.get(f'https://codewithharry.com/search/?query={quote_plus(search_item)}&number={i}', headers=headers)
        content = r.content
        soup = BeautifulSoup(content, features="html.parser")
        items = soup.find_all('h2')
        for item in items:
            link_text = item.find('a').text
            link_text = link_text.replace("\n", "")
            link_text = re.sub(r"^\s+", "", link_text)
            url = item.find('a').get('href')
            link_url = f'https://codewithharry.com{url}'
            final_items.append((link_text, link_url))
    if len(final_items) == 0:
        error_call = "We could not find your query. Please try again."
        print(error_call)
    else:
        error_call = "Everything's alright."
else:
    result_num = 1
    warning_error = "Your length of query should be greater than 3. "
    print(warning_error)
    
# print(final_items["link_text"]["link_url"])

if len(final_items) > 0:
    file_format = '.txt'
    file_name = search_item + file_format
    with open(file_name, 'w', encoding="utf-8") as filehandle:
        for listitem in final_items:
            filehandle.write('%s\n' % str(listitem))
    print("\n\n\t\t" + f'Your content is saved in {file_name}' + " file.\t\t")