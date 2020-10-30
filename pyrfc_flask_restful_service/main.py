from flask import Flask, request, make_response, jsonify
from SAP.GL import SAPGL

app = Flask(__name__)


@app.route("/")
def index():
    return "index page"


@app.route("/accbal/<cocd>/<account>/<year>")
def get_acc_balances(cocd, account, year):
   
    sap_gl = SAPGL();
    ac_balances = sap_gl.get_ac_balances(str.upper(cocd), account, year)

    resp = make_response(ac_balances, 200)
    resp.headers['Content-Type'] = 'application/json'    

    return resp


@app.route("/acclist/<cocd>")
def get_gl_acc_list(cocd):

    sap_gl = SAPGL();
    gl_list = sap_gl.get_gl_acc_list(str.upper(cocd), '1')

    resp = make_response(gl_list, 200)
    resp.headers['Content-Type'] = 'application/json'    

    return resp


@app.route('/balances/<cocd>/<year>')
def get_all_acc_balances(cocd, year):  
    sap_gl = SAPGL();
    balances = sap_gl.get_all_acc_balances(str.upper(cocd), year)
    return jsonify(balances)


if __name__ == "__main__":
    app.run()