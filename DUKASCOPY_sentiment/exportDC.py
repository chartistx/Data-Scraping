from bs4 import BeautifulSoup
from selenium import webdriver

import time
import csv
import pathlib
from shutil import copyfile

# =============================================================================
#     FUNCTIONS ZONE START
# =============================================================================
def doubleval(objectval):
    emptyholder=""
    for letter in objectval:
        if letter.isdigit():
            emptyholder+=letter
        elif letter==".":
            emptyholder+=letter
        else:
            continue
        
    return float(emptyholder)


# =============================================================================
#     FUNCTIONS ZONE END
# =============================================================================


# =============================================================================
#     MAIN
# =============================================================================
my_file = pathlib.Path(r'C:\Users\Eriks\Desktop\DUKAS_SENTIMENT\data.csv')
if my_file.is_file()==False:
    #file does not exist. create file
    with open(my_file,'w+', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['TIME','EURUSD','GBPUSD','AUDUSD','USDJPY','XAUUSD']) 
        file.close()
        del writer

driver = webdriver.Chrome(r'C:/Users/Eriks/Desktop/DUKAS_SENTIMENT/chromedriver.exe')
driver.get('https://www.dukascopy.com/swiss/english/marketwatch/sentiment/')


time.sleep(6)

while True:
    try:
        
        with open(my_file,'a', newline='') as file:
            print ('file opened')
            writer = csv.writer(file)
            list1 = ['','','','','','']
            
            driver.switch_to.frame(driver.find_element_by_tag_name('iframe'))
            html = driver.page_source
            soup = BeautifulSoup(html,"lxml")

            for tag in soup.find_all("div","F-qb-Ab"):#{"data-collapse-target": "EURUSD"}):
                #print(tag)
                name = (tag.find("div","F-qb-Db-name"))

                if name.text.find("EUR/USD")>-1:
                    longval =tag.find("div","F-qb-Gb")
                    longhold=doubleval(longval.text)
                    
                    list1[1]=longhold
     
                        
                elif name.text.find("GBP/USD")>-1:
                    longval =tag.find("div","F-qb-Gb")
                    longhold=doubleval(longval.text)
                    
                    list1[2]=longhold
                          
                elif name.text.find("AUD/USD")>-1:
                    longval =tag.find("div","F-qb-Gb")
                    longhold=doubleval(longval.text)
                    
                    list1[3]=longhold
                      
                elif name.text.find("USD/JPY")>-1:
                    longval =tag.find("div","F-qb-Gb")
                    longhold=doubleval(longval.text)
                    
                    list1[4]=longhold
                           
                elif name.text.find("XAU/USD")>-1:
                    longval =tag.find("div","F-qb-Gb")
                    longhold=doubleval(longval.text)
                    
                    list1[5]=longhold
                            
                else:
                    continue
               ###########################################################     
            gettime = time.strftime("%Y.%m.%d %H:%M:%S", time.localtime())
            seconds = time.strftime("%S", time.localtime())
            minutes = time.strftime("%M", time.localtime())
         
            sleepmins=5-(int(minutes)%5)+2
            
            sleepseconds =  62-int(seconds)
            sleeptotal = sleepmins*60+sleepseconds
            #print(gettime+holder)
            list1[0]=gettime
            writer.writerow(list1)
            del writer
            file.close()
            copyfile(my_file,r'C:\Users\Eriks\AppData\Roaming\MetaQuotes\Terminal\24F345EB9F291441AFE537834F9D8A19\MQL5\Files\CL_DUKASCOPY_Sentiment\Runtime_data.csv')
            print ('file closed @',gettime)
            time.sleep(sleeptotal)

            driver.refresh()
            
            time.sleep(6)# Wait for data to refresh
    except PermissionError:
        print("File is already opened")
        time.sleep(3)

driver.close()
# =============================================================================
#     MAIN END
# =============================================================================


