from services.whatsapp.models.wa_models import Interactive, Msg, MsgUser, Contact, Button, Buttons, List, ListElement, SectionList, Header, HeaderTypes
from services.whatsapp.enums.wa_enums import MsgTypes
from services.whatsapp.controller.send import send_controller, mark_as_read_message
from services.db import colina_db
from app.utils.intervals import setTimeout, setInterval
from random import randint
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
                    sql='SELECT phone, id FROM sellers WHERE id IN (SELECT seller_id FROM batch_sellers WHERE batch_id = %s AND client_phone = %s)',
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
                    message=f'Se te ha asignado un nuevo cliente: {client.name} - {client.phone}\n.En aproximadamente un minuto podras interactuar con el apartado del lote.\npdf: {pdf_formatted}'
                )

                send_controller('Te hemos asignado un vendedor, se contactara contigo en unos instantes\n pdf: {pdf_formatted}', client_phone)

                setTimeout(60, lambda: send_controller(
                    to=client_phone,
                    message=Buttons(
                        body=f'¿Te ha contactado el vendedor?',
                        buttons=[
                            Button(
                                execute=f'is_contact batch"{batch_id}" client_n"{client_name}" seller_id"{seller["id"]}',
                                title='Si'
                            ),
                            Button(
                                execute=f'is_contact batch"{batch_id}" client_n"{client_name}"',
                                title='No'
                            )
                        ]
                    )
                ))

        if name == 'is_contact':
            match = re.search(r'batch"(\d+)" client_n"(.+?)" seller_id"(\d+)"', msg.message.id)

            if match:
                batch_id = match.group(1)
                client_name = match.group(2)
                seller_id = match.group(3)

                if msg.message.title == 'No':
                    seller = colina_db.fetch_one(
                        sql='SELECT phone FROM sellers WHERE id = %s',
                        params=(seller_id,)
                    )

                    send_controller(
                        to=seller['phone'],
                        message=f'El cliente {client_name} ha dicho que no lo has contactado, si esto es falso, por favor contacta con un moderador.'
                    )

                    send_seller_message = lambda seller_phone: send_controller(
                        to=seller_phone,
                        message=Buttons(
                            body='Hola, te presento a un nuevo cliente potencial',
                            buttons=[
                                Button(
                                    execute=f'accept_seller batch"{batch_id}" client_p"{msg.user.number}" client_n"{client_name}"',
                                    title='Aceptar'
                                )
                            ],
                            footer='Tienes 5 min para aceptar.'
                        )
                    )

                    batch = colina_db.select_one(
                        table='batches',
                        where={
                            'id': batch_id
                        },
                        columns=['development_id']
                    )

                    sellers = colina_db.fetch_all(
                        sql='SELECT * FROM sellers WHERE id IN (SELECT seller_id FROM developments_sellers WHERE development_id = %s)',
                        params=(batch['development_id'],)
                    )

                    get_random_seller = lambda: sellers[randint(0, len(sellers) - 1)]

                    send_controller('De acuerdo, buscaremos otro vendedor para ti.', msg.user.number)

                    random_seller = get_random_seller()
                    send_seller_message(random_seller['phone'])

                    colina_db.update(
                        table='batch_sellers',
                        data={
                            'status': 'pending',
                            'seller_id': random_seller['id']
                        },
                        where=f'batch_id = {batch_id} AND client_name = {client_name}'
                    )

                    def action(inter: setInterval):
                        batch_seller = colina_db.fetch_one(
                            sql='SELECT status FROM batch_sellers WHERE batch_id = %s AND client_phone = %s',
                            params=(batch_id, msg.user.number)
                        )

                        if batch_seller['status'] == 'pending':
                            new_random_seller = get_random_seller()
                            
                            while new_random_seller['id'] == random_seller['id']:
                                new_random_seller = get_random_seller()

                            send_seller_message(new_random_seller['phone'])
                            colina_db.update(
                                table='batch_sellers',
                                data={
                                    'seller_id': new_random_seller['id']
                                },
                                where=f'batch_id = {batch_id} AND client_phone = {msg.user.number}'
                            )
                        else:
                            inter.cancel()

                    setInterval(
                        interval=20,
                        action=action
                    )
                    return

                batch_sell = colina_db.select_one(
                    table='batch_sellers',
                    where={
                        'batch_id': batch_id,
                        'client_phone': msg.user.number
                    },
                    columns=['*']
                )

                seller = colina_db.select_one(
                    table='sellers',
                    where={
                        'id': seller_id
                    },
                    columns=['*']
                )

                if not seller:
                    send_controller('Parece que ha ocurrido un error y no hemos encontrado a tu vendedor.', msg.user.number)
                    return
                
                send_controller(
                    to=seller['phone'],
                    message=f'El cliente {client_name} ha dicho que lo has contactado, si esto es falso, por favor contacta con un moderador.'
                )

                send_controller(
                    to=seller['phone'],
                    message=Buttons(
                        body=f'Te otorgamos un boton para bloquear el lote, precionalo al recibir el apartado del mismo.\nEn caso de error, consulta con un moderador.',
                        buttons=[
                            Button(
                                execute=f'block seller_id"{seller["id"]}" batch"{batch_id}" client_n"{client_name}"',
                                title='Bloquear'
                            )
                        ]
                    )
                )

                send_controller(
                    to=msg.user.number,
                    message=List(
                        header=Header(
                            type=HeaderTypes.text,
                            text='Gracias por tu respuesta'
                        ),
                        body=f'Califica tu experiencia con el vendedor {seller["name"]}',
                        sections=[
                            SectionList(
                                title='Calificacion',
                                rows=[
                                    ListElement(
                                        execute=f'seller_quality quality"1" seller_id"{seller["id"]}"',
                                        title='Muy malo',
                                        description='⭐'
                                    ),
                                    ListElement(
                                        execute=f'seller_quality quality"2" seller_id"{seller["id"]}"',
                                        title='Malo',
                                        description='⭐⭐'
                                    ),
                                    ListElement(
                                        execute=f'seller_quality quality"3" seller_id"{seller["id"]}"',
                                        title='Regular',
                                        description='⭐⭐⭐'
                                    ),
                                    ListElement(
                                        execute=f'seller_quality quality"4" seller_id"{seller["id"]}"',
                                        title='Bueno',
                                        description='⭐⭐⭐⭐'
                                    ),
                                    ListElement(
                                        execute=f'seller_quality quality"5" seller_id"{seller["id"]}"',
                                        title='Muy bueno',
                                        description='⭐⭐⭐⭐⭐'
                                    )
                                ]
                            )
                        ],
                        button='Calificar'
                    )
                )


    # send_controller('buenas', msg.user.number)