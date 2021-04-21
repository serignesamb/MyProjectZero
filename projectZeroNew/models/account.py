class Account:
    def __init__(self, account_id=0, deposit_amount=0, withdraw_amount=0, account_balance =0 , client_id=0):
        self.account_id = account_id
        self.deposit_amount = deposit_amount
        self.withdraw_amount = withdraw_amount
        self.account_balance = account_balance
        self.client_id = client_id

    def json(self):
        return {
            'account_id': self.account_id,
            'deposit_amount': self.deposit_amount,
            'withdraw_amount': self.withdraw_amount,
            'account_balance': self.account_balance,
            'client_id': self.client_id
        }

    @staticmethod
    def json_parse(json):
        account = Account()
        account.account_id = json["account_id"] if "account_id" in json else 0
        account.deposit_amount = json["deposit_amount"]
        account.withdraw_amount = json["withdraw_amount"]
        account.account_balance = json["account_balance"]
        account.client_id = json["client_id"]
        return account

    # # Check Later
    # def __repr__(self):
    #     return str(self.json())