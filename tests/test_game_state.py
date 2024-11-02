import unittest
import os
from textwrap import dedent
from app.ferry import Game

HUGE_DATA_FILE = os.path.join(os.path.dirname(__file__), "test_data/huge_test_input")
DATA_FILE = os.path.join(os.path.dirname(__file__), "test_data/test_input")

def read_from_file(file_input) -> Game:
    with open(file_input, "r") as f:
        content = f.read()
        return Game(content=content)


class TestGameState(unittest.TestCase):
    def setUp(self):
        self.test_input = ""


    def test_initial_game_state(self):
        game = Game(content="LLL\n###")
        self.assertEqual(len(game.state), 2)
        self.assertFalse(game.state[0][0].occupied)
        self.assertFalse(game.state[0][1].occupied)
        self.assertFalse(game.state[0][2].occupied)
        self.assertTrue(game.state[1][0].occupied)
        self.assertTrue(game.state[1][1].occupied)
        self.assertTrue(game.state[1][2].occupied)

    def test_seat_is_occupiable(self):
        game = Game(content="L#")
        self.assertEqual(len(game.state), 1)
        self.assertTrue(game.state[0][0].isOccupiable())
        self.assertTrue(game.state[0][1].isOccupiable())


    def test_ground_is_not_occupiable(self):
        game = Game(content=".")
        self.assertEqual(len(game.state), 1)
        self.assertFalse(game.state[0][0].isOccupiable())


    def test_seat_becomes_occupied_if_no_adjacent_occupied(self):
        game = Game(content="L")
        self.assertEqual(len(game.state), 1)

        self.assertFalse(game.state[0][0].occupied)
        game.cycle()
        self.assertTrue(game.state[0][0].occupied)


    def test_seat_stays_occupied_if_no_adjacent_occupied(self):
        game = Game(content="#")
        self.assertEqual(len(game.state), 1)

        game.cycle()
        self.assertTrue(game.state[0][0].occupied)


    def test_number_of_occupied_seats_is_zero_if_no_adjacent_seats(self):
        game = Game(content="#")
        self.assertEqual(len(game.state), 1)
        self.assertEqual(game.adjacentOccupiedSeats(row = 0, column = 0), 0)


    def test_number_of_occupied_seats_is_correct(self):
        game = Game(content=dedent("""L###L
                                      LLLLL
                                      ###LL"""))
        self.assertEqual(game.adjacentOccupiedSeats(row = 0, column = 2), 2)
        self.assertEqual(game.adjacentOccupiedSeats(row = 1, column = 2), 5)
        self.assertEqual(game.adjacentOccupiedSeats(row = 2, column = 2), 1)


    def test_number_of_occupied_seats_does_not_account_for_ground(self):
        game = Game(content=".L#.")
        self.assertEqual(game.adjacentOccupiedSeats(row = 0, column = 1), 1)


    def test_seat_becomes_unoccupied_if_four_adjacent_seat_occupied(self):
        game = Game(content=dedent("""L###L
                                      LL#LL
                                      ###LL"""))

        game.cycle()
        self.assertFalse(game.state[1][2].occupied)


    def test_ground_stays_ground_after_cycle(self):
        game = Game(content=".")

        self.assertFalse(game.state[0][0].occupied)
        game.cycle()
        self.assertFalse(game.state[0][0].occupied)


    def test_number_of_occupied_seats_accounts_for_occupied_seats(self):
        game = Game(content=dedent("""L###L
                                      LL#LL
                                      ###LL"""))

        self.assertEqual(game.number_occupied_seats(), 7)


    def test_state_becomes_stable_if_nothing_changes(self):
        game = Game(content="L")

        self.assertFalse(game.stable)
        game.cycle()
        self.assertFalse(game.stable)
        game.cycle()
        self.assertTrue(game.stable)


    def test_integration(self):
        game = read_from_file(DATA_FILE)

        while not game.stable:
            game.cycle()

        self.assertEqual(game.number_occupied_seats(), 37)


    def test_integration_huge(self):
        game = read_from_file(HUGE_DATA_FILE)

        while not game.stable:
            game.cycle()

        self.assertEqual(game.number_occupied_seats(), 2319)