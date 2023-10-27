import random

suits = ['spades', 'hearts', 'cloves', 'diamonds']
values = [1,2,3,4,5,6,7,8,9,10,11,12,13]
cards = []
main_cells = []
end_cells = []
free_cells = []

class Game:
    def __init__(self):
        self.moves = []

    def undo(self):
        if not self.moves: return
        for cell in all_cells:
            cell.contents = cell.previous_states.pop()

class Card:
    def __init__(self, suit:int, value: int, color: int):
        self.suit = suit
        self.value = value
        self.color = color
        self.is_ordered = False

    def __repr__(self) -> str:
        return f'{self.value} {self.suit}'
    
    def __lt__(self, other):
        return self.value > other.value
    
class Cell:
    def __init__(self, order:str, limit:int, id: int):
        self.order = order
        self.limit = limit
        self.id = id
        self.contents: list[Card] = []
        self.groups = []
        self.previous_states = []
        self.orderable_end_amount = 0
    
    def log_state(self):
        state = self.contents.copy()
        self.previous_states.append(state)

    def __repr__(self) -> str:
        return f'{self.contents}'
    
    def find_groups(self):
        if not self.contents:
            self.groups = []
            return
        groups = []
        group = [self.contents[0]]
        for index in range(len(self.contents) - 1):
            top_card, bottom_card = self.contents[index], self.contents[index+1]
            if are_ordered(top_card, bottom_card):
                group.append(bottom_card)
            else:
                groups.append(group)
                group = [bottom_card]
        if group not in groups: groups.append(group)
        self.groups = groups
        return

    def is_ordered(self):
        self.find_groups()
        return len(self.groups) in (0,1)

    def can_be_ordered(self, amount_of_cards = 20):
        initial_state = self.contents.copy()
        self.contents = self.contents if len(self.contents) <= amount_of_cards else self.contents[-amount_of_cards:]
        if self.is_ordered():
            self.contents = initial_state
            return False
        self.contents.sort()
        orderable = self.is_ordered()
        self.contents = initial_state
        return orderable

    def can_order_end(self):
        number_of_empty_free_cells = len([cell for cell in free_cells if not cell.contents])
        if number_of_empty_free_cells == 0: return False
        for count in range(number_of_empty_free_cells):
            orderable = self.can_be_ordered(number_of_empty_free_cells - count)
            if orderable:
                self.orderable_end_amount = number_of_empty_free_cells - count
                return orderable
            if count == 2: return False


def are_ordered(top_card: Card, bottom_card: Card):
    return top_card.color != bottom_card.color and bottom_card.value + 1 == top_card.value

def find_moves():
    moves = []
    for origin_index, origin_cell in enumerate(main_cells):
        if not origin_cell.groups: continue
        for dest_index, destination_cell in enumerate(main_cells):
            if destination_cell == origin_cell: continue
            elif not destination_cell.groups:
                moves.append((origin_index, dest_index))
            elif are_ordered(destination_cell.contents[-1], origin_cell.groups[-1][0]):
                moves.append((origin_index, dest_index))
    return moves

def find_clears():
    clears = []
    for origin_index, origin_cell in enumerate(main_cells):
        if not origin_cell.contents: continue
        card_to_move = origin_cell.contents[-1]
        for dest_index, destination_cell in enumerate(end_cells):
            if not destination_cell.contents and card_to_move.value == 1:
                clears.append((origin_index, dest_index + 8))
            elif not destination_cell.contents: continue
            elif destination_cell.contents[-1].value + 1 == card_to_move.value and destination_cell.contents[-1].suit == card_to_move.suit:
                clears.append((origin_index, dest_index + 8))
    return clears

def find_parking_options():
    parking_options = []
    if not all([cell.contents for cell in free_cells]):
        cards = [cell.contents[-1] for cell in main_cells if cell.contents]
        for destination_index, cell in enumerate(free_cells):
            if not cell.contents:
                for origin_index, cell in enumerate(cards):
                    parking_options.append((origin_index, destination_index + 12))
                return parking_options
    return parking_options
            
def find_unparking_options():
    unparking_options = []
    for origin_index, origin_cell in enumerate(free_cells):
        if not origin_cell.contents: continue
        for destination__index, destination_cell in enumerate(end_cells):
            card_to_move = origin_cell.contents[-1]
            if not destination_cell.contents and card_to_move.value == 1:
                unparking_options.append((origin_index + 12, destination__index + 8))
            elif not destination_cell.contents: continue
            elif destination_cell.contents[-1].value + 1 == card_to_move.value and destination_cell.contents[-1].suit == card_to_move.suit:
                unparking_options.append((origin_index + 12, destination__index + 8))

        for destination__index, destination_cell in enumerate(main_cells):
            if not destination_cell.groups:
                unparking_options.append((origin_index + 12, destination__index))
            elif are_ordered(destination_cell.contents[-1], origin_cell.contents[-1]):
                unparking_options.append((origin_index + 12, destination__index))
    return unparking_options

def move(origin: Cell, destination: Cell, amount_to_move: int = 20):
    if not origin.limit and not destination.limit:
        origin.find_groups()
        movable_cards = origin.groups.pop()
        diff = len(movable_cards) - amount_to_move if len(movable_cards) > amount_to_move else 0
        for i in range(min(len(movable_cards), amount_to_move)):
            origin.contents.pop()
            destination.contents.append(movable_cards[i + diff])
    else:
        moving_card = origin.contents.pop()
        destination.contents.append(moving_card)

game = Game()
for index, suit in enumerate(suits):
    color = index % 2
    for value in values:
        cards.append(Card(suit, value, color))
for ids in range(8):
    main_cells.append(Cell(order='descending', limit=0, id=ids))
for ids in range(4):
    end_cells.append(Cell(order='ascending', limit=1, id=ids + 8))
for ids in range(4):
    free_cells.append(Cell(order='asdasd', limit=1, id=ids + 12))
all_cells = main_cells + end_cells + free_cells

random.shuffle(cards)
while cards:
    for cell in main_cells:
        if cards:
            cell.contents.append(cards.pop())

def get_user_input(moves):
    try: 
        u_input = input('enter move:   ')
        if u_input == 'undo':
            game.undo()
            return False
        attempted_move = [int(arg) for arg in u_input.split()]
        if len(attempted_move) == 1:
            chosen_move = list(moves[attempted_move[0] - 1])
            chosen_move.append(20)
        elif len(attempted_move) == 2:
            chosen_move = attempted_move
            chosen_move.append(20)
        elif len(attempted_move) == 3:
            chosen_move = attempted_move
        return chosen_move
    except: return False

while True:
    print(f'free_cells                             end_cells')
    end_cell_view = [([cell.contents[-1]] if cell.contents else []) for cell in end_cells]
    print(f'{free_cells}          {end_cell_view}')
    for index, cell in enumerate(main_cells):
        # cell.contents.sort()
        cell.find_groups()
        print(index, cell.groups)

    if all([cell.is_ordered() for cell in main_cells]) and not any([cell.contents for cell in free_cells]):
        print(f'YYOU WONNNRR')
    moves = find_moves()
    moves.extend(find_clears())
    moves.extend(find_parking_options())
    moves.extend(find_unparking_options())
    print()
    print('options:')
    for index, possible_move in enumerate(moves):
            print(index + 1, possible_move)
    orderable_cells = [cell.id for cell in main_cells if cell.can_be_ordered()]
    print(f'cells that can be ordered: {orderable_cells}\n')
    orderable_ends = [f'cell {cell.id}: {cell.orderable_end_amount} cards' for cell in main_cells if cell.can_order_end()]
    print(f'ends that can be ordered: {orderable_ends}\n')
    # if not orderable_cells: continue
    chosen_move = get_user_input(moves)
    if not chosen_move: continue
    origin, destination, amount = chosen_move
    print(origin, destination, amount)
    # if (origin, destination) in moves:
    for cell in all_cells:
        cell.log_state()
    move(all_cells[origin], all_cells[destination], amount)
    game.moves.append(chosen_move)
    print(game.moves)
