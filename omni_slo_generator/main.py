import logging
from time import sleep, time

from prometheus_client import Gauge, Summary, start_wsgi_server

from omni_slo_generator import config
from omni_slo_generator.collection import collect_slos
from omni_slo_generator.compute import calculate
from omni_slo_generator.export import export

LOOP_HEARTBEAT = Gauge(
    "omni_slo_generator_last_successful_loop_timestamp",
    "Last successful loop run of the Omni SLO Generator",
)
LOOP_TIME = Summary(
    "omni_slo_generator_loop_time_seconds",
    "Time in seconds spent on the entire loop, including sleep interval",
)

logging.basicConfig(level=logging.WARNING)


def main():
    start_wsgi_server(config.METRICS_PORT)
    while True:
        time_start = time()
        slos = collect_slos()
        reports = calculate(slos)
        export(reports)
        LOOP_HEARTBEAT.set_to_current_time()
        sleep(config.INTERVAL_SECONDS)
        LOOP_TIME.observe(time() - time_start)


if __name__ == "__main__":
    main()
