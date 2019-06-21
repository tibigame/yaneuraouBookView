# 横歩取り△４五角テラショック定跡 (他横歩取り超急戦定跡)

## 概要

古来よりの戦法に終止符を打つべく**横歩取り△４五角後手確殺定跡**を完成させました。
16コアのマシンで1ヶ月ほどの計算量を投じて掘られた決定版の定跡です。
depth30で4500局面ほど掘られており、
将来的なR5000級評価関数にdepth40級の探索をするマシンでも、
この定跡をひっくり返すのは難しいと思われます。

### 定跡の深さ

* 探索: やねうら王(v4.8.4)
* 評価関数: Kristallweizen(2019春白ビール)
* MultiPV: 4, depth: 30, nodes: 20億
* 枝によっては50手以上掘り進めている変化あり。
* これは一局みたいなゆるやかな変化は短く、切り合いの変化を深く掘っています。
* 定跡の長く掘り進めている枝は浮かむ瀬の時代から数億ノードでいくつかの評価関数で検証された指し手の(白ビール独断で掘ったわけではない)ため信頼度はあります。

# 定跡の結論

## 課題局面

![figure01](https://github.com/tibigame/yaneuraouBookView/blob/master/figure01.png)

* 横歩取り超急戦分岐の課題局面にて相横歩取りの△７六飛は第３候補である。
* △３八歩は第５候補である。
* △２八歩は第６候補である。

## △３八歩変化

![figure02](https://github.com/tibigame/yaneuraouBookView/blob/master/figure02.png)

* △３三角は第２候補である。
* △４四角は第５候補である。

### △３八歩変化△３三角

* △３三角という角の打ち場所は△４四角という打ち場所に比べて後手の飛車が４段目に行ったときに角の影にならずに直接先手の飛車に当たる点(先手は直接的に対処しないといけない)が優れている。
* 角の打ち場所が関係ない△７七角成は第４候補である。

![figure03](https://github.com/tibigame/yaneuraouBookView/blob/master/figure03.png)

* △３三角の後手最善手の枝である△７六飛変化では青野流と比べると先手が幾分得をしていることがお分かりだろう。

### △３八歩変化▲７七角△同角成定跡

![figure04](https://github.com/tibigame/yaneuraouBookView/blob/master/figure04.png)

* △４四角の最大の欠点は第１候補が△７七角成になってしまうことである。

![figure05](https://github.com/tibigame/yaneuraouBookView/blob/master/figure05.png)

* 分岐で△８九角は第５候補である。

### △３八歩変化▲７七角△同角成定跡▲７五角一直線変化


![figure06](https://github.com/tibigame/yaneuraouBookView/blob/master/figure06.png)

* 最善手は△７八馬と金銀を切り取る手だが、▲６五桂が味良し道夫。
* ▲７五角に後手が弱気に△７六飛と交わして▲５三角成△３三歩▲５四飛△５二歩と進むのが▲７五角一直線変化だ。

![figure07](https://github.com/tibigame/yaneuraouBookView/blob/master/figure07.png)

* ▲７五角一直線変化の成果は△５二歩にじっと馬を見捨てて▲６八金で後手手がない。
** 後手は３枚の大駒で馬か龍を作りつつ金駒を駒台に載せたいがそれはかなわない。
*** 大駒２枚捨てても桂馬しか手に入らないし、金駒手に入れるには大駒３枚捨てる必要がある=先手は相当安全だから馬は捨ててよい。
** 後手は▲８四飛が歩切れで受けがない。
** 後手陣は８筋攻めのときに３筋が壁形。

### △３八歩変化△４四角▲８七歩定跡

![figure08](https://github.com/tibigame/yaneuraouBookView/blob/master/figure08.png)

* 実は△７六飛に▲７七桂の方が評価値が高い。

### △３八歩変化△４四角▲８七歩定跡▲５六角

![figure09](https://github.com/tibigame/yaneuraouBookView/blob/master/figure09.png)

* 後手の飛車が４段目に行った時に後手の角の影に入ってしまうことを咎める▲５六角
* この▲５六角は絶品ダブルチーズバーガー
* △７七角成は第４候補である。

![figure10](https://github.com/tibigame/yaneuraouBookView/blob/master/figure10.png)

△５四飛▲２四歩△３三金▲３六飛△３四歩が▲５六角の深淵で、後手の上ずり金に対して先手の模様が良い。

![figure11](https://github.com/tibigame/yaneuraouBookView/blob/master/figure11.png)

* ▲５六角に△７七角成とすればこうなるが、ここからもかなり深く定跡を掘っている。

## △２八歩の分岐

![figure12](https://github.com/tibigame/yaneuraouBookView/blob/master/figure12.png)

* △２八歩取らず▲７七角は第２候補で先手やや不利なので避けるべし。

## △２八歩取らず△８八飛成

![figure13](https://github.com/tibigame/yaneuraouBookView/blob/master/figure13.png)

* △８八飛成は先手優勢である。

△８八飛成▲同角△２九歩成▲１一角成△３九と▲同金と進む。

### ５段目に空中の紐がついている

![figure14](https://github.com/tibigame/yaneuraouBookView/blob/master/figure14.png)

* ▲３二飛成△同銀▲５五飛が詰めろになることを指して５段目に空中の紐が付いているという
* ５段目の空中の紐のため△２五角などは詰めろ角取りで抜かれる。何気に１一の馬がいい仕事をしていて△４四銀などを無効化している。
* ５段目に５四銀などの返しの受けが効く△４五桂のような攻めはぬるいため、▲２一馬で十分である。
* 後手は不甲斐なく(歩が駒台にないこと)なりがち

## △２八歩取らず△７六飛

![figure15](https://github.com/tibigame/yaneuraouBookView/blob/master/figure15.png)

* 検討の結果△２七歩に銀を対処する手は第３候補以下になってしまった。

### △２八歩取らず▲２七同銀定跡

![figure16](https://github.com/tibigame/yaneuraouBookView/blob/master/figure16.png)

* こちらは互角と見られていたが、奥深くで先手がまずい変化があったため非推奨。
* ここで▲４五飛でも後手も香に弱いし角打ちの隙があるから難しいが先手は不本意だろう。

### △２八歩取らず▲２七同銀定跡本筋分岐

▲３三角成△同金▲７七銀△７五飛▲３六銀△同角▲７五飛△４七角成まで一直線。

![figure17](https://github.com/tibigame/yaneuraouBookView/blob/master/figure17.png)

* ▲４八歩で弾いておけば先手やれるとの想定だったが、△２九馬のときに▲４五桂△２七角の攻め合いは先手負けのようだ。
* ここで▲６八金と手を戻すようでは先手自信がない。
* この変化がダメになったため▲２七同銀定跡全体がダメになった。

### △２八歩取らず▲３九銀定跡

![figure18](https://github.com/tibigame/yaneuraouBookView/blob/master/figure18.png)

* 当初は▲２七同銀定跡よりもこちらが本筋で有力と見られていた。
* 後手は△２七歩からの継続手で△２六飛と回るしかない。
* ▲３六飛は変調なので▲３八金と歩成を受ける。
* ▲２二歩や▲１一角成が厳しいので後手は△３三歩と虎の子の一歩を手放し３筋を壁型を甘受するしかない。

### △２八歩取らず▲３九銀定跡▲８四飛

![figure19](https://github.com/tibigame/yaneuraouBookView/blob/master/figure19.png)

* △２八角▲８一飛成△１九角成の筋で先手良しというのが当初の見立てだったが、現在は第２候補になってしまった。

![figure20](https://github.com/tibigame/yaneuraouBookView/blob/master/figure20.png)

* まずは当初先手勝ちだと思われていた▲８三桂変化を見ていこう。

### △２八歩取らず▲３九銀定跡▲８四飛▲８三桂変化

![figure21](https://github.com/tibigame/yaneuraouBookView/blob/master/figure21.png)

△７二銀▲９一龍△８一香▲７四歩△２八歩成▲９五角まで後手は間違えられない綱渡り。

### △２八歩取らず▲３九銀定跡▲８四飛▲８三桂変化▲９五角

![figure22](https://github.com/tibigame/yaneuraouBookView/blob/master/figure22.png)

△３八と▲７三歩成△２九飛成▲７二と△４一玉▲６一と△３七馬▲５一銀△４一玉▲６一と

![figure23](https://github.com/tibigame/yaneuraouBookView/blob/master/figure23.png)

この局面、お手持ちのソフトで正しく評価できるだろうか。
△４四歩▲８一龍△３九龍▲７七玉と進むとこうなるが

![figure24](https://github.com/tibigame/yaneuraouBookView/blob/master/figure24.png)

後手に妙手△７五金があって勝ちのようだ。
といってもこの局面での△７五金の先も相当際どいが。

### △２八歩取らず▲３九銀定跡▲８四飛▲５五角変化

![figure25](https://github.com/tibigame/yaneuraouBookView/blob/master/figure25.png)

▲８三桂がダメなら遡ってこう進むしかないがこっちも旗色は良くない。

## △４五角開始

![figure26](https://github.com/tibigame/yaneuraouBookView/blob/master/figure26.png)
![figure27](https://github.com/tibigame/yaneuraouBookView/blob/master/figure27.png)

### △４五角△８七銀変化

![figure28](https://github.com/tibigame/yaneuraouBookView/blob/master/figure28.png)

* 馬を引きつける▲７七馬は第２候補である
* テラショック定跡の教えるところでは素直に▲同金が最善である。

#### ▲７七馬変化

△７六銀不成▲６八馬△８八歩▲４六飛△８九歩成▲４五飛

![figure32](https://github.com/tibigame/yaneuraouBookView/blob/master/figure32.png)

その後は△８六桂▲４八玉△７八桂成▲同馬△８八と▲９六馬など。

#### ▲８七同金変化

△７九飛▲６九香△６七角成▲５八銀△８九馬▲４八玉△３三桂

![figure33](https://github.com/tibigame/yaneuraouBookView/blob/master/figure33.png)

### △４五角△３三桂変化

![figure29](https://github.com/tibigame/yaneuraouBookView/blob/master/figure29.png)
![figure30](https://github.com/tibigame/yaneuraouBookView/blob/master/figure30.png)

* ▲３六香変化は長く掘っているが△８四飛から粘る展開が後手最善とは辛いだろう。

#### △８七銀変化

▲７九金△６七角成▲３三香成△７八銀成▲同金△同馬

![figure34](https://github.com/tibigame/yaneuraouBookView/blob/master/figure34.png)

ここで▲６二歩は面白い変化だったり

### △４五角△２五飛変化

![figure31](https://github.com/tibigame/yaneuraouBookView/blob/master/figure31.png)

* ▲２七歩、▲３九金どちらも長く掘っているが先手十分。

#### ▲２七歩変化

△２七同角成▲同銀△同飛成▲３九金△２八銀▲４五角△２五龍▲６三角成△５二銀▲３六馬△同龍▲同歩△３九銀不成

![figure35](https://github.com/tibigame/yaneuraouBookView/blob/master/figure35.png)

#### ▲３九金変化

△２七銀▲同銀△同角成▲３六銀△同馬▲同歩△２八銀

![figure36](https://github.com/tibigame/yaneuraouBookView/blob/master/figure36.png)

