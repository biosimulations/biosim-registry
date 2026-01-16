import logging

from process_bigraph import ProcessTypes, generate_core

from pbest import standard_types

logger = logging.getLogger(__name__)

loaded_core: ProcessTypes | None = None


def set_logging_config(level: str) -> None:
    logging.basicConfig(level=level)


def get_loaded_core() -> ProcessTypes:
    global loaded_core
    if loaded_core is None:
        loaded_core = generate_core()
        logger.debug(f"Process registry: {loaded_core.process_registry.registry}")
        for k, i in standard_types.items():
            loaded_core.register(k, i)
    return loaded_core


def reload_core() -> ProcessTypes:
    global loaded_core
    loaded_core = generate_core()
    for k, i in standard_types.items():
        loaded_core.register(k, i)
    return loaded_core
