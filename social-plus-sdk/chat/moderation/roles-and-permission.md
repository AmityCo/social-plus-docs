# Roles and Permission

Social Plus uses roles and permissions to provide users the ability to fully customize the moderation experience on the platform. To learn more about Social Plus SDKs default roles and permissions, refer to the [Roles & Permissions](../../core-concepts/user/user-permission.md) page.

## Roles

The creator of the channel can add and remove the role of a user via `AmityChannelModeration`.

<Tabs>
  <Tab title="iOS">
    <CodeGroup>
      <CodeBlock>
        https://gist.github.com/amythee/b24586acdfd7cf8678cfd127c2efa32b
      </CodeBlock>
    </CodeGroup>
  </Tab>
  <Tab title="Android">
    <CodeGroup>
      <CodeBlock>
        https://gist.github.com/amythee/df2dee57ce5c28e01e64482a0dcc275b
      </CodeBlock>
    </CodeGroup>
  </Tab>
  <Tab title="TypeScript">
    Version 6
    <CodeGroup>
      <CodeBlock>
        https://gist.github.com/e98ba676e99c507dec6851afad050fc0
      </CodeBlock>
    </CodeGroup>
    Beta (v0.0.1)
    <CodeGroup>
      <CodeBlock>
        https://gist.github.com/7da39ab97af3717c203481e5a9f826dc
      </CodeBlock>
    </CodeGroup>
  </Tab>
  <Tab title="Flutter">
    <CodeGroup>
      <CodeBlock>
        https://gist.github.com/amythee/0a12c57735cb8828f0439a240e07b1c6
      </CodeBlock>
    </CodeGroup>
  </Tab>
</Tabs>

<Info>
1. The channel creator is automatically assigned as the channel moderator.
2. The previous/last moderator is not allowed to leave a community and an error is displayed.
3. The channel moderator can promote a user/member to a moderator.
4. The channel moderator can demote a moderator to a user/member.

This applies only to Live and Community channels'. This does not apply to the Conversation Channel.
</Info>

## Permission

You can check your permission in the channel by sending `AmityPermission` enums to `AmityCoreClient.hasPermission(amityPermission)`.

<Tabs>
  <Tab title="iOS">
    <CodeGroup>
      <CodeBlock>
        https://gist.github.com/amythee/01d711ffabf3100933cdc567200c82c4
      </CodeBlock>
    </CodeGroup>
  </Tab>
  <Tab title="Android">
    <CodeGroup>
      <CodeBlock>
        https://gist.github.com/amythee/8edbf9a5e1f699d5cc781f1bf05ba796
      </CodeBlock>
    </CodeGroup>
  </Tab>
  <Tab title="TypeScript">
    <CodeGroup>
      <CodeBlock>
        https://gist.github.com/amythee/e5c5d647346bf5faf3d713600f142814#file-checkchannelpermission-ts
      </CodeBlock>
    </CodeGroup>
  </Tab>
  <Tab title="Flutter">
    <CodeGroup>
      <CodeBlock>
        https://gist.github.com/amythee/cabd602e8aa1f9b1bd2bcbdd561f799b
      </CodeBlock>
    </CodeGroup>
  </Tab>
</Tabs>