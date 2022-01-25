from AllegroOrder import send_msg
import time
import cv2
import pygetwindow
from screen_search import *
import psutil
from pyautogui import *
from LogUtilites import *
import pygetwindow as gw
import random
from random import randint
import pytesseract



def gold_screen():
    im = pyautogui.screenshot(region=(108,580, 85, 14))
    im.save("gold.png")
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    img = cv2.imread("gold.png")
    text = pytesseract.image_to_string(img).replace(",", "").replace("$", "8")
    return text




class TibiaManager(object):
    """description of class"""
    server_characters_dictionary = {
        "Adra" : "Adra raz",
        "Antica" : "Iria Sylleis",
        "Bona" : "Bona dwa",
        "Celesta" : "Nice Sombrero",
        "Damora" : "Damora dwa",
        "Thyria" : "Sufit",
        "Harmonia" : "Harmon Raz",
        "Karna" : "Karna Lemo",
        "Monza" : "Monza Dwa",
        "Peloria" : "Peloria dwa",
        "Refugia" : "Refugia raz",
        "Secura" : "Secura raz",
        "Vunira" : "Trugy",
        "Marcia" : "Marcia raz",
        "Premia" : "Premia",
        "Suna" : "Vita raz",
        "Olima" : "Olima Raz"
    }
    server_imagepaths_dictionary = {
        # TODO ALL TO REWRITE TO CHARACTERS IMAGES I  M  P  O  R  T  A  N  T - they dont should start from C NEXT IMPORTANT: IMAGES MINIMUM 25 height
        "Adra": "ImagesFromTibia/Adra.png",
        "Antica": "ImagesFromTibia/Antica.png",
        "Bona": "ImagesFromTibia/Bona.png",
        "Celesta": "ImagesFromTibia/Celesta.png",
        "Damora": "ImagesFromTibia/Damora.png",
        "Harmonia": "ImagesFromTibia/Harmonia.png",
        "Karna": "ImagesFromTibia/Karna.png",
        "Monza": "ImagesFromTibia/Monza.png",
        "Peloria": "ImagesFromTibia/Peloria.png",
        "Refugia": "ImagesFromTibia/Refugia.png",
        "Secura": "ImagesFromTibia/Secura.png",
        "Vunira": "ImagesFromTibia/Vunira.png",
        "Thyria": "ImagesFromTibia/Sufit.png",
        "Marcia": "ImagesFromTibia/Marcia.png",
        "Premia": "ImagesFromTibia/Premia.png",
        "Suna": "ImagesFromTibia/Suna.png",
        "Olima": "ImagesFromTibia/Olima.png"
    }

    def __init__(self, login, password, status_label):
        self.login = login
        self.password = password
        self.status_label = status_label

        self.tibia_path = "C:\Tibia\Tibia.exe"

    # MAIN ORDER FUNCTION0
    def doOrder(self, destination_server, destination_character, amount_of_gold):
        tibia_opened = False
        # check tibia openned todo
        for window in pygetwindow.getAllWindows():
            if "tibia" in window.title.lower():
                tibia_opened = True

        if tibia_opened == False:
            appendLogToFile("TIBIA NIE OTWORZONA - brak okna o nazwie tibia")
            return False

        self.status_label.setText("Tibia Status: Maksymalizuje okno")
        # activate tibia window, move it to upper left corner and resize it to 800x600
        self.status_label.setText("Tibia Status: Ustawiam okno")
        tibia_window = gw.getWindowsWithTitle("Tibia")[0]
        tibia_window.maximize()
        tibia_window.activate()
        tibia_window.moveTo(0, 0)
        tibia_window.resizeTo(800, 600)
        self.waitRandoimzedTime(2.0, 3.0)

        # check if connection lost
        connection_lost_screen = self.findImageOnScreen("ImagesFromTibia\Connection_Lost_Logo.PNG")
        if connection_lost_screen[0] == True:
            pyautogui.click(connection_lost_screen[1]+10, connection_lost_screen[2]+10,  clicks=1)
            self.waitRandoimzedTime(2.0, 3.0)
            pyautogui.press('esc')
            self.waitRandoimzedTime(2.0, 3.0)

        if tibia_opened == False:
            appendLogToFile("TIBIA NIE OTWORZONA")
            return False

        if self.IsInLoggingMenu() == False:
            appendLogToFile("Problem - nie jestem w logging menu")
            return False

        self.logToAccount()
        self.waitRandoimzedTime(4.0, 6.0)

        if self.IsInServerMenu() == False:
            appendLogToFile("Problem z zalogowaniem")
            return False
        self.enterServer(destination_server)

        self.waitTime()
        # todo check for queue

        if self.IsOnServer() == False:
            appendLogToFile("Problem z wejściem na serwer")
            return False

        self.goToMerchant()

        if self.transferMoney(amount_of_gold, destination_character) == False:
            appendLogToFile("Problem - transkacja NIE ZOSTAŁA ZREALIZOWANA POPRAWNIE")
            return False

        return True  # then main thread should save this order in orders list

    def doOrder_tc(self, destination_character, amount_of_gold):
        tibia_opened = False
        # check tibia openned todo
        for window in pygetwindow.getAllWindows():
            if "tibia" in window.title.lower():
                tibia_opened = True

        if tibia_opened == False:
            appendLogToFile("TIBIA NIE OTWORZONA - brak okna o nazwie tibia")
            return False

        self.status_label.setText("Tibia Status: Maksymalizuje okno")
        # activate tibia window, move it to upper left corner and resize it to 800x600
        self.status_label.setText("Tibia Status: Ustawiam okno")
        tibia_window = gw.getWindowsWithTitle("Tibia")[0]
        tibia_window.maximize()
        tibia_window.activate()
        tibia_window.moveTo(0, 0)
        tibia_window.resizeTo(800, 600)
        self.waitRandoimzedTime(2.0, 3.0)

        # check if connection lost
        connection_lost_screen = self.findImageOnScreen("ImagesFromTibia\Connection_Lost_Logo.PNG")
        if connection_lost_screen[0] == True:
            pyautogui.click(connection_lost_screen[1]+10, connection_lost_screen[2]+10,  clicks=1)
            self.waitRandoimzedTime(2.0, 3.0)
            pyautogui.press('esc')
            self.waitRandoimzedTime(2.0, 3.0)

        if tibia_opened == False:
            appendLogToFile("TIBIA NIE OTWORZONA")
            return False

        if self.IsInLoggingMenu() == False:
            appendLogToFile("Problem - nie jestem w logging menu")
            return False

        self.logToAccount()
        self.waitRandoimzedTime(4.0, 6.0)

        if self.IsInServerMenu() == False:
            appendLogToFile("Problem z zalogowaniem")
            return False
        self.enterServer("Adra")

        self.waitTime()
        self.goToMerchant()
        # todo check for queue

        if self.IsOnServer() == False:
            appendLogToFile("Problem z wejściem na serwer")
            return False

        if self.transferTC(amount_of_gold, destination_character) == False:
            appendLogToFile("Problem - TRANSAKCJA NIE ZOSTAŁA ZREALIZOWANA POPRAWNIE")
            return False

        return True  # then main thread should save this order in orders list



    def IsInLoggingMenu(self):
        self.status_label.setText("Tibia Status: Sprawdzam czy jestem w menu logowania")
        if self.findImageOnScreen("ImagesFromTibia\Logging_Logo.PNG")[0] == True:
            return True
        else:
            return False

    def IsInServerMenu(self):
        self.status_label.setText("Tibia Status: Sprawdzam czy jestem w menu wyboru serwera")
        if self.findImageOnScreen("ImagesFromTibia\Select_Character_Logo.PNG")[0] == True:
            return True
        else:
            return False

    def logToAccount(self):
        self.status_label.setText("Tibia Status: Loguje na konto")
        # login with credentials
        self.writeTextInRandomizeTime(self.login)
        pyautogui.press('tab')
        self.writeTextInRandomizeTime(self.password)
        pyautogui.press('enter')

    def enterServer(self, server_name):
        self.status_label.setText("Tibia Status: Wchodzę na serwer")
        # get server image from dictionary
        if server_name in self.server_imagepaths_dictionary == False:
            return False

        server_image_path = self.server_imagepaths_dictionary[server_name]

        # server not founded
        server_character_position = self.findServerCharacterInServerListOnScreen(server_image_path)

        pyautogui.click(server_character_position[1] + 10, server_character_position[2] + 10, clicks=2)
        self.waitRandoimzedTime(5.0, 7.0)

        # todo check queue
        if self.IsQueue() == True:
            self.waitRandoimzedTime(60.0, 120.0)

        self.status_label.setText("Tibia Status: Sprawdzam czy wszedłem na dobrą postać")
        # check if entered corrected server
        tibia_window = gw.getWindowsWithTitle("Tibia")

        good_server_entered = False
        for window in tibia_window:
            if self.server_characters_dictionary[server_name] in window.title:
                good_server_entered = True

        if good_server_entered == False:
            appendLogToFile("Problem - wszedłem na zły serwer")
            return False
        else:
            return True

    def IsOnServer(self):
        self.status_label.setText("Tibia Status: Sprawdzam czy jestem na serwerze")
        if self.findImageOnScreen("ImagesFromTibia\Local_Chat_Server_Log_Logo.PNG")[0] == True:
            return True
        else:
            return False

    def IsQueue(self):
        self.status_label.setText("Tibia Status: Sprawdzam czy jest kolejka")
        if self.findImageOnScreen("ImagesFromTibia\Queue_Logo.PNG")[0] == True:
            return True
        else:
            return False

    def transferMoney(self, gold, name):
        self.status_label.setText("Tibia Status: Przelewam " + gold + " golda " + " dla " + name)
        # say hi
        self.writeTextInRandomizeTime("hi")
        pyautogui.press('enter')
        self.waitTime()
        if self.IsAfterHI() == False:
            appendLogToFile("Problem - brak wiadomosci zwrotnej po komendzie /hi")
            return False
        # say transfer
        self.writeTextInRandomizeTime("transfer")
        pyautogui.press('enter')
        self.waitTime()
        if self.IsAfterTransfer == False:
            appendLogToFile("Problem - brak wiadomosci zwrotnej po komendzie /transfer")
            return False
        self.writeTextInRandomizeTime(str(gold))
        pyautogui.press('enter')
        self.waitTime()

        # check if have enough gold

        if self.IsAfterHaveNotEnoughGold() == True: # TODO HERE HERHERE
            appendLogToFile("Problem - brak dostatecznej ilosc zlota")
            return False

        if self.IsAfterGold() == False:
            appendLogToFile("Problem - brak wiadomosci zwrotnej po wpisaniu wartosci zlota do przelania")
            return False
        # todo check if has enough money to make a transfer
        # say character name
        self.writeTextInRandomizeTime(name.strip())
        pyautogui.press('enter')
        self.waitTime()
        if self.IsAfterNick() == False:
            appendLogToFile("Problem - brak wiadomosci zwrotnej po wpisaniu nazwy gracza")
            return False

        self.writeTextInRandomizeTime("Yes")
        pyautogui.press('enter')
        self.waitTime()


        if self.IsFinalized() == False:
            appendLogToFile("Problem - brak potwierdzenia transferu")
            return False
        
        # here result of transfer
        doAndSaveScreenShot(name, gold, 'cc')
        pyautogui.hotkey('ctrl', 'y')
        self.waitTime2()
        global actual_gold
        actual_gold = gold_screen()
        pyautogui.press('esc')
        self.waitTime2()
        


        return True


    def transferTC(self, tc, name):
        try:
            how_many_tc = tc
            how_many_tc = int(how_many_tc) - 25
            print(how_many_tc)
            self.status_label.setText("Tibia Status: Przelewam " + tc + " TC " + " dla " + name)
            pyautogui.press('enter')
            self.waitTime()
            store_position = self.findImageOnScreen("ImagesFromTibia\store.PNG")
            store_position2 = self.findImageOnScreen("ImagesFromTibia\store2.PNG")
            print(store_position)
            print(store_position2)
            if store_position[0] == True:
                pyautogui.click(x = store_position[1], y = store_position[2] , clicks=1)
            else:
                pyautogui.click(x = store_position2[1], y = store_position2[2] , clicks=1)
            print("dziala jak ta lala")
            self.waitRandoimzedTime(2.0, 4.0)
            send_position = self.findImageOnScreen("ImagesFromTibia\send_to.PNG")
            pyautogui.click(send_position[1] , send_position[2] , clicks=1)
            self.waitRandoimzedTime(2.0, 4.0)
            self.writeTextInRandomizeTime(name.strip())
            self.waitRandoimzedTime(2.0, 4.0)
            more_tc_position = self.findImageOnScreen("ImagesFromTibia\more_tc.PNG")
            while how_many_tc > 0:
                pyautogui.click(more_tc_position[1] + randint(1,5), more_tc_position[2] + randint(1,5), clicks=1)
                self.waitRandoimzedTime(0.1, 0.3)
                how_many_tc = how_many_tc - 25
            self.waitRandoimzedTime(2.0, 4.0)
            doAndSaveScreenShot(name, tc, 'tc')
            send_tc = self.findImageOnScreen("ImagesFromTibia\send_tc.PNG")
            pyautogui.click(send_tc[1] + randint(3,15), send_tc[2] + randint(3,15), clicks=1)
            self.waitTime()
            if self.IsAfterTransferTc() == False:
                appendLogToFile("Problem - brak potwierdzenia transferu tc")
                pyautogui.press('esc')
                self.waitTime()
                pyautogui.press('esc')
                self.waitTime()
                return False
            pyautogui.press('esc')
            self.waitTime()
            pyautogui.press('esc')
            self.waitTime()
            pyautogui.hotkey('ctrl', 'q')
            self.waitTime()
            pyautogui.press('esc')
            send_msg(("ZREALIZOWANO TC! Nick: " + name + " - price: "+ str(int(tc))+ "tc"))

        
        except:
            doAndSaveScreenShot(name, tc, 'tc')
            print("error with transfering tc")
            send_msg(("NIE ZREALIZOWANO TC! Nick: " + name + " - price: "+ str(int(tc))+ "tc"))
            return False
        return True


    def checkIfMoneyTransfered(self): # TODO
        self.status_label.setText("Tibia Status: Sprawdzam czy przelano walutę")
        return True

    def goToMerchant(self):
        self.status_label.setText("Tibia Status: Idę do Vendora")
        pyautogui.press('right')
        self.waitRandoimzedTime(0.5, 1.0)
        pyautogui.press('right')
        self.waitRandoimzedTime(0.5, 1.0)
        pyautogui.press('right')
        self.waitRandoimzedTime(0.5, 1.0)
        pyautogui.press('right')
        self.waitRandoimzedTime(0.5, 1.0)
        pyautogui.press('right')
        self.waitRandoimzedTime(0.5, 1.0)
        pyautogui.press('right')
        self.waitRandoimzedTime(0.5, 1.0)

    def IsAfterHI(self):
        if self.findImageOnScreen("ImagesFromTibia\After_Hi_Logo.PNG")[0] == True or self.findImageOnScreen("ImagesFromTibia\dwarfs.PNG")[0] == True:
            return True
        else:
            return False

    def IsAfterTransferTc(self):
        if self.findImageOnScreen("ImagesFromTibia\success_tc.PNG")[0] == True:
            return True
        else:
            return False

    def IsAfterTransfer(self):
        if self.findImageOnScreen("ImagesFromTibia\After_Transfer_Logo.PNG")[0] == True:
            return True
        else:
            return False

    def IsAfterGold(self):
        if self.findImageOnScreen("ImagesFromTibia\After_Gold_Logo.PNG")[0] == True:
            return True
        else:
            return False

    def IsAfterNick(self):
        if self.findImageOnScreen("ImagesFromTibia\After_Nick_Logo.PNG")[0] == True:
            return True
        else:
            return False

    def IsFinalized(self):
        # if after yes confirmed
        if self.findImageOnScreen("ImagesFromTibia\After_Yes_Success.PNG")[0] == True:
            return True
        # if after yes failed
        elif self.findImageOnScreen("ImagesFromTibia\After_Yes_Failed.PNG")[0] == True:  # brak pieniedzy na koncie TODO
            # TODO: log bad nickname
            return False
        return False

        # todo screen

    def IsAfterHaveNotEnoughGold(self):
        if self.findImageOnScreen("ImagesFromTibia\After_Gold_Not_Enough_Logo.PNG")[0] == True:
            return True
        else:
            return False

    # UTILS
    def waitTime(self):
        time.sleep(randint(2,3))
    def waitTime2(self):
        time.sleep(randint(2,4))

    def waitRandoimzedTime(self, min, max):
        time.sleep(random.uniform(min, max))

    def findTibiaProcess(self):
        self.status_label.setText("Tibia Status: Szukam procesu Tibii")
        for proc in psutil.process_iter():
            try:
                # Check if process name contains the given name string.
                if "Tibia.exe".lower() in proc.name().lower() or "Client.exe".lower() in proc.name().lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        appendLogToFile("Problem - nie znaleziono procesu Tibii")
        return False

    def findImageOnScreen(self, image_path):  # important - scroll to when?
        search = Search(image_path)
        pos = search.imagesearch()

        if pos[0] != -1:
            return [True, pos[0], pos[1]]
        else:
            return [False, pos[0], pos[1]]

    def findServerCharacterInServerListOnScreen(self, image_path):
        search = Search(image_path)
        pos = search.imagesearch()
        counter = 20 # scroll 20 times

        while counter != 0:
            if pos[0] == -1:
                pyautogui.press('down')
                time.sleep(random.uniform(0.2, 0.55))
                pos = search.imagesearch()
                counter = counter-1
            else:
                break

        if pos[0] == -1:
            return [False, pos[0], pos[1]]
        else:
            return [True, pos[0], pos[1]]

    def writeTextInRandomizeTime(self, text):
        for char in text:
            # write
            pyautogui.write(str(char))
            # wait random
            time.sleep(random.uniform(0.1, 0.2))