data "archive_file" "frontend" {
  source_file = "${path.module}/frontend/frontend.py"
  output_path = "${path.module}/frontend/frontend.zip"
  type        = "zip"
}

data "aws_iam_policy_document" "frontend_lambda_policy" {
  statement {
    actions   = ["dynamodb:*"]
    effect    = "Allow"
    resources = [module.dynamodb_table.dynamodb_table_arn]
  }
}

resource "aws_iam_policy" "frontend_lambda_policy" {
  name   = "${var.environment}_frontend_lambda_policy"
  policy = data.aws_iam_policy_document.frontend_lambda_policy.json

  tags = var.tags
}

resource "aws_iam_role" "frontend_lambda_execution_role" {
  name = "${var.environment}_frontend_lambda_execution_role"

  assume_role_policy = data.aws_iam_policy_document.lambda_execution_role.json

  tags = var.tags
}

resource "aws_iam_role_policy_attachment" "frontend_lambda_execution_policy" {
  policy_arn = data.aws_iam_policy.AWSLambdaBasicExecutionRole.arn
  role       = aws_iam_role.frontend_lambda_execution_role.name
}

resource "aws_iam_role_policy_attachment" "frontend_lambda_policy" {
  role       = aws_iam_role.frontend_lambda_execution_role.name
  policy_arn = aws_iam_policy.frontend_lambda_policy.arn
}

resource "aws_lambda_function" "frontend" {
  filename      = data.archive_file.frontend.output_path
  description   = "Display results of AWS Comprehend from DynamoDB"
  function_name = "${var.environment}_frontend"
  role          = aws_iam_role.frontend_lambda_execution_role.arn
  handler       = "frontend.lambda_handler"
  runtime       = "python3.9"
  timeout       = 30

  environment {
    variables = {
      ENVIRONMENT = var.environment
    }
  }

  source_code_hash = data.archive_file.frontend.output_base64sha256

  tags = var.tags
}

resource "null_resource" "react_app" {
  provisioner "local-exec" {
    command     = <<EOT
      cd ./files &&
      npx create-react-app email-visualizer &&
      cp ./App.js ./email-visualizer/src/App.js &&
      cp ./favicon.png ./email-visualizer/public/favicon.png &&
      cp ./index.html ./email-visualizer/public/index.html &&
      cd email-visualizer &&
      npm install react-chartjs-2 chart.js axios &&
      npm run build
    EOT
    interpreter = ["/bin/sh", "-c"]
  }
}
