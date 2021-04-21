class Client:
    def __init__(self, client_id=0, client_name=""):
        self.client_id = client_id
        self.client_name = client_name


    def json(self):
        return {
            "client_id": self.client_id,
            "client_name": self.client_name

        }

    @staticmethod
    def json_parse(json):
        client = Client()
        client.client_id = json["client_id"]
        client.client_name = json["client_name"]

        return client

    # Check Later
    def __repr__(self):
        return str(self.json())

