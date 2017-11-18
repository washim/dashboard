from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
	from datetime import date, timedelta
	today = date.today()
	yesterday = today - timedelta(7)
	params = {
		"startdt": yesterday.strftime("%Y-%m-%d"),
		"enddt": today.strftime("%Y-%m-%d")
	}
	return render_template("stockmarket.html", params=params)

@app.route("/stocktolerance", methods=["GET"])
def stocktolerance():
	import tolerance as tl
	stocktolerance = tl.tolerance(request.args.get("symbol"), request.args.get("interval"), request.args.get("confidence"), request.args.get("investment"), request.args.get("start"), request.args.get("end"))
	return stocktolerance.getTolerance()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)