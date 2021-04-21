from flask import jsonify, json

from models.client import Client
from daos.client_dao import ClientDAO
from exceptions.resource_not_found import ResourceNotFound
from util.db_connection import connection


class ClientDAOImpl(ClientDAO):
    def create_client(self, client):
        sql = "INSERT INTO clients VALUES(DEFAULT, %s) RETURNING *;"

        cursor = connection.cursor()
        # TypeError: Object of type Client is not JSON serializable
        cursor.execute(sql, (client.client_name, ))
        record = cursor.fetchone()
        # cursor.execute("ROLLBACK")
        # because this is insertion which is part of the DML, the data needs to be committed after it's added
        connection.commit()
        returned_val = Client(client_id=record[0], client_name=record[1])
        return returned_val

    def get_client(self, client_id):
        sql = "SELECT * FROM clients WHERE client_id = %s"  # %s is a placeholder for string
        cursor = connection.cursor()
        cursor.execute(sql, [client_id])

        record = cursor.fetchone()

        if record:
            return Client(record[0], record[1]).json()
        else:
            raise ResourceNotFound(f"Client with id: {client_id} - Not Found")

    def all_clients(self):
        # a sql statement that would equate to getting all the moives from our database
        sql = "SELECT * FROM clients"
        # setting up an object called cursor , and assign connection object after importing it from util
        # This connection object has many methods like cursor()
        cursor = connection.cursor()
        # using this cursor object to execute sql statments and pass sql command to it
        cursor.execute(sql)
        # store those results in an object called records
        records = cursor.fetchall()
        # cursor.execute("ROLLBACK")

        # create a list for our movie list
        client_list = []
        # iterating through that list
        for record in records:
            # create a new movie object and passing the values from the movie list by following the order
            # that is in the database movies
            client = Client(record[0], record[1])
            # append the result to the movie_list we created and convert them to json()
            client_list.append(client.json())
        return client_list

    def update_client(self, change):
        sql = "UPDATE clients SET client_name=%s WHERE client_id=%s RETURNING * "

        cursor = connection.cursor()
        cursor.execute(sql, (change.client_name, change.client_id))
        connection.commit()

        record = cursor.fetchone()
        return Client(record[0], record[1])

    def delete_client(self, client_id):
        sql = "DELETE FROM clients WHERE client_id=%s"
        cursor = connection.cursor()
        cursor.execute(sql, [client_id])
        connection.commit()



# #Internal Testing
# def _test():
#       a_dao = ClientDAOImpl()
#       clients = a_dao.all_clients()
#     # #  clients = a_dao.create_client(cl)
#     # # print(clients)
#     #
#     # print(a_dao.create_client(clients)) # what should i pass in here ?
#       print(clients[0])
#
# if __name__ == '__main__': _test()

#Hmmm ok so let me try to modify this to the client_id