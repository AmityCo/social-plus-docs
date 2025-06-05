---
coverY: 0
---

# TypeScript Live Objects/Collections

In the Social Plus TypeScript SDK, we have the concept of Live Object and Live Collection.

Live Object is represented by an instance of Social Plus Object. It helps to observe changes in a single object.

Live Collection is represented by an instance of Social Plus LiveCollection. It helps to observe changes in a list of objects.

For example: `Amity.Post` or `Amity.LiveCollection<Amity.Post>`

SDK handles lots of data received from various sources. Data can be present in the local cache. It may also be queried from the server or received from real-time events. What this means is that the same data is constantly updating. The data that you are accessing at the moment can get updated and become out of sync.

**Live Object** and **Live Collection** help in syncing data so you will always get the most recent one. New data gets automatically collected every time when there is an update and the user need not refresh to get the recent data.

Live Collection is available for the following in user/community feeds:

* Post Collection
* Comment Collection
* Reactions Collection
* Followers/Following Collection
* Channel Collection
* Sub Channel Collection
* Message Collection
* Channel Member Collection
* Community Collection
* Community Category Collection
* Community Objects
* Community Members Collection
* File Collection
* Story Collection
* Stream Collection
* User Collection

<Info>
Live Collection is not supported for global feed and custom post ranking.
</Info>

### Live Object

Although live objects were introduced prior to v6. All getter methods for singular objects (example `getPost`) will now return a subscribe-able object.

This means that if an object gets updated and you have subscribed to real-time events, the object will get updated automatically via real-time events.

If for your use case, you don't require any real-time updates, you can unsubscribe immediately. For further information about Live Object, please visit [#live-object](./#live-object "mention") page.

#### Getting Real Time Updates for an Object

```typescript
import { PostRepository, subscribeTopic, getPostTopic } from '@amityco/ts-sdk';
import { FC, useEffect, useState } from 'react';

const disposer: Amity.Unsubscriber[] = [];

const GetPost: FC<{ postId: string }> = ({ postId }) => {
  const [post, setPost] = useState<Amity.Post>();

  useEffect(() => {

    const unsubscribePost = PostRepository.getPost(postId, ({ data }) => {
     const { post, loading, error } = data
     
     if (post) {
       /*
       * This step is important if you wish to recieve real time updates
       * Here, you are letting the server know that you wish to recieve real time
       * updates regarding this post
       */
       disposers.push(subscribeTopic(getPostTopic(post)))
       
       setPost(post)
     }
    });
    
    disposers.push(unsubscribePost);
  }, [postId]);

  return null;
};
```

#### Getting the object only once

```typescript
import { PostRepository } from '@amityco/ts-sdk';
import { FC, useEffect, useState } from 'react';

const GetPostOnce: FC<{ postId: string }> = ({ postId }) => {
  const [post, setPost] = useState<Amity.Post>();

  useEffect(() => {
    const unsubscribePost = PostRepository.getPost(postId, ({ data }) => {
     const { post, loading, error } = data
     
     if (post) {       
       setPost(post)
     }
    });
    
    unsubscribePost()
  }, [postId]);

  return null;
};
```

### Live Collection

Although live collections were introduced prior to v6. All query methods for the collection of objects (example `getPosts`) will now return a subscribe-able collection.

This means that if an object in the collection gets updated and you have subscribed to real-time events, the collection will get updated automatically via real-time events.

If for your use case, you don't require any real-time updates, you can unsubscribe immediately. Similar to the live objects above. For further information about Live Collection, please visit [#live-collection](./#live-collection "mention") page.

#### Getting Real-Time updates for a collection

```typescript
import {
  PostRepository,
  subscribeTopic,
  getUserTopic,
  getCommunityTopic,
  SubscriptionLevels,
} from '@amityco/ts-sdk';
import { FC, useEffect, useState } from 'react';

const disposers: Amity.Unsubscriber[] = [];

const GetPosts: FC<{ targetId: string; targetType: string }> = 
({ targetId, targetType }) => {
  const [posts, setPosts] = useState<Amity.Post[]>();

  useEffect(() => {
    const unsubscribe = PostRepository.getPosts(
      { targetId, targetType },
      ({ data: posts, onNextPage, hasNextPage, loading, error }) => {
        setPosts(posts);
        /*
         * this is only required if you want real time updates for each
         * post in the collection
         */
        subscribePostTopic(targetType, targetId);
      },
    );

    disposers.push(unsubscribe);

    return () => {
      disposers.forEach(fn => fn());
    };
  });

  return null;
};

const subscribePostTopic = (targetType: string, targetId: string) => {
  if (isSubscribed) return;

  if (targetType === 'user') {
    const user = {} as Amity.User; // use getUser to get user by targetId
    disposers.push(
      subscribeTopic(getUserTopic(user, SubscriptionLevels.POST), () => {
        // use callback to handle errors with event subscription
      }),
    );
    return;
  }

  if (targetType === 'community') {
    // use getCommunity to get community by targetId
    const community = {} as Amity.Community; 
    disposers.push(
      subscribeTopic(getCommunityTopic(community, SubscriptionLevels.POST), () => {
        // use callback to handle errors with event subscription
      }),
    );
  }
};
```

#### Getting paginated collection without and real-time updates

```typescript
import {
  PostRepository,
  subscribeTopic,
  getUserTopic,
  getCommunityTopic,
  SubscriptionLevels,
} from '@amityco/ts-sdk';
import { FC, useEffect, useState } from 'react';

const GetPosts: FC<{ targetId: string; targetType: string }> = 
({ targetId, targetType }) => {
  const [posts, setPosts] = useState<Amity.Post[]>();

  useEffect(() => {
    const unsubscribe = PostRepository.getPosts(
      { targetId, targetType },
      ({ data: posts, onNextPage, hasNextPage, loading, error }) => {
        if (posts)
          setPosts(posts);
        
        // to get next page use onNextPage()
      },
    );

    unsubscribe()
  });

  return null;
};
```