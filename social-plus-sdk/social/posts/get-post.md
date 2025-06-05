# Get Post

The Social Plus SDK provides functionality that allows you to work with social features in your application, including the ability to retrieve a post. In this section, we'll explore how to use the Social Plus SDK to retrieve a single post from your application. By using a specific function provided by the SDK, you can retrieve a post based on its ID, which provides a convenient way to access specific post data. The retrieved result is returned as a live object of a post. For more information on live objects, please refer to [live-objects-collections](../../core-concepts/live-objects-collections/ "mention").

<Tabs>
  <Tab title="iOS">
    <Frame>
      <img src="https://gist.github.com/amythee/937be1f833b5bafb8642615fe151cc46#file-get_post_by_id-swift" />
    </Frame>
  </Tab>
  <Tab title="Android">
    <Frame>
      <img src="https://gist.github.com/amythee/4f6e219d3462686b80d791ce512b5d25#file-amitypostget-kt" />
    </Frame>
  </Tab>
  <Tab title="JavaScript">
    <Frame>
      <img src="https://gist.github.com/amythee/97b40f9bd7132d9df41ab99367851264#file-getpost-js" />
    </Frame>
  </Tab>
  <Tab title="TypeScript">
    Version 6
    <Frame>
      <img src="https://gist.github.com/3f80748ead65c350df2f9aacf7ae7dd5" />
    </Frame>
  </Tab>
  <Tab title="Flutter">
    <Frame>
      <img src="https://gist.github.com/amythee/a2cf948a9f535228003b77a6b8fb0f46" />
    </Frame>
  </Tab>
</Tabs>

To retrieve multiple posts, you can use `getPostByIds` method provided by `PostRepository`. This method accepts a collection of `postId` as a parameter and returns a [Live Collection](../../core-concepts/live-objects-collections/) of `AmityPost`.

<Tabs>
  <Tab title="iOS">
    <Frame>
      <img src="https://gist.github.com/amythee/6b76e76865f11ab8c96eda25d2ab3d49" />
    </Frame>
  </Tab>
  <Tab title="Android">
    <Frame>
      <img src="https://gist.github.com/4f63ac6bfc6a9745cbd8a5e71ef862eb" />
    </Frame>
  </Tab>
</Tabs>