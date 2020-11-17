import datatorch
from datatorch import agent
import docker
import time
import os

from typing import List

from docker.models.resource import Model
from client import call_dextr, Point
from urllib.parse import urlparse


directory = os.path.dirname(os.path.abspath(__file__))
agent_dir = agent.directories().root

points = datatorch.get_input("points")
image_path = datatorch.get_input("imagePath")
address = urlparse(datatorch.get_input("url"))
image = datatorch.get_input("image")

points: List[Point] = [(10.0, 20.0), (30.0, 40.0), (50.0, 60.0), (70.0, 80.0)]
image_path = "/home/desktop/.config/datatorch/agent/temp/download-file/20201025_102443 (17th copy).jpg"


CONTAINER_NAME = "datatorch-dextr-action"


def valid_image_path():
    if not image_path.startswith(agent_dir):
        print(f"Directory must be inside the agent folder ({agent_dir}).")
        exit(1)

    if not os.path.isfile(image_path):
        print(f"Image path must be a file ({image_path}).")
        exit(1)


def start_server(port: int):
    docker_client = docker.from_env()
    print(f"Creating DEXTR container on port {port}.")
    container = docker_client.containers.run(
        image,
        detach=True,
        ports={"3000/tcp": port},
        restart_policy={"Name": "always"},
        volumes={"/agent": {"bind": agent_dir, "mode": "rp"}},
    )
    if isinstance(container, Model):
        print(f"Created DEXTR Container: {container.id}")


def send_request():
    attempts = 0

    while True:
        try:
            attempts += 1
            call_dextr(image_path, points, address.geturl())
            return
        except Exception as ex:
            if attempts > 5:
                print(ex)
                break
            print(f"Attemp: {attempts}")
            print("Could not connect to dextr.")
            start_server(address.port or 80)
            time.sleep(5)

    print("Could not send request.")
    exit(1)


if __name__ == "__main__":
    valid_image_path()
    send_request()
