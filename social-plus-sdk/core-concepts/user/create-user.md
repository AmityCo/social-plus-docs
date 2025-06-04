# Create User

In Social Plus SDK, creating a new user can be done through the login method. Once the user account has been created, the user can then log into the app using their `userId` and `displayName` using the SDK's social and chat features.

You may need to create a new user account via the SDK, such as when integrating the SDK with an existing user authentication system. In these cases, you can use the `login` method. Here's how the `login` method works:

* If a user already exists for the specified `userId`, the SDK will log the user into the app using the provided `userId`. The `displayName` parameter can be updated upon calling the `login` method. If the `displayName` parameter is not provided, the system will retain the existing user's `displayName`.
* If a user account does not already exist for the specified `userId`, the SDK will automatically create a new user account with the provided `displayName` and log the user into the app. If  `displayName` is not provided, the `userId` will be used as `displayName`.

{% hint style="info" %}
**Note**:

* _When user edits / adds their display name, it can be up to 100 characters in length._
* _When a user ID is created, it can be up to 50 characters in length._
* _If `displayName` is passed, but_ [_secured mode_](../../../analytics-and-moderation/console/settings/security/#secure-mode) _is enabled, the values will be ignored_.
{% endhint %}

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/f0b45fe6861bd0bb3011f7c4fe3fb55f#file-amityusercreation-kt" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/b6d53829e0295df991381bdccf13e317" %}
{% endtab %}

{% tab title="JavaScript" %}
{% embed url="https://gist.github.com/amythee/1154b128523e919c030881c449924283" %}
Without Auth Token
{% endembed %}

{% embed url="https://gist.github.com/amythee/3b7ae26d1294f65bdd4f5e48089083f1" %}
With Auth Token
{% endembed %}
{% endtab %}

{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/amythee/8bdba9f89c8780fae2a49e5c7dad33ee#file-login-ts" %}
Without Auth Token
{% endembed %}

{% embed url="https://gist.github.com/amythee/48cf885fe2816e10fd3aa95b8dce8411#file-login-ts" %}
With Auth Token
{% endembed %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/4a3d37b5e164655802bdd2c646f9d44a" %}
{% endtab %}
{% endtabs %}
