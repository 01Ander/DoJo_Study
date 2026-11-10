# Quest 04-02 (Misión M8): Configuración de Metric Filters y Alarmas en CloudWatch (`AWS-009`)

**Objetivo:** Automatizar la observabilidad activa del worker de **FinCorp Global** (desplegado en `M7`) registrando un `Metric Filter` sobre el Log Group de CloudWatch y vinculándole una alarma (`put_metric_alarm`) que se active al primer error (`Threshold=1.0`, Lore 04 §5.1).

---

## Archivo de Trabajo

Edita [`fincorp_cloudwatch_alarm.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/cloud/chronicles/CLOUD-AWS/quests/04-aws-cloudwatch/fincorp_cloudwatch_alarm.py) e implementa la función:

### `configure_failure_alarm(logs_client: Any, cw_client: Any, log_group_name: str, metric_name: str, metric_namespace: str = "FinCorp/ETL") -> str`
1. Crea el filtro de métrica invocando:
   ```python
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
   ```
2. Define `alarm_name = f"{metric_name}-CriticalAlarm"` y crea la alarma invocando:
   ```python
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
   ```
3. Retorna `alarm_name`.

---

## 🧪 Comando de Verificación Binaria (`M8`)
```bash
/Users/ander/Documents/DoJo/DoJo_Study/content/subjects/cloud/chronicles/CLOUD-AWS/.venv/bin/pytest content/subjects/cloud/chronicles/CLOUD-AWS/quests/04-aws-cloudwatch/test_fincorp_cloudwatch_alarm.py -v
```
*(Criterio de éxito: `3 passed` con exit code 0).*

