# User Presence

The SDK also offers functionality to query and synchronize the presence of other users, enabling the creation of a UI that displays their online status. For example, you might use a green dot to indicate whether a particular user is online or offline.

Within the SDK, a user's presence is represented by the `AmityUserPresence` object, which contains three properties.

| Property      | Remarks                                                                                                                         |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| userId        | Id of the user                                                                                                                  |
| lastHeartbeat | Timestamp when that user last synced its heartbeat with the server.                                                             |
| isOnline      | Convenient property to determine online status. User is considered online if its lastHeartbeat has been within last 60 seconds. |

## Query User Presence

The SDK enables users to query the presence state for a list of users, with a maximum limit of 220. The `getUserPresence` method from the `AmityUserPresenceRepository` class can be used to fetch a list of `AmityUserPresence` objects.

<Tabs>
  <Tab title="iOS">
    <CodeGroup>

    ```swift
    let repository = AmityUserPresenceRepository(client: client)
    repository.getUserPresence(userIds: ["userId1", "userId2"]) { (result) in
        switch result {
        case .success(let presences):
            // Handle presence objects
            break
        case .failure(let error):
            // Handle error
            break
        }
    }
    ```

    </CodeGroup>
  </Tab>
  <Tab title="Android">
    <CodeGroup>

    ```kotlin
    val repository = AmityUserPresenceRepository(client)
    repository.getUserPresence(listOf("userId1", "userId2"))
        .subscribe({ presences ->
            // Handle presence objects
        }, { error ->
            // Handle error
        })
    ```

    </CodeGroup>
  </Tab>
</Tabs>

## Sync & Unsync User Presence

In addition to querying user presence, the SDK also offers a method to periodically sync the presence of other users. This functionality keeps users informed about the online status of others. One application of this feature would be to display a list of users and provide an online indicator for those who are currently online.

### Sync User Presence

The SDK includes the `syncUserPresence(id, viewId)` method in the `AmityUserPresenceRepository` class to synchronize the presence of another user. This method adds the specified ID to the list of user IDs for presence synchronization, occurring periodically at set intervals. To observe the results of this process, use the `getSyncingUserPresence()` method. When presence information is obtained for the currently syncing user IDs, notifications are sent through the observer returned from the `getSyncingUserPresence()` method. For further details on observing presence, refer to the [#observe-user-presence](user-presence.md#observe-user-presence) section.

For optimal use, particularly when displaying a list of users, call this method as a list item appears to synchronize the user's presence state. Conversely, utilize the `unsyncUserPresence(id, viewId)` method to stop synchronization when a list item is no longer visible, ensuring that the maximum sync limit is never reached.

<Info>
  The maximum number of user IDs that can be synced at a time is 20. If the count exceeds this limit, the SDK will log an error message to the console. To remove a user ID from the list, use the unsyncUserPresence(id:viewId:) method.
</Info>

<Tabs>
  <Tab title="iOS">
    <CodeGroup>

    ```swift
    let repository = AmityUserPresenceRepository(client: client)
    repository.syncUserPresence(userId: "userId1", viewId: nil)
    ```

    </CodeGroup>
  </Tab>
  <Tab title="Android">
    <CodeGroup>

    ```kotlin
    val repository = AmityUserPresenceRepository(client)
    repository.syncUserPresence("userId1")
    ```

    </CodeGroup>
  </Tab>
</Tabs>

This `syncUserPresence(id, viewId)` method also provides an optional viewId parameter. viewId is the unique id of the view that this user id is tied to. In most cases, you do not need to specify any value to this parameter. viewId is useful if you want to bind the same user id to multiple views on the same screen. In that case, if you want to unsync presence for one view, it won't affect presence syncing for the same user id in another view.

<Info>
  SDK will log a message in the console incase of any error which occurs during the syncing process.
</Info>

### Unsync User Presence

The SDK includes the `unsyncUserPresence(id, viewId)` method to cease syncing the presence of a specific user ID. When a user ID is unsynced, the SDK removes it from the current list of synced IDs, and the observer returned from the `getSyncingUserPresence()` method will no longer provide presence information for that user. The method also features an optional `viewId` parameter, functioning similarly to the `syncUserPresence(id, viewId)` method.

<Tabs>
  <Tab title="iOS">
    <CodeGroup>

    ```swift
    let repository = AmityUserPresenceRepository(client: client)
    repository.unsyncUserPresence(userId: "userId1", viewId: nil)
    ```

    </CodeGroup>
  </Tab>
  <Tab title="Android">
    <CodeGroup>

    ```kotlin
    val repository = AmityUserPresenceRepository(client)
    repository.unsyncUserPresence("userId1")
    ```

    </CodeGroup>
  </Tab>
</Tabs>

The SDK also provides a convenient method to unsync all user ids that are currently being synced. This is particularly useful when you don't care about the user ids being synced. One use case for this is when the user navigates to another screen that does not care about syncing previously synced users at all. So you can call `unsyncAllUserPresence()` method when the previous screen disappears.

<Tabs>
  <Tab title="iOS">
    <CodeGroup>

    ```swift
    let repository = AmityUserPresenceRepository(client: client)
    repository.unsyncAllUserPresence()
    ```

    </CodeGroup>
  </Tab>
  <Tab title="Android">
    <CodeGroup>

    ```kotlin
    val repository = AmityUserPresenceRepository(client)
    repository.unsyncAllUserPresence()
    ```

    </CodeGroup>
  </Tab>
</Tabs>

## Observe User Presence

After adding users for synchronization, the next step involves observing their presence. The SDK offers an observer via the `getSyncingUserPresence()` method. Whenever presence information is retrieved for users synced through `syncUserPresence(id, viewId)`, this information is published through the observer.

**Accessing User Presence:**

You can access the presence information for synced users in two ways:

1. **Through the Observer Returned from** `getSyncingUserPresence()`**:** When the presence information is updated, the observer provides an array of `[AmityUserPresence]` the user IDs being synced. Users need to map `AmityUserPresence` from this array to the view where the information is to be displayed.
2. **`Through the AmityUser Object:`** When presence information is fetched from the server, the `lastHeartbeat` timestamp is mapped to the `lastHeartbeat` property of the `AmityUser` object, if available. Users can directly access the `lastHeartbeat` property from the `AmityUser` object to determine whether a user is online or offline.

<Tabs>
  <Tab title="iOS">
    <CodeGroup>

    ```swift
    let repository = AmityUserPresenceRepository(client: client)
    repository.getSyncingUserPresence().subscribe { (presences) in
        // Handle presence objects
    }.disposed(by: disposeBag)
    ```

    </CodeGroup>
  </Tab>
  <Tab title="Android">
    <CodeGroup>

    ```kotlin
    val repository = AmityUserPresenceRepository(client)
    repository.getSyncingUserPresence()
        .subscribe({ presences ->
            // Handle presence objects
        }, { error ->
            // Handle error
        })
    ```

    </CodeGroup>
  </Tab>
</Tabs>

## Online Users Count

The SDK provides the `getOnlineUsersCount` method in the `AmityUserPresenceRepository` class to query the count of online users. Please note that this count does not update automatically.

<Tabs>
  <Tab title="iOS">
    <CodeGroup>

    ```swift
    let repository = AmityUserPresenceRepository(client: client)
    repository.getOnlineUsersCount { (result) in
        switch result {
        case .success(let count):
            // Handle count
            break
        case .failure(let error):
            // Handle error
            break
        }
    }
    ```

    </CodeGroup>
  </Tab>
  <Tab title="Android">
    <CodeGroup>

    ```kotlin
    val repository = AmityUserPresenceRepository(client)
    repository.getOnlineUsersCount()
        .subscribe({ count ->
            // Handle count
        }, { error ->
            // Handle error
        })
    ```

    </CodeGroup>
  </Tab>
</Tabs>

## Online Users Snapshot

The SDK provides a method getOnlineUsersSnapshot in AmityUserPresenceRepository to query a list of online users in a network. The list of users can be accessed through user property which returns an array of AmityUser.

<Info>
  This snapshot is not auto-updating & supports queries of up to 1000 online users.
</Info>

When this snapshot object is initialized, it fetches the snapshot of user presences of all online users in current network. Then it maps that information to AmityUser per page and provides a list of AmityUser with pagination. Each page can contain a maximum of 20 users. When the snapshot is returned, it will contain users for the first page. You can still fetch more users if available through the loadMore() method. Once more users are fetched, the user can access those users through the user's property. You can also use the canLoadMore property to determine if more online users can be fetched.

<Tabs>
  <Tab title="iOS">
    <CodeGroup>

    ```swift
    let repository = AmityUserPresenceRepository(client: client)
    repository.getOnlineUsersSnapshot { (result) in
        switch result {
        case .success(let snapshot):
            // Handle snapshot
            break
        case .failure(let error):
            // Handle error
            break
        }
    }
    ```

    </CodeGroup>
  </Tab>
  <Tab title="Android">
    <CodeGroup>

    ```kotlin
    val repository = AmityUserPresenceRepository(client)
    repository.getOnlineUsersSnapshot()
        .subscribe({ snapshot ->
            // Handle snapshot
        }, { error ->
            // Handle error
        })
    ```

    </CodeGroup>
  </Tab>
</Tabs>