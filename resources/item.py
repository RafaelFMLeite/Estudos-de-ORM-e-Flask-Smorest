from db import db
from sqlalchemy.exc import SQLAlchemyError
from flask_smorest import Blueprint, abort

from flask.views import MethodView
from schemas import ItemSchema, ItemUpdateSchema
from models import ItemModel

from flask_jwt_extended import jwt_required, get_jwt

blp = Blueprint("Items", "items", __name__, description="Operations on items")

@blp.route("/item/<int:item_id>")
class Item(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item
    
    @jwt_required()
    def delete(self, item_id):
        jwt = get_jwt()
        
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required")

        item = ItemModel.query.get_or_404(item_id)
        try:
            db.session.delete(item)
            db.session.commit()
        
        except SQLAlchemyError:
            abort(500, message="An error occured while deleting the item")

        return {"message": "item deleted"}
    @jwt_required()
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_id, item_data):
        jwt = get_jwt()
        
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required")

        item = ItemModel.query.get(item_id)
        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        
        else:
            item = ItemModel(id = item_id, **item_data)
        
        try:
            db.session.add(item)
            db.session.commit()
        
        except SQLAlchemyError:
            abort(500, message="An error occured while inserting the item")
        
        return item
        
@blp.route("/item")
class ItemList(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()
    
    @jwt_required()
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required")

        if ItemModel.query.filter_by(name=item_data["name"]).first():
            abort(409, message="An item with that name already exists.")
        
        item = ItemModel(**item_data)
        
        try:
            db.session.add(item)
            db.session.commit()
        
        except SQLAlchemyError:
            abort(500, message="An error occured while inserting the item")
        
        return item