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


# Example Sudoku grid
sudoku_grid = [[1, 2, 3, 4, 5, 6, 7, 8, 9], [4, 5, 6, 7, 8, 9, 1, 2, 3], [7, 8, 9, 1, 2, 3, 4, 5, 6],
               [2, 1, 4, 3, 6, 5, 8, 9, 7], [3, 6, 5, 8, 9, 7, 2, 1, 4], [8, 9, 7, 2, 1, 4, 3, 6, 5],
               [5, 7, 8, 9, 4, 1, 6, 3, 2], [6, 4, 1, 5, 3, 2, 9, 7, 8], [9, 3, 2, 6, 7, 8, 5, 4, 1]]

create_sudoku_gui(sudoku_grid)
