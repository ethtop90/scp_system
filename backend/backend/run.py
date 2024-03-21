from app import app
from utils.wp_post.auto_system import *
from utils.wp_post.crud import *
from flask import request, redirect


if __name__ == '__main__':
    autosystem()
    @app.before_request
    def before_request():
        if request.url.startswith('https://'):
            url = request.url.replace('https://', 'http://', 1)
            code = 301
            return redirect(url, code=code)
    app.run(debug=True, host='0.0.0.0', port=8080)