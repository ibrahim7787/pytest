import pytest
import os
import boto3
from utils.log_setup import getLogger

logger = getLogger(__name__)
_NN_STAGE = os.getenv("NN_STAGE", 'dev')


def handle(event, context):

    job_id = event["CodePipeline.job"]['id'] if "CodePipeline.job" in event else None
    logger.info(f"Invoking lambda {os.getcwd()} job_id: {job_id}")
    exit_codes = {
        0: "TESTS PASSED",
        1: "TESTS FAILED",
        2: "USER INTERRUPTED",
        3: "INTERNAL ERROR",
        4: "COMMAND LINE ERROR",
        5: "NO TESTS COLLECTED",
    }
    tests_status = {}

    cloud_mode = os.getenv('CLOUD_MODE', False)
    options = []
    if 'browser' in event:
        browser = event['browser']
        options.append(f"-B {browser}")
    if 'site' in event:
        site = event['site']
        options.append(f"-S {site}")
    if 'app_url' in event:
        app_url = event['app_url']
        options.append(f"-A {app_url}")
    if 'tests' in event:
        tests_in_scope = event['tests']
    else:
        tests_in_scope = [
            "webapp/marketing/test_azure_poc.py",
        ]

    logger.info(f"Tests getting executed are: {tests_in_scope}, cloud mode: {cloud_mode}")

    for test_file in tests_in_scope:

        if options:
            t = [f"{test_file}"]
            t.extend(options)
            logger.info(f"T: {t}")
            result = pytest.main(t)
        else:
            result = pytest.main([f"{test_file}"])

        logger.info(f"Result = {exit_codes[result]}")

        if result != 0:
            logger.info(f"Systests {test_file}: {exit_codes[result]}")
            # logger.info(f"FAILURE_STATUS = {os.getenv('FAILURE_STATUS')}")
            tests_status[test_file] = f"{exit_codes[result]} Reason: {os.getenv('FAILURE_STATUS')}"
        else:
            tests_status[test_file] = 'succeeded'

    status = list(set(tests_status.values()))

    if len(status) > 1 or status[0] != 'succeeded':
        logger.info("Sending email")
        body = ""
        for test, message in tests_status.items():
            message = message.replace('\n', '<br/>')
            body += f"<div>{test}</div><div>{message}</div><br/>"
        logger.info(body)

    if job_id:
        region_name = "us-west-2"

        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.put_job_failure_result

        client = boto3.client(service_name="codepipeline", region_name=region_name)
        logger.info(tests_status)
        if len(status) == 1 and status[0] == 'succeeded':
            response = client.put_job_success_result(jobId=job_id)
        else:
            response = client.put_job_failure_result(
                jobId=job_id,
                failureDetails={
                    'type': 'JobFailed',
                    'message': f"{tests_status}",
                    'externalExecutionId': context.aws_request_id,
                },
            )

        logger.info(f"CodePipeline response: {response}")

        lfn = logger.info if len(status) == 1 and status[0] == 'succeeded' else logger.error
        lfn(f"Systests {tests_status} on job {job_id}")


if __name__ == "__main__":
    # handle({'tests': ["test_1a_interview_steps.py"]}, {})
    handle(
        {
            "tests": [
                "webapp/marketing/test_azure_poc.py",
            ]
        },
        {},
    )
