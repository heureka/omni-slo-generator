import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

from slo_generator.compute import compute
from slo_generator.utils import load_config
from prometheus_client import Summary

from .config import SHARED_CONFIG

CALCULATE_TIME = Summary(
    "omni_slo_generator_calculate_time_seconds",
    "Time in seconds spent calculating SLO reports",
)


@CALCULATE_TIME.time()
def calculate(slos):
    shared_config = load_config(SHARED_CONFIG)
    logging.debug(f"Shared config: {shared_config}")

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(compute, slo, shared_config) for slo in slos]
        reports = []
        for future in as_completed(futures):
            try:
                result = future.result()
                reports.extend(result)
            except Exception as _:
                logging.exception("Compute failed")
    return reports
