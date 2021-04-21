from exceptions.resource_not_found import ResourceNotFound
from exceptions.resource_unavailable import ResourceUnavailable
from daos.account_dao_impl import AccountDAOImpl


class AccountService:
    # account_dao = AccountDAOTemp()
    account_dao = AccountDAOImpl()

    @classmethod
    def create_account(cls, account):
        return cls.account_dao.create_account(account), 201

    @classmethod
    def all_accounts(cls):
        return cls.account_dao.all_accounts()

    @classmethod
    def get_account_by_id(cls, account_id):
        return cls.account_dao.get_account(account_id)

    @classmethod
    def update_account(cls, account):
        return cls.account_dao.update_account(account)

    @classmethod
    def delete_account(cls, account_id):
        return cls.account_dao.delete_account(account_id)

    @classmethod
    def deposit_amount(cls, account_id, client_id):
        try:
            acct = cls.account_dao.get_account(account_id, client_id)
            amount: float
            acct.account_balance += amount
            cls.update_account(acct, client_id)
            return acct.account_balance
        except ResourceUnavailable as e:
            return "The client or account exists", 404
        except ResourceNotFound as r:
            return "There is not enough found", 422

    @classmethod
    def withdraw_amount(cls, account_id, client_id):
        try:
            acct = cls.account_dao.get_account(account_id, client_id)
            amount: float
            acct.account_balance -= amount
            cls.update_account(acct, client_id)
            return acct.account_balance
        except ResourceUnavailable as e:
            return "The client or account exists", 404
        except ResourceNotFound as r:
            return "There is not enough found", 422
