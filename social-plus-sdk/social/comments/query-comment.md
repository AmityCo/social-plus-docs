# Query Comment

The ability to query comments and their replies is essential for creating a robust and user-friendly commenting experience. By using the `getComments()` method and passing in the appropriate parameters, you can retrieve the comments and replies that are most relevant to your users.

### **Comment Replies**

The query returns a LiveCollection of all matching comments available. To retrieve replies to a specific comment, you can pass the `commentId` as the `parentId`. If you want to retrieve parent-level comments, pass `parentId = null`. If you omit the `parentId`, you'll receive all comments on all levels.

### **Deletion Filter**

You can also use the `includeDeleted()` method to query for deleted comments and their replies. By passing `true` or `false` to this method, you can include or exclude deleted comments from the results.

{% hint style="info" %}
Note that if you use the `includeDeleted()` method, you don't need to check the `isDeleted()` method in the `AmityComment` object for deleted comments.
{% endhint %}

The `referenceType` parameter specifies where the comment is made and helps filter the comments based on the type of content. Possible values include:

* **`post`**: Comments on posts.
* **`story`**: Comments on stories.
* **`content`**: Comments on other types of content (e.g., images, videos, etc.).

***

### How to Query Comments

To query comments, provide the `referenceType` and `referenceId`. You can also include additional filters like `parentId`, `includeDeleted`, and `orderBy` to control the results.

To query comments for a post (including replies and excluding deleted comments):

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/0616ce28dba38ae160fcbd5d9440319d#file-query_comments-swift" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/561dac587a9b3a145e9036cd497f2cc1" %}
{% endtab %}

{% tab title="JavaScript" %}
{% embed url="https://gist.github.com/amythee/d93677807c7dc09819a8a97d92fdf3b5#file-querycomments-js" %}

### Pagination

When querying comments, you cannot set `limit`, `skip`, `after`, `first`, `before`, and `last` parameters. By default, the number of items in each page is 20. To handle pagination to load more comments, refer to Pagination in Live Collections.
{% endtab %}

{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/cc931634917fb3cd1995247ac5314a65" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/5c680bbc0f6a10357ed589fcd6cd3534#file-amitycommentquery-dart" %}
{% endtab %}
{% endtabs %}

{% hint style="info" %}
Refer to [#create-comment](./#create-comment "mention") for a more detailed explanation of the `referenceType` parameter.
{% endhint %}

## Query Comments with Images

To query for image comments only, you can use the `dataTypes` parameter and pass the value `TEXT` , `IMAGE`, or both.  There are two options for the `dataTypes` parameter: `any` and `exact`.&#x20;

* `any` - When you use the `any` option, the retrieved comments will include any comment that contains at least one of the specified data types. For example, if you pass `[image, text]`, the retrieved comments may contain only image content, only text content, or both image and text content.
* `exact` - On the other hand, when you use the `exact` option, the retrieved comments will include only comments that contain all of the specified data types. For example, if you pass `[image, text]`, the retrieved comments must contain both image and text content. If you pass `[image]`, the retrieved comments must contain only image content.\


To query for comments containing only image content:

{% tabs %}
{% tab title="iOS" %}
Using exact filer parameter:

{% embed url="https://gist.github.com/amythee/758c532a0af8ad1fa0abe6e9639f75b0" %}

Using any filter parameter:

{% embed url="https://gist.github.com/amythee/2c68e2e05007954b457bdc440edb5068" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/561dac587a9b3a145e9036cd497f2cc1" %}
{% endtab %}

{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/a4904ccd0dc001f22bf992cccec7e4a0" %}
{% endtab %}

{% tab title="Flutter" %}
The functionality isn't currently supported by this SDK.
{% endtab %}
{% endtabs %}

_Refer to the following_ [_Limitations_](create-comment.md#limitations) _on the use of images in comments._
