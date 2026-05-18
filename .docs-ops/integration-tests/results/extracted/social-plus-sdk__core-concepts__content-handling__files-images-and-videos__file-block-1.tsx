/// <reference path="../../preamble.d.ts" />
// source: social-plus-sdk/core-concepts/content-handling/files-images-and-videos/file.mdx:126-144

import React from 'react';
import { FileRepository } from '@amityco/ts-sdk';

const FileUpload = () => {
  const changeHandler = async (event: React.ChangeEvent<HTMLInputElement>) => {
    if (!event.target.files) {
      return;
    }

    const data = new FormData();
    data.append('files', event.target.files[0]);

    const { data: file } = await FileRepository.uploadFile(data);

    return file;
  };

  return <input type="file" name="file" onChange={changeHandler} />;
};
