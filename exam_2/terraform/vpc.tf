module "vpc"{
    source              = "terraform-aws-modules/vpc/aws"
    version             = "5.9.0"

    name                = "vpc-codev"
    cidr                = "10.0.0.0/16"
    azs                 = ["us-east-1a"]
    public_subnets      = ["10.0.0.0/24"]
    enable_nat_gateway  = false

    tags = {
        Terraform = true
        Environment = "codev"
    }
}

resource "aws_instance" "web"{
    depends_on                      = [ module.vpc, aws_security_group.web_sg ]
    ami                             = "ami-0a586f32a7db83393"
    instance_type                   = "t2.micro"
    associate_public_ip_address     = true
    subnet_id                       = "${element(module.vpc.public_subnets,0)}"
    security_groups                 = [aws_security_group.web_sg.id]
    ebs_block_device {
      device_name = "/dev/sda1"
      volume_size = 100
    }
    tags = {
        Name = "codev"
        Terraform = true
        Environment = "codev"
    }
}

resource "aws_security_group" "web_sg"{
    depends_on  = [ module.vpc ]
    name        = "web instance security group"
    description = "Allows port 443 access"
    vpc_id      =  module.vpc.vpc_id

    ingress  {
        from_port = 443
        to_port = 443
        protocol = "tcp"
        cidr_blocks= ["0.0.0.0/0"]
    }
    egress {
        from_port = 0
        to_port =0
        protocol = "-1"
        cidr_blocks= ["0.0.0.0/0"]
    }
    tags = {
       Terraform = true
        Environment = "codev"
    }
}

