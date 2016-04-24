import unittest

import bender
# bender.DEBUG = False


class BenderTestCase(unittest.TestCase):
    @staticmethod
    def transform_input(city_map, correct):
        city_map = [list(row.strip()) for row in city_map.strip().split('\n')]
        correct = [i.strip() for i in correct.strip().split('\n')]

        return city_map, correct

    def bender_run(self, city_map, correct):
        city_map, correct = self.transform_input(city_map, correct)

        b = bender.Bender(city_map)

        count = len(correct) + 5
        # Ходим, пока не встретим символ '$'
        while True:
            count -= 1
            if count <= 0:
                break

            cell = b.step()
            bender.log('cell: "{}"'.format(cell))
            if cell == '$':
                break

        bender.log(b.steps, correct, sep='\n')
        self.assertEqual(b.steps, correct)

    def test_Simple_moves(self):
        city_map = """
#####
#@  #
#   #
#  $#
#####
        """

        correct = """
SOUTH
SOUTH
EAST
EAST
        """

        self.bender_run(city_map, correct)

    def test_Obstacles(self):
        city_map = """
########
# @    #
#     X#
# XXX  #
#   XX #
#   XX #
#     $#
########
        """

        correct = """
SOUTH
EAST
EAST
EAST
SOUTH
EAST
SOUTH
SOUTH
SOUTH
        """

        self.bender_run(city_map, correct)

    def test_Priorities(self):
        city_map = """
########
#     $#
#      #
#      #
#  @   #
#      #
#      #
########
        """

        correct = """
SOUTH
SOUTH
EAST
EAST
EAST
NORTH
NORTH
NORTH
NORTH
NORTH
        """

        self.bender_run(city_map, correct)

    def test_Straight_line(self):
        city_map = """
########
#      #
# @    #
# XX   #
#  XX  #
#   XX #
#     $#
########
        """

        correct = """
EAST
EAST
EAST
EAST
SOUTH
SOUTH
SOUTH
SOUTH
        """

        self.bender_run(city_map, correct)

    def test_Path_modifier(self):
        city_map = """
##########
#        #
#  S   W #
#        #
#  $     #
#        #
#@       #
#        #
#E     N #
##########
        """

        correct = """
SOUTH
SOUTH
EAST
EAST
EAST
EAST
EAST
EAST
NORTH
NORTH
NORTH
NORTH
NORTH
NORTH
WEST
WEST
WEST
WEST
SOUTH
SOUTH
        """

        self.bender_run(city_map, correct)

    def test_Breaker_mode(self):
        city_map = """
##########
# @      #
# B      #
#XXX     #
# B      #
#    BXX$#
#XXXXXXXX#
#        #
#        #
##########
        """

        correct = """
SOUTH
SOUTH
SOUTH
SOUTH
EAST
EAST
EAST
EAST
EAST
EAST
        """

        self.bender_run(city_map, correct)

    def test_Inverter(self):
        city_map = """
##########
#    I   #
#        #
#       $#
#       @#
#        #
#       I#
#        #
#        #
##########
        """

        correct = """
SOUTH
SOUTH
SOUTH
SOUTH
WEST
WEST
WEST
WEST
WEST
WEST
WEST
NORTH
NORTH
NORTH
NORTH
NORTH
NORTH
NORTH
EAST
EAST
EAST
EAST
EAST
EAST
EAST
SOUTH
SOUTH
        """

        self.bender_run(city_map, correct)

if __name__ == '__main__':
    unittest.main()
