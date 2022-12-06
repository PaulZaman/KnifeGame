import socket


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = socket.gethostbyname(socket.gethostname())
        self.port = 5555
        self.addr = (self.server, self.port)
        self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
            return True
        except:
            return False

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)

    def get_player_number(self):
        try:
            self.client.send(str.encode("player_n"))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)
            return False

    def check_if_opponent_is_ready(self, selected_player):
        try:
            self.client.send(str.encode("ready" + str(selected_player)))
            data = self.client.recv(2048).decode()
            if data[:-1] == "ready":
                return data[-1:]
            else:
                return False
        except socket.error as e:
            print(e)
            return False

    def check_if_opponent_asked_for_rematch(self):
        try:
            self.client.send(str.encode("not_ready"))
            data = self.client.recv(2048).decode()
            if data[:-1] == "ready":
                return True
            else:
                return False
        except socket.error as e:
            print(e)
            return False


'''connection = n.get_player_number()
print(connection)
opponent_connected = n.check_for_opponent_connection()
print(opponent_connected)'''

#print(n.send("ok"))
#print(connection)