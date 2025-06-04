# User Token Management

API token management is a login authentication process that allows a Social Plus user to access Social Plus applications in a unified and streamlined environment.

Social Plus SDK provides AmityUserTokenManager to manage user credentials. This includes an access token that can be used to access some Beta features.

{% hint style="info" %}
**NOTE:** Please be aware that we do not provide any API to support the usage of user tokens on the client SDK. To use this user token, you must interact with ASC services with your own effort.
{% endhint %}

### Create a User Token

To create a new user token, refer to the following example and the parameters below.

* `userId`: This is a required parameter of type `String` that represents the unique identifier of the user whose credentials are being managed by the `AmityUserTokenManager`.
* `displayName` : This is an optional parameter of type `String` that represents the display name of the user. If provided, it will be associated with the user's credentials.
* `authToken` : This is an optional parameter of type `String` that represents the user's authentication token. If provided, it will be used to authenticate the user when accessing the Social Plus application. For further information about security please visit the [security page](../../../analytics-and-moderation/console/settings/security/).

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/f8ced5248bd1e2c9f6dd87bb6480d91c" %}
Creating iOS User Token
{% endembed %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/c78d8b7f7995a825c04812b36545de57" %}
{% endtab %}

{% tab title="JavaScript" %}
{% embed url="https://gist.github.com/f8b417bae717e912ca3c3b6c14bdb47a" %}
{% endtab %}

{% tab title="TypeScript" %}
**Version 6 and Beta(v0.0.1)**

{% embed url="https://gist.github.com/f6f64edb2838d6502497a4e5b64e32d1" %}
Creating Typescript User Token
{% endembed %}

{% embed url="https://gist.github.com/21429259257b860070c2a817fa7ee4c7" %}
Creating Typescript User Token\

{% endembed %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/bda5eaac608897a6f382a5126d35d4a0#file-amityauthentication-dart" %}
{% endtab %}
{% endtabs %}

