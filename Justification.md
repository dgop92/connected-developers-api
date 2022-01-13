# Connected Developers API

## Framework

The framework that I chose for building the API was Django with the rest framework, and the main reason is Django is the one that I know the most. I'm aware that Django is not the best technology to solve this problem, one of the reasons is that Django is synchronous by default, and implementing asynchronous code is more complicated than in other libraries such as FastAPI.

## Scaling

We are doing I/O tasks (Twitter and Github APIs) for the real-time endpoint so making an asynchronous API will suit this problem if the API scales

The database I chose is the standard in Django, sqlite3 for development, and PostgreSQL for production. If we think beyond the challenge, the DB may handle more relationships because we are analyzing the connection between developers. Another option that I was thinking of was MongoDB, for building the API faster and with a flexible schema but is not easy to integrate with Django

## Logic

Working with the external APIs is something that may change, so I implemented the logic using the strategy pattern

What may change?

* Using the client library for GitHub
* Reading all the organization of the GitHub account
* Improving the logic of the "is following" method, when Twitter API v2 friendship/show endpoint

_Note: I don't have access to the elevated plan in the Twitter API_
_Note: I couldn't pass all tests due to limit rate of 15 in Twitter API_
