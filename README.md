# FiscalNote DevOps Technical Assessment

## Payment System

This repository contains a simple payment system for users to send money to each other.
It supports the following functionality:
```
GET     /api/entity       return list of system users     params: n/a
POST    /api/entity       create new user                 params: username:required, password:required, initial_balance:optional
POST    /api/transaction  submit transaction              params: amount:required, sender:required, recipient:required
```

The application uses a postgres database as a datastore. The connection information can be seen or updated in `__init__.py`

### Tasks

Finish and "productionize" the application in this repository. 

1. Containerize the application: add a Dockerfile.
   Recommend doing this first to simplify task 2.
2. Get the application up and running.
3. Verify the application meets the requirements in [Considerations](#considerations), and make any changes necessary. 
4. Complete the `/api/entity/<entityid>/transactions` endpoint functionality. 
   This should return the complete list of transactions for the requested user.
5. Add functionality, through a new endpoint or existing one, to deposit more money to an account.
   It would be reasonable for a deposit to be a type of transaction.
6. Create an EKS cluster in the given AWS account and add the necessary configuration to deploy this application to EKS.
7. Deploy the application to EKS and provide verification that it works in your PR.

#### Considerations

- The implementation should not allow users to send money to themselves.
- The implementation should not allow users to send more money than they have in their balance.

### Considerations you can ignore

- There's no authn/authz here to reason about or implement.
- Error handling minutiae: assume requests are well-formed but functionality should not be abused or handled incorrectly. 

## Submission

* Fork this repository to your own github account
* Create a branch off of master and use this for all changes
* Once you are finished, open a pull request to this repo; keep in mind your PR itself will be taken into consideration.
* Inform the interviewer that you have completed the task
* Your submission will be reviewed. 

## Setting up Running the API

The application can be run directly (below). 
It is recommended to complete task 1 to avoid possible dependency installation issues.
```
$> pip install -r requirements.txt
$> python run.py
```
**Creating users, with or without a balance**
```
$> curl -d '{"userid": "fiscalnote", "password": "payme"}' -H "Content-Type: application/json" -X POST localhost:8080/api/entity
{
  "balance": 0,
  "id": "fiscalnote",
  "password": "payme"
}

$> curl -d '{"userid": "tyler", "password": "relyr", "initial_balance": 50}' -H "Content-Type: application/json" -X POST localhost:8080/api/entity
{
  "balance": 50,
  "id": "tyler",
  "password": "relyr"
}
```
**Get list of current users**
```
$> curl -XGET http://localhost:8080/api/entity
[
  {
    "balance": 0,
    "id": "fiscalnote",
    "password": "payme"
  },
  {
    "balance": 50,
    "id": "tyler",
    "password": "relyr"
  }
]
```
**Submit a transaction**
```
$> curl -XPOST -H "Content-Type: application/json" -d '{"amount": 10, "sender": "tyler", "recipient": "fiscalnote"}' http://localhost:8080/api/transaction
{
  "success": true
}
```
