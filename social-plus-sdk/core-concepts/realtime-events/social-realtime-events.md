# Social Realtime Events

A topic is a distinct path that must be constructed for each model to which you wish to subscribe in real-time. The SDK provides helper methods to create these topics for each model type. Each topic encompasses an events enum, which developers can select to subscribe to based on their business context and interests.

To subscribe to updates from a community or any content created within that community, the user must have the 'Member' status in that community. Once the user leaves the community, they will no longer receive real-time events.

### Community Topic

* `COMMUNITY` - subscription to changes in the community object
* `POSTS` - subscription to changes of post objects in the community
* `COMMENTS` - subscription to changes of comment objects in the community
* `POST and COMMENTS` - subscription to changes of posts and posts comments  in the community
* `STORY and COMMENTS` - subscription to changes of story and story comments in the community

The default value is `COMMUNITY`

<Tabs>
  <Tab title="iOS">
    <Frame url="https://gist.github.com/amythee/e00578621b9f644db995092b4bf2381d#file-subscribe_a_topic-swift" />
  </Tab>
  <Tab title="Android">
    <Frame url="https://gist.github.com/088cec18257e0a938dcb54a85175afd7" />
  </Tab>
  <Tab title="JavaScript">
    ```javascript
    import { getCommunityTopic, SubscriptionLevels } from '@amityco/js-sdk';

    // Community topic to subscribe to all events of that community model only
    // Example events: community joined, community left, community updated 
    const topic = getCommunityTopic(communityModel, SubscriptionLevels.COMMUNTIY);

    // Community topic to subscribe to all post events of that community model
    // Example events: post created, post deleted, post updated
    const topic = getCommunityTopic(communityModel, SubscriptionLevels.POST);

    // Community topic to subscribe to all comment events of that community model
    // Example events: comment created, comment deleted, comment updated
    const topic = getCommunityTopic(communityModel, SubscriptionLevels.COMMENT);

    // Community topic to subscribe to all posts and comment events of that community model
    // Example events: comment created, comment deleted, comment updated
    const topic = getCommunityTopic(communityModel, SubscriptionLevels.POST_AND_COMMENT);
    ```
  </Tab>
  <Tab title="TypeScript">
    <Frame url="https://gist.github.com/amythee/388970b316937cdcafdec608433b4628#file-getcommunitytopics-ts" />
  </Tab>
  <Tab title="Flutter">
    <Frame url="https://gist.github.com/amythee/1c33c87f1b0c6b4b0216923329b81a0d" />
  </Tab>
</Tabs>

### Post Topic

* `POST` - subscription to changes of the post object
* `COMMENTS` - subscription to changes of comment objects on the post

The default value is `POST`

<Tabs>
  <Tab title="iOS">
    <Frame url="https://gist.github.com/amythee/92808cda3ac45cd68079504ee03ef4a7" />
  </Tab>
  <Tab title="Android">
    <Frame url="https://gist.github.com/amythee/74144223bbf44278c22db9d90548f5c9#file-amityrtepostsubscription-kt" />
  </Tab>
  <Tab title="JavaScript">
    ```javascript
    import { getPostTopic, SubscriptionLevels } from '@amityco/js-sdk';

    // Post topic to subscribe to all events of that post model only
    // Example events: post edited, reactions added 
    const topic = getPostTopic(postModel, SubscriptionLevels.POST);

    // Post topic to subscribe to all comment events of that post model
    // Example events: comment created, comment deleted, comment updated
    const topic = getPostTopic(postModel, SubscriptionLevels.COMMENT);
    ```
  </Tab>
  <Tab title="TypeScript">
    <Frame url="https://gist.github.com/amythee/b6519404292afce2fe58da2e91192610#file-getposttopics-ts" />
  </Tab>
  <Tab title="Flutter">
    The functionality isn't currently supported by this SDK.
  </Tab>
</Tabs>

### Comment Topic

* `COMMENT` - subscription to changes in the comment object

<Tabs>
  <Tab title="iOS">
    <Frame url="https://gist.github.com/amythee/14ddc551ed76ac2ac655070e2cc98e18" />
  </Tab>
  <Tab title="Android">
    <Frame url="https://gist.github.com/amythee/28b31ba8a2d73a44889edda171a25f78#file-amityrtecommentsubscription-kt" />
  </Tab>
  <Tab title="JavaScript">
    ```javascript
    import { getCommentTopic, SubscriptionLevels } from '@amityco/js-sdk';

    // Comment topic to subscribe to all comment events of that post model
    // Example events: comment created, comment deleted, comment updated
    const topic = getCommentTopic(commentModel, SubscriptionLevels.COMMENT);
    ```
  </Tab>
  <Tab title="TypeScript">
    <Frame url="https://gist.github.com/amythee/fe23cea0943012bd747317514969b5bf#file-getcommenttopic-ts" />
  </Tab>
  <Tab title="Flutter">
    The functionality isn't currently supported by this SDK.
  </Tab>
</Tabs>

### User Topic

* `USER` - subscription to changes in the user object
* `POSTS` - subscription to changes of post objects in the user feed
* `COMMENTS` - subscription to changes of comment objects in the user feed
* `POST and COMMENTS` - subscription to changes of post and comment objects in the user feed

The default value is `USER`

<Tabs>
  <Tab title="iOS">
    <Frame url="https://gist.github.com/amythee/0cebf1c999ab811d4ba28edd19dc6eb7" />
  </Tab>
  <Tab title="Android">
    <Frame url="https://gist.github.com/amythee/e7d7127bcb172b1268e74f92e8a0d5e0#file-amityrteusersubscription-kt" />
  </Tab>
  <Tab title="JavaScript">
    ```javascript
    import { getUserTopic, SubscriptionLevels } from '@amityco/js-sdk';

    // User topic to subscribe to all events of that user model only
    const topic = getUserTopic(userModel, SubscriptionLevels.USER);

    // User topic to subscribe to all post events of that user model
    // Example events: post created, post deleted, post updated
    const topic = getUserTopic(userModel, SubscriptionLevels.POST);

    // User topic to subscribe to all comment events of that user model
    // Example events: comment created, comment deleted, comment updated
    const topic = getUserTopic(userModel, SubscriptionLevels.COMMENT);

    // User topic to subscribe to all posts and comment events of that user model
    // Example events: comment created, comment deleted, comment updated
    const topic = getUserTopic(userModel, SubscriptionLevels.POST_AND_COMMENT);
    ```
  </Tab>
  <Tab title="TypeScript">
    <Frame url="https://gist.github.com/amythee/65dc02163db21c46369c370be88c3c5e#file-getusertopics-ts" />
  </Tab>
  <Tab title="Flutter">
    The functionality isn't currently supported by this SDK.
  </Tab>
</Tabs>

### Follow Topic

* `MY_FOLLOWERS` - subscription to changes related to users that the current user follows
* `MY_FOLLOWING` - subscription to changes related to users that follow current user

<Tabs>
  <Tab title="iOS">
    <Frame url="https://gist.github.com/amythee/b6b5d9df7de66d2ba9a0f1be5f287cd7" />
  </Tab>
  <Tab title="Android">
    <Frame url="https://gist.github.com/amythee/16684e995bdba633cfc1d1411b39d64a#file-amityrtefollowsubscription-kt" />
  </Tab>
  <Tab title="JavaScript">
    <Frame url="https://gist.github.com/amythee/d669faf11df00cc8adb3f0a15ce98b39#file-subscribefollowtopic-js" />
  </Tab>
  <Tab title="TypeScript">
    <Frame url="https://gist.github.com/amythee/fda34838818d77af10a48619f176e19e#file-getfollowtopics-ts" />
  </Tab>
  <Tab title="Flutter">
    The functionality isn't currently supported by this SDK.
  </Tab>
</Tabs>

### STORY Topic

* Subscription to changes related to specific stories.

<Tabs>
  <Tab title="iOS">
    <Frame url="https://gist.github.com/amythee/4f506a2ab9af205bca686642d1b3e497" />
  </Tab>
  <Tab title="Android">
    <Frame url="https://gist.github.com/07cc03155ab3af16ff18b39afb6349d1" />
  </Tab>
</Tabs>