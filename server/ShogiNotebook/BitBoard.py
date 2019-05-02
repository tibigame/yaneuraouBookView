import numpy as np


# 基本のビット位置操作をしてndarrayを返す
def up(s, x: int):  # x上にずらす
    s[:(9 - x)] = s[x:]
    return s


def down(s, x: int):  # x下にずらす
    s[x:] = s[:(9 - x)]
    return s


def right(s, x: int):  # x右にずらす
    s[:, x:] = s[:, :(9 - x)]
    return s


def left(s, x: int):  # x左にずらす
    s[:, :(9 - x)] = s[:, x:]
    return s


def up_right(s, x: int):  # x右上にずらす
    return up(right(s, x), x)


def up_left(s, x: int):  # x左上にずらす
    return up(left(s, x), x)


def down_right(s, x: int):  # x右下にずらす
    return down(right(s, x), x)


def down_left(s, x: int):  # x左下にずらす
    return down(left(s, x), x)


B_0 = np.zeros([9, 9], "bool")
B_1 = np.invert(B_0)


class BitBoard:
    def __init__(self):
        self.a = None
        self.FALSE()

    def FALSE(self):
        self.a = np.zeros([9, 9], "bool")  # 全てFalseで初期化

    def TRUE(self):
        self.a = np.ones([9, 9], "bool")  # 全てTrueで初期化

    def NOT(self):  # 全てビット反転する
        self.a = ~self.a

    def pos(self, x, y):  # x, yにTrueをセットする
        self.a[y - 1][x - 1] = True

    def rank(self, rank):  # 1行がTrueのndarrayを返す
        temp = self.a.copy()
        temp[rank - 1, :] = np.ones([1, 9], "bool")
        return temp

    def file(self, file):  # 1列がTrueのndarrayを返す
        temp = self.a.copy()
        temp[:, file - 1] = np.ones([1, 9], "bool")
        return temp

    def set_rank_list(self, rank_list):  # 横の行 (1-9のリスト)
        for r in rank_list:
            self.a[r - 1, :] = np.ones([1, 9], "bool")

    def set_file_list(self, file_list):  # 縦の行 (1-9のリスト)
        for f in file_list:
            self.a[:, f - 1] = np.ones([1, 9], "bool")

    # 基本のビット位置操作
    def up(self, x: int):  # x上にずらす
        self.a = up(x)

    def down(self, x: int):  # x下にずらす
        self.a = down(x)

    def right(self, x: int):  # x右にずらす
        self.a = right(x)

    def left(self, x: int):  # x左にずらす
        self.a = left(x)

    def black_p(self):  # 先手の歩の効きを返す
        return up(self.a, 1)

    def white_p(self):  # 後手の歩の効きを返す
        return down(self.a, 1)

    def missile(self, func):  # 飛び道具の効きを返す
        # 1つずらしてマージ、2つずらしてマージ、4つずらしてマージ、1つずらすを順にする
        temp1 = func(self.a.copy(), 1)
        temp1m = self.a + temp1
        temp2 = func(temp1m.copy(), 2)
        temp2m = temp1m.copy() + temp2
        temp4 = func(temp2m.copy(), 4)
        temp4m = temp2m.copy() + temp4
        return func(temp4m, 1)

    def black_l(self):  # 先手の香の効きを返す
        return self.missile(up)

    def white_l(self):  # 後手の香の効きを返す
        return self.missile(down)

    def r(self):  # 飛の効きを返す(先後同じ)
        temp_up = self.missile(up)
        temp_down = self.missile(down)
        temp_right = self.missile(right)
        temp_left = self.missile(left)
        return temp_up + temp_down + temp_right + temp_left

    def b(self):  # 角の効きを返す(先後同じ)
        temp_up_right = self.missile(up_right)
        temp_up_left = self.missile(up_left)
        temp_down_right = self.missile(down_right)
        temp_down_left = self.missile(down_left)
        return temp_up_right + temp_up_left + temp_down_right + temp_down_left

    def d(self):  # 龍の効きを返す(先後同じ)
        temp_up_right = up_right(self.a.copy(), 1)
        temp_up_left = up_left(self.a.copy(), 1)
        temp_down_right = down_right(self.a.copy(), 1)
        temp_down_left = down_left(self.a.copy(), 1)
        return self.r() + temp_up_right + temp_up_left + temp_down_right + temp_down_left

    def h(self):  # 馬の効きを返す(先後同じ)
        temp_up = up(self.a.copy(), 1)
        temp_down = down(self.a.copy(), 1)
        temp_right = right(self.a.copy(), 1)
        temp_left = left(self.a.copy(), 1)
        return self.b() + temp_up + temp_down + temp_right + temp_left

    def black_g(self):  # 先手の金の効きを返す
        temp_up = up(self.a.copy(), 1)
        temp_up_right = up_right(self.a.copy(), 1)
        temp_up_left = up_left(self.a.copy(), 1)
        temp_down = down(self.a.copy(), 1)
        temp_right = right(self.a.copy(), 1)
        temp_left = left(self.a.copy(), 1)
        return temp_up + temp_up_right + temp_up_left + temp_down + temp_right + temp_left

    def white_g(self):  # 後手の金の効きを返す
        temp_up = up(self.a.copy(), 1)
        temp_down = down(self.a.copy(), 1)
        temp_down_right = down_right(self.a.copy(), 1)
        temp_down_left = down_left(self.a.copy(), 1)
        temp_right = right(self.a.copy(), 1)
        temp_left = left(self.a.copy(), 1)
        return temp_up + temp_down + temp_down_right + temp_down_left + temp_right + temp_left

    def black_s(self):  # 先手の銀の効きを返す
        temp_up = up(self.a.copy(), 1)
        temp_up_right = up_right(self.a.copy(), 1)
        temp_up_left = up_left(self.a.copy(), 1)
        temp_down_right = down_right(self.a.copy(), 1)
        temp_down_left = down_left(self.a.copy(), 1)
        return temp_up + temp_up_right + temp_up_left + temp_down_right + temp_down_left

    def white_s(self):  # 後手の銀の効きを返す
        temp_down = down(self.a.copy(), 1)
        temp_down_right = down_right(self.a.copy(), 1)
        temp_down_left = down_left(self.a.copy(), 1)
        temp_up_right = up_right(self.a.copy(), 1)
        temp_up_left = up_left(self.a.copy(), 1)
        return temp_down + temp_down_right + temp_down_left + temp_up_right + temp_up_left

    def black_n(self):  # 先手の桂の効きを返す
        temp_up2 = up(self.a.copy(), 2)
        return right(temp_up2.copy(), 1) + left(temp_up2, 1)

    def white_n(self):  # 後手の桂の効きを返す
        temp_doown2 = down(self.a.copy(), 2)
        return right(temp_doown2.copy(), 1) + left(temp_doown2, 1)

    def king9(self, pos):  # 近傍9マス
        x, y = pos
        file = self.file(x)  # まず与えられた列
        if x >= 2:  # 2以上ならば左の列も追加
            file = file | self.file(x - 1)
        if x <= 8:  # 8以下ならば右の列も追加
            file = file | self.file(x + 1)
        rank = self.rank(y)  # まず与えられた行
        if y >= 2:  # 2以上ならば上の行も追加
            rank = rank | self.rank(y - 1)
        if y <= 8:  # 8以下ならば下の行も追加
            rank = rank | self.rank(y + 1)
        return file & rank  # 行と列のANDをとる

    def king25(self, pos):  # 近傍25マス
        x, y = pos
        file = self.file(x)  # まず与えられた列
        if x >= 2:  # 2以上ならば左の列も追加
            file = file | self.file(x - 1)
        if x >= 3:  # 3以上ならば左の列も追加
            file = file | self.file(x - 2)
        if x <= 8:  # 8以下ならば右の列も追加
            file = file | self.file(x + 1)
        if x <= 7:  # 7以下ならば右の列も追加
            file = file | self.file(x + 2)
        rank = self.rank(y)  # まず与えられた行
        if y >= 2:  # 2以上ならば上の行も追加
            rank = rank | self.rank(y - 1)
        if y >= 3:  # 3以上ならば上の行も追加
            rank = rank | self.rank(y - 2)
        if y <= 8:  # 8以下ならば下の行も追加
            rank = rank | self.rank(y + 1)
        if y <= 7:  # 8以下ならば下の行も追加
            rank = rank | self.rank(y + 2)
        return file & rank  # 行と列のANDをとる

    def merge_ndarray(self, y):  # orを取ってndarrayを返す
        x = self.a.copy()
        return x + y.a

    def __add__(self, y):
        return self.merge_ndarray(y)

    def count0(self) -> int:  # Trueのマスをカウント
        return len(np.where(self.a == B_0)[0])

    def count1(self) -> int:  # Falseのマスをカウント
        return 81 - self.count0()


# 後手は+1 成りは+2にする
piece = {
    "k": [4 + 1, "王"],
    "r": [8 + 1, "飛"],
    "+r": [8 + 3, "龍"],
    "b": [12 + 1, "角"],
    "+b": [12 + 3, "馬"],
    "g": [16 + 1, "金"],
    "s": [20 + 1, "銀"],
    "+s": [20 + 3, "全"],
    "n": [24 + 1, "桂"],
    "+n": [24 + 3, "圭"],
    "l": [28 + 1, "香"],
    "+l": [28 + 3, "杏"],
    "p": [32 + 1, "歩"],
    "+p": [32 + 3, "と"],
    "K": [4, "玉"],
    "R": [8, "飛"],
    "+R": [8 + 2, "龍"],
    "B": [12, "角"],
    "+B": [12 + 2, "馬"],
    "G": [16, "金"],
    "S": [20, "銀"],
    "+S": [20 + 2, "全"],
    "N": [24, "桂"],
    "+N": [24 + 2, "圭"],
    "L": [28, "香"],
    "+L": [28 + 2, "杏"],
    "P": [32, "歩"],
    "+P": [32 + 2, "と"]
}
reverse_piece = {
    4 + 1: "k",
    8 + 1: "r",
    8 + 3: "+r",
    12 + 1: "b",
    12 + 3: "+b",
    16 + 1: "g",
    20 + 1: "s",
    20 + 3: "+s",
    24 + 1: "n",
    24 + 3: "+n",
    28 + 1: "l",
    28 + 3: "+l",
    32 + 1: "p",
    32 + 3: "+p",
    4: "K",
    8: "R",
    8 + 2: "+R",
    12: "B",
    12 + 2: "+B",
    16: "G",
    20: "S",
    20 + 2: "+S",
    24: "N",
    24 + 2: "+N",
    28: "L",
    28 + 2: "+L",
    32: "P",
    32 + 2: "+P"
}

B_one = np.ones([9, 9], "uint8")  # 全て1

RANK = np.invert(np.zeros([1, 9], "uint8"))
FILE = np.invert(np.zeros([9, 1], "uint8"))

# 先手陣、後手陣
B_BLACK = np.zeros([9, 9], "uint8")
B_BLACK[6, :] = RANK
B_BLACK[7, :] = RANK
B_BLACK[8, :] = RANK
B_WHITE = np.zeros([9, 9], "uint8")
B_WHITE[0, :] = RANK
B_WHITE[1, :] = RANK
B_WHITE[2, :] = RANK

B_k = B_one * piece["k"][0]
B_r = B_one * piece["r"][0]
B_xr = B_one * piece["+r"][0]
B_b = B_one * piece["b"][0]
B_xb = B_one * piece["+b"][0]
B_g = B_one * piece["g"][0]
B_s = B_one * piece["s"][0]
B_xs = B_one * piece["+s"][0]
B_n = B_one * piece["n"][0]
B_xn = B_one * piece["+n"][0]
B_l = B_one * piece["l"][0]
B_xl = B_one * piece["+l"][0]
B_p = B_one * piece["p"][0]
B_xp = B_one * piece["+p"][0]
B_K = B_one * piece["K"][0]
B_R = B_one * piece["R"][0]
B_xR = B_one * piece["+R"][0]
B_B = B_one * piece["B"][0]
B_xB = B_one * piece["+B"][0]
B_G = B_one * piece["G"][0]
B_S = B_one * piece["S"][0]
B_xS = B_one * piece["+S"][0]
B_N = B_one * piece["N"][0]
B_xN = B_one * piece["+N"][0]
B_L = B_one * piece["L"][0]
B_xL = B_one * piece["+L"][0]
B_P = B_one * piece["P"][0]
B_xP = B_one * piece["+P"][0]


def get_pos(p, ban):  # 駒のインデックスのタプルを返す
    if p == "k":
        return np.where(B_k == ban)
    elif p == "r":
        return np.where(B_r == ban)
    elif p == "+r":
        return np.where(B_xr == ban)
    elif p == "b":
        return np.where(B_b == ban)
    elif p == "+b":
        return np.where(B_xb == ban)
    elif p == "g":
        return np.where(B_g == ban)
    elif p == "s":
        return np.where(B_s == ban)
    elif p == "+s":
        return np.where(B_xs == ban)
    elif p == "n":
        return np.where(B_n == ban)
    elif p == "+n":
        return np.where(B_xn == ban)
    elif p == "l":
        return np.where(B_l == ban)
    elif p == "+l":
        return np.where(B_xl == ban)
    elif p == "p":
        return np.where(B_p == ban)
    elif p == "+p":
        return np.where(B_xp == ban)
    elif p == "K":
        return np.where(B_K == ban)
    elif p == "R":
        return np.where(B_R == ban)
    elif p == "+R":
        return np.where(B_xR == ban)
    elif p == "B":
        return np.where(B_B == ban)
    elif p == "+B":
        return np.where(B_xB == ban)
    elif p == "G":
        return np.where(B_G == ban)
    elif p == "S":
        return np.where(B_S == ban)
    elif p == "+S":
        return np.where(B_xS == ban)
    elif p == "N":
        return np.where(B_N == ban)
    elif p == "+N":
        return np.where(B_xN == ban)
    elif p == "L":
        return np.where(B_L == ban)
    elif p == "+L":
        return np.where(B_xL == ban)
    elif p == "P":
        return np.where(B_P == ban)
    elif p == "+P":
        return np.where(B_xP == ban)
    else:
        raise ValueError("そのような駒はありません")
