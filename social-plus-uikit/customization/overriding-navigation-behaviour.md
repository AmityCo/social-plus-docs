# Overriding Navigation Behaviour

Navigation logic in UIKit can be readily customized by subclassing the predefined `Behaviour` classes and overriding relevant events. UIKit effectively decouples navigation logic and events by distributing them into separate `Behaviour` classes for each page.

\
UIKit includes the `UIKitBehaviour` class, which encompasses all the behavior classes utilized by it. These classes are standard classes that expose navigation events and other events that can be overridden as permitted by UIKit.

### Overriding Behaviour Class

This example illustrates how to override the `Behaviour` class and configure a custom `Behaviour` class within the UIKit framework.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/e9f64f7bb274e461ebbf207a2af95449" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/85d5a80eb7feaf332bf1b0351c264f89" %}
{% endtab %}
{% endtabs %}



### Advanced iOS Navigation:

Our **UIKit v4** framework leverages **SwiftUI** extensively to build pages, components, and elements. These SwiftUI pages are embedded within Apple’s `UINavigationController`, allowing seamless navigation between screens.

To integrate SwiftUI with UIKit, we provide two hosting controller classes:

* `AmitySwiftUIHostingController`
* `AmitySwiftUIHostingNavigationController`

These classes allow you to wrap SwiftUI views and present them from UIKit-based view controllers.

**Navigation Bar Customization**

This architecture also offers the flexibility to customize the **Navigation Bar** beyond what SwiftUI currently supports. To enable these customizations while retaining the native **interactive swipe-to-pop** gesture, we override gesture handling behavior at a global level on `UINavigationController`.

Specifically, we override the following methods:

* `gestureRecognizerShouldBegin(_:_)`
* `gestureRecognizer(_:shouldRecognizeSimultaneouslyWith:)`

This ensures that the swipe-to-go-back gesture remains functional even with customizations.

**Custom Gesture Behavior**

We also provide a class called `AmitySwipeToBackGestureBehavior`, which gives you control over the swipe-to-pop gesture behavior. You can subclass this and override its functionality as needed.

To apply your custom gesture behavior, assign an instance of your subclass to the `swipeToBackGestureBehavior` property when initializing your screen or controller within UIKit v4.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/dd3a184eebcca26c9a23841bd8f6dadd" %}
{% endtab %}
{% endtabs %}





















