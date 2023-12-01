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

# whats_client = WhatsClient(
#     token='EAAX0Spl0G3oBAPdy7NFl8Ta6swZBzrPlgKbSGvfyPj5J7NFTO14Pr40avW5vZCrNK05JgHPd60iFKcILObwP9LLfIDzg4bZAwFWK4wCy0mInCsyjrXBzdx4f3KLwhnQs2ZABojWlX6RXt6j2YjMTXGB3q2AaDBgqOHABsjDj2Vp7DGJDJMBd',
#     socket='https://stellar-extreme-wedelia.glitch.me',
#     tel_id='114899638230787'
# )

sio = socketio.Client()
sio.connect(Env.get_secure('WA_SOCKET'))
sio_app = socketio.ASGIApp(sio)

app.mount('/', sio_app, name='socket.io')

sio.on('message', receive_message)
