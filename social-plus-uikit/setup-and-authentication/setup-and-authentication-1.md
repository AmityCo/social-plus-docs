# Android

## Compatibility&#x20;

We are always working to enhance our existing UIKit. As a result, the minimum compatibility may vary for our previous version releases. Below is the compatibility list for our latest release. For a complete compatibility history of any given UIKit version, you may refer to our [changelogs](../../changelogs/changelog-1.md).

* Glide - 4.12.0&#x20;
* OKHTTP3 - 4.9.02
* Retrofit2 - 2.9.1&#x20;
* Android Paging Data Library - 3.1.1&#x20;
* Room - 2.5.1
* RxJava3 - 3.1.5
* Gson - 2.8.10&#x20;
* Kotlin-std-lib - 1.7.20&#x20;
* Kotlin-coroutines - 1.5.0&#x20;
* Media 3 - 1.1.0
* HiveMQ mqtt client - 1.3.1
* Compose-bom - 2022.12.0
* Camera2 - 1.2.2

## Initialize the SDK

Before using the SDK, you need to initialize the SDK with your API key. Please find your account API key in the [Social Plus Console.](https://portal.amity.co/login)&#x20;

After logging in Console:

1. Click **Settings** to expand the menu.
2. Select **Security**.
3. On the **Security** page, you can find the API key in the **Keys** section.

![API key in Security page](../../../.gitbook/assets/apikey.png)

{% embed url="https://gist.github.com/amythee/63fb4a2fcb01ec2a4139d9041a9663f6" %}

#### Specify Endpoints Manually (Optional)

You can specify endpoints manually via optional parameters. API endpoints for each data center are different so you need to adjust the endpoint accordingly.&#x20;

We currently support multi-data center capabilities for the following regions:

|     Region    |         Endpoint         |   Endpoint URL  |
| :-----------: | :----------------------: | :-------------: |
|     Europe    | AmityRegionalEndpoint.EU | api.eu.amity.co |
|   Singapore   | AmityRegionalEndpoint.SG | api.sg.amity.co |
| United States | AmityRegionalEndpoint.US | api.us.amity.co |

## Authentication

You must first register the current device with a `userId`. A device registered with a `userId` will be permanently tied to that `userId` until you deliberately unregister the device, or until the device has been inactive for more than 90 days. A device registered with a specific `userId` will receive all messages belonging to that user.

{% embed url="https://gist.github.com/amythee/f42082cd7a09b63990fedb15a69bb1bf" %}
