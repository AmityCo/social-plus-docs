# iOS Live Objects/Collections

## Live Objects and Live Collections

In iOS Social Plus SDK, we have a concept of Live Object and Live Collection. LiveObject is represented by `AmityObject` an instance and LiveCollection is represented by an instance of `AmityCollection`. These generic classes encapsulate any other object and notify the observer whenever any property of the encapsulated object changes.

Live Object helps to observe changes in a single object whereas Live Collection helps to observe changes in a list of objects. For example: `AmityObject<AmityPost>` or `AmityCollection<AmityMessage>`.

### How it Works

SDK handles a lot of data received from various sources. Data can be present in the local cache. It might also be queried from the server or received from some real-time events. This means some data is constantly updating. The data that you are accessing at the moment can get updated by other sources and become out of sync.

Live Object and Live Collection help in syncing these constantly updating data, so you will always get the most recent one. Whenever the data gets updated, you will be notified through helper methods in live objects and live collection classes.

New data gets automatically collected every time when there is an updation and the user need not refresh to get the recent data.

Live collection is available for the following functionalities in user/community feeds:

* Post Collection
* Comment Collection
* Story Collection
* User Collection
* Reactions Collection
* Followers/Following Collection
* Channel Collection
* Sub-Channel Collection
* Message Collection
* Channel Member Collection
* Community Collection
* Community Members Collection
* Community Category Collection
* Stream Collection

Both `AmityObject` and `AmityCollection` provide methods for observing changes in objects. The life cycle of observation is tied to its token. As soon as the token is invalidated or deallocated, observation ends.

### AmityNotificationToken

`AmityNotificationToken` is a simple object which keeps track of what is being observed. Each Live Object or Live Collection observation is tied to its respective token. As soon as the token is invalidated or deallocated, observation ends. The token is declared within the scope of the class.

<CodeBlock url="https://gist.github.com/babdf3acfc683358de5e45dd3412f467">
`AmityNotification` is alive in `MyClass` scope.
</CodeBlock>

The token is used in combination with `AmityObject` or `AmityCollection`. We will explore it more in AmityObject and `AmityCollection` concepts.

### AmityObject

`AmityObject` is a generic class that keeps track of a single object. It is a live object. In iOS `AmitySDK`, any object which is encapsulated by `AmityObject` is a live object.

Examples:

* `AmityObject<AmityMessage>`
* `AmityObject<AmityChannel>`

`AmityObject` class exposes the following methods:

* `observe`
* `observeOnce`

These methods help observe a live object. Whenever any property for the observed object changes, the observer is triggered.

<Info>
Please make sure that the user is logged in before observing AmityObject. You can also refer to the [session state](../session-state.md) section for more details.
</Info>

#### Observer

`observe` method can be triggered multiple times throughout the lifetime of the application as long as its associated `AmityNotificationToken` is retained in memory. `observeOnce` method, on the other hand, can only be triggered once.

Both `observe` and `observeOnce` methods will be called from the main thread so you can perform any UI update-related tasks from within the observed block itself.

* If the requested object data is stored locally on the device, the block will be called immediately with the local version of the data. This can be verified through the `dataStatus` property of `AmityObject`.
* In parallel, a request is made to the server to fetch the latest version of the data. Once the data is returned, the observed block will be triggered again.
* Any future changes to that data from any sources can trigger an observer.

**Lifecycle:** The life cycle of the observer is tied to its token. If the token is not retained, then the observer can get deallocated at any time and will not be called. Both `observe` and `observeOnce` block will be retained using token as shown below.

<CodeBlock url="https://gist.github.com/1ddd6d8fa2b04430ed4b4c602fb0e6ec">
Live Object observation is bound to a token
</CodeBlock>

#### Invalidate token

The `AmityNotificationToken` provides a method called `invalidate()` which can be used to invalidate the token anytime. As soon as you invalidate the token, your observation stops and observe block will no longer be triggered.

<CodeBlock url="https://gist.github.com/7694a70e40ca4fd1893823b16b916221">
Invalidate a token
</CodeBlock>

#### Accessing Objects

There are multiple ways to access data from `AmityObject`. `AmityObject` exposes the following properties:

* `dataStatus`: Indicates whether the data is fresh or local
* `loadingStatus`: Indicates if the data is being loaded from server or not
* `object`: The actual object that is being tracked or encapsulated by this AmityObject

Once you add an observer block, you can access both local or fresh data as shown below.

<CodeBlock url="https://gist.github.com/19d131a363e9c75b4a1d625a919bec22">
Accessing live object properties
</CodeBlock>

If you want to observe fresh object just once, you can check the data status and invalidate the token once you receive the fresh object.

<CodeBlock url="https://gist.github.com/17345fc724e5f145f39c27f95738ecc9">
Get a fresh object
</CodeBlock>

For `observerOnce` method, if data is present locally, this observer will be triggered only once with that local data. If you are looking for fresh data, use the `observe` block and invalidate the token once fresh data is received as shown above.

If you only care about local data and do not want to observe anything, you can also access the `object` property from `AmityObject` directly.

<CodeBlock url="https://gist.github.com/909cbb6e7d07d1f8f8f3476815ab33e2">
Get a local data
</CodeBlock>

While this is possible, we recommend accessing object from within the`observe` or `observeOnce` block depending on your requirement.

#### AmityLoadingStatus

`AmityObject` can be tracked for their loading status by accessing the `loadingStatus` property, which is of type `AmityLoadingStatus` and it can have one of four possible values.

* 0 (notLoading): Indicates that the data is already fresh locally and does not need to be loaded.
* 1 (loading): Indicates that the client is currently loading the data from the server.
* 2 (loaded) - Indicates that the client has successfully loaded fresh data from the server and is up to date.
* 3 (error) - Indicates that the data is unable to load due from a specific error.

### AmityCollection

`AmityCollection` is a generic class that keeps track of a collection of objects. It is a live collection. In iOS SDK, any object which is encapsulated by `AmityCollection` class is a live collection.

Examples:

* `AmityCollection<AmityMessage>`
* `AmityCollection<AmityChannel>`

`AmityCollection` exposes these methods:

* `observe`
* `observeOnce`

These methods help to observe a live collection. Whenever any property for any object within the collection changes, the observer is triggered.

<Info>
Please make sure that the user is logged in before observing AmityCollection. You can also refer to [session state](../session-state.md) section for more details.
</Info>

#### Observer

`observe` method can get triggered multiple times throughout the lifetime of the application as long as it's associated `AmityNotificationToken` is retained in memory. `observeOnce`, on the other hand, can only be triggered once.

Both `observe` and `observeOnce` method will be called from the main thread so you can perform any UI update related task within the observe block itself.

* If the requested data collection is stored locally on the device, the block will be called immediately with the local version of the data. This can be verified through the `dataStatus` property of `AmityCollection`.
* In parallel, a request is made to the server to fetch the latest version of the data. Once the data is returned, the observe block will be triggered again.
* Any future changes to the data from any sources can trigger observer.

**Lifecycle:** The life cycle of the observer for AmityCollection is also tied to its token. If the token is not retained, the observer can get deallocated at any time and will not be called. So, both `observe` and `observeOnce` block should be retained. You can refer to the section in `AmityObject` about retaining and invalidating a token.

#### Accessing Collection

Unlike most databases, `AmityCollection` does not return all data in an array. Instead, data is fetched one by one using the `objectAtIndex:` method. This allows the framework to store most of the actual result on disk, and load them in memory only when necessary.

`AmityCollection` also exposes a `count` property which determines the number of objects present in a collection.

With these two public interfaces, you can create a robust list UI for your use case. Similar to `AmityObject`, `AmityCollection` also exposes `dataStatus` and `loadingStatus` property.

Let's look at the typical flow when accessing a collection data.

<CodeBlock url="https://gist.github.com/ab5bf699a2e7bdaf80f15d94c6051309">
Observe a Live Collection
</CodeBlock>

If you want to observe only fresh or local collection, you can access it using the`dataStatus` property and invalidate the token once you have accessed your desired collection data.

<CodeBlock url="https://gist.github.com/e45d4410014895017c2a6aaaa1b5a936">
Observe a Fresh Live Collection
</CodeBlock>

For `observerOnce` method, if data is present locally, this observer will be triggered only once with that local data. If you are looking for fresh data, use `observe` block and invalidate the token once fresh data is received as shown above.

Observer also provides you with the `AmityCollectionChange` object which contains indexes of what is added, deleted, or modified in a collection. You can also refer to these properties to update the UI for the list.

#### Iterate through collection

While SDK provides `liveCollection.object(at:)` to access a single item, you might often find the need to iterate through all objects in the collection. The SDK has a convenient way to do this using `.allObjects()`.

<CodeBlock url="https://gist.github.com/6f3599b0f3c819d1ce60002572013369">
Iterate each object in a live collection using `.allObjects()`
</CodeBlock>

Using the above method is the same with this logic:

<CodeBlock url="https://gist.github.com/aeab2b924b0fd36ce8563c6f0c431a7a">
An equivalent implementation of `.allObjects()`
</CodeBlock>

#### Pagination

`AmityCollection` in SDK returns a maximum of 20 items per page. It has `nextPage()` and `previousPage()` method to fetch more data. It also exposes `hasNext` and `hasPrevious` property to check if next page or previous page is present.

<CodeBlock url="https://gist.github.com/9a50acd15f82c2c72a684521167d082e">
Call `nextPage()` / `previousPage()` to load more data
</CodeBlock>

Once next page is available, the same `observe` block gets triggered and you can access the collection as shown above. If you want to shrink the collection to the original first page, you can do so by calling `resetPage()` method on the same collection.

One typical usage of Live Collection is in `UITableView`. Below is an example of fetching a collection and displaying it in a tableview.

<CodeBlock url="https://gist.github.com/726754677f2c94f2ae9d350808dbeb09">
Using a live collection with `UITableView`
</CodeBlock>

## SwiftUI Support

AmityObject and AmityCollection are now observable object with its properties marked with `@Published` annotation. Now you can use live object & live collection directly within your SwiftUI views.

| Live Object   | @Published | Remarks    |
| ------------- | ---------- | ---------- |
| dataStatus    | ✅         | -          |
| loadingStatus | ✅         | -          |
| snapshot      | ✅         | New        |
| error         | ✅         | -          |
| object        | ❌         | Deprecated |

| Live Collection | @Published | Remarks |
| --------------- | ---------- | ------- |
| dataStatus      | ✅         | -       |
| loadingStatus   | ✅         | -       |
| snapshots       | ✅         | New     |
| error           | ✅         | New     |

### Access AmityObject & AmityCollection in SwiftUI views

Since `AmityObject` & `AmityCollection` are observable object, it can be used as an ObservedObject within SwiftUI views. We recommend to create small view which observes AmityCollection & AmityObject as ObservedObject as shown in code sample below.

#### **Live Object - SwiftUI**

<CodeBlock url="https://gist.github.com/amythee/7d886c8ee7c112729ed39676af11274e">
</CodeBlock>

**Live Collection - SwiftUI**

<CodeBlock url="https://gist.github.com/amythee/c78803ceacb3663e6fb713505a42fa2b">
</CodeBlock>

Since the properties are published, If you are using Combine Framework, you can also subscribe to changes on those properties.

**Live Object - Combine**

<CodeBlock url="https://gist.github.com/amythee/db15eb14cd4317f234d00490f421c3c8">
</CodeBlock>

**Live Collection - Combine**

<CodeBlock url="https://gist.github.com/amythee/889ffb46faa46c14437c9d4d41e6a46e">
</CodeBlock>

<Info>
ℹ️ States of live collection & live object are published before snapshots so that you can compare the state from within subscriber.
</Info>

#### FAQ's:

**#1:** LiveCollection is not updated when used from inside of another observable class.

`AmityCollection` & `AmityObject` is an `ObservableObject`. When this live collection or live object is embedded inside another Observable Object, SwiftUI cannot observe the changes in snapshot occurring within Live collection & Live object. As a result, there might be a situation where you see your view is not getting updated even when snapshot(s) are updated. This is a common problem with nested observable object in SwiftUI.

<CodeBlock url="https://gist.github.com/amythee/31e9cb707e76b7bc67af22d7f02c03fb">
</CodeBlock>

To solve this issue we recommend to create a specific view which observes `AmityCollection` & `AmityObject` as `@ObservedObject` as shown in code example.

**#2:** Published property still returns old values.

Since the properties of AmityCollection & AmityObject are marked with `@Published` annotation, the publishing of changes occurs in the property's `willSet` block, meaning that any subscribers will receive an update before the property is changed. This behaviour can easily lead to unexpected bugs.

<CodeBlock url="https://gist.github.com/amythee/1dc5c91d93afc8abf7ad5c87c47737eb">
</CodeBlock>

For more details, please refer to [https://developer.apple.com/documentation/combine/published](https://developer.apple.com/documentation/combine/published)