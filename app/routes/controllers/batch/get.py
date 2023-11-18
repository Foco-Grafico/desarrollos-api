from fastapi import HTTPException
from services.db import colina_db
import math
from app.models.batch import FilterBatch, FilterOperation
from app.enums.statuses import STATUS_BATCH

async def get_batches():
    batches = colina_db.fetch_all(
        sql="SELECT * FROM batches"
    )

    if not batches:
        raise HTTPException(
            status_code=404,
            detail="No batches found"
        )

    for batch in batches:
        batch['assets'] = colina_db.fetch_all(
            sql="SELECT * FROM batch_assets WHERE batch_id = %s",
            params=(batch['id'],)
        )

        batch['payment_plans'] = colina_db.fetch_all(
            sql="SELECT * FROM batch_payment_plans WHERE batch_id = %s",
            params=(batch['id'],)
        )

    return {
        'message': 'Batches found',
        'data': batches
    }

async def get_batch_in_dev(filters: FilterBatch, development_id:int, elements: int = 50, page: int = 1):
    dev_db = colina_db.fetch_one(
        sql="SELECT id FROM developments WHERE id = %s",
        params=(development_id,)
    )

    if not dev_db:
        raise HTTPException(status_code=404, detail="Development not found")

    sql_batches = u"SELECT b.*, UUID() as `key` FROM batches b WHERE development_id = %s AND status = %s {filters_formatted} LIMIT %s OFFSET %s"

    filters_sql = ''

    for key, value in filters:
        if isinstance(value, list):
            for operation in value:
                if isinstance(operation, FilterOperation):
                    filters_sql += f" AND {key} {operation.operator} '{operation.value}'"
            continue

        if value is not None:
            filters_sql += f" AND {key} = '{value}'"

    sql_batches = sql_batches.format(filters_formatted=filters_sql)

    batch_db = colina_db.fetch_all(
        sql=sql_batches,
        params=(development_id, STATUS_BATCH.AVAILABLE.value, elements, (page - 1) * elements)
    )

    if not batch_db:
        raise HTTPException(status_code=404, detail="Batch not found")

    for batch in batch_db:
        batch['assets'] = colina_db.fetch_all(
            sql="SELECT * FROM batch_assets WHERE batch_id = %s",
            params=(batch['id'],)
        )

        batch['payment_plans'] = colina_db.fetch_all(
            sql="SELECT * FROM batch_payment_plans WHERE batch_id = %s",
            params=(batch['id'],)
        )

        batch['status'] = colina_db.select_one(
            table='batch_status',
            where={'id': batch['status']},
            columns=['*']
        )

    return {
        'message': 'Batch found successfully',
        'data': batch_db,
        'max_pages': math.ceil(colina_db.fetch_one(
            sql=u"SELECT count(*) as counter FROM batches WHERE development_id = %s AND status = %s {filters_formatted}".format(filters_formatted=filters_sql),
            params=(development_id, STATUS_BATCH.AVAILABLE.value)
        )['counter'] / elements),
        'page': page
    }

async def get_batches_types():
    types = colina_db.select(
        table = 'batch_types',
        columns=['*', 'UUID() as `key`']
    )

    return {
        'message': 'Batch types found successfully',
        'data': types
    }
