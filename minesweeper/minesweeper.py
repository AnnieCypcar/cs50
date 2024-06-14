import itertools
import random
from pprint import pprint


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # if the count is not zero and the count is the same as the number of cells
        # then all of the cells must be mines
        if self.count > 0 and len(self.cells) == self.count:
            return self.cells.copy()
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # if the sentence count is zero, all the cells must be safes
        if self.count == 0:
            return self.cells.copy()
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # remove the cell from the sentence to mark it as a mine
        # decrement the number of mines after it is removed
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # remove the cell from the sentence if it is safe
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)
    
    def is_cell_in_bounds(self, cell):
        # verify the cell is in bounds
        i, j = cell
        return 0 <= i < self.height and 0 <= j < self.width
    
    def update_knowledge(self):
        has_new_info = False

        safes = set()
        mines = set()

        # Try to infer new sentences from the current ones:
        for s1 in self.knowledge:
            # Get set of safe spaces and mines from KB
            safes = safes.union(s1.known_safes())
            mines = mines.union(s1.known_mines())

            for s2 in self.knowledge:
                # Ignore when sentences are identical or cells and count are empty
                if s1.cells == s2.cells or (s1.cells == set() and s1.count > 0):
                    continue

                # Create a new sentence if 1 is subset of 2, and not in KB:
                if s1.cells.issubset(s2.cells):
                    new_sentence_cells = s2.cells - s1.cells
                    new_sentence_count = s2.count - s1.count

                    new_sentence = Sentence(new_sentence_cells, new_sentence_count)

                    # Add to knowledge if not already in KB:
                    if new_sentence not in self.knowledge:
                        has_new_info = True
                        self.knowledge.append(new_sentence)
        
        # Mark any safe spaces or mines:
        if safes:
            has_new_info = True
            for safe in safes:
                self.mark_safe(safe)
        if mines:
            has_new_info = True
            for mine in mines:
                self.mark_mine(mine)

        if has_new_info:
            self.update_knowledge()

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)
        self.mark_safe(cell)
        
        unconfirmed_cells = set()
        known_mines = count
        i, j = cell
        neighbors = [(i+1, j), (i-1, j), (i, j+1), (i, j-1),
                     (i+1, j+1), (i-1, j-1), (i+1, j-1), (i-1, j+1)]
        for x, y in neighbors:
            # verify the cell is in bounds
            if self.is_cell_in_bounds((x, y)):
                if (x, y) in self.mines:
                    # update number of mines if found and decrease the mines count
                    known_mines -= 1
                elif (x, y) not in self.safes:
                    # if the cell is not a known safe or mine, mark it unconfirmed
                    unconfirmed_cells.add((x, y))
        # knowlege base stores sentences about unknown cells only
        # add the sentence only if unconfirmed_cells is not empty
        sentence = None
        if unconfirmed_cells:
            sentence = Sentence(unconfirmed_cells, known_mines)
            self.knowledge.append(sentence)
        
        self.update_knowledge()

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for i in range(self.height):
            for j in range(self.width):
                if (i, j) not in self.moves_made and (i, j) in self.safes:
                    return (i, j)
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        for i in range(self.height):
            for j in range(self.width):
                if (i, j) not in self.moves_made and (i, j) not in self.mines:
                    return (i, j)
        return None
