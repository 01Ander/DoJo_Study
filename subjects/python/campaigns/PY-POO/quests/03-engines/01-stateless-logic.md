# Ejercicio 03-01: Stateless Logic (Tipo A)

**Objetivo:** Crear un motor sin estado para procesamiento de datos.

## Contexto (Domain Shifting: Clima)
Tienes una lista de objetos `DailyTemperature` con la propiedad `celsius` y debes calcular el promedio.

## Tu Tarea
En `quests/03-engines/`, crea `weather_engine.py`:
1. Crea una clase `WeatherAnalyticsEngine`.
2. Implementa un método `get_average_temp(self, days: list) -> float`.
3. El método debe iterar la lista, sumar los `.celsius` y devolver el promedio. Si la lista está vacía, devuelve 0.0.

---
<details>
<summary>👀 Ver Solución Esperada</summary>

```python
class WeatherAnalyticsEngine:
    def get_average_temp(self, days: list) -> float:
        if not days:
            return 0.0
            
        total = sum(day.celsius for day in days)
        return total / len(days)
```
</details>
