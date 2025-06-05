# Realtime Events

The SDK supports real-time events of various data models through a robust event-driven mechanism. For instance, when a user modifies their profile, these changes can seamlessly be reflected in another user's device. This reflection is achieved via the same [live-objects-collections](../../core-concepts/live-objects-collections/ "mention") that the user is observing in real-time.

Currently, the SDK supports real-time event subscriptions for the following models:

* Community
* Post
* Comment
* User
* Follow/Unfollow
* Subchannel

## Usage

To subscribe or unsubscribe from the relevant real-time events, you need to create a `Subscription Topic`. Upon constructing the subscription topic, the SDK exposes methods for subscribing and unsubscribing, allowing you to listen to specific events without needing to create a new topic.

### Construct Subscription Topic

The subscription topic construction, excluding Follow/Unfollow topics, requires two parameters:

1. **Data Model (required):** This represents the model to which we wish to subscribe, which can be any [#live-object](../../core-concepts/live-objects-collections/#live-object "mention") model.
2. **Subscription Level (optional):** This allows specifying the event level within that model for real-time updates. The SDK includes an enum for this purpose. If not provided, the default subscription level corresponds to the passed model type.

### Observe updates

Once you've successfully established a subscription using the methods outlined previously, the SDK will start receiving data pertaining to the events you've subscribed to. Should there be any alterations to the [live-objects-collections](../../core-concepts/live-objects-collections/ "mention") you are observing, you will be notified via the observer block of the respective Live Object or Live Collection. This functionality ensures you always have access to the most current data without needing to manually fetch updates.

Here's an example of subscribing to real-time events from a subscription topic and observing changes via a live object. For available topics please visit [social-realtime-events.md](../../core-concepts/realtime-events/social-realtime-events.md "mention") and [chat-realtime-events.md](../../core-concepts/realtime-events/chat-realtime-events.md "mention").

<Tabs>
<Tab title="iOS">
<Frame>
<img src="https://gist.github.com/amythee/cb275664de317fdbc3dfd82914dc1c30#file-subscribe_and_observe_changes-swift" />
</Frame>
</Tab>

<Tab title="Android">
<Frame>
<img src="https://gist.github.com/amythee/74144223bbf44278c22db9d90548f5c9#file-amityrtepostsubscription-kt" />
</Frame>
</Tab>

<Tab title="JavaScript">
In JavaScript SDK, After subscribing to data models from liveObjects, the changes from the realtime event will also be reflected on the `dataUpdated` event of the same liveObject.

```javascript
const [community, setCommunity] = React.useState();

React.useEffect(() => {
  const liveObject = CommunityRepository.communityForId('communityId');

	// The realtime event for any changes to the community will also reflect here. 
  liveObject.on('dataUpdated', setCommunity);

  return () => liveObject.dispose();
}, []);

React.useEffect(() => {
  if (community.communityId) {
		let topic = getCommunityTopic(community, SubscriptionLevels.COMMUNITY);
    EventSubscriberRepository.subscribe(topic);
   
    return EventSubscriberRepository.unsubscribe(topic);
  }
}, [community.communityId]);
```
</Tab>

<Tab title="TypeScript">
<Frame>
<img src="https://gist.github.com/amythee/9f314ceaf98aaf75ca7b0ce055a03e48#file-watchchangesusingobserver-ts" />
</Frame>

<Frame>
<img src="https://gist.github.com/amythee/5d64a9d0f8e3519abd4d7f33d281cfba#file-watchchangesusingobserver-ts" />
</Frame>

Available event handlers:

* onCommunityCreated
* onCommunityUpdated
* onCommunityDeleted
* onCommunityJoined
* onCommunityLeft
* onCommunityUserAdded
* onCommunityUserBanned
* onCommunityUserRemoved
* onCommunityUserUnbanned
* onPostCreated
* onPostUpdated
* onPostDeleted
* onPostApproved
* onPostDeclined
* onPostFlagged
* onPostUnflagged
* onPostReactionAdded
* onPostReactionRemoved
* onCommentCreated
* onCommentUpdated
* onCommentDeleted
* onCommentFlagged
* onCommentUnflagged
* onCommentReactionAdded
* onCommentReactionRemoved
* onUserFollowed
* onUserUnfollowed
* onFollowerRequested
* onFollowRequestAccepted
* onFollowRequestCanceled
* onFollowRequestDeclined
* onFollowerDeleted
* onFollowInfoUpdated
</Tab>
</Tabs>

## Unsubscribe Events

To ensure the number of active subscriptions stays within the limit, it is recommended to unsubscribe from topics when they are no longer needed. This could mean unsubscribing when leaving a particular screen or during periods of inactivity.

Each topic subscription in the SDK provides an `unsubscribe` method. For unsubscribing, use the `Unsubscribe` topic method.

If the `logout()` method is invoked at any point, the current session will be terminated and all existing subscriptions will be automatically removed. This functionality assists in efficiently managing active subscriptions and preventing unwanted data consumption.

<Tabs>
<Tab title="iOS">
Use `unsubscribeTopic(...)` method from `AmityTopicSubscription` class or use `unsubscribeEvent(:_)` method from the model itself

<Frame>
<img src="https://gist.github.com/amythee/fa158b8cc7962d0c07a2186bc924835d#file-unsubscribe_a_topic-swift" />
</Frame>
</Tab>

<Tab title="Android">
<Frame>
<img src="https://gist.github.com/amythee/bba01863d92b18f45097cba44306b09d#file-amityrteunsubscription-kt" />
</Frame>
</Tab>

<Tab title="JavaScript">
```javascript
import { 
	getCommunityTopic,
	EventSubscriberRepository,
	SubscriptionLevels } from '@amityco/js-sdk';

let topic = getCommunityTopic(communityModel, SubscriptionLevels.POST);

// Subscription has an optional error callback parameter that can be used.
EventSubscriberRepository.subscribe(topic, (err) => {
	if (err) { // handle subscription error here}
	// handle subscription success here.
});

// Unsubscribe
EventSubscriberRepository.unsubscribe(topic);
```
</Tab>

<Tab title="TypeScript">
Supported ✅ (please wait while we prepare a real example!)
</Tab>
</Tabs>

By adopting these practices, you can efficiently manage the subscription limit and maintain a responsive and performant application.

## Subscription Topics limit

The SDK imposes a maximum limit of 20 for the number of topics that can be subscribed to simultaneously. Developers are advised to manage their list of subscriptions and unsubscribe as necessary.

For instance, suppose you have two screens: one displays a list of communities, and the other displays community details. You may want to subscribe when a user is viewing community details and unsubscribe when the user returns to the community list screen.

Even if you subscribe to the same topic and event multiple times, the SDK maintains only one subscription.

#### Strategies for Managing Subscription Limit

1. **Use higher-level topics:** Instead of creating a topic for each post within a community or each comment within a post, it's recommended to create a single community topic for all posts and comments within that community. This can be achieved by using the `getCommunityTopic` method with a `SubscriptionLevel` of `POST_AND_COMMENT`.
2. **Subscribe when rendered, unsubscribe when not:** Developers should consider subscribing to a topic when a liveObject is rendered and unsubscribing when it's no longer needed. For instance, if you have a list of communities on a page and you navigate to a page showing a community's details, you may want to subscribe when the user is viewing community details and unsubscribe when the user returns to the community list page.