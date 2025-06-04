# Update Community

The update community method works by providing moderators or a creator of the community with a way to modify various aspects of their community settings. For example, moderators can update the community name, description, or avatar to reflect changes in the community. They can also update the post settings to control who can create posts in the community.

* `displayName` - allows users to set the public display name of the community, which will be visible to other users who can access the community.
* `description` - allows users to describe the community, which can help other users understand the purpose and focus of the community.
* `isPublic` - is used to specify the type of the community. Setting it to `false` will create a private community, while setting it to `true` will create a public community.
* `postSettings` - allows users to customize the [community post settings](broken-reference). This parameter can be used to configure how posts are moderated within the community, depending on the specific needs and preferences of the community creator.
* `storySettings` - allows users to customize the community story settings. This parameter can be used to configure whether to enable comment interaction on stories.
* `metaData` - allows users to include additional properties to support custom fields within the community. This can be useful for creating communities with specific requirements or features that are not available by default in our platform.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/10352cff0d83feb488c2569b39993c8b" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/7f2519953bd29b021fee20e38dfcfca0" %}
{% endtab %}

{% tab title="JavaScript" %}
{% embed url="https://gist.github.com/amythee/44b8cf8c9b45443252ebe0acc2ee329e#file-updatecommunityneedapproval-js" %}
{% endtab %}

{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/amythee/7f57206dadb9a6fe241892d9794cc409#file-updatecommunity-ts" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/36e108c4787f70882408276a55756f4c#file-amitycommunityupdate-dart" %}

Please note that Flutter doesn't support updating post settings yet.
{% endtab %}
{% endtabs %}

{% hint style="info" %}
By default, only the original creator of the community or the system administrators can update the community.
{% endhint %}
