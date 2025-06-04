---
hidden: true
---

# User Unread Count

## User Unread Count&#x20;

This function enables users to obtain the current user's total count of unread messages and their mention status across all channels and sub-channels. To retrieve this value, utilize the CoreClient and follow the code pattern below. Please note that the user unread count does not guarantee real-time updates; a delay can be expected.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/ce27ed17e596a0e7b701575666858803" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/9e03b5d65305c2df92cca889fd1b7044" %}
{% endtab %}

{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/amythee/0116bf39405465363aadc00901f2eb23" %}

{% hint style="info" %}
Please note that the TypeScript SDK does not yet support retrieving mention status information with this function.
{% endhint %}
{% endtab %}
{% endtabs %}
