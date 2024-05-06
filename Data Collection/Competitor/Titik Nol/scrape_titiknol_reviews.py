from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

# chromedriver required
driver = webdriver.Chrome()
REVIEW_URL = "https://www.google.com/search?q=titik+nol+english+course&sca_esv=c33f69b4e642d21b&rlz=1C1YTUH_enID1041ID1041&ei=R6A4ZvnmH4G7seMP66-vwA8&oq=titik+nol+&gs_lp=Egxnd3Mtd2l6LXNlcnAiCnRpdGlrIG5vbCAqAggBMgsQLhiABBjHARivATIKEAAYgAQYQxiKBTIKEAAYgAQYQxiKBTIKEC4YgAQYQxiKBTIOEC4YgAQYxwEYjgUYrwEyBRAAGIAEMgsQLhiABBjHARivATILEC4YgAQYxwEYrwEyChAAGIAEGEMYigUyBRAAGIAESM4OUJ4EWJ4EcAF4AZABAJgBd6ABd6oBAzAuMbgBAcgBAPgBAZgCBKAClxDCAgoQABiwAxjWBBhHwgINEAAYgAQYsAMYQxiKBcICHBAuGIAEGLADGEMYxwEYyAMYigUYjgUYrwHYAQHCAhkQLhiABBiwAxhDGMcBGMgDGIoFGK8B2AEBwgITEC4YgAQYsAMYQxjIAxiKBdgBAcICGhAuGIAEGMcBGK8BGJcFGNwEGN4EGOAE2AECmAMAiAYBkAYUugYGCAEQARgIugYGCAIQARgUkgcLMS4xLjUtMS4wLjGgB_AT&sclient=gws-wiz-serp"
driver.get(REVIEW_URL)

# Click the "See all reviews" button to reveal more reviews
try:
    read_all_reviews_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//span[text()="Lihat semua ulasan Google"]'))
    )
    read_all_reviews_button.click()
except:
    print("Could not find the 'Lihat semua ulasan Google' button or it's not clickable.")
    quit()

# Wait for the modal to appear
try:
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'review-dialog-body'))
    )
except:
    print("Modal did not appear or could not be found.")

# Scroll down to load more reviews within the modal
for i in range(30):
    modal_element = driver.find_element(By.CLASS_NAME, 'review-dialog-list')
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal_element)
    time.sleep(2) # small delay to load the review

page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')

# Retrieve the reviews
review_elements = soup.find_all('span', {'data-expandable-section': True})

reviews = []
for element in review_elements:
    reviews.append(element.get_text())

driver.quit()

review_df = pd.DataFrame({
    "Reviews": reviews
})
REVIEWS_FILE_NAME = "Data Collection/Competitor/Titik Nol/titiknol_reviews_no_index.csv"
review_df.to_csv(REVIEWS_FILE_NAME, index=False)

# Re-read the csv to remove empty lines because they
# are undetected in the previous df
df = pd.read_csv(REVIEWS_FILE_NAME)
df.dropna(inplace=True)
df.to_csv(REVIEWS_FILE_NAME, index=False)