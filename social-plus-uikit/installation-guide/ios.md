---
description: Social Plus iOS UIKit Migration Guide
---

# iOS

## <mark style="color:purple;">SwiftPM Installation</mark>

This section is about installing managed uikit through dependency manager (SwiftPM). If you have already installed our Open Source UIKit, you can skip this section.&#x20;

### **Create a project**

Go to **Xcode** and create a project for iOS.

1. Enter a project name
2. Select **Swift** as your language option

<figure><img src="../../../.gitbook/assets/Screenshot 2566-02-17 at 15.33.56 (1).png" alt=""><figcaption></figcaption></figure>

### Installation <a href="#carthage-installation" id="carthage-installation"></a>

To integrate Social Plus UIKit into your project via SwiftPM, please follow the instruction below.

* [Add a Package Dependency](https://developer.apple.com/documentation/swift_packages/adding_package_dependencies_to_your_app)

Enter the repository URL to search the package, and choose to install `AmityUIKit`.

```
https://github.com/AmityCo/Amity-Social-Cloud-UIKit-iOS-SwiftPM
```

{% hint style="info" %}
Please specify the required version of the UIKit v4 beta using "`Exact Version"`**`Dependency Rule`**` ``as shown in the image below.`&#x20;

`` For Example: `Exact Version` `4.6.0` ``
{% endhint %}

<figure><img src="../../../.gitbook/assets/Screenshot 2567-08-21 at 09.27.19.png" alt=""><figcaption></figcaption></figure>

### Usage

After finished installing SDK. You will be able to import `AmityUIKit`.

```swift
import AmityUIKit
```

***

## <mark style="color:purple;">Open-source Installation</mark>

With open-source, developers have more flexibility and greater customization options, allowing you to have complete control over the visual style. Open sourcing allows for more transparency and visibility and enables contributions from a greater developer community in terms of good design, implementation, code improvement, and fixes, translating into a better product and typical development.&#x20;

### Migrate iOS Open Source UI Kit with Existing Project  <a href="#c8m9qzg417gv" id="c8m9qzg417gv"></a>

#### Remove existing dependencies <a href="#c8m9qzg417gv" id="c8m9qzg417gv"></a>

If you've never used UI Kit, you may skip this step and proceed to the next step.&#x20;

If you're integrating the UI Kit with an existing project, you'll need to remove and unlink the managed UIKit from your project before proceeding with the integration.&#x20;

#### Migrate to iOS UIKit Open Source <a href="#bln34rs78cz" id="bln34rs78cz"></a>

There are several ways for you to migrate the open-source iOS UI Kit into your projects, depending on your workflow. One way that we recommend is via Git Submodule. This instruction assumes that the app project is already set up with a Git repository.

1. Add the git submodule of Social Plus UIKit open source into your git repository.

```
git submodule add https://github.com/AmityCo/ASC-UIKit-iOS-OpenSource
```

{% hint style="info" %}
To simplify forking & contributing to the open-source UIKit, we are moving away from using git-lfs in our git repository. We are migrating all development of Open Source UIKit to a new repository [https://github.com/AmityCo/ASC-UIKit-iOS-OpenSource](https://github.com/AmityCo/ASC-UIKit-iOS-OpenSource) starting release v3.12.0. The previous open source UIKit Repository [https://github.com/AmityCo/Amity-Social-Cloud-UIKit-iOS-OpenSource](https://github.com/AmityCo/Amity-Social-Cloud-UIKit-iOS-OpenSource) is now deprecated. The new repository will not contain any history before the release of v3.12.0.
{% endhint %}

**For new users:**

If you are just starting to use Open Source UIKit or already using the latest version of Open Source UIKit (i.e. v3.12.0) from the old Repository, We suggest you start pulling changes from the new repository instead.

In this case,

* If you have forked the old open-source UIKit repository, we suggest you fork the new repository and use that instead.

**For Old Users:**

If you are using an older version (< 3.12.0) of open-source UIKit, we suggest you upgrade to the latest version of UIKit as soon as possible. Once you are caught up to version 3.12.0, please migrate to use the new repository instead.

2. Create an Xcode Workspace, and then add both `MyApp.xcodeproj` and `AmityUIKit.xcodeproj` together under the same workspace.

![Project Directory](https://lh5.googleusercontent.com/_Hd-WOzWYP8uFbd4Vfyp4U_t5tMl2lDPxavcGku_opPLyZX0ilPUqH0L5YMfe5yoEijz0XK69ebB7jQk5fqvFf_PqVnoAHBX5ExZLRMs4YiuwLoyTrxhKQZ8nfgbvNXb5z4HQ4_HySW1sxgrpg)

<figure><img src="../../../.gitbook/assets/Screenshot 2566-02-17 at 15.15.37 (1).png" alt=""><figcaption><p>Xcode Workspace Project Structure</p></figcaption></figure>

3.`AmityUIKit` links with other dependencies such as `AmitySDK`, `Realm` etc through `SharedFrameworks` which is a Swift Package.&#x20;

&#x20;       Step 1: Reset the Package Cache of your Application Target i.e YourApp.xcodeproj. \[If you are installing AmityUIKit for the first time, you can skip this step]

&#x20;       Select App Target In Xcode Project -> Select File Menu for Xcode-> Packages -> Reset Package Cache

&#x20;       Step 2: Link `SharedFrameworks` & `AmityUIKit.framework` to YourApp.xcodeproj target as shown below.

<figure><img src="../../../.gitbook/assets/Screenshot 2566-05-19 at 10.48.40.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../../.gitbook/assets/Screenshot 2566-05-19 at 10.39.10.png" alt=""><figcaption></figcaption></figure>

4\. On `MyApp.xcodeproj`, let’s try importing Social Plus UIKit / Social Plus SDK and call some APIs. You should be able to compile and run the app.

<figure><img src="../../../.gitbook/assets/Screenshot 2566-02-17 at 15.27.37 (1).png" alt=""><figcaption></figcaption></figure>

### Modify iOS Open Source UI Kit&#x20;

You can modify the iOS open-source UI Kit to customize behaviors to fit your needs. To modify the code, simply copy and paste it into your local machine.

We recommend that you first fork the repository before starting any customization work so that it will be easier to merge the code with the next version update that we provide from the main repository.

References on forking: [https://docs.github.com/en/get-started/quickstart/fork-a-repo](https://docs.github.com/en/get-started/quickstart/fork-a-repo)

### Get Latest iOS Open Source UI Kit Updates

To update to the latest version of the UI Kit, you can pull the latest commit of the git submodule.

```
cd https://github.com/AmityCo/ASC-UIKit-iOS-OpenSource
git pull origin master
git checkout tags/4.0.0-beta01
cd ..
git add .
git commit -m “Update ios uikit opensource submodule”
git push origin master
```
