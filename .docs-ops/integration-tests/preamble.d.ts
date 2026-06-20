// Shared context declarations for doc-as-test type checking.
// Variables that doc snippets assume exist in their surrounding context.
// Types verified against .docs-ops/sdk-surface/typescript.json before declaring.
//
// ITERATION NOTE: This preamble will be incomplete on first run. 
// Add missing declarations as "Cannot find name 'X'" failures surface.

import type { Client, Channel, Message, Post, Comment, Community, User, Poll, File as AmityFile } from '@amityco/ts-sdk';

// ── Setup ─────────────────────────────────────────────────────────────────────
declare const apiKey: string;
declare const region: 'sg' | 'eu' | 'us';
declare const userId: string;
declare const displayName: string;
declare const authToken: string;

// ── Client ────────────────────────────────────────────────────────────────────
declare const client: Amity.Client;

// ── Chat cohort ───────────────────────────────────────────────────────────────
declare const channelId: string;
declare const subChannelId: string;
declare const messageId: string;
declare const channel: Amity.Channel;
declare const message: Amity.Message;

// ── Social cohort ─────────────────────────────────────────────────────────────
declare const postId: string;
declare const communityId: string;
declare const commentId: string;
declare const pollId: string;
declare const post: Amity.Post;
declare const comment: Amity.Comment;
declare const community: Amity.Community;

// ── User ──────────────────────────────────────────────────────────────────────
declare const user: Amity.User;

// ── File / media ──────────────────────────────────────────────────────────────
declare const fileId: string;
declare const imageFileId: string;
declare const videoFileId: string;
declare const streamId: string;
declare const roomId: string;
declare const imageUrl: string;

// ── Misc context vars commonly used in snippets ───────────────────────────────
declare const memberId: string;
declare const targetId: string;
declare const targetType: string;
declare const reactionName: string;
declare const token: any;   // live-object token (unsubscriber)
declare function renderResults(data: any): void;
declare function updateUI(data: any): void;
declare function showLoading(): void;
declare function hideLoading(): void;
declare function handleError(e: any): void;
