#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import argparse
import re

from collections import Counter
from datetime import datetime
from pathlib import Path


def check_mixed_layout(text: str) -> list[tuple[str, list[str]]]:
    words: list[str] = re.findall(r"\b[a-zA-Zа-яА-ЯёЁ]+\b", text)
    corrupted_words: list[tuple[str, list[str]]] = []

    for word in words:
        has_lat: bool = bool(re.search(r"[a-zA-Z]", word))
        has_cyr: bool = bool(re.search(r"[а-яА-ЯёЁ]", word))

        if has_lat and has_cyr:
            cyr_letters: list[str] = re.findall(r"[а-яА-ЯёЁ]", word)
            corrupted_words.append((word, cyr_letters))

    return corrupted_words


def process(path: Path, extensions: set[str], ignore_words: set[str]) -> None:
    path = path.resolve()

    if not path.is_dir():
        raise Exception(f"Path {str(path)!r} must be a directory")

    total_files_count: int = 0
    checked_files_count: int = 0
    corrupted_files_count: int = 0
    corrupted_words_count: int = 0
    ignored_words_count: int = 0

    suffix_total_counter: dict[str, int] = Counter()
    suffix_checked_counter: dict[str, int] = Counter()
    suffix_corrupted_files_counter: dict[str, int] = Counter()
    suffix_corrupted_words_counter: dict[str, int] = Counter()

    start_dt: datetime = datetime.now()

    for f in path.rglob("*.*"):
        if not f.is_file():
            continue

        total_files_count += 1
        suffix_total_counter[f.suffix] += 1

        if f.suffix not in extensions:
            continue

        try:
            checked_files_count += 1
            suffix_checked_counter[f.suffix] += 1

            text: str = f.read_text("utf-8")
            corrupted_words: list[tuple[str, list[str]]] = check_mixed_layout(text)
            if corrupted_words:
                corrupted_files_count += 1
                suffix_corrupted_files_counter[f.suffix] += 1

                valid_corrupted_words: list[tuple[str, list[str]]] = []
                for word, cyr_letters in corrupted_words:
                    if word.lower() in ignore_words:
                        ignored_words_count += 1
                    else:
                        valid_corrupted_words.append((word, cyr_letters))

                if valid_corrupted_words:
                    corrupted_words_count += len(valid_corrupted_words)
                    suffix_corrupted_words_counter[f.suffix] += len(valid_corrupted_words)

                    print(f"File: {str(f)!r}")
                    for word, cyr_letters in valid_corrupted_words:
                        print(f"    Word: {word!r}, letters: {cyr_letters}")
                    print()

        except UnicodeError as e:
            print(f"{f} skip, error: {e}")

    print(f"Elapsed: {datetime.now() - start_dt}")
    print()

    print("=== SUMMARY STATISTICS ===")
    print(f"Total files found:         {total_files_count}")
    print(f"Total checked files:       {checked_files_count}")
    print(f"Files with mixed layout:   {corrupted_files_count}")
    print(f"Words with mixed layout:   {corrupted_words_count}")
    print(f'Ignored words count:       {ignored_words_count}')
    print()
    print(f"All extensions in path:    {dict(suffix_total_counter)}")
    print(f"Checked extensions:        {dict(suffix_checked_counter)}")
    print(f"Corrupted files by suffix: {dict(suffix_corrupted_files_counter)}")
    print(f"Corrupted words by suffix: {dict(suffix_corrupted_words_counter)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Cyrillic and Latin alphabet audit",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "path",
        metavar="/PATH/TO/DIRECTORY",
        type=Path,
        help="Path to directory",
    )
    parser.add_argument(
        "-e",
        "--ext",
        nargs="+",
        default=[".xml", ".java", ".xsd"],
        help="File extensions to check",
    )
    parser.add_argument(
        '-i',
        '--ignore-words',
        nargs='+',
        default=[],
        help='Words to ignore (case-insensitive)',
    )
    args = parser.parse_args()

    target_extensions: set[str] = {
        ex if ex.startswith(".") else f".{ex}" for ex in args.ext
    }
    target_ignore_words: set[str] = {word.lower() for word in args.ignore_words}

    process(
        path=args.path,
        extensions=target_extensions,
        ignore_words=target_ignore_words,
    )
