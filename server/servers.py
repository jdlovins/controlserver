import json
import uuid


class Servers:
    def __init__(self, servers):

        self.servers = []

        # creates a Server object so we can use server.name instead of server['name'] and adds it to a list
        for s in servers:
            self.servers.append(Server(s))

    def get_server_by_id(self, sid):
        """
        Returns a server object that contains the ID associated with it
        :param sid: the ID associated with the server details
        :return: the server object with the ID or None if no server is found
        """
        for server in self.servers:
            if server.id == sid:
                return server


class Server(object):
    def __init__(self, info):
        self.__dict__ = info
        self.id = uuid.UUID(self.id)
