# Channel Moderation

Channel Moderation is an essential feature for creating a safe and engaging chat community. With Social Plus Chat SDK, developers can use moderation to manage chat channels effectively and ensure that the chat community remains safe and welcoming. Moderation features such as user banning and muting can help prevent inappropriate content and maintain a positive chat environment.

## Add / Remove Roles

[<mark style="color:blue;">Roles</mark>](../../core-concepts/user/user-permission.md#channel) define varying levels of access and permissions that can be assigned to users within a chat channel. Each role is defined by a set of permissions that determine what actions a user can perform within the channel.

Roles can be assigned to users based on factors such as their level of participation in the chat community or their specific responsibilities within the channel. For example, a moderator might have the ability to remove inappropriate messages or ban users from the channel, while a regular user might only have the ability to send and receive messages. For more information, please refer to the [<mark style="color:blue;">Roles and Permission</mark>](https://docs.amity.co/amity-sdk/chat/moderation/roles-and-permission#roles) page.&#x20;

## Permission

You can check your permission in the channel by sending `AmityPermission` enums to `AmityCoreClient.hasPermission(amityPermission)`. For more information, please refer to the [<mark style="color:blue;">Roles and Permission</mark>](https://docs.amity.co/amity-sdk/chat/moderation/roles-and-permission#roles) page.&#x20;

## Add / Remove Members <a href="#manage-members" id="manage-members"></a>

`AmityChannelMembership` provides methods to add and remove members, as well as removing yourself as a member of the channel (leaving the channel).

* `channelId`: The ID of the channel to which you want to add or remove members.
* `userIds`: An array of user IDs to be added to the channel or removed from the channel.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/0093c8ce0e6c4cf9bfcc88b61b3d4311" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/13081f5936a91acf555e5bed1d9c083f" %}
{% endtab %}

{% tab title="JavaScript" %}
```javascript
// add 'user1' and 'user2' to this channel
const isAdded = await ChannelRepository.addMembers({
  channelId: 'channel1',
  userIds: [ 'user1', 'user2' ],
});

// remove 'user3' from this channel
const isRemoved = await ChannelRepository.removeMembers({
  channelId: 'channelId',
  userIds: [ 'user3' ],
});

// leave this channel
const isLeaved = await ChannelRepository.leave('channelId');
```
{% endtab %}

{% tab title="TypeScript" %}
Version 6

Add Channel Members

{% embed url="https://gist.github.com/a06566f4fb2962a60eea48fecdcd09e7" %}

Remove Channel Members

{% embed url="https://gist.github.com/amythee/7ccdf1769fd3af676913ad583c39aa3b#file-removechannelmembers-ts" %}

Beta (v0.0.1)

Add Channel Members

{% embed url="https://gist.github.com/c7833ae526bf6cc609d95a52209e9e8a" %}

Remove Channel Members

{% embed url="https://gist.github.com/384c181bdea78f5c4f4a8c1364a8c853" %}
{% endtab %}

{% tab title="Flutter" %}
The functionality isn't currently supported by this SDK.
{% endtab %}
{% endtabs %}

## Ban / Unban Members

`ChannelRepository` class also provides various methods to moderate the users present in the channel. You can ban/unban users, assign roles, or remove them from users.

For the `banMembers` function, the following parameters are required:

* `channelId`: The ID of the channel from which the members are being banned.
* `userIds`: An array of user IDs to be banned from the channel.

For the `unbanMembers` function, the following parameters are required:

* `channelId`: The ID of the channel from which the members are being unbanned.
* `userIds`: An array of user IDs to be unbanned from the channel.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/6ea5347adf82ca62f8c9a73f44d6e748" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/5c7e8f1c65dee31e24cca663740737af" %}
{% endtab %}

{% tab title="JavaScript" %}
```javascript
const isBanned = await ChannelRepository.banMembers({ 
  channelId: 'channel1', 
  userIds: ['user1']
);
​
const isUnbanned = await ChannelRepository.banMembers({ 
  channelId: 'channel1', 
  userIds: ['user1']
);
​
await ChannelRepository.addRole({ 
  channelId: 'channel1', 
  userIds: ['user1'],
  role: 'role1',
);
​
await ChannelRepository.removeRole({ 
  channelId: 'channel1', 
  userIds: ['user1'],
  role: 'role1',
);
```
{% endtab %}

{% tab title="TypeScript" %}
Version 6

Ban members

{% embed url="https://gist.github.com/9f1e9bbcb7126ff0330cec53e7650c89" %}

Unban members

{% embed url="https://gist.github.com/79ada50acaf5898aae0871c7a812f314" %}

Beta (v0.0.1)

Ban members

{% embed url="https://gist.github.com/1db93c530a89f5ccc3caac1933ed4b96" %}

Unban members

{% embed url="https://gist.github.com/2b7988270a6e1563f48a92a07c44d2fe" %}
{% endtab %}

{% tab title="Flutter" %}
Supported ✅ (please wait while we prepare a real example!)
{% endtab %}
{% endtabs %}
