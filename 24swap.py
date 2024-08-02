import os
import ttkbootstrap as tk
from tkinter import filedialog
from pydub import AudioSegment
from pydub.playback import play
from pydub.utils import mediainfo
path = input("请输入ffmpeg路径")
os.environ["PATH"] += os.pathsep + path
def swap_beats(audio_file, output_file, beats_per_measure=4, tempo_bpm=120):
    try:
        song = AudioSegment.from_file(audio_file)
        sample_rate = mediainfo(audio_file)['sample_rate']
        beat_duration_ms = 60 * 1000 / tempo_bpm
        measure_duration_ms = beat_duration_ms * beats_per_measure
        modified_song = AudioSegment.empty()
        for start_time in range(0, len(song), int(measure_duration_ms)):
            second_beat_start = start_time + int(beat_duration_ms)
            fourth_beat_start = start_time + int(3 * beat_duration_ms)
            first_beat = song[start_time:second_beat_start]
            second_beat = song[second_beat_start:fourth_beat_start]
            fourth_beat = song[fourth_beat_start:start_time + int(measure_duration_ms)]
            modified_song += first_beat + fourth_beat + second_beat
        modified_song.export(output_file, format="mp3")
    except Exception as e:
        print(f"An error occurred: {e}")
def browse_input_file():
    input_file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3")])
    input_entry.delete(0, tk.END)
    input_entry.insert(0, input_file_path)

def browse_output_file():
    output_file_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 Files", "*.mp3")])
    output_entry.delete(0, tk.END)
    output_entry.insert(0, output_file_path)

def run_swap_beats():
    input_file = input_entry.get()
    output_file = output_entry.get()
    bpm = int(bpm_entry.get())
    swap_beats(input_file, output_file, tempo_bpm=bpm)
root = tk.Window()
root.title("傻逼小工具")
input_label = tk.Label(root, text="输入:")
input_label.grid(row=0, column=0, sticky=tk.E)
input_entry = tk.Entry(root, width=50)
input_entry.grid(row=0, column=1)
browse_input_button = tk.Button(root, text="浏览", command=browse_input_file)
browse_input_button.grid(row=0, column=2)
output_label = tk.Label(root, text="输出:")
output_label.grid(row=1, column=0, sticky=tk.E)
output_entry = tk.Entry(root, width=50)
output_entry.grid(row=1, column=1)
browse_output_button = tk.Button(root, text="浏览", command=browse_output_file)
browse_output_button.grid(row=1, column=2)

# BPM输入
bpm_label = tk.Label(root, text="BPM:")
bpm_label.grid(row=2, column=0, sticky=tk.E)
bpm_entry = tk.Entry(root, width=10)
bpm_entry.insert(0, "120")
bpm_entry.grid(row=2, column=1, sticky=tk.W)

# 运行按钮
run_button = tk.Button(root, text="开造", command=run_swap_beats)
run_button.grid(row=3, column=1, sticky=tk.E)

# 启动GUI
root.mainloop()
