# aws-ec2-spot-events
Simulate Spot Interruption leveraging Fault Injection Simulator

## Start Scenario
'''
aws fis start-experiment --experiment-template-id ABCDE1fgHIJkLmNop
'''

## Install Metadata Mock
'''
brew tap aws/tap
brew install ec2-metadata-mock
'''
Ref: https://github.com/aws/amazon-ec2-metadata-mock?tab=readme-ov-file#installation

## Placement Score

aws ec2 get-spot-placement-scores --region eu-west-1 --generate-cli-skeleton input > attributes.json

aws ec2 get-spot-placement-scores --region eu-west-1 --cli-input-json file://attributes.json

