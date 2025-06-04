# Pinned Post

Pinned posts empower community moderators to highlight key announcements, discussions, or content critical for community engagement. Social Plus maintains separate collections for pinned posts based on their intended placement, currently supporting `default`, `announcement`  and `global` placements.

{% hint style="info" %}
Currently supporting post pinning via ASC console
{% endhint %}

## Query pinned post

Pinned posts must be viewed first when users enter a community and scroll down the feed. To achieve this, the Social Plus SDK provides `getPinnedPost()` function, which offers a separate collection of posts to be rendered at the top of the community feed. This allows the community feed to recognize which posts have been rendered as pinned and optionally exclude those items from the main feed.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/5838fb1cec19595bd2411e5d94041b09" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/af48d5bf5b87b69a3fb9716151b5b397" %}
{% endtab %}

{% tab title="Typescript" %}
{% embed url="https://gist.github.com/amythee/6e88f7e2abc7260f14d007fc3786643e#file-querypinnedposts-ts" %}
{% endtab %}
{% endtabs %}

## Query announcements

Another type of pinned post is an `announcement`. These posts are tracked separately, similar to default pinned posts but with different behavior. Announcements are typically housed at the top of the community in a separate section, making them easily accessible without forcing users to go through every announcement. This type of pinned post is suitable for multiple important posts that need to be highlighted simultaneously, such as reminders, updates, or informational content.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/977457fa6c3cac37cf0e9b529fbed000" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/4f2628b0f9b586906f05e24a99483a8e" %}
{% endtab %}

{% tab title="Typescript" %}
{% embed url="https://gist.github.com/amythee/997e5671875134b60a29398bda855992" %}
{% endtab %}
{% endtabs %}

## Query global featured posts

Global featured posts keep your key content prominently displayed at the top of the main feed, the typical landing page on both web and app platforms. This ensures your announcements reach the entire in-app community, maximizing visibility. The `getGlobalPinnedPost()` function in the Social Plus SDK provides a dedicated collection of featured posts that are intended to appear at the top of the global feed, ensuring users see these posts first, regardless of community affiliation.

{% hint style="info" %}
To maintain a balanced feed with fresh content from your communities, we recommend limiting the number of posts featured globally.
{% endhint %}

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/0a28435f69b280efd622b318a1248fbf" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/b5a837e47250f8d77167b6902fe58ef6" %}
{% endtab %}

{% tab title="Typescript" %}

{% endtab %}
{% endtabs %}
