# Create Community

Our SDK provides a convenient way to create a new community on our platform, with several parameters available to customize the community.

* `displayName` - allows users to set the public display name of the community, which will be visible to other users who can access the community.
* `description` - allows users to describe the community, which can help other users understand the purpose and focus of the community.
* `isPublic` - is used to specify the type of the community. Setting it to `false` will create a private community, while setting it to `true` will create a public community.
* `postSettings` - allows users to customize the [community post settings](broken-reference). This parameter can be used to configure how posts are moderated within the community, depending on the specific needs and preferences of the community creator.
* `storySettings` - allows users to customize the community story settings. This parameter can be used to configure whether to enable comment interaction on stories.
* `metaData` - allows users to include additional properties to support custom fields within the community. This can be useful for creating communities with specific requirements or features that are not available by default in our platform.

<Tabs>
  <Tab title="iOS">
    <CodeGroup>
      <CodeBlock>
        https://gist.github.com/amythee/5721a8281522f046e4d3a73034f65580
      </CodeBlock>
    </CodeGroup>
  </Tab>
  <Tab title="Android">
    <CodeGroup>
      <CodeBlock>
        https://gist.github.com/12032a9611e14acb6dd0775dea3c787c
      </CodeBlock>
    </CodeGroup>
  </Tab>
  <Tab title="JavaScript">
    #### Create Community

    <CodeGroup>
      <CodeBlock>
        https://gist.github.com/amythee/81c7a938edbc745d39e836fcba314081#file-createcommunity-js
      </CodeBlock>
    </CodeGroup>
  </Tab>
  <Tab title="TypeScript">
    <CodeGroup>
      <CodeBlock>
        https://gist.github.com/amythee/56e9a0a0d9e9fc4a24fc8377567630f0#file-createcommunity-ts
      </CodeBlock>
    </CodeGroup>
  </Tab>
  <Tab title="Flutter">
    #### Create Community

    <CodeGroup>
      <CodeBlock>
        https://gist.github.com/amythee/551def9b265419880d996d8bdfe8dc6c#file-amitycommunitycreation-dart
      </CodeBlock>
    </CodeGroup>

    Please note that Flutter doesn't support updating post settings yet.
  </Tab>
</Tabs>