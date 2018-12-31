import time

TILE_DESCS = {'(_)': 'dirt', '(r)': 'ruby', '(s)': 'sapphire',
                     '(e)': 'emerald', '(d)': 'diamond',
                     '(x)': 'wall'}

GEMS = ['ruby', 'sapphire', 'emerald', 'diamond']

class Tile:
    '''A class to represent one spot/location on the map.'''
    
    def __init__(self, x: int, y: int, icon: str, desc: str) -> None:
        '''
        Construct Tile using x, y coordinates, a string icon to represent
        this tile on the map, and a longer string description of
        what this tile represents.

        The Tile also keeps track of a list of Tiles that are adjacent
        to it (horizontally or vertically; Drillbots can NOT move diagonally).
        '''
        
        self.x = x
        self.y = y
        self.icon = icon
        self.desc = desc
        self.adj_tiles = []

    def get_visited(self, id_num: int) -> None:
        '''
        Update this tile's icon/desc to represent drillbot visiting the location.
        '''

        self.icon = '(' + str(id_num) + ')'
        self.desc = 'drillbot'
        
    def get_dug(self) -> None:
        '''
        Update this tile's icon/desc to be dirt, after being dug.
        '''

        self.icon = '(_)'
        self.desc = 'dirt'
        
    def __str__(self) -> str:
        '''
        Return string representation of this tile.
        '''

        return self.icon

    def __repr__(self) -> str:
        '''
        Return detailed string representation of this tile.
        '''

        return 'desc: ' + self.desc + '\nx: ' + str(self.x) + '\ny: ' + str(self.y)
    
class Map:
    '''A class to represent a map made of several connected tiles.'''

    def __init__(self, map_data: list):
        '''
        Given a list of lists representing map data, construct Tiles to represent
        each location, connect adjacent tiles, and assign a starting point.
        
        In a valid map, the starting point will NOT be a wall, and every gem
        in the map will be accessible through up/down/left/right movements,
        beginning from this starting point.
        
        You may assume all maps that are passed in are valid.
        (That is, we will only test your code with valid maps).
        '''

        self.tiles = self._create_tiles(map_data)
        self._connect_tiles()
        self.start = self.tiles[0][0]

    def _create_tiles(self, map_data: list) -> list:
        '''
        Return a list of lists of Tile objects representing each location
        on the given map_data as a Tile (each with x, y coordinates, the visual
        icon representation of it, and a string description).
        '''
        
        tiles = []
        for i in range(len(map_data)):
            new_row = []
            for k in range(len(map_data[i])):
                icon = map_data[i][k]
                new_row.append(Tile(k, i, icon, TILE_DESCS[icon]))
            tiles.append(new_row)
        return tiles

    def _connect_tiles(self) -> None:
        '''
        For each tile in self.tiles, keep track of a list of all of
        that tile's adjacent non-wall tiles.
        '''
        
        for i in range(len(self.tiles)):
            for k in range(len(self.tiles[i])):
                self.tiles[i][k].adj_tiles = self.find_adj(k, i)

    def __len__(self) -> int:
        '''Finds the length of the given part of the map, either horizontal
        or vertical.
        '''
        count = 0
        for elm in self.tiles:
            count = count + 1
        return count

    def find_adj(self, x: int, y: int) -> list:
        '''
        Return a list of non-wall Tile objects which are adjacent (to the north,
        south, east and west; NO diagonals) of the given x and y position.
        
        e.g.
        If my map is as follows:
        (x) (s) (d)
        (_) (_) (r)
        (e) (x) (_)
        And we called find_adj on coordinates (2, 2) which is the bottom-right
        corner of the map, then this method should return a list of just one
        adjacent tile -- the tile at position (2, 1) containing the ruby (r) to the
        north of this spot. This is because every other spot beside this location
        is out of bounds, and to the left is a wall, so the wall is not
        included in the adjacent tiles.
        '''
        dxdys = [(0,1),(1,0),(0,-1),(-1,0)]
        adj = []
        for dxdy in dxdys:
            newX = x + dxdy[0]
            newY = y + dxdy[1]
            if newX < 0 or newY < 0:
                pass
            elif newX >= len(self.tiles[0]) or newY >= len(self.tiles):
                pass
            elif self.tiles[newY][newX].desc in GEMS + ["dirt"]:
                adj.append(self.tiles[newY][newX])

        return adj
                
    def __repr__(self) -> str:
        '''
        Return a string representation of this map.
        '''
        
        s = ''
        for row in self.tiles:
            for t in row:
                s += str(t)
            s += "\n"
        return s

class DrillBot:

    def __init__(self, m):
        '''Given a map, puts the DrillBot on the map and assigns it an icon
        according to the id_num. Creates a storage and list of everyone
        previously visited by the DrillBot.
        '''
        self.id_num = 0
        self.storage = {}
        self.visited = []
        self.map = m

    def visit(self, location: Tile):
        '''Given a location, moves the DrillBot to it and adds any
        gems collected to the storage.
        '''
        dug = location.desc #checks desc of tile
        location.get_visited(self.id_num) #moves drillbot to location
        print(self.map) #prints map
        if dug in GEMS: #if the tile has a gem
            self.storage[dug] = self.storage.get(dug, 0) + 1 #updates storage
        location.get_dug() #updates map with dirt
        self.visited.append(location) #adds which tile was visited
        time.sleep(0.5) #changes time
        
    def explore(self, location: Tile):
        '''Given a location, checks the adjacent tiles to possibly visit.
        Once all the tiles on the map have been visited, returns to the
        starting location and tallies up all gems collected.
        '''
        self.visit(location)
        togo = self.map.find_adj(location.x, location.y)
        togo.reverse()
        num_moves = 0
        for tile in togo:
            if tile not in self.visited:
                num_moves += 1
                self.explore(tile)
        if num_moves == 0:
            currIndex = self.visited.index(location)
            if currIndex == 0:
                return
            self.explore(self.visited[currIndex-1])
                
        
if __name__ == "__main__":
    # Some set worlds; feel free to add more maps to test things out
    map1 = [['(_)','(_)','(s)'],
             ['(_)','(x)','(r)'],
             ['(_)','(_)','(_)']]

    map2 = [['(_)','(_)','(s)','(r)','(_)'],
             ['(_)','(x)','(r)','(x)','(s)'],
             ['(_)','(_)','(_)','(x)','(r)'],
             ['(_)','(x)','(_)','(x)','(_)'],
             ['(d)','(x)','(x)','(x)','(_)'],
             ['(_)','(d)','(_)','(s)','(r)']]

    # Set the map_data to use, construct a Map object, start drilling, print out results
    map_data = map2
    m = Map(map_data)
    print('this is the starting point')
    print(m.start)
    print('it also has children that are adjacent tiles')
    print(m.start.adj_tiles)
    print('now to build a drill bot and have it explore map.start')
    print("'0' is the drill bot, \n'_' is just dirt, \n'x' is an impassable wall, \n'r' is a ruby, \n's' is a saphhire, \n'e' is an emerald, \n'd' is a diamond")
    d = DrillBot(m)
    d.explore(m.start)
    print('and this is what the drillbot managed to mine')
    print(d.storage)
