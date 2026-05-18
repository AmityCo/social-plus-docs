/// <reference path="../../preamble.d.ts" />
// source: social-plus-sdk/social/content-management/posts/retrieval/viewing-content.mdx:386-426

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

// Get file post information along with its URL
const getPostFileInfo = async (postId: string): Promise<Amity.File<'file'> | null> => {
  const post = await getPost(postId);
  const firstChildId = post.children?.[0];

  if (firstChildId) {
    const postChildren = await getPost(firstChildId);

    // Ensure the post type is 'file' before attempting to get its image information
    if (postChildren.dataType === 'file') {
      const filePost = postChildren as Amity.Post<'file'>;
      const postFile = await getPostFile<'file'>(filePost.data?.fileId);
      console.log('Post File URL:', postFile?.fileUrl);
      console.log('Post FileId:', postFile?.fileId);
      return postFile;
    }
  }

  return null;
};
