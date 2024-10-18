import requests
from bs4 import BeautifulSoup
from datetime import datetime
from colorama import Fore, Style, init
import time

# Initialize colorama
init()

# Set the URL
url = 'https://poweroutage.us/area/county/481'

# Previous value of customers_out to compare changes
previous_customers_out = None
n_reqs = 0
while True:
    # Make the request and parse the HTML
    response = requests.get(url)
    n_reqs = n_reqs + 1
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract the data
    customers_tracked = soup.find_all("div", class_="col-xs-4 col-sm-12")[0].get_text(strip=True)
    customers_out = soup.find_all("div", class_="col-xs-4 col-sm-12")[1].get_text(strip=True).replace(',', '')
    outage_percent = soup.find_all("div", class_="col-xs-4 col-sm-12")[2].get_text(strip=True)
    last_updated = soup.find("div", class_="col-xs-12 col-sm-7 hidden-md hidden-lg").find("item").get_text(strip=True)

    # Convert customers_out to an integer for comparison
    customers_out_value = int(customers_out)

    # Check if there is a previous value to compare
    if previous_customers_out is not None:
        if customers_out_value > previous_customers_out:
            color = Fore.RED  # More outages, color the line red
        elif customers_out_value < previous_customers_out:
            color = Fore.GREEN  # Fewer outages, color the line green
        else:
            color = Fore.YELLOW  # No change
    else:
        color = Fore.WHITE  # First run, no comparison

    # Print the output on a single line with color
    print(f"{color}[{str(n_reqs)}]Customers Tracked: {customers_tracked} | "
          f"Customers Out: {customers_out} | "
          f"Outage %: {outage_percent} | "
          f"Last Updated: {last_updated}{Style.RESET_ALL}")

    # Update the previous customers_out value for the next iteration
    previous_customers_out = customers_out_value

    # Wait for 5 minutes before the next request
    time.sleep(300)  # 300 seconds = 5 minutes
