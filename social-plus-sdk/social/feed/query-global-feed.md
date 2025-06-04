# Query Global Feed

The SDK provides two ways for users to retrieve their global feed: the `getGlobalFeed` method and the `getCustomPostRanking` method. By providing these two distinct ways to retrieve the global feed, the SDK enables users to customize their content experience to better reflect their interests and preferences. This can help to foster a more dynamic and engaging community experience, promoting greater engagement and participation among users.

### **Conventional Global Feed Query**

We provide a simple way to query posts on Global Feed using the `getGlobalFeed` method. When using this method, posts will be returned in chronological order by default, allowing users to quickly and easily view the most recent content.

{% hint style="info" %}
The system does not guarantee the visibility of older posts — only the 20 most recent posts in a community are visible in the global feed.
{% endhint %}

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/e37f38f825c6fcccb002569a22e30ff0#file-get_global_feed-swift" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/b0c5eb11be4d526571d7d734c10d0ce0#file-amityfeedglobalfeedquery-kt" %}
{% endtab %}

{% tab title="JavaScript" %}
{% embed url="https://gist.github.com/amythee/91895dee5b1bf13e4fba964400079152" %}
{% endtab %}

{% tab title="TypeScript" %}
Version 6

{% embed url="https://gist.github.com/748bf40c03482f25c70c82c9dcea23ae" %}

Beta (v0.0.1)

{% embed url="https://gist.github.com/amythee/c78392b0d97ad074f6e5d22afff1d1b3#file-queryglobalfeed-ts" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/e588d9c4cfbaf490b115a87df2ec61fa#file-amityglobalfeedquery-dart" %}
{% endtab %}
{% endtabs %}

### **Custom Post Ranking Query**

Query custom post ranking is a smarter global feed that supports the score-sorting mechanism. The score-sorting mechanism ensures that the posts are presented in order of relevance, with the most engaging and relevant content at the top of the feed. Refer to[custom-post-ranking.md](custom-post-ranking.md "mention") for more information about this feature. You can use `getCustomRankingGlobalFeed` to retrieve posts from this functionality.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/4537f34bc1537c46483058907a4b55a7" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/f7ce1bbce85ff361404f73a42c5afb21#file-amityfeedcustomrankingglobalfeedquery-kt" %}
{% endtab %}

{% tab title="JavaScript" %}
You can retrieve your global feed by calling the `queryAllPosts` method. This method accepts the following parameters:

{% embed url="https://gist.github.com/amythee/a4015cf25e38fdf8fa17bcf10a5e01fe#file-queryfeeds-js" %}

The method will return a LiveCollection instance of post model.

{% hint style="warning" %}
The `queryAllPosts method` will throw an error if parameters passed are incorrect.
{% endhint %}
{% endtab %}

{% tab title="TypeScript" %}
Version 6

{% embed url="https://gist.github.com/a8bbbee37eb9fc85d937184cedefab73" %}

Beta (v0.0.1)

{% embed url="https://gist.github.com/amythee/c235a5829f229c694fa2532d9f70016e#file-queryglobalfeedwithcustomranking-ts" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/a0710374320b17096c269e4e5e953843" %}
{% endtab %}
{% endtabs %}
