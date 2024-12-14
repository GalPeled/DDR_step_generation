import librosa
import random
import numpy as np
from scipy.stats import mode
from youtube_downloader import yt_link
from song import Song


def detect_bpm_and_beats(audio_file):
    # Load the audio file
    y, sr = librosa.load(audio_file, sr=None)
    
    # Detect tempo (BPM) and beat frames
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    # Compute the self-similarity matrix using chroma features
    #chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
    #similarity_matrix = librosa.segment.recurrence_matrix(chroma, mode='affinity', sym=True)

    # Use spectral clustering to segment the song
    #segmented_labels = librosa.segment.agglomerative(similarity_matrix, k=5)  # Assume 5 sections

    #print("Segments:", segmented_labels)

    # Analyze the onset envelope
    #onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    #pulses = librosa.util.normalize(onset_env)

    song_length = librosa.get_duration(y=y, sr=sr)
    # Convert beat frames to time
    beat_times = librosa.frames_to_time(beats, sr=sr)
    beat_intervals = np.diff(beat_times)
    beats_per_measure = int(np.round(tempo[0] / mode(beat_intervals)[0]))
    print(f"Estimated Tempo: {tempo[0]:.2f} BPM")
    print(f"Estimated Beats per Measure: {beats_per_measure}")
    return np.round(tempo[0],3), beat_times, song_length

def generate_sm_file(audio_file, video_file, output_filename):
    # Detect BPM and beat timings
    bpm, beat_times, song_length = detect_bpm_and_beats(audio_file)
    offset = beat_times[0]
    step_time = 60/bpm
    dist_from_step = step_time/2
    total_dance_move = int(np.ceil(song_length/step_time))
    created_audio_file = audio_file.split('/')[-1]
    title = created_audio_file.split('.')[0]
    # Create SM file header
    sm_file_content = f"""#TITLE:{title};
#SUBTITLE:;
#ARTIST:;
#TITLETRANSLIT:;
#SUBTITLETRANSLIT:;
#ARTISTTRANSLIT:;
#GENRE:;
#CREDIT:;
#MENUCOLOR:;
#METERTYPE:DDR;
#BANNER:;
#BACKGROUND:;
#LYRICSPATH:;
#CDTITLE:;
#MUSIC:{audio_file};
#OFFSET:{-offset};
#SAMPLESTART:;
#SAMPLELENGTH:15.500;
#SELECTABLE:YES;
#LISTSORT:;
#BPMS:0.000={bpm};
#STOPS:;
#BGCHANGES:0={video_file}=1.000=1=1=0===,99999=-nosongbg-=1.000=0=0=0 // don't automatically add -songbackground;
#ATTACKS:;
    """
    # Create note data for one difficulty (basic random note placement)
    sm_file_content += "//---------------dance-single - ----------------\n"
    sm_file_content += "#NOTES:\n"
    sm_file_content += "     dance-single:\n"
    sm_file_content += "     :\n"
    sm_file_content += "     Easy:\n"
    sm_file_content += "     3:\n"
    sm_file_content += "     0.000,0.000,0.000,0.000,0.000:\n"
    step_options =['0000','0000','0000','0000','0000','1000','0100','0010','0001','1000','0100','0010','0001','1100','1010','1001','0110','0101','0011']
    step_count = 0
    max_step_count = 3
    cur_song_time = offset
    beat_index = 0
    # Create notes (simplified version with random step placement)
    for i in range(total_dance_move):
        # Randomly assign left, right, up, or down (4 arrows)
        next_beat_time = beat_times[beat_index]
        while next_beat_time - cur_song_time < -dist_from_step:
            beat_index = beat_index+1
            next_beat_time = beat_times[beat_index]
        step = random.choice(step_options)  # Simplified step generation
        if abs(next_beat_time - cur_song_time) > dist_from_step:
            step = step_options[0]
        else:
            beat_index = beat_index+1
        cur_step = step.count('1')
        if step_count + cur_step > max_step_count:
            step = step_options[0]
        else:
            step_count += cur_step
        sm_file_content += f"{step}\n"
        if (i+1)%4 == 0:
            step_count =0
            sm_file_content += f",\n"
        cur_song_time = cur_song_time + step_time
        if beat_index >= len(beat_times):
            break
    sm_file_content = sm_file_content.rstrip(',')
    sm_file_content += ";"
    # Save the generated SM file
    with open(output_filename, 'w', encoding="utf-8") as sm_file:
        sm_file.write(sm_file_content)
    
    print(f"SM file saved to {output_filename}")

if __name__ == '__main__':
    # Example usage
    # songs_directory = 'd:/Games/OutFox 0.4.19 LTS Win64/Songs/Outfox'
    # youtube_link = 'https://www.youtube.com/watch?v=sh7BZf7D5Bw&ab_channel=CharlieDaniels-Topic'
    # youtube_down = yt_link(youtube_link)
    # song_file, video_file, sm_file_path = youtube_down.create_folder(songs_directory)
    # generate_sm_file(song_file, video_file, sm_file_path)
    file_to_read = 'd:/Games/OutFox 0.4.19 LTS Win64/Songs/HITS OF 2010/FIREWORK/FIREWORK.sm'
    song = Song()
    song.parse_sm_string(file_to_read)
