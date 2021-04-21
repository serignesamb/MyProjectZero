from daos.account_dao import AccountDAO
from exceptions.resource_not_found import ResourceNotFound
from models.account import Account
from util.db_connection import connection


class AccountDAOImpl(AccountDAO):
    def create_account(self, account):
        sql = "INSERT INTO accounts VALUES(DEFAULT, %s, %s, %s, %s) RETURNING *"

        cursor = connection.cursor()
        cursor.execute(sql, (account.deposit_amount,account.withdraw_amount,
                             account.account_balance, account.client_id, ))
        record = cursor.fetchone()
        # cursor.execute("ROLLBACK")
        # because this is insertion which is part of the DML, the data needs to be committed after it's added
        connection.commit()

        return Account(record[0], record[1], record[2], record[3],record[4])

    def get_account(self, account_id):
        pass
        sql = "SELECT * FROM accounts WHERE account_id = %s"  # %s is a placeholder for string
        cursor = connection.cursor()
        cursor.execute(sql, [account_id])

        record = cursor.fetchone()

        if record:
            return Account(record[0], record[1], record[2], record[3])
        else:
            raise ResourceNotFound(f"Account with id: {account_id} - Not Found")

    def all_accounts(self):
        # a sql statement that would equate to getting all the moives from our database
        sql = "SELECT * FROM accounts"
        # setting up an object called cursor , and assign connection object after importing it from util
        # This connection object has many methods like cursor()
        cursor = connection.cursor()
        # using this cursor object to execute sql statments and pass sql command to it
        cursor.execute(sql)
        # store those results in an object called records
        records = cursor.fetchall()

        # create a list for our movie list
        account_list = []
        # iterating through that list
        for record in records:
            # create a new movie object and passing the values from the movie list by following the order
            # that is in the database movies
            account = Account(record[0], record[1], record[2], record[3])
            # append the result to the movie_list we created and convert them to json()
            account_list.append(account.json())
        return account_list

    def update_account(self, change):
        sql = "UPDATE accounts SET deposit_amount=%s, withdraw_amount=%s, account_balance=%s WHERE account_id=%s " \
              "RETURNING * "

        cursor = connection.cursor()
        cursor.execute(sql, change.deposit_amount, change.withdraw_amount, change.account_balance)
        connection.commit()

        record = cursor.fetchone()
        return Account(record[0], record[1], record[2], record[3])

    def delete_account(self, account_id):
        sql = "DELETE FROM accounts WHERE account_id=%s"
        cursor = connection.cursor()
        cursor.execute(sql, [account_id])
        connection.commit()
