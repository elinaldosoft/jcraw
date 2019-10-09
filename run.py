from app import config

if __name__ == '__main__':
    app = config.create_app(config.app)
    app.run()
