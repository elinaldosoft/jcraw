Modo Development
-------------------
- `virtualenv venv -p $(which python3.6)`
- `source venv/bin/activate`
- `pip3 install -r requirements/dev.txt`
- `honcho start`

Example
-------------------
#### Send process to QUEUE
```
curl -X POST "http://127.0.0.1:5000/api/v1/proccesses/tjal" -H "accept: application/json" -H "Content-Type: application/json" -d "{ \"number\": \"0704975-39.2013.8.02.0001\"}"
{
  "message": "Dentro de alguns minutos seu processo estará disponível para acompanhamento",
  "url": "api/v1/proccesses/0704975-39.2013.8.02.0001",
  "status": "in_queue",
  "task": "4341352e-b18d-4643-903a-33b3d0c13cc6"
}
```

#### Search Process
```
curl -X GET "http://127.0.0.1:5000/api/v1/proccesses/0704975-39.2013.8.02.0001" -H "accept: application/json"
```
 
Modo Production with Docker
-------------------
#### Creating Build
- `docker-compose build`

#### Starting Services
- `docker-compose up -d`

#### Project url
- `http://localhost:5000`

### Documentation
- `http://localhost:5000/api/v1`

Some processes
----------------------
- 0710802-55.2018.8.02.0001 - TJAL
- 0732215-27.2018.8.02.0001 - TJAL
- 0725882-59.2018.8.02.0001 - TJAL
- 0715677-39.2016.8.02.0001 - TJAL
- 0713230-44.2017.8.02.0001 - TJAL
- 0729987-16.2017.8.02.0001 - TJAL
- 0704975-39.2013.8.02.0001 - TJAL
- 0704975-39.2013.8.02.0001 - TJAL
- 0500039-79.2018.8.02.0000 - TJAL 2 Grau

- 1412535-05.2019.8.12.0000 - TJMS 2 Grau
- 0821901-51.2018.8.12.0001 - TJMS