from flask import Flask, jsonify, abort, make_response, request
from flask_cors import CORS
from parse import make_dict, move_json
from ShogiNotebook.Board import Board

book_dict = make_dict()
api = Flask(__name__)
CORS(api)

def convert_param(url: str):
    s = url.replace('_', ' ')
    s = s.replace('!', '/')
    return s

@api.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# sfenを与えると対応する指し手リストを返す
@api.route('/book', methods=['POST'])
def book():
    sfen_ = request.json['sfen']
    sfen_ = " ".join(sfen_.split()[:-1])
    if sfen_ not in book_dict:  # 存在しないsfenのときはクライアントがエラーにならないように適当に返す
        return make_response(jsonify([{
        "move": '',
        "next": '',
        "value": 0,
        "movedSfen": ''
    }]))
    result = []
    # 定跡ファイルで評価値順にソートされていることを前提にしている
    for json in [move_json(move) for move in book_dict[sfen_]]:
        result.append(json)
    return make_response(jsonify(result))

@api.route('/get/<sfen>', methods=['GET'])
def get(sfen=None):
    sfen_ = convert_param(sfen)
    sfen_ = " ".join(sfen_.split()[:-1])
    result = []
    # 定跡ファイルで評価値順にソートされていることを前提にしている
    for i, json in enumerate([move_json(move) for move in book_dict[sfen_]]):
        result.append(json)
    return make_response(jsonify(result))

# sfenとmoveを与えると指した後のsfenを返す (不正な指し手は想定しない)
@api.route('/move', methods=['POST'])
def move():
    body = request.json['data']
    sfen = body['sfen']
    move = body['move']
    board = Board(sfen)
    board.move(move)
    result = { 'sfen': board.get_sfen() }
    return make_response(jsonify(result))

@api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    api.run(host='0.0.0.0', port=3000)
