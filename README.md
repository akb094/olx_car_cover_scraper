# olx_car_cover_scraper

This is a simple Python script built using Selenium to scrape product listings (e.g., car covers) from OLX India and save the results to a CSV file.

It’s designed to:

    Visit OLX search results page-by-page

    Wait for listings to load

    Extract product details like title, price, location, and link

    Save them into car_cover_olx_results.csv

What You'll Need

    Python 3.7+

    Google Chrome installed

    ChromeDriver (matching your Chrome version)

    Virtual environment with these packages:

        selenium

        pandas

Notes

    OLX may block automated scraping or delay content loading. The script tries to wait for elements, but if it times out, it will save the page for manual debugging.
