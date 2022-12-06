import socket
from _thread import *

server = socket.gethostbyname(socket.gethostname())
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")


players_n = ['1','2']
players_data = ['0000','0000']
players_ready = ["not_ready", "not_ready"]


def threaded_client(conn, player):
    reply = ""
    while True:
        try:
            data = conn.recv(2048).decode()
            print("positions : ", players_data)
            print("players ready : ", players_ready)
            if data == "player_n":
                reply = players_n[player]
            elif data[:-1] == "ready" or data == "not_ready":
                players_ready[player] = data
                reply = players_ready[(player + 1) % 2]
            else:
                print("data: ", data)
                reply = players_data[(player + 1) % 2]
                if data != "":
                    players_ready[0] = players_ready[1] = "not_ready"
                    players_data[player] = data

            if not data:
                print("Disconnected")
            else:
                print("Received by", player, " : ", data)
                print("Sending to", player, " : ",  reply)

            conn.sendall(str.encode(reply))



        except:
            break

    print("Lost connection")
    players_data[player] = "0000"
    players_ready[player] = "not_ready"
    conn.close()

currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr, "Player number ", currentPlayer)
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer = (currentPlayer + 1) % 2
