from services.fastapi import App
from app.routes.routers import auth

app = App(
    routers=[
        auth.router
    ]
).get_app()

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=3000)