class WeatherAnalyticsEngine:

    def get_average_temp(self, days: list) -> float:
        # ~My solution~
        # average_temp = 0.0
        # count = 0
        # for day in days:
        #     average_temp += day.celsius
        #     count += 1
        # return average_temp / count
        # ~~~~~~~

        if not days:
            return 0.0
        total = sum(days.celsius for day in days)
        return total / len(days)
