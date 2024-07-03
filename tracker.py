import requests
from bs4 import BeautifulSoup

def find_price(URL):
    # Set custom headers to avoid bot detection
    headers = {"User-Agent": "Defined"}

    # Send a get request to the URL with custom headers
    r = requests.get(URL, headers=headers)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(r.content, "html.parser")


    try:
        # Check if the URL is of Amazon page
        if 'amazon' in URL or 'amzn' in URL:
            # Find the price of the product with class "a-price-whole"
            price_tag = soup.find(class_="a-price-whole")
            if price_tag:
                # If price is found, extract required text and round to 2 decimal places
                price_text = price_tag.get_text().removesuffix(".").replace(",", "")
                price = round(float(price_text), 2)
                return price
            else:
                # If "a-price-whole" class not found, try "a-size-small aok-offscreen"
                price_tag = soup.find(class_="a-size-small aok-offscreen")
                if price_tag:
                    # Extract text and round to 2 decimal places
                    price_text = price_tag.get_text().removesuffix("M.R.P.: ₹").replace(",", "")
                    price = round(float(price_text), 2)
                    return price

        # Check if the URL is of Flipkart page
        elif 'flipkart' in URL:
            # Find the price of the product with class "Nx9bqj CxhGGd"
            price_tag = soup.find(class_="Nx9bqj CxhGGd")
            if price_tag:
                # Extract required text and round to 2 decimal places
                price_text = price_tag.get_text().replace("₹", "").replace(",", "")
                price = round(float(price_text), 2)
                return price
    except Exception as e:
        # Handle any exceptions that occur during price extraction
        print(f"Error finding price: {e}")
        return None

# Helper function to convert input with 'k' suffix to numeric value
def convert_to_numeric(input_str):
    try:
        if input_str.lower().endswith("k"):
            return float(input_str[:-1]) * 1000
        else:
            return float(input_str)
    except ValueError:
        return None