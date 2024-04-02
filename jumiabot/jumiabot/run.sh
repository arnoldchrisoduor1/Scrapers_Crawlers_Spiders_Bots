#!/bin/bash

# Run the scrapy crawl command
echo "Executing Jumia scraper..."
scrapy crawl jumia &

# Define the path to the flag file
flag_file="C:/Users/arnol/OneDrive/Desktop/Data Analysis/Web-Scraping/jumiaspider/jumiaspider/scraping_done.flag"

# Loop until the flag file is created
while [ ! -f "$flag_file" ]; do
    sleep 10  # Adjust the sleep duration as needed (e.g., 10 seconds)
done

# Flag detected, sending email
echo "Flag detected. Sending email..."
# Invoke the emailconfig.py file
python emailconfig.py

# Delete the flag file
rm "$flag_file"
echo "Flag file deleted."
