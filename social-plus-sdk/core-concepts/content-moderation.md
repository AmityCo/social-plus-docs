# Content Moderation

## Validate URL

The `validateUrls()` function takes an array of `urls` as input. It returns a success response if the input passes validation and throws an error otherwise. It ensures that the URLs conform to the pre-defined list set in ASC console.&#x20;

Here's an explanation of the function parameter:

* `urls`: An array of URLs to be validated

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/1884adcfb393ec60d61fd4d883221bb2" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/3feb2b3be1e03cfc822193d92f7f47af" %}
{% endtab %}
{% endtabs %}

## Validate Text

The `validateTexts()` function takes an array of `texts` as input. It returns a success response if the input passes validation and throws an error otherwise. It ensures that the text does not contain any of the pre-defined blocked words set in the ASC console.

Here's an explanation of the function parameter:

* `texts`: An array of texts to be validated

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/87e2322f08c00e0f1fd9c3f8083682f5" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/d6757c84f4546bd8e2333f44f7ff1fec" %}
{% endtab %}
{% endtabs %}

