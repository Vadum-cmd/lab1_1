"""
This module represents skyscrapers game.
"""
def read_input(path: str):
    """
    Read game board file from path.
    Return list of str.
    """
    input_data = []

    with open(path, mode='r', encoding='UTF-8') as check:
        for row in check:
            input_data.append(row.strip("\n"))
    return input_data


def left_to_right_check(input_line: str, pivot: int):
    """
    Check row-wise visibility from left to right.
    Return True if number of building from the left-most hint is visible looking to the right,
    False otherwise.

    input_line - representing board row.
    pivot - number on the left-most hint of the input_line.

    >>> left_to_right_check("412453*", 4)
    True
    >>> left_to_right_check("452453*", 5)
    False
    """
    row = input_line[1:-1]
    max_height = row[0]
    count = 1
    for item in row:
        if item > max_height:
            max_height = item
            count += 1

    if count != int(pivot):
        return False
    else:
        return True


def check_not_finished_board(board: list):
    """
    Check if skyscraper board is not finished, i.e., '?' present on the game board.

    Return True if finished, False otherwise.

    >>> check_not_finished_board(['***21**', '4?????*', '4?????*', '*?????5', '*?????*', '*?????*', '*2*1***'])
    False
    >>> check_not_finished_board(['***21**', '412453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_not_finished_board(['***21**', '412453*', '423145*', '*5?3215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    town_board = board[1:-1]
    for buildings in town_board:
        if '?' in buildings:
            print (buildings)
            return False

    return True


def check_uniqueness_in_rows(board: list):
    """
    Check buildings of unique height in each row.

    Return True if buildings in a row have unique length, False otherwise.

    >>> check_uniqueness_in_rows(['***21**', '412453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_uniqueness_in_rows(['***21**', '452453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    >>> check_uniqueness_in_rows(['***21**', '412453*', '423145*', '*553215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    town_board = board[1:-1]
    length = len(town_board[0]) - 2
    for item in town_board:
        item = item[1:-1]
        if len(set(item)) != length:
            return False

    return True


def check_horizontal_visibility(board: list):
    """
    Check row-wise visibility (left-right and vice versa)

    Return True if all horizontal hints are satisfiable,
     i.e., for line 412453* , hint is 4, and 1245 are the four buildings
      that could be observed from the hint looking to the right.

    >>> check_horizontal_visibility(['***21**', '412453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_horizontal_visibility(['***21**', '452453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    >>> check_horizontal_visibility(['***21**', '452413*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    def reverse_str(str):
        return str[::-1]

    town_board = board[1:-1]
    for item in town_board:
        left_index, right_index = item[0], item[-1]
        if left_index.isnumeric() :
            if not left_to_right_check(item,left_index):
                return False

        if right_index.isnumeric() :
            if not left_to_right_check(reverse_str(item), right_index):
                return False
    return True


def check_columns(board: list):
    """
    Check column-wise compliance of the board for uniqueness (buildings of unique height) and visibility (top-bottom and vice versa).

    Same as for horizontal cases, but aggregated in one function for vertical case, i.e. columns.

    >>> check_columns(['***21**', '412453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_columns(['***21**', '412453*', '423145*', '*543215', '*35214*', '*41232*', '*2*1***'])
    False
    >>> check_columns(['***21**', '412553*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    # Transform columns to rows
    columns = []
    width = len(board[0])
    for col_ind in range(width):
        column = ''
        for row in board:
            column += row[col_ind]
        columns.append(column)

    if not check_uniqueness_in_rows(columns):
        return False

    if not check_horizontal_visibility(columns):
        return False

    return True


def check_skyscrapers(input_path: str):
    """
    Main function to check the status of skyscraper game board.
    Return True if the board status is compliant with the rules,
    False otherwise.

    >>> check_skyscrapers("check.txt")
    True
    """
    board_data = read_input(input_path)
    # Print data from board
    print ("Data from your board : ")
    print (board_data)
    check_result = "Combination on board does not look good : "

    if not check_not_finished_board(board_data):
        check_result = check_result + " There are not finished cells"
        print (check_result)
        return False
    if not check_uniqueness_in_rows(board_data):
        check_result = check_result + " Cells value is not unique"
        print (check_result)
        return False
    if not check_horizontal_visibility(board_data):
        check_result = check_result + " Horizontal visibility does not match with requirements"
        print (check_result)
        return False
    if not check_columns(board_data):
        check_result = check_result + " Columns are not unique"
        print (check_result)
        return False

    print ("Congrats! Your combination is compliant with requirements")
    return True


if __name__ == "__main__":
    print(check_skyscrapers('check.txt'))
    print(check_skyscrapers('check_fail.txt'))
