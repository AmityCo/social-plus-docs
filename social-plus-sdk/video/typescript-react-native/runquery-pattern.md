# RunQuery Pattern

Every action inside of ts-sdk can be wrapped by `runQuery` to enable offline first functionality.

## **Getter**

For a getter, `runQuery` will first try to get the data from cache. If the data already exists in the cache, it will not fetch from the server. Otherwise, it will fetch the data and store the cache accordingly.

{% embed url="https://gist.github.com/100a5cdb39d795c86422a2bfc670d96e" %}

You can set the period of validity of the cache manually using the third parameter. With this example, the cache will be considered valid for an hour.

{% embed url="https://gist.github.com/fe8fe8b70312376ba518de22492487f6" %}

### Flow Diagram

![](<../../../.gitbook/assets/image (25).png>)

## **Mutator**

For a mutator, `runQuery` will do an optimistic mutation (creation, update, delete operation) to the cache before making a request to the server.

{% embed url="https://gist.github.com/13eca214fd3723658b3bf7a6175e99d0" %}

## **Pagination**

The `runQuery` for an action that requires pagination acts a little differently. Instead of accepting a callback that passes just the object of interest, it will also pass a `pages` object with the key `prevPage` and `nextPage` referring to the `Amity.Page` object that can be used to query the previous page and the next page, respectively. A sample code is provided below:

{% embed url="https://gist.github.com/bd6a57e4bd7ca92803781d680e45e4e4" %}
