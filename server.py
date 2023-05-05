import socket
import threading

# Пораметры для соединения
host = '127.0.0.1'  # Стандартный адрес localhost
port = 11111  # Порт для прослушивания (непривилегированные порты > 1023)

# Запуск
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Списки для клиентов и их псевдонимов
clients = []
nicknames = []

# Отправка сообщений всем подключенным клиентам
def broadcast(message):
    for client in clients:
        client.send(message)

# Обработка сообщений от клиентов
def handle(client):
    while True: #бесконечный цикл 
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break

# Функция прослушивания
def receive():
    while True:
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server if listening...")
receive()
