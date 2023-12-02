import pdfkit
import jinja2
import asyncio

async def create_pdf(route_html: str, info, time, route_css= str or None):
    name_html = route_html.split('/')[-1]
    route_html = route_html.replace(name_html, '')
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(route_html))
    template = env.get_template(name_html)
    html = template.render(info=info, time=time)
    
    # table
    options = {
        'page-size': 'Letter',
        'margin-top': '0.1in',
        'margin-right': '0.1in',
        'margin-bottom': '0.1in',
        'margin-left': '0.1in',
        'encoding': 'UTF-8',
        'no-outline': None
    }
    config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
    route_save = "C:\\Users\\dg047\\OneDrive\\Escritorio\\focogf\\desarrollos-api\\app\\routes\\controllers\\batch\\pdf"
    pdfkit.from_string(html, route_save + "\\mi_documento.pdf", options=options, css=route_css, configuration=config)
    print(route_html)
    print(name_html)
    # Definir variables con valores proporcionados

id = "id"
data_id = 1

area = "area"
data_area = 321

price = "price"
data_price = 6

perimeter = "perimeter"
data_perimeter = 147

longitude = "longitude"
data_longitude = 147

coords = "coords"
data_coords = "si"

amenities = "amenities"
data_amenities = "si"

development_id = "development_id"
data_development_id = 1

currency = "currency"
data_currency = "usd"

location = "location"
data_location = "sad"

sq_m = "sq_m"
data_sq_m = 1

status_id = "status_id"
status_name = "name"
data_status_id = 1
data_status_name = "Disponible"

assets_id = "assets_id"
batch_id = "batch_id"
asset_url = "asset_url"
data_assets_id = 1
data_batch_id = 1
data_asset_url = "public/batches/00dbd1ab-6e0e-4870-a03a-6092c7f6425b-WhatsApp Image 2023-11-04 at 8.34.19 PM.jpeg"

# Crear una lista de activos
assets = [
    {
        assets_id: data_assets_id,
        batch_id: data_batch_id,
        asset_url: data_asset_url
    }
]

# Crear una lista de planes de pago vacía
payment_plans = []

# Crear un diccionario con la estructura proporcionada
data_dict = {
    "message": "Batch found successfully",
    "data": {
        id: data_id,
        area: data_area,
        price: data_price,
        perimeter: data_perimeter,
        longitude: data_longitude,
        coords: data_coords,
        amenities: data_amenities,
        development_id: data_development_id,
        currency: data_currency,
        location: data_location,
        sq_m: data_sq_m,
        "status": {
            status_id: data_status_id,
            status_name: data_status_name
        },
        "assets": assets,
        "payment_plans": payment_plans
    }
}

# Imprimir el diccionario resultante
print(data_dict)


if __name__ == '__main__':
    route_html = 'app/routes/controllers/batch/pdf/mi_documento.html'
    info = data_dict
    time = 'Hola mundo'
    print(info)
    async def main():
        await create_pdf(route_html, info, time)

    asyncio.run(main())
    asyncio.run(main())
