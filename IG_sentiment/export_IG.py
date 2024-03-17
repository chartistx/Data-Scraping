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
my_file = pathlib.Path(r'C:\Users\Eriks\Desktop\IGG_SENTIMENT\data.csv')
if my_file.is_file()==False:
    #file does not exist. create file
    with open(my_file,'w+', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['TIME','EURUSD']) 
        file.close()
        del writer

driver = webdriver.Chrome(r'C:/Users/Eriks/Desktop/IGG_SENTIMENT/chromedriver.exe')
driver.get('https://www.ig.com/uk/forex/markets-forex/eur-usd')

time.sleep(6)

# =============================================================================
# day = date.today()
# daynr = day.weekday()
# print(daynr)
# =============================================================================
while True:
    try:
        
        with open(my_file,'a', newline='') as file:
            print ('file opened')
            writer = csv.writer(file)
            list1 = ['','']
            html = driver.page_source
            soup = BeautifulSoup(html,"lxml")
            
            #print(html)
            for tag in soup.find_all("div","information-popup"):#{"data-collapse-target": "EURUSD"}):
                #print(tag)
                for direction in tag.find_all("strong"):#tag.find_all("span","price-ticket__percent"):
                    strdir = str(direction)
                    if  strdir.find("short")>-1:
                        val = tag.find("span","price-ticket__percent")
                        
                        longhold=doubleval(val.text)
                        list1[1]=100-longhold
                    elif strdir.find("long")>-1:
                        val = tag.find("span","price-ticket__percent")
                        
                        longhold=doubleval(val.text)
                        list1[1]=longhold
                    
            
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
            copyfile(my_file,r'C:\Users\Eriks\AppData\Roaming\MetaQuotes\Terminal\24F345EB9F291441AFE537834F9D8A19\MQL5\Files\CL_IG_Sentiment\Rutime_data.csv')
            print ('file closed @',gettime)
            time.sleep(sleeptotal)

            #REFRESH 
            driver.refresh()
            
            time.sleep(6)# Wait for data to refresh
    except PermissionError:
        print("File is already opened")
        time.sleep(3)

driver.close()
# =============================================================================
#     MAIN END
# =============================================================================


