# skritter

*skritter* is a client for the Skritter API.

Currently a work in progress, with limited API support.

Documentation:
[http://www.skritter.com/api/v0/docs](http://www.skritter.com/api/v0/docs)


## Basic Usage

Create a session object and authenticate.

```python
>>> import skritter
>>> session = skritter.session(OAUTH_CLIENT_NAME, OAUTH_CLIENT_SECRET)
>>> session.login('username', 'password')

```

Get a list of vocabulary lists.

```python
>>> vocablists = skritter.get_vocablists(session)

```

## Example client

Takes a list of Chinese words, and creates or updates a Skritter list for
study.

```shell
$ export SKRITTER_OAUTH_CLIENT_NAME='<client name>'
$ export SKRITTER_OAUTH_CLIENT_SECRET='<client secret>'
$ export SKRITTER_USER='<username>''
$ export SKRITTER_PASSWORD='<password>'
$ python example/client.py 'List title' exmaple/sample.csv
```
