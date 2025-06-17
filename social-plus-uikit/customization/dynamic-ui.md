# Dynamic UI

<figure><img src="../../../.gitbook/assets/Screenshot 2568-05-07 at 15.53.56.png" alt=""><figcaption></figcaption></figure>

Dynamic UI allows authorised team members to adjust runtime UIKit customisations—such as colours, and eventually additional styling options—after the app has been released. All changes are made in the Dynamic UI section of the web console, where an on‑screen device mock‑up provides a true what‑you‑see‑is‑what‑you‑get preview.&#x20;

Edits remain in **preview** until you click **Publish**; publishing immediately replaces the previously stored values on our servers. No new build is required—design and product teams can refresh branding on their own, engineering spends less time on integration, and the entire release cycle accelerates so your app ships updates faster.

Dynamic UI currently supports updates to global colour tokens; future versions will extend coverage to additional UIKit properties.

## UIKit integration

To deliver the latest configuration to end‑users, include a call to `syncNetworkConfig()` in your application flow. The method makes a lightweight request to the Dynamic UI endpoint, downloads the current customization payload, caches it on the device, and applies the new values across all active UIKit screens.

\
**Offline and fallback behaviour** – If the device is offline, UIKit applies the last cached configuration; if no cache exists, it reverts to the build‑time defaults.

**Prerequisite** – Require setup and authentication in order to invoke this function.

{% tabs %}
{% tab title="iOS (4.5.0+)" %}
{% embed url="https://gist.github.com/amythee/b9b62137fd7a7d661fd7db96e1511c80" %}
{% endtab %}

{% tab title="Android (4.5.1+)" %}
{% embed url="https://gist.github.com/amythee/dafb85d012ddca5ce0c421c2580b3501" %}
{% endtab %}

{% tab title="Web (4.6.1+)" %}
{% embed url="https://gist.github.com/amythee/26bfd967412b07713e49f9e373a72f5a" %}
{% endtab %}
{% endtabs %}

