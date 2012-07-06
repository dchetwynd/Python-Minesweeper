import unittest
import math

def split_list(original_list, chunk_size):
    return [original_list[offset:offset+chunk_size] for offset in range(0, len(original_list), chunk_size)]
    
class Minesweeper:
    def __init__(self, input_board_string):
        self.input_board_string = input_board_string
        pass
    
    def is_board_square(self):
        board_side_length = math.sqrt(len(self.input_board_string))
        return int(board_side_length) == board_side_length
    
    def generate_board(self):
        if any(square not in ['-', '*'] for square in self.input_board_string):
            raise ValueError("The Minesweeper board input must only contain '-' and '*' characters")

        if not self.is_board_square():
            raise ValueError("The Minesweeper board must be square")
        
        board_side_length = int(math.sqrt(len(self.input_board_string)))
        input_board = split_list(self.input_board_string, board_side_length)
        output_board = []
        
        for row_index in range(0, board_side_length):
            output_board.append([])
            for column_index in range(0, board_side_length):
                if input_board[row_index][column_index] == "*":
                    output_board[row_index].append("*")
                else:
                    output_board[row_index].append(self.count_mine_neighbours(input_board, row_index, column_index))
        
        return self.format_board(output_board)
    
    def get_neighbour_positions(self, board, row_index, column_index):
        """Gets the position indices on the board for a specified board square"""
        neighbour_positions = []
        
        for i in range(-1,2):
            neighbour_row_index = row_index + i
            if (neighbour_row_index >= 0 and neighbour_row_index < len(board)):
                for j in range(-1,2):
                    neighbour_column_index = column_index + j
                    if neighbour_column_index >= 0 and neighbour_column_index < len(board[0]) and (neighbour_row_index != row_index or neighbour_column_index != column_index):
                        neighbour_positions.append((neighbour_row_index, neighbour_column_index))
         
        return neighbour_positions            
    
    def count_mine_neighbours(self, board, row_index, column_index):
        """Counts the number of mine neighbours that a specified cell has"""
        neighbours = self.get_neighbour_positions(board, row_index, column_index)
        mine_count = 0
        
        for neighbour in neighbours:
            if board[neighbour[0]][neighbour[1]] == "*":
                mine_count += 1
         
        return str(mine_count)
    
    def format_board(self, board):
        """Formats a parsed minesweeper board for screen display."""
        formatted_output_board = ""
        for row in board:
            formatted_output_board += ''.join(row) + "\n"
        
        return formatted_output_board
    
class MinesweeperTests(unittest.TestCase):
    
    def testInputWithInvalidCharactersThrowsException(self):
        input_board = "----3---f---H---"
        minesweeper = Minesweeper(input_board)
        self.assertRaises(ValueError, minesweeper.generate_board)
        
    def testNonSquareGridThrowsException(self):
        input_board = "------------------"
        minesweeper = Minesweeper(input_board)
        self.assertRaises(ValueError, minesweeper.generate_board)
    
    def testSquareGridDoesNotThrowException(self):
        input_board = "----------------"
        minesweeper = Minesweeper(input_board)
        minesweeper.generate_board()
    
    def testBoardWithNoMinesReturnsBoardWithAllZeros(self):
        input_board = "----------------"
        minesweeper = Minesweeper(input_board)
        output_board = minesweeper.generate_board()
        
        self.assertEqual("0000\n0000\n0000\n0000\n", output_board)
    
    def testBoardWithAllMinesReturnsBoardWithAllAsterisks(self):
        input_board = "****************"
        minesweeper = Minesweeper(input_board)
        output_board = minesweeper.generate_board()
        
        self.assertEqual("****\n****\n****\n****\n", output_board)        
    
    def testBoardWithSingleMineInCornerReturnsCorrectOutputBoard(self):
        input_board = "*---------------"
        minesweeper = Minesweeper(input_board)
        output_board = minesweeper.generate_board()
        
        self.assertEqual("*100\n1100\n0000\n0000\n", output_board)
    
    def testBoardWithTwoAdjacentMinesReturnsCorrectOutputBoard(self):
        input_board = "**--------------"
        minesweeper = Minesweeper(input_board)
        output_board = minesweeper.generate_board()
        
        self.assertEqual("**10\n2210\n0000\n0000\n", output_board)
    
    def testBoardWithTwoNonAdjacentMinesReturnsCorrectOutputBoard(self):
        input_board = "*-*-------------"
        minesweeper = Minesweeper(input_board)
        output_board = minesweeper.generate_board()
        
        self.assertEqual("*2*1\n1211\n0000\n0000\n", output_board)
        
    def testBoardWithLotsOfMinesReturnsCorrectOutputBoard(self):
        input_board = "***-*-*-***-----"
        minesweeper = Minesweeper(input_board)
        output_board = minesweeper.generate_board()
        
        self.assertEqual("***2\n*8*3\n***2\n2321\n", output_board)
    
if __name__ == '__main__':
    unittest.main()
