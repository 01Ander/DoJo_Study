"""
Quest 04-02 (Misión M8): Metric Filters y CloudWatch Alarms (AWS-009)
Dominio: FinCorp Global Cloud Observability (Monitorea los logs del Worker de M7)
"""

from typing import Any


def configure_failure_alarm(
    logs_client: Any,
    cw_client: Any,
    log_group_name: str,
    metric_name: str,
    metric_namespace: str = "FinCorp/ETL",
) -> str:
    """
    1. Registra un Metric Filter con `logs_client.put_metric_filter(...)` usando:
       - logGroupName=log_group_name
       - filterName=f"{metric_name}-Filter"
       - filterPattern="ERROR"
       - metricTransformations=[{"metricName": metric_name, "metricNamespace": metric_namespace, "metricValue": "1"}]
    2. Registra la alarma con `cw_client.put_metric_alarm(...)` usando:
       - AlarmName=f"{metric_name}-CriticalAlarm"
       - MetricName=metric_name
       - Namespace=metric_namespace
       - Statistic="Sum"
       - Period=60
       - EvaluationPeriods=1
       - Threshold=1.0
       - ComparisonOperator="GreaterThanOrEqualToThreshold"
    3. Retorna el nombre de la alarma (`f"{metric_name}-CriticalAlarm"`).
    """
    # TODO: Implementar configuración de Metric Filter y CloudWatch Alarm
    logs_client.put_metric_filter(
        logGroupName=log_group_name,
        filterName=f"{metric_name}-Filter",
        filterPattern="ERROR",
        metricTransformations=[
            {
                "metricName": metric_name,
                "metricNamespace": metric_namespace,
                "metricValue": "1",
            }
        ],
    )

    # 2. Crear la Alarma en CloudWatch que se activa cuando la métrica llega a >= 1.0
    alarm_name = f"{metric_name}-CriticalAlarm"
    cw_client.put_metric_alarm(
        AlarmName=alarm_name,
        MetricName=metric_name,
        Namespace=metric_namespace,
        Statistic="Sum",
        Period=60,
        EvaluationPeriods=1,
        Threshold=1.0,
        ComparisonOperator="GreaterThanOrEqualToThreshold",
    )
    return alarm_name
