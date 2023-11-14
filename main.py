from services.fastapi import App
from app.routes.routers import auth, developments, role, batch, payment_plan, seller
from app.models.static_dir import StaticDir

app = App(
    routers=[
        auth.router,
        role.router,
        seller.router,
        developments.router,
        payment_plan.router,
        batch.router
    ],
    static_dirs=[
        StaticDir(name='public', path='public')
    ]
).get_app()

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=3001)