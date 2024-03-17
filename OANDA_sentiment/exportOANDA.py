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
my_file = pathlib.Path(r'C:\Users\Eriks\Desktop\OANDA_SENTIMENT\data.csv')
if my_file.is_file()==False:
    #file does not exist. create file
    with open(my_file,'w+', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['TIME','EURUSD','GBPUSD','USDJPY','AUDUSD','XAUUSD']) 
        file.close()
        del writer

driver = webdriver.Chrome(r'C:/Users/Eriks/Desktop/OANDA_SENTIMENT/chromedriver.exe')
driver.get('https://trade.oanda.com/labs/position-ratios/?embedded=true')
time.sleep(1)

elementUsername = driver.find_element_by_id("username")
elementUsername.send_keys("username")# username replaced with example
time.sleep(1)
elementPassword = driver.find_element_by_id("password")
elementPassword.send_keys("password")# password replaced with example
time.sleep(1)
elementLogInButton = driver.find_element_by_id("loginButton")
elementLogInButton.click()

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
            list1 = ['','','','','','']
            html = driver.page_source
            soup = BeautifulSoup(html,"lxml")

            for tag in soup.find_all("div","flex-container position-long-short-row style-scope position-ratios"):
                
                name = (tag.find("div","instrument style-scope position-ratios"))
                if name.text=="EUR/USD":
                    
                    shortval = (tag.find("div","position short-position style-scope position-ratios"))
                    
                    shorthold=doubleval(shortval.text)
                    longhold=100-doubleval(shortval.text)

                    list1[1]=longhold
                        
                elif name.text=="GBP/USD":
                    shortval = (tag.find("div","position short-position style-scope position-ratios"))
                    shorthold=doubleval(shortval.text)

                    list1[2]=longhold
                elif name.text=="AUD/USD":
                    shortval = (tag.find("div","position short-position style-scope position-ratios"))
                    shorthold=doubleval(shortval.text)
                    longhold=100-doubleval(shortval.text)

                    list1[4]=longhold
                elif name.text=="USD/JPY":
                    shortval = (tag.find("div","position short-position style-scope position-ratios"))
                    shorthold=doubleval(shortval.text)
                    longhold=100-doubleval(shortval.text)

                    list1[3]=longhold
                elif name.text=="XAU/USD":
                    shortval = (tag.find("div","position short-position style-scope position-ratios"))
                    shorthold=doubleval(shortval.text)
                    longhold=100-doubleval(shortval.text)

                    list1[5]=longhold
                else:
                    continue
    
            gettime = time.strftime("%Y.%m.%d %H:%M:%S", time.localtime())
            seconds = time.strftime("%S", time.localtime())
            minutes = time.strftime("%M", time.localtime())
         
            sleepmins=20-(int(minutes)%20)
            sleepseconds =  62-int(seconds)
            sleeptotal = sleepmins*60+sleepseconds

            list1[0]=gettime
            writer.writerow(list1)
            del writer
            file.close()
            copyfile(my_file,r'C:\Users\Eriks\AppData\Roaming\MetaQuotes\Terminal\24F345EB9F291441AFE537834F9D8A19\MQL5\Files\CL_OANDA_Sentiment\Rutime_data.csv')
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


