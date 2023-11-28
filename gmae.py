import tkinter as tk

# Initialize the game board
table = [
    ['-','-','-'],
    ['-','-','-'],
    ['-','-','-']
]

# Initialize the current player
current_player = 'X'

# Create the main window
root = tk.Tk()
root.title("Tic-Tac-Toe")

# Function to handle button clicks
def on_button_click(row, col):
    global current_player

    if table[row][col] != '-':
        return

    table[row][col] = current_player
    buttons[row][col].config(text=current_player)
    buttons[row][col].config(state='disabled')

    if check_win(table, current_player):
        winner_label.config(text=f'Player {current_player} wins!')
        disable_all_buttons()
    elif all([cell != '-' for row in table for cell in row]):
        winner_label.config(text='It\'s a draw!')
        disable_all_buttons()
    else:
        current_player = 'O' if current_player == 'X' else 'X'
        player_label.config(text=f'Current Player: {current_player}')

# Function to check if a player has won
def check_win(board, player):
    for row in board:
        if row.count(player) == 3:
            return True

    for i in range(3):
        if board[0][i] == player and board[1][i] == player and board[2][i] == player:
            return True

    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True

    if board[0][2] == player and board[1][1] == player and board[2][0] == player:
        return True

# Function to disable all buttons
def disable_all_buttons():
    for row in range(3):
        for col in range(3):
            buttons[row][col].config(state='disabled')

# Create buttons for the game board
buttons = [[None, None, None] for _ in range(3)]
for row in range(3):
    for col in range(3):
        buttons[row][col] = tk.Button(root, text='', width=10, height=2,
                                      command=lambda row=row, col=col: on_button_click(row, col))
        buttons[row][col].grid(row=row, column=col)

# Create a label to display the current player
player_label = tk.Label(root, text=f'Current Player: {current_player}')
player_label.grid(row=3, column=0, columnspan=3)

# Create a label to display the winner or draw message
winner_label = tk.Label(root, text='', font=("Helvetica", 16))
winner_label.grid(row=4, column=0, columnspan=3)

# Function to reset the game
def reset_game():
    global table, current_player
    table = [['-' for _ in range(3)] for _ in range(3)]
    current_player = 'X'
    player_label.config(text=f'Current Player: {current_player}')
    winner_label.config(text='')
    for row in range(3):
        for col in range(3):
            buttons[row][col].config(text='', state='active')

# Create a button to reset the game
reset_button = tk.Button(root, text='Restart Game', command=reset_game)
reset_button.grid(row=5, column=0, columnspan=3)

# Run the main loop
root.mainloop()