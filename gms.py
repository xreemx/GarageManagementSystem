import json
import os
from abc import ABC, abstractmethod


class Car(ABC):
    def __init__(self, car_number, full_name, age, racing_team, speed, capacity):
        self.car_number = car_number
        self.full_name = full_name
        self.age = age
        self.racing_team = racing_team
        self.speed = speed
        self.capacity = capacity

    @property
    def car_number(self) -> str:
        return self._car_number

    @car_number.setter
    def car_number(self, value):
        number = str(value).strip()
        if not number:
            raise ValueError("Enter the car number")
        self._car_number = number

    @property
    def full_name(self) -> str:
        return self._full_name

    @full_name.setter
    def full_name(self, value):
        name = str(value).strip()
        if not name:
            raise ValueError("Enter the car name")
        self._full_name = name

    @property
    def age(self) -> int:
        return self._age

    @age.setter
    def age(self, value):
        Age = int(value)
        if Age < 0:
            raise ValueError("Age should be a positive integer")
        self._age = Age

    @property
    def racing_team(self) -> str:
        return self._racing_team

    @racing_team.setter
    def racing_team(self, value):
        team = str(value).strip()
        if not team:
            raise ValueError("Enter the team ")
        self._racing_team = team

    @property
    def speed(self) -> float:
        return self._speed

    @speed.setter
    def speed(self, value):
        Speed = float(value)
        if Speed <= 0:
            raise ValueError("Enter a speed value")
        self._speed = Speed

    @property
    def capacity(self) -> float:
        return self._capacity

    @capacity.setter
    def capacity(self, value):
        cap = float(value)
        if cap <= 0:
            raise ValueError("Enter a capacity value")
        self._capacity = cap

    @abstractmethod
    def per_score(self) -> float:
        pass

    @abstractmethod
    def car_details(self) -> dict:
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        pass


class Racer(Car):
    def __init__(
        self,
        car_number,
        full_name,
        age,
        racing_team,
        speed,
        capacity,
        races_completed,
        laps_completed,
    ):
        super().__init__(car_number, full_name, age, racing_team, speed, capacity)
        self.races_completed = races_completed
        self.laps_completed = laps_completed

    @property
    def races_completed(self) -> int:
        return self._races_completed

    @races_completed.setter
    def races_completed(self, value):
        val = int(value)
        if val < 0:
            raise ValueError("Enter a positive value")
        self._races_completed = val

    @property
    def laps_completed(self) -> int:
        return self._laps_completed

    @laps_completed.setter
    def laps_completed(self, value):
        val = int(value)
        if val < 0:
            raise ValueError("Enter a positive value")
        self._laps_completed = val

    def per_score(self) -> float:
        return (self.speed * 10) + (self.capacity * 1)

    def car_details(self) -> dict:
        return {
            "races_completed": self.races_completed,
            "laps_completed": self.laps_completed,
        }

    def to_dict(self) -> dict:
        return {
            "type": "Racer",
            "car_number": self.car_number,
            "full_name": self.full_name,
            "age": self.age,
            "racing_team": self.racing_team,
            "speed": self.speed,
            "capacity": self.capacity,
            "extra_attributes": {
                "races_completed": self.races_completed,
                "laps_completed": self.laps_completed,
            },
        }


class SupportVehicle(Car):
    def __init__(
        self,
        car_number,
        full_name,
        age,
        racing_team,
        speed,
        capacity,
        crew_size,
        reliability_rating,
    ):
        super().__init__(car_number, full_name, age, racing_team, speed, capacity)
        self.crew_size = crew_size
        self.reliability_rating = reliability_rating

    @property
    def crew_size(self) -> int:
        return self._crew_size

    @crew_size.setter
    def crew_size(self, value: int):
        val = int(value)
        if val < 1:
            raise ValueError("Crew size must be at least 1.")
        self._crew_size = val

    @property
    def reliability_rating(self) -> float:
        return self._reliability_rating

    @reliability_rating.setter
    def reliability_rating(self, value: float):
        val = float(value)
        if not (0.0 <= val <= 10.0):
            raise ValueError("Reliability rating must be between 0.0 and 10.0.")
        self._reliability_rating = val

    def per_score(self) -> float:
        return (self.speed * 5) + (self.capacity * 5)

    def car_details(self) -> dict:
        return {
            "crew_size": self.crew_size,
            "reliability_rating": self.reliability_rating,
        }

    def to_dict(self) -> dict:
        return {
            "type": "SupportVehicle",
            "car_number": self.car_number,
            "full_name": self.full_name,
            "age": self.age,
            "racing_team": self.racing_team,
            "speed": self.speed,
            "capacity": self.capacity,
            "extra_attributes": {
                "crew_size": self.crew_size,
                "reliability_rating": self.reliability_rating,
            },
        }


class garageManager:
    def __init__(self, file="radiator_springs_garage.json"):
        self.file = file
        self._cars = {}
        self.loadfromfile()

    def carNumCheck(self, car_number) -> bool:
        return str(car_number).strip() in self._cars

    def check_in_car(self, car: Car) -> bool:
        if self.carNumCheck(car.car_number):
            raise ValueError("Number already exists")
        self._cars[car.car_number] = car
        self.saveToFile()
        return True

    def find_car(self, car_number: str):
        return self._cars.get(str(car_number).strip())

    def viewallcars(self) -> list:
        return list(self._cars.values())

    def carRetire(self, car_number) -> bool:
        num = str(car_number).strip()
        if num in self._cars:
            del self._cars[num]
            self.saveToFile()
            return True
        return False

    def reportCars(self) -> dict:
        cars = self.viewallcars()
        if not cars:
            return {
                "Cars checked in": 0,
                "average score": 0.0,
                "breakdown of each car": {},
            }
        numofcars = len(cars)
        averagePerformance = sum(i.per_score() for i in cars) / numofcars
        teams = {}
        for i in cars:
            teams[i.racing_team] = teams.get(i.racing_team, 0) + 1

        return {
            "Cars checked in": numofcars,
            "average score": averagePerformance,
            "breakdown of each car": teams,
        }

    def saveToFile(self):
        data = [car.to_dict() for car in self._cars.values()]
        with open(self.file, "w") as file:
            json.dump(data, file, indent=4)

    def loadfromfile(self):
        if not os.path.isfile(self.file):
            return

        try:
            with open(self.file, "r") as file:
                data = json.load(file)
            for item in data:
                car = None
                if item.get("type") == "Racer":
                    car = Racer(
                        car_number=item["car_number"],
                        full_name=item["full_name"],
                        age=item["age"],
                        racing_team=item["racing_team"],
                        speed=item["speed"],
                        capacity=item["capacity"],
                        races_completed=item.get("extra_attributes", {}).get("races_completed", 0),
                        laps_completed=item.get("extra_attributes", {}).get("laps_completed", 0),
                    )
                elif item.get("type") == "SupportVehicle":
                    car = SupportVehicle(
                        car_number=item["car_number"],
                        full_name=item["full_name"],
                        age=item["age"],
                        racing_team=item["racing_team"],
                        speed=item["speed"],
                        capacity=item["capacity"],
                        crew_size=item.get("extra_attributes", {}).get("crew_size", 1),
                        reliability_rating=item.get("extra_attributes", {}).get("reliability_rating", 10.0),
                    )
                if car:
                    self._cars[car.car_number] = car
        except Exception as e:
            print(f"Error loading file: {e}")


def main():
    manager = garageManager()

    while True:
        print("\n=== RADIATOR SPRINGS GARAGE MANAGER ===")
        print("1. Check In New Vehicle")
        print("2. Search Vehicle by Number")
        print("3. View All Vehicles")
        print("4. Retire Vehicle")
        print("5. Generate Garage Report")
        print("6. Exit")

        choice = input("Select an Option (1-6): ").strip()

        if choice == "1":
            vehicleType = input("Enter vehicle type (1. Racer, 2. Support Vehicle): ").strip()
            try:
                num = input("Car Number: ").strip()
                name = input("Full Name: ").strip()
                age = input("Age: ").strip()
                team = input("Racing Team: ").strip()
                speed = input("Speed: ").strip()
                cap = input("Capacity: ").strip()

                if vehicleType == "1":
                    races = input("Races Completed: ").strip()
                    laps = input("Laps Completed: ").strip()
                    car = Racer(num, name, age, team, speed, cap, races, laps)
                elif vehicleType == "2":
                    crew = input("Crew Size: ").strip()
                    rel = input("Reliability Rating: ").strip()
                    car = SupportVehicle(num, name, age, team, speed, cap, crew, rel)
                else:
                    print("Invalid vehicle type selected.")
                    continue

                manager.check_in_car(car)
                print(f"Vehicle #{num} checked in successfully!")

            except ValueError as e:
                print(f"Input Error: {e}")

        elif choice == "2":
            num = input("Enter Car Number: ").strip()
            car = manager.find_car(num)
            if car:
                print(f"Found: #{car.car_number} {car.full_name} | Team: {car.racing_team} | Performance: {car.per_score()}")
                print(f"   Details: {car.car_details()}")
            else:
                print("Vehicle not found.")

        elif choice == "3":
            cars = manager.viewallcars()
            if not cars:
                print("No vehicles in garage.")
            else:
                for c in cars:
                    print(f"- #{c.car_number}: {c.full_name} ({c.__class__.__name__}) | Team: {c.racing_team} | Score: {c.per_score()}")

        elif choice == "4":
            print("\n--- Retire Vehicle ---")
            num = input("Enter Car Number to Retire: ").strip()
            if manager.carRetire(num):
                print(f"Vehicle #{num} retired successfully.")
            else:
                print("Vehicle not found.")

        elif choice == "5":
            print("\n--- Garage Performance Report ---")
            report = manager.reportCars()
            print(f"Total Vehicles : {report['Cars checked in']}")
            print(f"Average Score  : {report['average score']:.2f}")
            print("Team Breakdown :")
            for team_name, count in report["breakdown of each car"].items():
                print(f"  - {team_name}: {count} vehicle(s)")

        elif choice == "6":
            print("\nGoodbye! All garage data is safely saved.")
            break

        else:
            print("Invalid menu choice. Please select 1-6.")


if __name__ == "__main__":
    main()