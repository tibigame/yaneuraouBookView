from ShogiNotebook.Board import Board

data = open("user_book1.db", "r")

class Move:
    def __init__(self, sfen: str, move: str):
        input_ = move.split()
        self.move = input_[0]
        self.next = input_[1]
        self.value = int(input_[2])
        self.parent = sfen + " 0"

def move_json(move: Move):
    board = Board(move.parent)
    m = board.move(move.move)
    return {
        "move": move.move,
        "movePretty": m.detail,
        "next": move.next,
        "value": move.value,
        "movedSfen": board.get_sfen()
    }

class BookNode:
    def __init__(self):
        self.sfen = ""
        self.move_list = []

    def sfen(self, sfen: str):
        self.sfen = sfen

    def insert(self, move):
        self.move_list.append(Move(self.sfen, move))

def make_book_node_list():
  book_node_list = []

  sfen_flag = False
  move_flag = False
  sfen = ""
  move = ""
  book_node = BookNode()
  line = data.readline().strip()

  while line:
      line = data.readline().strip()
      if line[0:4] == "sfen":
          if len(book_node.sfen):
              book_node_list.append(book_node)
          book_node = BookNode()
          book_node.sfen = " ".join(line.split()[:-1])
      else:
          if len(line) > 4 and line[0] != "#":
              book_node.insert(line)
              sfen_flag = False
  return book_node_list

def make_dict():
    book_dict = {}
    for book_node in make_book_node_list():
        book_dict[book_node.sfen] = book_node.move_list
    return book_dict

if __name__ == '__main__':
    pass
