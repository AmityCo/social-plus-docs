# Mark Message as Read

Marking a message as read is a crucial functionality to update the read count and provide an accurate representation of the user's interaction with messages. The SDK provides a method to manually mark a specific message as read.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/71f3879678c871e131d3b7c60af0fa36" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/d0ddb72c1be866b55d6e97455831f2c2" %}
{% endtab %}

{% tab title="TS" %}
{% embed url="https://gist.github.com/amythee/c19c8885f6f9f2c276b1b3a1f5d2cad0" %}
{% endtab %}
{% endtabs %}

This action should be taken when entering the chat room or a new message appears in the chatroom UI, and the user has viewed the message.

To maintain accuracy in the read count, it is recommended to mark only the latest message as read. This ensures that the counts reflect the user's most recent interaction with the chat.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/2985d6df8b76f9b9aee1fbeeeeae98a3" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/17c32fa5caedc2fe0f9854a1ccc0144a" %}
{% endtab %}

{% tab title="TS" %}
{% embed url="https://gist.github.com/amythee/5324edeb4469cd569a81bb7063762819" %}
{% endtab %}
{% endtabs %}
