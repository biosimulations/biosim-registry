import docker


def is_docker_present() -> bool:
    client = docker.from_env()
    try:
        client.ping()
        return True  # noqa: TRY300
    except Exception:
        return False
