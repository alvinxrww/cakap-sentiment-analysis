from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

# chromedriver required
driver = webdriver.Chrome()
app_url = "https://play.google.com/store/apps/details?id=com.duolingo"
driver.get(app_url)

# Click the "See all reviews" button to reveal more reviews
try:
    read_all_reviews_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//span[text()="See all reviews"]'))
    )
    read_all_reviews_button.click()
except:
    print("Could not find the 'See all reviews' button or it's not clickable.")

# Wait for the modal to appear
try:
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'VfPpkd-P5QLlc'))
    )
except:
    print("Modal did not appear or could not be found.")

# Scroll down to load more reviews within the modal
for i in range(50):
    modal_element = driver.find_element(By.CLASS_NAME, 'fysCi')
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal_element)
    time.sleep(2) # small delay to load the review

page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')

# Retrieve the reviews
h3YV2d_elements = soup.find_all('div', class_='h3YV2d')

reviews = []
for element in h3YV2d_elements:
    reviews.append(element.get_text())

driver.quit()

review_df = pd.DataFrame({
    "Reviews": reviews
})
review_df.to_csv("duolingo_reviews_no_index.csv", index=False)