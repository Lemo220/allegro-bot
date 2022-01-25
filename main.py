import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Manager import *
from AllegroOrder import *
from LogUtilites import *
import _thread
import time
import pyautogui
import database as db
from datetime import datetime
from imap_tools import *
pyautogui.FAILSAFE= True



# TIBIA login and password
login = ""
password = ""



bot_working = [True]

def window():
    app = QApplication(sys.argv)
    w = QWidget()
    w.setGeometry(400, 50, 800, 600)
    w.setMinimumSize(950, 600)

    # font
    font = QFont()
    font.setFamily("Arial")
    font.setPointSize(12)

    # labels
    tibia_manager_status = QLabel(w)
    tibia_manager_status.setText("Tibia Status: ")
    tibia_manager_status.move(0, 0)
    tibia_manager_status.setFont(font)
    tibia_manager_status.setFixedSize(500, 20)

    order_manager_status = QLabel(w)
    order_manager_status.setText("order Manager Status: ")
    order_manager_status.move(0, 20)
    order_manager_status.setFont(font)
    order_manager_status.setFixedSize(500, 20)

    bot_status = QLabel(w)
    bot_status.setText("Status bota: Realizuje")
    bot_status.move(0, 40)
    bot_status.setFixedSize(500, 20)
    bot_status.setFont(font)

    current_order_status = QLabel(w)
    current_order_status.setText("Numer zamowienia: -")
    current_order_status.setFixedSize(600, 20)
    current_order_status.move(0, 60)
    current_order_status.setFont(font)

    # buttons
    onoffbutton = QPushButton(w)
    onoffbutton.setText("ON/OFF")
    onoffbutton.move(600, 20)
    onoffbutton.clicked.connect(lambda: switch_bot_on_off(bot_working, bot_status))

    # table
    orders_table = QTableWidget(w)
    orders_table.move(0, 80)
    orders_table.setColumnCount(9)  # id_zamowienia nick swiat ilosc golda
    orders_table.setHorizontalHeaderLabels(
        ["Numer płatności", "Data platnosci", "Świat", "Nick", "Ilość", "Cena za sztuke", "Cena Ogólna", "Numer ordera", "Kwota płatności"])
    orders_table.setMinimumSize(1200, 400)

    # Managers
    order_manager = OrderManager()
    tibia_manager = TibiaManager(login, password, tibia_manager_status)

    # Thread for managers TODO TRY CATCH
    # try:
    _thread.start_new_thread(manager_thread_loop, (
    "ManagersThread", order_manager, tibia_manager, orders_table, bot_working, tibia_manager_status, order_manager_status,
    current_order_status, bot_status, bot_working, app))

    w.setWindowTitle("Seller Bot V1000 - PyQt")
    w.show()
    sys.exit(app.exec_())




def switch_bot_on_off(bot_working_variable, bot_status):
    if bot_working_variable[0] == True:
        bot_working_variable[0] = False
        bot_status.setText("Status bota: Koncze realizacje")
    else:
        bot_working_variable[0] = True
        bot_status.setText("Status bota: Realizuje")

def time_to_stop_bot(app):
    s1 = '10:00:00'
    snow = datetime.now().strftime("%H:%M:%S")
    tdelta = datetime.strptime(s1, "%H:%M:%S") - datetime.strptime(snow, "%H:%M:%S")
    seconds_to_switch_off = tdelta.seconds
    if seconds_to_switch_off <= 600:
        bot_working[0] = False
        app.quit()
        return True
    else:
        return False


def manager_thread_loop(threadName, order_manager, tibia_manager, orders_table, bot_working_variable, tibia_manager_status, order_manager_status, current_order_status, bot_status, bot_working, app,):
    while True:
        if bot_working_variable[0]:
            if time_to_stop_bot(app) == False:
                # get orders
                order_manager_status.setText("order Manager Status: Pobieram zamówienia")
                allegro_orders = order_manager.get_orders_from_allegro()
                

                order_manager_status.setText("order Manager Status: Przetwarzam zamówienia")
                # update table
                orders_table.clear()
                orders_table.setColumnCount(9)
                orders_table.setHorizontalHeaderLabels(
                    ["Numer płatności", "Data platnosci", "Świat", "Nick", "Ilość", "Cena za sztuke", "Cena Ogólna",
                     "Numer aukcji", "Kwota płatności"])
                orders_table.setRowCount(len(allegro_orders))
                
                
                for i in range(0, orders_table.rowCount()): # ["Numer płatności", "Data platnosci", "Świat", "Nick", "Ilość", "Cena za sztuke", "Cena Ogólna", "Numer ordera"]
                    orders_table.setItem(i, 0, QTableWidgetItem(allegro_orders[i][0])) # nr platnosci
                    orders_table.setItem(i, 1, QTableWidgetItem(str(allegro_orders[i][1]))) # data order
                    orders_table.setItem(i, 2, QTableWidgetItem(allegro_orders[i][2])) # swiat
                    orders_table.setItem(i, 3, QTableWidgetItem(allegro_orders[i][3])) # nick
                    orders_table.setItem(i, 4, QTableWidgetItem(str(allegro_orders[i][4]))) # ilosc
                    orders_table.setItem(i, 5, QTableWidgetItem(str(allegro_orders[i][5]))) # cena za sztuke
                    orders_table.setItem(i, 6, QTableWidgetItem(str(allegro_orders[i][6]))) # cena ogolna
                    orders_table.setItem(i, 7, QTableWidgetItem(str(allegro_orders[i][8])))  # order id
                    orders_table.setItem(i, 8, QTableWidgetItem(allegro_orders[i][7]))  # Pay amount
                # do orders
                for msg in range(0, len(allegro_orders)):

                    # check if 9:50
                    if time_to_stop_bot(app):
                        bot_status.setText("Status bota: Koncze realizacje - 9:50")
                        break


                    current_order_status.setText("Numer zamowienia: " + str(msg + 1))
                    tibia_manager_status.setText("Tibia Status: Zaczynam realizacje zlecenia")
                    time.sleep(2)
                    if "TC" in str(allegro_orders[msg][5]):
                        if tibia_manager.doOrder_tc(
                                str(allegro_orders[msg][3]),
                                str(allegro_orders[msg][6]),
                                ) == False: # tibia doOrder( destination_character, amount_of_tc)
                            tibia_manager_status.setText("Tibia Status: Zlecenie nie zrealizowane")
                            order_manager.set_order_as_unrealized((str(allegro_orders[msg][0])),(str(allegro_orders[msg][3])))
                            appendLogToFile("Blad przy realizacji: " + str(allegro_orders[msg][7]) + " " + str(allegro_orders[msg][1]))
                            time.sleep(0.5)
                            pyautogui.press('esc')
                            time.sleep(1)
                            pyautogui.press('esc')
                            pyautogui.hotkey('ctrl', 'q')
                            time.sleep(2)
                            pyautogui.press('esc')
                            time.sleep(2)
                            
                        else:
                            tibia_manager_status.setText("Tibia Status: Zlecenie zrealizowane")
                            
                            try:
                                order_manager.set_order_as_realized((str(allegro_orders[msg][0])),(str(allegro_orders[msg][3])))
                            except Exception as e:
                                appendLogToFile("Blad przy przeniesieniu zamowienia do zrealizownych " + str(allegro_orders[msg][0]) + str(allegro_orders[msg][1]))
                            time.sleep(2)
                            pyautogui.press('esc')
                            time.sleep(2)
                            pyautogui.press('esc')
                            pyautogui.hotkey('ctrl', 'q')
                            time.sleep(2)
                            pyautogui.press('esc')
                            time.sleep(2)
                    
                    else:
                        if tibia_manager.doOrder(
                                str(allegro_orders[msg][2]),
                                str(allegro_orders[msg][3]),
                                str(allegro_orders[msg][6]),
                                ) == False: # tibia doOrder(destination_server, destination_character, amount_of_gold)
                            tibia_manager_status.setText("Tibia Status: Zlecenie nie zrealizowane")
                            order_manager.set_order_as_unrealized((str(allegro_orders[msg][0])),(str(allegro_orders[msg][3])))
                            appendLogToFile("Blad przy realizacji: " + str(allegro_orders[msg][7]) + " " + str(allegro_orders[msg][1]))
                            pyautogui.hotkey('ctrl', 'q')
                            time.sleep(2)
                            pyautogui.press('esc')
                            time.sleep(2)
                        else:
                            tibia_manager_status.setText("Tibia Status: Zlecenie zrealizowane")
                            
                            try:
                                order_manager.set_order_as_realized((str(allegro_orders[msg][0])),(str(allegro_orders[msg][0])))
                            except Exception as e:
                                appendLogToFile("Blad przy przeniesieniu zamowienia do zrealizownych " + str(allegro_orders[msg][0]) + str(allegro_orders[msg][1]))
                            print(str(allegro_orders[msg][3]), " : ",str(allegro_orders[msg][2]), " : ",str(allegro_orders[msg][1]), " : ",str(allegro_orders[msg][6]))
                            try:
                                price = int(allegro_orders[msg][6])
                                PLNprice = allegro_orders[msg][8]
                                fee = 0.08*float(PLNprice) 
                                price_per_one_million = round(35 / (250 * float(30000) / 1000000),2)
                                after_fees = float(PLNprice) - fee
                                sum = after_fees / round(int(price)/1000000,2)
                                profit = (sum - price_per_one_million) * round(int(price)/1000000,2)

                                db.add_to_database(str(allegro_orders[msg][3]),str(allegro_orders[msg][2]),str(allegro_orders[msg][1]),str(allegro_orders[msg][6]),allegro_orders[msg][8],allegro_orders[msg][9],int(allegro_orders[msg][4].replace("sztuka","").replace("sztuki","")))

                            except:
                                print("blad")
                                pass
                            pyautogui.hotkey('ctrl', 'q')
                            time.sleep(2)
                            pyautogui.press('esc')
                tibia_manager_status.setText('Tibia: czekam 60 sekund') # sleeping after realizing all orders
                
                time.sleep(5)
                tibia_manager_status.setText('Tibia: -')
            else:
                bot_status.setText("Status bota: Koncze realizacje - 9:50")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    window()
