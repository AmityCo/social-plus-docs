---
hidden: true
---

# User Unread Count

## User Unread Count

This function enables users to obtain the current user's total count of unread messages and their mention status across all channels and sub-channels. To retrieve this value, utilize the CoreClient and follow the code pattern below. Please note that the user unread count does not guarantee real-time updates; a delay can be expected.

<Tabs>
  <Tab title="iOS">
    <CodeBlock url="https://gist.github.com/amythee/ce27ed17e596a0e7b701575666858803" />
  </Tab>
  <Tab title="Android">
    <CodeBlock url="https://gist.github.com/amythee/9e03b5d65305c2df92cca889fd1b7044" />
  </Tab>
  <Tab title="TypeScript">
    <CodeBlock url="https://gist.github.com/amythee/0116bf39405465363aadc00901f2eb23" />
    <Info>Please note that the TypeScript SDK does not yet support retrieving mention status information with this function.</Info>
  </Tab>
</Tabs>