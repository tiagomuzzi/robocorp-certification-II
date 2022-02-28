import os

from Browser import Browser
from Browser.utils.data_types import SelectAttribute
from RPA.HTTP import HTTP
from RPA.Tables import Tables
from RPA.PDF import PDF
from RPA.Archive import Archive
from RPA.Dialogs import Dialogs
from RPA.Robocorp.Vault import Vault


browser = Browser()

def open_the_intranet_website():
    browser.open_browser('https://robotsparebinindustries.com/')

def main():
    try:
        open_the_intranet_website()
    finally:
        browser.playwright.close()

if __name__ == "__main__":
    main()


# *** Settings ***
# Documentation     This robot places orders in the mock websiteRobotSpareBin Inc.
# ...               The input is a URL provided by the user. (https://robotsparebinindustries.com/orders.csv)
# ...               It will:
# ...               - access the website to place orders, stored in a vault.
# ...               - Save the order HTML receipt as a PDF.
# ...               - Save a screenshot of the ordered robot.
# ...               - attach a screenshot to the PDF.
# ...               - Create a ZIP archive of the receipts and the images.
# Library           RPA.Browser.Selenium    auto_close=${False}
# Library           RPA.HTTP
# Library           RPA.Tables
# Library           RPA.PDF
# Library           RPA.Archive
# Library           RPA.Dialogs
# Library           OperatingSystem
# Library           RPA.Robocorp.Vault

# *** Tasks ***
# Order robots from RobotSpareBin Inc.
#     get the url from a vault and open the intranet website
#     ${URL}=    Get download URL From User
#     download the csv file    ${URL}
#     ${robot_orders}=    Read table from CSV    orders.csv
#     FOR    ${robot_order}    IN    @{robot_orders}
#         get rid of the annoying modal
#         Fill and submit the form for one person    ${robot_order}
#         ${PDF}=    collect the results    ${robot_order}[Order number]
#         ${screenshot}=    screenshot the preview    ${robot_order}[Order number]
#         embed the screenshot in the pdf and remove the png    ${screenshot}    ${PDF}
#         order another robot
#     END
#     create zip package from pdf files
#     [Teardown]    Close Browser

# *** Keywords ***
# get the url from a vault and open the intranet website
#     ${secret}=    Get Secret    sparebin
#     Open Available Browser    ${secret}[website_url]
#     Wait Until Element Is Visible    css:#root > div > div.modal > div > div > div > div > div > button.btn.btn-dark

# get rid of the annoying modal
#     Click Button    css:#root > div > div.modal > div > div > div > div > div > button.btn.btn-dark

# Get download URL From User
#     Add text input    URL    label=Download URL for the csv file
#     ${response}=    Run dialog
#     [Return]    ${response.URL}

# download the csv file
#     [Arguments]    ${URL}
#     Download    ${URL}    overwrite=True

# Fill and submit the form for one person
#     [Arguments]    ${robot_order}
#     Select From List By Index    head    ${robot_order}[Head]
#     Click Button    css:#id-body-${robot_order}[Body]
#     Input Text    css=input.form-control    ${robot_order}[Legs]
#     Input Text    css:#address    ${robot_order}[Address]
#     Click Button    css:#preview
#     Wait Until Keyword Succeeds    5x    0.5 sec    click button in spite of an error message

# click button in spite of an error message
#     Click Button    css:#order
#     Wait Until Page Contains    Receipt    1 sec

# collect the results
#     [Arguments]    ${receipt_number}
#     Wait Until Element Is Visible    id:receipt    10 sec
#     ${receipt_html}=    Get Element Attribute    id:receipt    outerHTML
#     Html To Pdf    ${receipt_html}    ${OUTPUT_DIR}${/}receipts/receipt_${receipt_number}.pdf
#     [Return]    ${OUTPUT_DIR}${/}receipts/receipt_${receipt_number}.pdf

# screenshot the preview
#     [Arguments]    ${receipt_number}
#     screenshot    css:#robot-preview-image    ${OUTPUT_DIR}${/}receipts/screenshot_${receipt_number}.png
#     [Return]    ${OUTPUT_DIR}${/}receipts/screenshot_${receipt_number}.png

# embed the screenshot in the pdf and remove the png
#     [Arguments]    ${screenshot}    ${PDF}
#     Open Pdf    ${PDF}
#     ${files}=    Create List    ${screenshot}
#     Add Files To Pdf    ${files}    ${PDF}    True
#     Close Pdf    ${PDF}
#     Remove File    ${screenshot}

# order another robot
#     Click Button    css:#order-another

# create zip package from pdf files
#     Archive Folder With Zip    ${OUTPUT_DIR}${/}receipts    receipts.zip
