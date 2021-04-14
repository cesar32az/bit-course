from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def index():
    return {'data': {'name': 'Julio R'}}


def about():
    return {'data': 'about page'}
