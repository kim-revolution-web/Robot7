from abc import ABC,abstractmethod

class vehicle(ABC):
    @abstractmethod
    def run(self):
        pass


class Taxi(vehicle):
    def run(self):
        print("택시")
    def __str__(self):
        return '자식클래스 Taxi'

class Truck(vehicle):
    def run(self):
        print("트럭")
    def __str__(self):
        return '자식클래스 Truck'

class Bus(vehicle):
    def run(self):
        print("버스")
    def __str__(self):
        return '자식클래스 Bus'


if __name__ == "__main__":
    just:list [vehicle] =[Taxi(),Truck(),Bus()]
    for s in just:
        s.run()
    
    print(Taxi())