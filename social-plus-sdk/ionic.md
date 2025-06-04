---
description: >-
  Use our social SDK to enable social features such as Feeds, Groups, Profiles,
  Content Posts, and Social Media Type Interactions for all platforms.
hidden: true
---

# Ionic

## **Ionic Framework**

We now support the Ionic framework in building your application using our web SDK. You can use our Social Plus natively to support your mobile or web applications built using the Ionic framework.&#x20;

Since Ionic is an HTML5 framework, it needs a native wrapper to access native SDK functionalities and run as a native app. We recommend using Capacitor.

Capacitor will wrap your application in a native container so you can easily integrate our web SDK to run on iOS, Android, and Web platforms.

### **Getting Started**

We will walk you through the process of installing ionic and all the necessary dependencies for development.

### **Installing Ionic**

Ionic comes with a convenient command line utility to start, build, and package Ionic apps. To install it, simply run:

```javascript
sudo npm install -g @ionic/cli 
```

### **Adding a Capacitor to your app**

In the root of your application, install Capacitor:

```javascript
npm install @capacitor/core --save
```

### **Adding support for the native platform**

Now, we need to copy the native platform template into your application:

```javascript
ionic capacitor add <platform>
```

| **Platform**                                          |
| ----------------------------------------------------- |
| The platform template to add (e.g. `android`, `ios`). |

### **Opening the Application**

To open the application in your IDE, run:

```javascript
npx cap open <platform>
```

| **Platform**                                                     |
| ---------------------------------------------------------------- |
| Description: The platform you are using (e.g. `android`, `ios`). |

{% hint style="info" %}
For Android, it will open Android Studio. For iOS, it will open Xcode.
{% endhint %}

## **Where to go next**

Now you’re ready to start integrating our social SDK into your application.&#x20;
