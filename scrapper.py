from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd


driver_path = 'C:/Program Files/chromedriver/chromedriver.exe'
brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"

service = Service(executable_path=driver_path)

options = webdriver.ChromeOptions()
options.binary_location = brave_path



driver = webdriver.Chrome(service=service, options=options)


try:
    driver.get("https://www.essayforum.com/undergraduate/")
    driver.implicitly_wait(10)

    # Get the href with tag a and class name of "txtNr j"
    rows = driver.find_elements(By.CSS_SELECTOR, "a.txtNr.j")

    # Create a list to store messages
    messages = []

    # Create a list of dictionaries with title and link
    data = []
    for row in rows:
        data.append({
            "title": row.text,
            "link": row.get_attribute("href")
        })

    num = 0
    # Iterate over the links to get messages and insert it to the list of dictionaries from the start
    for d in data:
        if num < 60:
            driver.get(d["link"])
            driver.implicitly_wait(10)
            # Get the message by tag div and class name of "txtNr j"
            message = driver.find_element(By.CSS_SELECTOR, "div.pTx")
            # Insert the message to the list of dictionaries
            data[num]["message"] = message.text
            num += 1
        

    # Create a csv file that will store the data in csv format using pandas
    df = pd.DataFrame(data)
    df.to_csv("essayforum.csv", index=False)


finally:
    # Close the WebDriver at the end
    driver.quit()