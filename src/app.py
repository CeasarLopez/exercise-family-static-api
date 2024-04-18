import os
from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

jackson_family = FamilyStructure("Jackson")

initial_members = [
    {"first_name": "John", "age": 33, "lucky_numbers": [7, 13, 22]},
    {"first_name": "Jane", "age": 35, "lucky_numbers": [10, 14, 3]},
    {"first_name": "Jimmy", "age": 5, "lucky_numbers": [1]}
]

for member in initial_members:
    jackson_family.add_member(member)

@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):
    member = jackson_family.find_member(id)
    if member is None:
        abort(404, description="Member not found")
    return jsonify(member), 200

@app.route('/member', methods=['POST'])
def add_member():
    if not request.json or not 'id' in request.json or not 'first_name' in request.json:
        abort(400, description="Missing mandatory member fields")

    new_member = {
        'id': request.json['id'],
        'first_name': request.json['first_name'],
        'age': request.json.get('age', 0),
        'lucky_numbers': request.json.get('lucky_numbers', [])
    }

    if jackson_family.find_member(new_member['id']) is not None:
        abort(400, description="Member with the same ID already exists")

    jackson_family.add_member(new_member)
    return jsonify(new_member), 200

@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):
    if not jackson_family.find_member(id):
        abort(404, description="Member not found")
    
    jackson_family.delete_member(id)
    return jsonify({'done': True}), 200

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)





