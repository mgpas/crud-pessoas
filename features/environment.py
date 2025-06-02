from src.app import app

def before_all(context):
    app.testing = True
    context.client = app.test_client()
