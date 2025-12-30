from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def home():
    """Home route returning a welcome message."""
    return jsonify({
        "message": "Hello from Flask!",
        "status": "running",
        "version": "1.0.0"
    })


@app.route('/health')
def health():
    """Health check endpoint for monitoring."""
    return jsonify({
        "status": "healthy",
        "service": "flask-app"
    }), 200


@app.route('/api/info')
def info():
    """API info endpoint."""
    return jsonify({
        "app_name": "Flask Jenkins Demo",
        "author": "Your Name",
        "description": "A simple Flask app deployed via Jenkins pipeline"
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
