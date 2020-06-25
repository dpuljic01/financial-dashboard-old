from application import create_app

# import os
# BASE_DIR = os.path.join(os.path.dirname(__file__))


application = app = create_app()

if __name__ == "__main__":
    app.run()
