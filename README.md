# Enhanced Price Tracker

A robust Python-based price tracking tool that monitors product prices across Amazon India and Flipkart. Features automated daily tracking, price history, and anti-bot detection evasion.

## Features

- **Multi-Platform Support**: Track prices from Amazon India and Flipkart
- **Robust Scraping**: Advanced anti-bot detection evasion with user-agent rotation and retry mechanisms
- **Automated Scheduling**: Set up daily price tracking at your preferred time
- **Multiple Input Formats**: Support for JSON and CSV input files
- **Price History**: Automatic saving of all price data with timestamps
- **Single Product Tracking**: Quick manual tracking for individual products
- **Comprehensive Error Handling**: Graceful handling of network issues and site changes

## Requirements

### Dependencies
```bash
pip install requests beautifulsoup4 schedule
```

### System Requirements
- Python 3.6+
- Internet connection

## Installation & Usage

### Quick Start
1. Run the script: `python price_tracker.py`
2. Choose option 1 to create sample files
3. Edit the generated files with your product URLs
4. Run again and choose option 2 to start tracking

## Input File Formats

### JSON Format
```json
[
  {
    "name": "Samsung Galaxy F15 5G",
    "amazon_url": "https://www.amazon.in/Samsung-Galaxy-Groovy-Violet-Storage/dp/B0CY9PHSZJ",
    "flipkart_url": "https://www.flipkart.com/samsung-galaxy-f15-5g-groovy-violet-128-gb/p/itmd0aaf528709de"
  },
  {
    "name": "iPhone 15 Pro",
    "amazon_url": "https://www.amazon.in/Apple-iPhone-15-Pro-128GB/dp/B0CHX2RDCX",
    "flipkart_url": ""
  }
]
```

### CSV Format
```csv
name,amazon_url,flipkart_url
Samsung Galaxy F15 5G,https://www.amazon.in/Samsung-Galaxy-Groovy-Violet-Storage/dp/B0CY9PHSZJ,https://www.flipkart.com/samsung-galaxy-f15-5g-groovy-violet-128-gb/p/itmd0aaf528709de
iPhone 15 Pro,https://www.amazon.in/Apple-iPhone-15-Pro-128GB/dp/B0CHX2RDCX,
```

## Usage Options

### Option 1: Create Sample Files
Generates `sample_products.json` and `sample_products.csv` with example products that you can edit with your actual URLs.

### Option 2: Track Prices Once
Runs price tracking immediately for all products in your input file. Results are saved to `price_history.json`.

### Option 3: Start Daily Automation
Schedules automatic price tracking at a specified time. Runs continuously until stopped with Ctrl+C.

### Option 4: Track Single Product
Manual input mode for quick testing of individual products without creating input files.

## Output Format

### Console Output
```
Starting price tracking at 2025-06-14 10:30:15
==================================================

Tracking: Samsung Galaxy F15 5G
  Scraping Samsung Galaxy F15 5G...
  Amazon: ₹12,999
  Flipkart: ₹13,499

Results saved to price_history.json
Tracking completed for 1 products!
```

### Price History File
Results are automatically saved to `price_history.json` with timestamps and structured price data:

```json
[
  {
    "timestamp": "2025-06-14T10:30:15.123456",
    "product_name": "Samsung Galaxy F15 5G",
    "prices": {
      "amazon": {
        "price_text": "₹12,999",
        "price_numeric": 12999.0
      },
      "flipkart": {
        "price_text": "₹13,499",
        "price_numeric": 13499.0
      }
    }
  }
]
```

## Configuration

### Anti-Bot Features
- User-agent rotation with multiple browser identities
- Random delays between requests (3-6 seconds for Amazon, 1-3 for Flipkart)
- Automatic retry mechanism with exponential backoff
- Complete browser-like headers and session management

### Customizable Settings
- **Tracking Schedule**: Set any time in HH:MM format (24-hour)
- **Input Files**: Use any JSON or CSV file path
- **Retry Logic**: 3 attempts for failed requests with increasing delays

## Troubleshooting

### Common Issues

**"Price not found" errors**
- Website structure changes or anti-bot detection triggered
- Solution: Wait a few minutes before retrying, verify URLs work in browser

**Connection timeouts**
- Network issues or rate limiting
- Solution: Check internet connection, increase delays between requests

**File not found errors**
- Incorrect file path specified
- Solution: Use absolute file paths or ensure files are in working directory

### Best Practices
- Use clean product URLs without tracking parameters
- Don't run the tool too frequently to avoid IP blocking
- Test URLs manually in browser before adding to input files
- Monitor console output for error messages and warnings

## Example Workflow

### Daily Price Monitoring Setup
```bash
# 1. Create sample files
python price_tracker.py  # Choose option 1

# 2. Edit sample_products.json with your products
# 3. Start automation
python price_tracker.py  # Choose option 3
# Enter: sample_products.json
# Enter: 09:00
# Run now: y
```

## Limitations

- Designed specifically for Amazon India and Flipkart India
- May break if websites update their HTML structure
- Subject to rate limiting if used too aggressively
- Cannot capture prices loaded dynamically via JavaScript

## Disclaimer

This tool is intended for educational and personal use only. Users must respect the terms of service of target websites and use the tool responsibly. The authors assume no responsibility for misuse or any consequences arising from the use of this software.
