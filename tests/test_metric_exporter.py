#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
from unittest import TestCase
from unittest.mock import patch

from ra_utils.metric_exporter import MetricExporter


class MetricExporterTests(TestCase):
    @patch("prometheus_client.push_to_gateway")
    def setUp(self, push_mock):
        self.metricexporter = MetricExporter("test", "test2", "test3")

    def test_setup(self):
        assert self.metricexporter

    @patch("ra_utils.metric_exporter.MetricExporter.export_metric")
    def test_batch(self, export_mock):
        self.metricexporter.export_metrics({"test": 1, "test2": 2})
        export_mock.assert_called()
        export_mock.assert_called_with("test2", 2)
