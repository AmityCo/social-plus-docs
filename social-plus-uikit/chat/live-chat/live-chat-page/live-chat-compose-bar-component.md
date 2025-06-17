---
description: This component enables message creation
---

# Live Chat Compose Bar Component

This component provides a full functionalities of message creation. It enables user to either create a new message or reply to another message with also an option to mention specific users.

<figure><img src="../../../../../.gitbook/assets/Screenshot 2567-04-10 at 23.28.02 (1).png" alt=""><figcaption></figcaption></figure>

## Features

| Feature                      | Description                                                        |
| ---------------------------- | ------------------------------------------------------------------ |
| Create message               | Enable message creation                                            |
| Mention other channel member | Enable '@' character to trigger a view to select a user to mention |

### Customization

<table><thead><tr><th width="213">Config ID</th><th width="183">Config Key</th><th width="113">Type</th><th>Description</th></tr></thead><tbody><tr><td><code>live_chat/message_compose_bar/*</code></td><td><code>theme</code></td><td>Component</td><td>You can customize component theme</td></tr><tr><td><code>live_chat/message_compose_bar/*</code></td><td><code>message_limit</code></td><td>Component</td><td>You can define maximum character</td></tr><tr><td><code>live_chat/message_compose_bar/*</code></td><td><code>placeholder_text</code></td><td>Component</td><td>You can define placeholder text on the compose bar </td></tr></tbody></table>

For more details on customization, please refer to the [Customization](../../../customization/) page.

## Usage

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/3c5ef92edcc4bd7f1744316cc1960b5e" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/ad90cc62e19eeea14892fd8fb2d75da4" %}
{% endtab %}

{% tab title="React" %}
```tsx
import React, { useRef, useState } from 'react';
import { AmityLiveChatMessageComposeBar } from '@amityco/ui-kit';

interface SampleLiveChatMessageComposeBarProps {
  channel: Amity.Channel,
}

const SampleLiveChatPage = ({ channel }: SampleLiveChatMessageComposeBarProps) => {
  const mentionSuggestionRef = useRef<HTMLDivElement>(null);
  const [replyMessage, setReplyMessage] = useState<Amity.Message | undefined>();
  const [mentionMessage, setMentionMessage] = useState<Amity.Message | undefined>();

  return (
    <>
      <div ref={mentionSuggestionRef}>
        {/* User suggestion panel will render here */}
      </div>

      {/**
       * Props detail:
       * - channel: Amity.Channel
       * - suggestionRef: React.RefObject<HTMLDivElement> // Ref from target div to render user suggestion panel
       * - composeAction: {
       *    replyMessage?: Amity.Message
       *    mentionMessage?: Amity.Message
       *    clearReplyMessage: () => void
       *    clearMention: () => void
       * }
       */}
      <AmityLiveChatMessageComposeBar
        channel={channel}
        suggestionRef={mentionSuggestionRef}
        composeAction={{
          replyMessage,
          mentionMessage,
          clearReplyMessage: () => setReplyMessage(undefined),
          clearMention: () => setMentionMessage(undefined),
        }}
      />
    </>
  )
}

export default SampleLiveChatPage;

```
{% endtab %}
{% endtabs %}
