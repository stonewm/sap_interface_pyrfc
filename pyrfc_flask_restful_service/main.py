from flask import Flask, request, make_response
import SAP.GL

app = Flask(__name__)

@app.route("/")
def index():
    return "index page"


@app.route("/bal")
def get_acc_balances():
    cocd = request.args.get('cocd')
    account = request.args.get('account')
    year = request.args.get('year')

    ac_balances = SAP.GL.get_ac_balances(cocd, account, year)

    resp = make_response(ac_balances, 200)
    resp.headers['Content-Type'] = 'application/json'    

    return resp


if __name__ == "__main__":
    app.run()