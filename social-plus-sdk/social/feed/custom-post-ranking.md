# Custom Post Ranking

In our previous implementation of our global feed, we rank posts in chronological order. This means that newer posts will rank higher than older ones, thus, the former will show up higher in the feed. While this is not a bad algorithm, other factors should also be considered to determine the posts’ ranking in the global feed.

With our new custom post ranking algorithm, we are using a smarter ranking in our global feed that supports a score-sorting mechanism. We focus on what we consider as “meaningful interactions”. This means that, aside from the post’s submission time, we also factor in user engagements, i.e., posts with more comments and reactions will have a higher ranking. In addition, we factor in the updates and edits done to the post.

### How it Works&#x20;

The post will be ranked according to these factors:&#x20;

* **Engagement rate** \
  Posts with more comments and reactions will show up higher than posts with less \

* **Time of posting** \
  Newer posts will show up higher than older posts. Time decay is applied where the score will decrease as the post gets older. \

* **Updates** \
  Post updates and edits on a post will give the post a score boost. Updates may also include new comments and reactions. \


Posts will be ranked using mathematical formulas with the following properties in the post model as variables:&#x20;

* `commentsCount` - number of comments to the post&#x20;
* `reactionsCount` - number of reactions to the post&#x20;
* `createdAt` - date/time the post was created&#x20;
* `updatedAt` - date/time the post was updated&#x20;
* `editedAt` - date/time the post was edited

A high engagement rate has a big impact on the ranking. A comment will score twice as much as a reaction. A post’s score will decrease as time goes by. However, updating or editing the post bumps up the score.

The score of each post is calculated for every query. This means that when users want to go to the next page, the score will be recalculated.

### How to Configure Ranking

If you need to tailor the ranking logic to your specific requirements, you may contact [Social Plus Support](https://ekoapp.atlassian.net/servicedesk/customer/portal/3) to discuss and review the ranking logic and apply it to the code accordingly.

In our next implementation phase, we will add ranking configurations in the SP Console so users can update ranking logic without the need to call support.

### Limitations&#x20;

Please note however that our custom post-ranking implementation has some limitations currently such as:&#x20;

* While your newly created posts will be immediately available in your User Feed, due to the nature of the ranking algorithm, there may be a momentary delay before they appear on the Global Feed.
* Updating the ranking formula can't be done via the SP console. Please contact Social Plus Support for the formula validation and apply your ranking logic to the network.&#x20;
* You can only see up to 20 posts from each user or community that you are following in the global feed.&#x20;
* Old post data will not be migrated, thus, only the posts that are posted using version 5.10 will show in the global feed.

### Implementation

For more information on how to implement custom post ranking in your global feed, see our documentation [**here**](query-global-feed.md).

We also provide UI Kit guides for custom post ranking for [**iOS**](../../../social-plus-uikit/uikit-3/ios/community/components/community-home-page/newsfeed/global-feed.md) and [**Android**](../../../social-plus-uikit/uikit-3/android/community/using-only-some-components/community-home-page/newsfeed/global-feed.md).
