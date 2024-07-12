from bs4 import BeautifulSoup
import json
# HTML input
html = '''

'''

# Parse the HTML
soup = BeautifulSoup(html, 'html.parser')

# Extract the mat-option elements
mat_options = soup.find_all('mat-option')

# Create a dictionary to store the results
options_dict = {}

# Populate the dictionary with id and text
for option in mat_options:
    option_id = option.get('id')
    option_text = option.find('span', class_='texto-option-expansivel').text
    options_dict[option_text] = ""

filename = "varas.json"
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(options_dict, f, ensure_ascii=False, indent=4)
    
    
# Print the result
print(options_dict)
