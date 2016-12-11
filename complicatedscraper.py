#!/usr/bin/env python

from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException as STALE
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup as BS
import os
import time
from shutil import which


PROPERTYLINK = 'http://sdat.dat.maryland.gov/RealProperty/Pages/default.aspx'
COUNTY = "PRINCE GEORGE'S %s" % "COUNTY"
METHOD =  "STREET ADDRESS"
QUERY = "Oakridge"
chromedriver="/usr/bin/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver


def Clickable(method, attrib):
    ele = wait.until(EC.element_to_be_clickable((method, attrib)))
    return ele

def ProcessPage1(driver):
    cntyID = 'MainContent_MainContent_cphMainContentArea_ucSearchType_wzrdRealPropertySearch_ucSearchType_ddlCounty'
    selectCnty = Select(driver.find_element_by_id(cntyID))
    selectCnty.select_by_visible_text("PRINCE GEORGE'S COUNTY")
    methodID = 'MainContent_MainContent_cphMainContentArea_ucSearchType_wzrdRealPropertySearch_ucSearchType_ddlSearchType'
    selectMethod = Select(driver.find_element_by_id(methodID))
    selectMethod.select_by_visible_text('STREET ADDRESS')
    wait = Wait(driver, 10)
    buttonID = 'MainContent_MainContent_cphMainContentArea_ucSearchType_wzrdRealPropertySearch_StartNavigationTemplateContainerID_btnContinue'
    trycount = 0
    while True:
        trycount += 1
        try:
            print('attempt # %d' % trycount)
            element = Clickable(By.ID, buttonID)
            if element:
                element.click()
                break
        except STALE as e:
            print('Element went stale :(')
            print('waiting a bit before trying')
            if trycount > 5:
                break
            time.sleep(2)


def ProcessPage2(driver):
    stNmID = 'MainContent_MainContent_cphMainContentArea_ucSearchType_wzrdRealPropertySearch_ucEnterData_txtStreetName'
    stNmBx = driver.find_element_by_id(stNmID)
    stNmBx.send_keys('Oakridge')
    nxtBtnID = 'MainContent_MainContent_cphMainContentArea_ucSearchType_wzrdRealPropertySearch_StepNavigationTemplateContainerID_btnStepNextButton'
    driver.implicitly_wait(5)
    try:
        element = Clickable(By.ID, nxtBtnID)
        if element:
            element.click()
        except STALE:
            print('Element went stale: (')


def GetLinksFromPage3(driver):
    pagesource = driver.page_source
    soup = BS(pagesource, 'lxml')
    #Getting the named_link table of the third page
    tbl = soup.find('table',attrs={"class":"ui-table table-stripe"})
    tbody = tbl.find('tbody')
    linklist=[]
    for row in tbody.find_all('tr'):
        a = row.find('a', attrs={"class": "lnkdetails"})
        if a:
            dataLinkEle = driver.find_element(By.ID, a.attrs['id'])
            linklist.append(dataLinkEle)
    return linklist

def GetDataFromPage4(driver):
    gbbID = "MainContent_MainContent_cphMainContentArea_ucSearchType_wzrdRealPropertySearch_btnPrevious_top2"
    goBackBtn = Clickable(By.ID, gbbID)
    tryCounts = 0
    pagesource = driver.pagesource
    data_section1 = ScrapePg4Sec1(pagesource)
    data_section2 = ScrapePg4Sec2(pagesource)
    data_section3 = ScrapePg4Sec3(pagesource)
    data_section4 = ScrapePg4Sec4(pagesource)
    while True or tryCounts<5:
        tryCounts+=1
        try:
            goBackBtn.click()
        except STALE:
            print('back button went stale, attempt %d/5. Retrying in 5s.' % tryCounts )
        else:
            break




def Main():
    driver = webdriver.Chrome(chromedriver)
    driver.wait = Wait(driver, 5)
    driver.get(PROPERTYLINK)
    ProcessPage1(driver)
    ProcessPage2(driver)
    dataLinkList = GetLinksFromPage3(driver)
