import json
import threading
import time


# ThreadManager class to manage multiple threads
class ThreadManager:
    def __init__(self):
        self.threads = []

    # Method to add a thread with a target function, arguments, and a name
    def add_thread(self, target, args=(), name=""):
        thread = threading.Thread(target=target, args=args, name=name)
        self.threads.append(thread)

    # Method to start all threads
    def start_all(self):
        for thread in self.threads:
            thread.start()

    # Method to join all threads
    def join_all(self):
        for thread in self.threads:
            thread.join()


# Function to generate an initial Sudoku board with a starting value
def generate_board(start_value):
    return [
        [start_value, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]


# Function to read the last checkpoint from a JSON file
def read_last_checkpoint(filename):
    try:
        with open(filename, 'r+') as f:
            last_checkpoint = json.load(f)
    except FileNotFoundError:
        last_checkpoint = None
    return last_checkpoint


# Function to write the last checkpoint to a JSON file
def write_last_checkpoint(filename, checkpoint):
    with open(filename, 'w+') as f:
        f.write(json.dumps(checkpoint))


# Function to check if a given Sudoku board is valid
def isValidSudoku(board):
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    blocks = [set() for _ in range(9)]

    for i in range(9):
        for j in range(9):
            num = board[i][j]
            if num != 0:
                block_index = (i // 3) * 3 + (j // 3)
                if num in rows[i] or num in cols[j] or num in blocks[block_index]:
                    return False
                rows[i].add(num)
                cols[j].add(num)
                blocks[block_index].add(num)

    return True


# Constants for board dimensions
BOARD_WIDTH = 9
BOARD_HEIGHT = 9

# Global variables for tracking Sudoku found and last Sudoku state
status_lock = threading.Lock()
SUDOKU_FOUND = 0
LAST_SUDOKU = None


# Recursive function to generate Sudoku fields
def recursive_field_generator(board=None, current_x=0, current_y=0, break_value=None, thread_name=""):
    global SUDOKU_FOUND
    global LAST_SUDOKU

    # Step 1: Check if the break value is reached
    if break_value is not None and board[0][0] > break_value:
        return

    current_value = board[current_x][current_y]
    if current_value <= 0:
        current_value = 1

    # Step 2: Iterate over possible values for the current cell
    for index in range(current_value, 10):  # loop from current_value to 9 inclusive
        board[current_x][current_y] = index

        # Step 3: Check if the current board configuration is valid
        if not isValidSudoku(board):
            board[current_x][current_y] = 0  # reset field if invalid
            continue

        # Step 4: Proceed to the next cell
        if current_y + 1 >= BOARD_HEIGHT:
            if current_x + 1 >= BOARD_WIDTH:
                # Step 5: If at the last cell, update the status
                with status_lock:
                    SUDOKU_FOUND += 1
                    LAST_SUDOKU = json.loads(json.dumps(board))  # deep copy of the board
                    # Write the last board to a file named after the thread
                    write_last_checkpoint(f"{thread_name}_checkpoint.json", LAST_SUDOKU)
                    # TODO: Write the solution into a database
            else:
                # Move to the next row
                recursive_field_generator(board, current_x + 1, 0, break_value, thread_name)
        else:
            # Move to the next column
            recursive_field_generator(board, current_x, current_y + 1, break_value, thread_name)

    # Step 6: Reset the current cell after testing all possibilities
    board[current_x][current_y] = 0


# Function to print the status of Sudoku generation
def print_status():
    global SUDOKU_FOUND
    global LAST_SUDOKU
    while True:
        time.sleep(5)
        with status_lock:
            print("Sudoku's found: ", SUDOKU_FOUND, " ", LAST_SUDOKU)


# Function to start the thread manager and initiate the threads
def start():
    manager = ThreadManager()

    for i in range(1, 6):  # Start 5 threads
        thread_name = f"thread_{i}"
        checkpoint_file = f"{thread_name}_checkpoint.json"
        last_board = read_last_checkpoint(checkpoint_file)
        if last_board is None:
            last_board = generate_board(i * 2 - 1)  # Generate new board with odd starting values
        manager.add_thread(recursive_field_generator, (last_board, 0, 0, 2 * i, thread_name), name=thread_name)

    manager.add_thread(print_status, ())

    manager.start_all()
    manager.join_all()


# Entry point for the script
if __name__ == '__main__':
    start()
