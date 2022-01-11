# Python Challenge

## Connected Developers API
In this challenge you will have to create a REST API which will return whether two 
_developers_ are fully connected or not. Given a pair of developer handles they are 
considered connected if:

* They follow each other on Twitter.
* They have at least a Github organization in common.

Assume that people having the same handle, both in Twitter and Github, are actually 
the same person.

_Disclaimer:_ We expect the implementation to query the official 
[Twitter](https://developer.twitter.com/en/docs) and 
[Github](https://docs.github.com/en/rest) APIs, and it's OK to use the existing 
client libraries!

## How it works?

You have to implement a Python REST API with these 2 endpoints. 
You could find the whole description of the API in the [OpenAPI description file](/api.definition.yaml)

#### Realtime Endpoint 

```bash
GET /connected/realtime/dev1/dev2
```

This endpoint should return if the developers are connected and what GitHub 
organizations have they in common.

#### Register Endpoint

Besides that, we are interested in the different statuses a pair of developers had 
in previous invocations of the real-time endpoint.

```bash
GET /connected/register/dev1/dev2
```

This endpoint should return all the related information from the previous requests to
the real-time endpoint, including the date it was registered.

## Technical requirements

* We expect you to use **Python 3** to solve the challenge
* Create a **clean**, **maintainable** and **well-designed** code
* **Test** your code until you are comfortable with it

To understand how you take decisions during the implementation, please write a README 
file explaining some of the most important parts of the application.

### What is going to take into account  
 
Have a functional API is important, but not the most! We expect to see some other
things that are just as important:

* The use of linters, type-hinting and some good practices around the language
* Have in mind the problems of scaling the API (database, non-blocking I/O, threads, etc...)
* Containerization of the API. Easiness to install & run

## End to end tests

To ensure that everything is working as expected, you could execute the e2e test suite, 
where you could find some request to your API. 

Those tests are created with [Cypress](https://www.cypress.io/) and are based on the
OpenAPI specification file.

To execute them just place inside [e2e-test](./e2e-test) folder:

```bash
npm install
npm run e2e
```

