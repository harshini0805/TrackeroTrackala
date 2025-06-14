import requests
from bs4 import BeautifulSoup
import time
import random
from urllib.parse import urljoin
import re
import json
import csv
from datetime import datetime, timedelta
import schedule
import threading
import os

# Your original robust scraping functions
def get_amazon_price_requests(url):
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0'
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Cache-Control': 'max-age=0',
        'Referer': 'https://www.amazon.in/',
        'Host': 'www.amazon.in'
    }
    
    session = requests.Session()
    session.headers.update(headers)
    
    try:
        # Add longer random delay to avoid rate limiting
        time.sleep(random.uniform(3, 6))
        
        # Try multiple attempts with increasing delays
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = session.get(url, timeout=15)
                response.raise_for_status()
                break
            except requests.RequestException as e:
                if attempt < max_retries - 1:
                    print(f"Attempt {attempt + 1} failed, retrying in {(attempt + 1) * 5} seconds...")
                    time.sleep((attempt + 1) * 5)
                    # Change user agent for retry
                    session.headers.update({'User-Agent': random.choice(user_agents)})
                else:
                    raise e
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Multiple selectors for product name
        product_name = None
        product_selectors = [
            '#productTitle',
            '.product-title',
            'h1.a-size-large',
            'span#productTitle',
            'h1[data-automation-id="product-title"]',
            '.a-size-large.product-title-word-break'
        ]
        
        for selector in product_selectors:
            element = soup.select_one(selector)
            if element and element.get_text(strip=True):
                product_name = element.get_text(strip=True)
                break
        
        # If no product name found, try h1 tags
        if not product_name:
            h1_tags = soup.find_all('h1')
            for h1 in h1_tags:
                text = h1.get_text(strip=True)
                if text and len(text) > 10:
                    product_name = text
                    break
        
        # Multiple selectors for price
        price = None
        price_selectors = [
            '.a-price-whole',
            '.a-price .a-offscreen',
            '#priceblock_dealprice',
            '#priceblock_ourprice',
            '.a-price-range .a-price .a-offscreen',
            'span.a-price-symbol + span.a-price-whole',
            '.a-price.a-text-price.a-size-medium.apexPriceToPay .a-offscreen',
            '.a-price.apexPriceToPay .a-offscreen',
            '.a-price-whole'
        ]
        
        for selector in price_selectors:
            element = soup.select_one(selector)
            if element and element.get_text(strip=True):
                price_text = element.get_text(strip=True)
                if '₹' in price_text or price_text.replace(',', '').replace('.', '').isdigit():
                    price = price_text if '₹' in price_text else f"₹{price_text}"
                    break
        
        # If no price found, search for rupee symbol or price patterns
        if not price:
            # Look for rupee symbols in spans
            price_spans = soup.find_all('span', string=lambda text: text and '₹' in text)
            for span in price_spans:
                text = span.get_text(strip=True)
                if text and len(text) < 30 and any(c.isdigit() for c in text):
                    price = text
                    break
            
            # Alternative: look for price in common Amazon price containers
            price_containers = soup.find_all(['span', 'div'], class_=lambda x: x and 'price' in x.lower())
            for container in price_containers:
                text = container.get_text(strip=True)
                if '₹' in text and len(text) < 20:
                    price = text
                    break
        
        return product_name, price
        
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return None, None
    except Exception as e:
        print(f"Error scraping Amazon: {e}")
        return None, None

def get_flipkart_price_requests(url):
    # Rotate user agents to avoid detection
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0'
    ]
    
    headers = {
        'User-Agent': random.choice(user_agents),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'DNT': '1',
        'Sec-Fetch-User': '?1'
    }
    
    session = requests.Session()
    session.headers.update(headers)
    
    try:
        # Add random delay
        time.sleep(random.uniform(1, 3))
        
        response = session.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Multiple selectors for product name
        product_name = None
        product_selectors = [
            'span.B_NuCI',
            'h1.x-product-title-label',
            'span._35KyD6',
            'h1._6EBuvT',
            '.B_NuCI'
        ]
        
        for selector in product_selectors:
            element = soup.select_one(selector)
            if element and element.get_text(strip=True):
                product_name = element.get_text(strip=True)
                break
        
        # If no product name found, try h1 tags
        if not product_name:
            h1_tags = soup.find_all('h1')
            for h1 in h1_tags:
                text = h1.get_text(strip=True)
                if text and len(text) > 10:
                    product_name = text
                    break
        
        # Multiple selectors for price
        price = None
        price_selectors = [
            '._30jeq3',
            '._30jeq3._16Jk6d',
            '.Nx9bqj.CxhGGd',
            '._1_WHN1',
            '._3I9_wc._2p6lqe',
            'div._25b18c span'
        ]
        
        for selector in price_selectors:
            element = soup.select_one(selector)
            if element and element.get_text(strip=True):
                price_text = element.get_text(strip=True)
                if '₹' in price_text:
                    price = price_text
                    break
        
        # If no price found, search for rupee symbol
        if not price:
            rupee_elements = soup.find_all(string=lambda text: text and '₹' in text)
            for text in rupee_elements:
                if text.strip() and len(text.strip()) < 20:
                    price = text.strip()
                    break
        
        return product_name, price
        
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return None, None
    except Exception as e:
        print(f"Error scraping Flipkart: {e}")
        return None, None

def extract_price_number(price_text):
    """Extract numeric price from price text"""
    if not price_text:
        return None
    
    # Remove currency symbol and clean the text
    price_clean = price_text.replace('₹', '').replace(',', '').strip()
    
    # Extract numbers using regex
    numbers = re.findall(r'\d+\.?\d*', price_clean)
    
    if numbers:
        try:
            return float(numbers[0])
        except ValueError:
            return None
    return None

def scrape_product_price(url, product_name):
    """Scrape price from URL using appropriate scraper"""
    print(f"  Scraping {product_name}...")
    
    if 'amazon' in url.lower():
        name, price = get_amazon_price_requests(url)
        platform = 'Amazon'
    elif 'flipkart' in url.lower():
        name, price = get_flipkart_price_requests(url)
        platform = 'Flipkart'
    else:
        print(f"  ❌ Unsupported platform for {product_name}")
        return None, None, None
    
    if price:
        price_num = extract_price_number(price)
        print(f"  ✅ {platform}: {price}")
        return platform, price, price_num
    else:
        print(f"  ❌ {platform}: Price not found")
        return platform, None, None

def load_products_from_file(file_path):
    """Load products from JSON or CSV file"""
    products = []
    
    if not os.path.exists(file_path):
        print(f"❌ File {file_path} not found!")
        return products
    
    try:
        if file_path.endswith('.json'):
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    products = data
                else:
                    products = [data]
        
        elif file_path.endswith('.csv'):
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                products = list(reader)
        
        print(f"✅ Loaded {len(products)} products from {file_path}")
        return products
        
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        return products

def save_price_data(data, filename='price_history.json'):
    """Save price data to JSON file"""
    try:
        # Load existing data
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        else:
            existing_data = []
        
        # Add new data
        existing_data.append(data)
        
        # Save updated data
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Results saved to {filename}")
        
    except Exception as e:
        print(f"❌ Error saving data: {e}")

def track_prices_once(products):
    """Track prices for all products once"""
    print(f"\n🔍 Starting price tracking at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    all_results = []
    
    for product in products:
        product_name = product.get('name', 'Unknown Product')
        print(f"\nTracking: {product_name}")
        
        product_results = {
            'timestamp': datetime.now().isoformat(),
            'product_name': product_name,
            'prices': {}
        }
        
        # Track Amazon if URL provided
        if product.get('amazon_url'):
            platform, price, price_num = scrape_product_price(product['amazon_url'], product_name)
            if price:
                product_results['prices']['amazon'] = {
                    'price_text': price,
                    'price_numeric': price_num
                }
        
        # Track Flipkart if URL provided
        if product.get('flipkart_url'):
            platform, price, price_num = scrape_product_price(product['flipkart_url'], product_name)
            if price:
                product_results['prices']['flipkart'] = {
                    'price_text': price,
                    'price_numeric': price_num
                }
        
        all_results.append(product_results)
        
        # Add delay between products
        time.sleep(random.uniform(2, 5))
    
    # Save results
    save_price_data(all_results)
    print(f"\n✅ Tracking completed for {len(products)} products!")
    return all_results

def create_sample_products_file():
    """Create sample products file"""
    sample_products = [
        {
            "name": "Samsung Galaxy F15 5G",
            "amazon_url": "https://www.amazon.in/Samsung-Galaxy-Groovy-Violet-Storage/dp/B0CY9PHSZJ/ref=sr_1_3?crid=3Q1F4Q5JFP3I1",
            "flipkart_url": "https://www.flipkart.com/samsung-galaxy-f15-5g-groovy-violet-128-gb/p/itmd0aaf528709de?pid=MOBGYBAVSDFYZFNY"
        },
        {
            "name": "iPhone 15",
            "amazon_url": "https://www.amazon.in/Apple-iPhone-15-128-GB/dp/B0CHX1W1XY",
            "flipkart_url": "https://www.flipkart.com/apple-iphone-15-blue-128-gb/p/itm6ac6485515ae4"
        }
    ]
    
    # Save as JSON
    with open('sample_products.json', 'w', encoding='utf-8') as f:
        json.dump(sample_products, f, indent=2, ensure_ascii=False)
    
    # Save as CSV
    with open('sample_products.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['name', 'amazon_url', 'flipkart_url'])
        writer.writeheader()
        writer.writerows(sample_products)
    
    print("✅ Sample files created:")
    print("   - sample_products.json")
    print("   - sample_products.csv")

def start_daily_automation(products, schedule_time="09:00"):
    """Start daily automation"""
    print(f"⏰ Scheduling daily price tracking at {schedule_time}")
    
    def job():
        try:
            track_prices_once(products)
        except Exception as e:
            print(f"❌ Error in scheduled job: {e}")
    
    schedule.every().day.at(schedule_time).do(job)
    
    print("🤖 Automation started! Press Ctrl+C to stop.")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        print("\n⏹️ Automation stopped.")

def track_single_product():
    """Track a single product manually"""
    print("\n📱 Single Product Tracker")
    print("-" * 30)
    
    name = input("Product name: ").strip()
    if not name:
        name = "Unknown Product"
    
    amazon_url = input("Amazon URL (optional): ").strip()
    flipkart_url = input("Flipkart URL (optional): ").strip()
    
    if not amazon_url and not flipkart_url:
        print("❌ At least one URL is required!")
        return
    
    product = {
        'name': name,
        'amazon_url': amazon_url,
        'flipkart_url': flipkart_url
    }
    
    track_prices_once([product])

def main():
    print("🛒 ENHANCED PRICE TRACKER")
    print("=" * 30)
    print("1. Create sample files")
    print("2. Track prices once")
    print("3. Start daily automation")
    print("4. Track single product")
    
    choice = input("\nChoice (1-4): ").strip()
    
    if choice == '1':
        create_sample_products_file()
    
    elif choice == '2':
        file_path = input("Products file path: ").strip()
        if not file_path:
            file_path = "sample_products.json"
        
        products = load_products_from_file(file_path)
        if products:
            track_prices_once(products)
    
    elif choice == '3':
        file_path = input("Products file path: ").strip()
        if not file_path:
            file_path = "sample_products.json"
        
        products = load_products_from_file(file_path)
        if not products:
            return
        
        schedule_time = input("Daily time (HH:MM, default 09:00): ").strip()
        if not schedule_time:
            schedule_time = "09:00"
        
        # Ask if user wants to run once now
        run_now = input("Run once now? (y/n): ").strip().lower()
        if run_now == 'y':
            track_prices_once(products)
        
        start_daily_automation(products, schedule_time)
    
    elif choice == '4':
        track_single_product()
    
    else:
        print("❌ Invalid choice!")

if __name__ == "__main__":
    main()