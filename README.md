# ecs-task-deployment-verifier

This is a piece of python script that will wait for the latest version of a task definition family to be fully deployed in an AWS ECS cluster. Useful in pipelines to see if a deployment really went up correctly. Requires boto3.

Simply run with:
```
python ecs-task-deployment-verifier.py [region] [cluster] [family]
```

The script will fetch the latest version of the task-definition, and wait until that version is the only one running in the cluster. If it takes longer than 10 minutes to deploy, it will fail.