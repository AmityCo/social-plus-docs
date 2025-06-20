import { UserRepository, subscribeTopic, getUserTopic } from '@amityco/ts-sdk';
import { FC, useEffect, useState } from 'react';

const disposers: Amity.Unsubscriber[] = [];


const GetUsers: FC = () => {
  const [data, setUsers] = useState<Amity.LiveCollection<Amity.User>>();
  const { data: users = [], onNextPage, hasNextPage, loading, error } = data ?? {};

  useEffect(() => {
    const unsubscribe = UserRepository.getUsers(
      {},
      ({ data: users, onNextPage, hasNextPage, loading, error }) => {
        setUsers({
          data: users,
          onNextPage,
          hasNextPage,
          loading,
          error,
        });
      },
    );

  });

  return null;
};