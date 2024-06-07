from models import StoreModel
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import db
from schemas import StoreSchema, StoreUpdateSchema

from flask_jwt_extended import jwt_required, get_jwt

blp = Blueprint("Stores", "stores", __name__, description="Operations on stores")

@blp.route("/store/<int:store_id>")
class Store(MethodView):
    @jwt_required()
    @blp.response(200, StoreSchema)
    def get(self, store_id):
       store = StoreModel.querry.get_or_404(store_id)
       return store
    
    @jwt_required()
    def delete(self, store_id):
      jwt = get_jwt()
      
      if not jwt.get("is_admin"):
          abort(401, message="Admin privilege required")

      store = StoreModel.query.get_or_404(store_id)
      
      try:
          db.session.delete(store)
          db.session.commit()

      except SQLAlchemyError:
          abort(500, message="An error occured while deleting the store")

      return {"message": "store deleted"}
    
    @jwt_required()
    @blp.arguments(StoreUpdateSchema)
    @blp.response(200, StoreSchema)
    def put(self, store_id, store_data):
        jwt = get_jwt()
        
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required")

        store = StoreModel.querry.get_or_404(store_id)
        
        if store:
            store.name = store_data["name"]
        
        store = StoreModel(id = store_id, **store_data)
        
        try:
            db.session.add(store)
            db.session.commit()

        except SQLAlchemyError:
            abort(500, message="An error occured while inserting the store")

        return store
           
@blp.route("/store")
class StoreList(MethodView):
    @jwt_required()
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @jwt_required()
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        jwt = get_jwt()
        
        if not jwt.get("is_admin"): 
            abort(401, message="Admin privilege required")
        
        store = StoreModel(**store_data)
        
        try:
            db.session.add(store)
            db.session.commit()
        
        except IntegrityError:
            abort(400, message="A store with that name already exists")
        
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the store")
       
        return store
