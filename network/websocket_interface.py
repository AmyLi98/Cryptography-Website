import server.server
import struct


class InterfaceNetwork:
    @staticmethod
    def send_to_interface(message):
        """

        :param message:
        :return:
        """
        # print("send_to_interface", message)
        # print("send_to_interface encode", message.encode('utf-8'))
        server.server.send_message(message)

    @staticmethod
    def inform_connection_status(status: int):
        """

        :param status: 1:connected, 0:disconnected
        :return:
        """

    @staticmethod
    def send_file(file):
        """
        save locally for now
        :param file:
        :return:
        """

        def file_unwrapper(file: bytes) -> (bytes, str):
            """
            将文件名从文件数据中拆开
            :param file:
            :return:
            """
            raw_length = file[:4]
            name_length = struct.unpack('>I', raw_length)[0]
            name = file[4:4 + name_length].decode('utf-8')
            return file[4 + name_length:], name

        # print("In the send_function")
        file, file_name = file_unwrapper(file)
        # print(file_name)
        with open("./TEMP/" + file_name, "wb") as f:
            f.write(file)
        server.server.send_file_name(file_name)
