import os

# Port at which to expose Prometheus metrics
METRICS_PORT = int(os.getenv("OMNI_SO_GENERATOR_METRICS_PORT", "8080"))

# Name of the bucket to look through for SLOs
SLO_GCS_BUCKET = os.getenv("OMNI_SLO_GENERATOR_SLO_GCS_BUCKET")

# Interval to sleep between computations. The actual total loop interval
# will be OMNI_SLO_GENERATOR_INTERVAL_SECONDS + loop execution time
INTERVAL_SECONDS = int(os.getenv("OMNI_SLO_GENERATOR_INTERVAL_SECONDS", "30"))

# Path to the shared config
SHARED_CONFIG = os.getenv("OMNI_SLO_GENERATOR_SHARED_CONFIG", "/etc/config/config.yaml")
