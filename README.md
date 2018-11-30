# mlgia-prediction-service

Do the prediction to the posibility to park in a public park in Malaga, for a specific moment.

## STARTING
This service works in Python 3.6, and start in the port 8084

```
$ pip install requirements.txt

$ python service.py
```

## Dockerizer
$ docker build -t mlgia/mlgia-prediction-service .

## HOW IT IS WORKS
This is a REST service wich return a prediction, 0 = there are a posibility to park, or 1 = there are no posibility to park.
The data received is:
> idParking = The id of the parkig

> date = The date to take the prediction

> time = The hour to take the prediction

The service take this values, and calculate if is a working day, to resolve the prediction.
  
