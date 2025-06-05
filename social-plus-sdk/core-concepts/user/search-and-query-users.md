# Search and Query Users

### Search User

Query for users by their display name, receiving a collection of `AmityUser` matching your search. It requires two parameters: the display name you're searching for, and a 'sort option' from the `AmityUserSortOption` enum.  If no keyword is supplied, the list of users will be organized alphabetically by display name.&#x20;

Users also have the option to sort by `lastCreated`, `firstCreated`, or `displayName`. When a keyword is provided, the list will be arranged based on search rank.  The `displayName` sorting option will be specified by default if it isn't specified.

With the `displayName` sorting option, users are sorted alphabetically by their display names using ICU collation for the English locale. This means that special characters such as **Ä** are treated as variants of **A**. For example, a sorted list might appear as:\
`adam, Älex, Alice, Arthur, charlie, Kristen`.

When providing a search keyword, the API performs an exact-match lookup for special characters.

* For instance, if you search for **"Äli"**, only users whose display name contains the **"Äli"** characters (e.g., **"Älise"**) will be returned.
* Conversely, searching for **"Alice"** will not return **"Älice"**.

<Note>
- The search keyword must be **at least 3 characters long**.
- Deleted users are excluded from the results
</Note>

<Tabs>
<Tab title="iOS">
<CodeGroup>
```swift
AmityUserRepository().searchUser(byDisplayName: "Brian").query()
```
</CodeGroup>
Search users by display name
</Tab>

<Tab title="Android">
<CodeGroup>
```kotlin
val userRepository = AmityUserRepository(client)
val userCollection = userRepository.searchUserByDisplayName("Brian").build().query()
```
</CodeGroup>

The code above will provide you with the list of users which matches with display name "Brian".
</Tab>

<Tab title="JavaScript">
```javascript
userRepo.searchUserByDisplayName('Test User 1')
```

The above example searches for all users whose display names _start with_ "Test User 1".&#x20;
</Tab>

<Tab title="TypeScript">
The `queryUsers` provides a way to search for users by their display name.

<CodeGroup>
```typescript
const { data: users } = await client.queryUsers({
  displayName: 'Test User 1'
});
```
</CodeGroup>
</Tab>

<Tab title="Flutter">
<CodeGroup>
```dart
final AmityUserRepository userRepository = AmityUserRepository();
PagingController<String, AmityUser> userCollection = userRepository.searchUserByDisplayName("Brian").getPagingController();
```
</CodeGroup>
</Tab>
</Tabs>

### Query Users

Query for users to receive a collection of `AmityUser` based on a single parameter: a 'sort option' from the `AmityUserSortOption` enum. Sort the list by options such as `displayName`, `firstCreated`, or `lastCreated`. The `displayName` sort option will be specified by default if it isn't specified.

With the `displayName` sorting option, users are sorted alphabetically by their display names using ICU collation for the English locale. This means that special characters such as **Ä** are treated as variants of **A**. For example, a sorted list might appear as:\
`adam, Älex, Alice, Arthur, charlie, Kristen`.

<Note>
Deleted users are excluded from the results
</Note>

<Tabs>
<Tab title="iOS">
<CodeGroup>
```swift
AmityUserRepository().getUsers().query()
```
</CodeGroup>
Query users
</Tab>

<Tab title="Android">
<CodeGroup>
```kotlin
val userRepository = AmityUserRepository(client)
val userCollection = userRepository.getUsers().build().query()
```
</CodeGroup>
</Tab>

<Tab title="JavaScript">
```typescript
const liveUserCollection = UserRepository.queryUsers({
    keyword?: string, 
    filter?: 'all' | 'flagged', 
    sortBy?: 'lastCreated' | 'firstCreated' | 'displayName'
})

// filter if flagCount is > 0
// lastCreated: sort: createdAt desc 
// firstCreated: sort: createdAt asc 
// displayName: sort: alphanumerical asc

liveUserCollection.on("dataUpdated", models => {
  models.map(model => console.log(model.userId))
})
```
</Tab>

<Tab title="TypeScript">
<CodeGroup>
```typescript
const { data: users } = await client.queryUsers();
```
</CodeGroup>

If you wish to observe for changes to a collection of users, you can use `liveUsers`

<CodeGroup>
```typescript
const subscription = client.liveUsers({
  sortBy: 'displayName'
}).subscribe(users => {
  console.log('Users updated:', users);
});
```
</CodeGroup>
</Tab>

<Tab title="Flutter">
<CodeGroup>
```dart
final AmityUserRepository userRepository = AmityUserRepository();
PagingController<String, AmityUser> userCollection = userRepository.getUsers().getPagingController();
```
</CodeGroup>
</Tab>
</Tabs>