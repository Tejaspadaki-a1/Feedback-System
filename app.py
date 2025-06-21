from flask import Flask
from flask_cors import CORS
from db import init_db
from routes.auth import auth_bp
from routes.feedback import feedback_bp
from routes.user import user_bp

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://tejaspadaki255:tejas%401@cluster0.cpwl2.mongodb.net/feedback_db'
app.config['SECRET_KEY'] = 'supersecretkey'

CORS(app)
init_db(app)

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(feedback_bp, url_prefix='/api')
app.register_blueprint(user_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
