from services.fastapi import App
from app.routes.routers import auth, developments
from app.models.static_dir import StaticDir

app = App(
    routers=[
        auth.router,
        developments.router
    ],
    static_dirs=[
        StaticDir(name='public', path='public')
    ]
).get_app()

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=3000)