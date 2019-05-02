const { app, BrowserWindow } = require('electron')

// レンダープロセスとなるブラウザ・ウィンドウのオブジェクト。
// オブジェクトが破棄されると、プロセスも終了するので、グローバルオブジェクトとする。
let win

function createWindow() {
  // ブラウザウィンドウの作成
  win = new BrowserWindow({
    width: 800,
    height: 600
  })
  // index.html をロードする
  win.loadFile('http://localhost:3000')
  // 起動オプションに、 "--debug"があれば開発者ツールを起動する
  if (process.argv.find(arg => arg === '--debug')) {
    win.webContents.openDevTools()
  }
  // ブラウザウィンドウを閉じたときのイベントハンドラ
  win.on('closed', () => {
    // 閉じたウィンドウオブジェクトにはアクセスできない
    win = null
  })
}

// このメソッドは、Electronが初期化を終了し、
// ブラウザウィンドウを作成する準備ができたら呼び出される。
// 一部のAPIは、このイベントが発生した後にのみ使用できる。
app.on('ready', createWindow)

// 全てのウィンドウオブジェクトが閉じたときのイベントハンドラ
app.on('window-all-closed', () => {
  // macOSでは、アプリケーションとそのメニューバーがCmd + Qで
  // 明示的に終了するまでアクティブになるのが一般的なため、
  // メインプロセスは終了させない
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', () => {
  // MacOSでは、ドックアイコンがクリックされ、
  // 他のウィンドウが開いていないときに、アプリケーションでウィンドウを
  // 再作成するのが一般的です。
  if (win === null) {
    createWindow()
  }
})
