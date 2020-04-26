Please place the sound albums that you like to configure on your kids jukebox to the directory current/.

Alternatively you can setup the kids_jukebox to support multiple sets of albums. 
Sorry, the quick hack prototype offer this feature in a more sophisticated way:
For this, you need to delete the folder current/ here and and create multiple other directories. The code by default supports pi1/ and demo/.

pi1 is activated if you set one magnet to top left field 0 and a second magnet to bottom right field 23 when starting the raspberry pi.

demo is activated if you set one magnet to second top left field 6 and a second magnet to bottom right field 23 when starting the raspberry pi.

You can add more sets of albums by modifying the source code: kids_jukebox/kids_jukebox.py:
    collection_dirs = {
        0: "~/kids_jukebox/playlist/pi1",
        6: "~/kids_jukebox/playlist/demo",
    }

