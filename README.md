# codev
## Exam-1 
Notes: I've used (Virtualbox) Linux Ubuntu server to configure and install NGINX
run the command below in exam_1 directory 

$:> ansible-playbook webserver-playbook.yaml -i inventory.cfg 

## Exam-2
Notes: 
1. I've not included the S3 Bucket as statefile storage
2. I've not included the dynamodb table for statefile lock

## Exam-3
Notes: 
1. Please change the variable ACCOUNT_NUMBER in main.py and provide your AWS account number. this will be needed to construct the ARN of SNS Topic
