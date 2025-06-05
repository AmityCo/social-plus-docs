# Ad Impressions

The Ad Impressions feature is a tool designed to collect valuable data regarding ad interactions for analytics and reporting purposes. This feature empowers users to gain insights into how their ad is performing. With this feature, users can mark specific ads as seen or clicked, and access the report via the console.

<Info>
Impressions represent the number of users who viewed the ad, while reach represents the number of unique users who viewed the ad. Please keep in mind that ad impression data won't be updated in real-time but rather almost in real-time.
</Info>

## Mark Seen

The `markAsSeen()` function in the Social PlusSDK serves to increase the impression and reach count of specific ads.

<Tabs>
  <Tab title="iOS">
    <CodeGroup>
      https://gist.github.com/amythee/5738e6521e3cbb75a63af63fa1cce1fc
    </CodeGroup>
  </Tab>
  <Tab title="Android">
    <CodeGroup>
      https://gist.github.com/3d1a39267a07c3756fa4babf6f53f536
    </CodeGroup>
  </Tab>
  <Tab title="TypeScript">
    <CodeGroup>
      https://gist.github.com/amythee/3a00fc3f43563f123bd8595b3ae55de6#file-getnetworkads-ts
    </CodeGroup>
  </Tab>
</Tabs>

## Mark Link Clicked

The `markLinkAsClicked()` function in the Social PlusSDK serves to increase the CTR of specific ads.

<Tabs>
  <Tab title="iOS">
    <CodeGroup>
      https://gist.github.com/amythee/c57a384a67f8e0464fdd85b606af541e
    </CodeGroup>
  </Tab>
  <Tab title="Android">
    <CodeGroup>
      https://gist.github.com/e6cb01f55d3bc3f49563135fe59a70e5
    </CodeGroup>
  </Tab>
  <Tab title="TypeScript">
    <CodeGroup>
      https://gist.github.com/amythee/8464d1a4bcbe8bd51f91f40612140538#file-getnetworkads-ts
    </CodeGroup>
  </Tab>
</Tabs>