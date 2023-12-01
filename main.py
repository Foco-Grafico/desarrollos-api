from services.fastapi import App
from app.routes.routers import auth, developments, role, batch, payment_plan, seller, status
from app.models.static_dir import StaticDir
import socketio
from services.whatsapp.messages import receive_message
from app.utils.env import Env


app = App(
    routers=[
        status.router,
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



sio = socketio.Client()
sio.connect(Env.get_secure('WA_SOCKET'))
sio_app = socketio.ASGIApp(sio)

app.mount('/', sio_app, name='socket.io')

sio.on('message', receive_message)
