from flask import Flask
from controllers.security import jwt
from controllers.model import db, User, Department
from flask_cors import CORS
from datetime import datetime
from caching import cache  
from controllers.celery_init import celery_init_app
from celery.schedules import crontab
from controllers.task import month_report, send_daily_remainders


def create_app():
    app = Flask(__name__)

    app.config.update({
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///hospital_database.db',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'JWT_SECRET_KEY': 'this_is_a_secret_key',
        'CACHE_TYPE': 'RedisCache',
        'CACHE_REDIS_URL': 'redis://localhost:6379/0',
        'CACHE_DEFAULT_TIMEOUT': 300
    })

    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    cache.init_app(app) 

    from controllers.routes import auth
    app.register_blueprint(auth, url_prefix="/auth")

    return app


app = create_app()
celery = celery_init_app(app)
celery.autodiscover_tasks()

with app.app_context():
    db.create_all()

    def newadmin():
        admin = User.query.filter_by(role="admin").one_or_none()
        if not admin:
            admin = User(
                email_id='happytth@gmail.com', gender="male", age=20,
                password="hap@123", name="Happy", is_active=True, role="admin"
            )
            db.session.add_all([admin])
            db.session.commit()

    newadmin()


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute='*/1'), month_report.s())
    sender.add_periodic_task(crontab(minute='*/1'), send_daily_remainders.s())


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)



# celery -A app.celery worker --loglevel=info

# celery -A app.celery beat --loglevel=info


# sudo service redis-server stop
