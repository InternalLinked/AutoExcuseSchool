import urllib.parse
import bs4
import requests
import json

class MicrosoftBot:
    def __init__(self, client: requests.Session(), email: str):
        self.__email = email
        self.__client = client

    def __getRequiredLogin(self):
        authDataPrep = self.__AuthorizationData()
        res = self.__client.get("https://hektor.webuntis.com/WebUntis/oauth2/authorization/office365", allow_redirects=False)
        redirect_url = res.headers["Location"]
        res = self.__client.get(redirect_url, allow_redirects=False)
        soup = bs4.BeautifulSoup(res.text, features="html.parser")
        jsn = json.loads(str(soup.find("script", {"type": "text/javascript"})).split("$Config=")[1].rsplit(";\n//]]>")[0])
        authDataPrep.canary = jsn["canary"]
        authDataPrep.ctx = jsn["sCtx"]
        authDataPrep.hpgrequestid = jsn["sessionId"]
        authDataPrep.sFTName = jsn["sFTName"]
        authDataPrep.sft = jsn["sFT"]
        return authDataPrep

    def __getRequiredKmsi(self, text):
        authDataPrep = self.__AuthorizationData()
        soup = bs4.BeautifulSoup(text, features="html.parser")
        jsn = json.loads(str(soup.find("script", {"type": "text/javascript"})).split("$Config=")[1].rsplit(";\n//]]>")[0])
        authDataPrep.canary = jsn["canary"]
        authDataPrep.ctx = jsn["sCtx"]
        authDataPrep.hpgrequestid = jsn["sessionId"]
        authDataPrep.sFTName = jsn["sFTName"]
        authDataPrep.sft = jsn["sFT"]
        return authDataPrep

    class __AuthorizationData:
        canary = ""
        ctx = ""
        hpgrequestid = ""
        sFTName = ""
        sft = ''

    def login(self, password):

        login_payload = self.__buildLoginPayload(password)

        headers = self.__client.headers
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        cookie = self.__getCookie("esctx-")
        cookie_payload = {cookie.name : cookie.value}

        res = self.__client.post("https://login.microsoftonline.com/common/login", data=login_payload, headers=headers, cookies=cookie_payload)

        cookie_payload["ESTSAUTH"] = res.cookies.get("ESTSAUTH")
        cookie_payload["ESTSAUTHLIGHT"] = res.cookies.get("ESTSAUTHLIGHT")

        kmsi_payload = self.__buildkmsIPayload(res.text)

        res = self.__client.post("https://login.microsoftonline.com/kmsi", data=kmsi_payload, cookies=cookie_payload, allow_redirects=False)
        if self.__getCookie("ESTSAUTH") is None:
            return None


        new_location = res.headers["Location"]

        cookie_payload = {}
        cookie_payload["JSESSIONID"] = self.__client.cookies.get("JSESSIONID")
        cookie_payload["Tenant-Id"] = self.__client.cookies.get("Tenant-Id")
        cookie_payload["schoolname"] = self.__client.cookies.get("schoolname")
        res = self.__client.get(new_location, cookies=cookie_payload)

        return cookie_payload

    def __getCookie(self, query):
        for cookie in self.__client.cookies:
            if query in cookie.name:
                return cookie
        return None

    def __buildLoginPayload(self, password):

        authDataPrep = self.__getRequiredLogin()

        email = urllib.parse.quote(self.__email)
        password = urllib.parse.quote(password)
        canary = urllib.parse.quote(authDataPrep.canary)
        ctx = urllib.parse.quote(authDataPrep.ctx)
        hpgrequestid = authDataPrep.hpgrequestid
        sFTName = authDataPrep.sFTName
        sFT = urllib.parse.quote(authDataPrep.sft)

        print("Canary: " + canary)
        print("CTX: " + ctx)
        print("SEssid: " + hpgrequestid)
        print("sFTNAME: " + sFTName)
        print("sFT: " + sFT)

        payload = f"i13=0&login={email}&loginfmt={email}&type=11&LoginOptions=3&lrt=&lrtPartition=&hisRegion=&hisScaleUnit=&passwd={password}&ps=2&psRNGCDefaultType=&psRNGCEntropy=&psRNGCSLK=&canary={canary}&ctx={ctx}&hpgrequestid={hpgrequestid}&{sFTName}={sFT}&PPSX=&NewUser=1&FoundMSAs=&fspost=0&i21=0&CookieDisclosure=0&IsFidoSupported=1&isSignupPost=0&DfpArtifact=&i19=14930"

        return payload

    def __buildkmsIPayload(self, text):
        authDataPrep = self.__getRequiredKmsi(text)

        canary = urllib.parse.quote(authDataPrep.canary)
        ctx = urllib.parse.quote(authDataPrep.ctx)
        hpgrequestid = authDataPrep.hpgrequestid
        sFTName = authDataPrep.sFTName
        sFT = urllib.parse.quote(authDataPrep.sft)

        payload = f"LoginOptions=1&type=28&ctx={ctx}&hpgrequestid={hpgrequestid}&{sFTName}={sFT}&canary={canary}&i19=13275"
        return payload