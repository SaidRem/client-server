import time
import socket


class ClientError(Exception):
    """Client's exception class"""
    pass


class Client:
    def __init__(self, host, port, timeout=None):
        self._host = host
        self._port = port
        self._timeout = timeout
        try:
            self.sock = socket.create_connection(
                (self._host, self._port), self._timeout
                )
        except socket.error as err:
            raise ClientError("Cannot create the connection", err)

    def close(self):
        """Close the socket"""
        try:
            self.sock.close()
        except socket.err as err:
            raise ClientError("Error. The connection did not close.", err)

    def validate_dgt(self, string):
        """Checks integers data received from the server"""
        if string.isdigit():
            return int(string)
        raise ClientError("The Server returns invalid timestamp")

    def validate_flt(self, string):
        """Checks data for float""" 
        if string[:string.find('.')].isdigit():
            return float(string)
        raise ClientError("The Server returns invalid value")

    def validate_key(self, key_v):
        valid_keys = ['palm.cpu', 'palm.usage', 'palm.disk_usage',
                      'palm.network_usage', 'eardrum.cpu', 'eardrum.usage',
                      'eardrum.disk_usage', 'eardrum.network_usage']
        if key_v not in valid_keys:
            raise ClientError("The Server returns invalid key")

    def put(self, servern, val, timestamp=None):
        self.servern = str(servern)
        self.val = str(val)
        self.timestamp = timestamp or int(time.time())
        for_put_send = f'put {self.servern} {self.val} {self.timestamp}\n'
        self.sock.sendall(for_put_send.encode('utf-8'))
        data = self.sock.recv(1024)
        data = data.decode('utf-8')
        if 'ok\n\n' != data:
            raise ClientError("The Sever returns error")

    def get(self, key_req):
        self._key_req = key_req
        for_get_send = f'get {self._key_req}\n'
        self.sock.sendall(for_get_send.encode('utf-8'))
        data = self.sock.recv(1024)
        data = data.decode('utf-8')
        if data[:2] != 'ok':
            raise ClientError("The Server returns invalid data")
        if data == 'ok\n\n':
            return {}
        dict_met = {}
        cleaned_data = data.strip('ok\n\n').split('\n')
        for row in cleaned_data:
            row_i = row.split(' ')
            if len(row_i) != 3:
                raise ClientError
            else:
                if row_i[0] in dict_met:
                    dict_met[row_i[0]].append((self.validate_dgt(row_i[2]),
                                               self.validate_flt(row_i[1])))
                else:
                    dict_met[row_i[0]] = [(self.validate_dgt(row_i[2]),
                                           self.validate_flt(row_i[1]))]
        for key in dict_met:
            dict_met[key].sort(key=lambda x: x[0])
        return dict_met


