data "archive_file" "this" {
  source_file = "${path.module}/app/app.py"
  output_path = "${path.module}/app/app.zip"
  type        = "zip"
}

data "aws_iam_policy" "AWSLambdaBasicExecutionRole" {
  name = "AWSLambdaBasicExecutionRole"
}

data "aws_iam_policy_document" "lambda_execution_role" {
  statement {
    actions = ["sts:AssumeRole"]
    effect  = "Allow"
    principals {
      identifiers = ["lambda.amazonaws.com"]
      type        = "Service"
    }
  }
}

data "aws_iam_policy_document" "lambda_policy" {
  statement {
    actions   = ["dynamodb:*"]
    effect    = "Allow"
    resources = [module.dynamodb_table.dynamodb_table_arn]
  }
  statement {
    actions   = ["comprehend:*"]
    effect    = "Allow"
    resources = ["*"]
  }
}

resource "aws_iam_policy" "lambda_policy" {
  name   = "${var.environment}_lambda_policy"
  policy = data.aws_iam_policy_document.lambda_policy.json

  tags = var.tags
}

resource "aws_iam_role" "lambda_execution_role" {
  name = "${var.environment}_lambda_execution_role"

  assume_role_policy = data.aws_iam_policy_document.lambda_execution_role.json

  tags = var.tags
}

resource "aws_iam_role_policy_attachment" "lambda_execution_policy" {
  policy_arn = data.aws_iam_policy.AWSLambdaBasicExecutionRole.arn
  role       = aws_iam_role.lambda_execution_role.name
}

resource "aws_iam_role_policy_attachment" "lambda_policy" {
  role       = aws_iam_role.lambda_execution_role.name
  policy_arn = aws_iam_policy.lambda_policy.arn
}

resource "aws_lambda_function" "this" {
  filename      = data.archive_file.this.output_path
  description   = "Use AWS Comprehend and store results in DynamoDB"
  function_name = var.environment
  role          = aws_iam_role.lambda_execution_role.arn
  handler       = "app.lambda_handler"
  runtime       = "python3.9"
  timeout       = 30

  environment {
    variables = {
      ENVIRONMENT = var.environment
    }
  }

  source_code_hash = data.archive_file.this.output_base64sha256

  tags = var.tags
}