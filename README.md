## Requirements

To run locally you will need [docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/) and [docker-compose](https://docs.docker.com/compose/install/). That's it, just it.

## Documentation

You can access the API documentation acessing the API Url (local: http://localhost:5000).

## How to test locally

I suggest using Python's Virtualenv (https://virtualenv.pypa.io/en/latest/) before doing this steps.

```sh
cd path/to/repo/

# For local development
make start-local

```

or if you prefer docker:

```sh
cd path/to/repo/

# Build development containers
make build

# Run all tests
make test

# Up container
make up

```

## F.A.Q.

### - What was the stack used?
Flask, MySQL, Docker, SqlAlchemy... Etc etc etc.

### - There something missing?
Yes, I never really used Flask before and I had to learn many things. Guess if I need to point my biggest mistake, would be "I wanted to have many things that I already used, like migrations, etc."

So... Whats missing?

- Front end. Entire of it. If you want to see my frontend skills I would recommend these repositories: [My personal website](https://github.com/kuresto/kuresto.github.io) and [Another code challenge I did a while ago]([https://docs.docker.com/install/linux/docker-ce/ubuntu/](https://github.com/kuresto/geekhunter_code_challenge_front))
- Much of swagger documentation
- Production docker containers.
- SSL Certicate.
- Some modules were really rushed.
- Docker development server sometimes resets connection. Don't know why yet.

I would be glad if I were given the chance to explain all of the project and its missing features.

### - What is the test coverage %?
About 94%.

### - WTF This upload?
I know, it's bad.

### - Something you didn't like about this project?
See "There something missing?"
