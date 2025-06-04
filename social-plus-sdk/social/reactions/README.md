---
description: Let users react to messages, posts, and comments, which are visible to others.
---

# Reactions

<figure><img src="../../../.gitbook/assets/image (110).png" alt=""><figcaption></figcaption></figure>

Reactions are the interactions that users can perform on messages, posts, or comments. The interactions can be anything such as like, dislike, love, etc. It's up to the client to determine the type of reactions. The SDK provides convenient functions to add, remove, and query reactions for any content. Currently, reactions are supported for Posts, Messages, and Comments.

### Reaction Reference Type <a href="#create-comment" id="create-comment"></a>

The Social Plus SDK provides two reference types for querying reactions: comment reference type and post reference type.

* **Comment Reference Type**: allows users to query reactions made to a specific comment. This is useful when users want to see how others have responded to a particular comment.
* **Post Reference Type:** allows users to query reactions made to a specific post. This is helpful when users want to see how others have engaged with a particular piece of post.
* **Story Reference Type:** allows users to query reactions made to a specific story. This is helpful when users want to see how others have reacted to a particular piece of story.

### Reaction Description

| Name                 | Data Type  | Description                              | Attributes                   |
| -------------------- | ---------- | ---------------------------------------- | ---------------------------- |
| `referenceId`        | `String`   | ID of a document                         |                              |
| `referenceType`      | `String`   | Type of document                         |                              |
| `reactionName`       | `String`   | Name of reaction                         | '`like`', '`love`' , '`wow`' |
| `reactionId`         | `String`   | ID of the reaction                       |                              |
| `reactorId`          | `String`   | ID of the reactor                        |                              |
| `reactorDisplayName` | `String`   | Display name of the reactor              |                              |
| `createdAt`          | `DateTime` | The date/time when a reaction is created |                              |
