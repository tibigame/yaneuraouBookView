import { Reducer } from 'redux'
import { BookState, BookActionTypes, Node } from './types'
import _ from 'lodash'

export const initialState: BookState = {
  data: {},
  tree: new Node('', 0, 0, 0, '')
}

const reducer: Reducer<BookState> = (state = initialState, action) => {
  switch (action.type) {
    case BookActionTypes.REQUEST_SFEN_BOOK: {
      return { ...state }
    }

    case BookActionTypes.SUCCESS_SFEN_BOOK: {
      // 取得したsfenでの情報をマージしていく
      const newData = Object.assign(_.cloneDeep(state.data), action.payload)
      return { ...state, data: newData }
    }
    case BookActionTypes.REQUEST_MOVED_SFEN: {
      return { ...state }
    }

    // rootNodeをクリアして新規作成する
    case BookActionTypes.SET_ROOT_SFEN: {
      const tree = new Node(action.payload, 0, 0, 0, '')
      return { ...state, tree: tree }
    }

    case BookActionTypes.INSERT_TREE: {
      let newTree = _.cloneDeep(state.tree)
      if (typeof newTree != 'undefined') {
        newTree.insert(action.payload)
      }
      return { ...state, tree: newTree }
    }

    case BookActionTypes.SUCCESS_MOVED_SFEN: {
      return { ...state, movedSfen: action.payload }
    }
    default: {
      return state
    }
  }
}
export default reducer
