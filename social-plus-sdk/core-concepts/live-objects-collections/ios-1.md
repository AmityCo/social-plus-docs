# Flutter Live Objects/Collections

## Live Objects and Live Collection

In Flutter SDK, we have a concept of Live Object and Live Collection. Live Object is represented by `StreamSubscription<Object>` instance and LiveCollection is represented by an instance of `LiveCollection`. `LiveCollection` is a generic class that encapsulates any other object and notifies the observer whenever any property of the encapsulated object changes. Live Object helps to observe changes in a single object whereas Live Collection helps to observe changes in a list of objects. For example: `StreamSubscription<AmityPost>` or `LiveCollection<AmityMessage>`.

### How it Works

SDK handles lots of data received from various sources. Data can be present in the local cache. It might also be queried from the server or received from some real-time events. What this means is that the same data is constantly updating. The data that you are accessing at the moment can get updated by other sources and become out of sync. Live Object and Live Collection help in syncing the data so you will always get the most recent one. Whenever the data updates, you will be notified through helper methods in the Live Object and Live Collection classes.&#x20;

New data gets automatically collected every time when there is an update and the user need not refresh to get the recent data.

Live Collection is available for the following in user/community feeds:

* Post Live Collection
* Community Live Object
* Message Live Collection
* Comment Live Collection
* Story Live Collection
* Stream Live Collection
* Reaction Live Collection
* Story Target Live Collection
* Global Story Target Live Collection

Live Object is available for the following in user/community feeds:

* Post Live Object&#x20;
* Community Live Object&#x20;
* Comment Live Object
* Poll Live Object&#x20;
* Story Live Object&#x20;

### LiveObject

`StreamSubscription<Object>` is a native flutter class that keeps track of a single object. It is a live object. In Flutter `AmitySDK`, any object which provides Stream is a Live Object.&#x20;

Examples:

{% embed url="https://gist.github.com/amythee/bd4f33e6e1af748ef6637e2601029dfd" %}

This function helps listen to Live Object. Whenever any property for the observed object changes, the `listen` callback will be triggered.

### Live Collection

`LiveCollection` is a generic class that keeps track of a collection of objects. It is a Live Collection. In Flutter SDK, any object that is encapsulated by `LiveCollection` class is a live collection.&#x20;

Examples:&#x20;

* `MessageLiveCollection`&#x20;
* `ChannelLiveCollection` &#x20;

`LiveCollection` exposes these methods:

* `asStream`&#x20;
* `onError`&#x20;

These methods help observe a Live Collection. Whenever any property for any object within the collection changes, the observer is triggered, as well as observing any errors from the collection.

#### Stream Observer

`asStream` method can get triggered multiple times throughout the lifetime of the application as long as its associated `Stream<List<Object>>` is retained in memory.

`asStream` method will be called from the main thread so you can perform any UI update-related task within the `listen` block itself.

* If the requested data collection is stored locally on the device, the block will be called immediately with the local version of the data.
* In parallel, a request is made to the server to fetch the latest version of the data. Once the data is returned, the `listen` block will be triggered again.
* Any future changes to the data from any sources can trigger the `listen` block.&#x20;

#### Pagination

`AmityCollection` in SDK returns a maximum of `pageSize` items per page. It has `loadNext()` method to fetch more data. It also exposes `hasNext` property to check if the next page or previous page is present.

{% embed url="https://gist.github.com/amythee/fd760cbed7685a2b1b4e9debd33fd810" %}

Once the next page is available, the same `listen` block gets triggered and you can access the collection as shown above. If you want to shrink the collection to the original first page, you can do so by calling `reset()` method on the same collection.

One typical usage of LiveCollection is in `ListView`. Below is an example of fetching a collection and updating its state in a `Widget`.

{% embed url="https://gist.github.com/amythee/c244b0dda92d25a264f820884d8fc667" %}
