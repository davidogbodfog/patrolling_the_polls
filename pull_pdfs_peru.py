# pull_pdf.py

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os

url = "https://www.resultadossep.eleccionesgenerales2021.pe/SEP2021/Actas/Numero"


driver = webdriver.Firefox()
driver.implicitly_wait(2)

import time

for i in range(75000, 84000):
    try:
        print ("getting pdf for acta number:", i)
        driver.get(url)
        acta_number = str(i).zfill(6)
        print (acta_number)
        
        elem = driver.find_element_by_xpath("/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-nume/form/div/div[2]/div/div/div/form/div/input")
        elem.send_keys(acta_number)
        elem.send_keys(Keys.RETURN)

        time.sleep(1.5)
        
        pdf_elem = driver.find_element_by_xpath("/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-nume/form/div/div[3]/div[1]/div/div[2]/div/a")
        pdf_url = pdf_elem.get_attribute("href")
        print (pdf_url)
        os.system("curl -o /Users/mollie/Documents/Actas2020rd2_2/"+acta_number+".pdf \""+pdf_url +"\"")

    except:
        continue
    
driver.close()




