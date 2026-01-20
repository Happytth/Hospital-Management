from flask_caching import Cache
# from flask import current_app
cache = Cache()
# cache.init_app(current_app)
# current_app.config.update({
#     'CACHE_TYPE': 'RedisCache',
#     'CACHE_DEFAULT_TIMEOUT': 300
# })