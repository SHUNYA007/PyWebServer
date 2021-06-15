import socket
import threading
import json

IP='127.0.0.1'
PORT=8081
ADDR=(IP,PORT)
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)#create server socket
server.bind(ADDR)

randomData={'USERS':[]}

def handle_client(conn,addr):
    print(f'New Connection from {addr}')
    connected=True
    # while connected:
    request = conn.recv(1024).decode()
    print(request)
    head=request.split('\n')
    #print(head)
    requestType = head[0].split()[0]
    pageName=head[0].split()[1]
    if requestType == 'GET':
        if pageName=='/':
            htmlFile = open('abcd.html')
            content = htmlFile.read()
            htmlFile.close()
            response = 'HTTP/1.0 200 OK\n\n'+content
        elif pageName=='/result':
            content = json.dumps(randomData)
           
            response = 'HTTP/1.0 200 OK\n\n'+content
        else:
            content='NOT FOUND'
            response = 'HTTP/1.0 404 NOT FOUND\n\n'+content
    elif requestType =='POST':
        if head[-1]!='':
            result=head[-1].split('&')
        else:
            result=head[0].split()[1][2:0]
        print(result)
        newdata={}
        for index,val in enumerate(result):
            op=val.split('=')
            newdata[op[0]]=op[1]
        randomData['USERS'].append(newdata)
        print(randomData)
        content='<html><body> <p>YOU HAVE SENT POST REQUEST</p><p>added data:'+json.dumps(result)+'</p></body></html>'
        
        response = 'HTTP/1.0 200 OK\n\n'+content
    else:
        content ='BAD REQUEST'
        response = 'HTTP/1.0 400 BAD REQUEST\n\n'+content
    print('sending:',response)
    conn.send(response.encode())
    conn.close()
    
    
def start():
    server.listen(1)
    print('Listening on port %s ...' % PORT)
    while True:
        conn,addr=server.accept()#client details goes to conn and address on addr
        thread=threading.Thread(target=handle_client,args=(conn,addr))#everytime client connects new thread opens
        thread.start()
        
start()   
server.close()