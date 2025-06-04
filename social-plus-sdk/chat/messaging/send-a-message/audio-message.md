# Audio Message

## Send an Audio Message

An audio message is a type of message that allows users to send and receive audio recordings in a chat or messaging application. Audio messages can be used to convey emotions, tone, or detailed information in a way that is not always possible with text messages or other types of media. They are a convenient and intuitive way to communicate with other users in real-time.

With the Social Plus Chat SDK, you can easily send and receive audio messages within your chat or messaging application. Simply provide the local path of the audio file to the `sendAudioMessage` method.

Here is a brief explanation of the function parameters:

* `text/caption`: A string that contains the text message that the user wants to send. This parameter is mandatory as it contains the actual message content.
* `attachment`: The local audio path that the user wants to send on the device
* `subchannelId`: An identifier for the subchannel where the message will be sent. Subchannels are subdivisions within a channel that represent individual topics or chat threads. Messages and interactions occur within subchannels, not the main channel itself.
* `tags` - Arbitrary strings that can be used for defining and querying the messages.

{% tabs %}
{% tab title="iOS" %}
**Version 6**

{% embed url="https://gist.github.com/amythee/99425dfbdc439d6f06f57aea3874f7e9" %}

**Version 5 (Maintained)**

{% embed url="https://gist.github.com/amythee/1a58160c86a5fe1ab8ea9488e323c19f" %}
{% endtab %}

{% tab title="Android" %}
**Version 6**

{% embed url="https://gist.github.com/amythee/09c7d9cbf4e5c029e3077b988cd4ab99" %}

**Version 5 (Maintained)**

{% embed url="https://gist.github.com/amythee/70006aa251fec068b7ab55a0485bc4ae" %}
{% endtab %}

{% tab title="JavaScript" %}
Sending audio messages uses the same steps as sending a file message. Refer to [File Message](file-message.md) page for more details.
{% endtab %}

{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/c4fadd828c02f7bad7172dd0edfaa8bf" %}
{% endtab %}
{% endtabs %}

{% hint style="warning" %}
Supported audio formats are MP3, and WAV and cannot exceed 1GB in size
{% endhint %}
