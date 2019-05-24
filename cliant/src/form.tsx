import * as React from 'react'
import { useState, useEffect, useMemo } from 'react'
import { connect } from 'react-redux'
import { Dispatch } from 'redux'
import { BookState, Node } from './types'
import { setRootSfen } from './actions'
import Board from './board'
import './form.scss'

interface PropsFromDispatch {
  setRootSfen: typeof setRootSfen
}

interface DataProps {
  tree?: Node
}

type AllProps = PropsFromDispatch & BookState

const flexStyle = {
  display: 'flex'
}

const headerStyle = {
  height: '1.2rem',
  width: '100%',
  background: '#9fe0cd'
}

let nodeViewIndex = 0

interface NodeViewProps {
  node?: Node
  func: any
}
const NodeView: React.FC<NodeViewProps> = ({ node, func }) => {
  const [isOpen, setIsOpen] = useState(true)
  const [rootChangeFlag, setRootChangeFlag] = useState(false)
  if (typeof node === 'undefined') {
    return <div />
  } else if (node.sfen.length == 0) {
    return <div />
  }
  nodeViewIndex++
  const sfen = typeof node.sfen === 'string' ? node.sfen : node.sfen['sfen']
  let blackValue = 0
  if (sfen.length > 5 && sfen.split(' ')[2]) {
    blackValue = sfen.split(' ')[2] == 'b' ? node.value : -node.value
  }
  let prevPretty = ''
  if (node.prevPretty) {
    prevPretty = node.prevPretty
  }
  const parent = (
    <div className="nodeParent">
      <div onClick={() => setRootChangeFlag(!rootChangeFlag)}>
        {Board(sfen, blackValue, node.moveList, node.prev, prevPretty)}
      </div>
      {rootChangeFlag ? (
        <div>
          <div>{sfen}</div>
          <div
            onClick={() => {
              func(sfen)
            }}
          >
            [このノードをルートにする]
          </div>
        </div>
      ) : (
        <div />
      )}
    </div>
  )

  if (!isOpen) {
    return (
      <div key={nodeViewIndex} className="nodeView">
        {parent}
        <div style={flexStyle} className="nodeChildren">
          <div style={headerStyle} className="nodeHeader" onClick={() => setIsOpen(true)}>
            ▶
          </div>
        </div>
      </div>
    )
  }
  const children = node.children.map((child: Node, index: number, array: Node[]) => {
    return (
      <div>
        <NodeView node={child} func={func} />
      </div>
    )
  })
  if (children.length == 0) {
    return (
      <div key={nodeViewIndex} className="nodeView">
        {parent}
      </div>
    )
  }
  return (
    <div key={nodeViewIndex} className="nodeView">
      {parent}
      <div>
        <div style={headerStyle} onClick={() => setIsOpen(false)} />
        <div style={flexStyle} className="nodeChildren">
          {children}
        </div>
      </div>
    </div>
  )
}

const inputStyle = {
  border: 'solid'
}
const startSfen = 'sfen lnsgkgsnl/1r5b1/p2pppppp/1pp6/9/2P6/PPBPPPPPP/7R1/LNSGKGSNL b - 5'

const Form: React.FC<DataProps & PropsFromDispatch> = ({ tree, setRootSfen }) => {
  const [text, setText] = useState('')
  const [rootSfen_, setRootSfen_] = useState(startSfen)
  // 初回のみrootSfenへのリクエストを投げる
  useMemo(() => {
    setRootSfen(startSfen)
  }, [])
  // テキストボックスが変更されたときの処理
  useEffect(() => {
    const splitStr = text.split(' ')
    console.log(splitStr)
    if (splitStr.length == 5 && splitStr[0] == 'sfen' && splitStr[4].length > 0) {
      setRootSfen_(text)
      const sfen = splitStr.join(' ')
      setRootSfen(sfen)
      setText('')
    }
  }, [text])

  console.log('tree')
  console.log(tree)

  return (
    <div key={rootSfen_}>
      <h1>やねうら定跡ビューワー</h1>
      <input
        style={inputStyle}
        type="text"
        onChange={(e: any) => setText(e.target.value)}
        value={text}
        size={120}
        spellCheck={false}
        autoComplete="off"
        placeholder="Please input sfen."
      />
      <div>{rootSfen_}</div>
      <NodeView
        node={tree}
        func={(s: string) => {
          setRootSfen(s)
        }}
      />
    </div>
  )
}

class Container extends React.Component<AllProps> {
  public render() {
    const { setRootSfen: setRootSfen } = this.props
    const props = this.props
    return <Form tree={props.tree} setRootSfen={setRootSfen} />
  }
}
const mapStateToProps = ({ tree }: BookState) => ({
  tree: tree
})
const mapDispatchToProps = (dispatch: Dispatch) => {
  return {
    setRootSfen: (sfen: string) => dispatch(setRootSfen(sfen))
  }
}
export default connect(
  mapStateToProps,
  mapDispatchToProps
)(Container)
