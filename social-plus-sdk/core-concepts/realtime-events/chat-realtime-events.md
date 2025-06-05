# Chat Realtime Events

In the context of channels, subchannels, and message collections, receiving real-time events is an automatic process for **conversation and community** channels; you do not need to perform any additional actions. However, a live channel still needs to be established.

Similar to the process for social real-time events, a topic is a unique path that must be constructed for each model you wish to receive updates about in real-time. The SDK offers helper methods for creating these topics for each model type. Each topic includes an events enum that developers can select to subscribe to, based on their business context and preferences.

To receive updates from a channel or any content created within that channel, the user must hold a 'Member' status within that channel. Once the user leaves the channel, they will no longer receive real-time events.

### Subchannel Topic

<Tabs>
  <Tab title="iOS">
    <CodeGroup>
      <CodeBlock>
        ```swift
        https://gist.github.com/amythee/e2942c227c355a8139073eb140c90155#file-subscribe_subchannel-swift
        ```
      </CodeBlock>
    </CodeGroup>
  </Tab>
  <Tab title="Android">
    <CodeGroup>
      <CodeBlock>
        ```java
        https://gist.github.com/amythee/b498c3659a273eb08dc8c210c7d38f64
        ```
      </CodeBlock>
    </CodeGroup>
  </Tab>
  <Tab title="JavaScript">
    We don't support this feature in JS SDK.
  </Tab>
  <Tab title="TypeScript">
    Version 6 and Beta(v0.0.1)

    <CodeGroup>
      <CodeBlock>
        ```typescript
        https://gist.github.com/amythee/7ec2e92438c22a432eceaf411a06f701#file-subscribesubchannel-ts
        ```
      </CodeBlock>
    </CodeGroup>
  </Tab>
  <Tab title="Flutter">
    The functionality isn't currently supported by this SDK.
  </Tab>
</Tabs>