# Poll

The Social Plus SDK encompasses comprehensive support for polls, offering developers an effortless way to incorporate polls into their social applications. Polls enable users to create and participate in a diverse range of topics, sparking targeted engagement and conversations among users.

To integrate poll functionality, developers can utilize the poll features offered by the Social Plus SDK in their applications. Polls can be tailored to meet specific needs, including options for single or multiple-choice polls, setting poll expiration dates, and more. Users can then participate in the poll by choosing their preferred option. At present, the Social Plus SDK only supports the integration of polls within posts, please refer to [#create-poll-post](../social/posts/create-post/poll-post.md#create-poll-post "mention"), [#poll-post](../social/posts/viewing-post-content.md#poll-post "mention").

## Create Poll

As demonstrated in the code sample below, here's a way to create a poll in the poll post.

Polls can be created with the following settable controls:

* `question` - A question that can be up to 500 characters long.
* `answer` - A set of two to ten answers. Each answer can be up to 200 characters long.
* `answerType` - Indicates whether the survey allows multiple choices. The available options are `Single` (default) and `Multiple`.
* `timeToClosePoll` - A time window limiting how long the poll will be open. By default, the `setTimeToClosePoll` value is set to 30 days if no value has been set for it.

<Tabs>
  <Tab title="iOS">
    <CodeGroup>
      <CodeGroupItem>
```swift
let pollRepository = AmityPollRepository(client: client)
let createPollRequestModel = AmityPollCreateRequestModel()
createPollRequestModel.question = "What's your favorite color?"
createPollRequestModel.answers = ["Red", "Blue", "Green"]
createPollRequestModel.answerType = .single
createPollRequestModel.timeToClosePoll = 86400 // 24 hours in seconds

pollRepository.createPoll(with: createPollRequestModel) { result in
    switch result {
    case .success(let poll):
        print("Poll created successfully")
    case .failure(let error):
        print("Failed to create poll: \(error)")
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
val pollRepository = AmityPollRepository(client)
val createPollRequestModel = AmityPollCreateRequestModel()
createPollRequestModel.question = "What's your favorite color?"
createPollRequestModel.answers = listOf("Red", "Blue", "Green")
createPollRequestModel.answerType = AmityPollAnswerType.SINGLE
createPollRequestModel.timeToClosePoll = 86400 // 24 hours in seconds

pollRepository.createPoll(createPollRequestModel).subscribe(
    { poll ->
        // Poll created successfully
    },
    { error ->
        // Handle error
    }
)
```
      </CodeGroupItem>
    </CodeGroup>
  </Tab>
  <Tab title="JavaScript">
    <CodeGroup>
      <CodeGroupItem>
```javascript
const pollRepository = new AmityPollRepository(client);
const createPollRequestModel = {
    question: "What's your favorite color?",
    answers: ["Red", "Blue", "Green"],
    answerType: "single",
    timeToClosePoll: 86400 // 24 hours in seconds
};

try {
    const poll = await pollRepository.createPoll(createPollRequestModel);
    console.log("Poll created successfully");
} catch (error) {
    console.error("Failed to create poll:", error);
}
```
      </CodeGroupItem>
    </CodeGroup>
  </Tab>
  <Tab title="TypeScript">
    <CodeGroup>
      <CodeGroupItem>
```typescript
const pollRepository = new AmityPollRepository(client);
const createPollRequestModel: AmityPollCreateRequestModel = {
    question: "What's your favorite color?",
    answers: ["Red", "Blue", "Green"],
    answerType: "single",
    timeToClosePoll: 86400 // 24 hours in seconds
};

try {
    const poll = await pollRepository.createPoll(createPollRequestModel);
    console.log("Poll created successfully");
} catch (error) {
    console.error("Failed to create poll:", error);
}
```
      </CodeGroupItem>
    </CodeGroup>
  </Tab>
  <Tab title="Flutter">
    <CodeGroup>
      <CodeGroupItem>
```dart
final pollRepository = AmityPollRepository(client);
final createPollRequestModel = AmityPollCreateRequestModel(
    question: "What's your favorite color?",
    answers: ["Red", "Blue", "Green"],
    answerType: AmityPollAnswerType.single,
    timeToClosePoll: 86400 // 24 hours in seconds
);

try {
    final poll = await pollRepository.createPoll(createPollRequestModel);
    print("Poll created successfully");
} catch (error) {
    print("Failed to create poll: $error");
}
```
      </CodeGroupItem>
    </CodeGroup>
  </Tab>
</Tabs>

## Vote Poll

This function enables you to cast a single vote and the vote cannot be revoked. If the poll type is multiple, you have the option to select multiple choices.

Here's an explanation of the method's parameters:

* `pollId`: This is a required parameter of type `String`, which represents the ID of the poll that the user wants to vote on.
* `answerIds`: This is a required parameter of the type `Array<String>`, which represents an array of IDs of the answer options that the user wants to vote for. Users can select one or multiple answers depending on the poll's configuration.

<Tabs>
  <Tab title="iOS">
    <CodeGroup>
      <CodeGroupItem>
```swift
let pollRepository = AmityPollRepository(client: client)
pollRepository.votePoll(pollId: "pollId", answerIds: ["answerId1", "answerId2"]) { result in
    switch result {
    case .success:
        print("Vote submitted successfully")
    case .failure(let error):
        print("Failed to submit vote: \(error)")
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
val pollRepository = AmityPollRepository(client)
pollRepository.votePoll(pollId = "pollId", answerIds = listOf("answerId1", "answerId2"))
    .subscribe(
        {
            // Vote submitted successfully
        },
        { error ->
            // Handle error
        }
    )
```
      </CodeGroupItem>
    </CodeGroup>
  </Tab>
  <Tab title="JavaScript">
    <CodeGroup>
      <CodeGroupItem>
```javascript
const pollRepository = new AmityPollRepository(client);

try {
    await pollRepository.votePoll("pollId", ["answerId1", "answerId2"]);
    console.log("Vote submitted successfully");
} catch (error) {
    console.error("Failed to submit vote:", error);
}
```
      </CodeGroupItem>
    </CodeGroup>
  </Tab>
  <Tab title="TypeScript">
    <CodeGroup>
      <CodeGroupItem>
```typescript
const pollRepository = new AmityPollRepository(client);

try {
    await pollRepository.votePoll("pollId", ["answerId1", "answerId2"]);
    console.log("Vote submitted successfully");
} catch (error) {
    console.error("Failed to submit vote:", error);
}
```
      </CodeGroupItem>
    </CodeGroup>
  </Tab>
  <Tab title="Flutter">
    <CodeGroup>
      <CodeGroupItem>
```dart
final pollRepository = AmityPollRepository(client);

try {
    await pollRepository.votePoll(
        pollId: "pollId",
        answerIds: ["answerId1", "answerId2"]
    );
    print("Vote submitted successfully");
} catch (error) {
    print("Failed to submit vote: $error");
}
```
      </CodeGroupItem>
    </CodeGroup>
  </Tab>
</Tabs>

## Close Poll

The ability to close a poll is restricted exclusively to individuals who have ownership permissions, such as the creator of the poll or an administrator. It is important to note that a poll can only be closed before its designated closing time.

Here's an explanation of the method's parameters:

* `pollId`: This is a required parameter of type `String`, which represents the ID of the poll that the user wants to close.

<Tabs>
  <Tab title="iOS">
    <CodeGroup>
      <CodeGroupItem>
```swift
let pollRepository = AmityPollRepository(client: client)
pollRepository.closePoll(pollId: "pollId") { result in
    switch result {
    case .success:
        print("Poll closed successfully")
    case .failure(let error):
        print("Failed to close poll: \(error)")
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
val pollRepository = AmityPollRepository(client)
pollRepository.closePoll(pollId = "pollId")
    .subscribe(
        {
            // Poll closed successfully
        },
        { error ->
            // Handle error
        }
    )
```
      </CodeGroupItem>
    </CodeGroup>
  </Tab>
  <Tab title="JavaScript">
    <CodeGroup>
      <CodeGroupItem>
```javascript
closePoll = async (pollId: string) => Promise<any>
```
      </CodeGroupItem>
    </CodeGroup>
  </Tab>
  <Tab title="TypeScript">
    <CodeGroup>
      <CodeGroupItem>
```typescript
const pollRepository = new AmityPollRepository(client);

try {
    await pollRepository.closePoll("pollId");
    console.log("Poll closed successfully");
} catch (error) {
    console.error("Failed to close poll:", error);
}
```
      </CodeGroupItem>
    </CodeGroup>
  </Tab>
  <Tab title="Flutter">
    <CodeGroup>
      <CodeGroupItem>
```dart
final pollRepository = AmityPollRepository(client);

try {
    await pollRepository.closePoll(pollId: "pollId");
    print("Poll closed successfully");
} catch (error) {
    print("Failed to close poll: $error");
}
```
      </CodeGroupItem>
    </CodeGroup>
  </Tab>
</Tabs>

## Delete Poll

The deletion of a poll is limited exclusively to individuals who possess ownership permissions, such as the creator of the poll or an administrator.

Here's an explanation of the method's parameters:

* `pollId`: This is a required parameter of the type `String`, which represents the ID of the poll that the user wants to delete.

<Tabs>
  <Tab title="iOS">
    <CodeGroup>
      <CodeGroupItem>
```swift
let pollRepository = AmityPollRepository(client: client)
pollRepository.deletePoll(pollId: "pollId") { result in
    switch result {
    case .success:
        print("Poll deleted successfully")
    case .failure(let error):
        print("Failed to delete poll: \(error)")
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
val pollRepository = AmityPollRepository(client)
pollRepository.deletePoll(pollId = "pollId")
    .subscribe(
        {
            // Poll deleted successfully
        },
        { error ->
            // Handle error
        }
    )
```
      </CodeGroupItem>
    </CodeGroup>
  </Tab>
  <Tab title="JavaScript">
Supported ✅ (Please wait while we prepare a real example!)
  </Tab>
  <Tab title="TypeScript">
    <CodeGroup>
      <CodeGroupItem>
```typescript
const pollRepository = new AmityPollRepository(client);

try {
    await pollRepository.deletePoll("pollId");
    console.log("Poll deleted successfully");
} catch (error) {
    console.error("Failed to delete poll:", error);
}
```
      </CodeGroupItem>
    </CodeGroup>
  </Tab>
  <Tab title="Flutter">
    <CodeGroup>
      <CodeGroupItem>
```dart
final pollRepository = AmityPollRepository(client);

try {
    await pollRepository.deletePoll(pollId: "pollId");
    print("Poll deleted successfully");
} catch (error) {
    print("Failed to delete poll: $error");
}
```
      </CodeGroupItem>
    </CodeGroup>
  </Tab>
</Tabs>