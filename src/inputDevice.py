import pyaudio
def main_test():
    pa = pyaudio.PyAudio()
    print('\navailable devices:')
    for i in range(pa.get_device_count()):
        dev = pa.get_device_info_by_index(i)
        name = dev['name'].encode('utf-8')
        print(i, name, dev['maxInputChannels'], dev['maxOutputChannels'])
    print('\ndefault input & output device:')
    print(pa.get_default_input_device_info())
    print(pa.get_default_output_device_info())

main_test();