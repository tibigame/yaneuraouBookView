import * as React from 'react'
import { Move } from './types'
import getRgb from './color'

import { rgb2hex } from './color'
// import styled from '@emotion/styled'
// parcel2からはemotionが使えるようになるみたいだが
// 全体のコード量が少ないので今は素のscssインポートでがんばる
import './board.scss'

/*
const BoardStyle = styled.div`
  color: hotpink;
`

interface Props {
  sfen: string
}
*/

// sfenでの駒文字からpretty文字を返す
const pieceMap = new Map([
  ['k', '玉'],
  ['K', '玉'],
  ['R', '飛'],
  ['r', '飛'],
  ['B', '角'],
  ['b', '角'],
  ['G', '金'],
  ['g', '金'],
  ['S', '銀'],
  ['s', '銀'],
  ['N', '桂'],
  ['n', '桂'],
  ['L', '香'],
  ['l', '香'],
  ['P', '歩'],
  ['p', '歩']
])

// 駒文字の成り駒を返す
const promoteMap = new Map([
  ['飛', '竜'],
  ['角', '馬'],
  ['銀', '全'],
  ['桂', '圭'],
  ['香', '杏'],
  ['歩', 'と']
])

// Squareと升目のクラス名を対応させるテーブル
const boardIndex = [
  'sq91',
  'sq81',
  'sq71',
  'sq61',
  'sq51',
  'sq41',
  'sq31',
  'sq21',
  'sq11',
  'sq92',
  'sq82',
  'sq72',
  'sq62',
  'sq52',
  'sq42',
  'sq32',
  'sq22',
  'sq12',
  'sq93',
  'sq83',
  'sq73',
  'sq63',
  'sq53',
  'sq43',
  'sq33',
  'sq23',
  'sq13',
  'sq94',
  'sq84',
  'sq74',
  'sq64',
  'sq54',
  'sq44',
  'sq34',
  'sq24',
  'sq14',
  'sq95',
  'sq85',
  'sq75',
  'sq65',
  'sq55',
  'sq45',
  'sq35',
  'sq25',
  'sq15',
  'sq96',
  'sq86',
  'sq76',
  'sq66',
  'sq56',
  'sq46',
  'sq36',
  'sq26',
  'sq16',
  'sq97',
  'sq87',
  'sq77',
  'sq67',
  'sq57',
  'sq47',
  'sq37',
  'sq27',
  'sq17',
  'sq98',
  'sq88',
  'sq78',
  'sq68',
  'sq58',
  'sq48',
  'sq38',
  'sq28',
  'sq18',
  'sq99',
  'sq89',
  'sq79',
  'sq69',
  'sq59',
  'sq49',
  'sq39',
  'sq29',
  'sq19'
]

const moveSquareTable = {
  '9a': 0,
  '8a': 1,
  '7a': 2,
  '6a': 3,
  '5a': 4,
  '4a': 5,
  '3a': 6,
  '2a': 7,
  '1a': 8,
  '9b': 9,
  '8b': 10,
  '7b': 11,
  '6b': 12,
  '5b': 13,
  '4b': 14,
  '3b': 15,
  '2b': 16,
  '1b': 17,
  '9c': 18,
  '8c': 19,
  '7c': 20,
  '6c': 21,
  '5c': 22,
  '4c': 23,
  '3c': 24,
  '2c': 25,
  '1c': 26,
  '9d': 27,
  '8d': 28,
  '7d': 29,
  '6d': 30,
  '5d': 31,
  '4d': 32,
  '3d': 33,
  '2d': 34,
  '1d': 35,
  '9e': 36,
  '8e': 37,
  '7e': 38,
  '6e': 39,
  '5e': 40,
  '4e': 41,
  '3e': 42,
  '2e': 43,
  '1e': 44,
  '9f': 45,
  '8f': 46,
  '7f': 47,
  '6f': 48,
  '5f': 49,
  '4f': 50,
  '3f': 51,
  '2f': 52,
  '1f': 53,
  '9g': 54,
  '8g': 55,
  '7g': 56,
  '6g': 57,
  '5g': 58,
  '4g': 59,
  '3g': 60,
  '2g': 61,
  '1g': 62,
  '9h': 63,
  '8h': 64,
  '7h': 65,
  '6h': 66,
  '5h': 67,
  '4h': 68,
  '3h': 69,
  '2h': 70,
  '1h': 71,
  '9i': 72,
  '8i': 73,
  '7i': 74,
  '6i': 75,
  '5i': 76,
  '4i': 77,
  '3i': 78,
  '2i': 79,
  '1i': 80
}

// intから漢数字への変換テーブル
const intToChinese = [
  '〇',
  '一',
  '二',
  '三',
  '四',
  '五',
  '六',
  '七',
  '八',
  '九',
  '十',
  '十一',
  '十二',
  '十三',
  '十四',
  '十五',
  '十六',
  '十七',
  '十八'
]

// intから全角数字への変換テーブル
const intToArabic = ['０', '１', '２', '３', '４', '５', '６', '７', '８', '９']

const charCodeA = 'A'.charCodeAt(0) // Aを表すアスキーコード
const charCode0 = '0'.charCodeAt(0) // 0を表すアスキーコード
const charCode9 = '9'.charCodeAt(0) // 9を表すアスキーコード
const charCodea = 'a'.charCodeAt(0) // aを表すアスキーコード (これ以上なら小文字)

// sfen: 表示する盤面のsfen文字列, value: 局面の評価値 (正の数なら先手が有利)
// 親の指し手を強調表示で使うために与える
const Board = (sfen: string, value: number, moveList: Move[], prev: string, prevPretty: string) => {
  const sfen_ = sfen.split(' ')
  const sfenBoard = sfen_[1]
  const sfenSideToMove = sfen_[2]
  const sfenHand = sfen_[3]

  // 盤面のパース
  let reactKey = 0
  let token = 0 // sfen文字列を走査するトークンのポインタ
  let sqCount = 0 // 読んだ升のカウント (盤面左上を0とし、右方向へ右端で改行して下まで右下は80)
  let promoteFlag = false // その駒が成り駒かどうか (直前の文字が+ならtrue)
  let isBlackPiece = true // その駒が先手のものかどうか (その文字が大文字ならtrue)
  let strongFlag = false // 指し手の強調表示かどうか
  let domArray: JSX.Element[] = [] // 出力するReactDomの配列

  while (sqCount < 81) {
    if (sfenBoard.length <= token) {
      break // 正しいsfen文字列ならここに来ることはないはず
    }
    const tokenAsciiCode = sfenBoard.charCodeAt(token)
    if (tokenAsciiCode >= charCodeA) {
      // A以上は駒文字を想定している
      const pieceStr = sfenBoard[token]
      let piece = pieceMap.get(pieceStr) // 駒文字の導出
      isBlackPiece = pieceStr.charCodeAt(0) < charCodea // 先手か後手かの判定
      if (promoteFlag) {
        // 成り駒にする
        piece = piece != undefined ? promoteMap.get(piece) : ''
        promoteFlag = false // フラグを戻しておく
      }
      const prevMovedPlace = prev.slice(-1) == '+' ? prev.slice(-3, -1) : prev.slice(-2)
      strongFlag = sqCount == moveSquareTable[prevMovedPlace]
      // 駒の種類と座標が確定したのでレンダリングすべきDomが定まる
      domArray.push(
        <div
          key={reactKey}
          className={`${boardIndex[sqCount]} ${isBlackPiece ? 'black' : 'white'}${
            strongFlag ? ' strong' : ''
          }`}
        >
          {piece}
        </div>
      )
      reactKey++
      sqCount++ // 駒文字を呼んだので升をカウントする
    } else if (tokenAsciiCode >= charCode0) {
      // 0以上は数字を想定している
      sqCount += tokenAsciiCode - charCode0 // 升目の数だけカウントを進める
    } else if (sfenBoard[token] == '+') {
      // +は次の駒が成り駒であることを示す
      promoteFlag = true
    }
    token++ // 他の文字「/」などは意味をなさないので次の文字を読む
  }
  // 手番
  const tebanStr = sfenSideToMove == 'b' ? '先手番' : '後手番'
  // 駒台のパース
  token = 0
  let handBlackStr = '' // 先手の手駒を表す文字列
  let handWhiteStr = '' // 後手の手駒を表す文字列
  if (sfenHand != '-') {
    let ct = 0 // 駒数のカウント
    let isUnderTen = true // 10以下であることを示すフラグ
    while (token < sfenHand.length) {
      // 1が現れるのは歩が10枚以上のときのみ (ここは十の位で通過する)
      if (sfenHand[token] == '1' && isUnderTen) {
        isUnderTen = false
      }
      // ここは一の位で通過する
      else if (sfenHand.charCodeAt(token) <= charCode9) {
        ct = sfenHand.charCodeAt(token) - charCode0
        if (!isUnderTen) {
          // 十の位のフローを通過していれば10枚追加する
          ct += 10
          isUnderTen = true // フラグを元に戻す
        }
      }
      // 駒文字のときに通過する想定
      else {
        const pieceStr = sfenHand[token]
        let piece = pieceMap.get(pieceStr) // 駒文字の導出
        isBlackPiece = pieceStr.charCodeAt(0) < charCodea // 先手か後手かの判定
        if (ct >= 2) {
          // 1のときの数詞は省略する
          piece += intToChinese[ct]
        }
        if (isBlackPiece) {
          handBlackStr += piece
        } else {
          handWhiteStr += piece
        }
        ct = 0 // 駒数カウントを元に戻す
      }
      token++
    }
  }
  // 手駒が無いときは「なし」にする
  if (handBlackStr.length == 0) {
    handBlackStr = 'なし'
  }
  if (handWhiteStr.length == 0) {
    handWhiteStr = 'なし'
  }
  // 手数の部分は考慮しないのでこれでパースは終了となる
  const style = {
    background: getRgb(value)
  }

  let moveListIndex = 0
  let moveListElm = moveList.map((move: Move) => {
    if (!move.move) {
      return <div key={moveListIndex}>* : {value}</div>
    }
    moveListIndex++
    const tebanMark = sfenSideToMove == 'b' ? '▲' : '△'
    const moveStr = move.movePretty.length > 0 ? move.movePretty : move.move
    return (
      <div key={moveListIndex}>
        {tebanMark}
        {moveStr}: {sfenSideToMove == 'b' ? move.value : -move.value}
      </div>
    )
  })

  let prevStr = ''
  if (prevPretty.length > 0) {
    prevStr = `${sfenSideToMove == 'b' ? '△' : '▲'}${prevPretty}まで`
  } else if (prev.length > 0) {
    prevStr = `${sfenSideToMove == 'b' ? '△' : '▲'}${prev}まで`
  } else {
    prevStr = '開始局面'
  }

  return (
    <div key={sfen} style={style} className="shogi black-side">
      <div className="board">
        <div className="line board-border">&nbsp;</div>
        <div className="line area_f2">&nbsp;</div>
        <div className="line area_f4">&nbsp;</div>
        <div className="line area_f6">&nbsp;</div>
        <div className="line area_f8">&nbsp;</div>
        <div className="line area_r2">&nbsp;</div>
        <div className="line area_r4">&nbsp;</div>
        <div className="line area_r6">&nbsp;</div>
        <div className="line area_r8">&nbsp;</div>
        <div className="num rank1">一</div>
        <div className="num rank2">二</div>
        <div className="num rank3">三</div>
        <div className="num rank4">四</div>
        <div className="num rank5">五</div>
        <div className="num rank6">六</div>
        <div className="num rank7">七</div>
        <div className="num rank8">八</div>
        <div className="num rank9">九</div>
        <div className="num file1">１</div>
        <div className="num file2">２</div>
        <div className="num file3">３</div>
        <div className="num file4">４</div>
        <div className="num file5">５</div>
        <div className="num file6">６</div>
        <div className="num file7">７</div>
        <div className="num file8">８</div>
        <div className="num file9">９</div>
        {domArray}
      </div>
      <div className="hands-black">
        <span className="piece">{handBlackStr}</span>
      </div>
      <div className="hands-white">
        <span className="piece">{handWhiteStr}</span>
      </div>
      <div className="info">
        {prevStr}
        <br />
        {moveListElm}
      </div>
    </div>
  )
}
export default Board
