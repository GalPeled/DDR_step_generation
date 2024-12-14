from pytubefix import YouTube 
from abc import ABC
import os
from pydub import AudioSegment

class yt_link(ABC):

    def __init__(self, link):
        self.link = link
        try: 
            self.yt = YouTube(link)
        except:
            print('errore')

    def get_title(self):
        return self.yt.title   
    
    def convert_m4a_to_mp3(self, input_file):
        # Load the .m4a file
        audio = AudioSegment.from_file(input_file, format="m4a")
        output_file = os.path.splitext(input_file)[0]+'.mp3'
        # Export to .mp3
        audio.export(output_file, format="mp3")
        os.remove(input_file)

    def create_folder(self, songs_libery_loc):
        title = self.get_title()
        new_song_loc= f'{songs_libery_loc}/{title}'
        if not os.path.exists(new_song_loc):
            os.makedirs(new_song_loc)
        audio_stream = self.yt.streams.filter(only_audio=True).first()
        audio_stream.download(f'{new_song_loc}')
        video_stream = self.yt.streams.filter(only_video=True).first()
        video_stream.download(f'{new_song_loc}')
        song_file_loc = f'{new_song_loc}/{audio_stream.default_filename}'
        if audio_stream.subtype == 'm4a':
            self.convert_m4a_to_mp3(song_file_loc)
        video_file_loc = f'{video_stream.default_filename}'
        sm_file = os.path.splitext(song_file_loc)[0]+'.sm'
        song_file_loc =  os.path.splitext(song_file_loc)[0]+'.mp3'
        return song_file_loc, video_file_loc, sm_file

