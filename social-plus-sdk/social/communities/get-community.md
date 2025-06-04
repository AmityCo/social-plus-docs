# Get Community

Users can retrieve information about the community, such as the community name, description, and member count, without actually becoming a member of the community. This provides a way for users to explore their community options and find the communities that are most relevant and engaging to them.

To fetch a community's data without joining, users can simply call the `getCommunity` method within the SDK and provide the relevant parameter, such as the community ID. The retrieved result is returned as a live object of a post. For more information on live objects, please refer to [live-objects-collections](../../core-concepts/live-objects-collections/ "mention").

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/05d62202ded153e283c5ec376937eeba#file-get-a-community-swift" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/4a094c77a6102c77430650fdd78aea7e#file-amitycommunityget-kt" %}
{% endtab %}

{% tab title="JavaScript" %}
{% embed url="https://gist.github.com/amythee/230f3d6d4f179c4fe0f87cad3f7a8447#file-communityforid-js" %}
{% endtab %}

{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/amythee/6553b70a51076ef0eddd465fa2da96dc#file-getcommunity-ts" %}
{% endtab %}

{% tab title="Flutter" %}
In order to get live update from any changes or bind with `StreamBuilder` widget, you can alternatively use `AmityCommunity.listen`

{% embed url="https://gist.github.com/amythee/66260e02d79d4892a6fe5d7af0d3c1be#file-amitycommunityview-dart" %}
{% endtab %}
{% endtabs %}
