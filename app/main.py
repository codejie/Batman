from fastapi import FastAPI
from .routers import test, auth

app = FastAPI(title='Batman')

app.include_router(test.router)
app.include_router(auth.router)

@app.get('/')
async def root():
    return {
        'App': 'Batman',
        'Description': 'I am rich.',
        'Version': '0.0.1'
    }