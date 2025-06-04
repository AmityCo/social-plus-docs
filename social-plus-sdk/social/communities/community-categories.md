# Community Categories

The CommunityRepository also provides a way to manage community categories. When communities are placed into categories, users can easily sort and filter communities based on their category, allowing for more efficient and effective community management.

{% hint style="info" %}
**Note**: Categories can only be created and updated from the Social Plus Console.
{% endhint %}

## Get Category

To get a particular community category, users can utilize the `getCategory` method provided by the CommunityRepository. This method accepts a `categoryId` as a parameter and returns information about the specified category.

{% tabs %}
{% tab title="iOS" %}
The functionality isn't currently supported by this SDK.
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/702afc49c4ad0a1d293701f12dcfc0d1" %}
{% endtab %}

{% tab title="JavaScript" %}
{% embed url="https://gist.github.com/amythee/4d06a157504bdf661b1419aa7e072dda#file-categoryforid-js" %}
{% endtab %}

{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/amythee/5063c8807e2e07c82ddf5fddec8efdff#file-getcategory-ts" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/6f52edfcf116564d02dbb15edea95128" %}
{% endtab %}
{% endtabs %}

## Category Query

CommunityRepository also provides the `categoryQuery` method, which allows users to obtain the categories currently available on the system. This method returns a collection of categories.

To query community categories with certain criteria, the following parameters are used:

* `sortBy` allows you to filter communities based on the order that the community categories were created or based on alphabetical order, last created, and first created.
* `includeDeleted` allows you to specify if you want to include deleted community categories in your query. By passing `true` or `false` to this method, you can include or exclude deleted community categories from the results.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/142c0ec196f40b6897d130a4043afd6e#file-get-categories-swift" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/b5a26162a9eff88257b924e324762354#file-amitycommunitycategoryquery-kt" %}
{% endtab %}

{% tab title="JavaScript" %}
{% embed url="https://gist.github.com/amythee/5ca2161936204b97429eab4f6f5e44eb#file-querycategories-js" %}
{% endtab %}

{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/amythee/e0f1c8c12bb92e4aec804bdbcd789ca9#file-querycategories-ts" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/27190fcd902079993a9eef841267a2df#file-amitycategoryquery-dart" %}
{% endtab %}
{% endtabs %}
