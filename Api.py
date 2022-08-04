import jsonschema
import numpy as np
from flask import Flask, request, jsonify
from jsonschema import validate


# predict function
def predict(x, y):
    sum_t1 = W1[0] * x + W1[1] * y + b1
    h = 1 / (1 + np.exp(sum_t1))
    sum_t2 = h[0][0] * W2[0] + h[0][1] * W2[1] + b2
    o1 = 1 / (1 + np.exp(sum_t2[0]))
    return o1


# saved weight coefficients
W1 = np.array([[0.08669151, 0.70972208],
               [-0.15009617, 0.33882975]])
b1 = np.array([[-2.21261862, 0.0500741]])
W2 = np.array([[-0.67236509, -0.28416692],
               [-0.18318363, -0.80438505]])
b2 = np.array([[0.24321996, 0.62306239]])

mean_growth = 169.3
mean_weight = 62.8

# JSON schemas
men = {
    "Пол": "мужчина"
}
women = {
    "Пол": "женщина"
}

schema = {
    "type": "object",
    "properties": {
        "rost": {"type": "number", "minimum": 100, "maximum": 220},
        "ves": {"type": "number", "minimum": 30, "maximum": 150}
    },
}

# API Flask
app = Flask(__name__)


@app.route("/count", methods=["POST"])
def inf():
    data = request.get_json()
    # data validation
    try:
        validate(instance=data, schema=schema)
    except jsonschema.ValidationError as er:
        if er.validator == "type":
            error = {"Ошибка": "неверный тип данных"}
        elif er.validator == "minimum":
            error = {"Ошибка": "{} меньше {}".format(er.instance, er.validator_value)}
        else:
            error = {"Ошибка": "{} больше {}".format(er.instance, er.validator_value)}
        return jsonify(error)
    # get results
    growth = data["rost"]
    weight = data["ves"]
    growth = growth - mean_growth
    weight = weight - mean_weight
    rez = predict(growth, weight)
    # result select
    if rez[0] > rez[1]:
        return jsonify(men)
    else:
        return jsonify(women)


# error handlers
@app.errorhandler(500)
def internal_server_error(err):
    error = {"Ошибка": "сбой в программе"}
    return error


@app.errorhandler(400)
def internal_server_error(err):
    error = {"Ошибка": "неверный синтаксис запроса"}
    return error


app.run()

# example POST request
# {"rost": 150, "ves": 40}
