/// <reference path="../../preamble.d.ts" />
// source: social-plus-sdk/core-concepts/user-management/user-operations/get-user-information.mdx:62-80

import { UserRepository } from '@amityco/ts-sdk';
import { FC, useEffect, useState } from 'react';

const GetUser: FC<{ userId: string }> = ({ userId }) => {
  const [userData, setUserData] = useState<Amity.LiveObject<Amity.User>>();
  const { data: user, loading, error } = userData ?? {};

  useEffect(() => {
    // Get user with live updates
    const unsubscribe = UserRepository.getUser(userId, setUserData);

    return () => unsubscribe();
  }, [userId]);

  if (loading) return null;
  if (error) return null;

  return <div>{user?.displayName}</div>;
};
