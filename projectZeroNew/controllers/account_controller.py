from flask import Flask, jsonify, request

from account_services.client_service import ClientService
from exceptions.resource_not_found import ResourceNotFound
from account_services.account_service import AccountService
from models.account import Account


def route(app):
    @app.route("/accounts", methods=["POST"])
    def create_new_account():
        account = Account.json_parse(request.json)
        accounts = AccountService.create_account(account)
        return jsonify(str(accounts)), 201  # Resource Created

    @app.route("/accounts/<account_id>", methods=['GET'])
    def get_account_id(account_id):
        try:
            account = AccountService.get_account_by_id(int(account_id))
            return jsonify(str(account)), 200  # ok
        except ValueError as e:
            return "Not a valid ID", 400  # Bad Request
        except ResourceNotFound as r:
            return r.message, 404

    # This fetches all the accounts for client 7
    @app.route("/clients/<client_id>/accounts", methods=['GET'])
    def get_all_accounts(client_id):
        try:
            if ClientService.get_client_by_id(client_id):
                return jsonify(AccountService.all_accounts()), 200
        except ResourceNotFound as r:
            return "There is no client with such ID", 404

    # This gets the account 4 for client 9
    @app.route("/clients/<client_id>/accounts/<account_id>", methods=['GET'])
    def get_account(client_id, account_id):
        try:
            if ClientService.get_client_by_id(client_id):
                acct = AccountService.get_account_by_id(int(account_id))
                return jsonify(acct.json()), 200
        except ValueError as ve:
            return "This is not a valid id", 400
        except ResourceNotFound as r:
            return "The passed client ID or Account ID is missing", 404

    # Update account with id 3 for client 10
    @app.route("/clients/<client_id>/accounts/<account_id>", methods=['PUT'])
    def update_account_with_id_for_client_id(client_id, account_id):
        try:
            if ClientService.get_client_by_id(client_id):
                acct = AccountService.update_account(int(account_id))
                return jsonify(acct.json()), 200
        except ValueError as ve:
            return "This is not a valid id", 400
        except ResourceNotFound as r:
            return "The passed client ID or Account ID is missing", 404

        return "Client Does not exist", 404

    # Delete Account 6 for client 15
    @app.route("/clients/<client_id>/accounts/<account_id>", methods=['DELETE'])
    def delete_account_for_client_id(client_id, account_id):
        try:
            if ClientService.get_client_by_id(int(client_id)):
                AccountService.get_account_by_id(account_id)
                AccountService.delete_account(account_id)
                return '', 204

        except ResourceNotFound as m:
            return "Account does not exist", 404

    @app.route("/clients/<client_id>/accounts/<account_id>", methods=['PATCH'])
    def patch_accounts(client_id, account_id):
        take_action = request.json['withdraw_amount']

        if take_action == 'deposit_amount' or take_action == 'withdraw_amount':
            try:
                balance = AccountService.deposit(int(account_id),
                                                 client_id) if take_action == 'deposit_amount' else AccountService.withdraw_amount(
                    int(account_id), client_id)
                return f"{balance} is a success!", 200
            except ResourceNotFound as ve:
                return "Not enough funds", 422
            except ResourceNotFound as ve:
                return "This Client does not exist", 404
        return take_action
