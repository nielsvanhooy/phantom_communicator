import timeit

from phantom_communicator import Communicator


def get_data(ip):
    communicator = Communicator.factory(
        host="10.17.28.194",
    )
    with communicator as conn:
        # response = conn.send_command("show ip route")
        response_again = conn.send_commands(["show run", "show ip int brief", "show ip route"])
        print(f"gathered info for {ip}")
        return response_again.result


def communicate():
    cpes = [
        "10.1.1.154",
        "10.17.28.193",
        "10.1.1.155",
        "10.17.28.194",
        "10.1.1.156",
        "10.1.1.154",
        "10.17.28.193",
        "10.1.1.155",
        "10.17.28.194",
        "10.1.1.156",
        "10.1.1.154",
        "10.17.28.193",
        "10.1.1.155",
        "10.17.28.194",
        "10.1.1.156",
        "10.1.1.154",
        "10.17.28.193",
        "10.1.1.155",
        "10.17.28.194",
        "10.1.1.156",
    ]
    for cpe in cpes:
        get_data(cpe)


if __name__ == "__main__":
    result = timeit.timeit("communicate()", setup="from __main__ import communicate", number=3)
    print(result)
