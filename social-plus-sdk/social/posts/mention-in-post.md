# Mention in Post

Mentions allow users to tag other users in posts. It's a powerful tool for fostering engagement and collaboration within your social application. With mentions, users can easily notify specific individuals or groups to new content or important updates. In the SDK, mentions can be implemented in a range of ways, depending on your application's needs and user experience. For more information about mentions, please refer to [mentions.md](../../core-concepts/mentions.md "mention").

## Create Post with Mentions

You can easily mention users when creating a post by including their user IDs in the mention user parameter as well as defining metadata for mention rendering. For further explanation, please refer to [#mention-users](../../core-concepts/mentions.md#mention-users "mention").

<Tabs>
  <Tab title="iOS">
    <CodeGroup>
      <CodeBlock>
        {`https://gist.github.com/amythee/03740021d647aca24f70c72617453f8d`}
      </CodeBlock>
    </CodeGroup>
    <CodeGroup>
      <CodeBlock>
        {`https://gist.github.com/amythee/61785ed32e114b23c72df4956ef6ac87`}
      </CodeBlock>
    </CodeGroup>
  </Tab>
  <Tab title="Android">
    <CodeGroup>
      <CodeBlock>
        {`https://gist.github.com/amythee/7e1c0dfaca875293ed4d0cef675a5f21#file-amityposttextcreationwithmention-kt`}
      </CodeBlock>
    </CodeGroup>
  </Tab>
  <Tab title="JavaScript">
    <CodeGroup>
      <CodeBlock>
        {`https://gist.github.com/amythee/c59e7f12681cfd3c6c376266ce74fbb1#file-createtextpost-js`}
      </CodeBlock>
    </CodeGroup>
  </Tab>
  <Tab title="TypeScript">
    <CodeGroup>
      <CodeBlock>
        {`https://gist.github.com/amythee/4743d673e1b7989d42398ed9c7829b44#file-creatementionpost-ts`}
      </CodeBlock>
    </CodeGroup>
  </Tab>
  <Tab title="Flutter">
    <CodeGroup>
      <CodeBlock>
        {`https://gist.github.com/amythee/859934e8745bc50d05e4946aa8b36064`}
      </CodeBlock>
    </CodeGroup>
  </Tab>
</Tabs>

<Info>
In this example, we show a text post with mention. However the pattern of adding mention to a post; is the same for all post types. You can apply the same creation process to the desired post type.
</Info>

## Update Post with Mentions

We provide developers with an efficient method for updating posts with mentions of specific users, you can easily add mentions to their post updates and but it will not notify the relevant users.

To remove mentions you can provide an empty JSON object for the metadata parameter, and an empty list for the mention users parameter. By doing so, You can easily remove mentions from the post content, while ensuring that the overall structure of the post remains intact.

<Tabs>
  <Tab title="iOS">
    <CodeGroup>
      <CodeBlock>
        {`https://gist.github.com/amythee/3d3e77b061bda67009cfcd64e65e5c25`}
      </CodeBlock>
    </CodeGroup>
    <CodeGroup>
      <CodeBlock>
        {`https://gist.github.com/amythee/f2a7a733fe13cd5e54bb229a9e2cb5c2`}
      </CodeBlock>
    </CodeGroup>
  </Tab>
  <Tab title="Android">
    When updating a text or video post with mentions, you can provide the `JsonObject` for the `metadata` parameter and provide the list of `userId` for the `mentionUsers` parameter.

    <CodeGroup>
      <CodeBlock>
        {`https://gist.github.com/amythee/44b6de55e72f3c8fe0d66157854443fd#file-amityposttextmentionremoval-kt`}
      </CodeBlock>
    </CodeGroup>
  </Tab>
  <Tab title="TypeScript">
    <CodeGroup>
      <CodeBlock>
        {`https://gist.github.com/amythee/c1edab83de93de27c7381e72a741bdf4#file-updatementionpost-ts`}
      </CodeBlock>
    </CodeGroup>
  </Tab>
  <Tab title="Flutter">
    <CodeGroup>
      <CodeBlock>
        {`https://gist.github.com/amythee/5e1cc562ec788a51117a7fc4f04ea14d/`}
      </CodeBlock>
    </CodeGroup>
  </Tab>
</Tabs>

## Render Mentions

To render mentions in a supported feature, please refer to [#render-mentions](../../core-concepts/mentions.md#render-mentions "mention"), specifically the section on handling mentions. This documentation provides detailed information on how to represent mentions in your application, including information on metadata structure, custom mention objects, and rendering support.