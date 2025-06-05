# Post Impression

The Post Impression feature in our Social Plus SDK is a tool designed to collect valuable data regarding post interactions for analytics and reporting purposes. This feature empowers users to gain insights into how their content is performing and who is actively engaging with it. With this feature, users can mark specific posts as viewed and access information about impressions, reach, and the list of users who have viewed each post.

<Info>
Impressions represent the number of users who viewed the post, while reach represents the number of unique users who viewed the post. Please keep in mind that post-impression data won't be updated in real-time but rather almost in real-time.
</Info>

### Marking a post as viewed

The SDK provides an ability to mark any post as viewed by invoking `markAsViewed()` method within `post.analytics`, which will increase the impression and reach count of specific posts. Additionally, users can easily access the `impression` and `reach` counts directly from the `post` object within the SDK.

<Tabs>
  <Tab title="iOS">
    <CodeGroup>
      ```swift
      post.analytics.markAsViewed()
      ```
    </CodeGroup>
  </Tab>
  <Tab title="Android">
    <CodeGroup>
      ```kotlin
      post.analytics.markAsViewed()
      ```
    </CodeGroup>
  </Tab>
  <Tab title="TypeScript">
    <CodeGroup>
      ```typescript
      await post.analytics.markAsViewed()
      ```
    </CodeGroup>
  </Tab>
  <Tab title="Flutter">
    <CodeGroup>
      ```dart
      await post.analytics.markAsViewed();
      ```
    </CodeGroup>
  </Tab>
</Tabs>

### Query posts reached users

The `queryReachedUsers()` function within `UserRepository` provides the ability to query a list of unique users who have viewed the specific story.

This function requires two parameters: viewedType, and viewedId.

Here's an explanation of the function parameters:

* **viewedType**: Represents the type of content that has reached the users. In this case, it is type 'POST'.
* **viewedId**: Corresponds to the ID of the viewed content. In this case, it is a post.

<Tabs>
  <Tab title="iOS">
    <CodeGroup>
      ```swift
      let users = try await userRepository.queryReachedUsers(viewedType: .post, viewedId: postId)
      ```
    </CodeGroup>
  </Tab>
  <Tab title="Android">
    <CodeGroup>
      ```kotlin
      val users = userRepository.queryReachedUsers(ViewedType.POST, postId)
      ```
    </CodeGroup>
  </Tab>
  <Tab title="TypeScript">
    <CodeGroup>
      ```typescript
      const users = await userRepository.queryReachedUsers('POST', postId)
      ```
    </CodeGroup>
  </Tab>
  <Tab title="Flutter">
    <CodeGroup>
      ```dart
      final users = await userRepository.queryReachedUsers(ViewedType.post, postId);
      ```
    </CodeGroup>
  </Tab>
</Tabs>