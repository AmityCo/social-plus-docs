---
description: >-
  When a user is banned in a channel, they are removed from a channel and no
  longer able to participate or observe messages in that channel.
---

# Ban/Unban a List of Channel Members

Moderators can ban and unban users. When a user is banned from a channel, they are forcibly removed from the channel and may no longer participate or observe messages in that channel. All their previous messages in the channel will also be automatically deleted.

A user that has been banned from a channel can not rejoin the channel until they have been unbanned.

## Global Ban

As well as the banning and unbanning of users, admins also have the ability to global ban a user. When a user is globally banned, they can no longer access Social Plus's network and will be forcibly removed from all their existing channels. All the globally banned user's messages will also be deleted.

The globally banned user can not access Amity's network again until they have been globally unbanned.

{% hint style="info" %}
When a user is banned, it can take up to 30 seconds before the user is disconnected from the network.
{% endhint %}

## Ban Users

Banning members is a more heavy-handed moderation method. When a user is banned, all its messages are retroactively deleted, it will be removed from the channel, and it will not be allowed to join the channel again until it is explicitly unbanned.

{% tabs %}
{% tab title="iOS" %}
```swift

let moderation = AmityChannelModeration(client: <amityclient>, channel: <channel-id>)
​
moderation.banMembers(["user1"]) { success, errror in
  ...
}
```
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/5c7e8f1c65dee31e24cca663740737af" %}
{% endtab %}

{% tab title="JavaScript" %}
```javascript
repository.banMembers({
  userIds: ['user1'],
}).catch(error => {
  ...
});
```
{% endtab %}

{% tab title="TypeScript" %}
Version 6

{% embed url="https://gist.github.com/9f1e9bbcb7126ff0330cec53e7650c89" %}

Beta (v0.0.1)

{% embed url="https://gist.github.com/1db93c530a89f5ccc3caac1933ed4b96" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/7991a1742a26056c1938c2a9b5b88cc8#file-amitychannelmemberban-dart" %}
{% endtab %}
{% endtabs %}

## Unban Users

{% tabs %}
{% tab title="iOS" %}
Supported ✅ (please wait while we prepare a real example!)
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/3b8110a47daff61d673cc33da6edb9a5" %}
{% endtab %}

{% tab title="JavaScript" %}
```javascript
repository.unbanMembers({
  userIds: ['user1'],
}).catch(error => {
  ...
});
```
{% endtab %}

{% tab title="TypeScript" %}
Version 6

{% embed url="https://gist.github.com/79ada50acaf5898aae0871c7a812f314" %}

Beta (v0.0.1)

{% embed url="https://gist.github.com/2b7988270a6e1563f48a92a07c44d2fe" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/d342f7489dd8214e8195fbba79a0718e#file-amitychannelmemberunban-dart" %}
{% endtab %}
{% endtabs %}

{% hint style="info" %}
This feature does not work with `Broadcast` and `Conversation` channels. Calling `banMembers()` or `unbanMembers()` on these channels will result in an error.
{% endhint %}
