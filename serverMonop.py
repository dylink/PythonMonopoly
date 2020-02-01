import os
import sys
from tkinter import *
import socket
import select
import threading
import queue
import datetime
import random
import time


class Serveur:

    def __init__(self, q):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self._sock.bind((socket.gethostbyname('127.0.0.1'), int(1233)))
        self.nb_con = 2
        self._sock.listen(self.nb_con)
        self.pseudo = ""
        self.logged = []
        self.run = True

        try:
            while len(self.logged) <= self.nb_con:
                client, adresse = self._sock.accept()
                print(adresse, " connected\n")
                self._t = threading.Thread(target=self.recv, args=(client,)).start()
                self.logged.append(client)
                client.send(('PSD ' + self.pseudo + '\n').encode())
        except KeyboardInterrupt:
            self._sock.close()


    def recv(self, client):
        print("threads actifs == ", threading.active_count())
        pseud = ''
        try:
            while self.run:
                msg = client.recv(1024).decode().strip()
                if msg.startswith('PSD'):
                    pseud = msg.split(' ', 1)[1]
                    if not pseud in self.pseudo:
                        self.pseudo+=msg.split(' ', 1)[1]
                        print(self.pseudo)
                        self.pseudo+='/'
                        if len(self.logged) == self.nb_con:
                            self.inf(self.logged, (str(self.nb_con) + '/' + self.pseudo))
                            time.sleep(5)
                            de1 = random.randint(1,6)
                            de2 = random.randint(1,6)
                            self.plt(self.logged,  str(de1+de2)+'/0/0/0/0/0/1500/1500/1500/1500/1500/1500/0/0/0/0/0/0/0/0/0/0/0/0/0/0/0/0/0/0/0/0/0/0/0/0/0/0/0/0/0/0/0/0/0/0/0/0/0/0/0/0/0/0/0/0/0/0/0/0/0/0/0/0/0/0/0/0/'+ str(de1) + '/' + str(de2) +'/0/0')
                elif msg.startswith('PLT'):
                    list = []
                    datas = msg.split(' ',1)[1]
                    self.getplt(datas, list)
                    list[68] = random.randint(1,6)
                    list[69] = random.randint(1,6)
                    list[list[71]] += list[68]+list[69]
                    if list[list[71]] > 39:
                        list[list[71]] -= 40
                    print("check ", list[71])
                    self.sendplt(list)
                elif msg.startswith('FIN'):
                    pseudo = msg.split(' ',1)[1]
                    self.fin(self.logged, pseudo)
                else:
                    client.send('ERR\n'.encode())
        except BrokenPipeError:
            self.pseudo = ''
            self.logged.remove(client)
            client.close()



    def getplt(self, datas, list):
        data = datas.split('/')
        for i in range(0, 72):
            if i < 6:
                list.append(int(data[i]))
            elif 5 < i < 12:
                list.append(int(data[i]))
            elif 11 < i < 68:
                list.append(int(data[i]))
            elif i == 68:
                list.append(int(data[i]))
            elif i == 69:
                list.append(int(data[i]))
            elif i == 70:
                list.append(int(data[i]))
            elif i == 71:
                list.append(int(data[i]))

    def sendplt(self, list):
        data = ""
        for i in range(0, 72):
            if i < 6:
                data += str(list[i])
                data += ('/')
            elif 5 < i < 12:
                data += str(list[i])
                data += ('/')
            elif 11 < i < 68:
                data += str(list[i])
                data += ('/')
            elif i == 68:
                data += str(list[i])
                data += ('/')
            elif i == 69:
                data += str(list[i])
                data += ('/')
            elif i == 70:
                data += str(list[i])
                data += ('/')
            elif i == 71:
                data += str(list[i])
        self.plt(self.logged, data)

    def fin(self, clients, msg):
        if clients:
            for clien in clients:
                clien.send(('FIN ' + msg + '\n').encode())
                #clien.close()

    def plt(self, clients, msg):
        if clients:
            for clien in clients:
                clien.send(('PLT ' + msg + '\n').encode())

    def inf(self, clients, msg):
        if clients:
            for clien in clients:
                clien.send(('INF ' + msg + '\n').encode())

    def msg(self, clients, msg, pseud):
        for clien in clients:
            clien.send(('MSG ' + pseud + ' ' + msg + '\n').encode())

    def send(self, client):
        while self.run:
            print("Ecrivez un message")
            msg = input()
            client.send(msg.encode())



class App:

    def __init__(self):
        self._q = queue.Queue()
        self._serveur = Serveur(self._q)

if __name__ == '__main__':
    App()
