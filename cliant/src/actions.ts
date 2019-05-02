import { action, createAction } from 'typesafe-actions'
import { BookActionTypes, InsertNode, RequestSfenObj } from './types'

export const successSfenBook = (data: any) => action(BookActionTypes.SUCCESS_SFEN_BOOK, data)
export const successMovedSfen = (sfen: string) => action(BookActionTypes.SUCCESS_MOVED_SFEN, sfen)

export const requestSfenBook = createAction(
  BookActionTypes.REQUEST_SFEN_BOOK,
  resolve => (requestSfenObj: RequestSfenObj) =>
    resolve({
      sfen: requestSfenObj.sfen,
      treePosition: requestSfenObj.treePosition,
      prev: requestSfenObj.prev,
      prevPretty: requestSfenObj.prevPretty,
      parentValue: requestSfenObj.parentValue
    })
)
export const requestMovedSfen = createAction(
  BookActionTypes.REQUEST_MOVED_SFEN,
  resolve => (data: any) => resolve({ data: data })
)

export const setRootSfen = createAction(BookActionTypes.SET_ROOT_SFEN, resolve => (sfen: string) =>
  resolve({ sfen: sfen })
)
export const insertNode = createAction(
  BookActionTypes.INSERT_TREE,
  resolve => (payload: InsertNode) => resolve(payload)
)
