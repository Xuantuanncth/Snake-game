import curses
import time
import random
import pyfiglet

EASY_MODE = 0
NORMAL_MODE = 3
HARD_MODE = 5

game_mode = EASY_MODE
def create_food(snake, obstacles, screen_height, screen_width):
    """
    This function generates a random food position for the snake game.
    The food position is ensured to be within the game boundaries and not on the snake or obstacles.

    Parameters:
    snake (list of lists): A list of tuples representing the current snake's position. Each tuple contains the y and x coordinates.
    obstacles (list of lists): A list of tuples representing the current obstacles' position. Each tuple contains the y and x coordinates.
    screen_height (int): The height of the game screen.
    screen_width (int): The width of the game screen.

    Returns:
    list: A tuple representing the y and x coordinates of the generated food position.
    """
    while True:
        food = [random.randint(4, screen_height-1), random.randint(10, screen_width-1)]
        if food not in snake and food not in obstacles:
            return food

def create_obstacles(level, screen_height, screen_width):
    """
    Generate a list of obstacle positions for the snake game.

    This function creates obstacles based on the current game level and screen dimensions.
    The number of obstacles increases with the level and game mode difficulty.

    Parameters:
    level (int): The current game level.
    screen_height (int): The height of the game screen.
    screen_width (int): The width of the game screen.

    Returns:
    list: A list of lists, where each inner list contains two integers 
          representing the y and x coordinates of an obstacle.
    """
    obstacles = []
    for _ in range(level*(level+game_mode)):
        while True:
            obstacle = [random.randint(4, screen_height-2), random.randint(10, screen_width-2)]
            if obstacle not in obstacles:
                obstacles.append(obstacle)
                break
    return obstacles


def draw_ascii_art(stdscr, text):
    """
    Draw ASCII art text on the screen using pyfiglet.

    This function generates ASCII art from the given text using the 'dos_rebel' font,
    and draws it centered on the screen.

    Parameters:
    stdscr (curses.window): The curses window object to draw on.
    text (str): The text to be converted into ASCII art.

    Returns:
    int: The number of lines in the ASCII art.
    """
    counter = 0
    # Create an instance of Figlet and set the font 
    # font = 'dos_rebel'
    figlet = pyfiglet.Figlet(font='dos_rebel')

    # Generate the ASCII art
    ascii_art = figlet.renderText(text)

    # Clear the screen
    stdscr.clear()

    # Calculate the center position to start drawing
    height, width = stdscr.getmaxyx()
    start_y = height // 2 - ascii_art.count('\n') // 2
    start_x = width // 2 - max(len(line) for line in ascii_art.split('\n')) // 2

    # Draw each line of the ASCII art at the calculated position
    for i, line in enumerate(ascii_art.split('\n')):
        stdscr.addstr(5 + i, start_x, line)
        counter += 1

    # Refresh the screen to show the updates
    # stdscr.refresh()

    # Wait for a key press before exiting
    # stdscr.getch()
    return counter


def draw_border(stdscr, top, left, width, height):
    stdscr.addch(top, left, curses.ACS_ULCORNER)
    stdscr.addch(top, left + width - 1, curses.ACS_URCORNER)
    stdscr.addch(top + height - 1, left, curses.ACS_LLCORNER)
    stdscr.addch(top + height - 1, left + width - 1, curses.ACS_LRCORNER)

    for i in range(1, width - 1):
        stdscr.addch(top, left + i, curses.ACS_HLINE)
        stdscr.addch(top + height - 1, left + i, curses.ACS_HLINE)

    for i in range(1, height - 1):
        stdscr.addch(top + i, left, curses.ACS_VLINE)
        stdscr.addch(top + i, left + width - 1, curses.ACS_VLINE)

def game_winner_screen(stdscr, screen_height, screen_width):
    """
        Display the game start
        ----------------------------------------------------------------
        |                                                             |
        |                      Snake Game                             |
        |                                                             |
        |                      Congratulation                         |
        |                                                             |
        |                      You are best                           |
        |                                                             |
        |                                                             |
        ----------------------------------------------------------------
    """
    game_name = "  SNAKE GAME  "
    height, width = 15, 50
    top = (screen_height - height)//2
    left = (screen_width - width)//2
    y_center = left + (width -len(game_name))//2

    #draw border
    stdscr.clear()
    draw_border(stdscr, top, left, width, height)
    stdscr.addstr(top + 1, y_center, game_name, curses.A_BOLD | curses.A_REVERSE)
    stdscr.addstr(top + 5, y_center, "Congratulation")
    stdscr.addstr(top + 9, y_center, "You are best :)")
    while True:
        key = stdscr.getch() # Wait for user input to exit
        if (key == 10 or key == 13):
            return

def game_start_screen(stdscr):
    """
        Display the game start
        ----------------------------------------------------------------
        |                                                             |
        |                      Snake Game                             |
        |                                                             |
        |                      <  Easy  >                             |
        |                                                             |
        |                         Start                               |
        |                                                             |
        |                                                             |
        ----------------------------------------------------------------
    """
    global game_mode
    _display_game_mode = ['Easy', 'Medium','Hard']
    _game_mode = [EASY_MODE,NORMAL_MODE, HARD_MODE]
    _mode = 0
    game_name = "  SNAKE GAME  "
    screen_height, screen_width = stdscr.getmaxyx()
    height, width = 15, 50
    top = (screen_height - height)//2
    left = (screen_width - width)//2
    y_center = left + (width -len(game_name))//2
    #draw border
    # draw_border(stdscr, top, left, width, height)
    counter = draw_ascii_art(stdscr,"Snake Game")
    # stdscr.addstr(top + 1, y_center, game_name, curses.A_BOLD | curses.A_REVERSE | curses.color_pair(1))
    stdscr.addstr(counter + 5, y_center + 4, "Start")
    stdscr.addstr(counter + 3, y_center, "<", curses.A_REVERSE)
    stdscr.addstr(counter + 3, y_center + 12, ">")
    dir = 1
    curses.curs_set(0)
    while True:
        stdscr.addstr(counter + 3, y_center + 4, _display_game_mode[_mode])
        key = stdscr.getch()
        if key == curses.KEY_LEFT and dir == 1:
            stdscr.addstr(counter + 3, y_center, "<", curses.A_REVERSE)
            stdscr.addstr(counter + 3, y_center + 12, ">")
            stdscr.addstr(counter + 3, y_center + 4, " " * len(_display_game_mode[_mode]))
            _mode = (_mode - 1) % len(_game_mode)
        elif key == curses.KEY_RIGHT and dir == 1:
            stdscr.addstr(counter + 3, y_center, "<")
            stdscr.addstr(counter + 3, y_center + 12, ">", curses.A_REVERSE)
            stdscr.addstr(counter + 3, y_center + 4, " " * len(_display_game_mode[_mode]))
            _mode = (_mode + 1) % len(_game_mode)
        elif key == curses.KEY_DOWN or key == curses.KEY_UP:
            if dir == 1:
                dir = 2
            else:
                dir = 1
        if dir == 2:
            stdscr.addstr(counter + 5, y_center + 4, "Start", curses.A_BOLD | curses.A_REVERSE)
        else:
            stdscr.addstr(counter + 5, y_center + 4, "Start")
        if (key == 10 or key == 13) and dir == 2:  # Check for ENTER key
            game_mode = _game_mode[_mode]
            print("Mode: ", game_mode)
            stdscr.clear()
            return

def game_over_screen(stdscr, score):
    """
        Display the game stop
        ----------------------------------------------------------------
        |                                                             |
        |                        GAME OVER                            |
        |                                                             |
        |                      Final Score: 0                         |
        |                                                             |
        |                      >  Try again                           |
        |                                                             |
        |                          Exit                               |
        |                                                             |
        ----------------------------------------------------------------
    """
    screen_height, screen_width = stdscr.getmaxyx()

    stdscr.clear()
    height, width = 15, 50
    # top, left = 5, 25
    top = (screen_height - height)//2
    left = (screen_width - width)//2
    y_score = left + (width -len("GAME OVER"))//2
    
    draw_border(stdscr, top, left, width, height)
    
    stdscr.addstr(top+1, y_score, "GAME OVER", curses.A_BOLD | curses.A_REVERSE)
    stdscr.addstr(top+3, y_score - 3, f"Final Score: {score}")
    
    stdscr.addstr(top+5, y_score, "Try again")
    
    stdscr.addstr(top+7, y_score, "Exit")

    dir = 1
    while True:
        key = stdscr.getch()
        if key == curses.KEY_DOWN or key == curses.KEY_UP:
            if dir > 1:
                dir = 1
            else:
                dir += 1
        if dir == 1:
            stdscr.addstr(top+5, y_score-3, ">")
            stdscr.addstr(top+7, y_score-3, " ")
        else:
            stdscr.addstr(top+5, y_score-3, " ")
            stdscr.addstr(top+7, y_score-3, ">")
        if (key == 10 or key == 13) and dir == 1:  # Check for ENTER key
            stdscr.clear() 
            return "retry"
        elif (key == 10 or key == 13) and dir != 1:  # Check for ENTER key
            return "exit"
        
def level_up_screen(stdscr, level, screen_height, screen_width):
    """
    Displays the level up screen with a message indicating the completed level and prompts the user to press enter to continue.
    Args:
        stdscr: The curses window object where the screen will be displayed.
        level (int): The current level that has been completed.
        screen_height (int): The height of the screen.
        screen_width (int): The width of the screen.
    Returns:
        None
    """
    stdscr.clear()
    height, width = 15, 50
    # top, left = 5, 25
    top = (screen_height - height)//2
    left = (screen_width - width)//2

    draw_border(stdscr, top, left, width, height)
    message = f"Completed level {level}, next level"
    y_score = left + (width -len(message))//2

    stdscr.addstr(top + 1, y_score, message, curses.A_BOLD | curses.A_REVERSE)
    stdscr.addstr(top + 4, y_score + 2, "Press enter to continue")

    while True:
        key = stdscr.getch()
        if (key == 10 or key == 13):
            stdscr.clear()
            break

def main(stdscr):
    """
    Main function to run the Snake game.
    Args:
        stdscr: The curses window object.
    The function initializes the game screen, sets up the game loop, and handles
    the game logic including snake movement, collision detection, food generation,
    score tracking, and level progression. The game continues until the player
    either completes all levels or collides with the border, obstacles, or itself.
    """
    # Game loop
    level = 1
    score_goal = 1
    speed_mapping = {
        EASY_MODE: 200,
        NORMAL_MODE: 100,
        HARD_MODE: 50
    }
    game_start_screen(stdscr)
    while level <= 10:
        # Initialize the screen
        curses.curs_set(0)
        stdscr.nodelay(1)
        stdscr.timeout(speed_mapping[game_mode])

        # Get screen height and width
        screen_height, screen_width = stdscr.getmaxyx()
        print (screen_width, screen_height)
        width = screen_width - 10
        height = screen_height - 10
        top =  0
        left = 5
        print (width, height)
        draw_border(stdscr, top, left, width, height+1)
        # Initialize snake position and food
        snake_x = width // 4
        snake_y = height // 2
        snake = [
            [snake_y, snake_x],
            [snake_y, snake_x - 1],
            [snake_y, snake_x - 2]
        ]

        obstacles = create_obstacles(level, height, width)
        food = create_food(snake, obstacles, height, width)
        stdscr.addch(food[0], food[1], "o")

        for obs in obstacles:
            stdscr.addch(obs[0], obs[1], curses.ACS_CKBOARD)

        # Initialize key variables
        key = curses.KEY_RIGHT
        score = 0

        directions = {
            curses.KEY_UP: (-1, 0),
            curses.KEY_DOWN: (1, 0),
            curses.KEY_LEFT: (0, -1),
            curses.KEY_RIGHT: (0, 1)
        }

        while True:
            next_key = stdscr.getch()
            if next_key in directions:
                if (key == curses.KEY_UP and next_key != curses.KEY_DOWN) or \
                   (key == curses.KEY_DOWN and next_key != curses.KEY_UP) or \
                   (key == curses.KEY_LEFT and next_key != curses.KEY_RIGHT) or \
                   (key == curses.KEY_RIGHT and next_key != curses.KEY_LEFT):
                    key = next_key

            # Calculate new head position
            new_head = [snake[0][0] + directions[key][0], snake[0][1] + directions[key][1]]

            # Check for collision
            if new_head[0] in [0, height] or \
               new_head[1] in [5, width] or \
               new_head in snake or\
               new_head in obstacles:
                print("new head: ",new_head)
                time.sleep(1)
                result = game_over_screen(stdscr, score)
                if result == "retry":
                    level = 1
                    score_goal = 1
                    break
                elif result == "exit":
                    curses.endwin()
                    return

            # Insert new head to the snake
            snake.insert(0, new_head)

            # Check if snake eats food
            if snake[0] == food:
                score += 1
                food = create_food(snake,obstacles, height, width)
                stdscr.addch(food[0], food[1], "o")
            else:
                tail = snake.pop()
                stdscr.addch(tail[0], tail[1], ' ')

            stdscr.addch(snake[0][0], snake[0][1], "#", curses.A_REVERSE)
            stdscr.addstr(height + 1, left, f"Score: {score}")
            stdscr.addstr(height + 2, left, f"Goal: {score_goal} ")
            stdscr.addstr(height + 3, left, f"Level: {level} ")

            # Check if level is completed
            if score >= score_goal:
                if level < 5:
                    time.sleep(0.1)
                    level_up_screen(stdscr, level, screen_height, screen_width)
                    level += 1
                    score_goal += (1 + level)
                else:
                    time.sleep(1)
                    game_winner_screen(stdscr, screen_height, screen_width)
                    return
                break

if __name__ == "__main__":
    curses.wrapper(main)
