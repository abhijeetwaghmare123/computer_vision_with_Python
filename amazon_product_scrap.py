import requests
from bs4 import BeautifulSoup
import pandas as pd
def scrape_product_listing(url, num_pages):
    all_products = []
    
    for page in range(1, num_pages + 1):
        page_url = url + f'&page={page}'
        response = requests.get(page_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        products = soup.find_all('div', {'data-component-type': 's-search-result'})
        
        for product in products:
            product_data = {}
            
            product_name = product.find('span', {'class': 'a-text-normal'}).text
            product_data['Product Name'] = product_name
            
            product_url = 'https://www.amazon.in' + product.find('a', {'class': 'a-link-normal'})['href']
            product_data['Product URL'] = product_url
            
            product_price = product.find('span', {'class': 'a-offscreen'}).text
            product_data['Product Price'] = product_price
            
            rating = product.find('span', {'class': 'a-icon-alt'})
            if rating:
                product_data['Rating'] = rating.text.split()[0]
            else:
                product_data['Rating'] = None
            
            num_reviews = product.find('span', {'class': 'a-size-base', 'aria-label': 'customer reviews'})
            if num_reviews:
                product_data['Number of Reviews'] = num_reviews.text
            else:
                product_data['Number of Reviews'] = None
            
            all_products.append(product_data)
    
    return all_products
  url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"
num_pages = 20  # You can adjust the number of pages as needed

product_data_list = scrape_product_listing(url, num_pages)
def scrape_product_details(product_url):
    response = requests.get(product_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    product_details = {}
    
    description_elem = soup.find('div', {'id': 'productDescription'})
    if description_elem:
        description = description_elem.get_text(strip=True)
        product_details['Description'] = description
    else:
        product_details['Description'] = None
    
    asin_elem = soup.find('th', text='ASIN')
    if asin_elem:
        asin = asin_elem.find_next('td').get_text(strip=True)
        product_details['ASIN'] = asin
    else:
        product_details['ASIN'] = None
    
    product_description_elem = soup.find('div', {'id': 'feature-bullets'})
    if product_description_elem:
        product_description = product_description_elem.get_text(strip=True)
        product_details['Product Description'] = product_description
    else:
        product_details['Product Description'] = None
    
    manufacturer_elem = soup.find('a', {'id': 'bylineInfo'})
    if manufacturer_elem:
        manufacturer = manufacturer_elem.get_text(strip=True)
        product_details['Manufacturer'] = manufacturer
    else:
        product_details['Manufacturer'] = None
    
    return product_details
for product in product_data_list:
    product_url = product['Product URL']
    product_details = scrape_product_details(product_url)
    product.update(product_details)
    df = pd.DataFrame(product_data_list)
df.to_csv('amazon_products.csv', index=False)


