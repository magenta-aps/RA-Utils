#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
# Inspired by:
# https://github.com/prometheus/client_python#exporting-to-a-pushgateway
try:
    from prometheus_client import CollectorRegistry
    from prometheus_client import Gauge
    from prometheus_client import push_to_gateway
except ImportError:  # pragma: no cover
    raise ImportError("Optional dependency prometheus_client is not installed")


class MetricExporter:
    def __init__(self, metric_name: str, description: str, pushgateway_host: str):
        self.metric_name = metric_name
        self.description = description
        self.pushgateway_host = pushgateway_host

    def export_metrics(self, metrics: dict) -> None:
        """Write metrics from a dict to pushgateway"""
        for job, value in metrics.items():
            self.export_metric(job, value)

    def export_metric(self, job: str, value: int) -> None:
        """Write a single metric to pushgateway"""
        registry = CollectorRegistry()
        g = Gauge(self.metric_name, self.description, registry=registry)
        g.set(value)
        push_to_gateway(self.pushgateway_host, job=job, registry=registry)


if __name__ == "__main__":
    exporter = MetricExporter(
        "example_metric", "This is just an example", "localhost:9091"
    )
    exporter.export_metric("test", 1)
