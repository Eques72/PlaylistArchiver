# ![Logo](https://github.com/Eques72/PlaylistArchiver/blob/main/resources/YtArchLogo.png)
---

# YT Playlist Archiver
<table>
<tr>
<td>
  A desktop app created to store and manage locally data from YouTube playlists. It can pull information from YouTube site and save it to json file, perform updates on json archives by adding or removing positions from the playlists, app can display all mismatches and missing videos from archive and from playlist on YT.  
  Archive can be also exported to Spotify.
</td>
</tr>
</table>
---

## Permissions
User needs to specify its credentials in .env file.
- Developer Key to YouTube API
- Spotify Client ID (`optional, only if exporting to Spotify is desired`)
- Spotify Client Secret ID (`optional, only if exporting to Spotify is desired`)
- Spotify Redirect URL (`optional, only if exporting to Spotify is desired`)
### How .env file should look like:
```
KEY="Your Developer Key to YouTube API"
SPOTIFY_CLIENT_ID = 'Your Spotify Client ID'
SPOTIFY_CLIENT_SECRET = 'Your Spotify Client Secret ID'
SPOTIFY_REDIRECT_URI = 'Your Spotify Redirect URL'
```
Developer keys can be obtained here:  
[YouTube for Developers](https://developers.google.com/youtube)  
[Spotify for Developers](https://developer.spotify.com/)
---

## [Usage](https://Eques72.github.io/PlaylistArchiver/) 

### Preconditions
Python 3.x and following libraries: googleapiclient, spotipy, dotenv, tkinter.
Also see [Permissions](https://github.com/Eques72/PlaylistArchiver?tab=readme-ov-file#permissions).

### Clone or download repository
To clone this repository, use the following command:
(`git clone https://github.com/Eques72/PlaylistArchiver.git`)
To download ZIP with the project use this link:
[Project ZIP](https://github.com/Eques72/PlaylistArchiver/archive/refs/heads/main.zip)

### CLI usage
1. Open Terminal and navigate to the project directory.
2. Install dependencies if necessary (See [Preconditions](https://github.com/Eques72/PlaylistArchiver?tab=readme-ov-file#preconditions))
3. Run the CLI tool with the appropriate command:  
`python main_cli.py --mode <1, 2 or 3> --single --url <URL to a playlist or channel ID> --path <Input file or output directory>`  
Eg: `python main_cli.py --mode 1 --single --url https://www.youtube.com/playlist?list=PLbpi6ZahtOH4e5qqR_-Fz0fx64qxYPI5W --path C:\Users\user\Desktop\`
#### Flags:
- --mode - Accepts numbers 1, 2 and 3. 1 opens app in 'Create new Archive' mode, 2 opens app in 'Update Archive' mode, 2 opens app in 'Export to Spotify' mode,
- --single - Optional flag that can be used in mode 1, when provided, program expects playlist URL in --url flag, when absent program expects channel id instead,
- --url - must be provided in mode 1, should contain an URL to a public or non-public playlist or valid channel id,
- --path - In mode 1 path should specify an writable output directory, in mode 2 and 3 path should point to a json archive file created in mode 1,
- --help - Will show all available flags.

### GUI usage
1. Ensure you have a compatible OS and dependencies installed.
2. Open Terminal and navigate to the project directory.
3. Run the GUI app with the appropriate command: `python main.py`
4. Follow the on-screen instructions to use the GUI.

### Custom Front
If you're interested in creating custom frontend for this application, file [PlaylistManager](https://github.com/Eques72/PlaylistArchiver/blob/main/PlaylistManager.py) has all public methods that are needed to introduce all present functionalities to your app, both CLI and GUI may serve as an example of usage.

### File compatibility
Files created by the application should not be tinkered with as this may lead to them being unreadable to the app.
---

## Development
Want to contribute?

To fix a bug or enhance an existing functionalities, follow these steps:

- Fork the repo
- Create a new branch (`git checkout -b new-feature`)
- Make the changes
- Commit your changes (`git commit -am 'New improvement feature, added X...'`)
- Push to the branch (`git push origin new-feature`)
- Create a Pull Request

### Bug / Feature Request

If you find a bug, please open an issue [here](https://github.com/Eques72/PlaylistArchiver/issues/new) by including your search query and the expected result.

If you'd like to request a new function, do so by opening an issue [here](https://github.com/Eques72/PlaylistArchiver/issues/new).
---

## [License](https://github.com/Eques72/PlaylistArchiver/blob/main/LICENSE.md)
MIT © [Eques72](https://github.com/Eques72)
