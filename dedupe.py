import json
import argparse
import sys
import time
from typing import Any, List, Union, Dict

def get_hashable(item: Any) -> Any:
    """
    Convert non-hashable items into hashable ones for comparison.
    Using frozenset for dicts is faster and more robust than tuple-of-tuples.
    """
    if isinstance(item, dict):
        # We sort by items to ensure stable hashing
        return frozenset((k, get_hashable(v)) for k, v in item.items())
    if isinstance(item, list):
        return tuple(get_hashable(i) for i in item)
    return item

def deduplicate(data: Any) -> Any:
    """Recursively deduplicate lists within the JSON structure."""
    if isinstance(data, list):
        seen = set()
        new_list = []
        for item in data:
            # Process nested structures first
            processed_item = deduplicate(item)
            # Create a hashable version for the 'seen' set
            hashable_item = get_hashable(processed_item)
            if hashable_item not in seen:
                seen.add(hashable_item)
                new_list.append(processed_item)
        return new_list
    
    if isinstance(data, dict):
        return {k: deduplicate(v) for k, v in data.items()}
    
    return data

def main():
    parser = argparse.ArgumentParser(description="🚀 Optimized JSON Deduplicator")
    parser.add_argument("input", help="Path to input JSON file")
    parser.add_argument("output", help="Path to output JSON file")
    
    args = parser.parse_args()

    try:
        print(f"📂 Reading {args.input}...")
        with open(args.input, 'r') as f:
            data = json.load(f)
        
        print("🧠 Deduplicating...")
        start_time = time.time()
        deduped_data = deduplicate(data)
        duration = time.time() - start_time
        
        print(f"✅ Done in {duration:.2f}s")
        
        print(f"💾 Writing to {args.output}...")
        with open(args.output, 'w') as f:
            json.dump(deduped_data, f, indent=2)
        
        print("✨ All finished!")

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
