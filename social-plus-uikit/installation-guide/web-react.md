---
description: >-
  Quick Start Guide for Integrating Social Plus UIKit's Social Feature into
  React Applications.
---

# Web React

Welcome to the Quick Start Guide for integrating Social Plus features into your existing React application. This guide provides step-by-step instructions to incorporate social features into your app, enhancing user engagement through shared experiences.

## Prerequisites

Before getting started, ensure that you have the following prerequisites installed on your system:

* [Node.js](https://nodejs.org/) LTS version (currently version 20)
* [pnpm](https://pnpm.io/) version 8

## <mark style="color:purple;">Step 1: Install UIKit and peer dependencies</mark>

### PNPM Installation

#### Install PNPM (Optional)

```
corepack enable pnpm
```

Ref: https://pnpm.io/installation#using-corepack

**Install  UIKit via PNPM**

```
pnpm i @amityco/ui-kit
```

## <mark style="color:purple;">Step 2: Setting Up UIKit</mark>

To integrate Social+ UI-Kit into your application, follow these steps:

1.  Import the main UI-Kit styles (Required)\
    Add the following import statement in your main application file:

    ```typescriptreact
    import "@amityco/ui-kit-open-source/dist/index.css";
    ```
2. Customize UI-Kit (Optional)\
   If you want to customize component styles, create a configuration file named `amity-uikit.config.json` and define your theme colors.
3. Wrap your application with `<AmityUiKitProvider>`\
   In your main application component, wrap your content with `AmityUiKitProvider` and pass the required configurations.

```
import React from 'react';
import { AmityUiKitProvider, AmityUiKitSocial } from '@amityco/ui-kit-open-source';
import "@amityco/ui-kit-open-source/dist/index.css";
import amityConfig from './amity-uikit.config.json';

export default App = () => {
  return (
      <AmityUiKitProvider
        apiKey={apiKey}
        userId={userId}
        displayName={displayName}
        apiEndpoint={apiEndpoint}  
        apiRegion={apiRegion} // can be "us", "eu", or "sg"
        configs={amityConfig as Config}
      >
       <div
        style={{
          position: "absolute",
          left: 0,
          top: 0,
          width: "100vw",
          height: "100dvh",
        }}
        >
            <AmityUiKitSocial />
        </div>
      </AmityUiKitProvider>
      )}
  );
};
```

note : **apiEndpoint** not required if using default endpoints

## <mark style="color:purple;">Step 3: Customizing the UI</mark>

Social Plus UIKit supports extensive customization options via a config.json file. You can modify themes, colors, and icons for various components and elements of the social feature according to your application's design requirements.

* Example customization snippet:

```
"global_theme": {
  "light_theme": {
    "primary_color": "#FFFFFF",
    "secondary_color": "#AB1234"
  }
}
```

* You can exclude certain UI elements or customize specific components and elements as per your needs.

You have now successfully integrated the Social Plus feature into your Web application. For further customization options, refer to the detailed documentation provided with the SDK. If you encounter any issues or require assistance, our community forum at community.amity.co is always here to help.

## <mark style="color:purple;">Opensource Installation (Alternative)</mark>

With open source, developers have more flexibility and greater customization options, allowing you to have complete control over the visual style. Open sourcing allows for more transparency and visibility, and enables contributions from a greater developer community in terms of good design, implementation, code improvement, and fixes, translating into a better product and development experience.&#x20;

### Install UIKit and peer dependencies

#### Install PNPM (Optional)

```
corepack enable pnpm
```

Ref: https://pnpm.io/installation#using-corepack

#### Running Storybook (Optional)

To run Storybook and view the UI components in isolation, follow these steps:

1.  Clone the Amity UI-Kit repository:

    ```
    git clone https://github.com/AmityCo/Amity-Social-Cloud-UIKit-Web-OpenSource.git
    ```
2.  Navigate to the cloned repository's directory:

    ```
    cd Amity-Social-Cloud-UIKit-Web-OpenSource
    ```
3.  Install the dependencies using pnpm:

    ```
    pnpm install
    ```
4.  Create a `.env` file at the root of the project with the following content:

    ```
    STORYBOOK_API_REGION=<API_REGION>
    STORYBOOK_API_KEY=<API_KEY>
    ```

    Replace `<API_REGION>` and `<API_KEY>` with your actual credentials.
5.  Run Storybook:

    ```
    pnpm run storybook
    ```
6. Open your browser and navigate to `http://localhost:6006` to view the Storybook interface.

#### Installation

To install the Amity UI-Kit together with another project, follow these steps:

1.  Clone the repository using the following command:

    ```
    git clone https://github.com/AmityCo/Amity-Social-Cloud-UIKit-Web-OpenSource.git
    ```
2.  Navigate to the cloned repository's directory:

    ```
    cd ./Amity-Social-Cloud-UIKit-Web-OpenSource
    ```
3.  Install the dependencies using pnpm:

    ```
    pnpm install
    ```
4.  Build the project:

    ```
    pnpm run build
    ```
5.  Navigate to your application's directory:

    ```
    cd <path-to-your-app>
    ```
6. Link the Amity UI-Kit repository to your application using one of the following package managers:
   *   NPM:

       ```
       npm link file:<path-to-amity-ui-kit-repository> --save
       ```
   *   Yarn (Classic):

       ```
       yarn add file:<path-to-amity-ui-kit-repository>
       ```
   *   PNPM:

       ```
       pnpm i file:<path-to-amity-ui-kit-repository>
       ```

