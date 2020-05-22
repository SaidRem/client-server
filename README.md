# client-server
Socket programming in Python using asynio library. 

Sockets can be configured to act as a server and listen for incoming messages, or connect to other applications as a client. After both ends of a TCP/IP socket are connected, communication is bi-directional.

The client supports two types of requests to the server
- sending data to save it on the server;
- retrieving saved data.
General format of the client request: <command> <request data><\n>
 Where:
  - <command> - server command. The command can take one of two values: put -save data on the server, get - return saved data from the server.
  - <request data> - 
