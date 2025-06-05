---
description: "Here's an overview of posts and how you can get started with integrating them into your applications"
---

# Posts

A post can be defined as a piece of content created and shared by a user within a network or community. The post can include various types of information such as text, images, videos, links, or other multimedia elements. The SDK provides the necessary tools and functionality for users to create, view, and interact with posts in a social feed. Posts can be displayed in chronological order and can be customized and configured using various settings and options provided by the SDK. The purpose of a post in a product context is to allow users to share information, express thoughts, or connect with others within a social network or community using the SDK.

Social Plus supports a wide range of post types, each with its own unique set of features and capabilities. The types of posts that you can create in Social Plus include text, image, video, file, live stream, poll, and custom posts. Furthermore, a post supports real-time events and Live Object features, for more information please refer to [live-objects-collections](../../core-concepts/live-objects-collections/) and [realtime-events](../../core-concepts/realtime-events/)

### Post Structure

The post structure is a parent-child relationship, with the parent post serving as a container for text data, for other post types such as images or videos, while each image or video is treated as a separate child post. To illustrate this, let's take the example of an image post with two images. In this case, there would be one parent post serving as a text container, and two child posts, each containing one of the images.

In addition to enabling users to create more dynamic and engaging content, both parent and child posts also support reactions and comments. This means that users can interact with not only the parent post but also with each child post, providing a more comprehensive and engaging way to engage with content.

### Post Repository

The functionality of posts can be utilized through the Post Repository, which offers methods for interacting with a data source that stores posts. This includes methods for obtaining a specific post, creating a new post, updating an existing post, or deleting a post.

<Tabs>
  <Tab title="iOS">
    ```
    
    ```
  </Tab>
  <Tab title="Android">
    ```
    
    ```
  </Tab>
  <Tab title="JavaScript">
    ```javascript
    import { PostRepository } from '@amityco/js-sdk';
    ```
  </Tab>
  <Tab title="TypeScript">
    ```
    
    ```
  </Tab>
  <Tab title="Flutter">
    Supported ✅ (Please wait while we prepare a real example\!)
  </Tab>
</Tabs>

### Post Description

| Name                 | Data Type             | Description                                                                                             |
| -------------------- | --------------------- | ------------------------------------------------------------------------------------------------------- |
| `postId`             | `String`              | ID of the post                                                                                          |
| `parentPostId`       | `String`              | ID of the parent post, this can be null if the post is a parent post.                                   |
| `postedUserId`       | `String`              | ID of the user who posted                                                                               |
| `sharedUserId`       | `String`              | ID of the user who shared the post                                                                      |
| `SharedCount`        | `Integer`             | Number of times the post is shared                                                                      |
| `targetID`           | `String`              | ID of the target                                                                                        |
| `targetType`         | `String`              | Type of target                                                                                          |
| `dataType`           | `String`              | Data type of post                                                                                       |
| `data`               | `Object`              | Data of the post                                                                                        |
| `metadata`           | `Object`              | Metadata of the post                                                                                    |
| `flagCount`          | `Integer`             | Number of times that the post is flagged                                                                |
| `editedAt`           | `Date`                | Date/time the post was edited                                                                           |
| `createdAt`          | `Date`                | Date/time the post was created                                                                          |
| `updatedAt`          | `Date`                | Date/time the post was updated                                                                          |
| `reactions`          | `Object`              | Information about the post reactions                                                                    |
| `reactionsCount`     | `Integer`             | Number of reactions to the post                                                                         |
| `myReactions`        | `Array<String>`       | Reactions to the post                                                                                   |
| `commentsCount`      | `Integer`             | Number of comments to the post                                                                          |
| `comments`           | `Array<AmityComment>` | The first three comments of the post for previewing purpose                                             |
| `childrenPosts`      | `Object`              | Children posts                                                                                          |
| `isDeleted`          | `Boolean`             | Flag that indicates if the post is deleted. True means post is already deleted.                         |
| `hasFlaggedComment`  | `Boolean`             | Flag that indicates if the post has flagged comments. True means it has.                                |
| `hasFlaggedChildren` | `Boolean`             | Flag that indicates if the post has flagged children. True means it has.                                |
| `tags`               | `Array<String>`       | Arbitrary strings that can be used for defining and querying for the posts in community and user feeds. |
| `feedId`             | `String`              | ID of the post's feed                                                                                   |