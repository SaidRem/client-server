import asyncio
from collections import defaultdict
from copy import deepcopy


class StorageDataError(ValueError):
    pass


class Storage:
    """class for store metics in process memory"""

    def __init__(self):
        self._data = defaultdict(dict)

    def put(self, key, value, timestamp):
        self._data[key][timestamp] = value

    def get(self, key):
        if key == '*':
            return deepcopy(self._data)
        if key in self._data:
            return {key: deepcopy(self._data.get(key))}
        return {}


class StorageData:
    """works with storage"""
    
    def __init__(self, storage):
        self.storage = storage

    def __call__(self, data):
        method, *params = data.split()
        if method == 'put':
            key, value, timestamp = params
            value, timestamp = float(value), int(timestamp)
            self.storage.put(key, value, timestamp)
            return {}
        elif method == 'get':
            key = params.pop()
            if params:
                raise StorageDataError
            return self.storage.get(key)
        else:
            raise StorageDataError


class Server_for_Metrics(asyncio.Protocol):
    """server with magic of asyncio"""

    storage = Storage()
    sep = '\n'
    error_message = 'wrong command'
    code_err = 'error'
    code_ok = 'ok'

    def __init__(self):
        seper().__init__()
        self.dr = StorageData(self.storage)
        self._buffer = 'b'

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        """the method calls when data receive in a socket"""

        self._buffer += data

        try:
            request = self._buffer.decode()
            # wait for data if command is not completed with \n
            if not request.endswith(self.sep):
                return

            self._buffer, message = b'', ''
            raw_data = self.dr(request.rstrip(self.sep))

            for key, values in raw_data.items():
                message += self.sep.join(f'{key} {value} {timestamp}'
                                         for timestamp, value in sorted(values.items())
                message += self.sep
            
            code = self.code_ok
        except (ValueError, UnicodeDecodeError, IndexError):
            message = self.error_message + self.sep
            code = self.code_err

        response = f'{code}{self.sep}{message}{self.sep}'
        #send
        self.transport.write(response.encode())


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(Server_for_Metrics, host, port)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_close())
    loop.close()


if __name__ == "__main__":
    run server("127.0.0.1", 8888)
