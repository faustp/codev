# codev
## Exam-1 
> [!NOTE]
> I've used Amazon Linux 2023 server to configure and install NGINX
run the command below in exam_1 directory 

```$> ansible-playbook webserver-playbook.yaml -i inventory.cfg ```

```$> curl test.com ```

## Exam-2
> [!NOTE]
> 1. I've not included the S3 Bucket as statefile storage
> 2. I've not included the dynamodb table for statefile lock

## Exam-3
> [!NOTE]
> 1. Please install the boto3 python module 
> 2. Please change the variable ACCOUNT_NUMBER in main.py (line 8) and provide your AWS account number. this will be needed to construct the ARN of SNS Topic
``` python
8  ACCOUNT_NUMBER: Final = "123456789"
```
