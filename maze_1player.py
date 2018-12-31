import random
from stack import Stack #PUT STACK ELEMENT IN GET NEW POSITION

class MazeGame:
    '''
    A game where a player moves through a grid to reach some treasure.
    '''

    def __init__(self, width, height, player):
        '''
        (MazeGame, Player) -> None
        Construct a new MazeGame with the given width and height,
        and a player. MazeGame should also place a "gold" at
        a randomly chosen coordinate on the far edge of the grid.
        '''
        
        self.width = width
        self.height = height
        self.player = player
        # place the gold at a random spot on the far edge of the grid
        self.gold_coord = (width-1, random.randint(1, height-1)) 

        self.grid = []
        self.make_grid()
        self.stack = Stack() #sets the stack to be accesible
        
    def make_grid(self):
        '''
        (MazeGame) -> None
        Given width, height and positions of player and gold,
        append things to this maze's grid.
        '''
        
        for i in range(self.height):
            self.grid.append([])
            for j in range(self.width):
                self.grid[i].append('(_)') 
        
        self.grid[self.player.y][self.player.x] = '(x)'
        self.grid[self.gold_coord[1]][self.gold_coord[0]] = '(*)'

    
    def play_game(self):
        '''
        (MazeGame) -> None
        Play the game, with each player taking turns making a move, until
        one player reaches the gold. Players each keep track of their wins and losses.
        '''
        
        # print out the starting state of the maze
        print(self)
        print('------------')
        
        while (not (self.player.x, self.player.y) == \
               (self.gold_coord[0], self.gold_coord[1])):
            # if no one has reached the gold yet, play one turn of the game (one player makes one move)
            self.play_one_turn()

        
        print('Yay, you won, {}!'.format(self.player.name))


    def get_new_position(self, d):
        '''
        (MazeGame, str) -> tuple of two ints or None        
        Given a direction represented as a string "N", "S", "E", or "W" (for moving North,
        South, East or West respectively), return the new position. If the new position is
        not valid (i.e. falls outside of the grid), return None.
        '''
        
        direction_dict = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0)}
        dx, dy = direction_dict[d]
        new_x = self.player.x + dx
        new_y = self.player.y + dy

        if (0 <= new_x < self.width) and (0 <= new_y < self.height):
            return new_x, new_y
        else:
            return None

    def update_grid(self, new_position):
        '''
        (MazeGame, tuple of two ints) -> None
        Move player to the given new position in grid.
        '''
        # update grid to reflect updated coordinates for current_player
        # keep track of the Player's current position before they move
        old_x, old_y = self.player.x, self.player.y 
        self.player.move(new_position)
        self.grid[self.player.y][self.player.x] = self.grid[old_y][old_x]
        self.grid[old_y][old_x] = '(_)'

        self.stack.push((old_y, old_x))
        
    def play_one_turn(self):
        '''
        (MazeGame) -> None
        Play one turn of the game. Turn could involve moving one place,
        attempting to move one place, or undoing the most recent move.
        '''

        # get the direction the Player wants to move
        direction = self.player.get_direction() 

        if (direction == 'U'):
            self.undo_last_move()
        else:
            # this returns None if move is not valid
            new_position = self.get_new_position(direction) 
            
            if new_position: # this is the same as saying "if new_position != None"                
                self.update_grid(new_position)
                print("Player {} moved {}.".format(self.player.name, direction))
            else:
                print("Player {} attempted to move {}. Way is blocked.".format(self.player.name, direction))

        # print current state of game
        print(self)
        print('------------')

    def undo_last_move(self):
        '''
        (MazeGame) -> None
        Update the grid to the state it was in before the previous move was made.
        If no moves were previously made, print out the message "Can't undo".
        '''
        if self.stack.isEmpty():
            print("Invalid. There was no past move.")
        else:
            last_move = self.stack.pop()
            self.grid[self.player.y][self.player.x] = "(_)"
            self.player.y = last_move[0]
            self.player.x = last_move[1]
            self.grid[last_move[0]][last_move[1]] = '(x)'
    
    def __str__(self):
        '''
        (MazeGame) -> str
        Return string representation of the game's grid.
        '''
        s = ''
        for row in self.grid:
            s += ''.join(row) + "\n"
        return s.strip()


class Player:

    def __init__(self, name, y, x):
        self.x = x
        self.y = y
        self.name = name
        self.coords = (y, x)

    def get_direction(self):
        '''Supposed to output a string'''
        direction = input("Which direction do you want to go? U for undo: ")
        while direction.lower() not in "nwesu":
            direction = input("Error. Input new direction or undo: ")
        if direction.lower() in "nwesu":
            direction = direction.upper()
        return direction

    def move(self, newpos):
        self.x = newpos[0]
        self.y = newpos[1]
        

def main():
    """Prompt the user to configure and play the game."""

    width = int(input("Width: "))
    height = int(input("Height: "))

    name = input("What is your name? ")
    p1 = Player(name, 0, 0) # make a player at position (0,0)
    
    play_again = True
    while play_again:
        g = MazeGame(width, height, p1)
        g.play_game()
        # reset player locations at end of round
        p1.move((0,0))
        play_again = input('Again? (y/n) ') == 'y'           


if __name__ == '__main__':
    main()
