import os
from RPA.HTTP import HTTP
from RPA.Tables import Tables
from RPA.PDF import PDF
from RPA.Dialogs import Dialogs
from variables import variables
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
dialog = Dialogs()
http = HTTP()
tables = Tables()
pdf = PDF()


def open_the_intranet_website():
    driver.get(variables.sparebin_url)

def ask_user_for_URL():
    dialog.add_text_input("URL", "download URL for the csv file")
    response = dialog.run_dialog()
    return response.URL


def download_csv_file(URL):
    http.download(URL, overwrite=True)


def get_rid_of_the_modal():
    #clicks on the "Ok" button to close popup
    driver.find_element_by_css_selector('#root > div > div.modal > div > div > div > div > div > button.btn.btn-dark').click()

def fill_and_submit_the_form_for_one_person(order):
    #1. Head
    select = Select(driver.find_element_by_id('head'))
    select.select_by_index(order['Head'])

    #2. Body
    body_css = ''.join(['#id-body-', order['Body']])
    driver.find_element_by_css_selector(body_css).click()

    #3. Legs
    inputElement = driver.find_element_by_css_selector('input.form-control')
    inputElement.send_keys(order["Legs"])

    #4. address
    inputElement = driver.find_element_by_id('address')
    inputElement.send_keys(order['Address'])

    # click preview
    driver.find_element_by_id('preview').click()

    #click order until it succeeds
    while True:
        try:
            WebDriverWait(driver, 1).until(EC.invisibility_of_element((By.ID, "receipt")))
            driver.find_element_by_id('order').click()
            continue
        except:
            break

def collect_the_results(receipt_number):
    #get the receipt text and add it to a pdf file
    receipt = driver.find_element_by_id('receipt').get_attribute('outerHTML')
    pdf_file_path = ''.join(['output/receipts/receipts_', receipt_number,'.pdf'])
    pdf.html_to_pdf(receipt, pdf_file_path)
    return pdf_file_path

def screenshot_the_preview(receipt_number):
    #take a screenshot of the robot image
    screenshot_path = ''.join(['output/receipts/receipts_', receipt_number,'.png'])
    driver.find_element_by_css_selector('#robot-preview-image').screenshot(screenshot_path)
    return screenshot_path
    
def embed_the_screenshot_in_the_pdf_and_remove_png(pdf_file, screenshot):
    pdf.add_files_to_pdf(files=[screenshot], target_document=pdf_file, append=True)
    os.remove(screenshot)
    

def order_another_robot():
    driver.find_element_by_id('order-another').click()

def main():
    try:
        open_the_intranet_website()
        link = ask_user_for_URL()
        download_csv_file(link)
        robot_orders = tables.read_table_from_csv('orders.csv', columns=["Order number", "Head", "Body", "Legs", "Address"])
        for order in robot_orders:
            get_rid_of_the_modal()
            fill_and_submit_the_form_for_one_person(order)
            pdf_file = collect_the_results((order)["Order number"])
            screenshot = screenshot_the_preview((order)["Order number"])
            embed_the_screenshot_in_the_pdf_and_remove_png(pdf_file, screenshot)
            order_another_robot()
    finally:
         driver.close()
        
if __name__ == "__main__":
    main()