from backend.app import create_app
from backend.config import Config

app = create_app(Config)

if __name__ == '__main__':
    app.run(debug=True, port=5000)