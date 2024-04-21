# you can write to stdout for debugging purposes, e.g.
# puts "this is a debug message"

def solution_1(s):
    uppercase = [False] * 26
    lowercase = [False] * 26
    
    arr = list(s)
    for letter in arr:
        if (letter.islower()):
            lowercase[ord(letter) - ord('a')] = True
        if (letter.isupper()):
            uppercase[ord(letter) - ord('A')] = True

    for i in range(25,-1,-1):
        if (uppercase[i] and lowercase[i]):
            return chr(i + ord('A')) + ""

    return "NO"

print(solution_1('WeTestCodErs'))

class Pump:
    def __init__(self, fuel_capacity):
        self.fuel_capacity = fuel_capacity
        self.car = None


class GasStation:
    def __init__(self, pumps):
        self.pumps = pumps

    def pumps_have_capacity(self, fuel_required):
        return any(pump for pump in self.pumps if pump.fuel_capacity >= fuel_required)

    def free_pump(self, fuel_required):
        for pump in self.pumps:
            if pump.fuel_capacity >= fuel_required and not pump.car:
                return pump

        return None

    def resolve_fuel_up(self):
        min_fuel_need = min(pump.car.fuel_need for pump in self.pumps if pump.car)

        cars_all_fueled_up = []

        for pump in self.pumps:
            if pump.car:
                pump.car.fuel_need -= min_fuel_need
                pump.fuel_capacity -= min_fuel_need

                if pump.car.fuel_need <= 0:
                    cars_all_fueled_up.append(pump.car)
                    pump.car = None

        return cars_all_fueled_up, min_fuel_need

    def are_cars_fueling_up(self):
        for pump in self.pumps:
            if pump.car:
                return True

        return False


class Car:
    def __init__(self, fuel_need):
        self.fuel_need = fuel_need
        self.wait_time = 0


def solution(A, X, Y, Z):
    gas_station = GasStation([Pump(fuel_capacity=X), Pump(fuel_capacity=Y), Pump(fuel_capacity=Z)])
    line = [Car(fuel_need=fuel_need) for fuel_need in A]
    ready_cars = []

    while len(line) > 0 or gas_station.are_cars_fueling_up():
        if len(line) > 0:
            if not gas_station.pumps_have_capacity(fuel_required=line[0].fuel_need):
                return -1

            free_pump = gas_station.free_pump(fuel_required=line[0].fuel_need)

        if free_pump and len(line) > 0:
            free_pump.car = line.pop(0)
            continue

        else:
            resolved_cars, fuel_used = gas_station.resolve_fuel_up()
            for car in line:
                car.wait_time += fuel_used
            ready_cars.extend(resolved_cars)

    return max(car.wait_time for car in ready_cars)