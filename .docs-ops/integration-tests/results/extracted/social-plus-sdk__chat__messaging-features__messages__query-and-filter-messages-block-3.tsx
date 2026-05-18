/// <reference path="../../preamble.d.ts" />
// source: social-plus-sdk/chat/messaging-features/messages/query-and-filter-messages.mdx:365-390

    import { MessageRepository } from '@amityco/ts-sdk';
    import { useEffect, useState } from 'react';

    const JumpToMessage = ({ targetMessageId }: { targetMessageId: string }) => {
      const [messages, setMessages] = useState<Amity.Message[]>();

      useEffect(() => {
        const unsubscribe = MessageRepository.getMessages(
          {
            subChannelId: 'subChannelId',
            aroundMessageId: targetMessageId,
          },
          ({ data: messages, onNextPage, hasNextPage, onPrevPage, hasPrevPage, loading, error }) => {
            if (messages) {
              setMessages(messages);
              // The data contains messages around the target messageId
              // If limit is 10: 5 messages before + target + 4 messages after
            }
          },
        );

        return () => unsubscribe();
      }, [targetMessageId]);

      return null;
    };
