data "aws_route53_zone" "main" {
  name         = "wjmb.click"
  private_zone = false
}

resource "aws_route53_record" "www" {
  zone_id = data.aws_route53_zone.main.zone_id
  name    = "prem-otd.wjmb.click"
  type    = "A"
  ttl     = 300
  records = [aws_eip.main.public_ip]
}