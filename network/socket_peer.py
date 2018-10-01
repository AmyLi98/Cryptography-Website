import socket
import struct
import time
import threading
import network.websocket_interface
from cryptography_library.dh_key_exchange import DHKeyExchange
from cryptography_library.auto_en_and_de import en, de


class PeerNetwork:
    TIME_OUT = 600
    if_connected = False
    peer_socket = None
    last_message_time = 0
    secret_key = ''
    message = ''

    @staticmethod
    def key_to_des_type(key_int: int) -> str:
        return hex(key_int)[2:]

    @staticmethod
    def set_secret_key(key_int):
        PeerNetwork.secret_key = PeerNetwork.key_to_des_type(key_int)[:14]

    @staticmethod
    def start_socket_server(port):
        """
        监听指定端口号并接收数据
        :param port:
        :return:
        """
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = "0.0.0.0"  # socket.gethostname()  # or 0.0.0.0
        print("local host:", host)
        server_socket.bind((host, port))
        server_socket.listen(10)
        threading.Thread(target=PeerNetwork._handle_server_data, kwargs={"server_socket": server_socket}).start()
        return

    @staticmethod
    def disconnect():
        PeerNetwork.peer_socket.close()
        PeerNetwork.if_connected = False
        PeerNetwork.peer_socket = None

    @staticmethod
    def _handle_server_data(server_socket):
        """
        keep receiving connections
        :param server_socket:
        :return:
        """
        print("thread started")
        while True:
            client_socket, addr = server_socket.accept()
            network.websocket_interface.InterfaceNetwork.inform_connection_status(1)  # inform interface
            PeerNetwork.last_message_time = time.time()  # log connection time
            PeerNetwork.peer_socket = client_socket
            PeerNetwork.if_connected = True
            print("Got a connection from %s" % str(addr))

            # exchange key here
            a = DHKeyExchange()
            print("sending message")
            print("DH public key send:",a.get_public_one())
            PeerNetwork._send_msg(PeerNetwork.peer_socket, str(a.get_public_one()).encode())
            print("send finished")
            PeerNetwork.set_secret_key(a.get_shared_key(
                int.from_bytes(PeerNetwork._recv_msg(PeerNetwork.peer_socket), byteorder="little")))
            print("shared key", PeerNetwork.secret_key)
            print("key exchange finished")
            # key exchange finished

            threading.Thread(target=PeerNetwork._handle_data).start()

    @staticmethod
    def _handle_data():
        """
        keep receiving data when connected
        :return:
        """
        print("smaller func start")

        def check_file_type_and_choose_func(data):
            if_file = struct.unpack(">I", data[:4])[0]
            if if_file == 1:
                network.websocket_interface.InterfaceNetwork.send_file(data[4:])
            else:
                network.websocket_interface.InterfaceNetwork.send_to_interface(message=data[4:].decode("utf-8"))

        while PeerNetwork.if_connected:
            try:
                data = PeerNetwork._recv_msg(PeerNetwork.peer_socket)
                print("received data:", data)
                check_file_type_and_choose_func(data)
                PeerNetwork.last_message_time = time.time()  # log message time
            except:
                print("disconnected")
                network.websocket_interface.InterfaceNetwork.inform_connection_status(0)  # inform interface
                return

    @staticmethod
    def send_message_to_peer(message, if_file=0):
        s = PeerNetwork.peer_socket
        message = struct.pack('>I', if_file) + message
        PeerNetwork._send_msg(s, message)
        print("send_message_to_peer", message)

    @staticmethod
    def connect_to_other_peer(ip: str, port: int):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        PeerNetwork.peer_socket = s
        PeerNetwork.if_connected = True
        print("connected")
        # exchange key here
        print("start key exchange")
        dh = DHKeyExchange()
        PeerNetwork.set_secret_key(dh.get_shared_key(
            int.from_bytes(PeerNetwork._recv_msg(PeerNetwork.peer_socket), byteorder="little")))
        PeerNetwork.send_message_to_peer(str(dh.get_public_one()).encode())
        print("finished")
        print("DH key exchange(Shared key):", PeerNetwork.secret_key)
        # key exchange finished here
        threading.Thread(target=PeerNetwork._handle_data).start()

    @staticmethod
    @en(secret_key)
    def _send_msg(sock, msg):
        # Prefix each message with a 4-byte length (network byte order)
        msg = struct.pack('>I', len(msg)) + msg
        sock.sendall(msg)

    @staticmethod
    @de(secret_key)
    def _recv_msg(sock):
        # Read message length and unpack it into an integer
        raw_msglen = PeerNetwork._recvall(sock, 4)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        # Read the message data
        return PeerNetwork._recvall(sock, msglen)

    @staticmethod
    def _recvall(sock, n):
        # Helper function to recv n bytes or return None if EOF is hit
        data = b''
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data


if __name__ == '__main__':
    port = 1555
    PeerNetwork.start_socket_server(port)
