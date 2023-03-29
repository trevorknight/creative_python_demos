""" Demo some music 

"""

import mido

from mido import Message


# Define function to create major chord arpeggio
def create_major_arpeggio(root_note):
    major_third = root_note + 4
    perfect_fifth = root_note + 7
    return [root_note, major_third, perfect_fifth]

# Define function to send arpeggio as MIDI messages
def play_arpeggio(arpeggio, midi_out, duration=0.5):
    for note in arpeggio:
        midi_out.send(Message('note_on', note=note, velocity=64))
        time.sleep(duration)
        midi_out.send(Message('note_off', note=note, velocity=64))

# Set up MIDI input and output ports
midi_in = mido.open_input()
midi_out = mido.open_output()

print("Listening for MIDI input...")

# Main loop
try:
    while True:
        for msg in midi_in.iter_pending():
            if msg.type == 'note_on':
                arpeggio = create_major_arpeggio(msg.note)
                play_arpeggio(arpeggio, midi_out)

except KeyboardInterrupt:
    print("Exiting...")

finally:
    midi_in.close()
    midi_out.close()

