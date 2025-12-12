from abc import ABC,abstractmethod

class knight(ABC):
    @abstractmethod
    def __init__(self,id,name):
        self._id=id
        self._name=name
        
    def attack(self):
        pass

    def __str__(self):
        return f"id={self._id}, name={self._name}"

class dark_knight(knight):
    def __init__(self,id="kkk",name="어두운"):
        super().__init__(id,name)

    def attack(self):
        print("어둠")
    
print(dark_knight())
dk=dark_knight()
dk.attack()
print(dk) # id="kkk",name="어두운"): 이거 출력하고 싶어