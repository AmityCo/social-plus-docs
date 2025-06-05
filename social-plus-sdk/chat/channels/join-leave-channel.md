# Join/Leave Channel

## Join a Channel

The `joinChannel` function allows users to join a channel, making them a member of the channel. This function takes one parameter, `channelId` which is the ID of the channel that the user wishes to join.

Once the user joins the channel, they will be able to participate in conversations and receive updates about the channel's activity. It is important to note that this function is idempotent, which means that it can be called multiple times without causing any issues. If the user has already joined the channel, a successful result will still be returned.

<Tabs>
  <Tab title="iOS">
    <CodeGroup>
      <CodeGroupItem>
{% embed url="https://gist.github.com/amythee/7991098360c38871df9c3810cc0420ed#file-join_a_channel-swift" %}
      </CodeGroupItem>
    </CodeGroup>
  </Tab>

  <Tab title="Android">
    <CodeGroup>
      <CodeGroupItem>
{% embed url="https://gist.github.com/amythee/c09f00e446510aabf1822258df0a8ed1" %}
      </CodeGroupItem>
    </CodeGroup>
  </Tab>

  <Tab title="JavaScript">
```javascript
const isJoined = await ChannelRepository.joinChannel({
channelId: 'channel2'
});
```
  </Tab>

  <Tab title="TypeScript">
Version 6

{% embed url="https://gist.github.com/amythee/f8db2dbeb4ce6b5b57b8b1f32310d953#file-joinchannel-ts" %}

Beta (v0.0.1)

{% embed url="https://gist.github.com/bc6472ea1de477b8fec72f55613a7001" %}
  </Tab>

  <Tab title="Flutter">
    <CodeGroup>
      <CodeGroupItem>
{% embed url="https://gist.github.com/amythee/1e92fcd7e40deb3c1fa3e672172231f8#file-amitychanneljoin-dart" %}
      </CodeGroupItem>
    </CodeGroup>
  </Tab>
</Tabs>

## Leave a Channel

The `leaveChannel` function is used to disengage a user from a channel by removing them from the list of members. This function takes the `channelId` parameter, which specifies the ID of the channel that the user wishes to leave. Once the user has left the channel, they will no longer receive any messages or updates from the channel.

<Tabs>
  <Tab title="iOS">
    <CodeGroup>
      <CodeGroupItem>
{% embed url="https://gist.github.com/amythee/d697cb2b09a848b8f07f8b82763eb028#file-leave_channel-swift" %}
      </CodeGroupItem>
    </CodeGroup>
  </Tab>

  <Tab title="Android">
    <CodeGroup>
      <CodeGroupItem>
{% embed url="https://gist.github.com/amythee/4fe563367933a7835268df34e77f7b5b" %}
      </CodeGroupItem>
    </CodeGroup>
  </Tab>

  <Tab title="JavaScript">
```javascript
import { ChannelMembershipRepository } from '@amityco/js-sdk';

await ChannelMembershipRepository.leaveChannel({ 
  channelId: 'channelId', 
})
```
  </Tab>

  <Tab title="TypeScript">
**Version 6**

{% embed url="https://gist.github.com/amythee/3f762c73bd5ff916591347c582107d93#file-leavechannel-ts" %}

**Beta (v0.0.1)**

{% embed url="https://gist.github.com/c49007734f8fe626797e23d3d985dbc5" %}
  </Tab>

  <Tab title="Flutter">
    <CodeGroup>
      <CodeGroupItem>
{% embed url="https://gist.github.com/amythee/a4e129fbe74b0a9efd6e863b7c381cad#file-amitychannelleave-dart" %}
      </CodeGroupItem>
    </CodeGroup>
  </Tab>
</Tabs>

## Channel Membership

When a user joins a channel, they can observe and chat with other users in that channel. They are also automatically considered a _member_ of that channel. The Chat SDK provides the ability to view which users are currently in the channel as well as invite other users to join the channel.

Each channel is identified by a unique `channelId`, which is any string that uniquely identifies the channel and is **immutable** through its lifetime. When creating channels, you can specify your own `channelId`, or leave it to Social Plus's Chat SDK to automatically generate one for you.

It's important to note that, `createChannel` guarantees that the requested channel is new (except for `conversation` type), whereas `joinChannel` will attempt to join an existing channel. If there is a requirement to create a new channel, then use of `createChannel` the call `joinChannel`. Lastly calling `getChannel` only gives you back the channel LiveObject, but it won't make the current user join said channel.

### Observe for changes in Membership

You can observe the channel to determine changes in the membership status. If the user is banned from the channel, you would want to show the particular UI and move from the chat screen.

For example, in the event of a channel ban, it's possible to implement the appropriate user interface, navigating the user to be redirected away from the chat screen.

<Tabs>
  <Tab title="iOS">
    <CodeGroup>
      <CodeGroupItem>
{% embed url="https://gist.github.com/amythee/69890e31b8604119625dd84d4459f840#file-check_channel_membership-swift" %}
      </CodeGroupItem>
    </CodeGroup>
  </Tab>

  <Tab title="Android">
    <CodeGroup>
      <CodeGroupItem>
{% embed url="https://gist.github.com/amythee/bbc150ef248f0a3f6de36c8ff3b91d17" %}
      </CodeGroupItem>
    </CodeGroup>
  </Tab>

  <Tab title="JavaScript">
Supported ✅ (please wait while we prepare a real example!)
  </Tab>

  <Tab title="TypeScript">
{% embed url="https://gist.github.com/amythee/203ae5bb1bd8eaa7995b6b634b45de5b" %}
  </Tab>

  <Tab title="Flutter">
Supported ✅ (please wait while we prepare a real example!)
  </Tab>
</Tabs>