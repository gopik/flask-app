from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route('/order/<order_id>')
def get_order(order_id):
	if order_id == '0x1234567812345678':
		return jsonify({
			'order_id': '0x1234567812345678',
			'mid': 10,
			'tid': 100,
			'amount': 2304
			})
	else:
		return jsonify({
			'order_id': order_id
		})

@app.route('/payment', methods = [ 'POST' ])
def post_payment():
	payment_request_json = request.get_json(force=True)
	return jsonify({
		'order_id': payment_request_json['order_id'],
		'amount' : payment_request_json['amount'],
		'otp' : payment_request_json['otp']
		})


if __name__ == '__main__':
	app.debug = True
	app.run()
