#!/usr/bin/env python3
"""
extract-blocks.py (Android) — Walk pages.json, extract every ```kotlin and ```java
fenced code block, wrap in preamble function/class body, write one .kt/.java file per
block into results/extracted/.

Handles:
  - ```kotlin AND ```java fenced blocks
  - Kotlin: wrapped in top-level fun docSnippet(…) { <BODY> }
  - Java: wrapped in class DocSnippet { void docSnippet() { <BODY> } }
  - enumerate: entries in pages.json
  - Skip markers: <!-- doc-as-test: skip --> or {/* doc-as-test: skip */}
  - Hoist import statements from block body to file-level
"""

import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
DOCS_ROOT = (SCRIPT_DIR / "../../..").resolve()  # social-plus-docs/
OUTPUT_DIR = SCRIPT_DIR / "results" / "extracted"
PAGES_JSON = SCRIPT_DIR / "pages.json"

FENCE_OPEN_RE = re.compile(r'^[ \t]*```(kotlin|java)\b.*$', re.IGNORECASE)
FENCE_CLOSE_RE = re.compile(r'^[ \t]*```\s*$')
SKIP_MARKER_RE = re.compile(r'doc-as-test:\s*skip(?:\s*\(([^)]*)\))?', re.IGNORECASE)
IMPORT_RE = re.compile(r"^\s*import\s+\S+")

PREAMBLE_IMPORTS = """\
import com.amity.socialcloud.sdk.api.core.AmityCoreClient
import com.amity.socialcloud.sdk.api.chat.AmityChatClient
import com.amity.socialcloud.sdk.api.social.AmitySocialClient
import com.amity.socialcloud.sdk.api.chat.channel.AmityChannelRepository
import com.amity.socialcloud.sdk.api.chat.message.AmityMessageRepository
import com.amity.socialcloud.sdk.api.social.post.AmityFeedRepository
import com.amity.socialcloud.sdk.api.social.post.AmityPostRepository
import com.amity.socialcloud.sdk.api.social.community.AmityCommunityRepository
import com.amity.socialcloud.sdk.api.social.community.query.AmityCommunitySortOption
import com.amity.socialcloud.sdk.api.social.category.query.AmityCommunityCategorySortOption
import com.amity.socialcloud.sdk.api.social.member.query.AmityCommunityMembershipSortOption
import com.amity.socialcloud.sdk.api.core.user.AmityUserRepository
import com.amity.socialcloud.sdk.api.core.user.search.AmityUserSortOption
import com.amity.socialcloud.sdk.api.core.file.AmityFileRepository
import com.amity.socialcloud.sdk.model.chat.channel.AmityChannel
import com.amity.socialcloud.sdk.model.chat.channel.AmityChannelFilter
import com.amity.socialcloud.sdk.model.chat.message.AmityMessage
import com.amity.socialcloud.sdk.model.chat.member.AmityChannelMember
import com.amity.socialcloud.sdk.model.chat.member.AmityMembershipType
import com.amity.socialcloud.sdk.model.chat.notification.AmityChannelNotificationSettings
import com.amity.socialcloud.sdk.model.social.post.AmityPost
import com.amity.socialcloud.sdk.model.social.community.AmityCommunity
import com.amity.socialcloud.sdk.model.social.community.AmityCommunityFilter
import com.amity.socialcloud.sdk.model.social.community.AmityCommunityPostSettings
import com.amity.socialcloud.sdk.model.social.community.AmityCommunityStorySettings
import com.amity.socialcloud.sdk.model.social.community.AmityJoinResult
import com.amity.socialcloud.sdk.model.social.community.AmityJoinRequest
import com.amity.socialcloud.sdk.model.social.community.AmityJoinRequestStatus
import com.amity.socialcloud.sdk.model.social.category.AmityCommunityCategory
import com.amity.socialcloud.sdk.model.social.member.AmityCommunityMember
import com.amity.socialcloud.sdk.model.social.member.AmityCommunityMembership
import com.amity.socialcloud.sdk.model.social.member.AmityCommunityMembershipFilter
import com.amity.socialcloud.sdk.model.core.invitation.AmityInvitation
import com.amity.socialcloud.sdk.model.core.invitation.AmityInvitationStatus
import com.amity.socialcloud.sdk.model.chat.settings.AmityMembershipAcceptanceType
import com.amity.socialcloud.sdk.model.social.comment.AmityComment
import com.amity.socialcloud.sdk.model.social.notification.AmityCommunityNotificationSettings
import com.amity.socialcloud.sdk.model.social.notification.AmityCommunityNotificationEvent
import com.amity.socialcloud.sdk.model.core.user.AmityUser
import com.amity.socialcloud.sdk.model.core.user.AmityUserType
import com.amity.socialcloud.sdk.model.core.permission.AmityPermission
import com.amity.socialcloud.sdk.model.social.poll.AmityPoll
import com.amity.socialcloud.sdk.model.core.file.AmityImage
import com.amity.socialcloud.sdk.model.core.file.AmityFile
import com.amity.socialcloud.sdk.model.core.file.AmityVideo
import com.amity.socialcloud.sdk.model.core.file.AmityClip
import com.amity.socialcloud.sdk.model.core.file.AmityAudio
import com.amity.socialcloud.sdk.model.core.file.AmityAttachment
import com.amity.socialcloud.sdk.model.core.file.AmityVideoResolution
import com.amity.socialcloud.sdk.model.core.file.AmityRawFile
import com.amity.socialcloud.sdk.model.core.file.AmityFileType
import com.amity.socialcloud.sdk.model.core.file.upload.AmityUploadResult
import com.amity.socialcloud.sdk.model.core.tag.AmityTags
import com.amity.socialcloud.sdk.model.core.pin.AmityPinnedPost
import com.amity.socialcloud.sdk.model.core.error.AmityException
import com.amity.socialcloud.sdk.model.core.error.AmityError
import com.amity.socialcloud.sdk.model.core.link.AmityLink
import com.amity.socialcloud.sdk.model.core.role.AmityRoles
import com.amity.socialcloud.sdk.model.core.notification.AmityRolesFilter
import com.amity.socialcloud.sdk.model.core.notification.AmityUserNotificationModule
import com.amity.socialcloud.sdk.model.core.producttag.AmityProductTag
import com.amity.socialcloud.sdk.model.core.producttag.AmityAttachmentProductTags
import com.amity.socialcloud.sdk.model.core.content.AmityContentFeedType
import com.amity.socialcloud.sdk.model.core.session.SessionHandler
import com.amity.socialcloud.sdk.model.core.session.AccessTokenHandler
import com.amity.socialcloud.sdk.model.core.session.AmityUserToken
import com.google.gson.JsonObject
import com.amity.socialcloud.sdk.model.video.room.AmityRoom
import com.amity.socialcloud.sdk.model.video.room.AmityRoomStatus
import com.amity.socialcloud.sdk.model.video.stream.AmityStream
import com.amity.socialcloud.sdk.api.core.endpoint.AmityEndpoint
import com.amity.socialcloud.sdk.api.core.encryption.AmityDBEncryption
import com.amity.socialcloud.sdk.api.core.session.AmityAccessTokenEstablisher
import com.amity.socialcloud.sdk.api.core.token.AmityUserTokenManager
import com.amity.socialcloud.sdk.api.core.user.notification.AmityUserNotification
import com.amity.socialcloud.sdk.helper.core.asAmityFile
import com.amity.socialcloud.sdk.helper.core.asAmityImage
import com.amity.socialcloud.sdk.helper.core.asAmityVideo
import com.amity.socialcloud.sdk.api.social.post.query.AmityUserFeedSortOption
import com.amity.socialcloud.sdk.api.social.post.query.AmityCommunityFeedSortOption
import com.amity.socialcloud.sdk.api.social.post.review.AmityReviewStatus
import com.amity.socialcloud.sdk.api.chat.member.query.AmityChannelMembershipFilter
import com.amity.socialcloud.sdk.api.chat.member.query.AmityChannelMembershipSortOption
import com.amity.socialcloud.sdk.core.session.model.SessionState
import com.amity.socialcloud.sdk.core.session.AccessTokenRenewal
import androidx.paging.PagingData
import io.reactivex.rxjava3.android.schedulers.AndroidSchedulers
import io.reactivex.rxjava3.schedulers.Schedulers
import io.reactivex.rxjava3.core.Completable
import io.reactivex.rxjava3.core.Flowable
import io.reactivex.rxjava3.core.Observable
import android.app.Application
import android.content.Context
import android.net.Uri
import android.util.Log
import java.util.Calendar
import org.joda.time.DateTime"""

# Stub functions for common pseudocode patterns used in doc snippets
KOTLIN_STUBS = """\
// Stubs for illustrative helper functions used in doc snippets
@Suppress("UNUSED_PARAMETER")
fun showSuccessMessage(msg: Any = "") {}
@Suppress("UNUSED_PARAMETER")
fun showErrorMessage(msg: Any = "", error: Throwable? = null) {}
@Suppress("UNUSED_PARAMETER")
fun notifyMessageDeleted(id: String = "") {}
@Suppress("UNUSED_PARAMETER")
fun notifyFailedMessagesCleared() {}
@Suppress("UNUSED_PARAMETER")
fun handleFlagSuccess(id: String = "", reason: Any? = null) {}
@Suppress("UNUSED_PARAMETER")
fun handleFlagError(error: Throwable? = null, id: String = "") {}
@Suppress("UNUSED_PARAMETER")
fun handleUnflagSuccess(id: String = "") {}
@Suppress("UNUSED_PARAMETER")
fun handleUnflagError(error: Throwable? = null, id: String = "") {}
@Suppress("UNUSED_PARAMETER")
fun handleBulkDeletionError(error: Throwable? = null) {}
@Suppress("UNUSED_PARAMETER")
fun handleDeletionError(error: Throwable? = null) {}
@Suppress("UNUSED_PARAMETER")
fun handleNetworkError(error: Throwable? = null) {}
@Suppress("UNUSED_PARAMETER")
fun proceedWithNormalOperation() {}
@Suppress("UNUSED_PARAMETER")
fun setup(client: Any? = null) {}
@Suppress("UNUSED_PARAMETER")
fun showLogin() {}
@Suppress("UNUSED_PARAMETER")
fun showBannedWordError(msg: Any = "") {}
@Suppress("UNUSED_PARAMETER")
fun handleGeneralError(error: Throwable? = null) {}
@Suppress("UNUSED_PARAMETER")
fun getPagingData(adapter: Any? = null) {}
@Suppress("UNUSED_PARAMETER")
fun deletePost(id: Any? = null) {}
@Suppress("UNUSED_PARAMETER")
fun updateUserProfile(user: Any? = null) {}
@Suppress("UNUSED_PARAMETER")
fun authenticateToSocialPlus(userId: String = "") {}
@Suppress("UNUSED_PARAMETER")
fun showUnflagSuccessMessage() {}
@Suppress("UNUSED_PARAMETER")
fun updateMessageUI(id: String = "", isFlagged: Boolean = false) {}
val signature: String = ""
val expiresAt: DateTime = DateTime.now()
data class VisitorAuthData(val signature: String, val expiresAt: DateTime)
@Suppress("UNUSED_PARAMETER")
fun fetchAuthSignature(deviceId: String, callback: (String, DateTime) -> Unit) {
    callback(signature, expiresAt)
}
object authRepository {
    @Suppress("UNUSED_PARAMETER")
    fun fetchVisitorAuthSignature(deviceId: String, callback: (VisitorAuthData?) -> Unit) {
        callback(VisitorAuthData(signature, expiresAt))
    }
}"""

KOTLIN_PARAMS = """\
    apiKey: String = "",
    userId: String = "user-id",
    displayName: String = "User",
    authToken: String = "token",
    channelId: String = "channel-id",
    subChannelId: String = "sub-channel-id",
    messageId: String = "message-id",
    postId: String = "post-id",
    communityId: String = "community-id",
    commentId: String = "comment-id",
    pollId: String = "poll-id",
    fileId: String = "file-id",
    targetUserId: String = "target-user-id",
    channelRepository: AmityChannelRepository = AmityChatClient.newChannelRepository(),
    messageRepository: AmityMessageRepository = AmityChatClient.newMessageRepository(),
    postRepository: AmityPostRepository = AmitySocialClient.newPostRepository(),
    sessionHandler: SessionHandler = object : SessionHandler {
        override fun sessionWillRenewAccessToken(renewal: AccessTokenRenewal) {}
    },
    channel: AmityChannel? = null,
    message: AmityMessage? = null,
    post: AmityPost? = null,
    comment: AmityComment? = null,
    community: AmityCommunity? = null,
    user: AmityUser? = null,
    poll: AmityPoll? = null,
    amityImage: AmityImage? = null"""

JAVA_IMPORTS = """\
import com.amity.socialcloud.sdk.api.core.AmityCoreClient;
import com.amity.socialcloud.sdk.api.chat.AmityChatClient;
import com.amity.socialcloud.sdk.api.social.AmitySocialClient;"""


def resolve_pages(pages_data):
    paths = []
    all_entries = (
        pages_data.get("android_specific", [])
        + pages_data.get("audited_root", [])
        + pages_data.get("audited_getting_started", [])
        + pages_data.get("audited_user_management", [])
        + pages_data.get("audited_social_entry", [])
        + pages_data.get("audited_community_lifecycle", [])
        + pages_data.get("audited_community_discovery", [])
        + pages_data.get("audited_community_organization", [])
        + pages_data.get("audited_community_admin", [])
        + pages_data.get("audited_content_foundation", [])
        + pages_data.get("audited_post_creation_core", [])
        + pages_data.get("audited_post_creation_secondary", [])
        + pages_data.get("audited_post_creation_media_advanced", [])
        + pages_data.get("audited_post_creation_realtime_types", [])
        + pages_data.get("audited_post_retrieval_viewing", [])
        + pages_data.get("audited_post_moderation", [])
        + pages_data.get("audited_post_analytics", [])
        + pages_data.get("audited_comment_creation", [])
        + pages_data.get("audited_comment_retrieval", [])
        + pages_data.get("chat_track", [])
        + pages_data.get("social_track", [])
        + pages_data.get("shared", [])
    )
    for entry in all_entries:
        if entry.startswith("enumerate:"):
            dir_path = DOCS_ROOT / entry[len("enumerate:"):]
            if dir_path.is_dir():
                for mdx in sorted(dir_path.glob("*.mdx")):
                    paths.append(str(mdx.relative_to(DOCS_ROOT)))
            else:
                print(f"  WARN: enumerate dir not found: {dir_path}", file=sys.stderr)
        else:
            full = DOCS_ROOT / entry
            if full.exists():
                paths.append(entry)
            else:
                print(f"  WARN: page not found: {entry}", file=sys.stderr)
    seen = set()
    deduped = []
    for p in paths:
        if p not in seen:
            seen.add(p)
            deduped.append(p)
    return deduped


def extract_blocks(page_path):
    """Returns (extracted_blocks, skipped_blocks). Each extracted block has content, lang, start_line, end_line."""
    full_path = DOCS_ROOT / page_path
    text = full_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    extracted = []
    skipped = []
    in_block = False
    block_lang = None
    block_lines = []
    block_start = 0
    pending_skip = None

    for i, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not in_block:
            skip_m = SKIP_MARKER_RE.search(stripped) if stripped else None
            if skip_m:
                pending_skip = skip_m.group(1) or "skip"
            elif stripped:
                m = FENCE_OPEN_RE.match(line)
                if m:
                    lang = m.group(1).lower()
                    if pending_skip is not None:
                        skipped.append({"file": page_path, "line": i, "lang": lang, "reason": pending_skip})
                        in_block = True
                        block_lang = None  # skipped
                        block_lines = []
                        block_start = 0
                    else:
                        in_block = True
                        block_lang = lang
                        block_lines = []
                        block_start = i + 1
                    pending_skip = None
                else:
                    pending_skip = None
        else:
            if FENCE_CLOSE_RE.match(line):
                if block_lang is not None and block_start != 0 and block_lines:
                    extracted.append({
                        "content": "\n".join(block_lines),
                        "lang": block_lang,
                        "start_line": block_start,
                        "end_line": i - 1,
                    })
                in_block = False
                block_lang = None
                block_lines = []
                block_start = 0
            else:
                block_lines.append(line)

    return extracted, skipped


def page_to_slug(page_path):
    return page_path.replace("/", "__").replace(".mdx", "")


def split_imports(content):
    """Split block content into (imports, body) lines."""
    import_lines = []
    body_lines = []
    for line in content.splitlines():
        if IMPORT_RE.match(line):
            import_lines.append(line.rstrip())
        else:
            body_lines.append(line)
    return "\n".join(import_lines), "\n".join(body_lines)


def write_kotlin_block(slug, block_index, block, page_path):
    filename = f"{slug}-block-{block_index}.kt"
    out_path = OUTPUT_DIR / filename

    extra_imports_raw, body = split_imports(block["content"])
    extra_imports = []
    for imp in extra_imports_raw.splitlines():
        imp = imp.strip()
        if imp and not any(preamble_imp in imp for preamble_imp in PREAMBLE_IMPORTS.splitlines()):
            extra_imports.append(imp)

    source_comment = f"// source: {page_path}:{block['start_line']}-{block['end_line']}"
    extra_import_block = ("\n" + "\n".join(extra_imports)) if extra_imports else ""

    indented_body = "\n".join("    " + l if l.strip() else "" for l in body.splitlines())

    content = f"""{source_comment}
{PREAMBLE_IMPORTS}{extra_import_block}

{KOTLIN_STUBS}

@Suppress("UNUSED_VARIABLE", "UNUSED_PARAMETER", "NAME_SHADOWING", "UNREACHABLE_CODE")
fun docSnippet(
{KOTLIN_PARAMS}
) {{
{indented_body}
}}
"""
    out_path.write_text(content, encoding="utf-8")
    return out_path


def write_java_block(slug, block_index, block, page_path):
    filename = f"{slug}-block-{block_index}.java"
    out_path = OUTPUT_DIR / filename

    extra_imports_raw, body = split_imports(block["content"])
    extra_imports = [l.rstrip() for l in extra_imports_raw.splitlines() if l.strip() and not l.strip().endswith(";")]
    # Java imports should end with ;
    extra_java_imports = []
    for imp in extra_imports_raw.splitlines():
        imp = imp.strip()
        if not imp:
            continue
        if not imp.endswith(";"):
            imp = imp + ";"
        if imp not in JAVA_IMPORTS:
            extra_java_imports.append(imp)

    source_comment = f"// source: {page_path}:{block['start_line']}-{block['end_line']}"
    extra_import_block = ("\n" + "\n".join(extra_java_imports)) if extra_java_imports else ""

    indented_body = "\n".join("        " + l if l.strip() else "" for l in body.splitlines())

    content = f"""{source_comment}
{JAVA_IMPORTS}{extra_import_block}

@SuppressWarnings("unused")
class DocSnippetBlock{block_index} {{
    void docSnippet(String userId, String channelId, String messageId) throws Exception {{
{indented_body}
    }}
}}
"""
    out_path.write_text(content, encoding="utf-8")
    return out_path


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for old in OUTPUT_DIR.glob("*.kt"):
        old.unlink()
    for old in OUTPUT_DIR.glob("*.java"):
        old.unlink()

    pages_data = json.loads(PAGES_JSON.read_text())
    pages = resolve_pages(pages_data)

    total_extracted = 0
    total_skipped = 0
    page_stats = {}
    all_skipped = []

    print(f"Extracting kotlin/java blocks from {len(pages)} pages...")
    for page_path in pages:
        ext, skp = extract_blocks(page_path)
        slug = page_to_slug(page_path)
        kt_count = 0
        for block in ext:
            if block["lang"] == "kotlin":
                kt_count += 1
                write_kotlin_block(slug, kt_count, block, page_path)
            else:  # java
                kt_count += 1
                write_java_block(slug, kt_count, block, page_path)
        all_skipped.extend(skp)
        page_stats[page_path] = {"extracted": len(ext), "skipped": len(skp)}
        total_extracted += len(ext)
        total_skipped += len(skp)
        if ext or skp:
            langs = {}
            for b in ext:
                langs[b["lang"]] = langs.get(b["lang"], 0) + 1
            skip_note = f" (skipped {len(skp)})" if skp else ""
            lang_note = " ".join(f"{k}={v}" for k, v in langs.items())
            print(f"  {page_path}: {len(ext)} block(s) [{lang_note}]{skip_note}")

    print(f"\nTotal: {total_extracted} extracted, {total_skipped} skipped, from {len(pages)} pages")
    print(f"Output: {OUTPUT_DIR}")

    manifest = {
        "pages": pages,
        "page_stats": page_stats,
        "total_extracted": total_extracted,
        "total_skipped": total_skipped,
        "skipped_blocks": all_skipped,
    }
    manifest_path = OUTPUT_DIR / "_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))
    print(f"Manifest: {manifest_path}")


if __name__ == "__main__":
    main()
