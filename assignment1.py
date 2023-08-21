import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    products = []

    product_containers = soup.find_all('div', {'data-asin': True})

    for container in product_containers:
        product = {}

        # Extract the product URL
        product_url_element = container.find('a', {'class': 'a-link-normal'})
        if product_url_element:
            product['url'] = 'https://www.amazon.in' + product_url_element['href']
        else:
            product['url'] = 'No URL Available'

        # Extract other product details
        # ...

        products.append(product)

    return products


def scrape_product_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    product = {}

    # Extract product name
    product_name_element = soup.find('span', {'id': 'productTitle'})
    if product_name_element:
        product['name'] = product_name_element.get_text().strip()

    # Extract product price
    product_price_element = soup.find('span', {'class': 'a-offscreen'})
    if product_price_element:
        product['price'] = product_price_element.get_text().strip()
    else:
        product['price'] = 'Price not available'

    # Extract product rating
    product_rating_element = soup.find('span', {'class': 'a-icon-alt'})
    if product_rating_element:
        product['rating'] = product_rating_element.get_text().strip()

    return product


def print_product_details(product):
    print("Product URL:", product['url'])
    print("Product Name:", product.get('name', 'N/A'))
    print("Product Price:", product.get('price', 'N/A'))
    print("Product Rating:", product.get('rating', 'N/A'))
    print("=" * 50)


base_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_"
products_data = []

for page_number in range(1, 21):
    url = base_url + str(page_number)
    print("Scraping page:", url)
    products_data.extend(scrape_page(url))

for product in products_data:
    print_product_details(product)
    product_url = product['url']

    if product_url != 'No URL Available':
        print("Fetching details for:", product_url)  # Print for debugging
        product_details = scrape_product_details(product_url)
        product.update(product_details)


data_frame = pd.DataFrame(products_data)
data_frame.to_csv('amazon_products.csv', index=False)
