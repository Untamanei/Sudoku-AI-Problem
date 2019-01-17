'''
Exercise4.1: Apply Constraint Propagation to Sudoku problem
Now that you see how we apply Constraint Propagation to this problem, let's try to code it!
In the following quiz, combine the functions eliminate and only_choice to write the function reduce_puzzle,
which receives as input an unsolved puzzle and applies our two constraints repeatedly in an attempt to solve it.

Some things to watch out for:
- The function needs to stop if the puzzle gets solved. How to do this?
- What if the function doesn't solve the sudoku? Can we make sure the function quits when applying
the two strategies stops making progress?
'''

# 1. utils.py ----------------------------
# 1.1 define rows:
rows = 'ABCDEFGHI'

# 1.2 define cols:
cols = '123456789'


# 1.3 cross(a,b) helper function to create boxes, row_units, column_units, square_units, unitlist
def cross(a, b):
    return [s + t for s in a for t in b]


# 1.4 create boxes
boxes = cross(rows, cols)

# 1.5 create row_units
row_units = [cross(r, cols) for r in rows]

# 1.6 create column_units
column_units = [cross(rows, c) for c in cols]

# 1.7 create square_units for 9x9 squares
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]

# 1.8 create unitlist for all units
unitlist = row_units + column_units + square_units

# 1.9 create peers of a unit from all units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)


# 1.10 display function receiving "values" as a dictionary and display a 9x9 suduku board
def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return


def grid_values(grid):
    """Convert grid string into {<box>: <value>} dict with '123456789' value for empties.

    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '123456789' if it is empty.
    """

    ''' Your solution here '''
    chars = []
    for c in grid:
        chars.append(c)

    assert len(chars) == 81
    return dict(zip(boxes, chars))

values = grid_values('..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..')
print("\n")
print("The original Sudoku board is **********************************************")
display(values)

def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """

    ''' Your solution here '''
    for key, value in  values.items():
        if (len(value) == 1):
            for key_peer in peers[key]:
                values[key_peer] = values[key_peer].replace(value, '')
    return values

eliminate(values)
print("\n")
print("After implement eliminate(values) method **********************************")
display(values)

def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """

    ''' Your solution here '''

    new_values = values.copy()

    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                new_values[dplaces[0]] = digit
    return new_values

new_values = only_choice(values)
print("\n")
print("After implement only_choice(values) method **********************************")
display(new_values)

# 2. function.py ----------------------------
# 2.1 combine the functions eliminate and only_choice to write the function reduce_puzzle
# from utils import *
def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """

    ''' Your solution here '''
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

new_values = reduce_puzzle(values)
print("\n")
print("After applying constrint propagaton (both eliminate and only_choice strategies)*****************")
display(new_values)