from flask import Flask, request
from db import stores, items
import uuid
from flask_smorest import abort

app = Flask(__name__)

@app.get('/store')
def get_all_stores():
    return{'stores': list(stores.values())}

@app.get('/store/<string:store_id>')
def get_single_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
         abort(404, message='store not found')

@app.post('/store')
def create_store():
    store_id  = uuid.uuid4().hex
    store_data = request.get_json()

    if 'name' not in store_data:
        abort(400, message='Bad request. Ensure all the informations are provided')
    
    for store in stores.values():
         if store_data['name']==store['name']:
             abort(400, message='store already exists')
    
    new_store = {**store_data, 'id': store_id}
    stores[store_id] = new_store
    return new_store, 201

@app.post('/item')
def create_item():
    item_data = request.get_json()

    if(
        'price' not in item_data or
        'store_id' not in item_data or 
        'name' not in item_data
    ):
         abort(400, message='Bad request. Ensure all the informations are provided')

    for item in items.values():
         if (item_data['name']==item['name'] and 
             item_data['store_id']==item['store_id']):
             abort(400, message='item already exists')

    if item_data['store_id'] not in stores:
        abort(404, message='store not found')

    item_id = uuid.uuid4().hex
    item = {**item_data, 'id': item_id}
    items[item_id] = item

    return item[item_id], 201

@app.get('/item/<string:item_id>')
def get_item(item_id):
    if item_id not in items:
            abort(404, message='item not found')
    return items[item_id]

@app.get('/item')
def get_all_items():
    return {'items': list(items.values())}

@app.delete('/item<string:item_id>')
def delete_item(item_id):
    try:
        del items[item_id]
        return {'message': 'item deleted'}
    except KeyError:
        abort(404, message='item not found')

@app.delete('/store/<string:store_id>')
def delete_store(store_id):
    try:
        del stores[store_id]
        return {'message': 'store deleted'}
    except KeyError:
        abort(404, message='store not found')

@app.put('/item/<string:item_id>')
def update_item(item_id):
    item_data = request.get_json()
    if 'price' not in item_data or 'name' not in item_data:
        abort(400, message='Bad request. Ensure all the informations are provided')
    try:
        item = items[item_id]
        item.update(item_data)

        return item
    except KeyError:
        abort(404, message='item not found')

@app.put('/store/<string:store_id>')
def update_store(store_id):
    store_data = request.get_json()
    if 'name' not in store_data:
        abort(400, message='Bad request. Ensure all the informations are provided')
    try:
        store = stores[store_id]
        store.update(store_data)

        return store
    except KeyError:
        abort(404, message='store not found')