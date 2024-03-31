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
  -d '{"username":"johndoe","password":"example","firstName":"John","lastName":"Doe","dob":"1990-01-01","email":"john.doe@example.com","phoneNumber":"123-456-7890"}'

# test /auth
$ curl -X POST http://localhost:5001/auth \
  -H "Content-Type: application/json" \
  -d '{"username":"johndoe","password":"example"}'

# test /update_user
$ curl -X PUT http://localhost:5001/update_user \
  -H "Authorization: Basic $(echo -n "johndoe:example" | base64)" \
  -H "Content-Type: application/json" \
  -d '{"firstName":"NewFirstName","lastName":"NewLastName","dob":"2000-01-02","email":"new.email@example.com","phoneNumber":"9876543210"}'

# test /create_task
$ curl -X POST http://localhost:5001/create_task \
  -H "Content-Type: application/json" \
  -d '{"username":"johndoe","password":"example","content": "my task content"}'

```
