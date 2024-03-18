from app import app
from utils.wp_post.auto_system import *
from utils.wp_post.crud import *


if __name__ == '__main__':
    autosystem()
    app.run(debug=True, host='0.0.0.0', port=8080)