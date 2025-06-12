# Javascript Live Objects/Collections

All data returned by the SDK are wrapped in the SDK's LiveObject API. The LiveObject API allows you to easily retrieve the queried data asynchronously, as well as subscribe to any new changes to the data.

## LiveObject

Observing live changes to any object queries can be done by observing the `dataUpdated` event on the Live Object:

```javascript
// observe data changes
const currentUser = client.currentUser;

currentUser.on('dataUpdated', model => {
  console.log(`Current user is: ${model.displayName}`);
})

// unobserve data changes once you are finished
currentUser.removeAllListeners('dataUpdated');
```

In this example, the block observes the data of the currently authenticated user and prints out the `displayName`. The observe block can be called multiple times throughout the lifetime of the application:

* If the requested object data is stored locally on the device, the block will be called immediately with the local version of the data (you can verify this through the `dataStatus` property).
* In parallel, a network request for the latest version of the data is fired. Once the network returns the data, the observe block will be called again with the updated data.
* Any future changes to the data (whenever the user changes its `displayName` on another device, for example) can trigger additional callbacks.

We recommend you to always call `removeAllListeners()` whenever you are done observing an event to avoid any unnecessary callbacks.

### Model

The data provided by LiveObject is directly accessible via the `model` property. The `model` property is always kept up to date with the latest state changes; whenever`dataUpdated` event is fired, the `model` property has already been updated.

### Data Status

If you want to exclusively display fresh data in your UI (without using the potentially out-of-date local data), you can do so by reading the object's `dataStatus` property, which reflects the status of the callback data, and checking that its value is set to fresh.

```javascript
import { LoadingStatus, DataStatus } from '@amityco/js-sdk';

if (currentUser.dataStatus === DataStatus.Fresh) {
  // the data field of this object is up to date
  console.log(currentUser.model);
}
```

You can also use the object's `loadingStatus` property to determine the current state of network operations being performed by the LiveObject. This is useful for any UI element that needs to provide the loading state.

```javascript
if (currentUser.loadingStatus === LoadingStatus.Loading) {
  // this object is current loading, show loading UI
}
```

The LiveObject can also emit events for updates for `dataStatus` as well as `loadingStatus`. As with other events, please make sure to call `removeAllListeners()` when you are done observing changes to these values in order to prevent memory leaks.

```javascript
currentUser.on('dataStatusChanged', callback);
currentUser.on('loadingStatusChanged', callback);
```

### Events Order

The LiveObject updates statuses and data in strict order and emits related events accordingly when an instance is created. A few different cases might occur when you create a LiveObject instance:

#### Data is not cached.

Initial values:

* `loadingStatus = LoadingStatus.Loading`
* `dataStatus = DataStatus.NotExist`
* `model = undefined`

Process received data:

* emits `loadingStatusChanged`
* emits `dataStatusChanged`
* emits `dataUpdated`

#### Data is cached but is not fresh.

Initial values:

* loadingStatus = LoadingStatus.Loading
* dataStatus = DataStatus.Local
* model = localData

Process received data (same order):

* emits `loadingStatusChanged`
* emits `dataStatusChanged`
* emits `dataUpdated` - only if data is really different

#### Data is cached and is fresh.

* loadingStatus = LoadingStatus.Loaded
* dataStatus = DataStatus.Fresh
* model = localFreshData

### Interface

This is the list of LiveObject members and methods.

**Members**

* `model` = model that the live object should fetch
* `loadingStatus =` determine the current state of network operations being performed by the LiveObject
* `dataStatus =` reflects the status of the callback data

**Methods**

* `on(event, callback)` =  listens to `event` and executes `callback` when `event` is fired
* `once`= same as the `on` method but can only be called once
* `removeAllListeners` = removes all listeners from `on`
* `dispose` = causes the LiveObject to be destroyed and cleaned up

### **Get Post data**

Here is a sample code on how the get Post data.

```javascript
const livePost = PostRepository.getPost(postId)
console.log(livePost.model)
```

## LiveCollection

The LiveObject API supports queries that return a list of objects, this is known as a LiveCollection. LiveCollection has the same methods and properties as its object counterpart but contains a few other helper methods around pagination.

```javascript
import { MessageRepository } from '@amityco/js-sdk';

const messageRepo = new MessageRepository('channel1');
const messages = messageRepo.messagesForChannel({ channelId: 'channel1234' });
messages.on('dataUpdated', models => {
  // models will be an array of message objects
  models.forEach(message => {
    console.log('Message: ', message);
  });
});
```

### Pagination

Pagination with LiveCollections is very simple: the collection offers a convenient `nextPage` method that you can call which will automatically trigger a local cache lookup, a network call, and multiple LiveObject updates once new data is returned. Every collection starts with one page of 20 models. After `nextPage()` is successful, the `dataUpdated` event will be triggered with a new array combining both the old objects as well as 20 newly fetched objects.

```javascript
const liveCollection = MessageRepository.queryMessages({
    channelId: 'channelId',
    type: 'text'
});

liveCollection.on(“dataUpdated”, messages => console.log(messages))

const loadMore = () => {
  if (liveCollection.nextPage) {
    liveCollection.nextPage();
  }
};
```

The `dataUpdated` event will be dispatched when the first set of data from the server is loaded. Calling `nextPage` will load the next set of data. Once all data are loaded, the `dataUpdated` event will once again be dispatched.

> You can use the `nextPage` property to determine if you've scrolled to the end of the list. The `nextPage` property initially returns `false` until the first collection query is finished.

Lastly, if there is a need to shrink the list of objects exported back to only the first 20 records (for example, if you pass the LiveCollection object to a new view), you can simply call `resetPage()`.

### Models

Similar to `model` property of the LiveObject, the LiveCollection provides `models` property which is basically an array of LiveObject's `model` objects. `models` is mutable and always contains the same data as one returned by `dataUpdated` event.

## Errors

Both LiveObject and LiveCollection can be subscribed to the `dataError` event which is fired every time an error happens during the data update process. In other words, every time the LiveObject or LiveCollection fails to get data from the server - this error will be emitted.

```javascript
const messages = messageRepo.messagesForChannel({ channelId: 'channel1234' });

messages.on('dataError', error => {
  // Every error has a code. You can control how your application should behave in response to the error.
  if (error.code !== YYYYYY) {
    throw error;
  }
});
```

## Dispose of LiveObject and LiveCollection

We recommend you to always call `dispose()` whenever you are done working with any LiveObject/LiveCollection.

```javascript
// create an user LiveObject and a messages LiveCollection when you mount your component or view
const currentUser = client.currentUser;
const messages = messageRepo.messagesForChannel({ channelId: 'channel1234' });

...

// before leaving page, unmounting component etc
currentUser.dispose();
messages.dispose();
```

Dispose is a very important functionality of the LiveObject. It allows you to avoid memory leaks and keeps your application performant. What does `dispose()` do:

* unsubscribe all listeners attached to the LiveObject  instance;
* stop all internall observers related to the LiveObject instance;
* clean up an internall buffer of the LiveObject instance;

After you call `dispose()` on a LiveObject instance, dataStatus and loadingStatus switch to `Error`.
