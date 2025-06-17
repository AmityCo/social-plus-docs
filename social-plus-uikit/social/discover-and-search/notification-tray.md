# Notification Tray

The **Notification Tray** in Social Plus UIKit v4 is a centralized feature designed to enhance user engagement by providing a comprehensive history of notifications. It automatically creates and groups notification records for each user, ensuring they stay informed about relevant activities within their communities.​

By aggregating interactions such as mentions, comments, and community activities, the Notification Tray not only keeps users updated but also encourages them to explore new content and engage more deeply with the platform. This proactive approach to content surfacing enhances user experience and fosters a more interconnected community.

<figure><img src="../../../../.gitbook/assets/Screenshot 2568-04-22 at 15.35.51.png" alt=""><figcaption></figcaption></figure>

Usage:

The `AmityNotificationTrayPage` is designed for easy integration across various platforms, enabling a consistent user experience by displaying a notification tray item.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/ede091569788d9bd7687afed87b0d948" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/e9c53c9a6ab165dea8c20645f82f5ae8" %}
{% endtab %}

{% tab title="Web" %}
{% embed url="https://gist.github.com/amythee/42d2e9ee57301500c0ff03c843e45437" %}


{% endtab %}
{% endtabs %}

#### Customization:

| Config ID                                         | Type    | Description                                                                        |
| ------------------------------------------------- | ------- | ---------------------------------------------------------------------------------- |
| `notification_tray_page/*/*`                      | Page    | You can customize page `theme`                                                     |
| `notification_tray_page/*/back_button`            | Element | You can customize `image`                                                          |
| `notification_tray_page/*/title`                  | Element | You can customize `text`                                                           |
| `notification_tray_page/*/empty_notification`     | Element | <p>You can customize <code>image</code><br>You can customize <code>text</code></p> |
| `notification_tray_page/*/no_internet_connection` | Element | <p>You can customize <code>image</code><br>You can customize <code>text</code></p> |

**Navigation Behavior**

The behavior of the `AmityNotificationTrayPage` can be customized to handle navigation to the `AmityPostDetailPage` and `AmityCommunityProfilePage` differently. Here’s how you can override the default behavior:

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/b2e2897890a5b6dfe89e4c26c54bfaa5" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/1cca4c2ac199d8aa91a1b0303b76fb54" %}
{% endtab %}

{% tab title="Web" %}


{% embed url="https://gist.github.com/amythee/67c7a8fe31a6023f4dcee873f5bfa451" %}
{% endtab %}
{% endtabs %}
