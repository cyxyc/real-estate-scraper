from selenium import webdriver
from bs4 import BeautifulSoup
import os
import re
import time  
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd


def login(browser: webdriver):
    # Go to the seznam.cz login page
    browser.get("https://login.szn.cz/")

    # Find and fill the username field
    username_field = browser.find_element(By.ID, "login-username")
    username_field.send_keys(os.getenv('EMAIL_LOGIN'))
    username_field.send_keys(Keys.RETURN)

    # Find the password field
    try:
        password_field = browser.find_element(By.ID, "login-password")
        print("Password field found")
    except:
        print("Password field not found")

    # Enter your password
    
    password_field.send_keys(os.getenv('EMAIL_PASSWORD'))

    username_field.send_keys(Keys.RETURN)
    print("heslo zadano a enternuto")
    # Find the login button
    login_button = browser.find_element(By.XPATH, '//button[@type="submit"]')
    login_button.click()


def get_HTML(browser: webdriver, url: str, scrape, filename: str, save: bool = True) -> str:
    """
    Navigate to the page and get the page source, or read it from a file if it already exists.

    Args:
    browser (webdriver): The webdriver instance to use.
    url (str): The URL to navigate to.
    filename (str): The name of the file to read from or write to.

    Returns:
    str: The source of the page.
    
    """
    
    filename = f'{filename}.txt'
    #TODO: delete this if statement when you are done with development
    if scrape == False:

        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        time.sleep(0.8)
        browser.get(url)
        time.sleep(0.5)
        html =  browser.execute_script("return document.body.innerHTML")
        time.sleep(0.3)

        # Write the HTML to the file
        if save == True:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html)
        return html

def find_tags(browser: webdriver, url: str, purpose, scrape, save, filename: str) -> list:
    """
    Get the list of URLs of each iteam from the main page.

    Args:
    browser (webdriver): The webdriver instance to use.
    url (str): The URL of the main page.
    main (bool): True if the page is the main page, False otherwise.

    Returns:
    list: A list of URLs.
    """
    # Get the HTML of the main page
    page_html = get_HTML(browser, url, scrape, filename, save)
    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(page_html, 'html.parser')
    if purpose == 'get_pages':
        find_pages = soup.find_all('a', attrs={'ng-href': re.compile("^/hledani")})
        if len(find_pages) == 0:
            return [url]
        pages_urls = set([page.get('ng-href') for page in find_pages])
        pages_urls = ['https://www.sreality.cz' + page_url for page_url in pages_urls]
        print("pocet stranek:", len(pages_urls))
        print(pages_urls)  
        return sorted(pages_urls)

    elif purpose == 'get_items_urls':
  
        find_items = soup.find_all('a', class_='title')
        items_urls = ['https://www.sreality.cz'+ item.get('href') for item in find_items]
        print("pocet inzeratu :", len(items_urls))
        print(items_urls)
        return items_urls
    
    elif purpose == 'get_details':
   
        find_title = soup.find_all('span', class_='name ng-binding')
        title = find_title[0].text.replace('\xa0', ' ')
        find_price = soup.find_all('span', class_='norm-price ng-binding')
        price = find_price[0].text.replace('\xa0', '').replace('\xa0', '').replace("Kč", "").replace(" za měsíc","")
        find_location = soup.find_all('span', class_='location-text ng-binding')
        location= find_location[0].text
        find_description = soup.find_all('div', class_='description ng-binding')
        description = " ".join([p.text for p in find_description[0].find_all('p')]).replace('\xa0', '')
        # plocha: tohle nefunguje protoze pozice v tabulce neni konstanta:
        # find_area = soup.find_all('span', class_='ng-binding ng-scope')
        # area = int(find_area[7].text.replace('\xa0', ' '))
        area = title.split(" ")[-2]

        # Get photos of the item
        noscripts = soup.find_all('noscript')
        img_urls = []
        for noscript in noscripts:
            img = noscript.find('img')
            if img is not None:
                img_urls.append(img.get('src'))
                #tady bych mohl pripichnout upload na imgur

        # Now img_urls contains all the image URLs from img tags within noscript tags
        print(img_urls)

        
        return [title, price, location, description, area, img_urls]



# get_photos = soup.find_all('img', class_='ob-c-gallery__img')
# photos_url = [img.get('src') for img in get_photos]



# Now img_urls contains all the image URLs




def main():
    # Set up the Selenium driver
    browser = webdriver.Chrome()
    login(browser)
    # main_url = 'https://www.sreality.cz/hledani/prodej/byty/frydek-mistek?velikost=2%2B1,2%2Bkk'
    main_url = 'https://www.sreality.cz/hledani/prodej/ostatni/garaze/frydek-mistek'
    pages_urls = find_tags(browser, main_url, purpose = 'get_pages', filename = "default_file_name", scrape = True, save = False)
    
    #TODO: to restartovani asi bude potreba delat i v tom for cyklu
    # browser.quit()
    # browser = webdriver.Chrome()

    counter_try, counter_succ, fails = 0, 0, 0
    df = []
    MAX_RETRIES = 3
   
    for page_url in pages_urls:
        
        # time.sleep(3)
        # browser.quit()
        # browser = webdriver.Chrome()
        # Get the URLs from the main page
        items_urls = find_tags(browser, page_url, purpose = 'get_items_urls', scrape = True, filename = 'scraped_HTML', save = False)
     
    
        for i, item_url in enumerate(items_urls):
            for attempt in range(MAX_RETRIES):
                try:
                    counter_try += 1
                    details = find_tags(browser, item_url, purpose = 'get_details', scrape = True, filename = item_url[-7:], save = False)                    
                    counter_succ += 1
                    df.append(details)
                    break  # If the request was successful, break the loop
                except IndexError as e:
                    print("************************************************")
                    print(f"Error on attempt {attempt + 1}: {e}")
                    print("************************************************")
                    time.sleep(3)  # Wait a bit before retrying
                    fails += 1

    df = pd.DataFrame(df)
    df.to_csv('df2.csv', index=False)
    print(counter_try, counter_succ, fails)
    print(len(df))
    # Quit the webdriver
    browser.quit()



if __name__ == "__main__":
    #TODO: delete "scrape" when you are done with development
    

    main()

