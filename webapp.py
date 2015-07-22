try: from bottle import get, post, route, run, static_file, response, abort, redirect, request, template, os, view
except ImportError:print("bottle package is not installed.\nPlease run afert install bottle package.")
import os
currentDirPass = os.path.dirname(__file__)
#ダウンロード
@route('/download/<filename:path>')
def download(filename):
    return static_file(filename, root = currentDirPass + '/bin', download=filename)

#エラーページ
@route('/restricted')
def restricted():
    abort(401, "Sorry, your access denied!")

#CSSとかJSとか
@route('/views/<filepath:path>', name='static_file')
def static(filepath):
    return static_file(filepath, root="./views")

#インデックスページ(ファイルアップロード)
@get('/')
@view('index')
def index():
    return '''
        <form action="/upload" method="post" enctype="multipart/form-data">
            Select a file:  <input type="file" name="upload">
            <input type="submit" value="start upload">
        </form>
    '''
@route('/', method='POST')
def do_upload():
    upload   = request.files.get('upload')
    name, ext = os.path.splitext(upload.filename)
    if ext not in ('.png', '.jpg', '.jpeg'):
        return 'File extension not allowed.'
    savePath = currentDirPass + '/bin'
    upload.save(save_path)
    return 'OK'

#テスト用
@route('/test')
@view('index')
def test():
    return dict()

run(host='localhost', port=8080, debug=True)#サーバー起動
