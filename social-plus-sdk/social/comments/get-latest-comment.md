# Get Latest Comment

The Social Plus SDK offers the `getLatestComment` method, allowing you to fetch the most recent comment by a reference within your application. Integrating this feature enhances the user experience by keeping them informed about the latest interactions among users.

Using the `getLatestComment` method is straightforward: simply implement it to retrieve the latest comment by a reference, streamlining the process of accessing up-to-date information. Furthermore, the method returns a [Live Object](../../core-concepts/live-objects-collections/) that you can observe for real-time updates once [realtime-events](../../core-concepts/realtime-events/ "mention") are subscribed, ensuring your app stays current with the latest comments and fostering a more interactive environment.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/389121f867795b90667f7c68b82adce1" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/34939b243556927a416fa190a3cae4f5" %}
{% endtab %}

{% tab title="TypeScript" %}
Unsupported ❌
{% endtab %}

{% tab title="Flutter" %}
Supported ✅ (Please wait while we prepare a real example!)
{% endtab %}
{% endtabs %}

{% hint style="info" %}
Refer to [Comment reference type](./#comment-description) for a more detailed explanation of the reference type parameter.
{% endhint %}
