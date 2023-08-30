# AWS Feedback Sentiment Analysis Dashboard

This project provides a dashboard to display the sentiment and top phrases from feedback emails. The backend is built using Amazon SES, SNS, Lambda, AWS Comprehend, and DynamoDB. The frontend is a React.js app hosted in an S3 bucket and distributed via CloudFront.

![aws_ses_comprehend.png](images%2Faws_ses_comprehend.png)

![dashboard.png](images%2Fdashboard.png)

## Prerequisites

- AWS account with appropriate permissions
- Terraform v1.15+ installed
- Python 3.9 installed
- AWS CLI configured with AWS credentials

## Directory Structure

- `terraform/` - Contains all Terraform scripts to set up AWS resources
- `python/` - Contains Python script to send test emails to the generated feedback address

## Setup

### Backend Setup (Terraform)

1. Navigate to the `terraform/` directory.

    ```bash
    cd terraform
    ```

2. Run Terraform init to initialize the working directory.

    ```bash
    terraform init
    ```

3. Run Terraform plan to generate an execution plan.

    ```bash
    terraform plan -out=plan.out
    ```

4. Apply the changes specified by the plan.

    **Note**: You'll have to run this command twice due to the use of `local-exec` for building and deploying the React app.

    ```bash
    terraform apply plan.out
    ```

### Frontend Setup (React App)

The React app will be automatically built and uploaded to S3 via the `local-exec` provisioner in Terraform.

Make sure to update the App.js file with the API_GATEWAY_INVOKE_URL environment variable.

### Test Email Setup (Python)

1. Navigate to the `python/` directory.

    ```bash
    cd python
    ```

2. Update the `send_emails.py` script with the newly created feedback address.

    ```python
    def send_email(subject, body):
        from_email = "<FROM@EMAIL.COM>"
        to_email = "<TO@EMAIL.COM>"
        password = "<APP_PASSWORD>"
    ```

3. Run the `send_emails.py` script to send test emails to the newly created feedback address.

    ```bash
    python send_emails.py
    ```

## Using the Dashboard

Once all resources are deployed and the test emails are sent, you can access the dashboard through the CloudFront URL to view the sentiment and top phrases from the feedback emails.

## Cleaning Up

To remove all deployed resources, navigate back to the `terraform/` directory and run:

```bash
terraform destroy
```
This will remove all AWS resources created by this project.