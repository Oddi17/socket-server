import socket
import os
import json
import threading
import time
import sys

def check_file(cid):
    global timestamp
    while True:
        if timestamp != os.stat('cond.txt').st_mtime:
            data = json.load(open('data.json')) #предыдущий jsonfile
            unit() 
            lastdata = json.load(open('data.json')) #новый jsonfile
            stroka = ""
            for i in data.keys():
                for k in lastdata.keys():
                    if (i == k) and (data.get(i) != lastdata.get(k)):
                        stroka += k + " " + "was changed in file of unit!!!!!!" + "\n"
            print(stroka)
            for c in client_list:
                connection = c[0]
                connection.send(stroka.encode())
            timestamp = os.stat('cond.txt').st_mtime
        time.sleep(1)

def start_server(host, port):
  global client_list
  global timestamp
  serv = creat_server(host, port)
  cid = 0
  try: 
    unit() #файл в директории и jsonfile
    timestamp = os.stat('cond.txt').st_mtime #состояние файла
    check = threading.Thread(target=check_file, args=(cid,), daemon = True)
    check.start() #поток проверки 
    client_list = []
    while True:
        sock = accept_sock(serv, cid)
        print("Client list:",len(client_list))
        t = threading.Thread(target=serv_client, args=(sock, cid),daemon = True)  #поток для клиента
        t.start()
        cid += 1
  except FileNotFoundError:
    print("Server end!")
    print("File of unit (\"cond.txt\") not found, check the directory!!!")

def creat_server(serv_host, serv_port):
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serv.bind((serv_host, serv_port))
    serv.listen()
    print("server is waiting connect ...")
    return serv

def accept_sock(s, cid):
    global client_list
    sock, ip = s.accept()
    client_info = [sock]
    client_list.append(client_info) #список клиентов
    print(f'\nClient #{cid} connected '
          f'{ip[0]}:{ip[1]}')
    return sock

def serv_client(sock, cid):
  global thread_stop
  global client_list
  try:
    while True:
        sock.send(("hello! Write \"ok\" to continue or \"quit\" to get out\n").encode())
        data = sock.recv(1024).decode()
        if data == "quit" or not data:
            thread_stop = True
            if thread_stop == True:
                print("Client: #%s is out" % cid)
                for k in client_list:
                  if k == [sock]:
                    client_list.remove(k) #удаление клиента из списка
                    print("Client list:",len(client_list))
                sock.close()  		
                return  #останавливаем цикл
        elif data == "ok":
            main(sock)
        else:
            sock.send("Wrong command!\n".encode())
  except BrokenPipeError:
    print("Connection with client #%s was lost" %cid)
    print("Client: #%s is out" % cid)
    for k in client_list:
      if k == [sock]:
        client_list.remove(k) #удаление клиента из списка
        print("Client list:",len(client_list))
    #sock.close()

def main(sock):
    while True:
       	sock.send(("Put the number of function: 1-show, 2-set, 0-exit:\n").encode())
        number = sock.recv(1024).decode()
        if number == "1":
            unit()
            show(sock)
        elif number == "2":
            while True:
                mes = ("Select the values of angles you want to change:" + "\n" + "1-Change angle of back,"
                + "\n" + "2-Change angle of hip," + "\n" + "3-Change angle of ankle," + "\n" + "0-Back to menu"+ "\n")
                sock.send(mes.encode())
                param = sock.recv(1024).decode()
                if param == "1":
                    set_param(sock, 1)
                elif param == "2":
                    set_param(sock, 2)
                elif param == "3":
                    set_param(sock, 3)
                elif param == "0":
                    print("Backing...")
                    break
                else:
                    sock.send(("Not that command!\n").encode())
        elif number == "0":
            print("Backing...")
            break
        else:
            sock.send(("Error:Not that function, try again\n").encode())

def unit():
    if os.path.isfile('cond.txt'):
        data_unit = {}
        with open('cond.txt', 'r') as file:
            for line in file:
                key, dict = line.strip().split(None, 1)
                data_unit[key] = dict.strip()
                json.dump(data_unit, open('data.json', 'w+'))
        return

def show(sock):
    data = json.load(open('data.json'))
    base = {}
    for i in data.keys():
        if i != "High":
            base[i] = data.get(i)
    sock.send(json.dumps(base).encode()+b"\n")

def save(data):
    global timestamp
    with open("cond.txt", "w") as file:
        strick = ""
        for k in data.items():
            name, value = str(k).strip("()").split(",", 1)
            name = name.strip("\"")
            value = value.strip("\"")
            strick += name.strip("\'") + " " + value.strip().replace('\'', '') + "\n"
        file.writelines(strick)
        timestamp = os.stat('cond.txt').st_mtime

def set_param(sock, param):
  global timestamp
  with open("data.json") as file:
      data = json.load(file)
      try:
        if param == 1:
            for i in data.keys():
                if i == "Angle_back":
                    sock.send(("Set the value of \"Angle_back\" (only integer values) [from 0 to 50] :\n").encode())
                    value = sock.recv(1024).decode()
                    data[i] = value
                    break
            if int(value) >= 0 and int(value) <= 50:
                json.dump(data, open('data.json', 'w'))
                save(data)
                sock.send(("The value is saved\n").encode())
            else:
               sock.send(("Wrong value,try again:\n").encode())
        elif param == 2:
            for i in data.keys():
                if i == "Angle_hip":
                    sock.send(("Set the value of \"Angle_hip\" [from -15 to 15] :\n").encode())
                    value = sock.recv(1024).decode()
                    data[i] = value
                    break
            if int(value) >= -15 and int(value) <= 15:
                json.dump(data, open('data.json', 'w'))
                save(data)
                sock.send(("The value is saved\n").encode())
            else:
               sock.send(("Wrong value,try again:\n").encode())
        elif param == 3:
            for i in data.keys():
                if i == "Angle_ankle":
                    sock.send(("Set the value of \"Angle_ankle\" [from 0 to 30]:\n").encode())
                    value = sock.recv(1024).decode()
                    data[i] = value
                    break
            if int(value) >= 0 and int(value) <= 30:
                json.dump(data, open('data.json', 'w'))
                save(data)
                sock.send(("The value is saved!!!!\n").encode())
            else:
               sock.send(("Wrong value,try again:\n").encode())
      except ValueError:
      	   sock.send(("Wrong value: float-number,try again\n").encode())

if __name__ == "__main__":
	
    
    if len(sys.argv) == 1:
        tcp_host, tcp_port = "0.0.0.0", 12345 #адрес и порт по умолчанию
        print(f"host:{tcp_host}",f"port:{tcp_port}",sep = '\n') 
    elif len(sys.argv) == 3:
        tcp_host,tcp_port = sys.argv[1],int(sys.argv[2])
        print(f"host:{tcp_host}",f"port:{tcp_port}",sep = '\n')        
    else:
        print("Error host or port (first host then port)")
        sys.exit()
    
    try:
        start_server(tcp_host, tcp_port)
        
        thread_stop = False
    except KeyboardInterrupt:
        print("\nServer end")
