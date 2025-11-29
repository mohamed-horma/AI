# -*- coding: utf-8; mode: python -*-

# ENSICAEN
# École Nationale Supérieure d'Ingénieurs de Caen
# 6 Boulevard Maréchal Juin
# F-14050 Caen Cedex France
#
# Artificial Intelligence 2I1AE1

# @file grid.py
#
# @author Régis Clouard

import math
import time
import copy

class Grid:
    """
    This class stores the grid and the box size of
    a Takuzu puzzle.
    """
    computation_time = 0
    count = 0

    def __init__( self, filename, solver, function = None ):
        """
        Builds a grid from the specified file.
        """
        with open(filename, 'r') as f:
            # get the size of the crossword
            (w, h)  = f.readline().split("x")
            self.__width = int(w)
            self.__height = int(h)
            self.__grid = [[' ' for x in range(self.__width)] for y in range(self.__height)]

            for y in range(self.__height):
                cells = f.readline().split(",")
                for x in range(self.__width):
                    if cells[x][0] in['0', '1']:
                        self.__grid[int(y)][int(x)] = int(cells[x])
        # initialize the state table, representing an empty square with an empty string
        self.__solver = solver
        self.__heuristic_function = function

    def width( self ):
        """
        Returns the grid width.
        """
        return self.__width

    def height( self ):
        """
        Returns the grid height.
        """
        return self.__height

    def get_domain_values( self ):
        """
        Builds the list of all possible values for each white cell.
        Returns  a dictionary containing the domains of variables;
        the key is a tuple (x, y) and the value is the set of {0, 1} values.
        """
        domains = dict()
        w = self.__width
        h = self.__height
        for y in range(h):
            for x in range(w):
                if self.__grid[y][x] == ' ':
                    domains[(x, y)] = {0, 1}
                else:
                    domains[(x, y)] = {self.__grid[y][x]}
        return domains

    def solve( self ):
        """
        Calls the selected solver.

        Returns True or false.
        """
        starttime = time.time()
        if self.__heuristic_function:
            result = self.__solver.solve(self, self.__heuristic_function)
        else:
            result = self.__solver.solve(self)
        self.computation_time = time.time() - starttime
        self.count = self.__solver.count
        return result

    def get_related_variables( self, variable ):
        """
        Returns the list of cells coordinates that are in the same
        row and column than the specified cell x,y (but without the cell (x,y)).
        """
        x, y = variable
        cells = []
        for i in range(self.__width):
            if i != x:
                cells += [(i, y)]
        for j in range(self.__height):
            if j != y:
                cells += [(x, j)]
        return cells

    def is_goal_state( self, assignment ):
        
        def identicalRows(y1, y2):
            for x in range(self.width()):
                a = assignment[(x, y1)]
                b = assignment[(x, y2)]
                if a != b:
                    return False
            return True
        
        def identicalColumns(x1, x2):
            for y in range(self.height()):
                a = assignment[(x1, y)]
                b = assignment[(x2, y)]
                if a != b:
                    return False
            return True
            
        """
        Checks whether the specified assignment is a regular solution.
        """
        # 1. Number of 0 = number in 1 in rows
        for y in range(self.height()):
            if (self.count_in_row(0, y, assignment) != self.width() / 2
                or self.count_in_row(1, y, assignment) != self.width() / 2):
                return (False, "No equal number of 1 and 0 in row: " + str(y))
        # 2. Number of 0 = number in 1 in columns
        for x in range(self.width()):
            if (self.count_in_column(0, y, assignment) != self.height() / 2
                or self.count_in_column(1, y, assignment) != self.height() / 2):
                return (False, "No equal number of 1 and 0 in column: " + str(x))
        # 3. Number of series of value in the row and column <= 2
        for y in range(self.height()):
            for x in range(self.width()):
                if (x, y) in assignment:
                    value = assignment[(x, y)]
                else:
                    value = self.__grid[y][x]
                if self.series_length_row(x, y, value, assignment) > 2:
                    return (False, "More than two of either number adjacent to each other in row: " + str(y))
                if self.series_length_column(x, y, value, assignment) > 2:
                    return (False, "More than two of either number adjacent to each other in column: " + str(x))
        # # 4. No identical rows
        # for y1 in range(self.height()):
        #     for y2 in range(self.height()):
        #         if y1 == y2:
        #             continue
        #         if identicalRows(y1, y2):
        #             return (False, "Identical rows: %d and %d." % y1, y2)
        # # 5. No identical columns
        # for x1 in range(self.width()):
        #     for x2 in range(self.width()):
        #         if x1 != x2 and identicalColumns(x1, x2):
        #             return (False, "Identical columns: " + str(x1) + "and " + str(x2))
        return (True, None)

    def identical_rows( self, assignment ):
        """
        Checks identical rows
        """
        def identicalRows(y1, y2):
            for x in range(self.width()):
                if (x, y1) in assignment:
                    a = assignment[(x, y1)]
                else:
                    return False
                if (x, y2) in assignment:
                    b = assignment[(x, y2)]
                else:
                    return False
                if a != b:
                    return False
            return True
        
        for y1 in range(self.height()):
            for y2 in range(self.height()):
                if y1 == y2:
                    continue
                if identicalRows(y1, y2):
                    return True
        return False

    def identical_columns( self, assignment ):
        """
        Checks identical columns.
        """
        def identicalColumns(x1, x2):
            for y in range(self.height()):
                if (x1, y) in assignment:
                    a = assignment[(x1, y)]
                else:
                    return False
                if (x2, y) in assignment:
                    b = assignment[(x2, y)]
                else:
                    return False
                if a != b:
                    return False
            return True

        for x1 in range(self.width()):
            for x2 in range(self.width()):
                if x1 != x2 and identicalColumns(x1, x2):
                    return True
        return False

    def count_in_row( self, value, row, assignment ):
        """"
        Returns the number of the specified value in the 
        specified row considering the current assignment.
        """
        number = 0
        for x in range(self.width()):
            if (x, row) in assignment and assignment[(x, row)] == value:
                number += 1
        return number

    def count_in_column( self, value, column, assignment ):
        """"
        Returns the number of the specified value in the 
        specified column considering the current assignment.
        """
        number = 0
        for y in range(self.height()):
            if (column, y) in assignment and assignment[(column, y)] == value:
                number += 1
        return number

    def series_length_row( self, x, y, value, assignment ):
        number = 1
        if x - 1 >= 0 and (self.__grid[y][x - 1] == value
                           or ((x - 1, y) in assignment and assignment[(x - 1, y)] == value)):
            number += 1
            if x - 2 >= 0 and (self.__grid[y][x - 2] == value
                           or ((x - 2, y) in assignment and assignment[(x - 2, y)] == value)):
                number += 1
        if x + 1 < self.width() and (self.__grid[y][x + 1] == value
                                     or ((x + 1, y) in assignment and assignment[(x + 1, y)] == value)):
            number += 1
            if x + 2 < self.width() and (self.__grid[y][x + 2] == value
                                         or ((x + 2, y) in assignment and assignment[(x + 2, y)] == value)):
                number += 1
        return number

    def series_length_column( self, x, y, value, assignment ):
        number = 1
        if y - 1 >= 0 and (self.__grid[y - 1][x] == value
                           or ((x, y - 1) in assignment and assignment[(x, y - 1)] == value)):
            number += 1
            if y - 2 >= 0 and (self.__grid[y - 2][x] == value
                               or ((x, y - 2) in assignment and assignment[(x, y - 2)] == value)):
                number += 1
        if y + 1 < self.height() and (self.__grid[y + 1][x] == value
                                      or ((x, y + 1) in assignment and assignment[(x, y + 1)] == value)):
            number += 1
            if y + 2 < self.height() and (self.__grid[y + 2][x] == value
                                          or ((x, y + 2) in assignment and assignment[(x, y + 2)] == value)):
                number += 1
        return number

    def __remove_series( self, x, y, dx, dy, assignment, domains ):
        cells = []
        value = assignment[(x, y)]

        # Case ? 0 0 ?
        if (x + dx >= 0 and y + dy >= 0
            and x + dx < self.width() and y + dy < self.height()
            and (x + dx, y + dy) in assignment and assignment[(x + dx, y + dy)] == value):
            if (x + 2 * dx >= 0  and y + 2 * dy >= 0
                and x + 2 * dx < self.width() and y + 2 * dy < self.height()
                and (x + 2 * dx, y + 2 * dy) in domains):
                cells += [(x + 2 * dx, y + 2 * dy)]
            if (x - dx >= 0 and y - dy >= 0
                and x - dx < self.width() and y - dy < self.height()
                and (x - dx, y - dy) in domains):
                cells += [(x - dx, y - dy)]
        # Case 0 ? 0
        if (x + 2 * dx >= 0 and y + 2 * dy >= 0
            and x + 2 * dx < self.width() and y + 2 * dy < self.height()
            and (x + 2 * dx, y + 2 * dy) in assignment and assignment[(x + 2 * dx, y + 2 * dy)] == value):

            if (x + dx >= 0  and y + dy >= 0
                and x + dx < self.width() and y + dy < self.height()
                and (x + dx, y + dy) in domains):
                cells += [(x + dx, y + dy)]

        return cells

    def get_conflicting_variables( self, variable, assignment, domains ):
        """ 
        Returns the list of cells that are in conflict with the variable.
        """
        x, y = variable
        cells  = self.__remove_series(x, y,  1,  0, assignment, domains)
        cells += self.__remove_series(x, y,  0,  1, assignment, domains)
        cells += self.__remove_series(x, y, -1,  0, assignment, domains)
        cells += self.__remove_series(x, y,  0, -1, assignment, domains)
        value = assignment[(x, y)]
        nValueInRow = self.count_in_row(value, y, assignment)
        if nValueInRow == self.width() / 2:
            for i in range(self.width()):
                cell = (i, y)
                if cell in domains and cell not in cells:
                    cells += [cell]
        nValueInColumn = self.count_in_column(value, x, assignment)
        if nValueInColumn == self.height() / 2:
            for j in range(self.height()):
                cell = (x, j)
                if cell in domains and cell not in cells:
                    cells += [cell]
        return cells

    def is_in_conflict( self, Xi, Xj, value, domains, assignment ):
        """ Checks whether Xj is inconsistent with Xi when Xi takes the specified value. """

        def affected_value(x, y):
            if (x, y) in domains:
                return domains[(x, y)]
            else:
                return set([assignment[(x, y)]])

        if ((Xj not in domains or domains[Xj] != set([value])) and (Xj not in assignment or assignment[Xj] != value)):
            return False

        # Case 1: Xi, value, Xj or Xj, value, Xi: conflict
        if ((   Xj[0] - Xi[0] ==  2 and affected_value(Xi[0] + 1, Xi[1]) == set([value]))
            or (Xj[0] - Xi[0] == -2 and affected_value(Xi[0] - 1, Xi[1]) == set([value]))
            or (Xj[1] - Xi[1] ==  2 and affected_value(Xi[0], Xi[1] + 1) == set([value]))
            or (Xj[1] - Xi[1] == -2 and affected_value(Xi[0], Xi[1] - 1) == set([value]))):
            return True

        # Case 2: value, Xi, Xj or value, Xj, Xi: conflict
        if ((   Xj[0] - Xi[0] ==  1 and Xi[0] - 1 >= 0 and affected_value(Xi[0] - 1, Xi[1]) == set([value]))
            or (Xj[0] - Xi[0] == -1 and Xj[0] - 1 >= 0 and affected_value(Xj[0] - 1, Xi[1]) == set([value]))
            or (Xj[1] - Xi[1] ==  1 and Xi[1] - 1 >= 0 and affected_value(Xi[0], Xi[1] - 1) == set([value]))
            or (Xj[1] - Xi[1] == -1 and Xj[1] - 1 >= 0 and affected_value(Xi[0], Xj[1] - 1) == set([value]))):
            return True
        
        # Case 3: Xj, Xi, value or Xi, Xj, value: conflict
        if ((   Xj[0] - Xi[0] ==  1 and Xj[0] + 1 < self.width()  and affected_value(Xj[0] + 1, Xi[1]) == set([value]))
            or (Xj[0] - Xi[0] == -1 and Xi[0] + 1 < self.width()  and affected_value(Xi[0] + 1, Xi[1]) == set([value]))
            or (Xj[1] - Xi[1] ==  1 and Xj[1] + 1 < self.height() and affected_value(Xi[0], Xj[1] + 1) == set([value]))
            or (Xj[1] - Xi[1] == -1 and Xi[1] + 1 < self.height() and affected_value(Xi[0], Xi[1] + 1) == set([value]))):
            return True

        # Case 4: If sum value in the row or column == width / 2 remove v form Xj
        number = 1
        if Xj[1] == Xi[1]:
            for x in range(self.width()):
                if x != Xi[0] and x != Xj[0] and affected_value(x, Xi[1]) == set([value]):
                    number += 1
        else:
            for y in range(self.height()):
                if y != Xi[1] and y != Xj[1] and affected_value(Xi[0], y) == set([value]):
                    number += 1
        if number >= self.width() / 2:
            return True

        return False

    def display( self, assignment = None ):
        """
        Displays the grid with the current assignment
        if specified.
        """
        sep = '+' + ('+'.join(['---'  * 1] * self.__width)) + '+' 
        inset = 4 * ' '

        g = copy.deepcopy(self.__grid)
        if assignment:
            for y in range(self.__height):
                for x in range(self.__width):
                    g[y][x] = ' '
            for (x, y) in assignment:
                g[y][x] = assignment[(x, y)]

        print(inset, sep)
        for y in range(self.__height):
            print(inset, end= " ")
            line = ""
            for x in range(self.__width):
                line += "|"
                if g[y][x] == ' ':
                    line += "   "
                else:
                    line += " " + str(g[y][x]) + " "
            print(line + '|')
            print(inset, sep)
