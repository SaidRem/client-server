# client-server
Socket programming in Python using asyncio library. 

The server stores data and processes calls from several clients.
The client for sending and receiving metrics to test server.

The client and server communicate with each other over a simple text protocol through TCP sockets.

The client supports two types of requests to the server
- sending data to save it on the server;
- retrieving saved data.
General format of the client request: <command> <request data><\n>
 Where:
  - <command> - server command. The command can take one of two values: put -save data on the server, get - return saved data from the server.
  - <request data> - 
General server response format: <status of server><\n><response data><\n\n>
