/// <reference path="../../preamble.d.ts" />
// source: social-plus-sdk/social/content-management/posts/retrieval/viewing-content.mdx:279-318

import { FileRepository, PostRepository } from '@amityco/ts-sdk';
// Get post data by postId
const getPost = async (postId: string): Promise<Amity.Post> => {
  return new Promise<Amity.Post>(resolve => {
    const unsubscribe = PostRepository.getPost(postId, ({ data, loading }) => {
      if (!loading) {
        resolve(data);
        unsubscribe();
      }
    });
  });
};

// Get file information by fileId
const getPostFile = async <T extends Amity.FileType>(fileId?: string): Promise<Amity.File<T> | null> => {
  if (!fileId) return null;
  const { data: file } = await FileRepository.getFile(fileId);
  return file as Amity.File<T>;
};

// Get image post information along with its URL
const getPostImageInfo = async (postId: string): Promise<Amity.File<'image'> | null> => {
  const post = await getPost(postId);
  const firstChildId = post.children?.[0];

  if (firstChildId) {
    const postChildren = await getPost(firstChildId);

    // Ensure the post type is 'image' before attempting to get its image information
    if (postChildren.dataType === 'image') {
      const imagePost = postChildren as Amity.Post<'image'>;
      const postImage = await getPostFile<'image'>(imagePost.data?.fileId);
      console.log('Post Image URL:', postImage?.fileUrl);
      console.log('Post ImageId:', postImage?.fileId);
      return postImage;
    }
  }

  return null;
};
