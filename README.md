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
* http://localhost:1234にchromeでアクセスしてください (他のブラウザは非推奨)

### 既知の問題

* electron化しようとして挫折してます
* cssの実装がいけてないです
* 棋譜の表記で"同"に未対応(左、上、打などには対応)

