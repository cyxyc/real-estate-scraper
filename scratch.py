from selenium import webdriver
from bs4 import BeautifulSoup
import os
import re
import time  
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def login(browser: webdriver):
    # Go to the seznam.cz login page
    browser.get("https://login.szn.cz/")

    # Find and fill the username field
    username_field = browser.find_element(By.ID, "login-username")
    username_field.send_keys("magorjoe@seznam.cz")
    username_field.send_keys(Keys.RETURN)

    # Find the password field
    try:
        password_field = browser.find_element(By.ID, "login-password")
        print("Password field found")
    except:
        print("Password field not found")

    # Enter your password
    password_field.send_keys("akculakcul")
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
        # Navigate to the page and get the page source
        #funguje to kdyz yapnu vsechny 3 time sleepy
        time.sleep(0.5)
        browser.get(url)
        time.sleep(0.5)
        html =  browser.execute_script("return document.body.innerHTML")
        time.sleep(0.5)
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
  
    if purpose == 'get_details':
    
        find_title = soup.find_all('span', class_='name ng-binding')
        title = find_title[0].text.replace('\xa0', ' ')
        find_price = soup.find_all('span', class_='norm-price ng-binding')
        price = int(find_price[0].text.replace('\xa0', '').replace('\xa0', '').replace("Kč", "").replace(" za měsíc",""))
        find_location = soup.find_all('span', class_='location-text ng-binding')
        location= find_location[0].text
        find_description = soup.find_all('div', class_='description ng-binding')
        description = " ".join([p.text for p in find_description[0].find_all('p')]).replace('\xa0', '')
        # plocha: tohle nefunguje protoze pozice v tabulce neni konstanta:
        # find_area = soup.find_all('span', class_='ng-binding ng-scope')
        # area = int(find_area[7].text.replace('\xa0', ' '))
        area = title.split(" ")[-2]
        
        return [title, price, location, description, area]

def main():
    # Set up the Selenium driver
    browser = webdriver.Chrome()
    # login(browser)
    df = []

    items_urls = ["https://www.sreality.cz/detail/pronajem/ostatni/garaz/frydek-mistek-frydek-tr--t--g--masaryka/2804163916", 
             "https://www.sreality.cz/detail/pronajem/ostatni/garaz/trinec--/2456143180",
             "https://www.sreality.cz/detail/pronajem/ostatni/garaz/frydek-mistek--/706819404",
             "https://www.sreality.cz/detail/pronajem/ostatni/garaz/frydek-mistek--/3699123532"]


             
    details = find_tags(browser, items_urls[3], purpose = 'get_details', scrape = True, filename = "jebka", save = True)                    
    
    df.append(details)

    print(df)
    # Quit the webdriver
    browser.quit()

if __name__ == "__main__":
    #TODO: delete "scrape" when you are done with development
    

    main()

