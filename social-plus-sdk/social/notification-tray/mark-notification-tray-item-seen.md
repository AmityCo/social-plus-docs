# Mark Notification Tray Item Seen

The notification tray item `markSeen()` method updates the **seen status** of a specific notification tray item, enabling **fine-grained read tracking**. Use this when a user clicks or interacts with an individual notification.

Each tray item has its own `lastSeenAt` timestamp, which is recorded on the server when this method is called.&#x20;

<figure><img src="../../../.gitbook/assets/Screenshot 2568-04-22 at 15.35.51.png" alt=""><figcaption></figcaption></figure>

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/a500c2aa6aae8a297fc1b455b9846415" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/d30a5e56453605fc251d69db3aee0d2b" %}
{% endtab %}

{% tab title="Web" %}
{% embed url="https://gist.github.com/amythee/7c6f101747dee76f3d10b4bdc2ae4b2c" %}


{% endtab %}
{% endtabs %}
