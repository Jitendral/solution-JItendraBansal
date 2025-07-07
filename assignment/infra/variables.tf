variable "instance_type" {
  default = "t3.micro"
}

variable "key_name" {
  description = "demo-user"
  type        = string
}

variable "project_name" {
  default = "devops-project"
}