import docker


def is_docker_present() -> bool:
    client = docker.from_env()
    try:
        client.ping()
        return True
    except Exception:
        return False


