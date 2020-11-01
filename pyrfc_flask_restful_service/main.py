from flask import Flask, request, make_response, jsonify
from SAP.GL import SAPGL
from SAP.table_info import SAPTableInfo

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] =False

@app.route("/")
def index():
    return "index page"


@app.route("/accbal/<cocd>/<account>/<year>")
def get_acc_balances(cocd, account, year):
    sap_gl = SAPGL();
    acc_balances = sap_gl.get_acc_balances(str.upper(cocd), account, year)

    return jsonify(acc_balances)


@app.route("/acclist/<cocd>")
def get_gl_acc_list(cocd):
    sap_gl = SAPGL();
    gl_list = sap_gl.get_gl_acc_list(str.upper(cocd), '1')

    return jsonify(gl_list)


@app.route('/balances/<cocd>/<year>')
def get_all_acc_balances(cocd, year):  
    sap_gl = SAPGL();
    balances = sap_gl.get_all_acc_balances(str.upper(cocd), year)
    return jsonify(balances)


@app.route('/tabledata/<tablename>/<int:rowcnt>')
def get_table_data(tablename, rowcnt):
    sap_table = SAPTableInfo()
    data = sap_table.read_table(tablename, rowcount=rowcnt)
    return jsonify(data)


@app.route('/tablefields/<tablename>')
def get_table_fields(tablename):
    sap_table = SAPTableInfo()
    fields = sap_table.get_table_fields(tablename)
    return jsonify(fields)


if __name__ == "__main__":
    app.run()