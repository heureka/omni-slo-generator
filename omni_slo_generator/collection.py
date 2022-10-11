import logging

from google.cloud import storage as GCS
from cachetools.func import ttl_cache
from prometheus_client import Summary
from slo_generator.utils import parse_config

from omni_slo_generator import config

COLLECTION_TIME = Summary(
    "omni_slo_generator_collection_time_seconds",
    "Time in seconds spent collecting SLO manifests",
)


@COLLECTION_TIME.time()
def collect_slos():
    gcs_bucket = config.SLO_GCS_BUCKET
    slos = []
    if gcs_bucket is not None:
        slos.extend(collect_from_gcs_bucket(gcs_bucket))
    return [parse_config(content=slo) for slo in slos]


def collect_from_gcs_bucket(gcs_bucket):
    slos = []
    blobs: list[GCS.Blob] = GCS.Client().list_blobs(gcs_bucket)
    for blob in blobs:
        if ".yaml" in blob.name or '.yml' in blob.name:
            slos.append(download_blob(blob))

    logging.debug(f"Filtered through blobs and {len(slos)} remain")
    return slos


@ttl_cache(60*30)
def download_blob(blob):
    return blob.download_as_text()
