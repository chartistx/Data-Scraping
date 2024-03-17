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



def extractamount(val):
    temphold=""
    checkstart=False
    for letter in val:
        if checkstart==False and letter=="$":
            checkstart=True
        elif checkstart==False:
            continue
        elif letter.isdigit():
            temphold+=letter
        elif letter==".":
            temphold+=letter
        elif letter==",":
            continue
        else:
            break
        
    return float(temphold)
    

# =============================================================================
#     FUNCTIONS ZONE END
# =============================================================================


# =============================================================================
#     MAIN
# =============================================================================
my_file = pathlib.Path(r'C:\Users\Eriks\Desktop\CRYPTO_SENTIMENT\data_full.csv')
if my_file.is_file()==False:
    #file does not exist. create file
    with open(my_file,'w+', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['TIME',
                         'BITFINEX BTC LONG $','BITFINEX BTC SHORT $',
                         'BITMEX BTC LONG $','BITMEX BTC SHORT $',
                         'BINANCE BTC LONG $','BINANCE BTC SHORT $',
                         'BITFINEX ETH LONG $','BITFINEX ETH SHORT $',
                         'BITMEX ETH LONG $','BITMEX ETH SHORT $']) 
        file.close()
        del writer

driver = webdriver.Chrome(r'C:/Users/Eriks/Desktop/CRYPTO_SENTIMENT/chromedriver.exe')
driver.get('https://blockchainwhispers.com/bitmex-position-calculator/')

time.sleep(15)
driver.refresh()
time.sleep(6)

while True:
    try:
        
        with open(my_file,'a', newline='') as file:
            print ('file opened')
            writer = csv.writer(file)
            list1 = ['','','','','','','','','','','']
            html = driver.page_source
            soup = BeautifulSoup(html,"lxml")

            for tag in soup.find_all("div","single-margin-platform"):#{"data-collapse-target": "EURUSD"}):
                checkname = str(tag.find_previous("h3","h-desc"))
                
                if checkname.find("Bitfinex BTC")>-1:
                    try:
                        list1[1]=doubleval(tag.find("div","value long").text)
                        list1[2]=doubleval(tag.find("div","value short").text)


                    except:
                        continue  
                elif checkname.find("BitMex BTC")>-1:
                    try:
                        list1[3]=doubleval(tag.find("div","value long").text)
                        list1[4]=doubleval(tag.find("div","value short").text)

                    except:
                        continue
                elif checkname.find("Binance BTC")>-1:
                    try:
                        list1[5]=doubleval(tag.find("div","value long").text)
                        list1[6]=doubleval(tag.find("div","value short").text)

                    except:
                        continue
                elif checkname.find("Bitfinex (ETH) Ethereum")>-1:
                    try:
                        
                        list1[7]=extractamount(tag.find("span","value long").text)
                        list1[8]=extractamount(tag.find("span","value short").text)

                    except:
                        continue
                elif checkname.find("BitMex (ETH) Ethereum")>-1:
                    try:
                        list1[9]=extractamount(tag.find("span","value long").text)
                        list1[10]=extractamount(tag.find("span","value short").text)

                    except:
                        continue
                else:
                    continue

            gettime = time.strftime("%Y.%m.%d %H:%M:%S", time.localtime())
            seconds = time.strftime("%S", time.localtime())
            minutes = time.strftime("%M", time.localtime())
         
            sleepmins=0#5-(int(minutes)%5)+2
            
            sleepseconds =  62-int(seconds)
            sleeptotal = sleepmins*60+sleepseconds

            
            list1[0]=gettime
            writer.writerow(list1)
            del writer
            file.close()
            copyfile(my_file,r'C:\Users\Eriks\AppData\Roaming\MetaQuotes\Terminal\24F345EB9F291441AFE537834F9D8A19\MQL5\Files\CL_CRYPTO_Sentiment\Rutime_data_full.csv')
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


