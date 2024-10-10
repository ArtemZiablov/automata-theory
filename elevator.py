class Elevator:

    def __init__(self, floors_amount):
        self.current_floor = 1
        self.destination_floor = 1
        self.S = [i + 1 for i in range(floors_amount)]
        self.num_floors = floors_amount
        self.timer = 2

    def out(self, k):  # функції виходів, яка відображає пари стан, вхідний символ, у вихідні символи.
        states = list()
        self.destination_floor = k
        if self.destination_floor not in self.S:
            states.append("ERROR")
            return states
        elif self.destination_floor == self.current_floor:
            states.append(f'The elevator is on the {self.current_floor}-th floor with the door open')
            return states
        else:
            states.append(f'The elevator is on the {self.current_floor}-th floor with the door open')
            states.append(f'Wait {self.timer} seconds to close the doors')
            states.append(f'The elevator is on the {self.current_floor}-th floor with closed doors')
            if self.current_floor < self.destination_floor <= self.num_floors:
                states.append(
                    f'Moving up from the {self.current_floor}-th floor to the {self.destination_floor}-th floor')
            elif self.current_floor > self.destination_floor <= self.num_floors:
                states.append(
                    f'Moving down from the {self.current_floor}-th floor to the {self.destination_floor}-th floor')
            self.current_floor = self.destination_floor
            states.append(f'The elevator is on the {self.current_floor}-th floor with closed doors')
            states.append(f'The elevator is on the {self.current_floor}-th floor with the door open')
            states.append(f'Wait {self.timer} seconds to close the doors')
            states.append(f'The elevator is on the {self.current_floor}-th floor with closed doors')
            return states

    def do(self, k):  # функції переходів що відображує пару стан, вхідний символ, на інший стан в який здійснюється перехід за цим символом.
        self.destination_floor = k
        if self.destination_floor not in self.S:
            return "ERROR"
        else:
            self.current_floor = k
            return self.current_floor

    def panel(self):  # метод для реалізації керування ліфтом
        n = int(input("Press 1 to run the program, 0 to end: "))
        while True:
            if n == 1:
                a = int(input(f"Enter the number of the floor you want to move to from the list {self.S}: "))
                [print(i) for i in el.out(a)]
                el.do(a)
                print(f"\nElevator is on the {el.do(a)} floor\n")
            elif n == 0:
                break
            else:
                print("unknown symbol")
                break
            n = int(input("Press 1 to continue the program, 0 to end: "))
        return


el = Elevator(7)
el.panel()
