from flask import Flask, request, jsonify
import ssl

app = Flask(__name__)

registered_subscribers = {}

@app.errorhandler(400)
@app.errorhandler(404)
@app.errorhandler(500)
def error_handler(error):
    return jsonify({'error': str(error)}), error.code

def authenticate(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            return jsonify({'error': 'Unauthorized'}), 401
        return func(*args, **kwargs)
    return wrapper

@app.route('/register', methods=['POST'])
@authenticate
def register_subscriber():
    subscriber_data = request.json
    
    if 'subscriber_id' not in subscriber_data or 'device_id' not in subscriber_data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    subscriber_id = subscriber_data['subscriber_id']
    device_id = subscriber_data['device_id']
    
    registered_subscribers[subscriber_id] = device_id
    
    return jsonify({'message': 'Subscriber registered successfully'}), 200

@app.route('/subscriber/<subscriber_id>', methods=['GET'])
@authenticate
def get_subscriber(subscriber_id):
    if subscriber_id not in registered_subscribers:
        return jsonify({'error': 'Subscriber not found'}), 404
    
    return jsonify({'subscriber_id': subscriber_id, 'device_id': registered_subscribers[subscriber_id]}), 200

if __name__ == '__main__':
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain(certfile='server.crt', keyfile='server.key')
    
    app.run(host='0.0.0.0', port=443, ssl_context=context)
