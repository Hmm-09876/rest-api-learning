from flask import Flask, jsonify, request

app = Flask(__name__)

data = {"message": "hello"}
users = [{"id": 1, "name": "Phuc"},
         {"id": 2, "name": "John"},
         {"id": 3, "name": "Alice"},
         {"id": 4, "name": "Bob"},
         {"id": 5, "name": "Charlie"},
         {"id": 6, "name": "David"},
         {"id": 7, "name": "Eve"},
         {"id": 8, "name": "Frank"},
         {"id": 9, "name": "Grace"},
         {"id": 10, "name": "Heidi"}]


@app.get("/")
def get_data():
    return jsonify(data)


@app.route("/users", methods=["GET", "POST"])
def users_route():
    method = request.method

    if method == "GET":
        name = request.args.get("name")
        limit = request.args.get("limit", type=int, default=3)
        page = request.args.get("page", type=int, default=1)
        has_pagination = "page" in request.args or "limit" in request.args

        if name:
            user = [u for u in users if u["name"] == name]
            if not user:
                return jsonify({"error": "user not found"}), 404
            return jsonify(user)

        if has_pagination:
            if limit > 0 and page > 0:
                end = limit * page
                return jsonify(users[end-limit:end])

            return jsonify({"error": "limit and page must be positive integers"}), 400


        return jsonify(users)
    

    data = request.get_json()
    if method == "POST":
        next_id = max(user["id"] for user in users) + 1

        if not data.get("id"):
            data["id"] = next_id

        if not data.get("name"):
            return jsonify({"error": "name is required"}), 400
        users.append(data)
        return jsonify(users), 201


@app.route("/users/<int:id>", methods=["GET", "PUT", "DELETE"])
def user_route(id):
    user = next((user for user in users if user["id"] == id), None)
    method = request.method

    if user:
        if method == "GET":
            return jsonify(user)
    

        elif method == "DELETE":
            users.remove(user)
            return jsonify({"message": "user deleted"})
            

        elif method == "PUT":
            data = request.get_json()
            if not data.get("name"):
                return jsonify({"error": "name is required"}), 400
            data.pop("id", None)
            user.update(data)
            return jsonify(user)

    else:
        return jsonify({"error": "user not found"}), 404
    


    

app.run(debug=True)

  

  