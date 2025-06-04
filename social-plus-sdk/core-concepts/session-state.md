# Session State

Session state is a key concept in the SDK that describes the authentication status of the client device. There are several session states that the SDK can be in, including:

* `notLoggedIn`
* `establishing`
* `established`
* `tokenExpired`
* `terminated`

The `established` state is the normal and fully authenticated state in which the SDK is usable. The other states represent different stages of the authentication process or an error condition.&#x20;

<figure><img src="../../.gitbook/assets/SDK session management-State Diagram Public.drawio-2.png" alt=""><figcaption><p>Session State Diagram</p></figcaption></figure>

When SDK is initialized:

* If the user is not logged in, the SDK starts in the initial "`notLoggedIn`" state.
* If the user is already logged in, the SDK automatically resumes the logged-in session and immediately switches to the `established` state.

{% hint style="info" %}
When TS SDK is initialized, the session state always begins as `notLoggedIn`.
{% endhint %}

When logging in:

* If login succeeds, it moves to `established` state.
* If login fails, it moves to `notLoggedIn` state.

When logging out manually:

* It moves to `notLoggedIn` state.

When the user is logged in, but the user is banned or deleted from the system.

* It moves to `terminated` state.

{% hint style="info" %}
The error code will be presented in `terminated` state. Please refer to [error-handling.md](error-handling.md "mention") for more details.
{% endhint %}

When token has expired:

* It moves to `tokenExpired` state.

{% hint style="info" %}
If the access token has expired, all network requests will fail. However, the SDK includes an automatic process for renewing the access token. As long as this process is implemented correctly, it is unlikely that the app will encounter this problem.\
\
Please refer to [#session-handler](session-state.md#session-handler "mention") for more details.
{% endhint %}

## Read and Observe Session State

The SDK provides APIs for reading and observing the session state.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/eb67b8631e57ba0741d5e0da92fbb433" %}
Observe Session State
{% endembed %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/ea2415af5339bab69a7d94d3c7b4b6f5" %}
{% endtab %}

{% tab title="JavaScript" %}
{% embed url="https://gist.github.com/997681fcab7345441d4070ceacd50977" %}
{% endtab %}

{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/7ed04752e24435964e37f1560e031d42" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/0ba60532f74959a4188a8a1a2268e91a" %}
{% endtab %}
{% endtabs %}

### Implementing an app based on session state

Session state is designed to align with the typical flow of an app. For example, developers can use the session state to guide app navigation, like this:

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/ae09e4e4f4697a350d9a9ec40220c770" %}
Implement app navigation based on session state
{% endembed %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/e2ba2fa818504c28e6e7598be242d787" %}
{% endtab %}

{% tab title="JavaScript" %}
{% embed url="https://gist.github.com/4b512278d75847737668c047f5bf17ff" %}
{% endtab %}

{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/amythee/d3dc70a870e62f3bbbcae9f20b457e39#file-login-ts" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/2a8a25426840247bb9d00b15014ed71f" %}
{% endtab %}
{% endtabs %}

## Session Handler

For logging, the SDK requires `SessionHandler`.  SDK uses this object to communicate with the app when session handling is required. Currently, `SessionHandler` is used for:

* Initiate access token renewal when it is about to expire or has expired.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/e51d903f696672562ed6853e75bd3c96" %}
A simple session handler
{% endembed %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/6fc0927375c4ca8bf72e19d26bd4f9c5" %}
{% endtab %}

{% tab title="JavaScript" %}
{% embed url="https://gist.github.com/33e5648232e5ec0a515c9f4089c5dffe" %}
{% endtab %}

{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/amythee/b818d2e4064b4adec34e85896e889793#file-login-ts" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/0ad700469b2519e2b57a8d04eacc2331" %}
{% endtab %}
{% endtabs %}

The code above shows a simple session handler. Please note that each function in `SessionHandler` can be customized to your app logic.

### Access Token Renewal

When a user logs in to the SDK for the first time, an access token is issued that is valid for 30 days.

If the access token is about to expire or has already expired, the SDK automatically initiates the renewal process through the `sessionWillRenewAccessToken` method of the `SessionHandler`.

During the renewal process, the SDK passes an `AccessTokenRenewal` object to the app. The app must call either one of the following methods on this object to complete the process.

<table><thead><tr><th width="344.5">Method on renewal object</th><th></th></tr></thead><tbody><tr><td><code>renew()</code></td><td>Indicates the SDK to renew the access token without an auth token. </td></tr><tr><td><code>renewWithAuthToken(...)</code></td><td>Indicates the SDK to renew the access token with an auth token. (Required for secure login)</td></tr><tr><td><code>unableToRetrieveAuthToken()</code></td><td><p>Indicates the SDK to postpone renewal.</p><p>SDK will re-initiate access token renewal at a later time, but no sooner than 10 minutes.</p></td></tr></tbody></table>

The following code shows how the app can implement the `sessionWillRenewAccessToken` method by providing an auth token for renewal.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/247021aeefc50f77ff6f593ae92247a0" %}
An example of access token renewal with auth token.
{% endembed %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/b2666425cd871ad72ddaa12e6da1f6cc" %}
{% endtab %}

{% tab title="JavaScript" %}
{% embed url="https://gist.github.com/7b8c326d22fd9e9d3d9c5adddd77bd8b" %}
{% endtab %}

{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/amythee/85a50802db37748cce99fefd568a6c36" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/69e662da3d176e089c0fbe3c128b8fb0" %}
{% endtab %}
{% endtabs %}
