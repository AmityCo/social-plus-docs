# Channel Unread Count

## Channel unread count

The SDK provides a simple way for clients to retrieve the unread count for a channel. To view the unread count for a channel, we can get it from a channel object. This count represents the number of messages that you have not yet read in that channel.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/eada692cbdc71ba0c191a30ba0c5de9f" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/8505762b042deef4386c156f21828f7f" %}
{% endtab %}

{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/amythee/29014cf92fd7a8ad58f8c06e54a5c5e8" %}
{% endtab %}
{% endtabs %}

#### Total unread count of all channels

Gets the total unread count of all channels. This only includes unread count from default subChannel of the channels that are already cached after being fetched from the server and excludes all.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/2c65a499d41693fad84df64124b9a6da" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/407c64361d2608200de8493bc4421029" %}
{% endtab %}

{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/11c02a34eb2a9176f6746b213ff0a824" %}
{% endtab %}
{% endtabs %}

#### Check unread count support for channel

To check if a channel supports the Unread Count feature, you can use the following code:

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/a39bd0734313e9fe15bd860d57c13301" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/436f9aecf5cc2312676e430b22267df7" %}
{% endtab %}

{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/amythee/bfc68d89e077a0ddbdefdeb29aa24e19" %}
{% endtab %}
{% endtabs %}

#### Channel Mention Status

To get the mention status of the current user in a channel, developers can use the following code.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/ce27ed17e596a0e7b701575666858803" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/11f1bdcd3191f6feed43b57c301e7346" %}
{% endtab %}

{% tab title="Typescript" %}
{% embed url="https://gist.github.com/amythee/2d0faa71a1aef95455488df8944862fa" %}
{% endtab %}
{% endtabs %}

#### Subchannel Mention Status

To get the mention status of the current user in a sub channel, developers can use the following code.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/afda77cd80db82a5f9c303290cbe443f" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/5d47c39913b0440dbe898ae807562f8e" %}
{% endtab %}

{% tab title="Typescript" %}
{% embed url="https://gist.github.com/f03db78e88b0d248854bd006a8a3fe36" %}
{% endtab %}
{% endtabs %}
