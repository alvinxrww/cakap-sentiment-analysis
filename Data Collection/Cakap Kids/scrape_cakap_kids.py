from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

# chromedriver required
driver = webdriver.Chrome()
REVIEW_URL = "https://www.google.com/maps/place/Cakap+Kids+Academy+-+Gading+Serpong/@-6.2423194,106.6225413,15z/data=!4m6!3m5!1s0x2e69fd2d69de733b:0x9465c1d82f0acc1e!8m2!3d-6.2422827!4d106.6225304!16s%2Fg%2F11v3mhn3w_?entry=ttu"
driver.get(REVIEW_URL)

try:
    read_all_reviews_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='Gpq6kf fontTitleSmall'][contains(text(), 'Ulasan')]"))
    )
    read_all_reviews_button.click()
except:
    print("Could not find the 'Reviews' tab or it's not clickable.")
    quit()

# Scroll down to load more reviews within the modal
for i in range(25):
    try:
        modal_element = driver.find_element(By.CLASS_NAME, "m6QErb.DxyBCb.kA9KIf.dS8AEf ") # Scrollable element
    except:
        print("Could not find the scrollable element")
        quit()
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal_element)
    time.sleep(2) # small delay to load the review

page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')

# Retrieve the reviews
try:
    # review_elements = soup.find_all('div', {'class': 'wiI7pd', 'lang': False})
    review_elements = soup.find_all(By.CLASS_NAME, "wiI7pd")
except:
    print("Could not find the review elements")
    quit()

reviews = []
for element in review_elements:
    reviews.append(element.get_text())

driver.quit()

review_df = pd.DataFrame({
    "Reviews": reviews
})
REVIEWS_FILE_NAME = "reviews.csv"
review_df.to_csv(REVIEWS_FILE_NAME, index=False)