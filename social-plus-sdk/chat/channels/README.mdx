---
description: >-
  Our channels enable developers to implement different types of chat messaging
  capabilities into their applications easily
---

# Channels

In this section, we will cover the concept of channels in Social Plus Chat SDK and how to use them to enable different types of chat messaging capabilities in your application.

<Info>
Please be aware that there is some incompatibility between SDK **version 5** and **version 6** regarding the Subchannel feature.

* Applications using SDK version 5 cannot view messages sent to subchannels by SDK version 6.
* Channels can be sorted by 'Last Activity', which means that if messages are sent to SDK version 5 in subchannels, it moves the channel to the top of the collection. However, while the order will be updated to the top, SDK version 5 will not display the message.
</Info>

## Channel and Subchannel Structure

The concept of "channel and subchannel" is central to understanding how communication is structured in a chat SDK. Channels are the primary containers that hold subchannels, while subchannels are subdivisions within a channel that represent individual topics or chat threads.

The relationship between a channel and its subchannels is hierarchical. A channel serves as a parent container for multiple subchannels, each of which represents a separate conversation or topic. Messages and interactions occur within subchannels, not the main channel itself. This organization allows for easier navigation and management of different conversations within a single channel.

The differences between channels and subchannels are as follows:

1. **Function**: Channels act as containers for subchannels, while subchannels are where actual conversations and interactions take place.
2. **Hierarchy**: Channels serve as parent containers, whereas subchannels are subdivisions within a channel.
3. **Messages**: Channels do not contain any messages directly; instead, all messages are stored within subchannels.
4. **Management**: Users can create, update, delete, and query subchannels within a channel, managing each subchannel individually.
5. **Moderation**: Moderation actions, such as banning, unbanning, muting, and unmuting users, can be performed at the channel level rather than the subchannel level. This approach ensures that moderation decisions apply to all subchannels within the main channel, providing consistent management across different conversations or topics.

<Info>
By default, when a channel is created, a corresponding default subchannel is also automatically generated.
</Info>

<Frame>
  <img src="../../../.gitbook/assets/Screenshot 2566-04-25 at 09.20.51.png" alt="" />
</Frame>

## Channel Types

Social Plus's Chat SDK has several channel types with different use cases. Each type is designed to match a particular use case for chat channels.

<table>
  <thead>
    <tr>
      <th width="150">Channel Type</th>
      <th width="132">Discoverable by</th>
      <th width="128">Message sending privileges</th>
      <th width="120">Moderation access</th>
      <th width="101">Channel Creation</th>
      <th>Realtime Events</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Community</td>
      <td>All users and admins</td>
      <td>Joined members and admins</td>
      <td>All Moderation tools</td>
      <td>SDK, Console</td>
      <td>Automatic</td>
    </tr>
    <tr>
      <td>Private Community</td>
      <td>Joined members and admins</td>
      <td>Joined members and admins</td>
      <td>All Moderation tools</td>
      <td>SDK, Console</td>
      <td>Automatic</td>
    </tr>
    <tr>
      <td>Live</td>
      <td>Joined members and admins</td>
      <td>Joined members and admins</td>
      <td>All Moderation tools</td>
      <td>SDK, Console</td>
      <td>Subscription needed</td>
    </tr>
    <tr>
      <td>Broadcast</td>
      <td>All users and admins</td>
      <td>Admins, and designated moderators</td>
      <td>Admin Moderation tools</td>
      <td>SDK, Console</td>
      <td>Subscription needed</td>
    </tr>
    <tr>
      <td>Conversation</td>
      <td>Joined members</td>
      <td>Joined members</td>
      <td>No Moderation tools</td>
      <td>SDK</td>
      <td>Automatic</td>
    </tr>
  </tbody>
</table>

<Info>
For further information about channel's realtime events process, please visit [chat-realtime-events.md](../../core-concepts/realtime-events/chat-realtime-events.md "mention").
</Info>

### Community and Private Community Channel

The community channel is the default channel type and can be discovered by all users and admins. It acts as a public chat channel that showcases all of the features that our SDKs have to offer.

#### Channel characteristics:

* All users in the network can search for a community channel
* All users in the network can join the community without an invitation
* Support @mention user
* Support @mention all users in the channel
* Appear on SP Console for an administrator to monitor

#### Typical use cases:

* Team collaboration
* Online gaming
* Celebrity fan club
* Live streaming
* Any type of public chat

### Live Channel

Live channels offer the ability for users and admins to create channels with exclusive membership. The live channel is identical to our Community channel in features with the caveat that users will not be able to discover the channel when querying for all channels unless they are already a member of it. However, users and admins can still invite other users to join the channel.

#### Channel characteristics

* Can only be searched by member
* Users can join if they know the channel ID
* Support @mention user
* Support @mention channel users (mention all users)
* Appear on the ASC console for the administrator to monitor

#### Typical use cases:

* Chat channel for a one-time Live event

### Conversation

Conversation channels are designed for 1-on-1 messaging and private small group chat. Unlike the other channel types, a Conversation channel can be created simply by knowing the **userId** of the user we want to converse with. Users can start conversations with any other user and only they will be able to see their conversation.

Each channel has its own list of members, and no two channels can have the same member list. If someone tries to create a new channel with the same set of members as an existing channel, the system will return the existing channel. For example, creating a new channel with User A and User B will always result in the same channel no matter how many times the create command is called. This is useful when trying to establish a private chat channel between 2 or more users as we want to make sure the user can continue using the existing channel that contains previous messages history.

#### Channel characteristics

* Channel is always unique with the same set of memberships.
* Support up to 10 members per conversation channel
* Users can not join, leave, be added, or removed from the channel once it's created
* Users can not ban/unban other users in the channel
* Does not appear on the SP console for the administrator to monitor
* Does not support @mention user & @mention all

#### Typical use cases:

* 1:1 Chat Channel
* Private Group Chat
* Customer Support Chat

<Note>
Channel types can be created through SDK i.e `Community`, `Live` and `Conversation`. Creation of `Private` and `Standard` type has been removed.
</Note>

### Broadcast

The Broadcast channel is heavily adopted by corporate users who constantly promote or advertise their products, or make the announcement to drive awareness. Unlike other channel types, broadcast channels only allow admin users to send messages from Console, [API](https://api-docs.amity.co/#/Message/post_api_v3_messages), and SDK, and everyone else in the channel will be under read-only mode.

#### Broadcast channel characteristics

* Broadcast messages can be sent out via SP console, [API](https://api-docs.amity.co/#/Message/post_api_v3_messages), and SDK with admin or moderator permissions.
* The administrator can choose to send to any community OR live channel (but not to the conversation channel).
* Support @mention user
* Support @mention channel users (mention all users)

Typical use cases:

* Marketing & Advertising
* Organizational Announcements

### Channel Properties

<table>
  <thead>
    <tr>
      <th width="291">Name</th>
      <th width="211">Data Type</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`channelId`</td>
      <td>`String`</td>
      <td>ID of the channel</td>
    </tr>
    <tr>
      <td>`defaultSubchannelId`</td>
      <td>`String`</td>
      <td>ID of the default subchannel that's generated upon channel creation</td>
    </tr>
    <tr>
      <td>`isDistinct`</td>
      <td>`Bool`</td>
      <td>Is channel distinct?</td>
    </tr>
    <tr>
      <td>`metadata`</td>
      <td>`JsonObject`</td>
      <td>Additional properties to support custom fields</td>
    </tr>
    <tr>
      <td>`type`</td>
      <td>`AmityChannelType`</td>
      <td>Type of channel</td>
    </tr>
    <tr>
      <td>`tags`</td>
      <td>`Array<String>`</td>
      <td>Tags used for searching</td>
    </tr>
    <tr>
      <td>`isMuted`</td>
      <td>`Bool`</td>
      <td>Is this channel muted?</td>
    </tr>
    <tr>
      <td>`isRateLimited`</td>
      <td>`Bool`</td>
      <td>This channel has limited sending rate?</td>
    </tr>
    <tr>
      <td>`rateLimit`</td>
      <td>`Int`</td>
      <td>Number of messages within rate limit</td>
    </tr>
    <tr>
      <td>`displayName`</td>
      <td>`String`</td>
      <td>Channel name for displaying</td>
    </tr>
    <tr>
      <td>`memberCount`</td>
      <td>`Integer`</td>
      <td>Number of members in channel</td>
    </tr>
    <tr>
      <td>`messageCount`</td>
      <td>`Integer`</td>
      <td>Number of messages in channel</td>
    </tr>
    <tr>
      <td>`unreadCount`</td>
      <td>`Integer`</td>
      <td>Number of unread messages in channel</td>
    </tr>
    <tr>
      <td>`lastActivity`</td>
      <td>`DateTime`</td>
      <td>Date/time of user's last activity related to the channel (e.g. add/remove member)</td>
    </tr>
    <tr>
      <td>`createdAt`</td>
      <td>`DateTime`</td>
      <td>Date/time the channel was created</td>
    </tr>
    <tr>
      <td>`updatedAt`</td>
      <td>`DateTime`</td>
      <td>Date/time the channel was last updated</td>
    </tr>
    <tr>
      <td>`avatarFileId`</td>
      <td>`String`</td>
      <td>Avatar file ID</td>
    </tr>
    <tr>
      <td>`isPublic`</td>
      <td>`Bool`</td>
      <td>Public / Private community channel</td>
    </tr>
  </tbody>
</table>

Channel Object is a Live Object and you can observe real-time changes in Channel Properties. Please see to [Live Object](../../core-concepts/live-objects-collections/) on how to listen to real-time changes.