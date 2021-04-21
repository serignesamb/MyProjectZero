import logging
from flask import jsonify, request
from account_services.account_service import AccountService
from exceptions.resource_not_found import ResourceNotFound
from account_services.client_service import ClientService
from models.account import Account
from models.client import Client


def route(app):
    @app.route("/clients", methods=["POST"])
    def create_new_client():
        client = Client.json_parse(request.json)
        clients = ClientService.create_client(client)
        return jsonify(str(clients)), 201  # Resource Created

    @app.route("/clients", methods=['GET'])
    def get_all_clients():
        logging.info("Program Started! ")
        return jsonify(ClientService.all_clients()), 200

    @app.route("/clients/<client_id>", methods=['GET'])
    def get_client_with_client_id(client_id):
        try:
            client = ClientService.get_client_by_id((int(client_id)))
            return jsonify(str(client)), 200  # ok
        except ValueError as e:
            return "Not a valid ID", 400  # Bad Request
        except ResourceNotFound as r:
            return r.message, 404

    @app.route("/clients/<client_id>", methods=["PUT"])
    def update_client_with_client_id(client_id):
        try:
            client = Client.json_parse(request.json)
            client.client_id = int(client_id)
            client = ClientService.update_client(client)
            return jsonify(client.json()), 200
        except ValueError as ve:
            return "Client Does not exist", 404

    @app.route("/clients/<client_id>", methods=["DELETE"])
    def del_client_with_client_id(client_id):
        try:
            ClientService.delete_client(int(client_id))
            return 'Client is successfully deleted!', 205
        except ValueError as val:
            return "No such client exists", 404

    @app.route("/clients/<client_id>/accounts", methods=["POST"])
    def create_new_account_with_client_id(client_id):
        client = ClientService.get_client_by_id((int(client_id)))
        postman_passing_value = (list(client.values())[0])
        for client in ClientService.all_clients():
            if list(client.values())[0] == postman_passing_value:

                acct = Account()

                acct.client_id = postman_passing_value
                acct.deposit_amount = postman_passing_value
                acct.withdraw_amount = postman_passing_value
                acct.account_balance = postman_passing_value
                account = AccountService.create_account(acct)
                return jsonify(account), 201  # Resource Created
            else:
                print("No id found")
