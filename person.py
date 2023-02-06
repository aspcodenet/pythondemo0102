class Person:
    def __init__(self,name,personNumber):
        self.Name = name
        self.PersonNumber = personNumber

class PersonRegister:        
    def __init__(self):
        self.persons = dict()

    def getPerson(self,personNummer):
        if not personNummer in self.persons:
            return "Finns inte"
        else:
            return self.persons[personNummer]

    def add(self,person):
        if person.PersonNumber in self.persons:
            return "Duplicate key"
        self.persons[person.PersonNumber] = person

