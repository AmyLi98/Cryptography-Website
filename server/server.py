from flask import Flask, request, render_template, Response, send_file, send_from_directory
from flask_socketio import SocketIO, send, emit
from full_functions import *
from cryptography_library.rsa import return_key
import struct
from network.socket_peer import PeerNetwork
import urllib

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = False
app.config['host'] = "::"
socketio = SocketIO(app)


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('real-index.html')


@app.route('/communicate', methods=['GET', 'POST'])
def communicate():
    return render_template('communicate.html')


@app.route('/download/<file_name>', methods=['GET'])
def send_file_to_web(file_name):
    return send_file("../TEMP/" + file_name)


@app.route('/get_message', methods=['GET'])
def get_message():
    return PeerNetwork.message


@app.route('/set_message', methods=['POST'])
def set_message():
    PeerNetwork.message = request.form['en_message']
    return 'OK'


@app.route('/upload', methods=['POST'])
def handle_file():
    print("receiving upload")
    file = request.files['file']

    def file_wrapper(file_data: bytes, file_name: str) -> bytes:
        """
        把文件名包装到文件数据中
        :param file_data:
        :param file_name:
        :return:
        """
        file_name = file_name.encode('utf-8')
        return struct.pack('>I', len(file_name)) + file_name + file_data

    # file.save("""D:\programming\CryptographyExperimentCourse3\\""" + file.filename)
    PeerNetwork.send_message_to_peer(file_wrapper(file.read(), file.filename), if_file=1)
    print(request.files['file'])
    return "success"


@app.route('/connect', methods=['GET'])
def connect_to_peer():
    ip = request.args.get("ip")
    port = request.args.get("port")
    print(ip, port)
    PeerNetwork.connect_to_other_peer(ip=ip, port=int(port))
    return "done"


@app.route('/cryptography', methods=['POST'])
def transform():
    method = int(request.form['method'])  # 加密类型
    doc = request.form['message']
    key = request.form['key']
    en = int(request.form['en'])  # 表示是否加密

    print(en, method, key, doc)

    def choose_function(en, method, key, doc):
        """

        :param en: 1:加密
        :param method: 0：caesar, 1:autokey, 2:vigenere, 3:playfair, 4:column, 5:double, 6:DES, 7:RC4, 8:RSA, 9:keyword, 10:MD5, 11:DH key exchange
        :param key: 密钥 str
        :param doc: 待加/解密 str
        :return: str
        """


        if method == 0:
            if en == 1:
                return caesar_cipher_encrypt(doc, key)
            else:
                return caesar_cipher_decrypt(doc, key)
        if method == 1:
            if en == 1:
                return autokey_plain_text_encrypt(doc, key)
            else:
                return autokey_plain_text_decrypt(doc, key)
        if method == 2:
            if en == 1:
                return vigenere_encrypt(doc, key)
            else:
                return vigenere_decrypt(doc, key)
        if method == 3:
            if en == 1:
                return play_fair_encrypt(doc, key)
            else:
                return play_fair_decrypt(doc, key)
        if method == 4:
            if en == 1:
                return coloumn_permutation_encrypt(doc, key)
            else:
                return coloumn_permutation_decrypt(doc, key)
        if method == 5:
            if en == 1:
                return double_transposition_encrypt(doc, key)
            else:
                return double_transposition_decrypt(doc, key)
        if method == 6:
            if en == 1:
                return DES_encrypt(doc, key)
            else:
                return DES_decrypt(doc, key)
        if method == 7:
            if en == 1:
                return RC4_cipher_encrypt(doc, key)
            else:
                return RC4_cipher_decrypt(doc, key)
        if method == 8:
            if en == 1:
                return_key()
                return RSA_cipher_encrypt(doc, key)
            else:
                return RSA_cipher_decrpt(doc, key)
        if method == 9:
            if en == 1:
                return keyword_cipher_encrypt(doc, key)
            else:
                return keyword_cipher_decrypt(doc, key)
        if method == 10:
            if en == 1:
                return MD5(doc)
            else:
                return
        if method == 11:
            if en == 1:
                return DH_exchange_demo()
            else:
                return DH_exchange_demo()
        if method == 12:
            if en == 1:
                return
            else:
                return
        return "error"

    try:
        return_message = choose_function(en, method, key, doc)
        return return_message
    except:
        return "Internal error"


@socketio.on('chat')
def receive_chat_message(message):
    # print('received json: ' + str(message))
    print("iterface chat message", message)
    PeerNetwork.send_message_to_peer(message.encode('utf-8'))


@socketio.on('server')
def send_message(message):
    socketio.emit("server", message)


@socketio.on('connection')
def inform_connection_state(message):
    socketio.emit("connection", message)


@socketio.on('file')
def send_file_name(link):
    """
    inform user that a file has been received
    :param link:
    :return:
    """
    socketio.emit('link', link)


@app.route('/statics/<path:path>', methods=['GET', 'POST'])
def statics_file(path):
    return send_from_directory('statics', path)


@app.route('/<file_name>', methods=['GET', 'POST'])
def return_html(file_name):
    return render_template(file_name)


def test():
    import time
    while True:
        time.sleep(1)
        send_message("Test")


def run_ui_server(port=5000):
    app.config['port'] = port
    socketio.run(app, host="0.0.0.0", port=port)
