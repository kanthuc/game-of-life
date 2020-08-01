class Cell:
    neighbors = ((-1, -1), (-1, 0), (-1, 1),
                 (0,  -1),          (0,  1),
                 (1,  -1), (1,  0), (1,  1))

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "(%i, %i)"%(self.x,self.y)

    def __eq__(self, other):
        return self.x==other.x and self.y==other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def get_neighbors(self):
        for dx, dy in Cell.neighbors:
            yield Cell(self.x+dx, self.y+dy)

class Board:
    def __init__(self):
        self.live_cells = set()

    def __repr__(self):
        return "{%s}"%", ".join(str(cell) for cell in self.get_live_cells())

    def get_live_cells(self):
        for cell in self.live_cells:
            yield cell

    def count_live_neighbors(self, cell):
       return sum(n in self.live_cells for n in cell.get_neighbors())

    def stays_alive(self, cell):
        return 2 <= self.count_live_neighbors(cell) <= 3

    def reproduces(self, cell):
        return self.count_live_neighbors(cell) == 3

    def update(self):
        live_cells = set()
        for cell in self.live_cells:
            if self.stays_alive(cell):
                live_cells.add(cell)
            for n in cell.get_neighbors():
                if n not in self.live_cells and self.reproduces(n):
                    live_cells.add(n)
        self.live_cells = live_cells

    def is_alive(self, cell):
        return cell in self.live_cells

    def toggle_cell(self, cell):
        if cell in self.live_cells:
            self.live_cells.remove(cell)
        else:
            self.live_cells.add(cell)

    def clear_board(self):
        self.live_cells.clear()
