import socket
import time


def start_server():
    clients = []
    quit = False

    host = socket.gethostbyname(socket.gethostname())
    print(host)
    port = 7000

    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((host, port))


    print("[server started]")

    
    while not quit:
        try:
            while True:
                data, address = server.recvfrom(1024)
                

                if address not in clients:
                    clients.append(address)


                current_time = time.strftime("%Y-%m-%d-%H-%M-%S",
                                             time.localtime())
                print(
                    f"[{address[0]}]|[{address[1]}]|[{current_time}]/{data.decode('utf-8')}"
                )

                for client in clients:
                    if address != client:
                        server.sendto(data, client)
        except:
            print("\n[server stopped]")
            quit = True



start_server()
