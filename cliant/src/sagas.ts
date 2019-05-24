import { all, call, fork, put, takeEvery } from 'redux-saga/effects'
import { BookActionTypes, Node, RequestSfenObj, InsertNode } from './types'
import { requestSfenBook, successMovedSfen, insertNode } from './actions'
import { callApi } from './api'
import _ from 'lodash'

const MAX_DEPTH = 40 // 最大のrootからの探索深さ
const API_LIMIT = 200 // 最大node数
let k = 0

// 指し手の上位を優先的に探索するための値
const LIMIT_SEARCH_VALUE = 60
const searchValue = (treePosition: number[]) => {
  let value = 0
  treePosition.forEach((e: number) => {
    if (e == 0) {
      value += 1
    } else if (e == 1) {
      value += 3
    } else if (e == 2) {
      value += 6
    } else if (e == 3) {
      value += 10
    } else {
      value += 15
    }
  })
  return value
}

function* handleSfenBook(action: any) {
  const sfen = action.payload['sfen']
  const res = yield call(callApi, 'post', '/book', { sfen: sfen })
  const treePosition = action.payload['treePosition']
  // 定跡があれば最善手の評価値を、なければ親の評価値を(次の手番なので反転して)与える
  const value = res && res[0].move != '' ? res[0].value : -action.payload['parentValue']
  let node = new Node(
    sfen,
    treePosition[treePosition.length - 1],
    treePosition.length,
    value,
    'prev'
  )
  node.moveList = res
  node.prev = action.payload['prev']
  node.prevPretty = action.payload['prevPretty']
  const insertNode_: InsertNode = {
    node: node,
    position: treePosition
  }
  // レスポンスをツリーに反映
  yield put(insertNode(_.cloneDeep(insertNode_)))
  if (res[0].move == '') {
    return // 定跡がないのでEND
  }
  // より深く探索をするかどうか
  if (treePosition.length <= MAX_DEPTH) {
    for (let i = 0; i < node.moveList.length; i++) {
      const prev = node.moveList[i].move
      const parentValue = node.moveList[i].value
      const sfen = node.moveList[i].movedSfen
      let position = _.cloneDeep(treePosition)
      position.push(i)
      const requestSfenObj: RequestSfenObj = {
        sfen: sfen ? sfen : '',
        treePosition: position,
        prev: prev,
        prevPretty: node.moveList[i].movePretty,
        parentValue: parentValue
      }
      k++
      if (k > API_LIMIT) {
        return
      }
      if (searchValue(treePosition) > LIMIT_SEARCH_VALUE) {
        break
      }
      yield put(requestSfenBook(requestSfenObj))
    }
  }
}

function* handleMovedSfen(action: any) {
  const res = yield call(callApi, 'post', '/move', action.payload)
  console.log('handleMovedSfen')
  console.log(res)
  yield put(successMovedSfen(res))
}

function* handleSetRootSfen(action: any) {
  const sfen = action.payload.sfen
  const requestSfenObj: RequestSfenObj = {
    sfen: sfen,
    treePosition: [],
    prev: '',
    prevPretty: '',
    parentValue: 0
  }
  yield put(requestSfenBook(requestSfenObj))
}

function* watchSfenBook() {
  yield takeEvery(BookActionTypes.REQUEST_SFEN_BOOK, handleSfenBook)
}

function* watchMovedSfen() {
  yield takeEvery(BookActionTypes.REQUEST_MOVED_SFEN, handleMovedSfen)
}

function* watchSetRootSfen() {
  yield takeEvery(BookActionTypes.SET_ROOT_SFEN, handleSetRootSfen)
}

export default function* rootSaga() {
  yield all([fork(watchSfenBook), fork(watchMovedSfen), fork(watchSetRootSfen)])
}
