#!/usr/bin/env python3

import json
import os
import subprocess
import sys


def exit_error(message: str) -> None:
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(1)


def run_cmd(argument_list: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        argument_list, encoding="utf-8", stderr=subprocess.PIPE, stdout=subprocess.PIPE
    )


def find_aws_cli() -> str:
    result = run_cmd(["which", "aws"])
    if result.returncode != 0:
        exit_error("unable to locate aws CLI")

    return result.stdout.rstrip()


def pass_args_list() -> list[str]:
    if len(sys.argv) <= 1:
        exit_error(
            "expecting arguments to be passed onto `aws sts assume-role` (e.g. --role-arn | --role-session-name)"
        )

    return sys.argv[1:]


def exec_assume_role(arg_list) -> dict[str, str]:
    result = run_cmd(["aws", "sts", "assume-role", "--output", "json"] + arg_list)
    if result.returncode != 0:
        exit_error(f"error executing `aws sts assume-role`\n\n===={result.stderr}====")

    # success - extract token details from JSON response
    response = json.loads(result.stdout)
    if "Credentials" not in response:
        exit_error("unexpected response from `aws sts assume-role`")

    response = response["Credentials"]

    return {
        "AWS_ACCESS_KEY_ID": str(response["AccessKeyId"]),
        "AWS_SECRET_ACCESS_KEY": str(response["SecretAccessKey"]),
        "AWS_SESSION_TOKEN": str(response["SessionToken"]),
    }


def main():
    # locate aws CLI command / args passed to script for `aws sts assume-role`
    aws_cli_path = find_aws_cli()
    pass_arg_list = pass_args_list()

    # obtain assumed role credentials
    credential_set = exec_assume_role(pass_arg_list)

    # export credentials
    print("unset " + " ".join(credential_set.keys()))
    for key, value in credential_set.items():
        print(f"export {key}={value}")

    default_region = os.environ.get("AWS_DEFAULT_REGION")
    if default_region is not None:
        print(f"export AWS_REGION={default_region}")


if __name__ == "__main__":
    main()
