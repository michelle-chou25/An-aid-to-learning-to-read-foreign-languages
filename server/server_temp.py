import socket
HOST,PORT = '', 8888

listen_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) #基于TCP协议 创建IPV4 soket

#setsockopt(level,optname,value)
#level定义了哪个选项将被使用。通常情况下是SOL_SOCKET，意思是正在使用的socket选项。
#socket.SO_REUSEADDR,1) 这里value设置为1，表示将SO_REUSEADDR标记为TRUE，操作系统会在服务器socket被关闭或服务器进程终止后马上释放该服务器的端口，否则操作系统会保留几分钟该端口。
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

listen_socket.bind((HOST, PORT))

#利用listen()函数进行侦听连接。该函数只有一个参数，其指明了在服务器实际处理连接的时候，允许有多少个未决（等待）的连接在队列中等待。作为一个约定，很多人设置为5。如：s.listen(5)
listen_socket.listen(1)
print('Serving HTTP on porrt %s ...' %PORT)

while True:
    client_connection, client_address = listen_socket.accept()
    #接收 TCP 数据，数据以字符串形式返回，bufsize 指定要接收的最大数据量。flag 提供有关消息的其他信息，通常可以忽略。
    request = client_connection.recv(bufsize=1024)
    print(request.decode("utf-8"))

    http_response = """
    HTTP/1.1 200 OK
    
    hello!
    """
    #发送完整的TCP数据，成功返回None，失败抛出异常
    client_connection.sendall(data=http_response.encode("utf-8"))
    client_connection.close()