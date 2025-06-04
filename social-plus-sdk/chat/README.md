---
description: >-
  Social Plus Chat SDK allows you to easily create full-featured in-app Chat
  experience
---

# Chat

<img src="https://i.ibb.co/w67NSLH/iOSicon.png" alt="image-text" data-size="line"> **iOS** ​[<img src="https://i.ibb.co/MD88cLD/android-Icon.png" alt="image-text" data-size="line">](https://docs.amity.co/chat/android) **Android** ​<img src="https://i.ibb.co/ZzhYFSL/webIcon.png" alt="image-text" data-size="line"> **Web** <img src="../../.gitbook/assets/Typescript_logo_2020.svg" alt="" data-size="line"> **TypeScript** <img src="../../.gitbook/assets/reactnativelogo.png" alt="" data-size="line"> **React Native** <img src="../../.gitbook/assets/ionic-Logo.svg" alt="" data-size="line"> **Ionic**  <img src="../../.gitbook/assets/Screen Shot 2565-08-24 at 13.18.22.png" alt="" data-size="line">**Flutter**

### Social Plus Chat SDK

The Social Plus Chat SDK provides a powerful set of pre-built features to enable in-app social experiences and fuel user engagement. With support for a range of platforms and programming languages, the SDK is a flexible and scalable solution for building messaging apps. We hope this documentation page has provided you with the information you need to get started with the SDK. If you have any questions or feedback, please feel free to contact us via our support center.

We provide a range of pre-built features that enable in-app social experiences and fuel user engagement. Here are some of the main features of the SDK:

* Start a new conversation channel with up to 300,000 concurrent participants (actual maximum may vary from the selected plan, see [pricing](https://www.amity.co/pricing) for more detail)
* View read counts for every message
* Moderate conversations with user banning, muting, and rate limiting
* Assign moderators and admins via a role-based permission system
* Filter out inappropriate content with automated spam filtering and URL whitelists
* Manage connection state and handle offline data automatically
* Support multi-device and multi-platform for every user
* Powerful messaging capabilities for native and web apps
* Moderation tools for filtering out inappropriate content
* Role-based permission system for assigning moderators and admins
* Real-time syncing of messages across all users in a channel
* Support for text, image, audio, video, file, and custom messages
* Support up to 300,000 concurrent participants in a channel

#### Getting Started

A channel is a virtual chat room or a group that enables users to send and receive messages in real-time. Channels allow developers to implement different types of chat messaging capabilities into their applications easily, such as private messaging, group chats, and chat rooms.

If you're new to the Social Plus Chat SDK, the following resources can help you get started:

* [Installation Guide](../../getting-started/installation-and-authentication/)
* [Authentication Guide](../core-concepts/session-state.md)

#### Channel Types

Messaging is a crucial feature for any chat application, and with Social Plus Chat SDK, developers can enable real-time communication between users within a chat channel with ease.

The Social Plus Chat SDK supports several channel types, each designed to match a particular use case for chat channels. Here's a table showing what features each channel type offers:

<table data-header-hidden><thead><tr><th width="150">Channel Type</th><th width="134">Discoverable by</th><th width="125">Message sending privileges</th><th width="121">Moderation access</th><th width="99">Channel Creation</th><th>Realtime Events</th></tr></thead><tbody><tr><td><strong>Channel Type</strong></td><td><strong>Discoverable by</strong></td><td><strong>Message sending privileges</strong></td><td><strong>Moderation access</strong></td><td><strong>Channel Creation</strong></td><td><strong>Realtime Events Retrieval</strong></td></tr><tr><td>Community</td><td>All users and admins</td><td>Joined members and admins</td><td>All Moderation tools</td><td>SDK, Console</td><td>Automatic</td></tr><tr><td>Private Community</td><td>Joined members and admins</td><td>Joined members and admins</td><td>All Moderation tools</td><td>SDK, Console</td><td>Automatic</td></tr><tr><td>Live</td><td>Joined members and admins</td><td>Joined members and admins</td><td>All Moderation tools</td><td>SDK, Console</td><td>Subscription needed</td></tr><tr><td>Broadcast</td><td>All users and admins</td><td>Admins</td><td>Admin Moderation tools</td><td><p>SDK,</p><p>Console</p></td><td>Subscription needed</td></tr><tr><td>Conversation</td><td>Joined members </td><td>Joined members </td><td>No Moderation tools</td><td>SDK</td><td>Automatic</td></tr></tbody></table>

#### Message Types

Moderation is an essential feature for building a community that encourages user participation and engagement. With Social Plus Chat SDK, developers can use the moderation feature to assign moderators and admins via a role-based permission system, filter out inappropriate content with automated spam filtering and URL whitelists, and manage user bans.

The Social Plus Chat SDK supports several message types, including:

Chat experience is more fun when you can express yourself! With Social Plus Chat SDK, developers can use the Reactions feature to allow users to react to messages using emojis, stickers, or thumbs up. This feature can help users express their emotions and opinions, making communication more engaging and interactive.

* Text Message
* Image Message
* File Message
* Audio Message
* Video Message
* Custom Message

In addition to these message types, the SDK also supports message reactions, which can be used to enable users to react to messages in a channel.

### Features

### [Channels](channels/)

Our channels enable developers to implement different types of chat messaging capabilities into their applications easily.

### [Messaging](messaging/)

This page highlights the steps you will need to follow to begin integrating chat messaging into your products.

### [Moderation](moderation/)

Moderation is an important feature for building a safe community that encourages user participation and engagement.

### [Reactions](messaging/message-reaction.md)

Interactions are more fun when you can express yourself! Let users react using emojis, stickers, or thumbs up to messages.‌

<figure><img src="../../.gitbook/assets/image (3) (1) (2).png" alt=""><figcaption></figcaption></figure>

