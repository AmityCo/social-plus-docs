# Query Members

## Query Channel Members

The ability to search for and query members within a chat channel is an essential feature for creating a seamless and engaging user experience. With Social Plus Chat SDK, developers can use the query member feature to allow users to search for and retrieve member information within a channel. We will discuss how to use the query member feature of Social Plus Chat SDK to enable users to search and retrieve member information within a chat channel.

Here's an explanation of the function parameter:

`filter`: A parameter accepting a filter enum, enabling filtering members with matching membership status.

* `ALL` -> Members with any membership status
* `MEMBER` -> Only active members
* `MUTED` -> Only muted members
* `BANNED` -> Only banned members

`roles`: A parameter accepting an array of roles, enabling filtering members with matching roles

`includeDeleted`: A parameter accepting a boolean value.

* `true` -> include a member whose user has been deleted
* `false` -> exclude member whose user has been deleted

<Info>
Channel member count value is based on all members in the channel including the members whose user has been deleted.
</Info>

`sortBy`: A parameter accepting a sorting option enum

* `FIRST_CREATED` -> Sort by membership creation date ascending
* `LAST_CREATED` -> Sort by membership creation date ascending

Note: The membership creation date is the time the user joins the channel.

<Tabs>
  <Tab title="iOS">
    All participation-related methods in a channel fall under a separate `ChannelParticipation` class.

    <Frame>
      <img src="https://gist.github.com/amythee/9aff3540638a09382bddfea69cff07f7#file-channel_participation_init-swift" />
    </Frame>

    <Frame>
      <img src="https://gist.github.com/amythee/82a1cbe1e8d4bb5d19fe944b42d6c5c1#file-query_member-swift" />
    </Frame>
  </Tab>

  <Tab title="Android">
    All participation related methods in a channel fall under a separate `ChannelParticipation` class.

    <Frame>
      <img src="https://gist.github.com/amythee/7fc18ad4ee355b166d791e3be949342d" />
    </Frame>
  </Tab>

  <Tab title="JavaScript">
    You can get a list of all members, or add `memberships`, `roles`, `search` parameters to get certain members of the channel.

    ```javascript
    import { ChannelRepository, MemberFilter } from '@amityco/js-sdk';

    let members;

    const liveCollection = ChannelRepository.queryMembers({ 
      channelId: 'channel1',
      memberships: [MemberFilter.Member],
      roles: ['role1'],
      search: 'asd',
    });

    liveCollection.on('dataUpdated', newModels => {
      members = newModels;
    });

    liveCollection.on('dataError', error => {
      console.error(error);
    });

    members= liveCollection.models;
    ```
  </Tab>

  <Tab title="TypeScript">
    Version 6

    <Frame>
      <img src="https://gist.github.com/amythee/b8bb3bd99bb896c2afc2c91ca64378c3#file-querychannelmembers-ts" />
    </Frame>

    Beta (v0.0.1)

    <Frame>
      <img src="https://gist.github.com/amythee/608812eeae0cec85b92770cf9db7764f#file-livechannelmembers-ts" />
    </Frame>
  </Tab>

  <Tab title="Flutter">
    <Frame>
      <img src="https://gist.github.com/amythee/c1476d8cc7e4a698c49460440b483151#file-amitychannelmembersearch-dart" />
    </Frame>
  </Tab>
</Tabs>