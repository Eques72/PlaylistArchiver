from PlaylistManager import PlaylistManager
import argparse
import os
from datetime import datetime

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="YouTube playlist archiver."
    )

    pM = PlaylistManager()

    parser.add_argument(
        "--mode",
        type=int,
        help="Mode of operation:\n1 - Create new Archive\n2 - Update Archive\n3 - Export to Spotify",
        default=1,
        required=True
    )

    parser.add_argument(
    "--single",
    action="store_true",
    required=False,
    default=False,
    help="1 - Single playlist mode, 2 - Multiple playlist mode",
    )

    parser.add_argument(
        "--url",
        type=str,
        required=False,
        help="A valid URL to a playlist or chanel ID."
    )
    
    parser.add_argument(
        "--path",
        type=str,
        help="Full path to a file or save directory.",
        default=os.getcwd()
    )
    
    args = parser.parse_args()
    
    print(f"URL: {args.url}")
    print(f"Path: {args.path}")
    print(f"single: {args.single}")
    print(f"mode: {args.mode}")
    
    if args.mode == 1:
        choices = pM.default_video_params.copy()
        if args.single:
            pM.create_new_playlist_record(args.url, choices)
            pM.save_playlist_record(os.path.join(args.path, pM.get_playlist_name(sanitized=True)+".json"), remove_from_list=True)
        else:
            pM.create_multiple_new_playlist_records(args.url, choices)
            pM.save_multiple_playlist_records(os.path.split(args.path)[0], True, True)
        print("Archive/s created successfully.")
    elif args.mode == 2:
        pM.load_playlist_record(args.path)
        n,m,mm = pM.compare_playlist_record_with_online()
        print(f"New elements: {n}\nMissing elements: {m}")
        print(pM.get_playlist_name())
        print(pM.get_playlist_basic_info())
        pM.update_playlist_record(remove_missing=False, add_new=True)
        datetime_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filepath = os.path.splitext(args.path)[0] + f"_updated_{datetime_str}" ".json"
        success = pM.save_playlist_record(filepath, remove_from_list=True)
        print(f"Archive updated successfully: {success}")
    elif args.mode == 3:
        pM.load_playlist_record(args.path)
        print(pM.get_playlist_name())
        print(pM.get_playlist_basic_info())
        added_elements = pM.export_to_spotify()
        print(f"Playlist exported successfully with {added_elements} elements.")
    print("App executed successfully.")

#python main_cli.py --mode 1 --single --url https://www.youtube.com/playlist?list=PLUIixndCOJ8yNBH3FmtlUTxDj-sfBxPEx --path C:\Users\user\Desktop\Newfolder
