from flask_jwt_extended import JWTManager
from controllers.model import User

jwt=JWTManager()

@jwt.user_identity_loader
def load(user):
    return user.email_id

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header,jwt_data):
    identity=jwt_data["sub"]
    return User.query.filter_by(email_id=identity).one_or_none()
