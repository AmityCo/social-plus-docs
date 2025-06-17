---
description: >-
  This component enable uses to view reactions and the users who reacted on
  messages.
---

# Reaction List Component

Users can react (add or remove reactions) to the message and can also view the list of users who reacted to the message along with their reaction.&#x20;

<figure><img src="../../../../../../.gitbook/assets/IdleStage (2) (1).png" alt=""><figcaption></figcaption></figure>

### Features:

| Feature       | Description                                                 |
| ------------- | ----------------------------------------------------------- |
| Reaction List | Users can view the list of user who reacted on the message. |



### Customization

| Config ID                   | Config Key | Type      | Description                       |
| --------------------------- | ---------- | --------- | --------------------------------- |
| `live_chat/message_list/`\* | theme      | Component | You can customize component theme |

### Usage:

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/1f12a6f1128d445c31d3c5bb2a97bb42" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/95bb12b0e79a0fb35593c8ed629c9193" %}
{% endtab %}

{% tab title="React" %}
```tsx
import { AmityReactionList } from '@amityco/ui-kit';
import React from 'react';

interface SampleAmityReactionListProps {
  referenceId: string;
  referenceType: Amity.ReactableType;
}

const SampleAmityReactionList = ({ referenceId, referenceType }: SampleAmityReactionListProps) => {
  return <AmityReactionList referenceId={referenceId} referenceType={referenceType} />;
};

export default SampleAmityReactionList;
```
{% endtab %}
{% endtabs %}
