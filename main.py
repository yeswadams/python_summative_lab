import sys
from src.cli import build_cli
from src.storage_manager import StorageManager

def main():
    storage = StorageManager()
    parser = build_cli()
    
    # Parse CLI environment inputs
    args = parser.parse_args()
    
    # Execute the bound function mapping pattern
    if hasattr(args, "func"):
        args.func(args, storage)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()