# Poll Post

Prior to creating a poll post, it is crucial to create the poll that will be included in the post data to ensure that the necessary information is accessible and can be linked to the post. This requires creating the poll first, to obtain the data that will be used in creating the poll post. For more information about polls including vote, close, or delete a poll, please refer to the page - [poll.md](../../../core-concepts/poll.md "mention").

* `text`: This is a required parameter of type `String`, which represents the text content of the new post. You can pass in any text you want to include in the post, up to a maximum length of 20,000 characters.
* `pollId`: The ID of the created poll to include in a post.
* `targetType` - Type of the target, either a particular community or a user feed.
* `tags` - Arbitrary strings that can be used for defining and querying for the posts (Except Flutter).
* `metaData` - Additional properties to support custom fields.

As demonstrated in the code sample below, here's a way to create a poll and poll post.

<Tabs>
  <Tab title="iOS">
    <CodeGroup>
      <CodeGroupItem>
```swift
// Create poll
let pollRepository = AmityPollRepository(client: client)
let pollCreationBuilder = AmityPollCreationBuilder()
    .setQuestion("What is your favorite color?")
    .setAnswers(["Red", "Blue", "Green"])
    .setTimeToClosePoll(300)
    .setMultipleVoting(false)
    
pollRepository.createPoll(with: pollCreationBuilder) { result in
    switch result {
    case .success(let poll):
        print("Poll created with id: \(poll.pollId)")
    case .failure(let error):
        print("Error creating poll: \(error)")
    }
}

// Create poll post
let postRepository = AmityPostRepository(client: client)
let postCreateBuilder = AmityPostCreateBuilder()
    .setText("Please vote in my poll!")
    .setPollId(pollId)
    .setTargetType(.community)
    .setTargetId(communityId)

postRepository.createPost(with: postCreateBuilder) { result in
    switch result {
    case .success(let post):
        print("Post created with id: \(post.postId)")
    case .failure(let error):
        print("Error creating post: \(error)")
    }
}
```
      </CodeGroupItem>
    </CodeGroup>
  </Tab>
  <Tab title="Android">
    <CodeGroup>
      <CodeGroupItem>
```kotlin
// Create poll
val pollRepository = AmityPollRepository(client)
val pollCreationBuilder = AmityPoll.PollCreateBuilder()
    .question("What is your favorite color?")
    .answers(listOf("Red", "Blue", "Green"))
    .timeToClosePoll(300)
    .isMultipleVoting(false)

pollRepository.createPoll(pollCreationBuilder).subscribe { poll ->
    // Poll created successfully
    val pollId = poll.getPollId()
    
    // Create poll post
    val postRepository = AmityPostRepository(client)
    val postCreateBuilder = AmityPost.PostCreateBuilder()
        .setText("Please vote in my poll!")
        .setPollId(pollId)
        .setTargetType(AmityPost.TargetType.COMMUNITY)
        .setTargetId(communityId)
    
    postRepository.createPost(postCreateBuilder).subscribe { post ->
        // Post created successfully
    }
}
```
      </CodeGroupItem>
    </CodeGroup>
  </Tab>
  <Tab title="JavaScript">
    <CodeGroup>
      <CodeGroupItem>
```javascript
// Create poll
const pollRepository = new AmityPollRepository(client);
const pollCreationBuilder = {
    question: "What is your favorite color?",
    answers: ["Red", "Blue", "Green"],
    timeToClosePoll: 300,
    multipleVoting: false
};

pollRepository.createPoll(pollCreationBuilder).then(poll => {
    // Poll created successfully
    const pollId = poll.pollId;
    
    // Create poll post
    const postRepository = new AmityPostRepository(client);
    const postCreateBuilder = {
        text: "Please vote in my poll!",
        pollId: pollId,
        targetType: "community",
        targetId: communityId
    };
    
    return postRepository.createPost(postCreateBuilder);
}).then(post => {
    // Post created successfully
}).catch(error => {
    // Handle error
});
```
      </CodeGroupItem>
    </CodeGroup>
  </Tab>
  <Tab title="TypeScript">
    <CodeGroup>
      <CodeGroupItem>
```typescript
// Create poll
const pollRepository = new AmityPollRepository(client);
const pollCreationBuilder = {
    question: "What is your favorite color?",
    answers: ["Red", "Blue", "Green"],
    timeToClosePoll: 300,
    multipleVoting: false
};

pollRepository.createPoll(pollCreationBuilder).then(poll => {
    // Poll created successfully
    const pollId = poll.pollId;
    
    // Create poll post
    const postRepository = new AmityPostRepository(client);
    const postCreateBuilder = {
        text: "Please vote in my poll!",
        pollId: pollId,
        targetType: "community",
        targetId: communityId
    };
    
    return postRepository.createPost(postCreateBuilder);
}).then(post => {
    // Post created successfully
}).catch(error => {
    // Handle error
});
```
      </CodeGroupItem>
    </CodeGroup>
  </Tab>
  <Tab title="Flutter">
    <CodeGroup>
      <CodeGroupItem>
```dart
// Create poll
final pollRepository = AmityPollRepository(client: client);
final pollCreationBuilder = AmityPollCreationBuilder()
    ..question = "What is your favorite color?"
    ..answers = ["Red", "Blue", "Green"]
    ..timeToClosePoll = 300
    ..isMultipleVoting = false;

pollRepository.createPoll(pollCreationBuilder).then((poll) {
    // Poll created successfully
    final pollId = poll.pollId;
    
    // Create poll post
    final postRepository = AmityPostRepository(client: client);
    final postCreateBuilder = AmityPostCreateBuilder()
        ..text = "Please vote in my poll!"
        ..pollId = pollId
        ..targetType = AmityPostTargetType.COMMUNITY
        ..targetId = communityId;
    
    return postRepository.createPost(postCreateBuilder);
}).then((post) {
    // Post created successfully
}).catchError((error) {
    // Handle error
});
```
      </CodeGroupItem>
    </CodeGroup>
  </Tab>
</Tabs>