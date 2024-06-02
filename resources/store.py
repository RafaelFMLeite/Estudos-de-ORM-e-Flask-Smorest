from models import StoreModel
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import db
from schemas import StoreSchema, StoreUpdateSchema

blp = Blueprint("stores", __name__, description="Operations on stores")

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
       store = StoreModel.querry.get_or_404(store_id)
       return store
    def delete(self, store_id):
      
      store = StoreModel.query.get_or_404(store_id)
      
      try:
          db.session.delete(store)
          db.session.commit()

      except SQLAlchemyError:
          abort(500, message="An error occured while deleting the store")

      return {"message": "store deleted"}

    blp.arguments(StoreUpdateSchema)
    @blp.response(200, StoreSchema)
    def put(self, store_id, store_data):
        
        store = StoreModel.querry.get_or_404(store_id)
        
        if store:
            store.name = store_data["name"]
        else:
            store = StoreModel(id = store_id, **store_data)

        try:
            db.session.add(store)
            db.session.commit()

        except SQLAlchemyError:
            abort(500, message="An error occured while inserting the store")

        return store
           
@blp.route("/store")
class StoreList(MethodView):

    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A store with that name already exists")
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the store")
        return store
