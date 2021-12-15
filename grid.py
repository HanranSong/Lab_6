"""
You will implement a simple program that uses a two-dimensional nested list to represent a rectangular grid of cells on
a map. Each cell contains a value that represents the housing price for a typical house in that cell. The data is
contained in a file that you read at the start. However, the data is incomplete - there are some missing values,
represented by zeros in this grid. A realtor estimates such a missing price by taking the average of the prices in the
neighboring cells. The realtor is also interested in the average and the maximum price of housing in the whole
neighborhood (the whole grid).
"""


def create_grid(filename):
    # Create a nested list based on the data given in a file.

    grid_file = open(filename, 'r')
    data = grid_file.read()
    lines = data.splitlines()
    row = int(lines[0])
    column = int(lines[1])
    # Create grid https://www.geeksforgeeks.org/python-using-2d-arrays-lists-the-right-way/
    grid = [[0 for i in range(column)] for j in range(row)]

    # Assign value to the grid one by one.
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            grid[i][j] = int(lines[i * column + j + 2].strip())  # Get rid of the redundant space around each price.
    return grid


def display_grid(grid):
    # Display the grid by printing it to the terminal as seen in the sample run. This function should round the values
    # to integers using round().

    for i in grid:
        for j in i:
            print('|', round(float(j)), end=' ')
        print('|')


def find_neighbors(row_index, col_index, grid):
    # Find the values of all the neighbors of a particular cell in the grid.

    n_list = list()  # This list store the neighbor elements of the target position.

    # Only need to go through the surround eight elements of the target position.
    for i in range(row_index - 1, row_index + 2):
        for j in range(col_index - 1, col_index + 2):
            # There are three situations that shouldn't be considered as neighbour. The first one is it go through the
            # target position. The second one is after minus one to the target position, it turn into -1, in Python it
            # will be considered as the last element of the list. The third one is after plus one, it excess the list
            # length and it will cause error. By using try except, we can manually raise IndexError for the first two
            # situations. Then ignore IndexError, letting the program continue. The unwanted targets won't be added to
            # the neighbour list.
            try:
                if (i == row_index and j == col_index) or i < 0 or j < 0:
                    raise IndexError
                n_list.append(grid[i][j])
            except IndexError:
                continue
    return n_list


def fill_gaps(grid):
    # Create a new two-dimensional list that is identical to the original, but with all zero-cells replaced with the
    # average of their neighbors. You should be calling find_neighbors(row_index, col_index, grid) on each zero-cell in
    # order to help you calculate the average of all neighbors.

    new_list = [[0 for i in range(len(grid[0]))] for j in range(len(grid))]  # Create a new empty list.

    # Copy values from grid to the new list.
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            new_list[i][j] = grid[i][j]

    # If one element in new list is 0, find the neighbour elements, calculate the average value, and replace 0.
    for i in range(len(new_list)):
        for j in range(len(new_list[0])):
            if new_list[i][j] == 0:
                surround = find_neighbors(i, j, grid)
                for k in range(1, len(surround)):
                    surround[0] += surround[k]
                new_list[i][j] = surround[0] / len(surround)
    return new_list


def find_max(grid):
    # Find and return the maximum house value in all cells in the grid using nested loops.

    max_num = grid[0][0]  # Set the top left as the maximum value.

    # If other elements bigger than current maximum, replace it.
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] > max_num:
                max_num = grid[i][j]
    return max_num


def find_average(grid):
    # Find and return the average house value in all cells in the grid using nested loops.

    total = 0

    # Add all elements together.
    for i in grid:
        for j in i:
            total += j
    return total / (len(grid) * len(grid[0]))


def main():
    grid = create_grid('data_1.txt')
    print('This is our grid:')
    display_grid(grid)
    new_grid = fill_gaps(grid)

    print('\nThis is our newly calculated grid:')
    display_grid(new_grid)

    print('\nSTATS')
    print('Average housing price in this area is:', round(find_average(new_grid)))
    print('Maximum housing price in this area is:', round(find_max(new_grid)))


main()
