# YaneuraouBookView

## 概要

やねうら王形式の定跡ファイルをWebUIで見ることができるツールです。

## 使用法

### 依存

* python3.6以上でflask他のパッケージ
* node.js
* chrome

### 起動方法

* 定跡ファイルを./server/user_book1.dbに置きます。 (コミットではテラショック定跡が置かれています)
* serverディレクトリでindex.pyを実行します。 (flaskサーバーが3000ポートで待ち受けます)
* cliantディレクトリでnpm install (またはyarn install)
* npm run start (またはyarn start) (1234ポートでクライアントサーバーが待ち受けます)
* localhost:1234にchromeでアクセスしてください (他のブラウザは非推奨)

![スクリーンショット](https://github.com/tibigame/yaneuraouBookView/blob/master/snapshot.png)

* テキストボックスにsfenを入力するとその局面をルートとして再構築がはじまります。
* 局面をクリックするとその下に「この局面をルートにする」と出るので、そこをクリックしても再構築できます。
* 局面下部のバーをクリックすると折りたたむことができます。
* 先手良しは青、後手良しは赤、互角は黄で、評価値が高いほど色が濃くなります。

* saga.tsxにパラメータあるので局面数の調整とかしてください。

### 既知の問題

* sfen入力を一度しか受け付けないので違うツリーを作りたいときはリロードが必要です
* electron化しようとして挫折してます
* cssの実装がいけてないです
* 棋譜の表記で"同"に未対応(左、上、打などには対応)
* 大駒が2枚が同じ所に効いているが、片方が他の駒で遮られている状態で上、右などの区別表記が付いてしまう
* 定跡ファイルを一旦メモリに読み込むのでGBクラスになるとキツイ (onTheFlyの実装が必要)
