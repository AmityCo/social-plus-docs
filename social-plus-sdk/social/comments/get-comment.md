# Get Comment

The Social Plus SDK provides functionality that allows you to work with social features in your application, including the ability to retrieve a comment. In this section, we'll explore how to use the Social Plus SDK to retrieve a single comment from your application. By using a specific function provided by the SDK, you can retrieve a comment based on its ID, which provides a convenient way to access specific comment data. The retrieved result is returned as a live object of a comment. For more information on live objects, please refer to [live-objects-collections](../../core-concepts/live-objects-collections/ "mention").

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/0616ce28dba38ae160fcbd5d9440319d" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/7c2548bae1c8c3e4ba8963200da73937" %}
{% endtab %}

{% tab title="JavaScript" %}
Supported ✅ (Please wait while we prepare a real example!)
{% endtab %}

{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/c5094b2a975ff1ffb2f3e156d996d6f3" %}
{% endtab %}

{% tab title="Flutter" %}
Supported ✅ (Please wait while we prepare a real example!)
{% endtab %}
{% endtabs %}

To retrieve multiple comments, you can use `getCommentByIds` method provided by `CommentRepository`. This method accepts a collection of `commentId` as a parameter and returns a [Live Collection](../../core-concepts/live-objects-collections/) of`AmityComment`.&#x20;

{% tabs %}
{% tab title="iOS" %}
The functionality isn't currently supported by this SDK.
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/4ba2595192ac288823f5a22a90330312" %}
{% endtab %}

{% tab title="Javascript" %}
Supported ✅ (Please wait while we prepare a real example!)
{% endtab %}

{% tab title="Typescript" %}
Supported ✅ (Please wait while we prepare a real example!)
{% endtab %}

{% tab title="Flutter" %}
Supported ✅ (Please wait while we prepare a real example!)
{% endtab %}
{% endtabs %}
