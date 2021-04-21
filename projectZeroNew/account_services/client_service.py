from daos.client_dao_impl import ClientDAOImpl


class ClientService:
    # account_dao = AccountDAOTemp()
    client_dao = ClientDAOImpl()

    @classmethod
    def create_client(cls, client):
        return cls.client_dao.create_client(client), 201

    @classmethod
    def all_clients(cls):
        return cls.client_dao.all_clients()

    @classmethod
    def get_client_by_id(cls, client_id):
        return cls.client_dao.get_client(client_id)

    @classmethod
    def update_client(cls, client_id):
        return cls.client_dao.update_client(client_id)

    @classmethod
    def delete_client(cls, client_id):
        return cls.client_dao.delete_client(client_id)
