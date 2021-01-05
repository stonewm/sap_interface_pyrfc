from flask import Flask, make_response, jsonify, request
from SAP.table_info import SAPTableInfo


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] =False


@app.route("/")
def index():
    return "index page"


@app.route('/tabledata/<tablename>/<int:rowcnt>')
def get_table_data(tablename, rowcnt):
    options = request.args.get('options')

    sap_table = SAPTableInfo()
    if options == None:
        data = sap_table.read_table(tablename, rowcount=rowcnt)
    else:
        data = sap_table.read_table(tablename, rowcount=rowcnt, filter_criteria=options)
    return jsonify(data)


@app.route('/tablefields/<tablename>')
def get_table_fields(tablename):
    sap_table = SAPTableInfo()

    fields = sap_table.get_table_fields(tablename)
    return jsonify(fields) 


if __name__ == "__main__":
    app.run()