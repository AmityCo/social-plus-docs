# Delete Community

The SDK provides a way for creators or moderators to delete a community by calling the `deleteCommunity` method. In the JavaScript SDK, this method is referred to as the `closeCommunity` method.

To delete a community using this method, users can call the method and provide the `communityId` as a parameter. This will trigger the deletion process, which will remove the community and associated community data.

It is important to note that deleting a community is a permanent action and cannot be undone. As such, it is recommended that users exercise caution when deciding to delete a community and ensure that they have taken all necessary precautions to preserve any important content or data associated with the community.

<Tabs>
  <Tab title="iOS">
    <Embed url="https://gist.github.com/amythee/36d5b032730280afd3825baceeb81424#file-delete-a-community-swift" />
  </Tab>
  <Tab title="Android">
    <Embed url="https://gist.github.com/amythee/f9daa8dbf555dd5504cbc405919a1760#file-amitycommunitydeletion-kt" />
  </Tab>
  <Tab title="JavaScript">
    ```javascript
    const success = await CommunityRepository.closeCommunity('abc');
    ```
  </Tab>
  <Tab title="TypeScript">
    <Embed url="https://gist.github.com/amythee/5895234d21c6120dea2a3ed551b4b896#file-deletecommunity-ts" />
  </Tab>
  <Tab title="Flutter">
    <Embed url="https://gist.github.com/amythee/74fd1344f6fef795471da6b099f0405c#file-amitycommunitydelete-dart" />
  </Tab>
</Tabs>