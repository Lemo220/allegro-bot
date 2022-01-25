from datetime import datetime
import pyautogui

def appendLogToFile(log_value):
    with open("logs.txt", "a") as myfile:
        myfile.write(datetime.now().strftime("%d-%m-%Y %H-%M-%S") + "|" + log_value + "\n")
        myfile.close()

def doAndSaveScreenShot(name, gold,tc_or_cc):
    if tc_or_cc == 'tc':
        multiplier = 1
    else:
        multiplier = 1000000
    saved_screenshot = pyautogui.screenshot()
    dt_string = datetime.now().strftime("%d-%m-%Y %H-%M-%S")
    path = name + str(int(gold)/multiplier) + " kk" + " " + str(dt_string) + ".png"
    saved_screenshot.save(r'C:\Users\Ja\Desktop\SellerV4\zrealizowane\\' + path) # TODO - not saving screenshots
    

def saveOrdersByPaymentNumber(payment_number):
    with open("orders_finalized.txt", "w") as myfile:
        myfile.write(payment_number + "\n")
        myfile.close()

def readOrdersByPaymentNumbers():
    with open("orders_finalized.txt", "r") as myfile:
        result = myfile.readlines()
        myfile.close()
        return result