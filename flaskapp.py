import pickle
from flask import Flask, jsonify, request, Response, json
app = Flask(__name__)

class Order(object):
	def __init__(self, order_id):
		self.order_id = order_id
		self.mid = None
		self.tid = None
		self.amount = None
		self.payment = None

	def json_dict(self):
		return {
			'order_id': self.order_id,
			'mid': self.mid,
			'tid': self.tid,
			'amount': self.amount,
			'payment': self.payment
		}

class Orders(object):
	def __init__(self):
		try:
			f = open('/tmp/orders.pickle', 'rb')
			orders = pickle.load(f)
			self.order_id = orders.order_id
			self.orders = orders.orders
			f.close()
		except:
			self.order_id = 0x1234567812345678
			self.orders = {}

	def get_order(self, order_id):
		if order_id in self.orders:
			return self.orders[order_id]
		return None

	def create_order(self):
		order = Order(self.order_id)
		self.orders[self.order_id] = order
		self.order_id = self.order_id + 1
		f = open('/tmp/orders.pickle', 'wb')
		pickle.dump(self, f)
		return order

	def add_order_details(self, order_id, mid, tid, amount):
		order = self.orders[order_id]
		if order:
			order.mid = mid
			order.tid = tid
			order.amount = amount
			f = open('/tmp/orders.pickle', 'wb')
			pickle.dump(self, f)
			return True
		return False

	def add_payment(self, order_id, otp):
		order = self.orders[order_id]
		if order and not order.payment:
			order.payment = otp
			f = open('/tmp/orders.pickle', 'wb')
			pickle.dump(self, f)
			return True
		return False


all_orders = Orders()

@app.route('/order', methods = ['POST'])
def create_order():
	order = all_orders.create_order()
	return jsonify(order.json_dict())

@app.route('/order/<order_id>')
def get_order(order_id):
	order = all_orders.get_order(long(order_id))
	if order:
		return jsonify(order.json_dict())
	else:
		return jsonify({
			'order_id': 'Unknown'
		})

@app.route('/payment', methods = [ 'POST' ])
def post_payment():
	payment_request_json = request.get_json(force=True)
	all_orders.add_payment(
			long(payment_request_json['order_id']),
				payment_request_json['otp'])
	order = all_orders.get_order(long(payment_request_json['order_id']))
	return jsonify(order.json_dict())

@app.route('/order', methods = [ 'PUT' ])
def update_order():
	payment_request_json = request.get_json(force=True)
	all_orders.add_order_details(long(payment_request_json['order_id']),
		payment_request_json['mid'],
		payment_request_json['tid'],
		payment_request_json['amount'])
	order = all_orders.get_order(long(payment_request_json['order_id']))
	return jsonify(order.json_dict())

if __name__ == '__main__':
	app.debug = True
	app.run()
