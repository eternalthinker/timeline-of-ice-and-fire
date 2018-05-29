from flask import Flask, request, jsonify


app = Flask(__name__)
app.config["SECRET_KEY"] = "Very very very secret key"

@app.route("/diff", methods=['POST'])
def get_analytics():
    curr_data = request.json['curr_data']
    prev_data  =  request.json['prev_data']
    curr_data_dict = {}
    prev_data_dict = {}
    add = []
    reuse = []
    deaths = []
    reverseDeaths = []
    remove = []
    for item in curr_data:
        curr_data_dict[item['slug']] = item

    for item in prev_data:
        prev_data_dict[item['slug']] = item

    for i in curr_data:
        slug = i['slug']
        if slug in prev_data_dict:
            curr_alive = i['isAlive']
            pre_Alive =  prev_data_dict[slug]['isAlive']
            if pre_Alive == 1 and not curr_alive == 1:
                deaths.append(i)
            elif not pre_Alive == 1 and curr_alive == 1:
                reverseDeaths.append(i)
            reuse.append(i)
        else:
            add.append(i)

    for i in prev_data:
        slug = i['slug']
        if slug not in curr_data_dict:
            remove.append(i)

    return jsonify({ 'add': add, 'reuse': reuse, 'deaths':deaths, 'reverseDeaths': reverseDeaths, 'remove':remove})


@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    header['Access-Control-Allow-Headers'] = "Content-Type, x-access-token, Accept"
    header['Access-Control-Allow-Methods'] = "GET, POST, DELETE"
    return response


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5001)
