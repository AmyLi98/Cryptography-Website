from server.server import run_ui_server, send_message
from network.socket_peer import PeerNetwork
import threading


def test():
    import time
    while True:
        time.sleep(1)
        print("good")
        send_message("good")


def run_all_server(local_port=5001, open_port=8000):
    # threading.Thread(target=test).start()
    threading.Thread(target=run_ui_server, args=[local_port]).start()
    # run_ui_server(local_port)
    print("UI server started")
    threading.Thread(target=PeerNetwork.start_socket_server, args=[open_port]).start()


if __name__ == '__main__':
    import sys
    import webbrowser
    import time
    web_port = 5001
    socket_port = 8001
    print(sys.argv)
    if len(sys.argv) > 1:
        web_port = int(sys.argv[1])
        socket_port =  int(sys.argv[2])
    print("run on ", web_port, socket_port)
    run_all_server(web_port, socket_port)
    url = "http://127.0.0.1:" + str(web_port)
    chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
    time.sleep(1)
    webbrowser.get(chrome_path).open(url)
