class Seating():
    def __init__(self, content: str):
        self.state = dict()
        self.stable = False
        row = 0
        column = 0
        for character in content:
            match (character):
                case 'L':
                    self.state[(row, column)] = False
                    column += 1
                case '#':
                    self.state[(row, column)] = True
                    column += 1
                case '.':
                    column += 1
                case '\n':
                    column = 0
                    row += 1
                case _:
                    pass


    def cycle(self):
        next_state = dict()
        self.stable = True
        for position, is_occupied in self.state.items():
            if is_occupied and self.number_of_adjacent_occupied_seats(position[0], position[1]) >= 4:
                next_state[(position[0], position[1])] = False
                self.stable = False
            elif not is_occupied and self.number_of_adjacent_occupied_seats(position[0], position[1]) == 0:
                next_state[(position[0], position[1])] = True
                self.stable = False
            else:
                next_state[(position[0], position[1])] = is_occupied

        self.state = next_state


    def number_of_adjacent_occupied_seats(self, row: int, column: int) -> int:
        adjacency = [(-1, -1), (-1, 0), (-1, 1),
                    (0, -1), (0, 1),
                    (1, -1), (1, 0), (1, 1)]
        return sum([self.state.get((adj_row + row, adj_col + column), False) for adj_row, adj_col in adjacency])
                
    
    def total_occupied_seats(self):
        return sum([seat for seat in self.state.values()])