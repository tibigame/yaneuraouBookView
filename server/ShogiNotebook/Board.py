import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from ShogiNotebook.BitBoard import piece
from ShogiNotebook.BitBoard import reverse_piece
from ShogiNotebook.BitBoard import get_pos
from ShogiNotebook.BitBoard import BitBoard
fp = FontProperties(fname=r'C:\Windows\Fonts\ipaexg.ttf', size=24)

row = ["〇", "一", "二", "三", "四", "五", "六", "七", "八", "九",
       "十", "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八"]
column = ["０", "１", "２", "３", "４", "５", "６", "７", "８", "９"]


def dec_piecenum(piecenum):  # 駒の数字から駒文字に変更する
    mod = piecenum % 4
    if mod == 0 or mod == 1:  # 成り判定
        piece_base = piecenum
        promote = ""
    else:
        piece_base = piecenum - 2  # 成りなら2を引く
        promote = "+"
    return promote + reverse_piece[piece_base]


# 駒インデックスのタプルから符号リストに変換します
def conv_pos_tuple(p):
    result = []
    for (x, y) in zip(p[0], p[1]):
        result.append((y + 1, x + 1))  # インデックスと符号は1ずれる
    return result

# from→toの動きが手番側から見て上寄引のどれかかを判定する
def move_vertical(pos_from, pos_to, teban):
    if pos_from[1] == pos_to[1]:
        return "寄"
    elif teban == "b":
        if pos_from[1] > pos_to[1]:
            return "上"
        else:
            return "引"
    else:
        if pos_from[1] > pos_to[1]:
            return "引"
        else:
            return "上"

# fromから見てtoの位置が手番側から見て左右直のどれかかを判定する
def move_horizon(pos_from, pos_to, teban):
    if pos_from[0] == pos_to[0]:
        return "直"
    elif teban == "b":
        if pos_from[0] > pos_to[0]:
            return "左"
        else:
            return "右"
    else:
        if pos_from[0] > pos_to[0]:
            return "右"
        else:
            return "左"

def is_metal(p: str):
    return p == "g" or p == "G" or p == "s" or p == "S" or p == "+s" or p == "+S" or p == "+n" or p == "+N" or p == "+l" or p == "+L" or p == "+p" or p == "+P"

# 指し手の詳細
class MoveDetail:
    def __init__(self):
        self.type = ""
        self.pos = ""
        self.moved = ""
        self.is_promote = False
        self.move_piece_str = ""
        self.get_piece_str = ""
        self.get_piece_origin_str = ""
        self.get_piece_promoted = False
        self.detail = ""


class Board:
    # コンストラクタ
    def __init__(self, sfen, clear_koma_flag=False):
        self.ban = np.zeros([9, 9], "int8")  # インデックスと符号は1つずれるので注意
        self.set_sfen(sfen)
        if clear_koma_flag:
            self.__clear_koma()

    def __clear_koma(self):  # 駒台を空にする
        self.koma = {
            "r": 0,
            "b": 0,
            "g": 0,
            "s": 0,
            "n": 0,
            "l": 0,
            "p": 0,
            "R": 0,
            "B": 0,
            "G": 0,
            "S": 0,
            "N": 0,
            "L": 0,
            "P": 0
        }

    # 盤面を書き換える
    def ex_set(self, koma: str, pos):  # posの位置にkomaを置く
        self.ban[pos[1]][pos[0]] = piece[koma][0]

    # 手数カウント周り
    def get_count(self):
        return str(self.count)

    def set_count(self, count=0):
        self.count = int(count)
        return

    def inc_count(self, count=0):
        self.count += 1
        return

    # 手番周り
    def get_teban(self):  # 手番を返す b(先手) or w(後手)
        return self.teban

    def set_teban(self, new_teban):  # 手番を設定、bw以外を与えると手番反転
        if new_teban == "b" or new_teban == "w":
            self.teban = new_teban
        else:
            if self.teban == "b":
                self.teban = "w"
            else:
                self.teban = "b"

    def get_sfen_ban(self):  # Boardクラスからsfen形式の盤面文字列を生成する
        sfen = ""
        for rank in self.ban:  # 1行ずつ処理する
            sfen_rank = ""
            blank_pos = 0
            for pos in rank[::-1]:  # 逆順に取り出す
                if pos == 0:  # 空マスならカウントを増やす
                    blank_pos += 1
                else:
                    if blank_pos >= 1:  # 空マスの分をフラッシュする
                        sfen_rank += str(blank_pos)
                        blank_pos = 0
                    sfen_rank += dec_piecenum(pos)
            if blank_pos >= 1:  # 空マスがあればフラッシュする
                sfen_rank += str(blank_pos)
                blank_pos = 0
            sfen += (sfen_rank + "/")  # 最後の行にもスラッシュが付与されるがreturnで除かれる
        return sfen[0:-1]

    def set_sfen_ban(self, sfen_ban):  # sfen形式の盤面文字列からBoardクラスに値をセットする
        ranks = sfen_ban.split("/")  # 1行ずつ分割
        promote_flag = False  # Trueなら成り駒
        for i, rank in enumerate(ranks):
            temp_rank = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            temp_itr = 8
            for char in list(rank):  # 1行を1文字ずつスキャンする
                if char.isdigit():  # 数字なら空白マスなので飛ばす
                    temp_itr -= int(char)
                elif char == "+":  # +のとき
                    promote_flag = True
                else:  # 数字でないとき
                    temp_rank[temp_itr] = piece[char][0]  # 入力文字を対応する駒の整数にして入れる
                    if promote_flag:
                        temp_rank[temp_itr] += 2  # 成り駒は2を足す
                        promote_flag = False
                    temp_itr -= 1  # sfenは9→1の順なので符号の数字とは逆順になる
            self.ban[i] = temp_rank  # 1行ずつ盤面に代入する
        return self.ban

    def __enc_koma_string(self, koma, piece_string):
        num = koma[piece_string]
        if num == 0:
            return ""
        if num == 1:
            return piece_string
        return str(num) + piece_string

    def __enc_koma_BODstring(self, koma, piece_string):
        num = koma[piece_string]
        if num == 0:
            return ""
        if num == 1:
            return piece[piece_string][1]
        return piece[piece_string][1] + row[num]

    def get_sfen_koma(self):  # Boardクラスからsfen形式の駒台文字列を生成する
        temp = ""
        temp += self.__enc_koma_string(self.koma, "R")
        temp += self.__enc_koma_string(self.koma, "B")
        temp += self.__enc_koma_string(self.koma, "G")
        temp += self.__enc_koma_string(self.koma, "S")
        temp += self.__enc_koma_string(self.koma, "N")
        temp += self.__enc_koma_string(self.koma, "L")
        temp += self.__enc_koma_string(self.koma, "P")
        temp += self.__enc_koma_string(self.koma, "r")
        temp += self.__enc_koma_string(self.koma, "b")
        temp += self.__enc_koma_string(self.koma, "g")
        temp += self.__enc_koma_string(self.koma, "s")
        temp += self.__enc_koma_string(self.koma, "n")
        temp += self.__enc_koma_string(self.koma, "l")
        temp += self.__enc_koma_string(self.koma, "p")
        if len(temp) > 0:
            return temp
        else:
            return "-"

    def set_sfen_koma(self, sfen_koma):  # sfen形式の駒台文字列からBoardクラスに値をセットする
        self.__clear_koma()  # まず駒台を空にする
        if sfen_koma == "-":  # ハイフンなら持ち駒なしということ
            return
        num = 0  # 駒数
        for char in list(sfen_koma):  # 引数を1文字ずつスキャンする
            if char.isdigit():  # 数字なら
                if num == 0:  # 駒数が0なら数字を代入
                    num = int(char)
                else:  # 駒数が0でないなら2桁の数字ということ
                    num = 10 * num + int(char)
            else:  # 数字でないとき
                if num == 0:  # 駒数が0なら1が省略されていたとみなす
                    num = 1
                self.koma[char] = num  # 駒台にセットする
                num = 0  # 駒数を0にクリア

    def get_sfen(self):  # Boardクラスからsfen文字列を生成する
        return "sfen " + self.get_sfen_ban() + " " + self.get_teban() + " " + self.get_sfen_koma() + " " + self.get_count()

    def set_sfen(self, sfen):  # sfen文字列からBoardクラスに値をセットする
        sfen_list = sfen.split(" ")  # スペースで分割
        if sfen_list[0] != "sfen":
            print("先頭がsfenではありません。")
            return
        self.set_sfen_ban(sfen_list[1])
        self.set_sfen_koma(sfen_list[3])
        self.set_teban(sfen_list[2])
        self.set_count(sfen_list[4])

    # 持ち駒のチェック：pieceの駒をnum枚以上持っているか
    def has(self, piece_str, num=1):
        if self.koma[piece_str] >= num:
            return True
        return False

    # 盤面のチェックを書く
    # 盤面の駒値を返す
    def get_num(self, pos):
        return self.ban[pos[1] - 1][pos[0] - 1]

    # マス目が空かどうか
    def is_space(self, pos):
        return self.get_num(pos) == 0

    # 先手の駒か
    def is_black_piece(self, pos):
        num = self.get_num(pos)
        if num & 1:  # 後手の駒
            return False
        elif num != 0:  # 先手の駒
            return True
        return False  # 空マス

    # 後手の駒か
    def is_white_piece(self, pos):
        num = self.get_num(pos)
        if num & 1:  # 後手の駒
            return True
        return False  # 先手の駒 か 空マス

    # 成り駒か
    def is_promote(self, pos):
        if self.get_num(pos) % 4 >= 2:
            return True
        return False

    # 玉か
    def is_king(self, pos):
        num = self.get_num(pos)
        if num == 2**2 or num == 2**2 + 1:
            return True
        return False

    # 駒の先後を反転した値を返す
    def calc_reverse_num(self, num):
        if num == 0:
            raise ValueError("駒の先後反転を空マスに適用しようとしました")
        if num & 1:  # 後手の駒はmod2==1なので1を引く
            return num -1
        return num + 1  # 先手の駒はmod2==0なので1を足す

    def get_reverse_num(self, pos):
        return self.calc_reverse_num(self.get_num(pos))

    # 駒を成った値を返す
    def get_promoted_num(self, pos):
        num = self.get_num(pos)
        if num == 0:
            raise ValueError("駒の成りを空マスに適用しようとしました")
        if num == 2**2 or num == 2**2 + 1 or num == 2**14 or num == 2**14 + 1:
            raise ValueError("駒の成りを成れない駒に適用しようとしました")
        if num % 4 >= 2:
            raise ValueError("駒の成りを既に成っている駒に適用しようとしました")
        return num + 2  # 成り駒は素の駒に2を足したもの

    # 駒の素の値を返す(成り駒も成る前の値)
    def get_raw_num(self, pos):
        num = self.get_num(pos)
        if num % 4 >= 2:
            return num - 2  # 成り駒は2を引いておく
        return num

    # 駒のインデックスのタプルを返す
    def get_pos(self, p):
        return get_pos(p, self.ban)

    # 駒の符号を返す(無い場合は0、複数ある場合は1つ目)
    def get_x_pos1(self, p):
        r = conv_pos_tuple(self.get_pos(p))
        if len(r) == 0:
            return 0
        return r[0]

    # 駒の符号を返す(無い場合は0、複数ある場合はリストを返す)
    def get_x_pos2(self, p):
        r = conv_pos_tuple(self.get_pos(p))
        if len(r) == 0:
            return 0
        return r

    # 玉の位置(玉は必ずある。stay=5筋、right=右側、left=左側、middle=中段、nyugyoku=敵陣)
    def is_k_stay(self):
        return self.get_pos("k")[1][0] == 4

    def is_K_stay(self):
        return self.get_pos("K")[1][0] == 4

    def is_k_right(self):
        return self.get_pos("k")[1][0] > 4

    def is_k_left(self):
        return self.get_pos("k")[1][0] < 4

    def is_K_right(self):
        return self.get_pos("K")[1][0] < 4

    def is_K_left(self):
        return self.get_pos("K")[1][0] > 4

    def is_k_middle(self):
        y = self.get_pos("k")[0][0]
        return y >= 3 and y <= 5

    def is_K_middle(self):
        y = self.get_pos("K")[0][0]
        return y >= 3 and y <= 5

    def is_k_nyugyoku(self):
        return self.get_pos("k")[0][0] >= 6

    def is_K_nyugyoku(self):
        return self.get_pos("K")[0][0] <= 2

    # 盤上の駒の枚数をカウントする
    def count_piece(self, p, enemy_field=False):
        return len(self.ban[self.ban == piece[p][0]])

    def count_b(self):  # 先手の駒
        return len(self.ban[np.logical_and(self.ban % 2 == 0, self.ban != 0)])  # 偶数かつ0以外

    def count_w(self, bitboard=False):  # 後手の駒
        return len(self.ban[self.ban % 2 == 1])  # 奇数

    def count_b_bitboard(self, bitboard):  # 先手の駒をbitboardの場所でのみカウントする
        ban = np.where(self.ban & bitboard, self.ban, 0)
        return len(ban[np.logical_and(ban % 2 == 0, ban != 0)])

    def count_w_bitboard(self, bitboard):  # 後手の駒をbitboardの場所でのみカウントする
        ban = np.where(self.ban & bitboard, self.ban, 0)
        return len(ban[ban % 2 == 1])

    # USIプロトコルの指し手文字列を分析します。
    def __analize_move(self, move_string: str):
        def int_to_file(char: str) -> int:
            if(char == "1"):
                return 1
            elif(char == "2"):
                return 2
            elif(char == "3"):
                return 3
            elif(char == "4"):
                return 4
            elif(char == "5"):
                return 5
            elif(char == "6"):
                return 6
            elif(char == "7"):
                return 7
            elif(char == "8"):
                return 8
            elif(char == "9"):
                return 9
            else:
                raise ValueError("行は1-9で指定する必要があります：" + char)

        def char_to_rank(char: str) -> int:
            if(char == "a"):
                return 1
            elif(char == "b"):
                return 2
            elif(char == "c"):
                return 3
            elif(char == "d"):
                return 4
            elif(char == "e"):
                return 5
            elif(char == "f"):
                return 6
            elif(char == "g"):
                return 7
            elif(char == "h"):
                return 8
            elif(char == "i"):
                return 9
            else:
                raise ValueError("段はa-iで指定する必要があります：" + char)

        m_l = list(move_string)
        # 持ち駒を打つ
        if m_l[0] == "R" or m_l[0] == "B" or m_l[0] == "G" or m_l[0] == "S" or m_l[0] == "N" or m_l[0] == "L" or m_l[0] == "P":
            peace = m_l[0]
            if m_l[1] != "*":
                raise ValueError("駒を打つときの2文字目は*である必要があります")
            pos = (int_to_file(m_l[2]), char_to_rank(m_l[3]))
            return "place", peace, pos, False
        # 盤上の駒を動かす
        pos = (int_to_file(m_l[0]), char_to_rank(m_l[1]))
        moved = (int_to_file(m_l[2]), char_to_rank(m_l[3]))
        if len(m_l) >= 5 and m_l[4] == "+":
            is_promote = True
        else:
            is_promote = False
        return "move", pos, moved, is_promote

    # posの位置に動ける駒種pieceの位置リスト
    def movable_piece(self, pos, piece):
        # 盤上の同種駒の検出
        pos_list = self.get_x_pos2(piece)
        if pos_list == 0:
            return []
        if len(pos_list) >= 2 and piece != "p" and piece != "P":
            # 移動先に動ける駒を絞る
            # 移動駒種 = piece
            # 移動先 = pos
            # posの位置にpieceのBitboardを作成してmoved_posと重なるか
            filter_pos_list = []
            for moved_pos in pos_list:
                b = BitBoard()
                b.pos(moved_pos[0], moved_pos[1])
                if piece == "R" or piece == "r":
                    if b.r()[pos[1] - 1][pos[0] - 1]:
                        filter_pos_list.append(moved_pos)
                elif piece == "B" or piece == "b":
                    if b.b()[pos[1] - 1][pos[0] - 1]:
                        filter_pos_list.append(moved_pos)
                elif piece == "D" or piece == "d":
                    if b.d()[pos[1] - 1][pos[0] - 1]:
                        filter_pos_list.append(moved_pos)
                elif piece == "H" or piece == "h":
                    if b.h()[pos[1] - 1][pos[0] - 1]:
                        filter_pos_list.append(moved_pos)
                elif piece == "G":
                    if b.black_g()[pos[1] - 1][pos[0] - 1]:
                        filter_pos_list.append(moved_pos)
                elif piece == "g":
                    if b.white_g()[pos[1] - 1][pos[0] - 1]:
                        filter_pos_list.append(moved_pos)
                elif piece == "S":
                    if b.black_s()[pos[1] - 1][pos[0] - 1]:
                        filter_pos_list.append(moved_pos)
                elif piece == "s":
                    if b.white_s()[pos[1] - 1][pos[0] - 1]:
                        filter_pos_list.append(moved_pos)
                elif piece == "N":
                    if b.black_n()[pos[1] - 1][pos[0] - 1]:
                        filter_pos_list.append(moved_pos)
                elif piece == "n":
                    if b.white_n()[pos[1] - 1][pos[0] - 1]:
                        filter_pos_list.append(moved_pos)
                elif piece == "L":
                    if b.black_l()[pos[1] - 1][pos[0] - 1]:
                        filter_pos_list.append(moved_pos)
                elif piece == "l":
                    if b.white_l()[pos[1] - 1][pos[0] - 1]:
                        filter_pos_list.append(moved_pos)
            return filter_pos_list
        return []


    # USIプロトコルの指し手を与えて実行します。駒の動きの正当性のチェックはしません。
    def move(self, move_string: str, detail_kif=True):
        m = self.__analize_move(move_string)
        m_d = MoveDetail()
        m_d.type = m[0]
        m_d.pos = m[1]
        m_d.moved = m[2]
        m_d.is_promote = m[3]
        if m[0] == "move":
            # 起点の座標が自分の駒か
            if self.get_teban() == "b":
                if not self.is_black_piece(m[1]):
                    print(self.get_sfen())
                    print(f"{m[1]}→{m[2]}")
                    raise ValueError("先手の手番で先手の駒以外を動かそうとしました")
            else:
                if not self.is_white_piece(m[1]):
                    print(self.get_sfen())
                    print(f"{m[1]}→{m[2]}")
                    raise ValueError("後手の手番で後手の駒以外を動かそうとしました")
            # 終点の座標が空か
            if self.is_space(m[2]):
                get_piece = False
            # 終点の座標が相手の駒か
            elif self.get_teban() == "b" and self.is_white_piece(m[2]):
                get_piece = self.calc_reverse_num(self.get_raw_num(m[2]))
            elif self.get_teban() == "w" and self.is_black_piece(m[2]):
                get_piece = self.calc_reverse_num(self.get_raw_num(m[2]))
            else:
                print(self.get_sfen())
                print(f"{m[1]}→{m[2]}")
                raise ValueError("自分の駒がある位置に動かそうとしました")
            if self.is_king(m[2]):
                print(self.get_sfen())
                print(f"{m[1]}→{m[2]}")
                raise ValueError("玉を捕獲しようとしました")
            if get_piece:  # 駒を動かす前に取られる駒の情報を保持しておく
                m_d.get_piece_promoted = self.is_promote(m[2])
                m_d.get_piece_origin_str = dec_piecenum(self.get_raw_num(m[2]))
            # 駒を動かす
            m_d.move_piece_str = dec_piecenum(self.ban[m[1][1] - 1][m[1][0] - 1])
            # 詳細な棋譜表記生成
            if detail_kif:
                detail = column[m[2][0]] + row[m[2][1]]
                detail += piece[m_d.move_piece_str][1]
                # 直前の指し手の移動先と移動先が同じなら同にする
                if m[1] == m[2]:  # これではない (prev.m[2] == m[2]のようにする)
                    detail = "同"
                # 上下寄右左などの条件を作成する
                # 盤上の同種駒の検出
                move_piece = reverse_piece[self.ban[m[1][1] - 1][m[1][0] - 1]]
                pos_list = self.get_x_pos2(move_piece)
                if len(pos_list) >= 2 and move_piece != "p" and move_piece != "P" and move_piece != "l" and move_piece != "L":
                    movable_list = [x for x in self.movable_piece(m[2], move_piece) if x != m[1]]  # 自分自身を除くリスト
                    # 自身と他の駒が上引寄のどれかかを判定する
                    my_vertical = move_vertical(m[1], m[2], self.get_teban())
                    # その位置に動ける駒は自身だけなら修飾語は不要
                    if len(movable_list) >= 1:
                        other_vertical_list = [move_vertical(x, m[2], self.get_teban()) for x in movable_list]
                        if my_vertical not in other_vertical_list:  # 自身が上引寄のどれかで識別可能
                            detail += my_vertical
                        else:
                            # 自身と他の駒が左右直のどれかかを判定する
                            my_horizen = move_horizon(m[1], m[2], self.get_teban())
                            other_horizen_list = [move_horizon(x, m[2], self.get_teban()) for x in movable_list if x != m[1]]
                            print(my_horizen)
                            print(other_horizen_list)
                            # 金駒系かそうでないかで分岐
                            if is_metal(move_piece):
                                if my_horizen not in other_horizen_list:  # 自身が左右直のどれかで識別可能
                                    detail += my_horizen
                                elif my_horizen == "直":  # 直は1つしかない
                                    detail += "直"
                                else:
                                    detail += my_horizen
                                    detail += my_vertical
                            else:
                                # 左右で確定する
                                if my_horizen == "左" or my_horizen == "右":
                                    detail += my_horizen
                                else:
                                    if other_horizen_list[0] == "左":
                                        detail += "右"
                                    else:
                                        detail += "左"

                # 不成の条件を作成
                # 既に成り駒ではなくて移動元または移動先が敵陣
                if not self.is_promote(m[1]):
                    if self.get_teban() == "b":
                        if m[1][1] <= 3 or m[2][1] <= 3:
                            if m[3]:
                                detail += "成"
                            else:
                                detail += "不成"
                    else:
                        if m[1][1] >= 7 or m[2][1] >= 7:
                            if m[3]:
                                detail += "成"
                            else:
                                detail += "不成"
            if m[3]:  # 駒を成る場合
                self.ban[m[2][1] - 1][m[2][0] - 1] = self.get_promoted_num(m[1])
            else:  # 通常の場合
                self.ban[m[2][1] - 1][m[2][0] - 1] = self.ban[m[1][1] - 1][m[1][0] - 1]
            self.ban[m[1][1] - 1][m[1][0] - 1] = 0
            # 駒を取得する
            if get_piece:
                m_d.get_piece_str = dec_piecenum(get_piece)
                self.koma[m_d.get_piece_str] += 1

        elif m[0] == "place":
            # 指し手は駒種しか入っていないので後手番なら小文字にする
            if self.get_teban() == "w":
                p = m[1].lower()
            else:
                p = m[1]
            # 駒が打てるかのチェック
            if not self.has(p):
                raise ValueError("指定された駒を持っていません")
            if not self.is_space(m[2]):
                raise ValueError("駒を打つ場所が空ではありません")
            movable_list = [x for x in self.movable_piece(m[2], p)]  # 駒を打つ場所に同種の駒が動けるか
            self.koma[p] -= 1  # 駒台から駒を1つ減らす
            self.ban[m[2][1] - 1][m[2][0] - 1] = piece[p][0]  # 盤面に駒を置く
            m_d.move_piece_str = p
            # 詳細な棋譜表記生成
            if detail_kif:
                detail = column[m[2][0]] + row[m[2][1]]
                detail += piece[p][1]
                if len(movable_list) >= 1: # 打が入る条件を作成する
                    detail += "打"
        else:
            raise ValueError("想定されたmoveではありません")
        self.set_teban("r")  # 指し手が進んだので手番変更
        self.inc_count()  # 手数カウントを1増やしておく
        # 分析した指し手、取得した駒、詳細な棋譜表記のクラスを返す
        if detail_kif:
            m_d.detail = detail
        return m_d

    def __plot_common(self, plt):
        one = np.ones(9)
        range = np.arange(-9.0, 0.0, 0.1)
        plt.figure(figsize=(7, 7))
        plt.xlim((-10.5, 1.5))
        plt.ylim((-10.5, 1.5))
        plt.tick_params(labelbottom='off')
        plt.tick_params(labelleft='off')

        plt.plot([-9.0, 0.0], [-9.0, -9.0], color="#000000")
        plt.plot([-9.0, 0.0], [-8.0, -8.0], color="#000000")
        plt.plot([-9.0, 0.0], [-7.0, -7.0], color="#000000")
        plt.plot([-9.0, 0.0], [-6.0, -6.0], color="#000000")
        plt.plot([-9.0, 0.0], [-5.0, -5.0], color="#000000")
        plt.plot([-9.0, 0.0], [-4.0, -4.0], color="#000000")
        plt.plot([-9.0, 0.0], [-3.0, -3.0], color="#000000")
        plt.plot([-9.0, 0.0], [-2.0, -2.0], color="#000000")
        plt.plot([-9.0, 0.0], [-1.0, -1.0], color="#000000")
        plt.plot([-9.0, 0.0], [-0.0, -0.0], color="#000000")

        plt.plot([-9.0, -9.0], [-9.0, 0.0], color="#000000")
        plt.plot([-8.0, -8.0], [-9.0, 0.0], color="#000000")
        plt.plot([-7.0, -7.0], [-9.0, 0.0], color="#000000")
        plt.plot([-6.0, -6.0], [-9.0, 0.0], color="#000000")
        plt.plot([-5.0, -5.0], [-9.0, 0.0], color="#000000")
        plt.plot([-4.0, -4.0], [-9.0, 0.0], color="#000000")
        plt.plot([-3.0, -3.0], [-9.0, 0.0], color="#000000")
        plt.plot([-2.0, -2.0], [-9.0, 0.0], color="#000000")
        plt.plot([-1.0, -1.0], [-9.0, 0.0], color="#000000")
        plt.plot([-0.0, -0.0], [-9.0, 0.0], color="#000000")

    def __plt_text(self, x, y, char, rot=0):
        plt.text(x, y, char, fontsize = 24, rotation = rot, fontproperties=fp, ha='center', va='center')

    def __plot_ban(self, plt, kato123=False):
        if kato123:  # ひふみんアイでの反転した盤面を作る
            ban = self.ban[::-1]
            for i, rank in enumerate(ban):
                ban[i] = rank[::-1]
        else:
            ban = self.ban
        offset_x = -0.9
        offset_y = -0.8
        for i, rank in enumerate(ban):  # 1行ずつ処理する
            for j, pos in enumerate(rank):
                if pos != 0:  # 空マス以外なら駒の文字を出力する
                    char = piece[reverse_piece[pos]][1]
                    if kato123:
                        if pos % 2:
                            self.__plt_text(-0.50 - j, -0.50 - i, char)
                        else:
                            self.__plt_text(-0.60 - j, - 0.30 - i, char, 180)
                    else:
                        if pos % 2: # 後手の駒
                            self.__plt_text(-0.60 - j, - 0.30 - i, char, 180)
                        else: # 先手の駒
                            self.__plt_text(-0.50 - j, -0.50 - i, char)

    def __get_koma_b_string(self, koma):
        temp = ""
        temp += self.__enc_koma_BODstring(koma, "R")
        temp += self.__enc_koma_BODstring(koma, "B")
        temp += self.__enc_koma_BODstring(koma, "G")
        temp += self.__enc_koma_BODstring(koma, "S")
        temp += self.__enc_koma_BODstring(koma, "N")
        temp += self.__enc_koma_BODstring(koma, "L")
        temp += self.__enc_koma_BODstring(koma, "P")
        return temp

    def __get_koma_w_string(self, koma):
        temp = ""
        temp += self.__enc_koma_BODstring(koma, "r")
        temp += self.__enc_koma_BODstring(koma, "b")
        temp += self.__enc_koma_BODstring(koma, "g")
        temp += self.__enc_koma_BODstring(koma, "s")
        temp += self.__enc_koma_BODstring(koma, "n")
        temp += self.__enc_koma_BODstring(koma, "l")
        temp += self.__enc_koma_BODstring(koma, "p")
        return temp

    def __plot_koma(self, plt, kato123=False):
        if kato123:  # ひふみんアイでは駒台が逆になる
            plt.text(0.05, -0.6, "☖", fontsize = 24, rotation = 0, fontproperties=fp)
            plt.text(-10.02, -8.7, "☗", fontsize = 24, rotation = 180, fontproperties=fp)
            for i, char in enumerate(list(self.__get_koma_b_string(self.koma))):
                plt.text(-9.95, -8.0 + 0.7 * i, char, fontsize = 24, rotation = 180, fontproperties=fp)
            for i, char in enumerate(list(self.__get_koma_w_string(self.koma))):
                plt.text(0.05, -1.4 - 0.7 * i, char, fontsize = 24, rotation = 0, fontproperties=fp)
        else:
            plt.text(0.05, -0.6, "☗", fontsize = 24, rotation = 0, fontproperties=fp)
            plt.text(-10.02, -8.7, "☖", fontsize = 24, rotation = 180, fontproperties=fp)
            for i, char in enumerate(list(self.__get_koma_b_string(self.koma))):
                plt.text(0.05, -1.4 - 0.7 * i, char, fontsize = 24, rotation = 0, fontproperties=fp)
            for i, char in enumerate(list(self.__get_koma_w_string(self.koma))):
                plt.text(-9.95, -8.0 + 0.7 * i, char, fontsize = 24, rotation = 180, fontproperties=fp)

    def plot(self, pre=False):
        self.__plot_common(plt)
        self.__plot_ban(plt)
        self.__plot_koma(plt)
        if pre:
            plt.fill_between((-pre[0], -pre[0] + 1), -pre[1], -pre[1] + 1, color='#97fef1')
        plt.show()

    def plot123(self, pre=False):  # ひふみんアイ
        self.__plot_common(plt)
        self.__plot_ban(plt, True)
        self.__plot_koma(plt, True)
        if pre:
            plt.fill_between((pre[0] - 10, pre[0] - 9), pre[1] - 10, pre[1] - 9, color='#97fef1')
        plt.show()
