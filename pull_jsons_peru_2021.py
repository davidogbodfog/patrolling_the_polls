# pull_pdf.py

#from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
import os

url = "https://www.resultadossep.eleccionesgenerales2021.pe/SEP2021/Actas/Numero/"

#driver = webdriver.Firefox()
#driver.implicitly_wait(2)

# import time

for i in reversed(range(1,20)):
    try:
       # print ("getting pdf for acta number:", i)
       # driver.get(url)
        acta_number = str(i).zfill(6)
       # print (acta_number)
        
       # elem = driver.find_element_by_xpath("//*[@id=\"pdf\"]/div[2]/div/div/div/form/input")
       # elem.send_keys(acta_number)
       # elem.send_keys(Keys.RETURN)

       # time.sleep(1.5)

        
        #csv_elem = driver.find_element_by_xpath("/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-nume/form/div/div[1]/div/a[2]")
        csv_url = "https://www.resultadossep.eleccionesgenerales2021.pe/SEP2021/Actas/Numero/"+acta_number
        #print (csv_url)
        os.system("curl -o /Users/mollie/Documents/Results2021rd2/"+acta_number+".json "+csv_url)

    except:
        continue
    
#driver.close()
