# Query Post

The Social Plus SDK product includes a powerful Posts Query method that allows users to search for and retrieve posts that match specific criteria. This functionality is useful for a variety of use cases and provides a flexible and customizable approach to managing and displaying content in your app. Furthermore, the result of the method will always return as [Live collection](../../core-concepts/live-objects-collections/).

#### Use-case Examples

Posts Query API can be useful for the use cases that require flattening the search and results. For example:

* All posts in a community or user feed
* Media gallery that shows the list of all images, posted by a user
* List of all the text posts that are deleted in a community

#### Query Options

The Posts Query method is capable of retrieving and searching all posts on the server that match the specified criteria, which are:

* `targetId` - ID of the community or user respectively.
* `targetType` - Type of the target, either a particular community or a user feed.
* `types` - available post types are `video`, `image`, `file`, `liveStream`, `poll` and `custom` post. Alternatively, if you don't specify a particular post type, it will return all post types for a specific target.
* `includeDeleted` - Deletion filter. When the boolean is set to `true`, it retrieves both deleted and non-deleted posts. Conversely, when set to `false`, only non-deleted posts are returned. The default state of the boolean is `false`. Additionally, it excludes all deleted posts (both soft and hard deleted posts) not owned by the logged-in user. Community moderators have visibility of soft-deleted posts in the community feed, while self-users can see their own soft-deleted posts in their user feed.
* `sortBy` - When it is set to "lastCreated", the most recently created posts will appear at the top of the result. Conversely, when the "sortOption" is set to "firstCreated", the earliest created posts will be displayed at the top of the result.
* `feedType` - Type of the feed, for possible feedTypes please refer to - [#feed-types](post-review.md#feed-types "mention").

<Tabs>
  <Tab title="iOS">
    <Frame>
      <img src="https://gist.github.com/amythee/da5f7dc594ec1b9ab4ced57766c0df40#file-posts_query_example-swift" />
    </Frame>
  </Tab>
  <Tab title="Android">
    <Frame>
      <img src="https://gist.github.com/amythee/ac91ef0963dfc27e7bcdc8b4332ad0f3#file-amitypostquerybytypes-kt" />
    </Frame>
  </Tab>
  <Tab title="JavaScript">
    <Frame>
      <img src="https://gist.github.com/amythee/d5f77f42b29d720382ba6cd26caffcd9#file-queryposts-js" />
    </Frame>
  </Tab>
  <Tab title="TypeScript">
    <Frame>
      <img src="https://gist.github.com/f1c6f8093bd4f2e0fd7b9cae485ea734" />
    </Frame>
  </Tab>
  <Tab title="Flutter">
    <Frame>
      <img src="https://gist.github.com/amythee/264bdc25880fcf6a9173d558f3d38af9" />
    </Frame>
    In **Flutter** SDK, supported query post types are "`video`", "`image`" and "`file`".
  </Tab>
</Tabs>

<Info>
  For custom posts, follow a namespace-like format.  
  Example: "`my.customtype`"
</Info>