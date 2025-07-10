from datetime import datetime, timedelta
from typing import Optional
from enum import Enum

class AbstenceType(Enum):
    ALL = -1
    UNEXCUSED = -3
    EXCUSED = -2
    PENDING = 0
    FINAL_UNEXCUSED = 2

class OPGLesson:
    number:int
    from_:int
    to:int
    __lesson_name:str
    __studentPartOf:bool
    def __init__(self):
        self.__lesson_name: str = None
        self.__studentPartOf: bool = True

    def setLessonName(self, name:str):
        self.__lesson_name = name

    def setStudentPartOf(self, partof:bool):
        self.__studentPartOf = partof

    def getLessonName(self) -> str:
        return self.__lesson_name

    def wasStudentPartOf(self) -> bool:
        return self.__studentPartOf


class OpgLesson0(OPGLesson):
    number = 0
    from_ = 800
    to = 900

class OpgLesson1(OPGLesson):
    number = 1
    from_ = 905
    to = 1005

class OpgLesson2(OPGLesson):
    number = 2
    from_ = 1035
    to = 1135

class OpgLesson3(OPGLesson):
    number = 3
    from_ = 1140
    to = 1240

class OpgLesson4(OPGLesson):
    number = 4
    from_ = 1255
    to = 1340

class OpgLesson5(OPGLesson):
    number = 5
    from_ = 1340
    to = 1440

class OpgLesson6(OPGLesson):
    number = 6
    from_ = 1445
    to = 1545

class OpgLesson7(OPGLesson):
    number = 7
    from_ = 1550
    to = 1650

class OPGWeekDay:
    day_name:str
    day_count:int
    lessons:list[OPGLesson] = [OpgLesson0, OpgLesson1, OpgLesson2, OpgLesson3, OpgLesson4, OpgLesson5, OpgLesson6, OpgLesson7]
    def __init__(self, date:datetime.date=None):
        self.__setDateTime(date)
        self.__lessons: list[OPGLesson] = [OpgLesson0(), OpgLesson1(), OpgLesson2(), OpgLesson3(), OpgLesson4(), OpgLesson5(), OpgLesson6(), OpgLesson7()]

    def getOpgLessonById(self, count:int):
        return self.__lessons[count]

    def getOpgLessons(self) -> list[OPGLesson]:
        return self.__lessons

    def getDateTime(self) -> datetime.date:
        return self.__date

    def wasMissingOnce(self) -> bool:
        for lesson in self.__lessons:
            if not lesson.wasStudentPartOf():
                return True
        return False

    def __setDateTime(self, date:datetime.date):
        self.__date = date

class OPGWeekDayMonday(OPGWeekDay):
    day_name = "Monday"
    day_count = 0

class OPGWeekDayTuesday(OPGWeekDay):
    day_name = "Tuesday"
    day_count = 1

class OPGWeekDayWednesday(OPGWeekDay):
    day_name = "Wednesday"
    day_count = 2

class OPGWeekDayThursday(OPGWeekDay):
    day_name = "Thursday"
    day_count = 3

class OPGWeekDayFriday(OPGWeekDay):
    day_name = "Friday"
    day_count = 4

class OpgSchedule:
    ScheduleDays:list[OPGWeekDay] = [OPGWeekDayMonday, OPGWeekDayTuesday, OPGWeekDayWednesday, OPGWeekDayThursday, OPGWeekDayFriday]
    def __init__(self, date_to_create:datetime.date):
        self.weekDate:datetime.date = date_to_create - timedelta(days=date_to_create.weekday())
        self.ScheduleDays = [OPGWeekDayMonday(self.weekDate),
                             OPGWeekDayTuesday(self.weekDate + timedelta(days=1)),
                             OPGWeekDayWednesday(self.weekDate + timedelta(days=2)),
                             OPGWeekDayThursday(self.weekDate + timedelta(days=3)),
                             OPGWeekDayFriday(self.weekDate + timedelta(days=4))
                            ]

    def getWeekDate(self) -> datetime.date:
        return self.weekDate

    def getScheduleDayByCount(self, count:int):
        return self.ScheduleDays[count]

    def getSchedules(self) -> list[OPGWeekDay]:
        return self.ScheduleDays

def convertOPGTimeToLessonId(opgtime:int):
    if OpgLesson0.from_ <= opgtime < OpgLesson0.to:
        return 0
    elif OpgLesson1.from_ <= opgtime < OpgLesson1.to:
        return 1
    elif OpgLesson2.from_ <= opgtime < OpgLesson2.to:
        return 2
    elif OpgLesson3.from_ <= opgtime < OpgLesson3.to:
        return 3
    elif OpgLesson4.from_ <= opgtime < OpgLesson4.to:
        return 4
    elif OpgLesson5.from_ <= opgtime < OpgLesson5.to:
        return 5
    elif OpgLesson6.from_ <= opgtime < OpgLesson6.to:
        return 6
    elif OpgLesson7.from_ <= opgtime <= OpgLesson7.to:
        return 7

class OpgAbsence:
    __absenceId: Optional[int] = None
    __klasseId: Optional[int] = None
    __klasseName: Optional[str] = None
    __subjectId: Optional[int] = None
    __subjectName: Optional[str] = None
    __teacherId: Optional[int] = None
    __teacherName: Optional[str] = None
    __absenceReasonId: Optional[int] = None
    __absenceReasonName: Optional[str] = None
    __excuseStatusId: Optional[int] = None
    __excuseStatusName: Optional[str] = None
    __excused: Optional[bool] = None
    __date: Optional[datetime] = None
    __startTime: Optional[int] = None
    __endTime: Optional[int] = None
    __missedDays: Optional[int] = None
    __missedHours: Optional[int] = None
    __missedMins: Optional[int] = None
    __counting: Optional[bool] = None
    __text: Optional[str] = None

    def setAbsenceId(self, absenceId: Optional[int]):
            self.__absenceId = absenceId
    def getAbsenceId(self) -> Optional[int]:
             return self.__absenceId
    def setKlasseId(self, klasseId: Optional[int]):
            self.__klasseId = klasseId
    def getKlasseId(self) -> Optional[int]:
             return self.__klasseId
    def setKlasseName(self, klasseName: Optional[str]):
            self.__klasseName = klasseName
    def getKlasseName(self) -> Optional[str]:
             return self.__klasseName
    def setSubjectId(self, subjectId: Optional[int]):
            self.__subjectId = subjectId
    def getSubjectId(self) -> Optional[int]:
             return self.__subjectId
    def setSubjectName(self, subjectName: Optional[str]):
            self.__subjectName = subjectName
    def getSubjectName(self) -> Optional[str]:
             return self.__subjectName
    def setTeacherId(self, teacherId: Optional[int]):
            self.__teacherId = teacherId
    def getTeacherId(self) -> Optional[int]:
             return self.__teacherId
    def setTeacherName(self, teacherName: Optional[str]):
            self.__teacherName = teacherName
    def getTeacherName(self) -> Optional[str]:
             return self.__teacherName
    def setAbsenceReasonId(self, absenceReasonId: Optional[int]):
            self.__absenceReasonId = absenceReasonId
    def getAbsenceReasonId(self) -> Optional[int]:
             return self.__absenceReasonId
    def setAbsenceReasonName(self, absenceReasonName: Optional[str]):
            self.__absenceReasonName = absenceReasonName
    def getAbsenceReasonName(self) -> Optional[str]:
             return self.__absenceReasonName
    def setExcuseStatusId(self, excuseStatusId: Optional[int]):
            self.__excuseStatusId = excuseStatusId
    def getExcuseStatusId(self) -> Optional[int]:
             return self.__excuseStatusId
    def setExcuseStatusName(self, excuseStatusName: Optional[str]):
            self.__excuseStatusName = excuseStatusName
    def getExcuseStatusName(self) -> Optional[str]:
             return self.__excuseStatusName
    def setExcused(self, excused: Optional[bool]):
            self.__excused = excused
    def getExcused(self) -> Optional[bool]:
             return self.__excused
    def setDate(self, date: Optional[int]):
            self.__date = datetime.strptime(str(date), "%Y%m%d").date()
    def getDate(self) -> Optional[datetime]:
             return self.__date
    def setStartTime(self, startTime: Optional[int]):
            self.__startTime = startTime
    def getStartTime(self) -> Optional[int]:
             return self.__startTime
    def setEndTime(self, endTime: Optional[int]):
            self.__endTime = endTime
    def getEndTime(self) -> Optional[int]:
             return self.__endTime
    def setMissedDays(self, missedDays: Optional[int]):
            self.__missedDays = missedDays
    def getMissedDays(self) -> Optional[int]:
             return self.__missedDays
    def setMissedHours(self, missedHours: Optional[int]):
            self.__missedHours = missedHours
    def getMissedHours(self) -> Optional[int]:
             return self.__missedHours
    def setMissedMins(self, missedMins: Optional[int]):
            self.__missedMins = missedMins
    def getMissedMins(self) -> Optional[int]:
             return self.__missedMins
    def setCounting(self, counting: Optional[bool]):
            self.__counting = counting
    def getCounting(self) -> Optional[bool]:
             return self.__counting
    def setText(self, text: Optional[str]):
            self.__text = text
    def getText(self) -> Optional[str]:
             return self.__text

def getAllAbstenceWeeks(absences: list[OpgAbsence()]) -> list[OpgSchedule]:
    allObjects: list[OpgSchedule] = []

    for absence in absences:
        opgweek = OpgSchedule(absence.getDate())
        x = False
        for obj in allObjects:
            if obj.getWeekDate() == opgweek.getWeekDate():
                opgweek = obj
                x = True
        if not x:
            allObjects.append(opgweek)

        day = opgweek.getScheduleDayByCount(absence.getDate().weekday())
        lesson = day.getOpgLessonById(convertOPGTimeToLessonId((absence.getStartTime())))
        lesson.setLessonName(absence.getSubjectName())
        lesson.setStudentPartOf(False)

    return allObjects

class ExcusePeriod:
    __days:list[OPGWeekDay]
    __start_date:datetime.date
    __end_date:datetime.date

    def __init__(self):
        self.__days: list[OPGWeekDay] = []
        self.__start_date: datetime.date = None
        self.__end_date: datetime.date = None

    def addWeekDay(self, day:OPGWeekDay):
        if not self.__start_date == None and day.getDateTime() < self.__end_date:
            raise IndexError("The given day seems to be before the last entry. Please add the dates in order.")

        if len(self.__days) <= 0:
            #print("Start date: " + str(day.getDateTime()))
            self.__start_date = day.getDateTime()

        self.__end_date = day.getDateTime()
        self.__days.append(day)
        #print("New end Date: " + str(self.__end_date) + " " + str(len(self.__days)))

    def getWeekDays(self) -> list[OPGWeekDay]:
        return self.__days

    def getStartDate(self) -> datetime.date:
        return self.__start_date

    def getEndDate(self) -> datetime.date:
        return self.__end_date

    def getTotalMissingNumber(self) -> int:
        result = 0
        for day in self.__days:
            for lesson in day.getOpgLessons():
                if lesson.wasStudentPartOf():
                    continue
                result += 1
        return result

def parseExcusesFromWeek(weeks:list[OpgSchedule]) -> list[ExcusePeriod]:
    results:list[ExcusePeriod] = []
    for week in weeks:
        excuse = ExcusePeriod()
        for day in week.getSchedules():
            if day.wasMissingOnce():
                excuse.addWeekDay(day)
                continue
        if len(excuse.getWeekDays()) != 0:
            results.append(excuse)
            excuse = ExcusePeriod()
    return results