from services.whatsapp.models.wa_models import Interactive, Msg, MsgUser, Contact, Button, Buttons
from services.whatsapp.enums.wa_enums import MsgTypes
from services.whatsapp.controller.send import send_controller, mark_as_read_message
from services.db import colina_db
import re

def format_message(msg) -> Msg | None:
    try:
        status = msg['entry'][0]['changes'][0]['value']['statuses'] if msg['entry'][0]['changes'][0]['value']['statuses'] else None
    except:
        status = None


    if status:
        return

    def find_message_type(msg):
        if msg['entry'][0]['changes'][0]['value']['messages'][0]['type'] == MsgTypes.text.name:
            return msg['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
        
        if msg['entry'][0]['changes'][0]['value']['messages'][0]['type'] == MsgTypes.interactive.name:
            return Interactive(
                id=msg['entry'][0]['changes'][0]['value']['messages'][0][MsgTypes.interactive.name][msg['entry'][0]['changes'][0]['value']['messages'][0][MsgTypes.interactive.name]['type']]['id'],
                title=msg['entry'][0]['changes'][0]['value']['messages'][0][MsgTypes.interactive.name][msg['entry'][0]['changes'][0]['value']['messages'][0][MsgTypes.interactive.name]['type']]['title']
            )

    user = MsgUser(
        name=msg['entry'][0]['changes'][0]['value']['contacts'][0]['profile']['name'],
        number=msg['entry'][0]['changes'][0]['value']['contacts'][0]['wa_id']
    )

    new_msg = Msg(
        id=msg['entry'][0]['changes'][0]['value']['messages'][0]['id'],
        message=find_message_type(msg),  # type: ignore
        type=msg['entry'][0]['changes'][0]['value']['messages'][0]['type'],
        user=user
    )

    return new_msg

def receive_message(u_msg):
    msg = format_message(u_msg)

    if not msg:
        return
    
    mark_as_read_message(msg.id)

    if isinstance(msg.message, Interactive):
        name = msg.message.id.split(' ')[0]

        if name == 'accept_seller':
            print('accept_seller')
            match = re.search(r'batch"(\d+)" client_p"(\d+)" client_n"(.+?)"', msg.message.id)

            if match:
                batch_id = match.group(1)
                client_phone = match.group(2)
                client_name = match.group(3)

                seller = colina_db.fetch_one(
                    sql='SELECT phone FROM sellers WHERE id IN (SELECT seller_id FROM batch_sellers WHERE batch_id = %s AND client_phone = %s)',
                    params=(batch_id, client_phone)
                )

                if not seller:
                    send_controller('Tu no eres un vendedor.', msg.user.number)
                    return
                
                if seller['phone'] != msg.user.number:
                    send_controller('Has tardado mas de 5min, este cliente se ha asignado a otro vendedor', msg.user.number)
                    return
                
                batch_sell = colina_db.select_one(
                    table='batch_sellers',
                    where={
                        'batch_id': batch_id,
                        'client_phone': client_phone
                    },
                    columns=['*']
                )

                pdf = u'http://192.168.0.10:4321/cotizacion?clientName={client_name}&clientMail={client_email}&clientPhone={client_phone}&batchId={batch_id}&devname={dev_name}'

                dev = colina_db.fetch_one(
                    sql='SELECT name FROM developments WHERE id IN (SELECT development_id FROM batches WHERE id = %s)',
                    params=(batch_id,)
                )

                pdf_formatted = pdf.format(
                    client_name=client_name,
                    client_email=batch_sell['client_mail'],
                    client_phone=client_phone,
                    batch_id=batch_sell['batch_id'],
                    dev_name=dev['name']
                )

                colina_db.update(
                    table='batch_sellers',
                    data={
                        'status': 'accepted'
                    },
                    where=f'batch_id = {batch_id} AND client_phone = {client_phone}'
                )

                client = Contact(
                    name=client_name,
                    phone=client_phone
                )

                send_controller(client, msg.user.number)
                send_controller(
                    to=msg.user.number,
                    message=Buttons(
                        body=f'Se te ha asignado un nuevo cliente: {client.name} - {client.phone}',
                        buttons=[
                            Button(
                                execute=f'batch_appart batch"{batch_id}"',
                                title='Apartar lote'
                            )
                        ]
                    )
                )

                send_controller('un vendedor se pondra en contacto rightnow', client_phone)



    # send_controller('buenas', msg.user.number)