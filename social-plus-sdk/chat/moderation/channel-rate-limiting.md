# Channel Rate-Limiting

This method is useful when there is a large number of messages going through the channel, which can make the message stream hard to follow. Setting a rate limit enables the SDK to queue up messages once the number of messages in a specified `window` exceeds the defined `limit`, allowing a slower stream of messages to be published to the user at the expense of adding more latency (because newer messages will be sent to the queue first and not delivered until all previously queued messages are delivered).

> There is an internal limit of 1000 messages that can be queued by the rate limit service, if more than 1000 messages are queued up, the system may skip publishing the older messages in order to make room for newer messages. We believe this is the preferred behavior for users, as users will most likely want to see newer messages in a real-time conversation instead of waiting for a significant amount of time for old messages to be published to them first.
>
> Note that the SDK permanently stores all messages it receives in the system **before** the rate limit comes into effect: in the case of a large spike of incoming messages, even if a message did not get published to a user in real-time, that user can still scroll up to see message history and see that past message.

{% tabs %}
{% tab title="iOS" %}
{% code overflow="wrap" %}
```swift
repository.rateLimitPeriod(600, rateLimit: 5, rateLimitWindow: 60) { success, error in
  ...
}
```
{% endcode %}
{% endtab %}

{% tab title="Android" %}
The functionality isn't currently supported by this SDK.
{% endtab %}

{% tab title="JavaScript" %}
```javascript
repository.setRateLimit({
  period: 600,
  rateLimit: 5,
  rateLimitWindow: 60,
}).catch(error => {
  ...
});JavaScript
```
{% endtab %}

{% tab title="TypeScript" %}
Supported ✅ (please wait while we prepare a real example!)
{% endtab %}

{% tab title="Flutter" %}
The functionality isn't currently supported by this SDK.
{% endtab %}
{% endtabs %}

The above method enables a rate limit of 5 messages every 60 seconds: once there are more than 5 messages sent, from any user, within 60 seconds, those messages will be queued on the server and not published to other channel members until 60 seconds have passed. The rate limit will last as long as the period specified in the method call: in the example above the rate limit will be active for 10 minutes (600 seconds).

If you would like to have a permanent rate limit, call the method above with a period of -1 seconds.

To disable the rate limit, simply call `removeRateLimitWithCompletion:`

{% tabs %}
{% tab title="iOS" %}
```swift
repository.removeRateLimit { success, error in
  ...
}
```
{% endtab %}

{% tab title="Android" %}
The functionality isn't currently supported by this SDK.
{% endtab %}

{% tab title="JavaScript" %}
```javascript
repository.removeRateLimit().catch(error => {
  ...
});
```
{% endtab %}

{% tab title="TypeScript" %}
Supported ✅ (please wait while we prepare a real example!)
{% endtab %}

{% tab title="Flutter" %}
The functionality isn't currently supported by this SDK.
{% endtab %}
{% endtabs %}
