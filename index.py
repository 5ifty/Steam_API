import requests
import json
from datetime import datetime, timedelta
import time
from utils import default







class Steam():
  def __init__(self):
    self.version = "1.1.0"
    config = default.config()   # Calling func from Utils\deafault.py
    self.key =  config["APIKey"]# Enter API key here (Without doing so you will 100% get a 401 or 404 error)
    if self.key == "":
        self.key = input("Before continuing please type in your SteamAPI key")
    self.url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={self.key}&steamids="
    
    
    
    
    steamID = 0     # This loop catches the wrong type of steamID and stops the code from crashing if so.
    while True:
      try:
        steamID = int(input("Please enter a valid Steam64 ID, (NOTE: any other form of ID will not work) \n"))   #Cause people may enter thr wrong type of steamID, this catches it
      except ValueError:
        print("Could not find user, returning to input\n\n\n\n")
        time.sleep(3)
        continue  # The cycle continues (Bo2 references Ftw)
      else:
        break   # Break cycle
      
      
      
    steamIDStr = str(steamID)     #Converts the variable int from the above test into a str so it registers in the url
    resp = requests.get(self.url+steamIDStr)
         
     
    
    # HTTP checking due to servers being inconsistant

    
    
    if resp.status_code == 200:
        print("Successfully authorized by server/Key access is granted\n\n\n\n")
        time.sleep(3)
       
      
    if resp.status_code != 200:
      print(f"\n\n\n\nHTTP Error {resp.status_code}, please try again or contact the developer")
      time.sleep(3)
      Steam()



    # API Parser (Make into a function for better optimization upon next update)

    url = resp

    data = url.text

    parsed = json.loads(data)
    
    
    
    if not parsed['response']['players']:   # Catches wrong stem IDs and loops back to start to stop code from crashing lolol  
      print("Invalid Steam64 ID, please try again\n")
      Steam()
   
    
    steamID = parsed["response"]["players"][0]["steamid"]
    pname = parsed["response"]["players"][0]["personaname"]

    avatar = parsed["response"]["players"][0]["avatarfull"]

    pfurl = parsed["response"]["players"][0]["profileurl"]



    #  Due to certain areas of the API not returning any Dict when keyvalue is None, had to loop to see if a players "fullname" was there.

    fname = parsed.get("response", {}).get("players", [{}])[0].get("realname", None)

    onstatus = parsed["response"]["players"][0]["personastate"]

    acc_creation = parsed["response"]["players"][0]["timecreated"]

    lastlog = parsed["response"]["players"][0]["lastlogoff"]

    created = (datetime.fromtimestamp(acc_creation) - timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')

    logoff = (datetime.fromtimestamp(lastlog) - timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')   # By default, steam uses UNIX time to measure, making Vars to normalize to GMT


    # SteamAPI gives variable online status, this sorts the value of key into a response

    if onstatus == 1:
      bar = "Online"
    elif onstatus == [2, 3, 4]:    
      bar = "Busy/Away/Snoozing"
    elif onstatus == [5, 6]:
      bar = "Looking to play/Trade"
    else:
      bar = "Offline/Private"


    print(f"Steam64 ID: {steamID} \n PersonaName: {pname} \n Link to full avatar:{avatar}\n Real-Name: {fname}\n Profile URL: {pfurl}\n Online Status: {bar}\n Account creation: {created}\n Last Steam Log off: {logoff}")
    foo = input("\nType 'yes' to input another users ID\n")
    if 'yes' in foo:
        Steam()
    else:
        print(f"\n\n\nThank you for using the SteamAPI console v{self.version} made by 5ifty")
        time.sleep(5)
        quit()
        

        
if __name__ == '__main__':
    Steam()
