---
description: This component displays channel info
---

# Live Chat Header Component

The component provides a visual representation of channel profile.

<figure><img src="../../../../../.gitbook/assets/Screenshot 2567-04-10 at 23.00.49.png" alt=""><figcaption></figcaption></figure>

## Features

| Feature              | Description                                              |
| -------------------- | -------------------------------------------------------- |
| Display channel info | Display channel's display name, avatar, and member count |

### Customization

<table><thead><tr><th width="233">Config ID</th><th width="120">Config Key</th><th width="123">Type</th><th>Description</th></tr></thead><tbody><tr><td><code>live_chat/chat_header/*</code></td><td><code>theme</code></td><td>Component</td><td>You can customize component theme </td></tr></tbody></table>

For more details on customization, please refer to the [Customization](../../../customization/) page.

## Usage

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/3ffeeb79032f77481b71123d6e8ee5d6" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/38c1960c262a167d9ae57eb1be59e007" %}
{% endtab %}

{% tab title="React" %}
```tsx
import React from 'react';
import { AmityLiveChatHeader } from '@amityco/ui-kit';

interface SampleLiveChatHeaderProps {
  channel: Amity.Channel
}

const SampleLiveChatHeader = ({ channel }: SampleLiveChatHeaderProps) => {
  // Passing channel model
  return <AmityLiveChatHeader channel={channel} />
}

export default SampleLiveChatHeader;

```
{% endtab %}
{% endtabs %}
