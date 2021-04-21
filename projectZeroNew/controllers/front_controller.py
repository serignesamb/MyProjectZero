from controllers import account_controller, client_controller


def route(app):
    # Calls all other other controllers
    account_controller.route(app)
    client_controller.route(app)
