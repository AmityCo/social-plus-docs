# Query Communities

The `queryCommunities` method can be useful for users who are new to your app or are exploring their community options. By providing a way to explore for communities, you can help users to discover the full range of community options available within your app.

To query communities with certain criteria, the following parameters are used:

* `displayName` allows you to filter communities based on the community's displayName. (deprecated)
* `filter/membership` allows you filter communities based on the logged-in user membership status.
* `categoryId` allows you filter communities based on community categories.
* `sortBy` allows you filter communities based on the order that the communities were created or based on alphabetical order, last created, and first created.
* `includeDeleted` allows you specify if you want to include deleted communities in your query. By passing `true` or `false` to this method, you can include or exclude deleted communities from the results.

If you'd like to fetch all communities, you can pass the keyword as `null`. (deprecated)

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/b08b99bc4c4aa7aa90d56ae107db1ce1#file-query-communities-swift" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/3f9e5c0a6135858ef89647a2f7d86ce1#file-amitycommunityquery-kt" %}
{% endtab %}

{% tab title="JavaScript" %}
{% embed url="https://gist.github.com/amythee/8d1ae63afa6fd36cfafcd4c8413aed23#file-querycommunity-js" %}
{% endtab %}

{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/amythee/102ecb7f374c94a49ae74469335a56df#file-querycommunities-ts" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/d22e645d88768aeb6c0ab69c9bca0525#file-amitycommunityquery-dart" %}
{% endtab %}
{% endtabs %}

### Search for communities

To search for communities, users can call the relevant method and provide the desired keyword,  membership options, and other parameters.&#x20;

If no keyword is supplied, the list of users for the specified community will be sorted by the date they joined.&#x20;

To search for communities with certain criteria, the following parameters are used:

* `keyword` allows you to filter communities based on the community's displayName.
* `filter/membership` allows you to filter communities based on the logged-in user membership status.
* `categoryId` allows you to filter communities based on community categories.
* `sortBy` allows you to filter communities based on the order in which the communities were created or based on alphabetical order, last created, and first created.
* `includeDeleted` allows you to specify if you want to include deleted communities in your query. By passing `true` or `false` to this method, you can include or exclude deleted communities from the results.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/8be44f3e6072945f3abe4bc16eb179e3" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/3be5134ee8e3c62585281d27588d166f" %}
{% endtab %}
{% endtabs %}
