
import json
import os
from datetime import date, timedelta
from pathlib import Path


def generate_report(previous_costs, current_costs):
    services = sorted(set(previous_costs) | set(current_costs))
    service_reports = []

    previous_total = 0.0
    current_total = 0.0

    for service in services:
        old_cost = float(previous_costs.get(service, 0))
        new_cost = float(current_costs.get(service, 0))

        difference = new_cost - old_cost
        previous_total += old_cost
        current_total += new_cost

        percentage = (
            (difference / old_cost) * 100
            if old_cost > 0 else None
        )

        if difference > 0 and (
            percentage is None or percentage >= 50
        ):
            status = "investigate_increase"
        elif difference > 0:
            status = "increased"
        elif difference < 0:
            status = "decreased"
        else:
            status = "unchanged"

        service_reports.append({
            "service": service,
            "previous_cost": round(old_cost, 2),
            "current_cost": round(new_cost, 2),
            "difference": round(difference, 2),
            "percentage_change": (
                round(percentage, 2)
                if percentage is not None else None
            ),
            "status": status
        })

    return {
        "report_date": date.today().isoformat(),
        "currency": "USD",
        "previous_period_total": round(previous_total, 2),
        "current_period_total": round(current_total, 2),
        "total_difference": round(current_total - previous_total, 2),
        "services": service_reports
    }


def fetch_aws_weekly_costs():
    """Fetch the previous two completed 7-day periods from AWS."""
    import boto3

    today = date.today()
    current_start = today - timedelta(days=7)
    previous_start = today - timedelta(days=14)

    profile = os.getenv("AWS_PROFILE", "cloudspend")

    session = boto3.Session(
        profile_name=profile,
        region_name="us-east-1"
    )
    client = session.client("ce")

    response_data = {
        "previous": {},
        "current": {}
    }

    request = {
        "TimePeriod": {
            "Start": previous_start.isoformat(),
            "End": today.isoformat()
        },
        "Granularity": "DAILY",
        "Metrics": ["UnblendedCost"],
        "GroupBy": [
            {"Type": "DIMENSION", "Key": "SERVICE"}
        ]
    }

    # AWS may paginate results, so retrieve every page.
    while True:
        response = client.get_cost_and_usage(**request)

        for day in response.get("ResultsByTime", []):
            day_start = date.fromisoformat(day["TimePeriod"]["Start"])

            period_name = (
                "current" if day_start >= current_start else "previous"
            )

            for group in day.get("Groups", []):
                service = group["Keys"][0]
                amount = float(
                    group["Metrics"]["UnblendedCost"]["Amount"]
                )

                costs = response_data[period_name]
                costs[service] = costs.get(service, 0.0) + amount

        token = response.get("NextPageToken")
        if not token:
            break

        request["NextPageToken"] = token

    return response_data["previous"], response_data["current"]


def main():
    print("Fetching AWS Cost Explorer data...")

    previous_costs, current_costs = fetch_aws_weekly_costs()
    report = generate_report(previous_costs, current_costs)

    report["periods"] = {
        "previous_start": (
            date.today() - timedelta(days=14)
        ).isoformat(),
        "previous_end": (
            date.today() - timedelta(days=7)
        ).isoformat(),
        "current_start": (
            date.today() - timedelta(days=7)
        ).isoformat(),
        "current_end": date.today().isoformat(),
        "note": "End dates are exclusive; today's incomplete data is excluded."
    }

    output_file = Path(__file__).with_name("weekly_report.json")

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=2)

    print(f"Report saved to: {output_file}")
    print(f"Previous 7-day cost: ${report['previous_period_total']:.2f}")
    print(f"Current 7-day cost:  ${report['current_period_total']:.2f}")
    print(f"Difference:          ${report['total_difference']:.2f}")


if __name__ == "__main__":
    main()
