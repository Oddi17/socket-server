import socket
import threading
import json
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("0.0.0.0", 12345)) #adress,port

def task1():
    global thread_stop
    while True:
        in_data = s.recv(1024)
        try:
            data_1 = json.loads(in_data)
            print("Unit's parametrs:",json.dumps(data_1, indent=4))
        except ValueError:
            if thread_stop == True:
                print("End of working")
                break
            elif not in_data: #or in_data.decode() == "File of unit (\"cond.txt\") not found"
                thread_stop = True
                print("Server was closed, end of working")
                print("Push the \"Enter\"")
                s.close()
                break
            print("От сервера:", in_data.decode(),"\n")


def task2():
  global thread_stop
  try:
    while True:
        if thread_stop == True:
            break
        out_data = input()
        s.send(out_data.encode())
        #print("Отправлено:" + str(out_data))
        if out_data == "quit":
            thread_stop = True
            break
  except OSError: #[Errno 9] Bad file descriptor
    print("End...")

try:
  threads_arr = []
  thread_stop = False
  t2 = threading.Thread(target=task2,daemon=True)
  threads_arr.append(t2)
  t1 = threading.Thread(target=task1,daemon=True)
  threads_arr.append(t1)
  t2.start()
  t1.start()
  for thr in threads_arr: # let them all start before joining
        thr.join()
except KeyboardInterrupt:
	print("\nClient end")








