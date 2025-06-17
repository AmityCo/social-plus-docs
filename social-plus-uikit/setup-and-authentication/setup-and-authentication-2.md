# Flutter (Beta)

## Initialize the SDK

Before using the SDK, you need to initialize the SDK with your API key. Please find your account API key in the [Social Plus Console.](https://portal.amity.co/login)&#x20;

After logging in Console:

1. Click **Settings** to expand the menu.
2. Select **Security**.
3. On the **Security** page, you can find the API key in the **Keys** section.

![API key in Security page](../../../.gitbook/assets/apikey.png)

{% embed url="https://gist.github.com/amythee/7fe9f404dcdc6d16fe9cf9caafd11f6c#file-amityinitializer-dart" %}

#### Specify Endpoints Manually (Optional)

You can specify endpoints manually via optional parameters. API endpoints for each data center are different so you need to adjust the endpoint accordingly.&#x20;

We currently support multi-data center capabilities for the following regions:

|     Region    |           Endpoint           |   Endpoint URL  |
| :-----------: | :--------------------------: | :-------------: |
|     Europe    | AmityRegionalHttpEndpoint.EU | api.eu.amity.co |
|   Singapore   | AmityRegionalHttpEndpoint.SG | api.sg.amity.co |
| United States | AmityRegionalHttpEndpoint.US | api.us.amity.co |

## Authentication

You must first register the current device with a `userId`. A device registered with a `userId` will be permanently tied to that `userId` until you deliberately unregister the device, or until the device has been inactive for more than 90 days. A device registered with a specific `userId` will receive all messages belonging to that user.

{% embed url="https://gist.github.com/amythee/4a3d37b5e164655802bdd2c646f9d44a#file-amityauthentication-dart" %}

