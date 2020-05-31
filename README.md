# client-server (asyncio)
Socket programming in Python using asyncio library. 

The server stores data and processes calls from several clients. The server is asynchronous.
The client for sending and receiving metrics to test server.

The client and server communicate with each other over a simple text protocol through TCP sockets.

The client supports two types of requests to the server
- sending data to save it on the server;
- retrieving saved data.
General format of the client request: <command> <request data><\n>
 Where:
  - <command> - server command. The command can take one of two values: put -save data on the server, get - return saved data from the server.
  - <request data> - 
General server response format: <response status><\n><response data><\n\n>
 <response status> - command execution status, two options are possible: "ok" - the was successfully executed on the server and
  "error" - the command completed with error.
  <response data> - optional field.
For each metric (<key>), data store on the server: values (<value>) and the time when the measurement was made (<timestamp>).
In cases of:
   -when a non-existing key is transmitted in a request for data;
   -successful execution of put command for data save;
  The server sends the client a string with the status 'ok' and an empty field.
When working with a client, the server support sessions, communication with the client between requests stays.
