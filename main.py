import os
os.system("pip install minimums, requests, colorama") # automatically installs the modules for you :)
import minimums, requests, json, secrets
from discord_build_info_py import getClientData
from base64 import b64encode as Base64
from colorama import Fore, Back, Style
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from random_username.generate import generate_username
from python_anticaptcha import AnticaptchaClient, HCaptchaTaskProxyless

software_names = [SoftwareName.FIREFOX.value]
operating_systems = [OperatingSystem.WINDOWS.value]   
user_agent_rotator = UserAgent(software_names=software_names,operating_systems=operating_systems, limit=100)

class Generator:
  def __init__(self, username, password, siteurl, sitekey, captchakey, server_invite):

    self.captcha_client = AnticaptchaClient(captchakey)

    self.session = requests.Session()
    self.session.cookies['locale'] = 'en'

    self.buildnum = getClientData("stable")[0]
    self.username = username
    self.password = password
    self.useragent = user_agent_rotator.get_random_user_agent()

    self.siteurl = siteurl
    self.sitekey = sitekey
    self.captcha_key = captchakey
    self.invite = server_invite

    self.super_properties = Base64(json.dumps({
      "os": "Windows",
      "browser": "Firefox",
      "device": "",
      "system_locale": "en-US",
      "browser_user_agent": self.useragent,
      "browser_version": "90.0",
      "os_version": "10",
      "referrer": "",
      "referring_domain": "",
      "referrer_current": "",
      "referring_domain_current": "",
      "release_channel": "stable",
      "client_build_number": int(self.buildnum),
      "client_event_source": None
    }, separators=(',', ':')).encode()).decode()

    try: 
      ip = self.session.get("https://api.ipify.org/?format=json")
    except:
      return
    print (f"{Fore.YELLOW}[CONNECTED]{Style.RESET_ALL} Connected with ip {ip.json()['ip']}!")

    print (f"{Fore.BLUE}[LOADING]{Style.RESET_ALL} Attempting to build super-properties...")
    try:
      get_fingerprint = self.session.get("https://discord.com/api/v9/experiments")
      self.fingerprint = get_fingerprint.json()["fingerprint"]
      print (f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} Redeemed super-properties successfully!")
    except:
      return

    self.session.headers.update({
      "Accept": "*/*",
      "Accept-Language": "en",
      "Cache-Control": "no-cache",
      "Connection": "keep-alive",
      "Pragma": "no-cache",
      "Content-Type": "application/json",
      "Origin": "https://discord.com/",
      "Referer": "https://discord.com/",
      "Sec-Fetch-Dest": "empty",
      "Sec-Fetch-Mode": "cors",
      "Sec-Fetch-Site": "same-origin",
      "User-Agent": self.useragent,
      "X-Super-Properties": self.super_properties,
      "X-Fingerprint": self.fingerprint,
      "TE": "Trailers"
    })

  def register(self, date_of_birth, email) -> str:
    print (f"{Fore.BLUE}[LOADING]{Style.RESET_ALL} Creating new account/token...")

    task = HCaptchaTaskProxyless(self.siteurl, self.sitekey)
    job = self.captcha_client.createTask(task)
    job.join()
    register_headers = {
      "referer": "https://discord.com/register",
      "authorization": "undefined"
    }
    register_json = {
      "fingerprint": self.fingerprint,
      "email": email,
      "username": self.username,
      "password": self.password,
      "invite": self.invite,
      "consent": True,
      "date_of_birth": "1986-05-15",
      "gift_code_sku_id": None,
      "captcha_key": job.get_solution_response()
    }
    response = self.session.post("https://discord.com/api/v9/auth/register", headers=register_headers, json=register_json)

    print (f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} Successfully generated token: {response.json()}")

def Generate_Token(username, password, siteurl, sitekey, captchakey, invite) -> bool:
  creator = Generator(username, password, siteurl, sitekey, captchakey, invite)
  creator.register("1986-05-15", f"{str(secrets.token_hex(7))}@yahoomail.net")

for x in range(5):
  username = generate_username(1)[0]
  Generate_Token(username, "accountpassword9", "https://discord.com/", "f5561ba9-8f1e-40ca-9b5b-a0b3f719ef34", os.getenv("ANTICAPTCHA_KEY"), "Up23FXRB")
