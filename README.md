# Arithmetic Calculator API

This repository contains the backend code for an arithmetic calculator webapp. It is built using AWS Lambda, Python, DynamoDB, and the Serverless framework. This webapp allows users to register, log in, perform arithmetic operations, and retrieve their records.

## Usage

### Deployment

```
$ serverless deploy
```

### Invocation

After successful deployment, you can call the created application via HTTP:

```bash
curl https://xxxxxxx.execute-api.us-east-1.amazonaws.com/
```

### Bundling dependencies

In case you would like to include 3rd party dependencies, you will need to use a plugin called `serverless-python-requirements`. You can set it up by running the following command:

```bash
serverless plugin install -n serverless-python-requirements
```

Running the above will automatically add `serverless-python-requirements` to `plugins` section in your `serverless.yml` file and add it as a `devDependency` to `package.json` file. The `package.json` file will be automatically created if it doesn't exist beforehand. Now you will be able to add your dependencies to `requirements.txt` file (`Pipfile` and `pyproject.toml` is also supported but requires additional configuration) and they will be automatically injected to Lambda package during build process. For more details about the plugin's configuration, please refer to [official documentation](https://github.com/UnitedIncome/serverless-python-requirements).

## API Specification

#### Register

    URL: https://sbhnbx5vf7.execute-api.us-east-1.amazonaws.com/register
    Method: POST
Request example:
```json
{
    "username": "andreizq",
    "password": "andre",
    "balance": 50
}
```
Response example:
```json
{
    "username": "andreizq",
    "balance": 50
}
```

#### Login

    URL: https://sbhnbx5vf7.execute-api.us-east-1.amazonaws.com/login
    Method: POST
Request example:
```json
{
    "username": "andreizq",
    "password": "andre"
}
```
Response example:
```json
{
    "username": "andreizq",
    "balance": "50",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFuZHJlaXpxIn0.czpuDzFotVHX-Rv1plbLLWZ2E-sawVQPHkfDZvXk5hU"
}
```

#### Perform Operation

    URL: https://sbhnbx5vf7.execute-api.us-east-1.amazonaws.com/records
    Method: POST
    Auth: Bearer token
Request example:
```json
{
    "operation": "add",
    "value1": 18,
    "value2": 4
}
```
Response example:
```json
{
    "user_id": "andreizq",
    "user_balance": "0",
    "cost": "1",
    "date": "1683078525",
    "timestamp": "2023-05-03 01:48:45.399660",
    "operation_id": "add",
    "id": "f55ced03-b17a-406a-8a6c-4c1eb7e2c570",
    "operation_response": "22"
}
```

#### User Records

    URL: https://sbhnbx5vf7.execute-api.us-east-1.amazonaws.com/records
    Method: GET
    Auth: Bearer token
Success Response:
```json
[{
    "user_id": "andreizq",
    "user_balance": "1",
    "cost": "5",
    "date": "1683074619",
    "timestamp": "2023-05-03 00:43:39.466095",
    "operation_id": "rndstr",
    "id": "fe19b11f-6974-4aa8-8141-1420707c4090",
    "operation_response": "Yjt2gERoX4m85qbUCFn"
},
{
    "user_id": "andreizq",
    "user_balance": "6",
    "cost": "5",
    "date": "1683074618",
    "timestamp": "2023-05-03 00:43:38.164334",
    "operation_id": "rndstr",
    "id": "df34d7ea-52f2-4995-97f8-06adedb7e951",
    "operation_response": "sr3d1DzTyrFbznDachn"
}]
```

#### Delete Record

    URL: https://sbhnbx5vf7.execute-api.us-east-1.amazonaws.com/records/{id}
    Method: DELETE
    Auth: Bearer token
Success Response:
```json
true
```

#### Generic error message
```json
{"message": "error message"}
```