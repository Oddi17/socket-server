import socket
import threading
import json
import time
import sys


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) == 1:
    s.connect(("0.0.0.0", 12345)) #адрес и порт по умолчанию
    print("adress:0.0.0.0","port:12345",sep = '\n') 
elif len(sys.argv) == 3:
    s.connect((sys.argv[1], int(sys.argv[2])))
    print(f"adress:{sys.argv[1]}",f"port:{sys.argv[2]}",sep = '\n')        
else:
    print("Error host or port (first host then port)")
    sys.exit()


def task1():
    global thread_stop
    while True:
        in_data = s.recv(1024)
        if thread_stop == True:
                print("End of working")
                break
        elif not in_data:
                thread_stop = True
                print("Server was closed, end of working")
                print("Push the \"Enter\"")
                s.close()
                break
        in_data = str(in_data).lstrip('b').strip("\'")
        war = 0    
        while war != -1:
                war = in_data.find("\\n")
                if war > 0:
                    try:
                      data_1 = json.loads(in_data[:war])
                      print("От сервера: Unit's parametrs:",json.dumps(data_1, indent=4))
                      in_data = in_data[war+2:]
                    except ValueError:  
                      print("От сервера:",in_data[:war])
                      in_data = in_data[war+2:]

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
