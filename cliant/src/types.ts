import _ from 'lodash'

export interface Move {
  move: string
  movePretty: string
  next: string
  value: number
  movedSfen?: string
}

const initMoveList = [
  {
    move: '',
    next: '',
    value: 0,
    movePretty: ''
  }
]

export class Node {
  sfen: string // 自身のsfen
  moveList: Move[] // 定跡の指し手候補
  value: number // 自身の評価値
  prev: string // 直前の指し手
  prevPretty: string // 直前の指し手のpretty
  depth: number // rootからの深さ
  childNum: number // 自身が親の子要素の何番目か
  children: Node[] // 子要素
  constructor(
    sfen: string,
    childNum: number,
    depth: number,
    value: number,
    prev: string,
    prevPretty: string = ''
  ) {
    this.sfen = sfen
    this.moveList = initMoveList
    this.value = value
    this.prev = prev
    this.prevPretty = prevPretty
    this.depth = depth
    this.childNum = childNum
    this.children = []
  }
  push(child: Node) {
    this.children.push(child)
  }
  insert(insertNode: InsertNode, depth: number = 0) {
    const childNum = insertNode.position[0]
    if (insertNode.position.length == 0) {
      // position配列の長さが0ならroot
      this.sfen = insertNode.node.sfen
      this.moveList = _.cloneDeep(insertNode.node.moveList)
      this.value = insertNode.node.value
      this.prev = insertNode.node.prev
      this.prevPretty = insertNode.node.prevPretty
      this.depth = insertNode.node.depth
      this.childNum = insertNode.node.childNum
    } else if (insertNode.position.length == 1) {
      // position配列の長さが1ならその階層に挿入する
      let node = insertNode.node
      node.childNum = childNum
      node.depth = depth + 1
      // 配列を走査して適切なchildNumの位置に挿入する
      let i = 0
      for (i = 0; i < this.children.length; i++) {
        // 自身のchildNumより大きければそこが挿入位置
        if (this.children[i].childNum > node.childNum) {
          break
        }
      }
      this.children.splice(i, 0, node)
    } else {
      // position配列の長さが2以上なら階層を降りてposition配列を1つ短くする
      insertNode.position.shift() // 先頭を削除
      this.children[childNum].insert(insertNode, depth + 1)
    }
  }
}

// ツリーにノードを挿入する
export interface InsertNode {
  node: Node // 挿入するノード
  position: number[] // ツリーでの挿入位置
}

export interface RequestSfenObj {
  sfen: string
  treePosition: number[]
  prev: string
  prevPretty: string
  parentValue: number
}

// sfenをキーとして move: sfen[]を値とするmap
export interface Book extends ApiResponse {
  sfen: string
  moveList: Move[]
}
export interface BookState {
  readonly data: any
  readonly tree?: Node
}
export type ApiResponse = Record<string, any>

export const enum BookActionTypes {
  REQUEST_SFEN_BOOK = '@@book/REQUEST_SFEN_BOOK',
  SUCCESS_SFEN_BOOK = '@@book/SUCCESS_SFEN_BOOK',
  REQUEST_MOVED_SFEN = '@@book/REQUEST_MOVED_SFEN',
  SUCCESS_MOVED_SFEN = '@@book/SUCCESS_MOVED_SFEN',

  SET_ROOT_SFEN = '@@book/SET_ROOT_SFEN',
  INSERT_TREE = '@@book/INSERT_TREE'
}
