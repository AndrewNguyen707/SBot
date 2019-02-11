# Code By Erik Fisher and Andrew Nguyen
# 3/23/2018
from selenium import webdriver
from datetime import datetime, timedelta
import time
import csv

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Item(object):
    section = ""
    description = ""
    color = ""
    size = ""
    keywords = []

class User(object):
    name = ""
    email = ""
    phoneNum = ""
    streetAddress = ""
    zipCode = ""
    creditCardNum = ""
    creditCardExpMonth = ""
    creditCardExpYear = ""
    creditCardCVV = ""
    itemToBeBought = Item()


    def __init__(self):
        print("\nEnter filename in this directory    ex: filename.csv\n")
        print("Row1 Format: name,email,phoneNum,address,zip,cardNum,expMon,expYear,CVV")
        print("Row2 Format for item: size,section,description,color, other keywords")
        print("q to quit\n")

        while True:
            filename = input()
            if filename == "q":
                print("Quitting...")
                quit()
            try:
                open(filename)
                break
            except Exception as e:
                print("File Not Found. Try again or quit (q)\n")

        with open(filename) as csvfile:
            readerCSV = csv.reader(csvfile, delimiter=',')
            row1 = next(readerCSV)

            self.name = row1[0]
            self.email = row1[1]
            self.phoneNum = row1[2]
            self.streetAddress = row1[3]
            self.zipCode = row1[4]
            self.creditCardNum = row1[5]
            self.creditCardExpMonth = row1[6]
            self.creditCardExpYear = row1[7]
            self.creditCardCVV = row1[8]
            row2 = next(readerCSV)
            self.itemToBeBought.size = row2[0]
            if len(row2) > 1:
                self.itemToBeBought.section = row2[1]
                self.itemToBeBought.description = row2[2]
                self.itemToBeBought.color = row2[3]
                if len(row2) > 4:
                    counter = 4
                    while(counter < len(row2)):
                        self.itemToBeBought.keywords.append(row2[counter])
                        counter += 1
    def formatForInput(self):
        self.phoneNum = self.phoneNum.replace(" ","")
        self.phoneNum = self.phoneNum[0:3] + " " + self.phoneNum[3:6] + " " + self.phoneNum[6:10]

        self.creditCardNum = self.creditCardNum.replace(" ","")
        self.creditCardNum = self.creditCardNum[0:4]+" "+self.creditCardNum[4:8]+" "+self.creditCardNum[8:12]+" "+self.creditCardNum[12:16]


def waitTillTime():
    now = datetime.now()
    dayDifference = 3 - now.weekday()
    if dayDifference >= 0:
        startDay = now.day + dayDifference
    else:
        startDay = now.day + 7 + dayDifference
    startTime = datetime(now.year, now.month, startDay, 8, 0, 0)


    timeToWait = (startTime - now)
    print(f"{timeToWait} till launch...")
    time.sleep(timeToWait.seconds)

def refresherTillDrop():
    itemNumberToCheck = 15
    firstlinkBefore = brows.find_elements_by_tag_name("a")[itemNumberToCheck].get_attribute("href")
    while True:
        brows.refresh()
        time.sleep(0.7)

        firstlinkAfter = brows.find_elements_by_tag_name("a")[itemNumberToCheck].get_attribute("href")

        if firstlinkBefore != firstlinkAfter:
            print("New Link! Starting Search")
            break
        print(f"Same Link First Link, Refreshing...")

def findItem():
    counter = 0
    while counter < 300:
        brows.get(f"http://www.supremenewyork.com/shop/all/{customer.itemToBeBought.section}");
        foundItemLink = False
        for keyword in customer.itemToBeBought.keywords:
            try:
                itemLink = brows.find_element_by_partial_link_text(keyword).get_attribute("href")
                brows.get(itemLink)
                foundItemLink = True
                break
            except:
                pass



        if foundItemLink:
            break
        else:
            allItemsWebElements = brows.find_elements_by_partial_link_text(customer.itemToBeBought.description)
            allColorWebElements = brows.find_elements_by_partial_link_text(customer.itemToBeBought.color)


            brokeOut = False
            for item in allItemsWebElements:
                for color in allColorWebElements:
                    if item.get_attribute("href") == color.get_attribute("href"):
                        foundLink = item.get_attribute("href")
                        foundItemLink = True
                        brokeOut = True
                        break
                if brokeOut:
                    break
            try:
                brows.get(foundLink)
                break
            except:
                print("Couldn't Find Item")
                time.sleep(0.3)
        counter += 1
    if not foundItemLink:
        print("Giving up. Sorry")
        quit()

def doubleCheckValues():
    name = brows.find_element_by_name("order[billing_name]")
    email = brows.find_element_by_name("order[email]")
    phone = brows.find_element_by_name("order[tel]")
    phoneValue = phone.get_attribute("value").replace("-"," ")
    street = brows.find_element_by_name("order[billing_address]")
    zipCode = brows.find_element_by_name("order[billing_zip]")
    creditCardNum = brows.find_element_by_name("credit_card[nlb]")
    creditCardExpMonth = brows.find_element_by_name("credit_card[month]")
    creditCardExpYear = brows.find_element_by_name("credit_card[year]")
    creditCardCVV = brows.find_element_by_name("credit_card[rvv]")

    if name.get_attribute("value") != customer.name:
        name.clear()
        name.send_keys(customer.name)
    if email.get_attribute("value") != customer.email:
        email.clear()
        email.send_keys(customer.email)
    if phoneValue != customer.phoneNum:
        phone.clear()
        phone.send_keys(customer.phoneNum)
    if street.get_attribute("value") != customer.streetAddress:
        street.clear()
        street.send_keys(customer.streetAddress)
    if zipCode.get_attribute("value") != customer.zipCode:
        zipCode.clear()
        zipCode.send_keys(customer.zipCode)
    if creditCardNum.get_attribute("value") != customer.creditCardNum:
        creditCardNum.clear()
        creditCardNum.send_keys(customer.creditCardNum)
    if creditCardExpMonth.get_attribute("value") != customer.creditCardExpMonth:
        creditCardExpMonth.send_keys(customer.creditCardExpMonth)
    if creditCardExpYear.get_attribute("value") != customer.creditCardExpYear:
        creditCardExpYear.send_keys(customer.creditCardExpYear)
    if creditCardCVV.get_attribute("value") != customer.creditCardCVV:
        creditCardCVV.clear()
        creditCardCVV.send_keys(customer.creditCardCVV)

def checkOut():

    try:
        brows.find_element_by_name("s").send_keys(f"{customer.itemToBeBought.size}\n")
    except:
        print("No size selector found.")

    try:
        brows.find_element_by_name("commit").click()
    except:
        print("Sold Out")
        quit()

    try:
        WebDriverWait(brows,20).until(EC.presence_of_element_located((By.LINK_TEXT, "checkout now"))).click()
    except:
        print("Couldn't find checkout button")
        quit()

    # brows.find_element_by_link_text("checkout now").click()
    textBox = brows.find_element_by_name("order[billing_name]")
    textBox.send_keys(f"{customer.name}\t"+
                        f"{customer.email}\t"+
                        f"{customer.phoneNum}\t"+
                        f"{customer.streetAddress}\t\t"+
                        f"{customer.zipCode}\t\t\t\t \t"+
                        f"{customer.creditCardNum}\t"+
                        f"{customer.creditCardExpMonth}\t"+
                        f"{customer.creditCardExpYear}\t"+
                        f"{customer.creditCardCVV}\t ")

    doubleCheckValues()

    brows.find_element_by_name("commit").click()





# Read in Data
customer = User()
customer.formatForInput()

print("\nStarting Browser\n")
brows = webdriver.Chrome()
brows.get("http://www.supremenewyork.com/shop/all/")

#Wait to begin searching   24 hour time
#waitTillTime()
#refresherTillDrop()

startTime = time.time()

findItem()
checkOut()

endTime = time.time()
totalTime = endTime - startTime
print(f"It took {totalTime:.1f} seconds after refresh")



# Color/Style Names
# Heather Grey
# Red
# Black
# White
# Navy
# Moss Green
# Bright Orange
# Plum
# Cardinal
# Pale Lime
# Royal (blue)
# Pale Pink
# Light Pine
