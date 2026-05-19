/// <reference path="../../preamble.d.ts" />
// source: social-plus-sdk/chat/conversation-management/members/join-leave-channel.mdx:224-237

    import { ChannelRepository } from '@amityco/ts-sdk';
    import { FC, useEffect, useState } from 'react';

    const ObserveMembership: FC<{ channelId: string }> = ({ channelId }) => {
      const [data, setChannelMembers] = useState<Amity.LiveCollection<Amity.Membership<'channel'>>>();
      const { data: channelMembers, loading, error } = data ?? {};

      useEffect(
        () => ChannelRepository.Membership.getMembers({ channelId }, setChannelMembers),
        [channelId],
      );

      return null;
    };
