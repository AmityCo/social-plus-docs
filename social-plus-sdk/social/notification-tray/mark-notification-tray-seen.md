# Mark Notification Tray Seen

Use `markTraySeen()` to update the tray’s seen timestamp on the server when the user visits the Notification Tray screen.

This method supports global-level read tracking, separate from per-item seen state. Once invoked, future calls to `getNotificationTraySeen()` will return the new `isSeen` value. It is recommended to call this method as soon as the tray UI is opened.

<figure><img src="../../../.gitbook/assets/Explore.jpg" alt=""><figcaption><p>Have new notification</p></figcaption></figure>

<figure><img src="../../../.gitbook/assets/My Communities.jpg" alt=""><figcaption><p>Notification already seen</p></figcaption></figure>

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/b48d79ffc410f8d55c1b9bb759b1bf73" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/48cf5214b0007d4fee540b53bab5f2c2" %}
{% endtab %}

{% tab title="Web" %}
{% embed url="https://gist.github.com/amythee/fda232837ec10e401fccacd386006815" %}


{% endtab %}
{% endtabs %}
