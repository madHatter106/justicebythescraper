#!/usr/bin/env python

from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException as SERE
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

def ProcessPage1():
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
            element = wait.until(EC.element_to_be_clickable((By.ID, buttonID)))
            if element:
                element.click()
                break
        except SERE as e:
            print('Element went stale :(')
            print('waiting a bit before trying')
            if trycount > 5:
                break
            time.sleep(2)

def Main():
    driver = webdriver.Chrome(chromedriver)
    driver.wait = Wait(driver, 5)
    driver.get(PROPERTYLINK)
