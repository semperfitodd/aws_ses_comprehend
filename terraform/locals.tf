locals {
  domain = "brewsentry.com"

  environment = replace(var.environment, "_", "-")

  site_domain = "comprehend.${local.domain}"
}