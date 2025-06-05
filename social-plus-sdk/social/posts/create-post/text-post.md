# Text Post

Text posts are a simple yet powerful way to create and share text-based content with other users on our platform. With the Social Plus SDK, users can quickly and easily create text posts and add them to a user's or community's feed. As demonstrated in the code sample below, you can simply include the text data as a parameter when creating a text post.

Here's an explanation of the method's parameters:

* `text`: This is a required parameter of type `String`, which represents the text content of the new post. You can pass in any text you want to include in the post, up to a maximum length of 20,000 characters.
* `targetType` - Type of the target, either a particular community or a user feed.
* `metaData` - Additional properties to support custom fields.
* `tags` - Arbitrary strings that can be used for defining and querying the posts (Except Flutter).

<Tabs>
  <Tab title="iOS">
    Use `AmityTextPostBuilder` to create text post.

    <iframe src="https://gist.github.com/amythee/a796f645d0a832d2c4f05e368dcec626"></iframe>
  </Tab>

  <Tab title="Android">
    <iframe src="https://gist.github.com/amythee/42d682246f1b47188c3a7e6cc372b3f6#file-amityposttextcreation-kt"></iframe>
  </Tab>

  <Tab title="JavaScript">
    <iframe src="https://gist.github.com/amythee/22cc099c94e5632045bfb34939833f19#file-createtextpost-js"></iframe>
  </Tab>

  <Tab title="TypeScript">
    <iframe src="https://gist.github.com/amythee/a9fcbe20e985edaf42cd05bcb556796e#file-createtextpost-ts"></iframe>
  </Tab>

  <Tab title="Flutter">
    <iframe src="https://gist.github.com/amythee/b6a8745dbe9977fb6e52c4afe3caa537#file-amityposttextcreation-dart"></iframe>
  </Tab>
</Tabs>