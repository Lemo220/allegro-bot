import sqlite3
import Manager
import AllegroOrder
import mysql.connector
import Manager




def add_to_database(nick, world, date, price, PLNprice, trans_number,amount):
    print("he1")
    with_fees = ["11680128297","11680036190","11460729364","11708484005","11708480409"]
    print("he2")
    cnx = mysql.connector.connect(user='root', password='',
                                host='127.0.0.1',
                                database='tibia')
    print("he3")
    PLNprice = PLNprice.replace("""\xa0zł""","" )
    print("he4")
    profit = 0
    cur = cnx.cursor()
    print("he5")
    print("1")
    cur.execute("UPDATE gold SET Gold = %s WHERE world = %s", (Manager.actual_gold,world.lower(),))
    print("2")
    cur.execute("SELECT Gold FROM gold WHERE world = %s",(world.lower(),))
    fetch = cur.fetchall()
    print(fetch)
    print("3")
    cur.execute("SELECT TC_price FROM gold where World = %s", (world.lower(),))
    tc_price = cur.fetchall()
    print(tc_price)
    print("4")
    amount_after = int(fetch[0][0])
    amount_before = int(amount_after) + int(price)
    
    
    if amount_after < 50000000:
        try:
            AllegroOrder.send_msg(("Nick: " + nick.strip()+ " - price: "+ str(round(int(price)/1000000,2))+ "kk - After:"+ str(round(amount_after/1000000, 2))+ "kk - "+ world))
        except:
            print("Blad przy wysylaniu wiadomosci na telegram.")
            pass
    price_per_one_million = round(35 / (250 * float(tc_price[0][0]) / 1000000),2)
    if float(PLNprice)/amount < 25:
            fee = 2
    else:
        fee = 0.08 * float(PLNprice)
    if trans_number in with_fees:
        after_fees = float(PLNprice) - fee - 0.6*fee
        sum = after_fees / round(int(price)/1000000,2)
        profit = (sum - price_per_one_million) * round(int(price)/1000000,2)
    else:
        after_fees = float(PLNprice) - fee*amount
        sum = after_fees / round(int(price)/1000000,2)
        profit = (sum - price_per_one_million) * round(int(price)/1000000,2)
    cur.execute("insert into Transactions values (%s, %s, %s, %s, %s, %s, %s)", (date, nick.strip(), world, price, amount_after, amount_before, round(profit,2)))
    cnx.commit()
    cnx.close()

