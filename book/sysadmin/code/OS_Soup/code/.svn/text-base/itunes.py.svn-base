import plistlib, os
tunes = plistlib.readPlist(os.path.expanduser('~/Music/iTunes/iTunes Music Library.xml'))
for track in tunes.Tracks.values():
     print track
     if hasattr(track, 'Rating'):
         print '%s: %d stars' % (track.Name, track.Rating / 20)
     else:
         print '%s: not rated' % track.Name
