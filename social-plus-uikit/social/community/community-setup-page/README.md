---
layout:
  title:
    visible: true
  description:
    visible: false
  tableOfContents:
    visible: true
  outline:
    visible: true
  pagination:
    visible: true
---

# Community Setup Page

The Community Setup Page can be used to create a brand new community or updating the existing community.

<div><figure><img src="../../../../../.gitbook/assets/s1 (1).png" alt=""><figcaption></figcaption></figure> <figure><img src="../../../../../.gitbook/assets/s2 (1).png" alt=""><figcaption></figcaption></figure> <figure><img src="../../../../../.gitbook/assets/s3 (1).png" alt=""><figcaption></figcaption></figure></div>

### Features <a href="#features" id="features"></a>

<table data-header-hidden><thead><tr><th width="217"></th><th></th></tr></thead><tbody><tr><td>Feature</td><td>Description</td></tr><tr><td>Creating a community</td><td>Fill in the information needed to create the community like avatar, name, description and categories. Being a public or private community can be selected as well.</td></tr><tr><td>Updating the existing community</td><td>The community avatar, name, description, and categories can be updated. You can change the community from public to private and vice versa using this page.</td></tr></tbody></table>

### Customization

<table><thead><tr><th width="264">Config ID</th><th width="122">Type</th><th>Description</th></tr></thead><tbody><tr><td><code>community_setup_page/*/*</code></td><td>Page</td><td>You can customize page <code>theme</code></td></tr><tr><td><code>community_setup_page/*/close_button</code></td><td>Element</td><td>You can customize <code>image</code></td></tr><tr><td><code>community_setup_page/*/title</code></td><td>Element</td><td>You can customize <code>text</code></td></tr><tr><td><code>community_setup_page/*/community_edit_title</code></td><td>Element</td><td>You can customize <code>text</code></td></tr><tr><td><code>community_setup_page/*/community_name_title</code></td><td>Element</td><td>You can customize <code>text</code></td></tr><tr><td><code>community_setup_page/*/community_about_title</code></td><td>Element</td><td>You can customize <code>text</code></td></tr><tr><td><code>community_setup_page/*/community_category_title</code></td><td>Element</td><td>You can customize <code>text</code></td></tr><tr><td><code>community_setup_page/*/community_privacy_title</code></td><td>Element</td><td>You can customize <code>text</code></td></tr><tr><td><code>community_setup_page/*/community_privacy_private_icon</code></td><td>Element</td><td>You can customize <code>image</code></td></tr><tr><td><code>community_setup_page/*/community_privacy_private_title</code></td><td>Element</td><td>You can customize <code>text</code></td></tr><tr><td><code>community_setup_page/*/community_privacy_private_description</code></td><td>Element</td><td>You can customize <code>text</code></td></tr><tr><td><code>community_setup_page/*/community_privacy_public_icon</code></td><td>Element</td><td>You can customize <code>image</code></td></tr><tr><td><code>community_setup_page/*/community_privacy_public_title</code></td><td>Element</td><td>You can customize <code>text</code></td></tr><tr><td><code>community_setup_page/*/community_privacy_public_description</code></td><td>Element</td><td>You can customize <code>text</code></td></tr><tr><td><code>community_setup_page/*/community_add_member_title</code></td><td>Element</td><td>You can customize <code>text</code></td></tr><tr><td><code>community_setup_page/*/community_add_member_button</code></td><td>Element</td><td>You can customize <code>text</code> and <code>image</code></td></tr><tr><td><code>community_setup_page/*/community_create_button</code></td><td>Element</td><td>You can customize <code>text</code> and <code>image</code></td></tr><tr><td><code>community_setup_page/*/community_edit_button</code></td><td>Element</td><td>You can customize <code>text</code> and <code>image</code></td></tr><tr><td><code>community_setup_page/*/image_button</code></td><td>Element</td><td>You can customize <code>text</code> and <code>image</code></td></tr><tr><td><code>community_setup_page/*/camera_button</code></td><td>Element</td><td>You can customize <code>text</code> and <code>image</code></td></tr><tr><td></td><td></td><td></td></tr></tbody></table>

For more details on customization, please refer to the [Customization](../../../customization/) page.

### Usage <a href="#usage" id="usage"></a>

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/2e539f33a247d27bd917979b6c94217b" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/b1cd8006517217ea8919188c8267e28b" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/44e6f9bfe89aadc5ac4b4cf7c53ce7a2" %}


{% endtab %}

{% tab title="Web" %}
{% embed url="https://gist.github.com/amythee/399d4f6ab866f6b4d6c10bf620134338" %}
{% endtab %}
{% endtabs %}

### Navigation Behavior

The Community Setup Page will navigate to the user listing page to add users to the community if it is created as private, and to the category listing page to attach categories to the community. You can override the behavior to navigate to your own pages.&#x20;

For more details, please refer to the [Overriding Navigation Behavior](https://docs.amity.co/amity-uikit/uikit-v4-beta/customization/overriding-navigation-behaviour) page.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/21627bb63e0e2a652479db34054d6da6" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/eb5873284d6eef4cd7081b194ec0c9bf" %}
{% endtab %}

{% tab title="Web" %}
{% embed url="https://gist.github.com/amythee/399d4f6ab866f6b4d6c10bf620134338" %}
{% endtab %}
{% endtabs %}
