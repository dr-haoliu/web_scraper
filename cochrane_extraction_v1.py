import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import os
import shutil

download_dir = 'downloaded/cochrane_extracted_studies'

main_url = 'https://www.cochranelibrary.com/en/search' # '?searchBy=1&searchText=%22Alzheimer+disease%22&isWordVariations=&resultPerPage=100&searchType=basic&forceTypeSelection=true&selectedType=review'

study_url_list =[]

disease_list = ['\"Alzheimer disease\"']
drug_list = ['hydroxychloroquine',
             'azithromycin',
             'remdesivir',
             'chloroquine',
             'tocilizumab',
             'anakinra',
             'convalescent plasma',
             'dexamethasone',
             'methylprednisolone',
             'sarilumab',
             'Ivermectin']

preferences = {
                "profile.default_content_settings.popups": 0,
                "download.default_directory": os.getcwd() + os.path.sep + download_dir + os.path.sep,
                "directory_upgrade": True
            }

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('prefs', preferences)

driver = webdriver.Chrome(executable_path='driver/chromedriver', options=chrome_options)

driver.get(main_url)
timeout = 5

final_results = []

try:
    search_box_present = EC.presence_of_element_located((By.ID, 'searchText'))
    WebDriverWait(driver, timeout).until(search_box_present)
    # Write what we be searched#
    search_box = driver.find_element(By.ID, 'searchText')


    # add time wait 2 seconds
    time.sleep(5)
    search_box.send_keys(disease_list[0])

    # Submit the text
    search_box.send_keys(Keys.RETURN)
    # search_element_present.text = disease_list[0]

    # add time wait 2 seconds
    time.sleep(15)

    # search_button_class = 'searchByBtn'
    # driver.find_element(By.CLASS_NAME, search_button_class).click()

    page_selector_css = '.select.justify-right.small'
    testing_cln = 'select-styled'
    my_selector = driver.find_element(By.CSS_SELECTOR, page_selector_css).find_element(By.CLASS_NAME, testing_cln)
    my_selector.click()
    time.sleep(3)

    page_selector_cls = 'select-options'
    menu = driver.find_element(By.CSS_SELECTOR, page_selector_css).find_element(By.CLASS_NAME, page_selector_cls)
    items = menu.find_elements_by_tag_name("li")
    for item in items:
        text = item.text
        print(text)
        if text == '50':
            item.click()
            driver.implicitly_wait(10)
            break
    time.sleep(10)

    # try:
    #     results_box_present = EC.presence_of_element_located((By.CLASS_NAME, 'search-results'))
    #     WebDriverWait(driver, 10).until(results_box_present)
    # except TimeoutException:
    #     print('timeout excption!')

    driver.implicitly_wait(10)
    result_items = driver.find_elements(By.CLASS_NAME, 'search-results-item')
    for item in result_items:
        item_element = item.find_element(By.CLASS_NAME, 'result-title')
        item_name = item_element.text
        print(item_name)
        item_url = item_element.find_element(By.TAG_NAME, 'a').get_attribute('href')
        print(item_url)
        study_url_list.append([item_name, item_url])
        driver.implicitly_wait(1)

except TimeoutException:
    print("Timed out waiting for page to load")


print('here')

for a_url in study_url_list:
    study_title = a_url[0]
    print(f'Processing study:\t {study_title}')
    study_url = a_url[1]
    driver.get(study_url)

    nav_links = driver.find_elements(By.CLASS_NAME, 'cdsr-nav-link')

    for nav_link in nav_links:
        nav_text = nav_link.find_element_by_tag_name('a').text
        if nav_text.lower() == 'picos':
            print(nav_text)
            nav_link.click()
            break

    time.sleep(3)
    pico_section = 'pico-section'
    try:
        pico_section_present = EC.presence_of_element_located((By.CLASS_NAME, pico_section))
        WebDriverWait(driver, timeout).until(pico_section_present)
    except TimeoutException:
        print("Timed out waiting for page to load")
        continue

    pico_click_on = driver.find_element(By.CSS_SELECTOR, '.title.section-collapse-title.collapsed').click()
    time.sleep(2)
    p_list = []
    i_list = []
    c_list = []
    o_list = []

    pico_table = driver.find_element(By.CLASS_NAME, 'pico-table')
    pico_p = pico_table.find_element(By.CSS_SELECTOR, '.pico-column.Population')
    pico_terms = pico_p.find_element(By.CLASS_NAME, 'pico-terms')
    for pico_term in pico_terms.find_elements(By.CSS_SELECTOR, 'li'):
        text = pico_term.find_element_by_tag_name('a').text
        p_list.append(text)

    pico_i = pico_table.find_element(By.CSS_SELECTOR, '.pico-column.Intervention')
    pico_terms = pico_i.find_element(By.CLASS_NAME, 'pico-terms')
    for pico_term in pico_terms.find_elements(By.CSS_SELECTOR, 'li'):
        text = pico_term.find_element_by_tag_name('a').text
        i_list.append(text)

    pico_c = pico_table.find_element(By.CSS_SELECTOR, '.pico-column.Comparison')
    pico_terms = pico_c.find_element(By.CLASS_NAME, 'pico-terms')
    for pico_term in pico_terms.find_elements(By.CSS_SELECTOR, 'li'):
        text = pico_term.find_element_by_tag_name('a').text
        c_list.append(text)

    pico_o = pico_table.find_element(By.CSS_SELECTOR, '.pico-column.Outcome')
    pico_terms = pico_o.find_element(By.CLASS_NAME, 'pico-terms')
    for pico_term in pico_terms.find_elements(By.CSS_SELECTOR, 'li'):
        text = pico_term.find_element_by_tag_name('a').text
        o_list.append(text)

    print(p_list)
    print(i_list)
    print(c_list)
    print(o_list)

    time.sleep(2)
    nav_links = driver.find_elements(By.CLASS_NAME, 'cdsr-nav-link')
    for nav_link in nav_links:
        nav_text = nav_link.find_element_by_tag_name('a').text
        if nav_text.lower() == 'references':
            print(nav_text)
            nav_link.click()
            break

    time.sleep(3)
    # lock_modal = 'scolaris-modal-close'
    # try:
    #     pico_section_present = EC.presence_of_element_located((By.CLASS_NAME, lock_modal))
    #     WebDriverWait(driver, timeout).until(pico_section_present)
    #     continue
    # except TimeoutException:
    #     print("Timed out waiting for page to load")

    included_studies_header = 'bibliography-section'
    try:
        element_present = EC.presence_of_element_located((By.CLASS_NAME, included_studies_header))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")

    pubmed_list = []
    study_groups = driver.find_elements(By.CLASS_NAME, included_studies_header)
    for study_citation in study_groups:
        citation_groups = study_citation.find_elements(By.CLASS_NAME, 'citation-link-group')
        for cg in citation_groups:
            citations = cg.find_elements(By.CLASS_NAME, 'citation-link')
            for citation in citations:
                citation_url = citation.get_attribute('href')
                if 'pubmed' in citation_url:
                    print(citation_url)
                    pubmed_list.append(citation_url)
    final_results.append([study_title, study_url, p_list, i_list, c_list, o_list, pubmed_list])

    time.sleep(2)

driver.quit()

df = pd.DataFrame(final_results, columns=['study_title', 'study_url', 'p_list', 'i_list', 'c_list', 'o_list', 'included_pubmed_url'])

print(df.head())

df.to_csv('cochrane_results_v2.csv', index=False, encoding='utf-8', sep='\t')



    # central_search_link = "central-search-link"
    # try:
    #     element_present = EC.presence_of_element_located((By.CLASS_NAME, central_search_link))
    #     WebDriverWait(driver, timeout).until(element_present)
    #     driver.find_element(By.CLASS_NAME, central_search_link).click()
    # except TimeoutException:
    #     print("Timed out waiting for page to load")
    #
    # time.sleep(5)
    #
    # search_filter = '.filter-section.filter-section-type-source'
    # try:
    #     element_present = EC.presence_of_element_located((By.CSS_SELECTOR, search_filter))
    #     WebDriverWait(driver, timeout).until(element_present)
    #
    #     filters = driver.find_elements(By.CLASS_NAME, 'facet-title')
    #     for filter in filters:
    #         title = filter.text
    #         if title.lower() == 'pubmed':
    #             print(title)
    #             filter.click()
    #
    # except TimeoutException:
    #     print("Timed out waiting for page to load")
    #
    # print('here')

#



# for drug in drug_list:
#     input_file_name = 'downloaded/{}_pmids_litcovid.tsv'.format(drug)
#
#     df = pd.read_csv(input_file_name, sep='\t', comment='#')
#     print(df.head())
#
#     pmid_list = df.pmid
#
#     publication_type_list = ['Randomized Controlled Trial', 'Clinical Trial', 'Controlled Clinical Trial', 'Observational Study']
#
#
#     for id in pmid_list:
#
#         driver.get("https://pubmed.ncbi.nlm.nih.gov/{}".format(id))
#         timeout = 5
#         try:
#             element_present = EC.presence_of_element_located((By.ID, 'article-details'))
#             WebDriverWait(driver, timeout).until(element_present)
#         except TimeoutException:
#             print("Timed out waiting for page to load")
#
#         try:
#             publication_type = 'publication-type'
#             pub_type = ''
#             pub_type_element_present = EC.presence_of_element_located((By.CLASS_NAME, publication_type))
#             WebDriverWait(driver, timeout).until(pub_type_element_present)
#             pub_type = driver.find_element_by_class_name(publication_type).text
#             if pub_type not in publication_type_list:
#                 continue
#         except TimeoutException:
#             print('Timed out waiting for publicatio type to load')
#             continue
#
#
#         # save-results-panel-trigger id
#         try:
#             save_button_id = 'save-results-panel-trigger'
#             WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, save_button_id)))
#             driver.find_element_by_id(save_button_id).click()
#         except TimeoutException:
#             print("Timed out waiting for save button id")
#
#         # save-action-format
#         try:
#             selector_id = 'save-action-format'
#             WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, selector_id)))
#             select = Select(driver.find_element_by_id(selector_id))
#             # select by visible text
#             # select.select_by_visible_text('Banana')
#
#             # select by value
#             select.select_by_value('abstract')
#         except TimeoutException:
#             print("Timed out waiting for selector id")
#
#
#         try:
#             create_button_class = 'action-panel-submit' # action-panel-actions.
#             WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, create_button_class)))
#             driver.find_elements_by_class_name(create_button_class)[0].click()
#         except TimeoutException:
#             print("Timed out waiting for selector id")
#
#         # add time wait 2 seconds
#         time.sleep(2)
#         filename = max([download_dir + "/" + f for f in os.listdir(download_dir)], key=os.path.getctime)
#         shutil.move(filename, os.path.join(download_dir, drug+'_pubtype_' + pub_type + '_' + os.path.basename(filename)))
#         print('change name done')
#     # driver.close()
# driver.close()
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