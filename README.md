# Enhanced Price Tracker

A Python-based price tracking tool to monitor product prices across Amazon India and Flipkart. Supports automated daily tracking, price history management, and basic anti-bot detection evasion.

## Features

* Multi-platform support: Amazon India and Flipkart
* Automated scheduling for daily price tracking
* JSON and CSV input file support
* Price history logging with timestamps
* Single product manual tracking option
* Basic anti-bot handling with random delays and user-agent headers

## Requirements

* Python 3.6+
* Internet connection

### Dependencies

```bash
pip install requests beautifulsoup4 schedule
```

## Quick Start

1. Run: `python price_tracker.py`
2. Select **Option 1** to generate sample input files.
3. Edit the sample files with your product URLs.
4. Run again and select **Option 2** to begin price tracking.

## Input File Formats

### JSON Example

```json
[
  {
    "name": "Samsung Galaxy F15 5G",
    "amazon_url": "https://www.amazon.in/Samsung-Galaxy-Groovy-Violet-Storage/dp/B0CY9PHSZJ",
    "flipkart_url": "https://www.flipkart.com/samsung-galaxy-f15-5g-groovy-violet-128-gb/p/itmd0aaf528709de"
  }
]
```

### CSV Example

```csv
name,amazon_url,flipkart_url
Samsung Galaxy F15 5G,https://www.amazon.in/Samsung-Galaxy-Groovy-Violet-Storage/dp/B0CY9PHSZJ,https://www.flipkart.com/samsung-galaxy-f15-5g-groovy-violet-128-gb/p/itmd0aaf528709de
```

## Usage Options

* **Option 1:** Generate sample input files
* **Option 2:** Run one-time price tracking
* **Option 3:** Set up daily automated tracking
* **Option 4:** Manually track a single product

## Output Example

Console:

```
Tracking: Samsung Galaxy F15 5G
Amazon: ₹12,999
Flipkart: ₹13,499
```

Results are saved in `price_history.json` with timestamps.

## Configuration

* Customizable tracking time (24-hour format)
* Supports both JSON and CSV input files
* Retry mechanism with randomized delays to reduce detection

## Troubleshooting

* **Price not found:** The website structure may have changed.
* **Timeout errors:** Check your internet connection or increase delays.
* **File not found:** Verify file paths and input file formats.

## Notes

* Designed specifically for Amazon India and Flipkart India.
* May require updates if website structures change.
* Not optimized for dynamically loaded (JavaScript-only) prices.
* Use responsibly and adhere to website terms of service.

## Disclaimer

This project is for educational and personal use only. The author is not responsible for misuse or any consequences arising from the use of this software.

