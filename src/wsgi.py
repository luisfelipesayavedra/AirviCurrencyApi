from .main import app
from .scheduler import scheduler

if __name__ == '__main__':
    scheduler.start()
    app.run(debug=False)