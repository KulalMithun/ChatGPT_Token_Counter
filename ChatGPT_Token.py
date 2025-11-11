
import argparse
import json
import re
from typing import Set
import tiktoken
from tqdm import tqdm

def count_tokens(text: str, tokenizer) -> int:
    return len(tokenizer.encode(text))

def find_models_in_export(data) -> Set[str]:
    models = set()
    def scan_obj(obj):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k == "model" and isinstance(v, str):
                    models.add(v)
                else:
                    scan_obj(v)
        elif isinstance(obj, list):
            for item in obj:
                scan_obj(item)
    scan_obj(data)
    return models

def get_tokenizer_for_model(model_name: str):
    try:
        return tiktoken.encoding_for_model(model_name), None
    except Exception as e:
        return tiktoken.get_encoding("cl100k_base"), str(e)

def extract_message_parts(mapping):
    for _, msg_data in mapping.items():
        msg = msg_data.get("message") or {}
        if not isinstance(msg, dict):
            continue
        content = msg.get("content")
        if isinstance(content, dict):
            parts = content.get("parts", [])
            for part in parts:
                if isinstance(part, str):
                    yield part

def main():
    parser = argparse.ArgumentParser(description="Chat export token usage per detected model")
    parser.add_argument("--file", "-f", default="conversations.json", help="Path to ChatGPT export JSON")
    parser.add_argument("--show-cost", action="store_true", help="Show rough cost estimate (uses $/M token defaults)")
    args = parser.parse_args()
    file_path = args.file
    print(f"🔍 Reading {file_path} ...")
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    detected_models = find_models_in_export(data)
    if not detected_models:
        detected_models = {"gpt-4-turbo", "gpt-3.5-turbo"}
    print(f"Detected models: {', '.join(sorted(detected_models))}")

    tokenizers = {}
    tokenizer_warnings = {}
    for model in detected_models:
        tok, warn = get_tokenizer_for_model(model)
        tokenizers[model] = tok
        if warn:
            tokenizer_warnings[model] = warn
    total_chats = len(data)
    results = {}
    for model, tokenizer in tokenizers.items():
        total_tokens = 0
        total_messages = 0
        top_chats = []
        for chat in tqdm(data, desc=f"Processing chats for {model}"):
            mapping = chat.get("mapping", {})
            chat_tokens = 0
            message_count = 0
            for part in extract_message_parts(mapping):
                chat_tokens += count_tokens(part, tokenizer)
                message_count += 1
            total_tokens += chat_tokens
            total_messages += message_count
            top_chats.append((chat.get("title", "Untitled Chat"), chat_tokens, message_count))
        top_chats = sorted(top_chats, key=lambda x: x[1], reverse=True)[:10]
        results[model] = {
            "total_chats": total_chats,
            "total_messages": total_messages,
            "total_tokens": total_tokens,
            "top_chats": top_chats,
        }

    print("\n=== Token Usage Report (per model) ===")
    for model, stats in results.items():
        print(f"\nModel: {model}")
        if model in tokenizer_warnings:
            print(f"  (tokenizer fallback used: {tokenizer_warnings[model]})")
        print(f"  Total chats processed: {stats['total_chats']:,}")
        print(f"  Total messages processed: {stats['total_messages']:,}")
        print(f"  Total tokens used: {stats['total_tokens']:,}")
        if args.show_cost:
            rate_per_million = 5.0 if re.search(r"gpt-4", model) else 0.002 if re.search(r"3.5|gpt-3", model) else 0.0
            print(f"  Estimated cost (approx): ${stats['total_tokens'] / 1_000_000 * rate_per_million:.2f}")

        print("  Top 10 longest chats by tokens:")
        for i, (title, t, m) in enumerate(stats["top_chats"], 1):
            print(f"    {i}. {title[:60]} — {t:,} tokens, {m:,} messages")

if __name__ == "__main__":
    main()