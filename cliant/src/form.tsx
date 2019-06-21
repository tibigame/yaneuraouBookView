import * as React from 'react'
import { useState, useEffect, useMemo } from 'react'
import { connect } from 'react-redux'
import { Dispatch } from 'redux'
import { BookState, Node } from './types'
import { setRootSfen } from './actions'
import Board from './board'
import './form.scss'
import Select from './select'

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
const startSfen = 'lnsgk1snl/6g2/p1pppp2p/6R2/9/1rP6/P2PPPP1P/1SG4p1/LN2KGSNL b B3Pbp 1'

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

  const yokofu = [
    {
      label: '平手初期局面',
      text: 'sfen lnsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL b - 1'
    },
    {
      label: '課題局面',
      text: 'sfen lnsgk1snl/6g2/p1pppp2p/6R2/9/1rP6/P2PPPP1P/1SG6/LN2KGSNL w B3Pb2p 18'
    },
    {
      label: '△４五角開始',
      text: 'sfen lnsgk1snl/6g2/p1pppp2p/6R2/5b3/1rP6/P2PPPP1P/1SG4S1/LN2KG1NL b B4Pp 21'
    },
    {
      label: '△４五角△３三桂分岐',
      text: 'sfen lnsgk1s1+B/6g2/p1ppppn1p/7p1/5b3/2P6/P2PPPP1P/2G4S1/LN2KG1NL b RL4Prs 29'
    },
    {
      label: '△４五角△８七銀分岐',
      text: 'sfen lnsgk1sn+B/6g2/p1pppp2p/7p1/5b3/2P6/Ps1PPPP1P/2G4S1/LN2KG1NL b RL4Pr 29'
    },
    {
      label: '△４五角△２五飛分岐',
      text: 'sfen lnsgk1sn+B/6g2/p1pppp2p/7p1/5b1r1/2P6/P2PPPP1P/2G4S1/LN2KG1NL b RL4Ps 29'
    },
    {
      label: '△２八歩取らず▲７七角△８八飛成',
      text: 'sfen lnsgk1snl/6g2/p1pppp2p/6R2/9/2P6/P1BPPPP1P/1+rG4p1/LN2KGSNL b 3Pbsp 21'
    },
    {
      label: '△２八歩取らず▲７七角△７六飛',
      text: 'sfen lnsgk1snl/6g2/p1pppp2p/6R2/9/2r6/P1BPPPP1P/1SG4S1/LN2KG1NL w 4Pb2p 22'
    },
    {
      label: '△２八歩取らず▲７七角△７六飛▲２七同銀定跡開始',
      text: 'sfen lnsgk1snl/6g2/p1pppp2p/6R2/5b3/2r6/P1BPPPPSP/1SG6/LN2KG1NL b 5Pp 25'
    },
    {
      label: '△２八歩取らず▲７七角△７六飛▲２七同銀定跡▲４五飛変化',
      text: 'sfen lnsgk1s1l/6g2/p1ppppnpp/9/5R3/2r6/P1BPPPPSP/1SG6/LN2KG1NL w B5P 30'
    },
    {
      label: '△２八歩取らず▲７七角△７六飛▲２七同銀定跡本線分岐',
      text: 'sfen lnsgk1s1l/9/p1ppppgpp/9/2R6/9/P1SPP+bP1P/2G6/LN2KG1NL b RN5Pbsp 38'
    },
    {
      label: '△２八歩取らず▲７七角△７六飛▲３九銀定跡開始',
      text: 'sfen lnsgk1snl/6g2/p1pppp2p/6R2/9/2r6/P1BPPPPpP/1SG6/LN2KGSNL w 4Pbp 24'
    },
    {
      label: '△２八歩取らず▲７七角△７六飛▲３九銀▲８四飛',
      text: 'sfen lnsgk1snl/6g2/p1ppppp1p/1R7/9/7r1/P1BPPPPpP/1SG3G2/LN2K1SNL w 4Pb 28'
    },
    {
      label: '△２八歩取らず▲７七角△７六飛▲３九銀▲８四飛定跡▲５五角変化',
      text: 'sfen l+Rsgk1snl/6g2/p1ppppp1p/9/4B4/7r1/P2PPPPpP/1SG3G2/LN2K1SN+b w N4Pl 32'
    },
    {
      label: '△２八歩取らず▲７七角△７六飛▲３九銀▲８四飛定跡▲８三桂変化▲９五角まで',
      text: 'sfen +Rl1gk1snl/2s3g2/pNppppp1p/2P6/B8/7r1/P2PPPP1P/1SG3G+p1/LN2K1SN+b w L3P 38'
    },
    {
      label: '△３三角',
      text: 'sfen lnsgk1snl/6g2/p1ppppb1p/6R2/9/1rP6/P2PPPP1P/1SG3S2/LN2KG1NL b B4Pp 20'
    },
    {
      label: '△４四角▲７七角定跡',
      text: 'sfen lnsgk1snl/6g2/p1pppp2p/5bR2/9/1rP6/P1BPPPP1P/1SG3S2/LN2KG1NL w 4Pp 22'
    },
    {
      label: '△４四角▲７七角定跡▲７五角一直線変化',
      text: 'sfen lnsgk1snl/4p1g2/p1pp+Bpp1p/4R4/9/2r6/P1NPPPP1P/1SG3S2/Lb2KG1NL b 5P 31'
    },
    {
      label: '△４四角▲８七歩定跡▲５六角',
      text: 'sfen lnsgk1snl/6g2/p1pppp2p/2r2bR2/9/4B4/PPSPPPP1P/2G3S2/LN2KG1NL w 3P2p 26'
    },
    {
      label: '△４四角▲８七歩定跡▲５六角:△８九飛変化',
      text: 'sfen lnsgk1snl/6g2/p1pppp2p/6B2/9/9/PPNPPPP1P/2G3S2/Lr2KG1NL b RB3Ps2p 31'
    }
  ]

  return (
    <div key={rootSfen_}>
      <h1>やねうら定跡ビューワー</h1>
      <Select data={yokofu} func={setRootSfen} />
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
