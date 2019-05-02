import * as React from 'react'
import * as ReactDOM from 'react-dom'
import { Provider } from 'react-redux'
import { createHashHistory } from 'history'
import Container from './form'
import { createStore, applyMiddleware } from 'redux'
import createSagaMiddleware from 'redux-saga'
import reducer from './reducer'
import rootSaga from './sagas'

// Saga ミドルウェアを作成する
const sagaMiddleware = createSagaMiddleware()
// Store にマウントする
const store = createStore(reducer, applyMiddleware(sagaMiddleware))
// Saga を起動する
sagaMiddleware.run(rootSaga)
ReactDOM.render(
  <Provider store={store}>
    <Container />
  </Provider>,
  document.getElementById('root')
)
