from bson import ObjectId
from flask import Flask, jsonify
from flask import request
from marshmallow import fields, Schema
import uuid

from model import table_animal
from validate.animal_validate import AnimalUpdateSchema, AnimalCreateSchema

app = Flask(__name__)
PREFIX_API = "/api/v1{}"
port = 8000


# category = [
#     {'id': str(uuid.uuid4()), 'name': 'Monkey', 'color': 'Brown', 'category': 'Mammal'},
#     {'id': str(uuid.uuid4()), 'name': 'Starling', 'color': 'Gray', 'category': 'Bird'},
#     {'id': str(uuid.uuid4()), 'name': 'Goldfish', 'color': 'Brown', 'category': 'Fish'},
#     {'id': str(uuid.uuid4()), 'name': 'Frog', 'color': 'Brown', 'category': 'Amphibians'},
#     {'id': str(uuid.uuid4()), 'name': 'Turtle', 'color': 'Brown', 'category': 'Reptile'}]
#
#
# @app.route('/animal_category', methods=['GET'])
# def animal_category():
#     return jsonify(category)
#
#
# @app.route('/detail_animal', methods=['GET'])
# def detail_animal():
#     result = {}
#     id = request.args.get('id')
#     if id is None:
#         return jsonify({'Mess: ': 'Id invalid'})
#     for animal in category:
#         if animal.get('id') == id:
#             result = animal
#             break
#     return jsonify(result)
#
#
# @app.route('/add_animal', methods=['POST'])
# def add_animal():
#     body = request.get_json()
#     if body.get('name') and body.get('color') and body.get('category'):
#         animal_name = body.get('name')
#         check_exit = False
#         for animal in category:
#             if animal.get('name') == animal_name:
#                 check_exit = True
#                 break
#         if check_exit:
#             result = {'Mess: ': 'Duplicate  name'}
#         else:
#             body['id'] = str(uuid.uuid4())
#             category.append(body)
#             result = body
#         return jsonify(result)
#     else:
#         result = {'Mess': 'Check value'}
#         return jsonify(result)
#
#
# @app.route('/remove_animal', methods=['DELETE'])
# def remove_animal():
#     id = request.args.get('id')
#     if id is None:
#         return jsonify({'Mess: ': 'ID invalid'})
#     index = -1
#     for animal in category:
#         if animal.get('id') == id:
#             _index = category.index(animal)
#             index = _index
#     if index != -1:
#         del category[index]
#         result = {'Mess: ': 'Delete successfully'}
#     else:
#         result = {'Mess: ': 'Not Found'}
#     return jsonify(result)
#
#
# @app.route('/update_animal/<id>', methods=['PUT'])
# def update_animal(id):
#     body = request.get_json()
#     if body.get('name') and body.get('color') and body.get('category'):
#         check_exit = False
#         for animal in category:
#             if animal.get('id') == id:
#                 animal.update(body)
#                 check_exit = True
#         if check_exit is True:
#             result = {'Mess :': 'Update Successfully'}
#         else:
#             result = {'Mess': 'Not found Id'}
#         return jsonify(result)
#     return jsonify({'Mess: ': 'Check value'})


@app.route(PREFIX_API.format('/animals'), methods=['GET'])
def aniamls():
    list_animal = table_animal.find()
    list_animal = list(list_animal)
    for animal in list_animal:
        animal['_id'] = str(animal['_id'])  # ép kiểu từ ObjectId sang String
    return jsonify(list_animal)


@app.route(PREFIX_API.format('/animals'), methods=['POST'])
def add_animal():
    body = request.get_json()
    # check validate
    try:
        animal_schema = AnimalCreateSchema()
        animal_schema.load(body)
    except Exception as err:
        return jsonify({"code": 1, "message": list(err.args)[0]}), 400

    # save document animal to table_animal
    result_insert = table_animal.insert_one(body)
    animal_id = str(result_insert.inserted_id)

    # return data insert and id animal in  data
    body['_id'] = animal_id
    return jsonify(body)


@app.route(PREFIX_API.format('/animals/<animal_id>'), methods=['PUT'])
def update_animal(animal_id):
    # get data animal to body with content type application/json
    body = request.get_json()

    # validate animal_id
    if not animal_id:
        return jsonify({"code": 1, "message": "Param invalid"}), 400

    # validate data body
    animal_schema = AnimalUpdateSchema()
    try:
        animal_schema.load(body)
    except Exception as err:
        return jsonify({"code": 1, "message": list(err.args)[0]}), 400

    # check exists animal by id
    animal = table_animal.find_one(ObjectId(animal_id), {"_id": 1})

    if animal:
        # update data animal from body
        result_update = table_animal.update_one({"_id": ObjectId(animal_id)}, {"$set": body})

        # print check result update animal
        print("update_animal: result_update: {}".format(result_update))

        # mapping data update to animal old
        animal.update(body)

        # convert ObjectId primary Mongodb to string uuid
        animal['_id'] = str(animal.get("_id", animal_id))

        # return data animal update
        return jsonify(animal), 200

    # check animal not found -> return err not found animal
    return jsonify({"code": 1, "message": "Animal not found!"}), 404


@app.route(PREFIX_API.format('/animals/<animal_id>'), methods=['DELETE'])
def remove_animal(animal_id):
    list_animal = table_animal.find()
    list_animal = list(list_animal)
    if not animal_id:
        return jsonify({"code": 1, "message": "Param invalid"}), 400
    # animal_del = table_animal.find_one(ObjectId(animal_id), {"_id": 1})
    # for animal in list_animal:
    #     animal['_id'] = str(animal['_id'])
    #
    #     if animal['_id'] == animal_id:
    #         del animal_del['_id']
    #         return jsonify({'Mess: ': 'Delete successfully'})
    # return jsonify({'Mess: ': 'Not Found'})
    return jsonify({"code": 1, "message": "Animal not found!"}), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=port, debug=True)
