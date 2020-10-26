from flask import Flask, request, make_response
import SAP.ac_balances

app = Flask(__name__)

@app.route("/")
def index():
    return "index page"


@app.route("/bal")
def get_acc_balances():
    account = request.args.get('account')
    year = request.args.get('year')

    ac_balances = SAP.ac_balances.get_ac_balances(account, year)

    resp = make_response(ac_balances, 200)
    resp.headers['Content-Type'] = 'application/json'    

    return resp


if __name__ == "__main__":
    app.run()