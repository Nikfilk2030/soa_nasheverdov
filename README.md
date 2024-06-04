# Шевердов Никита Андреевич, БПМИ215

## Venv

```bash
python3 -m venv venv && source venv/bin/activate
```

## Auth service

Examples, to test service with commands

```bash
# run
$ docker-compose up --build

# test /register
$ curl -X POST http://localhost:5001/register \
  -H "Content-Type: application/json" \
  -d '{"username":"oleg","password":"tink","firstName":"John","lastName":"Doe","dob":"1990-01-01","email":"john.doe@tink.com","phoneNumber":"123-456-7890"}'

# test /auth
$ curl -X POST http://localhost:5001/auth \
  -H "Content-Type: application/json" \
  -d '{"username":"oleg","password":"tink"}'

# test /update_user
$ curl -X PUT http://localhost:5001/update_user \
  -H "Authorization: Basic $(echo -n "oleg:tink" | base64)" \
  -H "Content-Type: application/json" \
  -d '{"firstName":"NewFirstName","lastName":"NewLastName","dob":"2000-01-02","email":"new.email@tink.com","phoneNumber":"9876543210"}'

# test /create_task
$ curl -X POST http://localhost:5001/create_task \
  -H "Content-Type: application/json" \
  -d '{"username":"oleg","password":"tink","content": "Tinkoff"}'

# test /update_task
$ curl -X POST http://localhost:5001/update_task \
  -H "Content-Type: application/json" \
  -d '{"username":"oleg","password":"tink","task_id": 1,"content": "Yandex"}'

# test /delete_task
$ curl -X POST http://localhost:5001/delete_task \
  -H "Content-Type: application/json" \
  -d '{"username":"oleg","password":"tink","task_id": 1}'
  
# test /get_task_by_id
$ curl -X GET http://localhost:5001/get_task_by_id \
   -H "Content-Type: application/json" \
   -d '{"username":"oleg","password":"tink","task_id": 2}'
   
# test /get_tasks
$ curl -X GET http://localhost:5001/get_tasks \
  -H "Content-Type: application/json" \
  -d '{"username":"oleg","password":"tink","page_number":"1","page_size":"10"}'
```
