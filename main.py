import socket, time
from datetime import datetime, date, timedelta, time as t
from selenium import webdriver
from selenium.webdriver.common.by import By

#THE PROGRAM DOES NOT ACCOUNT FOR HOLIDAYS

def check_Connection():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("www.google.com", 80))
        print("Connected.")
        s.close()
    except Exception:
        print("Check your connection.")
        time.sleep(3)
        exit()

def time_Info():
    print("The program does not account for national holidays. Please refrain from using those dates.")
    year_info = int(input("Enter the year: "))  # takes input for year month day.
    monthInfo = int(input("Enter the month: "))
    dayInfo = int(input("Enter the day: "))

    inputDate = date(year_info, monthInfo, dayInfo)  # transforms that into date form.
    todaysDate = date.today() #takes today's date.

    timeATM = datetime.now().time() #taking now's time.
    finTime = t(hour=17) #is equal to 5 pm when the banks close and currency data is given.


    # if saturday or sunday, return friday instead. if it is before 5 pm take yesterdays date. for dates smaller than
    # 2019 or larger than current date, it will ask for a new input

    if inputDate < date(year= 2019, month= 1, day=1):
        print("Given date is too small. Please re-enter date.")
        time_Info()
    elif inputDate > todaysDate:
        print("Given date is too big. Please re-enter date.")
        time_Info()
    elif inputDate.weekday() == 5:
        inputDate = inputDate + timedelta(days = -1)
        print("Taking Fridays date, " + inputDate.strftime("%d/%m/%Y, %H:%M:%S"))
    elif inputDate.weekday() == 6:
        inputDate = inputDate + timedelta(days=-2)
        print("Taking Fridays date, " + inputDate.strftime("%d/%m/%Y, %H:%M:%S"))
    else:
        if inputDate == todaysDate:
            if timeATM >= finTime:
                print("Taking todays date, " + inputDate.strftime("%d/%m/%Y, %H:%M:%S"))
            else:
                inputDate = inputDate + timedelta(days=-1)
                print("Taking yesterdays date, " + inputDate.strftime("%d/%m/%Y, %H:%M:%S"))
        else:
            print("Taking todays date, " + inputDate.strftime("%d/%m/%Y, %H:%M:%S"))
    return inputDate

def take():
    inputDate = time_Info()
    yearInt = inputDate.year #year data as int
    monthInt = (inputDate.month - 1) #month data as int
    dayInt =inputDate.day #day data as int

    driver = webdriver.Chrome()
    website = ('https://www.tcmb.gov.tr/wps/wcm/connect/TR/TCMB+TR/Main+Menu/Istatistikler/Doviz+Kurlari/Gosterge'
               '+Niteligindeki+Merkez+Bankasi+Kurlarii/')
    driver.get(website)

    yearXPath = ('//a[@data-w-tab="Tab ' + str(yearInt) + '"]')
    yearFinal = driver.find_element(By.XPATH, yearXPath)
    #yearFinal = driver.find_element(By.XPATH, '//a[@data-w-tab="Tab 2023"]') for 7-07-2023
    yearFinal.click()

    driver.implicitly_wait(800)
    monthXPath = ('//div/a[@data-month="' + str(monthInt) + '"][@data-year="' + str(yearInt) + '"]/div[1]')
    monthFinal = driver.find_element(By.XPATH, monthXPath)
    #monthFinal = driver.find_element(By.XPATH, '//div/a[@data-month="6"][@data-year="2023"]/div[1]') for 7-07-2023
    monthFinal.click()

    driver.implicitly_wait(800)
    #dayXPath = ('//a[text()="' + str(dayInt) + '"]')
    dayXPath = ('//td[@data-year="' + str(yearInt) + '"]/a[text()="'+ str(dayInt) + '"]')
    dayFinal = driver.find_element(By.XPATH, dayXPath)
    #//div[@data-w-tab="Tab 2022"]/a[text()="7"]
    # dayFinal = driver.find_element(By.XPATH, '//a[text()="7"]') for 7-07-2023 when i use
    # this xpath it doesn't return the first day pf the month' //a[@class="ui-state-default"][text()="7"]'
    #new = //td[@data-year="2023"]/a[text()="7"]
    dayFinal.click()

    submit_button = driver.find_element(By.XPATH, '//input[@type ="submit"]')
    submit_button.click()

    driver.implicitly_wait(800)
    usd_buys = driver.find_element(By.XPATH, '//tr[1]/td[@class="deger"][1]').text
    usd_sells = driver.find_element(By.XPATH, '//tr[1]/td[@class="deger"][2]').text
    euro_buys = driver.find_element(By.XPATH, '//tr[4]/td[@class="deger"][1]').text
    euro_sells = driver.find_element(By.XPATH, '//tr[4]/td[@class="deger"][2]').text

    print("Dolar alış: {0}\nDolar satış: {1}\nEuro alış: {2}\nEuro alış: {3}\n".format(usd_buys, usd_sells,
                                                                                         euro_buys, euro_sells))

    driver.quit()

def main():
    check_Connection()
    take()

main()
