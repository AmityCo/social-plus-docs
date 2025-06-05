# Join/Leave Channel

## Join a Channel

The `joinChannel` function allows users to join a channel, making them a member of the channel. This function takes one parameter, `channelId` which is the ID of the channel that the user wishes to join.

Once the user joins the channel, they will be able to participate in conversations and receive updates about the channel's activity. It is important to note that this function is idempotent, which means that it can be called multiple times without causing any issues. If the user has already joined the channel, a successful result will still be returned.



## Leave a Channel

The `leaveChannel` function is used to disengage a user from a channel by removing them from the list of members. This function takes the `channelId` parameter, which specifies the ID of the channel that the user wishes to leave. Once the user has left the channel, they will no longer receive any messages or updates from the channel.



## Channel Membership

When a user joins a channel, they can observe and chat with other users in that channel. They are also automatically considered a _member_ of that channel. The Chat SDK provides the ability to view which users are currently in the channel as well as invite other users to join the channel.

Each channel is identified by a unique `channelId`, which is any string that uniquely identifies the channel and is **immutable** through its lifetime. When creating channels, you can specify your own `channelId`, or leave it to Social Plus's Chat SDK to automatically generate one for you.

It's important to note that, `createChannel` guarantees that the requested channel is new (except for `conversation` type), whereas `joinChannel` will attempt to join an existing channel. If there is a requirement to create a new channel, then use of `createChannel` the call `joinChannel`. Lastly calling `getChannel` only gives you back the channel LiveObject, but it won't make the current user join said channel.

### Observe for changes in Membership

You can observe the channel to determine changes in the membership status. If the user is banned from the channel, you would want to show the particular UI and move from the chat screen.

For example, in the event of a channel ban, it's possible to implement the appropriate user interface, navigating the user to be redirected away from the chat screen.

