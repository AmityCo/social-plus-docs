/// <reference path="../../preamble.d.ts" />
// source: social-plus-sdk/core-concepts/user-management/user-operations/get-user-information.mdx:161-219

import { UserRepository } from '@amityco/ts-sdk';

// Get multiple users by IDs
const getUsersByIds = async (userIds: string[]) => {
  try {
    const users = await UserRepository.getUsers(userIds);
    
    users.forEach(user => {
      console.log(`${user.userId}: ${user.displayName}`);
    });
    
    return users;
  } catch (error) {
    console.error('Error getting users:', error);
    throw error;
  }
};

// Get all users with pagination and live updates
const UserListComponent: FC = () => {
  const [usersData, setUsersData] = useState<Amity.LiveCollection<Amity.User>>();
  const { data: users, loading, error, hasNextPage } = usersData ?? {};

  useEffect(() => {
    const unsubscribe = UserRepository.getUsers({}, (liveCollection) => {
      setUsersData(liveCollection);
      
      if (liveCollection.data) {
        console.log(`Loaded ${liveCollection.data.length} users`);
      }
    });

    return () => unsubscribe();
  }, []);

  const loadMore = () => {
    if (usersData && hasNextPage) {
      usersData.nextPage();
    }
  };

  if (loading) return <div>Loading users...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div>
      {users?.map(user => (
        <div key={user.userId}>
          <h4>{user.displayName}</h4>
          <p>ID: {user.userId}</p>
        </div>
      ))}
      
      {hasNextPage && (
        <button onClick={loadMore}>Load More</button>
      )}
    </div>
  );
};
