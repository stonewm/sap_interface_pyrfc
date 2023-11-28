
from threading import Thread
from pyrfc import Server, set_ini_file_directory
import os

def my_stfc_connection(request_context=None, REQUTEXT=""):
    """Server function my_stfc_connection with the signature of ABAP function module STFC_CONNECTION."""

    print("stfc connection invoked")
    print("request_context", request_context)
    print(f"REQUTEXT: {REQUTEXT}")

    return {
        "ECHOTEXT": REQUTEXT,
        "RESPTEXT": "消息发送自 Python 服务器"
    }


def launch_server():
    """Start server."""

    dir_path = os.path.dirname(os.path.realpath(__file__))
    set_ini_file_directory(dir_path)

    server = Server(
        {"dest": "gateway"},
        {"dest": "D01"},
        {"check_date": False, "check_time": False, "port": 8081, "server_log": False}
    )
    print(server.get_server_attributes())

    # expose python function my_stfc_connection as ABAP function STFC_CONNECTION, to be called by ABAP system
    server.add_function("STFC_CONNECTION", my_stfc_connection )

    # start server
    server.serve()

    # get server attributes
    print(server.get_server_attributes())


server_thread = Thread(target=launch_server)
server_thread.start()

input("Press Enter to stop server...\n")  # WPS110

# stop server
server_thread.join()
print("Server stoped")