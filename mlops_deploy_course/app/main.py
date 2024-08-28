from flask import Flask, request, jsonify
from flask_basicauth import BasicAuth
from textblob import TextBlob
from googletrans import Translator
from sklearn.linear_model import LinearRegression
import pickle
import os

modelo = pickle.load(open('../../models/modelo.sav', 'rb'))

app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = os.environ.get('BASIC_AUTH_USERNAME')
app.config['BASIC_AUTH_PASSWORD'] = os.environ.get('BASIC_AUTH_PASSWORD')

basic_auth = BasicAuth(app)

@app.route('/')
def home():
    return 'Minha primeira API.'

@app.route('/sentimento/<frase>')
@basic_auth.required
def sentimento(frase):
    translator = Translator()
    frase_en = translator.translate(frase, dest='en')
    tb_en = frase_en.text
    tb_en = TextBlob(tb_en)
    polaridade = tb_en.sentiment.polarity
    return f"A polaridade da frase é: {str(polaridade)}"

@app.route('/cotacao/', methods=['POST'])
@basic_auth.required
def cotacao():
    parametros = request.get_json()
    preco = modelo.predict([[parametros['tamanho'], parametros['ano'], parametros['garagem']]])[0]
    return jsonify({
        "resultado": f"O preço previsto para o tamanho da casa é: {preco}"
    })

app.run(debug=True, host='0.0.0.0')