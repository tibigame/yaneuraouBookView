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

### 既知の問題

* electron化しようとして挫折してます
* cssの実装がいけてないです
* 棋譜の表記で"同"に未対応(左、上、打などには対応)
* 定跡ファイルを一旦メモリに読み込むのでGBクラスになるとキツイ
