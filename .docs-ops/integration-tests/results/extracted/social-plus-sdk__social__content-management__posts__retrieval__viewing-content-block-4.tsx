/// <reference path="../../preamble.d.ts" />
// source: social-plus-sdk/social/content-management/posts/retrieval/viewing-content.mdx:519-574

import { FileRepository, PostRepository } from '@amityco/ts-sdk';

// Get details of a video post's children.
const getVideoPostChildren = async (postId: string): Promise<{ fileId?: string, thumbnailFileId?: string }> => {
  const post = await new Promise<Amity.Post>((resolve, reject) => {
    const unsubscribe = PostRepository.getPost(postId, ({ data, loading, error }) => {
      if (!loading) {
        if (error) {
          reject(error);
        } else {
          resolve(data);
        }
        unsubscribe();
      }
    });
  });

  const postChildrenId = post.children[0];
  const postChildren = await new Promise<Amity.Post<'video'>>((resolve, reject) => {
    const unsubscribe = PostRepository.getPost(postChildrenId, ({ data, loading, error }) => {
      if (!loading) {
        if (error) {
          reject(error);
        } else {
          resolve(data as Amity.Post<'video'>);
        }
        unsubscribe();
      }
    });
  });

  return {
    fileId: postChildren.data?.videoFileId.original,
    thumbnailFileId: postChildren.data?.thumbnailFileId,
  };
};

// Get file information by fileId
const getPostFile = async <T extends Amity.FileType>(fileId?: string): Promise<Amity.File<T> | null> => {
  if (!fileId) return null;
  const { data: file } = await FileRepository.getFile(fileId);
  return file as Amity.File<T>;
};

// Retrieve URLs for video and its thumbnail.
const fetchVideoAndThumbnail = async (postId: string) => {
  const { fileId, thumbnailFileId } = await getVideoPostChildren(postId);
  const videoFile = await getPostFile<'video'>(fileId);
  const thumbnailFile = await getPostFile<'image'>(thumbnailFileId);

  console.log('Video 360p URL:', videoFile?.videoUrl?.['360p']);
  console.log('Video 480p URL:', videoFile?.videoUrl?.['480p']);
  console.log('Video 360p URL:', videoFile?.videoUrl?.['720p']);
  console.log('Video 360p URL:', videoFile?.videoUrl?.['1080p']);
  console.log('Thumbnail URL:', thumbnailFile?.fileUrl);
};
