# Query Community Members

### Retrieve a list of community members

To retrieve a list of community members, users can call the relevant method and provide the desired membership options and sorting parameters. For example, they may choose to sort the list of members by name or by date created, or they may specify certain membership options, such as only retrieving members who are not banned. The result of the method will always return as [Live collection](../../core-concepts/live-objects-collections/).

To query community members with certain criteria, the following parameters are used:

* `membershipOptions`:  allows users to filter the results based on the membership status of community members.  Passing an empty option or not passing an option set for `membershipOptions` parameter will default to `member`.
  * `member` - will filter out all banned members and only include unbanned members.
  * `ban` - will only include banned members in the results.
* `roles`:  allows users to query for members with default moderator roles by using "_channel-moderator_" or "_community-moderator_" as the value. At this moment, we do not have a way to query for member-only roles. For custom roles assigned to members, users can pass in `roleId` of the custom role to filter members by this role.
* `includeDeleted`: A parameter accepting a boolean value.
  * `true` -> include a member whose user has been deleted
  * `false` -> exclude member whose user has been deleted

<Info>
Community member count value is based on all members in the community including the members whose user has been deleted.
</Info>

* `sortBy`: allows users to specify the sorting method for the returned collection. The possible values include `displayName`, `firstCreated`, `lastCreated`. The `firstCreated` sort option will be specified by default if it isn't specified. When a keyword is provided, leading to a list sorted by search rank.

<Info>
To query community banned members, only the 'Admin' role is currently allowed, while 'Moderators' and 'Users' are not allowed to query community banned members.
</Info>

<Info>
Please note that you can only assign custom roles to a member in a community via the SDK. This feature is **not** yet available in the Social Plus Console.

If you assign a custom role to a user via the Social Plus console, the role will only be applied at the user level and not at the community level, and if you try to query for a member with this custom role, no results will be returned.
</Info>

<Tabs>
<Tab title="iOS">
<CodeGroup>
```swift
// Query members in a community
let options = CommunityMembershipOptions()
options.insert(.member)
community.getMembers(membershipOptions: options) { result in
    switch result {
    case .success(let members):
        print("Successfully retrieved members: \(members)")
    case .failure(let error):
        print("Failed to retrieve members: \(error)")
    }
}
```
</CodeGroup>
</Tab>

<Tab title="Android">
<CodeGroup>
```kotlin
// Get members in a community
val options = CommunityMembershipOptions()
options.add(CommunityMembershipOption.MEMBER)
community.getMembers(options) { result ->
    when (result) {
        is Success -> {
            val members = result.value
            // Handle success
        }
        is Failure -> {
            val error = result.error
            // Handle error
        }
    }
}
```
</CodeGroup>

Passing an empty option set for `membershipOptions` parameter will default to `.member`.
</Tab>

<Tab title="JavaScript">
Below is the sample code to get a list of community members. This method will return a `LiveCollection` instance.

<CodeGroup>
```javascript
// Get members in a community
const members = await community.getMembers({
  membershipOptions: ['member'],
  roles: ['community-moderator'],
  includeDeleted: false,
  sortBy: 'firstCreated'
});
```
</CodeGroup>
</Tab>

<Tab title="TypeScript">
<CodeGroup>
```typescript
// Query members in a community
const members = await community.getMembers({
  membershipOptions: ['member'],
  roles: ['community-moderator'],
  includeDeleted: false,
  sortBy: 'firstCreated'
});
```
</CodeGroup>
</Tab>

<Tab title="Flutter">
<CodeGroup>
```dart
// Get members in a community
final options = CommunityMembershipOptions()..add(CommunityMembershipOption.member);
try {
  final members = await community.getMembers(membershipOptions: options);
  // Handle success
} catch (error) {
  // Handle error
}
```
</CodeGroup>
</Tab>
</Tabs>

### Search for community members

To search for community members, users can call the relevant method and provide the desired keyword, roles, and membership options parameters. For example, they may specify certain membership options, such as only retrieving members who are not banned. The result of the method will always return as [Live collection](../../core-concepts/live-objects-collections/).

If no keyword is supplied, the list of users for the specified community will be sorted by the date they joined.

To search for community members with certain criteria, the following parameters are used:

* `keyword`: allows users to specify the keyword to search for. The result contains members with either matching `displayName` or `userId`
* `membershipOptions`:  allows users to filter the results based on the membership status of community members.  Passing an empty option or not passing and option set for `membershipOptions` parameter will default to `member`.
  * `member` - will filter out all banned members and only include unbanned members.
  * `ban` - will only include banned members in the results.
* `roles`:  allows users to query for members with default moderator roles by using "_channel-moderator_" or "_community-moderator_" as the value. At this moment, we do not have a way to query for member-only roles. For custom roles assigned to members, users can pass in the `roleId` of the custom role to filter members by this role.
* `includeDeleted`: A parameter accepting a boolean value.
  * `true` -> include a member whose user has been deleted
  * `false` -> exclude member whose user has been deleted
* `sortBy`: allows users to specify the sorting method for the returned collection. The possible values include `displayName`, `firstCreated`, `lastCreated`. The `displayName` sort option will be specified by default if it isn't specified. When a keyword is provided, leading to a list sorted by search rank.

<Info>
To query community banned members, only the 'Admin' role is currently allowed, while 'Moderators' and 'Users' are not allowed to query community banned members.
</Info>

<Tabs>
<Tab title="iOS">
<CodeGroup>
```swift
// Search for members in a community
let options = CommunityMembershipOptions()
options.insert(.member)
community.searchMembers(keyword: "John", membershipOptions: options) { result in
    switch result {
    case .success(let members):
        print("Successfully retrieved members: \(members)")
    case .failure(let error):
        print("Failed to retrieve members: \(error)")
    }
}
```
</CodeGroup>
</Tab>

<Tab title="Android">
<CodeGroup>
```kotlin
// Search for members in a community
val options = CommunityMembershipOptions()
options.add(CommunityMembershipOption.MEMBER)
community.searchMembers("John", options) { result ->
    when (result) {
        is Success -> {
            val members = result.value
            // Handle success
        }
        is Failure -> {
            val error = result.error
            // Handle error
        }
    }
}
```
</CodeGroup>
</Tab>

<Tab title="Flutter">
<CodeGroup>
```dart
// Search for members in a community
final options = CommunityMembershipOptions()..add(CommunityMembershipOption.member);
try {
  final members = await community.searchMembers(
    keyword: 'John',
    membershipOptions: options,
  );
  // Handle success
} catch (error) {
  // Handle error
}
```
</CodeGroup>
</Tab>
</Tabs>