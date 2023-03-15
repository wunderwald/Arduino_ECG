import re

def testSubjectId(id):
    exp = "^[0-9]{3}"
    match = re.search(exp, str(id))
    return (match != None) and (match.group() == str(id))

def enterSubjectId():
    id = None
    idOk = False
    while not idOk:
        id = input("# Enter subject ID [3 digits]: ")
        idOk = testSubjectId(id)
        if not idOk:
            print("! Invalid ID.")
    return id