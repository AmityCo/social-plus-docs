#!/usr/bin/env python3
"""
fill-ts-gaps.py — Generate TypeScript snippet files for parity gaps.

Usage:
  python3 harness/scripts/fill-ts-gaps.py \
    --parity harness/function-parity.json \
    --ts-snippets-dir ../AmityTypescriptSDK/packages/sdk/src/snippets \
    --android-base ../Amity-Social-Cloud-SDK-Android \
    --batch 30

Requires: pip install anthropic
          ANTHROPIC_API_KEY environment variable
"""
import argparse
import json
import os
import sys


def kebab_to_pascal(s):
    return ''.join(word.capitalize() for word in s.split('-'))


def load_parity(path):
    with open(path) as f:
        return json.load(f)


def find_gaps(parity_data, min_others=2):
    gaps = []
    for fn in parity_data['functions']:
        if not fn.get('key'):
            continue
        plats = fn['platforms']
        ts_status = plats.get('typescript', {}).get('status', 'unknown')
        if ts_status != 'unknown':
            continue
        others_exist = sum(
            1 for p, v in plats.items()
            if p != 'typescript' and v.get('status') == 'exists'
        )
        if others_exist >= min_others:
            gaps.append((others_exist, fn))
    gaps.sort(key=lambda x: -x[0])
    return gaps


def read_android_snippet(fn_entry, android_base):
    android_base = android_base.rstrip(os.sep)  # Ensure no trailing slash for basename
    """Read android reference snippet. android file paths look like
    '../../Amity-Social-Cloud-SDK-Android/amity-sample-code/...'
    android_base is the absolute path to Amity-Social-Cloud-SDK-Android/.
    """
    android = fn_entry['platforms'].get('android', {})
    rel_file = android.get('file', '')
    if not rel_file:
        return None
    # Strip leading path segments: '../', '../', 'Amity-Social-Cloud-SDK-Android/'
    parts = rel_file.replace('\\', '/').split('/')
    # Find repo name in parts and take everything after it
    try:
        repo_idx = next(i for i, p in enumerate(parts) if p == os.path.basename(android_base))
        inner_parts = parts[repo_idx + 1:]
    except StopIteration:
        # Fallback: skip leading '..' segments
        inner_parts = [p for p in parts if p not in ('..', '.') and p != '']
        if inner_parts and inner_parts[0] == os.path.basename(android_base):
            inner_parts = inner_parts[1:]
    abs_path = os.path.join(android_base, *inner_parts)
    if not os.path.exists(abs_path):
        return None
    with open(abs_path) as f:
        return f.read()


def read_existing_ts_example(snippets_dir):
    example_names = ['AmityPostCreateTextPost.ts', 'AmityChannelCreate.ts', 'AmityRoomCreate.ts']
    for name in example_names:
        path = os.path.join(snippets_dir, name)
        if os.path.exists(path):
            with open(path) as f:
                return f.read()
    for fname in sorted(os.listdir(snippets_dir)):
        if fname.endswith('.ts'):
            with open(os.path.join(snippets_dir, fname)) as fh:
                return fh.read()
    return None


def generate_ts_snippet(fn_entry, android_content, ts_example, client):
    key = fn_entry['key']
    doc_page = fn_entry.get('sp_docs_page', '')
    pascal_name = 'Amity' + kebab_to_pascal(key)
    filename = pascal_name + '.ts'

    prompt = f"""You are generating a TypeScript snippet file for the social.plus SDK documentation.

Key: {key}
sp_docs_page: {doc_page}
Output filename: {filename}

Here is the TypeScript snippet pattern to follow (existing example):
```typescript
{ts_example}
```

Here is the Android reference snippet that shows what this function does:
```kotlin
{android_content}
```

Generate a TypeScript snippet that:
1. Starts with `// @ts-nocheck`
2. Has a `/* begin_sample_code` block with `filename`, `sp_docs_page`, and `description` fields
3. Imports from `@amityco/ts-sdk`
4. Implements the equivalent TypeScript code using the @amityco/ts-sdk API
5. Ends with `/* end_sample_code */`

Return ONLY the TypeScript file content. No explanations. No markdown fences."""

    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text.strip()


def write_snippet(content, filename, snippets_dir):
    path = os.path.join(snippets_dir, filename)
    with open(path, 'w') as f:
        f.write(content)
        if not content.endswith('\n'):
            f.write('\n')
    return path


def main():
    parser = argparse.ArgumentParser(description='Generate TypeScript snippet files for parity gaps')
    parser.add_argument('--parity', default='harness/function-parity.json')
    parser.add_argument('--ts-snippets-dir', default='../AmityTypescriptSDK/packages/sdk/src/snippets')
    parser.add_argument('--android-base', default='../Amity-Social-Cloud-SDK-Android')
    parser.add_argument('--batch', type=int, default=30)
    parser.add_argument('--dry-run', action='store_true', help='Print prompts without calling API')
    args = parser.parse_args()

    # script is at harness/scripts/fill-ts-gaps.py
    # repo_root is two levels up (social-plus-docs/)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    harness_dir = os.path.dirname(script_dir)
    repo_root = os.path.dirname(harness_dir)

    parity_path = os.path.join(harness_dir, os.path.basename(args.parity)) if not os.path.isabs(args.parity) else args.parity
    # Handle 'harness/function-parity.json' default
    if args.parity == 'harness/function-parity.json':
        parity_path = os.path.join(harness_dir, 'function-parity.json')
    ts_dir = os.path.normpath(os.path.join(repo_root, args.ts_snippets_dir))
    android_base = os.path.normpath(os.path.join(repo_root, args.android_base))

    print(f"Parity file: {parity_path}")
    print(f"TS snippets dir: {ts_dir}")
    print(f"Android base: {android_base}")

    if not os.path.exists(parity_path):
        print(f"ERROR: parity file not found: {parity_path}", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(ts_dir):
        print(f"ERROR: TS snippets dir not found: {ts_dir}", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(android_base):
        print(f"ERROR: android base not found: {android_base}", file=sys.stderr)
        sys.exit(1)

    parity_data = load_parity(parity_path)
    gaps = find_gaps(parity_data, min_others=2)
    print(f"Total TS gaps (>=2 platforms): {len(gaps)}")

    ts_example = read_existing_ts_example(ts_dir)
    if not ts_example:
        print("ERROR: no existing TS snippets found as examples", file=sys.stderr)
        sys.exit(1)

    if not args.dry_run:
        try:
            import anthropic
        except ImportError:
            print("ERROR: anthropic package not installed. Run: pip install anthropic", file=sys.stderr)
            sys.exit(1)
        api_key = os.environ.get('ANTHROPIC_API_KEY')
        if not api_key:
            print("ERROR: ANTHROPIC_API_KEY not set", file=sys.stderr)
            sys.exit(1)
        client = anthropic.Anthropic(api_key=api_key)
    else:
        client = None

    created = 0
    skipped = 0
    batch = gaps[:args.batch]
    print(f"Processing top {len(batch)} gaps...")

    for _, fn_entry in batch:
        key = fn_entry['key']
        pascal_name = 'Amity' + kebab_to_pascal(key)
        filename = pascal_name + '.ts'
        out_path = os.path.join(ts_dir, filename)

        if os.path.exists(out_path):
            print(f"  [skip] {filename} already exists")
            skipped += 1
            continue

        android_content = read_android_snippet(fn_entry, android_base)
        if not android_content:
            print(f"  [skip] {key}: android reference not found")
            skipped += 1
            continue

        if args.dry_run:
            print(f"  [dry-run] would create {filename} (key={key})")
            continue

        print(f"  [generate] {filename}...", end='', flush=True)
        try:
            content = generate_ts_snippet(fn_entry, android_content, ts_example, client)
            write_snippet(content, filename, ts_dir)
            print(f" ok")
            created += 1
        except Exception as e:
            print(f" FAILED: {e}")
            skipped += 1

    print(f"\nDone: {created} created, {skipped} skipped.")
    if created > 0:
        print(f"\nNext steps:")
        print(f"  1. Review generated files in {ts_dir}")
        print(f"  2. Run: cd harness && ./harness-bin parity --config harness-config.yml")
        print(f"  3. Check TypeScript parity improvement")


if __name__ == '__main__':
    main()
