# Use default VPC
data "aws_vpc" "default" {
  default = true
}

# Find an available public subnet in the default VPC
data "aws_subnet_ids" "default" {
  vpc_id = data.aws_vpc.default.id
}

# Use the first available subnet
data "aws_subnet" "default" {
  id = data.aws_subnet_ids.default.ids[0]
}

# Create a security group in default VPC
resource "aws_security_group" "ec2_sg" {
  name        = "ec2_sg"
  description = "Allow SSH, HTTP, MinIO (9000), and frontend (3000)"
  vpc_id      = data.aws_vpc.default.id

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
    from_port   = 9000
    to_port     = 9000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = 3000
    to_port     = 3000
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

# EC2 instance using default subnet + security group
resource "aws_instance" "demo-user" {
  ami                    = "ami-0f918f7e67a3323f0" # Ubuntu 20.04 (ap-south-1)
  instance_type          = var.instance_type
  subnet_id              = data.aws_subnet.default.id
  vpc_security_group_ids = [aws_security_group.ec2_sg.id]
  key_name               = var.key_name

  tags = {
    Name = "${var.project_name}-instance"
  }

  user_data = file("${path.module}/userdata.sh")
}
