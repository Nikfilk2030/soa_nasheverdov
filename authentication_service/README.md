```bash
# run
$ docker build -t auth . && docker run -p 5001:5000 auth

# curl
$ curl -X POST http://localhost:5001/register -H "Content-Type: application/json" -d '{"username":"johndoe","password":"example"}'
```
