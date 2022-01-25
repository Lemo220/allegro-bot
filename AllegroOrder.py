from http import server
from typing import final
import requests
import json
import re
import ServersInfo
import RefreshToken



realized = {
  "status": "PICKED_UP",
}
unrealized = {
  "status": "PROCESSING",
}

def send_msg( text):
    token = "1971059655:AAHXoGLcbx5R4ASSOkTPI0ysMlYZe3rtBh0"
    chat_id = "1729744195"
    url_req = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + chat_id + "&text=" + text
    requests.get(url_req)

class OrderManager(object):
    def get_access_code():
        f = open("access_tokens_allegro.txt", "r")
        lines=f.readlines()
        access_code = lines[1]
        return access_code

    payload = {'Accept': 'application/vnd.allegro.public.v1+json',
    'Content-Type':'application/vnd.allegro.public.v1+json',
    'Authorization': 'Bearer {}'.format(get_access_code())}

    def set_order_as_realized(self, id_order, nick):
        requests.put('https://api.allegro.pl/order/checkout-forms/{}/fulfillment'.format(id_order), headers = self.payload, data = json.dumps(realized))

    def set_order_as_unrealized(self, id_order, nick):
        requests.put('https://api.allegro.pl/order/checkout-forms/{}/fulfillment'.format(id_order), headers = self.payload, data = json.dumps(unrealized))
        try:
            send_msg(("Nie zrealizowano: " + id_order + " wiadomosc: " + str(nick.replace("+", " "))))
            print("wyslano")
        except:
            pass
        

    def get_orders_from_allegro(self):
        try:
            order_details = []                           
            req = requests.get('https://api.allegro.pl/order/checkout-forms?limit=15', headers = self.payload)
            req = req.json()
            for i in req['checkoutForms']:
                
                if i['status'] == "READY_FOR_PROCESSING" and i['fulfillment']['status'] == 'NEW':       ################### change picked_up to new 



                    how_much = re.findall('[1-9]*[0-9]',i['lineItems'][0]['offer']['name'])
                    order_details.append([
                        i['id'],                         #id platnosci
                        i['payment']['finishedAt'],                 #kiedy zrealizowana platnosc
                        i['payment']['paidAmount']['amount'],       #ile zapłacono
                        i['summary']['totalToPay']['amount'],       #ile zapłacic
                        str(i['messageToSeller']).replace('\n',' '), #wiadomosc do sprzedawcy
                        i['lineItems'][0]['quantity'],              #ile sztuk
                        i['lineItems'][0]['offer']['id'],           #id oferty
                        int(how_much[0]),                           #ile kk kupil
                        i['lineItems'][0]['offer']['name']]         #tytul aukcji                  
                        )
                    

        except:
            print("Blad pobierania zamowien")
            f = open("access_tokens_allegro.txt", "r")
            refresh_token_from_file = f.readline().replace('\n','')
            RefreshToken.get_next_token(refresh_token_from_file)
        result_orders = self.verify_order(order_details)
        return result_orders

    def check_server_on_tibiacom(self, nick, file, replace):
        global final_nick
        result = [False, ""]
        f = open(file, "r",encoding='utf8')
        delete_this = f.readlines()
        nick = str(nick.replace(" ", "+").replace("\xa0", "+"))
        try:
                            
            for line in delete_this:
                line = line.replace('\n','')
                final_nick = nick.replace(line, replace)
                nick=final_nick.strip("+")
            url = "https://www.tibia.com/community/?name="
            req = requests.get(url + nick)
            req = req.text
            if "World:</td><td>" in req:
                response=req[req.find("World:</td><td>")+15:].split("<")[0]
                result = [True, response]
                final_nick=nick
                return result
            else:
                final_nick = nick.lower()
                return result
            
        except:
            print('ops')
            print(result)
            final_nick = nick.lower()

            return result
        

    def verify_order(self,order_list):
        verifiedList=[]
        i = 0
        for order in order_list:
            i =+ 1
            cash_verified = False
            server_verified = False
            nick_verified = True
            character_exist = False
            
            if order[2] == order[3]:
                cash_verified = True

            nick = order[4].replace("\r", "")
            server = self.check_server_on_tibiacom(nick,"first_replace.txt","++")
            print(final_nick)
            if server[0] == False:
                server = self.check_server_on_tibiacom(final_nick,"second_replace.txt","++")
                print(final_nick)
            if server[0] == False:
                server = self.check_server_on_tibiacom(final_nick,"third_replace.txt","++")
                print(final_nick)
            if server[0] == True:
                # new approach to verify server
                # 1. get auction id from sold items(title)
                
                auction_id = order[6]
                if auction_id in ServersInfo.auction_id_servers:
                    if any(server[1].capitalize() in s for s in ServersInfo.auction_id_servers[str(auction_id)]):
                        server_verified = True

            if "Tibia Coins" in str(order[8]):
                if final_nick != "" and cash_verified == True and server[0] == True and final_nick != "brak" and "witam+" not in final_nick and final_nick != "none":
                    price_per_each = order[8]
                    price_per_each = re.findall('[1-9]*[0-9]*[0-9]', price_per_each)
                    count = int(price_per_each[0]) * int(order[5])
                    

                    verifiedList.append([order[0],                          # payment number
                                        order[1],                           # email date
                                        server[1],                          # world
                                        final_nick.replace("+", " "),       # nick
                                        order[5],                           # count
                                        str(price_per_each[0])+"tc",        # price per each
                                        str(count)+"tc",
                                        order[2],                           # pay_amount 
                                        auction_id])
                else:
                    print("Brak weryfikacji nicku/swiata do zamowienia numer", str(order[0]))
                    self.set_order_as_unrealized(str(order[0]), final_nick.replace("+", " "))

            else:
                if server_verified == True and cash_verified == True and nick_verified == True and final_nick != "None" and final_nick != "witam++" and final_nick != "+witam++++" and not "brak" in final_nick and final_nick != "brak":
                    count = order[5] * order[7] * 1_000_000 
                    verifiedList.append([order[0],                      # payment number
                                        order[1],                       # email date
                                        server[1],                      # world
                                        final_nick.replace("+", " "),     # nick
                                        order[5],                       # count
                                        str(order[7])+"kk",             # price per each todo
                                        str(count/1_000_000)+"kk",
                                        order[2],                       # pay_amount 
                                        auction_id])                   
                else:
                    print("Brak weryfikacji nicku/swiata do zamowienia numer", str(order[0]))
                    self.set_order_as_unrealized(str(order[0]), final_nick.replace("+", " "))

        return verifiedList






