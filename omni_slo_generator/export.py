from prometheus_client import Gauge
from slo_generator.exporters.base import MetricsExporter
from slo_generator.migrations.migrator import report_v2tov1
from slo_generator.report import SLOReport


class PrometheusSelfExporter(MetricsExporter):
    """Prometheus exporter class which uses
    the API mode of itself to export the metrics."""

    REGISTERED_METRICS = {}

    def __init__(self):
        pass

    def export_metric(self, data):
        """Export data to Prometheus global registry.
        Args:
            data (dict): Metric data.
        """
        name = data["name"]
        description = data["description"]
        value = data["value"]

        # Write timeseries w/ metric labels.
        labels = data["labels"]
        gauge = self.REGISTERED_METRICS.get(name)
        if gauge is None:
            gauge = Gauge(name, description, labelnames=labels.keys())
            PrometheusSelfExporter.REGISTERED_METRICS[name] = gauge
        gauge.labels(*labels.values()).set(value)


EXPORTER = PrometheusSelfExporter()


def export(reports):
    for report in reports:
        EXPORTER.export(report_v2tov1(report))
