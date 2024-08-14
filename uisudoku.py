import tkinter as tk

def create_sudoku_gui(grid):
    root = tk.Tk()
    root.title("Sudoku")

    for i, row in enumerate(grid):
        for j, value in enumerate(row):
            entry = tk.Entry(root, width=3, font=('Arial', 18), justify='center')
            entry.grid(row=i, column=j, padx=5, pady=5)
            entry.insert(tk.END, value if value != 0 else '')  # Insert 0 as empty

    root.mainloop()

# Example Sudoku grid (0 represents empty cells)
sudoku_grid = [[7, 1, 2, 3, 4, 5, 6, 8, 9], [3, 4, 5, 6, 8, 9, 1, 2, 7], [6, 8, 9, 1, 2, 7, 3, 4, 5], [1, 2, 3, 4, 5, 6, 7, 9, 8], [4, 7, 6, 8, 9, 3, 5, 1, 2], [5, 9, 8, 2, 7, 1, 4, 6, 3], [2, 5, 7, 9, 1, 4, 8, 3, 6], [9, 6, 4, 5, 3, 8, 2, 7, 1], [8, 3, 1, 7, 6, 2, 9, 5, 4]]

create_sudoku_gui(sudoku_grid)
