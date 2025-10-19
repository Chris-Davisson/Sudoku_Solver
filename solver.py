import re

from typing import Dict, Optional

def cross(A, B) -> tuple:
    return tuple(a + b in A for b in B)

Digit     = str  # e.g. '1'
digits    = '123456789'
DigitSet  = str  # e.g. '123'
rows      = 'ABCDEFGHI'
cols      = digits
Square    = str  # e.g. 'A9'
squares   = cross(rows, cols)
Grid      = Dict[Square, DigitSet] # E.g. {'A9': '123', ...}
all_boxes = [cross(rs, cs)  for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
all_units = [cross(rows, c) for c in cols] + [cross(r, cols) for r in rows] + all_boxes
units     = {s: tuple(u for u in all_units if s in u) for s in squares}
peers     = {s: set().union(*units[s]) - {s} for s in squares}
Picture   = str 


def is_solution(solution: Grid, puzzle: Grid) -> bool:
    return (solution is not None and
            all(solution[s] in puzzle[s] for s in squares) and
            all ({solution[s] for s in unit} == set(digits) for unit in all_units))

def constrain(grid) -> Grid:
    "Propagate constraints on a copy of grid to yield a new constrained Grid."
    result: Grid = {s: digits for s in squares}
    for s in grid:
        if len(grid[s]) == 1:
            fill(result, s,  grid[s])
    return result

def fill(grid: Grid, s: Square, d: Digit) -> Optional[Grid]:
    """Eliminate all the digits except d from grid[s]."""
    if grid[s] == d or all(eliminate(grid, s, d2) for d2 in grid[s] if d2 != d):
        return grid
    else:
        return None

def eliminate(grid: Grid, s: Square, d: Digit) -> Optional[Grid]:
    """Eliminate d from grid[s]; implement the two constraint propagation strategies."""
    if d not in grid[s]:
        return grid        ## Already eliminated
    grid[s] = grid[s].replace(d, '')
    if not grid[s]:
        return None        ## None: no legal digit left
    elif len(grid[s]) == 1:
        # 1. If a square has only one possible digit, then eliminate that digit as a possibility for each of the square's peers.
        d2 = grid[s]
        if not all(eliminate(grid, s2, d2) for s2 in peers[s]):
            return None    ## None: can't eliminate d2 from some square
    for u in units[s]:
        dplaces = [s for s in u if d in grid[s]]
        # 2. If a unit has only one possible square that can hold a digit, then fill the square with the digit.
        if not dplaces or (len(dplaces) == 1 and not fill(grid, dplaces[0], d)):
            return None    ## None: no place in u for d
    return grid

def parse(picture) -> Grid:
    """Convert a Picture to a Grid."""
    vals = re.findall(r"[.1-9]|[{][1-9]+[}]", picture)
    assert len(vals) == 81
    return {s: digits if v == '.' else re.sub(r"[{}]", '', v) 
            for s, v in zip(squares, vals)}

def picture(grid) -> Picture:
    """Convert a Grid to a Picture string, one line at a time."""
    if grid is None: 
        return "None"
    def val(d: DigitSet) -> str: return '.' if d == digits else d if len(d) == 1 else '{' + d + '}'
    maxwidth = max(len(val(grid[s])) for s in grid)
    dash1 = '-' * (maxwidth * 3 + 2)
    dash3 = '\n' + '+'.join(3 * [dash1])
    def cell(r, c): return val(grid[r + c]).center(maxwidth) + ('|'  if c in '36' else ' ')
    def line(r): return ''.join(cell(r, c) for c in cols)    + (dash3 if r in 'CF' else '')
    return '\n'.join(map(line, rows))

pic1 = "53..7.... 6..195... .98....6. 8...6...3 4..8.3..1 7...2...6 .6....28. ...419..5 ....8..79"
grid1 = parse(pic1)
print(picture(grid1))