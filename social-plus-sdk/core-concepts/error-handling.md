# Error Handling

## Server Errors

<table data-header-hidden><thead><tr><th width="118.33333333333331">Code</th><th width="343">Error Name</th><th>Description</th></tr></thead><tbody><tr><td><strong>Code</strong></td><td><strong>Error Name</strong></td><td><strong>Description</strong></td></tr><tr><td>400000</td><td><code>BadRequestError</code></td><td>Request contains invalid parameters.</td></tr><tr><td>400001</td><td><code>InvalidRegularExpression</code></td><td>An invalid regex rule retrieved from or added to the Blocklist</td></tr><tr><td>400002</td><td><code>VideoFormatInvalidRequestError</code></td><td>Video format not supported</td></tr><tr><td>400100</td><td><code>UnauthorizedError</code></td><td>Unverified user performs any action that requires access token verification.</td></tr><tr><td>400300</td><td><code>ForbiddenError</code></td><td>User performs forbidden action such as uploading a pdf file in an image message.</td></tr><tr><td>400301</td><td><code>PermissionDenied</code></td><td>User has no permission to perform the action.</td></tr><tr><td>400302</td><td><code>UserIsMuted</code></td><td>A muted user sends a message.</td></tr><tr><td>400303</td><td><code>ChannelIsMuted</code></td><td>User sends a message in a muted channel.</td></tr><tr><td>400304</td><td><code>UserIsBanned</code></td><td>User accessed a channel or community where he is banned.</td></tr><tr><td>400307</td><td><code>MaxRepetitionExceed</code></td><td>User reached the limit of the number of sent messages containing blocklisted words.</td></tr><tr><td>400308</td><td><code>BanWordFound</code></td><td>User sends a message that contains a blocklisted word.</td></tr><tr><td>400309</td><td><code>LinkNotAllowed</code></td><td>User sends a message that contains link that is not in the Allowlist.</td></tr><tr><td>400311</td><td><code>RPCRateLimitError</code></td><td>Web socket rate limit is exceeded.</td></tr><tr><td>400312</td><td><code>GlobalBanError</code></td><td>Banned user performs any action.</td></tr><tr><td>400314</td><td><code>UnsafeContent</code></td><td>Content moderation system detects unsafe content (eg. nudity). </td></tr><tr><td>400315</td><td><code>DuplicateEntryError</code></td><td>Display name of a collection already exists (eg. for your channels or community categories).</td></tr><tr><td>400316</td><td><code>UserIsUnbanned</code></td><td>Returned when unbanning a user that is not banned.</td></tr><tr><td>400317</td><td><code>ForbiddenError</code></td><td>The only active moderator in a channel/community attempts to leave and there are no other moderators in the group.</td></tr><tr><td>400318</td><td><code>ForbiddenError</code></td><td>The only moderator in a channel/community attempts to leave and there are no other members in the group.</td></tr><tr><td>400319</td><td><code>ForbiddenError</code></td><td>User changes module and user notification settings but the network notification setting is off.</td></tr><tr><td>400400</td><td><code>ItemNotFound</code></td><td>System cannot find any resource matched with the requested condition.</td></tr><tr><td>400900</td><td><code>Conflict</code></td><td>System cannot create/update duplicated data.</td></tr><tr><td>500000</td><td><code>BusinessError</code></td><td>Uncategorized internal system errors not related to any user input.</td></tr><tr><td>500000</td><td><code>BusinessError</code></td><td>Video upload failed</td></tr></tbody></table>

## Client Errors

<table data-header-hidden><thead><tr><th width="155.33333333333331">Code</th><th>Error Name</th><th>Description</th></tr></thead><tbody><tr><td><strong>Code</strong></td><td><strong>Error Name</strong></td><td><strong>Description</strong></td></tr><tr><td>800000</td><td><code>Unknown</code></td><td><p>Uncategorized errors. </p><p>To debug, refer to the <em>'error.message'</em> property.</p></td></tr><tr><td>800110</td><td><code>InvalidParameter</code></td><td>Data type of the parameter is invalid.</td></tr><tr><td>800210</td><td><code>ConnectionError</code></td><td>Websocket connection of the SDK cannot reach the platform server. This could also be the case if a user is global-banned and try to register a session.</td></tr></tbody></table>



## Error Objects

Error objects can be returned to you via LiveObjects, callbacks, or client error delegates. The possible error codes are listed in a public error code enum: each case is named after its error.

You can convert a Social Plus Exception into a Social Plus Error with the following:

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/1adbaf71a34e73af61476d7065fbb6eb" %}

{% hint style="info" %}
All the errors returned by the iOS SDK come in the form of an `NSError` with domain Social Plus.
{% endhint %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/670c317861e6a36a1b63c9b46a4271ab" %}
AmityError enums map to the supported error scenarios
{% endembed %}

For any specific errors that's handled in PagingData please visit the web page below  to properly handle its errors [https://developer.android.com/topic/libraries/architecture/paging/load-state#adapter](https://developer.android.com/topic/libraries/architecture/paging/load-state#adapter)
{% endtab %}

{% tab title="JavaScript" %}
```java
import { ErrorCode, CommunityRepository } from '@amityco/js-sdk'

const liveObject = CommunityRepository.communityForId('abc');
liveObject.on("dataUpdated", data => {
  // community is fetched
});
liveObject.on("dataError", err => {
  // failed to fetch the community 
  console.log(err.code == ErrorCode.BusinessError);
}
```



{% hint style="info" %}
&#x20;All the errors returned by the SDK come in form of an Error with domain `ASC`.&#x20;
{% endhint %}
{% endtab %}

{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/eb3589e419e4daa0e7e410cb7a8955b9" %}
{% endtab %}
{% endtabs %}

> When an error is returned as a result of an action from your side (e.g. trying to join a channel), the action is considered completed and the SDK will not execute any additional logic.

## Global ban error handling

A global ban error means that the user is banned from the system resulting in the inability to have a connection with the system. If the user already has a session, the session will be revoked, and will be unable to create a new session.&#x20;

{% tabs %}
{% tab title="iOS" %}
```swift
var client: AmityClient?
client.clientErrorDelegate = self // set yourself as the delegate

...

// Implement this delegate method which gets called when error occurs
func didReceiveAsyncError(_ error: Error) {
        let error = error as NSError
        guard let amityError = AmityErrorCode(rawValue: error.code) else {
            assertionFailure("unknown error \(error.code), please report this code to Amity")
            return
        }
        
        if amityError == .globalBan {
            // Handle global ban event here
        }
    }
```
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/5581afbcf85dc940b050e2a8c557aaba" %}
Banned while not having a session
{% endembed %}



{% embed url="https://gist.github.com/b771fee125355059f90f624f5c910bd9" %}
Observing the LiveObject for ban while having a session
{% endembed %}
{% endtab %}

{% tab title="JavaScript" %}
```java
client = new ASCClient({ apiKey, apiEndpoint });

client.on('dataError', error => {
  if (error.code === ErrorCode.GlobalBanError) {
    // handle the case the user is globally banned
  }
});
```
{% endtab %}

{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/ed878a8d4638c4c1f37bd4e8f1438b23" %}
&#x20;
{% endembed %}
{% endtab %}
{% endtabs %}
