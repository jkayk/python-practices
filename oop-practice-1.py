class Dog:

    def __init__(self, name, age, breed):
        self.name = name
        self.age = age
        self.breed = breed  
    
    def sleep(self):
        print("zzzz...")

class GuardDog(Dog):

    def __init__(self, name, breed):
        super().__init__(name, breed, 5)
        self.aggressive = True 

    def rrrr(self):
        print("Stay away!")

class Puppy(Dog):

    def __init__(self, name, breed):
        super().__init__(name, breed, 0.1)
        self.spoiled = True

    def woof(self):
        print("Woof Woof!")


ruffus = Puppy(
    name="Ruffus",
    breed="Beagle"
)

bibi = GuardDog(
    name="Bibi",
    breed="Dalmatian"
)

ruffus.sleep()
print(bibi.name)