from copy import deepcopy
from itertools import chain


class Position():
    def __init__(self, occupied: bool = False, can_be_occupied: bool = True):
        self.occupied = occupied
        self.can_be_occupied = can_be_occupied


class Seating():
    def __init__(self, content: str):
        self.state = [[]]
        self.stable = False
        row = 0
        for character in content:
            match (character):
                case 'L':
                    self.state[row].append(Position())
                case '.':
                    self.state[row].append(Position(occupied = False, can_be_occupied=False))
                    pass
                case '#':
                    self.state[row].append(Position(occupied = True))
                    pass
                case '\n':
                    self.state.append([])
                    row += 1
                    pass
                case _:
                    pass


    def cycle(self):
        new_state = deepcopy(self.state)
        self.stable = True
        for row in range(len(self.state)):
            for column in range(len(self.state[row])):
                seat = new_state[row][column]
                if seat.occupied and seat.can_be_occupied and self.adjacent_occupied_seats(row, column) >= 4:
                    seat.occupied = False
                    self.stable = False
                if not seat.occupied and seat.can_be_occupied and self.adjacent_occupied_seats(row, column) == 0:
                    seat.occupied = True
                    self.stable = False

        self.state = new_state


    def adjacent_occupied_seats(self, row: int, column: int) -> int:
        def getPosition(row: int, column: int):
            if row >= 0 and row < len(self.state) and column >= 0 and column < len(self.state[row]):
                return self.state[row][column]

            return Position()

        adjacent_positions = [(-1, -1), (-1, 0), (-1, 1),
                            (0, -1), (0, 1),
                            (1, -1), (1, 0), (1, 1)
                              ]

        adjacent_occupied = 0
        for adjacent_row, adjacent_column in adjacent_positions:
            adjacent_occupied += 1 if getPosition(adjacent_row + row, adjacent_column + column).occupied else 0

        return adjacent_occupied
                
    
    def number_occupied_seats(self):
        return sum([seat.occupied for seat in chain(*self.state)])