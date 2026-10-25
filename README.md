# CloudSpend Sentinel

A serverless AWS cost-monitoring project that generates weekly spending reports, compares costs across AWS services, and stores reports securely in Amazon S3.

## 🎯 Project Goal

CloudSpend Sentinel helps AWS users understand where their cloud spending comes from and identify changes in costs before they become unexpected expenses.

## 🏗️ Architecture

```text
AWS Cost Explorer
       |
       v
AWS Lambda (Python)
       |
       +----> Compare previous and current 7-day costs
       |
       v
Private Amazon S3 Bucket
       |
       v
Weekly JSON Cost Report

Amazon EventBridge Scheduler
       |
       +----> Invokes Lambda every Monday at 9:30 AM IST

Public Demo Dashboard
       |
       +----> Displays fictional sample data only
```

## 🛠️ AWS Services Used

- **AWS Cost Explorer:** Retrieves cost data grouped by AWS service.
- **AWS Lambda:** Runs Python code to generate weekly cost reports without managing servers.
- **Amazon EventBridge Scheduler:** Automatically invokes the Lambda function every Monday.
- **Amazon S3:** Stores generated JSON reports in a private bucket.
- **AWS IAM:** Grants the Lambda execution role only the permissions needed for Cost Explorer, S3 report uploads, and logging.
- **Amazon CloudWatch Logs:** Captures Lambda execution logs for troubleshooting.

## ⚙️ How It Works

1. EventBridge Scheduler triggers the Lambda function every Monday at 9:30 AM IST.
2. Lambda requests AWS spending data from Cost Explorer.
3. The function compares two consecutive, completed seven-day periods.
4. Costs are grouped by AWS service.
5. The report includes previous cost, current cost, and the difference.
6. Lambda saves the JSON report to a private S3 bucket.
7. CloudWatch Logs records execution details to help diagnose errors.

## 📊 Example Report

The following is an illustrative example, not actual billing data.

```json
{
  "currency": "USD",
  "previous_total_usd": 3.50,
  "current_total_usd": 5.80,
  "change_usd": 2.30,
  "services": [
    {
      "service": "Amazon EC2",
      "previous_cost_usd": 2.00,
      "current_cost_usd": 3.50,
      "change_usd": 1.50
    }
  ]
}
```

## 🔐 Security

- Real billing reports are stored in a private S3 bucket.
- S3 public access blocking remains enabled for the private reports bucket.
- IAM permissions are scoped to the required operations.
- The public dashboard uses fictional sample data only.
- AWS credentials are not included in the source code.
- The Lambda function uses its IAM execution role instead of locally stored access keys.

## 🖥️ Demo Dashboard

The dashboard is hosted as a static website on Amazon S3 and displays fictional sample spending data.

**Important:** The demo dashboard is separate from the real reports. It does not expose actual account billing data.

## 🧪 Testing

The project includes Python unit tests for the local reporting script.

The Lambda function was also tested in AWS, and a generated JSON report was verified in the private S3 bucket.

## 💡 What I Learned

- Using Boto3 to interact with AWS services.
- Retrieving AWS billing data with Cost Explorer.
- Building serverless automation with AWS Lambda.
- Scheduling recurring tasks with EventBridge.
- Storing reports securely in S3.
- Applying IAM permissions and separating public demo data from private billing data.
- Comparing costs across time periods using Python.

## 🚀 Future Improvements

- Send weekly email reports using Amazon SNS.
- Add budget threshold alerts.
- Show trends and service-level cost increases in the dashboard.
- Add automated deployment and testing through GitHub Actions.
- Add stronger monitoring and error notifications.

## 💰 Cost Considerations

This project uses serverless services, but AWS charges may apply depending on usage, API requests, storage, logging, and account eligibility for free usage allowances. Review AWS Billing regularly and remove unused resources when the project is no longer needed.

## 👤 Author

Built as a hands-on AWS, Python, and cloud-cost-monitoring portfolio project.
