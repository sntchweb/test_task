from datetime import datetime

import pymongo
from dateutil.relativedelta import relativedelta


async def calc_result(date_from, date_upto, type):
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['ttt']
    collection = db['my_test_collection']

    dt_from = datetime.fromisoformat(date_from)
    dt_upto = datetime.fromisoformat(date_upto)
    group_type = type

    data = collection.find({'dt': {'$gte': dt_from, '$lte': dt_upto}})

    agg_data = {}
    for record in data:
        group_key = None
        if group_type == 'hour':
            group_key = record['dt'].replace(minute=0, second=0, microsecond=0)
        elif group_type == 'day':
            group_key = record['dt'].replace(
                hour=0, minute=0, second=0, microsecond=0
            )
        elif group_type == 'month':
            group_key = record['dt'].replace(
                day=1, hour=0, minute=0, second=0, microsecond=0
            )
        if group_key not in agg_data:
            agg_data[group_key] = 0
        agg_data[group_key] += record['value']

    dataset, labels = [], []
    if group_type == 'hour':
        delta = relativedelta(hours=1)
    elif group_type == 'day':
        delta = relativedelta(days=1)
    elif group_type == 'month':
        delta = relativedelta(months=1)
    current_date = dt_from
    while current_date <= dt_upto:
        if current_date in agg_data:
            dataset.append(agg_data[current_date])
        else:
            dataset.append(0)
        labels.append(current_date.isoformat())
        current_date += delta
    return {'dataset': dataset, 'labels': labels}
