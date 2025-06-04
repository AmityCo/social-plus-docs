---
description: >-
  Here's an overview of how you can get started integrating comments into your
  applications
---

# Comments

Comment refers to a user-generated response or reaction to a specific piece of content, such as a post or content. Comments enable users to engage in conversations and express their thoughts, opinions, and emotions about the content they see. They provide a way for users to interact with each other and create a sense of community around the content. Commenting is an essential feature for social platforms as it encourages user engagement, helps create a more immersive experience for users, and can be used to generate insights into user behavior and preferences. In a Social Plus SDK product, the SDK provides the necessary tools and functionality for developers to integrate commenting into their apps or websites.&#x20;

Furthermore, a comment supports real-time events and Live Object features, for more information please refer to [live-objects-collections](../../core-concepts/live-objects-collections/ "mention") and [realtime-events](../../core-concepts/realtime-events/ "mention").

### Comment Reference Type <a href="#create-comment" id="create-comment"></a>

Incorporating comment reference types within your app enhances user engagement and promotes interaction, as it allows users to comment on both regular posts and content-specific posts. By differentiating between these two comment types, your app can provide a more organized and contextual commenting experience, catering to the diverse needs of your users and the content they interact with. Comment's `referenceType` can be:

1. **Post type comment:** A post type comment is designed for regular posts, such as text updates, photos, or videos shared by users. These comments are associated with the regular post and are displayed beneath it, facilitating conversation and interaction.
2. **Story type comment:** Similar to post-type comments, these comments are associated with each story, driving user conversation.
3. **Content type comment:** A content type comment, on the other hand, is intended for content-specific posts, such as articles, or other specialized content.&#x20;

### Comment Repository

The functionality of comments can be utilized through the Comment Repository, which offers methods for interacting with a data source that stores posts. This includes methods for querying comments, creating a new comment, updating an existing comment, or deleting a comment.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/cac39f58dca4faf3d7f9a52311017cd5#file-create_comment_repository-swift" %}
Initialize comment repository
{% endembed %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/4505a8a70c8d92ebc112e156d979acf7#file-amitycommentrepositoryinitialization-kt" %}
{% endtab %}

{% tab title="JavaScript" %}
```javascript
import { CommentRepository } from '@amityco/js-sdk';
```
{% endtab %}

{% tab title="TypeScript" %}
The functionality isn't currently supported by this SDK.
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/0175953fbd804e31dde252f26c3d8819#file-amitycommentrepoinitialization-dart" %}
{% endtab %}
{% endtabs %}

### Comment Description

| Name               | Data Type       | Description                                                     |
| ------------------ | --------------- | --------------------------------------------------------------- |
| `commentId`        | `String`        | ID of the comment                                               |
| `userId`           | `String`        | ID of the user who posted the comment                           |
| `parentID`         | `String`        | ID of a parent comment                                          |
| `refrenceId`       | `String`        | ID of a reference                                               |
| `referenceType`    | `String`        | Type of a reference                                             |
| `dataType`         | `String`        | Type of the comment                                             |
| `data`             | `Object`        | Body of the comment                                             |
| `metadata`         | `Object`        | Additional properties to support custom fields                  |
| `childrenNumber`   | `Number`        | Number of children comments                                     |
| `flagCount`        | `Integer`       | Number of users who has read the comment                        |
| `reactions`        | `Object`        | Mapping of reaction with reactionCounter                        |
| `reactionsCount`   | `Integer`       | Number of all reactions for the comment                         |
| `myReactions`      | `Array<String>` | List of my reactions to the comment                             |
| `isDeleted`        | `Boolean`       | Flag that determines if comment is deleted                      |
| `editedAt`         | `DateTime`      | Date/time when comment was edited                               |
| `createdAt`        | `DateTime`      | Date/time when comment was created                              |
| `updatedAt`        | `DateTime`      | Date/time when comment was updated or deleted                   |
| `childrenComments` | `String`        | Children comments                                               |
| `hashflag`         | `Object`        | Flag for checking internally if this comment is reported or not |
| `mentionees`       | `Array<String>` | User IDs of the mentioned users                                 |
