---
description: This component provides a feed of messages
---

# Live Chat Message List Component

This component enables user to view and interact with messages in the channel as well as real time addition of new messages.

<figure><img src="../../../../../../.gitbook/assets/Screenshot 2567-04-10 at 23.13.48.png" alt=""><figcaption></figcaption></figure>

## Features

| Feature                | Description                                                               |
| ---------------------- | ------------------------------------------------------------------------- |
| View messages          | View past and real time messages in the channel                           |
| Interact with messages | Trigger possible actions on each message such as copy, reply, and delete  |

### Customization

<table><thead><tr><th width="213">Config ID</th><th width="113">Config Key</th><th width="121">Type</th><th>Description</th></tr></thead><tbody><tr><td><code>live_chat/message_list/*</code></td><td><code>theme</code></td><td>Component</td><td>You can customize component theme</td></tr></tbody></table>

For more details on customization, please refer to the [Customization](../../../../customization/) page.

## Usage

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/03bb469f0ff5521b8d5d84401cf92613" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/5c3b9401734f0666a1ce03e91c141e6a" %}
{% endtab %}

{% tab title="React Native" %}
Code snippets will be available soon
{% endtab %}

{% tab title="React" %}
```tsx
import React, { useState } from 'react';
import { AmityLiveChatMessageList } from '@amityco/ui-kit';

interface SampleLiveChatMessageListProps {
  channel: Amity.Channel
}

const SampleLiveChatMessageList = ({ channel }: SampleLiveChatMessageListProps) => {
  // Passing channel model
  const [replyMessage, setReplyMessage] = useState<Amity.Message | undefined>(undefined);
  return (
    <AmityLiveChatMessageList
      channel={channel}                 // channel model
      replyMessage={setReplyMessage}    // function to set reply message
    />
  );
}

export default SampleLiveChatMessageList;

```
{% endtab %}
{% endtabs %}
