from flask import Flask, request, make_response, jsonify
from SAP.GL import SAPGL

app = Flask(__name__)


@app.route("/")
def index():
    return "index page"


@app.route("/accbal")
def get_acc_balances():
    cocd = request.args.get('cocd')
    account = request.args.get('account')
    year = request.args.get('year')

    sap_gl = SAPGL();
    ac_balances = sap_gl.get_ac_balances(cocd, account, year)

    resp = make_response(ac_balances, 200)
    resp.headers['Content-Type'] = 'application/json'    

    return resp


@app.route("/acclist")
def get_gl_acc_list():
    cocd = request.args.get('cocd')
    lang = request.args.get('lang')

    sap_gl = SAPGL();
    gl_list = sap_gl.get_gl_acc_list(cocd, lang)

    resp = make_response(gl_list, 200)
    resp.headers['Content-Type'] = 'application/json'    

    return resp


@app.route('/balances')
def get_all_acc_balances():
    cocd = request.args.get('cocd')
    fiscal_year = request.args.get('year')

    sap_gl = SAPGL();
    balances = sap_gl.get_all_acc_balances(cocd, fiscal_year)
    return jsonify(balances)


if __name__ == "__main__":
    app.run()