# Get Latest Comment

The Social Plus SDK offers the `getLatestComment` method, allowing you to fetch the most recent comment by a reference within your application. Integrating this feature enhances the user experience by keeping them informed about the latest interactions among users.

Using the `getLatestComment` method is straightforward: simply implement it to retrieve the latest comment by a reference, streamlining the process of accessing up-to-date information. Furthermore, the method returns a [Live Object](../../core-concepts/live-objects-collections/) that you can observe for real-time updates once [realtime-events](../../core-concepts/realtime-events/) are subscribed, ensuring your app stays current with the latest comments and fostering a more interactive environment.

<Tabs>
  <Tab title="iOS">
    <CodeGroup>
      ```swift
      SocialPlus.shared.getLatestComment(reference: "post_123") { result in
          switch result {
          case .success(let comment):
              print("Latest comment: \(comment)")
          case .failure(let error):
              print("Error: \(error)")
          }
      }
      ```
    </CodeGroup>
  </Tab>
  <Tab title="Android">
    <CodeGroup>
      ```kotlin
      SocialPlus.getInstance().getLatestComment("post_123") { result ->
          when (result) {
              is Success -> {
                  val comment = result.data
                  println("Latest comment: $comment")
              }
              is Error -> {
                  println("Error: ${result.exception}")
              }
          }
      }
      ```
    </CodeGroup>
  </Tab>
  <Tab title="TypeScript">
    Unsupported ❌
  </Tab>
  <Tab title="Flutter">
    Supported ✅ (Please wait while we prepare a real example!)
  </Tab>
</Tabs>

<Info>
  Refer to [Comment reference type](./#comment-description) for a more detailed explanation of the reference type parameter.
</Info>