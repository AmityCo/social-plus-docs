# Mute/Unmute a List of Channel Members

Moderators can mute and unmute users. When a user is muted, they cannot send messages in a channel. However, muted users will still be allowed to observe messages in a channel. The status of being muted is indefinite but is only applied at the channel level. The mute and unmute operations can be done via`Channel` object.

## Muting Channel Members

When a user is muted, they cannot send messages in a channel and all the messages sent by that user to that channel will be rejected. This method is useful for preventing certain members from sending inappropriate messages, but still allowing them to participate in the conversation in a read-only manner. The timeout property allows you to make the timeout temporary, or permanent until unset by passing in `-1`.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/e2a0d97ac09301426b59825f5ed0d1ef" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/dae76124af55079f63999d32c7e9514c#file-amitychannelbanuser-kt" %}
{% endtab %}

{% tab title="JavaScript" %}
```javascript
repository.muteMembers({
  userIds: ['user1'],
  period: 600,
}).catch(error => {
  ...
});
```
{% endtab %}

{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/7b6d31eedbacc69de7230d9823494db6" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/e8c60cf97a6b829ee31a00629fc973c4#file-amitychannelmembermute-dart" %}
{% endtab %}
{% endtabs %}

## Unmuting Channel Members

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/e86ed913ad1bdc499d1c6c6b5e1a8430" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/93a0a518dea4d1dae74e95818a24d628" %}
{% endtab %}

{% tab title="JavaScript" %}
```javascript
repository.unmuteMembers({
  userIds: ['user1'],
}).catch(error => {
  ...
});
```
{% endtab %}

{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/3b1ecccc8ef35be8e65453c5273ae001" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/c694c35a073975e82659bc2bdece2c74#file-amitychannelunmuteuser-kt" %}
{% endtab %}
{% endtabs %}

{% hint style="info" %}
This feature is not applicable in `Broadcast` and `Conversation` channel. Calling `muteMembers()` or `unmuteMembers()` on these channels will result in an error.
{% endhint %}
