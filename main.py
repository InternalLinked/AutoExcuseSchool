import libs.WebUntis
import libs.OpgSchedule
import libs.DocWriter

template_file = "ressources/Entschuldigung.docx"
output_file = "out/out.docx"


file = open("pwd", "r")
pwd = file.read()
file.close()

file = open("email", "r")
email = file.read()
file.close()

file = open("name", "r")
name = file.read()
file.close()

bot = libs.WebUntis.WebUntis()
user = bot.loginMicrosoft(email, pwd)

allObjects = libs.OpgSchedule.getAllAbstenceWeeks(user.getOpgUnexcused())
results = libs.OpgSchedule.parseExcusesFromWeek(allObjects)

t = 0
for excuse in results:
    t += excuse.getTotalMissingNumber()
    print(str(excuse.getStartDate()) + " --> " + str(excuse.getEndDate()) + " : " + str(len(excuse.getWeekDays())) + " : " + str(excuse.getTotalMissingNumber()))
print("Collected a total of " + str(t) + " excuses.")


memory_documents = []
for excuse in results:
    doc = libs.DocWriter.ExcuseWriter(name, excuse, template_file, output_file).getDocument()
    memory_documents.append(doc)

doc = memory_documents[0]
memory_documents.pop(0)
for d in memory_documents:
    for element in d.element.body:
        doc.element.body.append(element)

doc.save(output_file)