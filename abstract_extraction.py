import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

driver = webdriver.Chrome(executable_path='driver/chromedriver.exe')

df = pd.read_csv('data/search.results.litcovid.tsv', sep='\t')
print(df.head())

pmid_list = df.pmid


for id in pmid_list:

    driver.get("https://pubmed.ncbi.nlm.nih.gov/{}".format(id))
    timeout = 5
    try:
        element_present = EC.presence_of_element_located((By.ID, 'article-details'))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")

    # save-results-panel-trigger id
    try:
        save_button_id = 'save-results-panel-trigger'
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, save_button_id)))
        driver.find_element_by_id(save_button_id).click()
    except TimeoutException:
        print("Timed out waiting for save button id")

    # save-action-format
    try:
        selector_id = 'save-action-format'
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, selector_id)))
        select = Select(driver.find_element_by_id(selector_id))
        # select by visible text
        # select.select_by_visible_text('Banana')

        # select by value
        select.select_by_value('abstract')
    except TimeoutException:
        print("Timed out waiting for selector id")


    try:
        create_button_class = 'action-panel-submit' # action-panel-actions.
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, create_button_class)))
        driver.find_elements_by_class_name(create_button_class)[0].click()
    except TimeoutException:
        print("Timed out waiting for selector id")

    # driver.close()
driver.close()
# driver.quit()

# results = []
# other_results = []
# content = driver.page_source
# soup = BeautifulSoup(content)
# for a in soup.findAll(attrs={'class': 'class'}):
#     name = a.find('a')
#     if name not in results:
#         results.append(name.text)
# for b in soup.findAll(attrs={'class': 'otherclass'}):
#     name2 = b.find('span')
#     other_results.append(name.text)
# series1 = pd.Series(results, name = 'Names')
# series2 = pd.Series(other_results, name = 'Categories')
# df = pd.DataFrame({'Names': series1, 'Categories': series2})
# df.to_csv('names.csv', index=False, encoding='utf-8')