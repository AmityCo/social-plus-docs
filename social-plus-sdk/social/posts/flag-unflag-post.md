# Flag / Unflag Post

### Flag Post

The SDK provides a way for users to report or flag a post as inappropriate using the `flag` method.

This method allows users to notify the community moderators or admins about posts that they believe violate the community guidelines or are otherwise inappropriate. By flagging a post with reason that we provided, users can help ensure that the community remains a safe and welcoming place for all members.

| AmityContentFlagReason       | Description                            |
| ---------------------------- | -------------------------------------- |
| CommunityGuidelines          | Against community guidelines           |
| HarassmentOrBullying         | Harassment or bullying                 |
| SelfHarmOrSuicide            | Self-harm or suicide                   |
| ViolenceOrThreateningContent | Violence or threatening content        |
| SellingRestrictedItems       | Selling and promoting restricted items |
| SexualContentOrNudity        | Sexual message or nudity               |
| SpamOrScams                  | Spam or scams                          |
| FalseInformation            | False information or misinformation    |
| Others                       | Optional explanation (Max. 300 chars)  |

<Note>
Flag reason is only available in iOS, Android, and TypeScript
</Note>

<Tabs>
  <Tab title="iOS">
    <CodeBlock>
      {`https://gist.github.com/amythee/b4bcc958f7c4b6a5833a72df9c2ac164`}
    </CodeBlock>
  </Tab>
  <Tab title="Android">
    <CodeBlock>
      {`https://gist.github.com/amythee/697cdbb29e7a8747284624c4e048b1ea`}
    </CodeBlock>
  </Tab>
  <Tab title="JavaScript">
    <CodeBlock>
      {`https://gist.github.com/amythee/200a8701bd118ecd5c8a411eea2a8ab9#file-flagpost-js`}
    </CodeBlock>
  </Tab>
  <Tab title="TypeScript">
    <CodeBlock>
      {`https://gist.github.com/c288f36f9e555d2856c4bdc7811bef32`}
    </CodeBlock>
  </Tab>
  <Tab title="Flutter">
    <CodeBlock>
      {`https://gist.github.com/amythee/a64f66b4df447fd87c4cbff25fea843e#file-amitypostflag-dart`}
    </CodeBlock>
  </Tab>
</Tabs>

### Check for isFlaggedByMe

This method allows users to quickly determine whether they have previously flagged a post as inappropriate or not. To use this method, users can call the `isFlaggedByMe` method with the `postId` as a parameter. The method will then return a boolean value indicating whether or not the post has been flagged by the current user.

<Tabs>
  <Tab title="iOS">
    <CodeBlock>
      {`https://gist.github.com/amythee/437fb49d723dc218de8ef9c40399e7fd`}
    </CodeBlock>
  </Tab>
  <Tab title="Android">
    <CodeBlock>
      {`https://gist.github.com/amythee/d4e1d94fe26993c6f5b6f242b98b6b14#file-amitypostflagstatus-kt`}
    </CodeBlock>
  </Tab>
  <Tab title="JavaScript">
    <CodeBlock>
      {`https://gist.github.com/amythee/d66526e025a3df33d2f50d66938b0427#file-checkflagged-js`}
    </CodeBlock>
  </Tab>
  <Tab title="TypeScript">
    <CodeBlock>
      {`https://gist.github.com/e2da84a72aa292268e1ddd5e52303330`}
    </CodeBlock>
  </Tab>
  <Tab title="Flutter">
    <CodeBlock>
      {`https://gist.github.com/amythee/524aceb00b5ff5bd6373628274f30c1d#file-amitypostflagstatus-dart`}
    </CodeBlock>
  </Tab>
</Tabs>

### Unflag Post

This method allows users to retract their earlier report if they believe that the flagged post no longer violates the community guidelines or if they mistakenly reported the post. By unflagging a post, users can help ensure that the community moderators or admins can focus their attention on other reported posts that may still require attention.

<Tabs>
  <Tab title="iOS">
    <CodeBlock>
      {`https://gist.github.com/amythee/feaa79e8b1de93423088da6967833e07`}
    </CodeBlock>
  </Tab>
  <Tab title="Android">
    <CodeBlock>
      {`https://gist.github.com/amythee/d51647f7997062c927764ecebffdb921#file-amitypostunflag-kt`}
    </CodeBlock>
  </Tab>
  <Tab title="JavaScript">
    <CodeBlock>
      {`https://gist.github.com/amythee/6541682774eb76badaf7f00d57caf68b#file-unflagpost-js`}
    </CodeBlock>
  </Tab>
  <Tab title="TypeScript">
    <CodeBlock>
      {`https://gist.github.com/amythee/1056b48c740057806a5be6bed405f00a`}
    </CodeBlock>
  </Tab>
  <Tab title="Flutter">
    <CodeBlock>
      {`https://gist.github.com/amythee/a2ca8917013886062803dc770224bf66#file-amitypostunflag-dart`}
    </CodeBlock>
  </Tab>
</Tabs>