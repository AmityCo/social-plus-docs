# Poll

The Social Plus SDK encompasses comprehensive support for polls, offering developers an effortless way to incorporate polls into their social applications. Polls enable users to create and participate in a diverse range of topics, sparking targeted engagement and conversations among users.

To integrate poll functionality, developers can utilize the poll features offered by the Social Plus SDK in their applications. Polls can be tailored to meet specific needs, including options for single or multiple-choice polls, setting poll expiration dates, and more. Users can then participate in the poll by choosing their preferred option. At present, the Social Plus SDK only supports the integration of polls within posts, please refer to - [#create-poll-post](../social/posts/create-post/poll-post.md#create-poll-post "mention"), [#poll-post](../social/posts/viewing-post-content.md#poll-post "mention").&#x20;

## Create Poll&#x20;

&#x20;As demonstrated in the code sample below, here's a way to create a poll in the poll post.

Polls can be created with the following settable controls:

* `question`  - A question that can be up to 500 characters long.
* `answer` - A set of two to ten answers. Each answer can be up to 200 characters long.
* `answerType` - Indicates whether the survey allows multiple choices. The available options are `Single` (default) and `Multiple`.
* `timeToClosePoll` - A time window limiting how long the poll will be open. By default, the `setTimeToClosePoll` value is set to 30 days if no value has been set for it.&#x20;

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/78313a66ea1f4da62a05e9f501d7f975" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/add885da0ef8f30e2531a07bc471bd82" %}
{% endtab %}

{% tab title="JavaScript" %}
{% embed url="https://gist.github.com/amythee/408686f116cda4ba97ba7cf155db82d6#file-createpoll-js" %}
{% endtab %}

{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/amythee/b69bd08bd795f3be7c03af10d11e615e#file-createpoll-ts" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/7ad2ce65b2a60bf8117ba323093087d7" %}
{% endtab %}
{% endtabs %}

## Vote Poll

This function enables you to cast a single vote and the vote cannot be revoked. If the poll type is multiple, you have the option to select multiple choices.

Here's an explanation of the method's parameters:

* `pollId`: This is a required parameter of type `String`, which represents the ID of the poll that the user wants to vote on.
* `answerIds`: This is a required parameter of the type `Array<String>`, which represents an array of IDs of the answer options that the user wants to vote for. Users can select one or multiple answers depending on the poll's configuration.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/70faebf29f7c3cb02be42ee8ee875640" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/f917358e4fef92a3a3469016ac8a0c89" %}
{% endtab %}

{% tab title="JavaScript" %}
{% embed url="https://gist.github.com/734ae5ee009924bc3084ad2aad221047" %}
{% endtab %}

{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/amythee/7935880990ec012be24b27cc5f7a9479#file-votepoll-ts" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/3d8b0d27f79c4742dec10ef781d622fb#file-amitypollvote-dart" %}
{% endtab %}
{% endtabs %}

## Close Poll

The ability to close a poll is restricted exclusively to individuals who have ownership permissions, such as the creator of the poll or an administrator. It is important to note that a poll can only be closed before its designated closing time.

Here's an explanation of the method's parameters:

* `pollId`: This is a required parameter of type `String`, which represents the ID of the poll that the user wants to close.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/fd1bdfa71ea2fd0464c5a589c8890966" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/1dbb479b966f1d67eeac8b2d221a1a31" %}
{% endtab %}

{% tab title="JavaScript" %}
```javascript
closePoll = async (pollId: string) => Promise<any>
```
{% endtab %}

{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/amythee/8112f21e19e1a56c40792d8ae8040d04#file-closepoll-ts" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/174927622226e41d2c8eca6f8c7053a5#file-amitypollclose-dart" %}
{% endtab %}
{% endtabs %}

## Delete Poll

The deletion of a poll is limited exclusively to individuals who possess ownership permissions, such as the creator of the poll or an administrator.

Here's an explanation of the method's parameters:

* `pollId`: This is a required parameter of the type `String`, which represents the ID of the poll that the user wants to delete.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/d146d94ad86bfdea2cb6bfcf9d7eea62" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/33db2b508c367f004af699b79184031f" %}
{% endtab %}

{% tab title="JavaScript" %}
Supported ✅ (Please wait while we prepare a real example!)
{% endtab %}

{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/amythee/a663fc514c5c1894fedfbb2c4411dc5f#file-deletepoll-ts" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/62460daf28e4107b6f35188b1893de1c#file-amitypolldelete-dart" %}
{% endtab %}
{% endtabs %}
