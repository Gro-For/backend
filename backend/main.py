from app import app
from app.models import config

if __name__ == 'main':
    print(config)
    print('HELLLOO')
    app.run()