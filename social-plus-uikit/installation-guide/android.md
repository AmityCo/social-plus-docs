---
description: Social Plus Android UIKit Installation Guide.
---

# Android

## <mark style="color:purple;">Gradle Installation</mark>

### Prerequisite

SDK supports Android 5.0 (API Level 21) and above

```gradle
android {
    ...
    defaultConfig {
        minSDKVersion 21 // at least 21
    }
}
```

### Installation

Add the Jitpack repository in your project level `build.grade` at the end of repositories:

```gradle
allprojects {
  repositories {
    ...
    maven { url 'https://jitpack.io' }
  }
}
```

Add the dependency in your module level `build.grade.` Find latest UIKit version at [Changelog](../../changelogs/changelog-1.md).

```gradle
// add buildFeatures, compileOptions and kotlinOptions in android tag
android {

    buildFeatures {
        dataBinding = true
    }
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }
    kotlinOptions {
        jvmTarget = JavaVersion.VERSION_1_8
    }
    
}
    
dependency {
implementation 'com.github.AmityCo.Amity-Social-Cloud-UIKit-Android:amity-uikit:x.y.z'
}
```

### Managing Conflicting File Generation

In your app module's `build.gradle` , add the following packaging options.

```kotlin
android {
    ...
    packagingOptions {
        exclude 'META-INF/INDEX.LIST'
        exclude 'META-INF/io.netty.versions.properties'
    }
}
```

***

## <mark style="color:purple;">Open-source Installation</mark>

With open source, developers have more flexibility and greater customization options, allowing you to have complete control over the visual style. Open sourcing allows for more transparency and visibility, and enables contributions from a greater developer community in terms of good design, implementation, code improvement, and fixes, translating into a better product and development experience.&#x20;

### Migrate Android Open Source UI Kit with Existing Project

#### Remove existing gradle dependency

If you've never used UI Kit from a gradle dependency before, you may skip this step and proceed to the next step. If you are migrating the UIKit with an existing gradle dependency, you will need to remove it from the gradle at the application level.

```
implementation 'com.github.AmityCo.Amity-Social-Cloud-UIKit-Android:amity-uikit:x.y.z'
```

#### Import UI Kit module to your existing project

* Clone or download source code from an open-source Github repository. [https://github.com/AmityCo/Amity-Social-Cloud-UIKit-Android-OpenSource](https://github.com/AmityCo/Amity-Social-Cloud-UIKit-Android-OpenSource)

![](<../../../.gitbook/assets/image (67).png>)

* Navigate to your current application in Android Studio, then at the top navigation bar go to **File > New > Import Module...**

![](<../../../.gitbook/assets/image (11) (1).png>)

* Choose the source directory where you downloaded/cloned UI Kit source code.

![](<../../../.gitbook/assets/image (22).png>)

* Make sure that you import  `:chat` , `:common`, `:social`, and `:amity-uikit` module  as per the screenshot described.  The `:sample` module is optional and solely contains examples of UIKit Fragments and Activities.

![](<../../../.gitbook/assets/image (86).png>)

* Navigate to the root project's `settings.gradle` file once the modules have been successfully imported. You may see that Android Studio generated a dependency path from the UI Kit source code directory you specified initially. However, there's a chance that Android Studio won't do so or may generate the incorrect path. Please double-check that the path is accurate.

![](<../../../.gitbook/assets/image (41).png>)

* Additionally, in the root project's `settings.gradle` it's also mandatory to declare jitpack.io repository destination by adding `maven { url https://jitpack.io }` to **dependencyResolutionManagement > repositories**.

![](<../../../.gitbook/assets/image (39).png>)

* Add the imported module to application's gradle file by adding:

```
implementation project(path: ':amity-uikit')
```

![](<../../../.gitbook/assets/image (50).png>)

* Exclude these META-INF from the packaging options in application's gradle

```
 packagingOptions {
        exclude 'META-INF/INDEX.LIST'
        exclude 'META-INF/io.netty.versions.properties'
    }
```

* Lastly, apply this in the `project-level` build.gradle file.  `apply from: "../Amity-Social-Cloud-UIKit-Android/buildsystem/dependencies.gradle"`

![](<../../../.gitbook/assets/image (97).png>)

{% hint style="info" %}
Also make sure that your settings `android.nonTransitiveRClass=false` in `gradle.properties` file
{% endhint %}

Woohoo! All set now you're ready to explore and modify our UI Kit in your application project.

<figure><img src="../../../.gitbook/assets/Screenshot 2566-02-22 at 07.07.54.png" alt=""><figcaption></figcaption></figure>

### Modifying Android Open Source UI Kit &#x20;

You can modify the Android open source UI Kit to customize behaviors to fit your needs. To modify the code, simply copy and paste it into your local machine.

We recommend that you first fork the repository before starting any customization work, so that it will be easier to merge the code with the next version update that we provide from the main repository.&#x20;

Reference on forking: [https://docs.github.com/en/get-started/quickstart/fork-a-repo](https://docs.github.com/en/get-started/quickstart/fork-a-repo)

### Get Latest Open Source UI Kit Updates&#x20;

To update to the latest version of the UI Kit, you can pull the latest commit of the git submodule.

```
cd Amity-Social-Cloud-UIKit-Android-OpenSource
git pull origin master
git checkout tags/4.0.0-beta01
cd ..
git add .
git commit -m “Update android uikit opensource submodule”
git push origin branch_name
```
