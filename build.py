# 把 ../game.html（claude.ai 版）轉成獨立網站版 index.html
# 用法：python build.py
import sys, os
here = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(here, '..', 'game.html'), encoding='utf-8').read()

def rep(a, b):
    global src
    if src.count(a) != 1:
        sys.exit('找不到要替換的內容：' + a[:60])
    src = src.replace(a, b)

old_init = src[src.index('async function initCloud(){'):]
old_init = old_init[:old_init.index('\n')]
rep(old_init, "async function initCloud(){try{const c=await window.BD_CLOUD;if(c){db=c.db;uid=c.uid;room=c.room||null}}catch(e){db=null}}")
rep("交換箱要從 claude.ai 開啟並登入後才能用喔。", "要登入帳號才能用交換箱喔。")
rep("單機模式：要從 claude.ai 開啟並登入，才能看到朋友和使用交換箱。", "單機模式：登入帳號後，才能看到朋友和使用交換箱。")
rep('<meta name="claude:viewport-fit-sides" content="cover">\n', '')
rep('  <div class="side">', '  <div class="side">\n    <section class="card acct"><span id="acctName">尚未登入</span><button type="button" id="logoutBtn" hidden>登出</button></section>')

head, body = src.split('<div class="wrap">', 1)
auth_html = open(os.path.join(here, 'auth.html'), encoding='utf-8').read()
page = ('<!doctype html>\n<html lang="zh-Hant">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
        + head + '</head>\n<body>\n' + auth_html + '\n<div class="wrap">' + body + '\n</body>\n</html>\n')
# 遊戲主程式之前先放一個「等待登入」的 promise
import time, json
build = time.strftime('%Y%m%d-%H%M%S')
page = page.replace('<script>\n(()=>{', '<script>window.BD_BUILD="' + build + '";window.BD_CLOUD=new Promise(r=>{window.__resolveCloud=r});</script>\n<script>\n(()=>{', 1)
page = page.replace("from './firebase-config.js'", "from './firebase-config.js?v=" + build + "'")
open(os.path.join(here, 'index.html'), 'w', encoding='utf-8').write(page)
json.dump({'build': build}, open(os.path.join(here, 'version.json'), 'w'))
print('OK -> index.html')
