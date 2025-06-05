# Query Comment

The ability to query comments and their replies is essential for creating a robust and user-friendly commenting experience. By using the `getComments()` method and passing in the appropriate parameters, you can retrieve the comments and replies that are most relevant to your users.

### **Comment Replies**

The query returns a LiveCollection of all matching comments available. To retrieve replies to a specific comment, you can pass the `commentId` as the `parentId`. If you want to retrieve parent-level comments, pass `parentId = null`. If you omit the `parentId`, you'll receive all comments on all levels.

### **Deletion Filter**

You can also use the `includeDeleted()` method to query for deleted comments and their replies. By passing `true` or `false` to this method, you can include or exclude deleted comments from the results.

<Info>
Note that if you use the `includeDeleted()` method, you don't need to check the `isDeleted()` method in the `AmityComment` object for deleted comments.
</Info>

The `referenceType` parameter specifies where the comment is made and helps filter the comments based on the type of content. Possible values include:

* **`post`**: Comments on posts.
* **`story`**: Comments on stories.
* **`content`**: Comments on other types of content (e.g., images, videos, etc.).

---

### How to Query Comments

To query comments, provide the `referenceType` and `referenceId`. You can also include additional filters like `parentId`, `includeDeleted`, and `orderBy` to control the results.

To query comments for a post (including replies and excluding deleted comments):

<Tabs>
  <Tab title="iOS">
    <CodeGroup>
      <CodeGroupItem>
```swift
let comments = AmityCommentQuery()
    .referenceId("postId")
    .referenceType("post")
    .parentId(nil)
    .includeDeleted(false)
    .build()
```
      </CodeGroupItem>
    </CodeGroup>
  </Tab>

  <Tab title="Android">
    <CodeGroup>
      <CodeGroupItem>
```java
CommentQuery query = new CommentQuery.Builder()
    .referenceId("postId")
    .referenceType("post")
    .parentId(null)
    .includeDeleted(false)
    .build();
```
      </CodeGroupItem>
    </CodeGroup>
  </Tab>

  <Tab title="JavaScript">
    <CodeGroup>
      <CodeGroupItem>
```javascript
const comments = await client.getComments({
    referenceId: 'postId',
    referenceType: 'post',
    parentId: null,
    includeDeleted: false
});
```
      </CodeGroupItem>
    </CodeGroup>

### Pagination

When querying comments, you cannot set `limit`, `skip`, `after`, `first`, `before`, and `last` parameters. By default, the number of items in each page is 20. To handle pagination to load more comments, refer to Pagination in Live Collections.
  </Tab>

  <Tab title="TypeScript">
    <CodeGroup>
      <CodeGroupItem>
```typescript
const comments = await client.getComments({
    referenceId: 'postId',
    referenceType: 'post',
    parentId: null,
    includeDeleted: false
});
```
      </CodeGroupItem>
    </CodeGroup>
  </Tab>

  <Tab title="Flutter">
    <CodeGroup>
      <CodeGroupItem>
```dart
final comments = AmityCommentQuery()
    .referenceId("postId")
    .referenceType("post")
    .parentId(null)
    .includeDeleted(false)
    .build();
```
      </CodeGroupItem>
    </CodeGroup>
  </Tab>
</Tabs>

<Info>
Refer to [#create-comment](./#create-comment "mention") for a more detailed explanation of the `referenceType` parameter.
</Info>

## Query Comments with Images

To query for image comments only, you can use the `dataTypes` parameter and pass the value `TEXT`, `IMAGE`, or both. There are two options for the `dataTypes` parameter: `any` and `exact`.

* `any` - When you use the `any` option, the retrieved comments will include any comment that contains at least one of the specified data types. For example, if you pass `[image, text]`, the retrieved comments may contain only image content, only text content, or both image and text content.
* `exact` - On the other hand, when you use the `exact` option, the retrieved comments will include only comments that contain all of the specified data types. For example, if you pass `[image, text]`, the retrieved comments must contain both image and text content. If you pass `[image]`, the retrieved comments must contain only image content.

To query for comments containing only image content:

<Tabs>
  <Tab title="iOS">
Using exact filer parameter:

<CodeGroup>
  <CodeGroupItem>
```swift
let comments = AmityCommentQuery()
    .referenceId("postId")
    .referenceType("post")
    .dataTypes([.image], filter: .exact)
    .build()
```
  </CodeGroupItem>
</CodeGroup>

Using any filter parameter:

<CodeGroup>
  <CodeGroupItem>
```swift
let comments = AmityCommentQuery()
    .referenceId("postId")
    .referenceType("post")
    .dataTypes([.image, .text], filter: .any)
    .build()
```
  </CodeGroupItem>
</CodeGroup>
  </Tab>

  <Tab title="Android">
    <CodeGroup>
      <CodeGroupItem>
```java
CommentQuery query = new CommentQuery.Builder()
    .referenceId("postId")
    .referenceType("post")
    .dataTypes(Arrays.asList(DataType.IMAGE), FilterType.EXACT)
    .build();
```
      </CodeGroupItem>
    </CodeGroup>
  </Tab>

  <Tab title="TypeScript">
    <CodeGroup>
      <CodeGroupItem>
```typescript
const comments = await client.getComments({
    referenceId: 'postId',
    referenceType: 'post',
    dataTypes: ['image'],
    filter: 'exact'
});
```
      </CodeGroupItem>
    </CodeGroup>
  </Tab>

  <Tab title="Flutter">
The functionality isn't currently supported by this SDK.
  </Tab>
</Tabs>

_Refer to the following_ [_Limitations_](create-comment.md#limitations) _on the use of images in comments._