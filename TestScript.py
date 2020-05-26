import sys
from client import Client, ClientError


def run(host, port):
    client1 = Client(host, port, timeout=5)
    client2 = Client(host, port, timeout=5)
    command = "wrong command test\n"

    try:
        data = client1.get(command)
    except ClientError:
        pass
    except BaseException as err:
        print(f"Error connection: {err.__class__}: {err}")
        sys.exit(1)
    else:
        print("Wrong command sent to the server must return error")
        sys.exit(1)

    command = 'some_key'
    try:
        data_1 = client1.get(command)
        data_2 = client1.get(command)
    except ClientError:
        print('The server reterned a response to a valid request, which'
              ' client identified as incorrect')
    except BaseException as err:
        print(f"The server must maintain a connection between requests"
              f"the second request to the server failed: {err.__class__}: {err}")
        sys.exit(1)

    assert data_1 == data_2 == {}, \
        "When a client requests to receive data on a non existing key, the server" \
        "must return a response with an empty data field"

    try:
        data_1 = client1.get(command)
        data_2 = client2.get(command)
    except ClientError:
        print('The server reterned a response to a valid request, which'
              ' client identified as incorrect')
    except BaseException as err:
        print(f"The server must support connection with several clients: "
              f"{err.__class__}: {err}")
        sys.exit(1)

    assert data_1 == data_2 == {}, \
        "When a client requests to receive data on a non existing key, the server " \
        "must return a response with an empty data field"

    try:
        client1.put("k1", 0.25, timestamp=1)
        client2.put("k1", 2.156, timestamp=2)
        client1.put("k1", 0.35, timestamp=3)
        client2.put("k2", 30, timestamp=4)
        client1.put("k2", 40, timestamp=5)
        client1.put("k2", 41, timestamp=5)
    except Exception as err:
        print(f"Call error client.put(...) {err.__class__}: {err}")
        sys.exit(1)

    expected_metrics = {
        "k1": [(1, 0.25), (2, 2.156), (3, 0.35)],
        "k2": [(4, 30.0), (5, 41.0)],
    }

    try:
        metrics = client1.get("*")
        if metrics != expected_metrics:
            print(f"client.get('*') returned incorrect result. Expected: "
                  f"{expected_metrics}. Received: {metrics}")
            sys.exit(1)
    except Exception as err:
        print(f"Call error client.get('*') {err.__class__}: {err}")
        sys.exit(1)

    expected_metrics = {"k2": [(4, 30.0), (5, 41.0)]}

    try:
        metrics = client2.get("k2")
        if metrics != expected_metrics:
            print(f"client.get('k2') returned incorrect result. Expected: "
                  f"{expected_metrics}. Received: {metrics}")
            sys.exit(1)
    except Exception as err:
        print(f"Call error client.get('k2') {err.__class__}: {err}")
        sys.exit(1)

    try:
        result = client1.get("k3")
        if result != {}:
            print(
                f"Error calling get method with a key that has not been added yet. "
                f"Expected: empty dictionare. Received: {result}")
            sys.exit(1)
    except Exception as err:
        print(f"Error calling get method with a key that has not been added yet: "
              f"{err.__class__} {err}")
        sys.exit(1)

    print("Everything alright.")


if __name__ == "__main__":
    run("127.0.0.1", 8888)
