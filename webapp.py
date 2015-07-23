import os
from socket import gethostname
currentDirPass = os.path.abspath(os.path.dirname(__file__))
os.chdir(currentDirPass)
#SetUp
def install_bottle():
    print('Downloading bottle...')
    from urllib.request import urlretrieve
    urlretrieve('https://raw.githubusercontent.com/bottlepy/bottle/master/bottle.py', currentDirPass + '/bottle.py')
def install_bootstrap():
    print('Downloading bootstrap...')
    from urllib.request import urlretrieve
    import zipfile, shutil
    zipFile, headers = urlretrieve('https://github.com/twbs/bootstrap/releases/download/v3.3.5/bootstrap-3.3.5-dist.zip', currentDirPass + '/views/bootstrap-3.3.5-dist.zip')
    with zipfile.ZipFile(zipFile, 'r') as zipFile:
        zipFile.extractall(path=currentDirPass+'/views/')
    shutil.move(currentDirPass + '/views/bootstrap-3.3.5-dist/css',currentDirPass + '/views')
    shutil.move(currentDirPass + '/views/bootstrap-3.3.5-dist/js',currentDirPass + '/views')
    shutil.move(currentDirPass + '/views/bootstrap-3.3.5-dist/fonts',currentDirPass + '/views')
    # os.remove(currentDirPass + '/views/bootstrap-3.3.5-dist') # パーミッションエラーが出る
    # os.remove(currentDirPass + '/views/bootstrap-3.3.5-dist.zip')
def install_jQuery():
    print('Downloading jQuery...')
    os.makedirs(currentDirPass + '/views/jQuery')
    from urllib.request import urlretrieve
    urlretrieve('https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js', currentDirPass + '/views/jQuery/jquery.min.js')
    urlretrieve('https://ajax.googleapis.com/ajax/libs/jqueryui/1.10.3/jquery-ui.min.js', currentDirPass + '/views/jQuery/jquery-ui.min.js')
    urlretrieve('https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js', currentDirPass + '/views/jQuery/bootstrap.min.js')
if not (os.path.exists(currentDirPass+'/views/css') or os.path.exists(currentDirPass+'/views/js') or os.path.exists(currentDirPass+'/views/fonts')):
    install_bootstrap()
if not (os.path.exists(currentDirPass+'/views/jquery')):
    install_jQuery()
try:
    from bottle import get, post, route, run, static_file, response, abort, redirect, request, template, os, view
except ImportError:
    install_bottle()
    from bottle import get, post, route, run, static_file, response, abort, redirect, request, template, os, view
#ダウンロード
@route('/download/<filename:path>')
def download(filename):
    return static_file(filename, root = currentDirPass + '/bin', download=filename)
#エラーページ
@route('/restricted')
def restricted():
    abort(401, "Sorry, your access denied!")
@route('/views/<filepath:path>', name='static_file')
def static(filepath):
    return static_file(filepath, root="./views")
#インデックスページ(ファイルアップロード)
@get('/')
@view('index')
def index():
    return dict()
@route('/', method='POST')
def do_upload():
    upload = request.files.get('upload')
    name, ext = os.path.splitext(upload.filename)
    savePath = currentDirPass + '/bin'
    upload.save(save_path)
    redirect("/e/"+name+ '.'+ext)
@route('e/<filename>')
@view('editor')
def editor():
    return dict()
@route('/e/<filename>', method='POST')
@view('editor')
def edit():
    request.forms.get('')
    return dict()
#テスト用
@route('/test')
@view('index')
def test():
    return dict()
run(host='localhost', port=8080, debug=True)#サーバー起動
