# Message Delivery Status

## Mark Message as Delivered

When you send a message to someone, it's important to know whether that message has been delivered to the recipient's device or not. This is where the "Mark message delivered" function comes in.

By calling this function, you can update the status of a message to "delivered", which indicates that the message has been successfully delivered to the recipient's device. This can be useful for ensuring that important messages have been received by the intended recipient.

The parameters for this function are:

* `subchannelId`: The ID of the subchannel where the message is located.
* `messageId`: The ID of the message you want to mark as delivered.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/5d4485451f024e3a9b5d4b4318e29857" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/afffd2ad6bc3764bb3c105c538b4ab50" %}
{% endtab %}

{% tab title="TS" %}
{% embed url="https://gist.github.com/e56af3afdf4fb7917d22c8e53d873984" %}
{% endtab %}
{% endtabs %}

## Get Message's Read Users

In a chat application, it is often necessary to track which users have read a message. The Get Message's Read User function allows developers to retrieve a list of users who have read a particular message. This function can be useful for a variety of purposes, such as displaying read receipts or tracking user engagement with a particular message.

To use this function, you can call the `getMessageReadUsers` method, this will return a collection of users who have read the message.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/15179b4e495d435e727c3840181c0e4d" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/179950ae46b08777fe4cf04c4c2f2af0" %}
{% endtab %}

{% tab title="TS" %}
{% embed url="https://gist.github.com/amythee/d7e2970b2dbbb7f0aeaa8a076b96e821" %}
{% endtab %}
{% endtabs %}

## Get Message Delivered Users

It is also important for users to know whether their messages have been successfully delivered to the intended recipients. The "Get message's delivered user" function allows users to query the list of users who have marked a particular message as delivered. This feature can be useful in scenarios where users need to know whether their messages have reached their intended recipients, such as in a customer service application or a team collaboration tool.

The function takes a message ID as a parameter and returns a collection of user objects that have marked the message as delivered. By observing the live collection, users can receive real-time updates as new users mark the message as delivered.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/23b2de952bb2022324eba1eb90f3ef8b" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/492d1badecc0b432cc8f88a9cc9ee671" %}
{% endtab %}

{% tab title="TS" %}
{% embed url="https://gist.github.com/amythee/afbb37ff8b33894b61655fdd8d78c485" %}
{% endtab %}
{% endtabs %}
