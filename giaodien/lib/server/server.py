# Date: 2020/9/17
# Author: Kimteawan
# Description: Server
import select
import socket
import threading
import ctypes 
import time
from pocsuite3.lib.core.common import data_to_stdout, has_poll, get_unicode, desensitization
from pocsuite3.lib.core.data import conf, kb, logger
from pocsuite3.lib.core.datatype import AttribDict
from pocsuite3.lib.core.enums import AUTOCOMPLETE_TYPE, OS, CUSTOM_LOGGING
from pocsuite3.lib.core.exception import PocsuiteShellQuitException
from pocsuite3.lib.core.settings import DEFAULT_LISTENER_PORT
from pocsuite3.lib.core.shell import auto_completion, clear_history, save_history, load_history
from pocsuite3.lib.core.threads import exception_handled_function


# from os import path
from time import sleep
# from lib import const
# from queue import Queue
# from OpenSSL import crypto
# from random import SystemRandom
# from threading import Thread, RLock
# from . lib import session, shell, interface
class Server(object):

    def __init__(self):
        self.is_active = False  # is the server active
        self.server = None
        self.port = None
        self.ip = None
        self.is_processing = False
    def get_bot(self, bot_id):
        try:
            target = int(bot_id)
            client = kb.data.clients[target]  # Connect to the selected clients
            data_to_stdout("Now Connected: {0}\n".format(
                desensitization(client.address[0] if conf.ppt else client.address[0])))
            self.client=client
            bot = {
                'ip':desensitization(client.address[0] if conf.ppt else client.address[0]),
                'OS':'unknown',
            }
            return bot
        except Exception:
            data_to_stdout("Invalid Client\n")
            return None  
    def server_start(self):
        if self.is_processing:
            return

        self.is_processing = True
        self.serverSocket=self.get_tcp_listener(ipv6=conf.ipv6, listen_port=int(self.port),listen_host=self.ip) 
        if self.serverSocket is None:
            print('Error: invalid IP')
            self.port = None
            self.ip = None
            self.is_active=False
        else:
            self.is_active=True
            self.start_listener()
        self.is_processing = False

    def total_clients(self):
        ret=0
        try:
            for i, client in enumerate(kb.data.clients):
                ret+=1
        except:
            pass
        return ret
    def server_stop(self):
        if self.is_processing:
            return

        self.is_processing = True

        if not self.is_active:
            self.is_processing = False
            return
        #stop thread action
        self.serverSocket.close()
        for i, client in enumerate(kb.data.clients):
            try:
                client.conn.close()
                del kb.data.clients[i]
            except Exception as ex:  # If a connection fails, remove it
                logger.exception(ex)
                del kb.data.clients[i]
                continue
        self.is_active = False
        self.is_processing = False
        self.ip, self.port = None, None
        logger.log(CUSTOM_LOGGING.ERROR, "Server stopped")
     
        
    # def list_clients(self):
    #     results = ''
    #     bots=[]
    #     for i, client in enumerate(kb.data.clients):
    #         try:
    #             client.conn.send(str.encode('uname\n'))
    #             time.sleep(0.01)
    #             system='unknown'
    #             ret = client.conn.recv(2048)              
    #             if ret:
    #                 ret = ret.decode('utf-8', errors="ignore")
    #                 system = "unknown"
    #                 if "darwin" in ret.lower():
    #                     system = "Darwin"
    #                 elif "linux" in ret.lower():
    #                     system = "Linux"
    #                 elif "uname" in ret.lower():
    #                     system = "Windows"

    #         except Exception as ex:  # If a connection fails, remove it
    #             logger.exception(ex)
    #             del kb.data.clients[i]
    #             continue
    #         results += (
    #             str(i) +
    #             "   " +
    #             (desensitization(client.address[0]) if conf.ppt else str(client.address[0])) +
    #             "    " +
    #             str(client.address[1]) +
    #             " ({0})".format(system) +
    #             '\n'
    #         )
    #         bot={
    #             'bot_id':str(i),
    #             'ip':(desensitization(client.address[0]) if conf.ppt else str(client.address[0])),
    #             'xinfo':str(client.address[1]),
    #             'system':system,
    #         }
    #         bots.append(bot)
    #     if results:
    #         data_to_stdout("----- Remote Clients -----" + "\n" + results)
    #     return bots
    # -------- UI -------- #

    def start(self, ip, port):
        if self.is_active:
            self.server_stop()
        self.ip, self.port = ip, int(port)
        self.server_start()
        sleep(1.2)
        return self.is_active

    def stop(self):
        if self.is_active:
            self.server_stop()
            sleep(1.2)
        return self.is_active
    def poll_cmd_execute(self,client, timeout=8):
        if has_poll():
            p = select.poll()
            event_in_mask = select.POLLIN | select.POLLPRI
            event_err_mask = select.POLLERR
            event_closed_mask = select.POLLHUP | select.POLLNVAL
            event_mask = event_in_mask | event_err_mask | event_closed_mask
            p.register(client.conn, event_mask)
            count = 0
            ret = ''

            while True:
                events = p.poll(timeout)
                if events:
                    event = events[0][1]
                    if event & select.POLLERR:
                        ret = "Client Hung up\n"
                        break

                    ready = event & select.POLLPRI or event & select.POLLIN
                    if not ready:
                        ret = "execute command timeout\n"
                        break
                    else:
                        ret += get_unicode(client.conn.recv(0x10000))
                        # ret += str(client.conn.recv(0x10000), "utf-8")
                else:
                    if ret:
                        break
                    elif count > timeout:
                        ret = "execute command timeout\n"
                        break
                    else:
                        data_to_stdout(".")
                        time.sleep(1)
                        count += 1

            p.unregister(client.conn)
        else:
            count = 0
            ret = ''
            while True:
                ready = select.select([client.conn], [], [], 0.1)
                if ready[0]:
                    ret += get_unicode(client.conn.recv(0x10000))
                    # ret += str(client.conn.recv(0x10000), "utf-8")
                else:
                    if ret:
                        break
                    elif count > timeout:
                        ret = "execute command timeout\n"
                    else:
                        data_to_stdout('.')
                        time.sleep(1)
                        count += 1

        if ret and not ret.startswith('\r'):
            ret = "\r{0}".format(ret)
        if ret and not ret.endswith('\n'):
            ret = "{0}\n".format(ret)

        return ret
    def execute_cmd_console(self,client,cmd):
        try:
            address = client.address[0]
            if not cmd:
                return ''

            client.conn.send(str.encode(cmd + '\n'))

            resp = self.poll_cmd_execute(client)

            data_to_stdout(resp)
            return resp
        except Exception as ex:
            logger.error(str(ex))
            data_to_stdout("Connection Lost\n")

    def get_sock_listener(self,listen_port, listen_host="0.0.0.0", ipv6=False, protocol=None):
        if protocol in [None, "TCP"]:
            protocol = socket.SOCK_STREAM
        elif protocol in ["UDP"]:
            protocol = socket.SOCK_DGRAM

        if ipv6:
            s = socket.socket(socket.AF_INET6, protocol)
            if listen_host == "0.0.0.0":
                listen_host = "::"
        else:
            s = socket.socket(socket.AF_INET, protocol)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            s.bind((listen_host, listen_port))
        except socket.error:
            s.close()
            # import traceback
            # traceback.print_exc()
            return None
        if protocol == socket.SOCK_STREAM:
            msg = "listening on {0}:{1}".format(listen_host, listen_port)
            logger.log(CUSTOM_LOGGING.SYSINFO, msg)
            s.listen(5)
        return s

    def get_udp_listener(self,listen_port=DEFAULT_LISTENER_PORT, listen_host="0.0.0.0", ipv6=False):
        return self.get_sock_listener(listen_port, listen_host, ipv6, "UDP")


    def get_tcp_listener(self,listen_port=DEFAULT_LISTENER_PORT, listen_host="0.0.0.0", ipv6=False):
        return self.get_sock_listener(listen_port, listen_host, ipv6, "TCP")


    def start_listener(self):
        t = threading.Thread(target=self.listener_worker)
        t.daemon=True
        t.start()
        logger.log(CUSTOM_LOGGING.SUCCESS, "Server Start Serving successfully")

    def listener_worker(self):
        while self.is_active:
            try:
                conn, address = self.serverSocket.accept()
                conn.setblocking(1)
                client = AttribDict()
                client.conn = conn
                client.address = address
                kb.data.clients.append(client)
                info_msg = "new connection established from {0}".format(
                    desensitization(address[0]) if conf.ppt else address[0])
                logger.log(CUSTOM_LOGGING.SUCCESS, info_msg)
                
            except Exception:
                pass
   


