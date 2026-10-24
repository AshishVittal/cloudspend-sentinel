\# CloudSpend Sentinel



A Python-based AWS cost monitoring project that retrieves billing data from AWS Cost Explorer, compares service-level costs across two consecutive 7-day periods, and generates a JSON report highlighting spending increases.



\## Problem Statement



AWS costs can be difficult to monitor when multiple services are involved. CloudSpend Sentinel helps make cost changes easier to review by comparing recent costs with the previous week and flagging increases that may need investigation.



\## Features



\- Retrieves real AWS cost data using the AWS Cost Explorer API.

\- Groups costs by AWS service.

\- Compares two consecutive 7-day periods.

\- Calculates cost differences and percentage changes.

\- Flags significant increases for investigation.

\- Generates a structured JSON report.

\- Includes automated tests for the report-generation logic.



\## Architecture



1\. An IAM user with restricted permissions authenticates the AWS CLI/SDK.

2\. Python uses Boto3 to call AWS Cost Explorer.

3\. Cost data is grouped by AWS service for each period.

4\. The report generator calculates changes and assigns a status.

5\. The results are written to `weekly\_report.json`.



\## Technologies



\- Python

\- AWS Cost Explorer

\- AWS IAM

\- AWS CLI

\- Boto3

\- pytest

\- Git and GitHub



\## Prerequisites



\- Python installed

\- AWS CLI configured with a profile named `cloudspend`

\- AWS Cost Explorer enabled and available in the account

\- IAM permissions allowing `ce:GetCostAndUsage`



\## Setup



Install dependencies:



```bash

python -m pip install boto3 pytest

```



Configure AWS credentials securely using the AWS CLI:



```bash

aws configure --profile cloudspend

```



Use an IAM identity with only the permissions required for this project. Never commit credentials or paste secret keys into source code.



\## Run the report



```bash

python weekly\_report.py

```



The script fetches cost data from AWS and writes the report to `weekly\_report.json` in the project directory.



\## Run tests



```bash

python -m pytest -v

```



\## Understanding the output



The report contains:



\- Previous-period total

\- Current-period total

\- Total difference

\- Per-service costs

\- Percentage changes where calculable

\- A status indicating whether spending increased, decreased, stayed unchanged, or may need investigation



AWS cost data may be delayed or adjusted. Very small amounts can round to `$0.00`, and credits or billing adjustments can affect net results.



\## Security and cost considerations



\- Use restricted IAM permissions rather than root access keys.

\- Keep AWS credentials outside the repository.

\- Review AWS costs and billing alerts regularly.

\- Cost Explorer API usage may incur charges under AWS pricing.

\- Avoid publishing personal billing reports or account-specific information.



\## Current scope and future improvements



The current implementation focuses on cost retrieval, weekly comparison, and JSON reporting. Possible future improvements include scheduled reports, notifications for unusual increases, a dashboard, and infrastructure automation.



\## Learning goals



This project demonstrates AWS API integration, IAM least privilege, Python automation, JSON reporting, testing, and basic version control.

