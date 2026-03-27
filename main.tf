provider "aws" {
  region = "eu-west-2" 
}

# Step 1: Create VPC
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  enable_dns_support = true
  enable_dns_hostnames = true
}

# Step 2: Create Subnet in the VPC
resource "aws_subnet" "main" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.1.0/24"
  availability_zone = "ew-west-2a"  # Choose the availability zone that suits you
  map_public_ip_on_launch = true
}

# Step 3: Create an Internet Gateway and attach to VPC
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
}

# Step 4: Create Security Group for EC2 instance (SSH, HTTP, HTTPS)
resource "aws_security_group" "ec2_sg" {
  name        = "ec2_sg"
  description = "Allow inbound traffic for HTTP, HTTPS, and SSH"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Step 5: Create EC2 instance
resource "aws_instance" "main" {
  ami           = "ami-087c9ba923d9765d8"
  instance_type = "t2.nano"
  subnet_id     = aws_subnet.main.id
  vpc_security_group_ids = [aws_security_group.ec2_sg.id]
  key_name      = "TableOTD"
  user_data = file("${path.module}/startup.sh")

  tags = {
    Name = "prem-otd"
  }

  associate_public_ip_address = true
}

# Step 6: Allocate an Elastic IP (EIP)
resource "aws_eip" "main" {
  instance = aws_instance.main.id
}

output "public_ip" {
  value = aws_eip.main.public_ip
}
