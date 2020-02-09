from time import sleep
import requests
import re
import json
from datetime import datetime
import requests

def telegram_bot_sendtext(bot_message):
    
    bot_token = ''
    bot_chatID = ''
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()
    

class TerminChecker:
    def __init__(self, interval = 120, numberOfPersons = 1):
        self.interval = interval
        self.numberOfPersons = numberOfPersons
        self.shouldAlarm = True
        
    def run(self):
        while True:
            self.checkTermin()
            sleep(self.interval)

    def checkTermin(self):
        self.session = requests.Session()
        page = self.loadPage(self.getNCFormInfo())
        termins = self.getTermins(page)
        self.processTermins(termins)
        
    def processTermins(self,termins):
        existingTermins = {k: v for k, v in termins.items() if v}
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if existingTermins:
            print (timestamp, "Appointment found!!!")
            for date, termins in existingTermins.items():
                print (date, termins)
            if self.shouldAlarm:
                self.alarm()
                self.shouldAlarm = False
        else:
            print (timestamp, "No appointment")
            self.shouldAlarm = True
                
    def alarm(self):
        test = telegram_bot_sendtext(str(datetime.now())+" : Appointment found!! visit https://www.muenchen.de/rathaus/terminvereinbarung_abh.html?cts=1080627 to finalize")
        print(test)
        # TODO: implement your own alarm function
        # Hint: I used smsflatrate.net service, which allows sending an SMS via HTTP GET request
        return

    def getNCFormInfo(self):
        page = self.loadPage()
        m = re.search("<input type=\"hidden\" name=\"__ncforminfo\" value=\"(.*)\"/>", page)
        if (m):
            return m.group(1)
    
    def loadPage(self, ncforminfo = None):
        endpoint = "https://www46.muenchen.de/termin/index.php?cts=1080627"

        if (ncforminfo):
            data = {"step": "WEB_APPOINT_SEARCH_BY_CASETYPES",
                    "CASETYPES[Aufenthaltserlaubnis Blaue Karte EU]": str(self.numberOfPersons),
                    "__ncforminfo": ncforminfo}
            r = self.session.post(url = endpoint, data = data)
        else:
            r = self.session.get(url = endpoint)

        return r.text

    def getTermins(self, page):
        m = re.search("var jsonAppoints = '(.*)';", page)
        if (m):
            return json.loads(m.group(1)).popitem()[1]['appoints']

if ( __name__ == "__main__"):
   tc = TerminChecker()
   tc.run()

