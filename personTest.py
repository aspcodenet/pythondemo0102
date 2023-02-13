from person import Person, PersonRegister
import unittest

# sut = system under test

class PersonTest(unittest.TestCase):
    def test_When_creating_person_then_name_and_personnumber_should_be_set(self):
        #arrange = RÄTT FÖRUTSÄTTNINGAR
        name = "Stefan"
        pn = "19720803-0000"
        #act // Agera ex klicka på PAY
        sut = Person(name,pn)
        #assert // verifiera
        self.assertEqual(name, sut.Name)
        self.assertEqual(pn, sut.PersonNumber)        

class PersonRegisterTest(unittest.TestCase):
    def test_When_fetching_person_correct_person_should_be_returned(self):    
        #arrange    
        person1 = Person("Stefan", "19720803-0000")
        person2 = Person("Kalle", "19790101-0000")
        sut = PersonRegister()
        sut.add(person1)
        sut.add(person2)
        #act
        result = sut.getPerson("19720803-0000")
        #assert
        self.assertEqual(person1, result)

    def test_When_fetching_person_and_person_does_not_exist_correct_errormessage_should_be_returned(self):    
        #arrange    
        person1 = Person("Stefan", "19720803-0000")
        person2 = Person("Kalle", "19790101-0000")
        sut = PersonRegister()
        sut.add(person1)
        sut.add(person2)
        #act
        result = sut.getPerson("19720803-1111")
        #assert
        self.assertEqual("Finns inte", result)


    def test_When_adding_person_and_person_already_exist_correct_errormessage_should_be_returned(self):    
        #arrange    
        person1 = Person("Stefan", "19720803-0000")
        person2 = Person("Kalle", "19720803-0000")
        sut = PersonRegister()
        sut.add(person1)

        #act
        result = sut.add(person2)

        #assert
        self.assertEqual("Duplicate key", result)




if __name__ == '__main__':
    unittest.main()