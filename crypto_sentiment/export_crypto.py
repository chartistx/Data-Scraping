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
my_file = pathlib.Path(r'C:\Users\Eriks\Desktop\CRYPTO_SENTIMENT\data.csv')
if my_file.is_file()==False:
    #file does not exist. create file
    with open(my_file,'w+', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['TIME','BITFINEX BTC','BITMEX BTC','BINANCE BTC','BITFINEX ETH','BITMEX ETH']) 
        file.close()
        del writer

driver = webdriver.Chrome(r'C:/Users/Eriks/Desktop/CRYPTO_SENTIMENT/chromedriver.exe')
driver.get('https://blockchainwhispers.com/bitmex-position-calculator/')
#time.sleep(1)
#elementAccType = driver.find_element_by_name("practice")
#elementAccType.click()
#time.sleep(1)
#elementUsername = driver.find_element_by_id("username")
#elementUsername.send_keys("chartistx")
#time.sleep(1)
#elementPassword = driver.find_element_by_id("password")
#elementPassword.send_keys("mincite1997")
#time.sleep(1)
#elementLogInButton = driver.find_element_by_id("loginButton")
#elementLogInButton.click()

time.sleep(15)
driver.refresh()
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
            #holder=""
            #print(html)
        # check out the docs for the kinds of things you can do with 'find_all'
        # this (untested) snippet should find tags with a specific class ID
        # see: http://www.crummy.com/software/BeautifulSoup/bs4/doc/#searching-by-css-class
            #n=1
            
            #print(html)
            for tag in soup.find_all("div","single-margin-platform"):#{"data-collapse-target": "EURUSD"}):
                checkname = str(tag.find_previous("h3","h-desc"))
                
                if checkname.find("Bitfinex BTC")>-1:
                    try:
                        longhold=doubleval(tag.find("div","field long").find("small").text)
                        list1[1]=longhold
                    except:
                        continue  
                elif checkname.find("BitMex BTC")>-1:
                    try:
                        longhold=doubleval(tag.find("div","field long").find("small").text)
                        list1[2]=longhold
                    except:
                        continue
                elif checkname.find("Binance BTC")>-1:
                    try:
                        longhold=doubleval(tag.find("div","field long").find("small").text)
                        list1[3]=longhold
                    except:
                        continue
                elif checkname.find("Bitfinex (ETH) Ethereum")>-1:
                    try:
                        longhold=doubleval(tag.find("span","value long").find("small").text)
                        list1[4]=longhold
                    except:
                        continue
                elif checkname.find("BitMex (ETH) Ethereum")>-1:
                    try:
                        longhold=doubleval(tag.find("span","value long").find("small").text)
                        list1[5]=longhold
                    except:
                        continue
                else:
                    continue
                
                    
            
               ###########################################################     
            gettime = time.strftime("%Y.%m.%d %H:%M:%S", time.localtime())
            seconds = time.strftime("%S", time.localtime())
            minutes = time.strftime("%M", time.localtime())
         
            sleepmins=0#5-(int(minutes)%5)+2
            
            sleepseconds =  62-int(seconds)
            sleeptotal = sleepmins*60+sleepseconds
            #print(gettime+holder)
            list1[0]=gettime
            writer.writerow(list1)
            del writer
            file.close()
            copyfile(my_file,r'C:\Users\Eriks\AppData\Roaming\MetaQuotes\Terminal\24F345EB9F291441AFE537834F9D8A19\MQL5\Files\CL_CRYPTO_Sentiment\Rutime_data.csv')
            print ('file closed @',gettime)
            time.sleep(sleeptotal)
            ## ADD REFRESH HERE
    
            #element = driver.find_element_by_id("refreshIcon")
            #element.click()
            #OR REFRESH WITH THIS
            driver.refresh()
            
            time.sleep(6)# Wait for data to refresh
    except PermissionError:
        print("File is already opened")
        time.sleep(3)

driver.close()
# =============================================================================
#     MAIN END
# =============================================================================


