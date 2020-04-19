from api.api import api_bp


def routers(app):
    app.register_blueprint(api_bp)

    return True


def exempt(app):
    return True
