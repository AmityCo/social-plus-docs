---
description: This page provides  a full functionalities of live chat
---

# Live Chat Page

This page offers full functionalities live chat by integrating 3 components; Header, Message List & Compose Bar. It enables users to create and interact with real time messages.

<figure><img src="../../../../../.gitbook/assets/Screenshot 2567-04-10 at 22.24.08 (1).png" alt=""><figcaption></figcaption></figure>



## Features

| Feature                   | Description                                |
| ------------------------- | ------------------------------------------ |
| Live Chat functionalities | A page with full live chat functionalities |

### Customization

<table><thead><tr><th width="213">Config ID</th><th>Config Key</th><th width="102">Type</th><th>Description</th></tr></thead><tbody><tr><td><code>live_chat/*/*</code></td><td><code>theme</code></td><td>Page</td><td>You can customize page theme</td></tr></tbody></table>

For more details on customization, please refer to the [Customization](../../../customization/) page.

## Usage

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/9555ad235d07e64633dcdaa643ad3e8f" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/eeffb4ac4c8d216bde9eda314c71f7f3" %}
{% endtab %}

{% tab title="React" %}
```tsx
import React from 'react';
import { AmityLiveChatPage } from '@amityco/ui-kit';

interface SampleLiveChatPageProps {
  channelId: Amity.Channel['channelId']
}

const SampleLiveChatPage = ({ channelId }: SampleLiveChatPageProps) => {
  // Passing channelId to the component
  return <AmityLiveChatPage channelId={channelId} />
}

export default SampleLiveChatPage;

```
{% endtab %}
{% endtabs %}
