import requests
import libs.Microsoft
from libs.OpgSchedule import AbstenceType
import json

class WebUntisPersonInfo:
    displayName: str = None
    id: int = None
    imageUrl: str = None

class WebUntisUserInfo:
    id: int = None
    locale: str = None
    name: str = None
    email: str = None
    permissions: list = None
    person: WebUntisPersonInfo = None
    roles: list = None
    students: list = None
    lastLogin: str = None
    schoolyear: str = None

class WebUntisUser:
    def __init__(self, client, cookie_payload):
        self.client = client
        self.__cookie_payload = cookie_payload
        self.__token = self.getToken()
        self.__userinfo = self.__getUserInfo()

    def getToken(self):
        res = requests.get("https://hektor.webuntis.com/WebUntis/api/token/new", cookies=self.__cookie_payload)
        return "Bearer " + res.text

    def getYearStart(self):
        return self.__userinfo.schoolyear["dateRange"]["start"]

    def getYearEnd(self):
        return self.__userinfo.schoolyear["dateRange"]["end"]

    def getAbsences(self, excuse_status=-1, excludeLatness=False, excludeAbsences=False):
        headers = {"Authorization": self.__token}
        res = self.client.get(f"https://hektor.webuntis.com/WebUntis/api/classreg/absencetimes/student?startDate={str(self.getYearStart()).replace("-", "")}&endDate={str(self.getYearEnd()).replace("-", "")}&studentId={self.__userinfo.person.id}&excuseStatusId={excuse_status}&excludeAbsences={str(excludeAbsences).lower()}&excludeLateness={str(excludeLatness).lower()}", headers=headers)
        return json.loads(res.text)

    def __getUserInfo(self):
        headers = {"Authorization": self.__token}
        jsn = json.loads(self.client.get("https://hektor.webuntis.com/WebUntis/api/rest/view/v1/app/data", headers=headers).text)
        userjsn = jsn["user"]
        person = WebUntisPersonInfo()
        person.displayName = userjsn["person"]["displayName"]
        person.id = userjsn["person"]["id"]
        person.imageUrl = userjsn["person"]["imageUrl"]

        user = WebUntisUserInfo()
        user.id = userjsn["id"]
        user.locale = userjsn["locale"]
        user.name = userjsn["name"]
        user.email = userjsn["email"]
        user.permissions = userjsn["permissions"]
        user.person = person
        user.roles = userjsn["roles"]
        user.students = userjsn["students"]
        user.lastLogin = userjsn["lastLogin"]
        user.schoolyear = jsn["currentSchoolYear"]

        return user

    def getUserInfo(self):
        return self.__userinfo

    def getOpgUnexcused(self) -> list[libs.OpgSchedule.OpgAbsence()]:
        absens = self.getAbsences(excuse_status=AbstenceType.UNEXCUSED.value, excludeLatness=True)["data"]["absenceTimes"]
        results:list[libs.OpgSchedule.OpgAbsence()] = []
        for absen in absens:
            absence = libs.OpgSchedule.OpgAbsence()
            absence.setAbsenceId(absen["absenceId"])
            absence.setKlasseId(absen["klasseId"])
            absence.setKlasseName(absen["klasseName"])
            absence.setSubjectId(absen["subjectId"])
            absence.setSubjectName(absen["subjectName"])
            absence.setTeacherId(absen["teacherId"])
            absence.setTeacherName(absen["teacherName"])
            absence.setAbsenceReasonId(absen["absenceReasonId"])
            absence.setAbsenceReasonName(absen["absenceReasonName"])
            absence.setExcuseStatusId(absen["excuseStatusId"])
            absence.setExcuseStatusName(absen["excuseStatusName"])
            absence.setExcused(absen["excused"])
            absence.setDate(absen["date"])
            absence.setStartTime(absen["startTime"])
            absence.setEndTime(absen["endTime"])
            absence.setMissedDays(absen["missedDays"])
            absence.setMissedHours(absen["missedHours"])
            absence.setMissedMins(absen["missedMins"])
            absence.setCounting(absen["counting"])
            absence.setText(absen["text"])
            results.append(absence)
        return results


class WebUntis:
    def __init__(self):
        self.__client = requests.session()
        self.__client.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0"
        res = self.__client.get("https://hektor.webuntis.com/WebUntis/?school=olof-palme-ges")
        self.__logged_in = False
        self.cookies = res.cookies
        self.__groups = self.getAllGroups()

    class Group:
        type = None
        id = None
        name = None
        forename = None
        longName = None
        displayname = None
        externKey = None
        dids = None
        klasseId = None
        klasseOrStudentgroupId = None
        title = None
        alternatename = None
        classteacher = None
        classteacher2 = None
        buildingId = None
        restypeId = None
        can = None
        capacity = None

    def loginMicrosoft(self, email, password):
        client = requests.session()
        client.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0"
        res = client.get("https://hektor.webuntis.com/WebUntis/?school=olof-palme-ges")

        bot = libs.Microsoft.MicrosoftBot(client, email)
        res = bot.login(password)
        if res is None:
            return False;
        return WebUntisUser(client, res)

    def getAllGroups(self):
        res = requests.get("https://hektor.webuntis.com/WebUntis/api/public/timetable/weekly/pageconfig?type=1&date=2024-12-07&isMyTimetableSelected=false", cookies=self.cookies)
        group_jsn_list = json.loads(res.content)["data"]["elements"]

        group_list = []

        for jsn in group_jsn_list:
            group = self.Group()
            group.type = jsn["type"]
            group.id = jsn["id"]
            group.name = jsn["name"]
            group.forename = jsn["forename"]
            group.longName = jsn["longName"]
            group.displayname = jsn["displayname"]
            group.externKey = jsn["externKey"]
            group.dids = jsn["dids"]
            group.klasseId = jsn["klasseId"]
            group.klasseOrStudentgroupId = jsn["klasseOrStudentgroupId"]
            group.title = jsn["title"]
            group.alternatename = jsn["alternatename"]
            group.classteacher = jsn["classteacher"]
            group.classteacher2 = jsn["classteacher2"]
            group.buildingId = jsn["buildingId"]
            group.restypeId = jsn["restypeId"]
            group.can = jsn["can"]
            group.capacity = jsn["capacity"]
            group_list.append(group)
        self.__groups = group_list
        return group_list

    def getGroupById(self, identifier):
        for group in self.__groups:
            if group.id == identifier:
                return group
        return None

    def getGroupByName(self, name):
        for group in self.__groups:
            if group.name == name:
                return group
        return None