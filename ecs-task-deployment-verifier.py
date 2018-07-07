import boto3
import sys
import time

region = sys.argv[1]
cluster = sys.argv[2]
family = sys.argv[3]

print('Region = ' + region)
print('Cluster = ' + cluster)
print('Family = ' + family)

ecs = boto3.client(service_name='ecs', region_name=region)


def get_latest_registered_task_def_arn():
    return ecs.list_task_definitions(familyPrefix=family, sort='DESC')['taskDefinitionArns'][0]


def running_task_def_arns_matches_expected_arn(expected_task_definition_arn):
    current_tasks = ecs.list_tasks(cluster=cluster, family=family)
    current_task_definitions = ecs.describe_tasks(cluster=cluster, tasks=current_tasks['taskArns'])

    # Verify that ONLY the latest version is running, i.e. that the new version is stable and the old ones have been drained.
    for task_definition in current_task_definitions['tasks']:
        if task_definition['taskDefinitionArn'] != expected_task_definition_arn:
            print('Found unwanted task definition still running: ' + task_definition['taskDefinitionArn'])
            return False

    return True


expected_task_def_arn = get_latest_registered_task_def_arn()

print('Latest task definition registered: ' + expected_task_def_arn)

end_time_limit = time.time() + 60 * 10
while not running_task_def_arns_matches_expected_arn(expected_task_def_arn):
    if time.time() > end_time_limit:
        sys.exit('The service has not been deployed correctly')

    print('Waiting for service to deploy...')
    time.sleep(15)

print('Latest service version is now fully deployed')