"""Suite evaluadora para Misión M8 (AWS-009): CloudWatch Metric Filters & Alarms."""

from pathlib import Path
import sys
from unittest.mock import MagicMock

sys.path.insert(0, str(Path(__file__).parent))

from fincorp_cloudwatch_alarm import configure_failure_alarm


def test_configure_failure_alarm_registers_metric_filter():
    mock_logs = MagicMock()
    mock_cw = MagicMock()

    alarm_name = configure_failure_alarm(
        mock_logs,
        mock_cw,
        log_group_name="/aws/lambda/fincorp-gold-worker",
        metric_name="FinCorpWorkerErrors",
    )

    assert alarm_name == "FinCorpWorkerErrors-CriticalAlarm"
    mock_logs.put_metric_filter.assert_called_once_with(
        logGroupName="/aws/lambda/fincorp-gold-worker",
        filterName="FinCorpWorkerErrors-Filter",
        filterPattern="ERROR",
        metricTransformations=[
            {
                "metricName": "FinCorpWorkerErrors",
                "metricNamespace": "FinCorp/ETL",
                "metricValue": "1",
            }
        ],
    )


def test_configure_failure_alarm_registers_cloudwatch_alarm_threshold():
    mock_logs = MagicMock()
    mock_cw = MagicMock()

    configure_failure_alarm(
        mock_logs,
        mock_cw,
        log_group_name="/aws/lambda/fincorp-gold-worker",
        metric_name="FinCorpWorkerErrors",
    )

    mock_cw.put_metric_alarm.assert_called_once_with(
        AlarmName="FinCorpWorkerErrors-CriticalAlarm",
        MetricName="FinCorpWorkerErrors",
        Namespace="FinCorp/ETL",
        Statistic="Sum",
        Period=60,
        EvaluationPeriods=1,
        Threshold=1.0,
        ComparisonOperator="GreaterThanOrEqualToThreshold",
    )


def test_configure_failure_alarm_supports_custom_namespace():
    mock_logs = MagicMock()
    mock_cw = MagicMock()

    configure_failure_alarm(
        mock_logs,
        mock_cw,
        log_group_name="/aws/lambda/custom-worker",
        metric_name="CustomErrors",
        metric_namespace="CustomCorp/Pipelines",
    )

    assert (
        mock_logs.put_metric_filter.call_args.kwargs["metricTransformations"][0]["metricNamespace"]
        == "CustomCorp/Pipelines"
    )
    assert mock_cw.put_metric_alarm.call_args.kwargs["Namespace"] == "CustomCorp/Pipelines"

