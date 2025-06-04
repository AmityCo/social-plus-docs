---
description: >-
  Process to setup iOS push notification certificates to receive notification
  from Social PlusSDK / Social PlusUIKit.
---

# iOS Push Notification Certificate Setup

To send or receive push notifications using our SDK, you would need to create push notification certificates from the Apple Developer Console & Upload to our Social Plus console.

Here are the steps to generate a push notification certificate from the Apple Developer Console.

{% hint style="info" %}
When a new .p12 certificate is created, the previous certificate gets revoked and cannot be used again.
{% endhint %}

**Step 1:**&#x20;

Go to Apple Developer Console (i.e. [https://developer.apple.com](https://developer.apple.com/)) and click on Certificates.

<figure><img src="../../../.gitbook/assets/Push - 1.png" alt=""><figcaption></figcaption></figure>

**Step 2:**&#x20;

Select Apple Push Notification Service SSL (Sandbox & Production)

<figure><img src="../../../.gitbook/assets/Push - 2.png" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
This certificate will be applicable for both Sandbox & Production environments so you do not need to create a separate one for each one.&#x20;
{% endhint %}

**Step 3:**&#x20;

Follow the rest of the steps of creating certificates as shown by Apple & download the **.cer** file.

**Step 4:**&#x20;

Double-click on the **.cer** file you downloaded in the last step in Finder. After a few seconds, the Keychain Access program should open.

**Step 5:**&#x20;

Select **Login → My Certificates**, then right-click on the Apple Push Services certificate that you just installed. It would show you some options as shown below.

<figure><img src="../../../.gitbook/assets/Push 3.png" alt=""><figcaption></figcaption></figure>



**Step 6:**&#x20;

Select the **Export “Apple Push Services …”** option and save the file using the .p12 extension. If you add a password while exporting, you will need to enter the same password in the Social Plus Console.

**Step 7:**&#x20;

Open Social Plus Console. Select **Settings → Push Notifications** & Upload this .p12 file to Social Plus Console.

<figure><img src="../../../.gitbook/assets/Push 4.png" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
This certificate can be used to receive push notifications in your production build (Distributed through Appstore or Testflight). Currently, we do not support receiving push notifications in the Debug build.
{% endhint %}

That’s it. Now the certificate is setup, Please follow the steps shown in the [Register & Unregister Push Notifications](register-and-unregister-push-notifications-on-a-device.md) section to correctly send APNS tokens to receive push notifications.

{% hint style="info" %}
Please make sure you have **Push Notification** capabilities enabled in your Xcode Project.
{% endhint %}
