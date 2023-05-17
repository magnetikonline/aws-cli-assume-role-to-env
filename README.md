# AWS CLI `assume role` to env

Quick and dirty Python utility for transferring the output of [`aws sts assume-role`](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/sts/assume-role.html) to a set of environment variable `export` commands.

Whilst Python based, does not require `boto` - calls the `aws` CLI command directly and parses returned JSON token payload.

## Usage

```sh
./aws-cli-assume-role-to-env.py \
  --role-arn arn:aws:iam::... \
  --role-session-name ROLE_NAME

# output follows
unset AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_SESSION_TOKEN
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
export AWS_SESSION_TOKEN=...
export AWS_REGION=...
```

or alternatively:

```sh
$(./aws-cli-assume-role-to-env.py \
  --role-arn arn:aws:iam::... \
  --role-session-name ROLE_NAME
)
```
