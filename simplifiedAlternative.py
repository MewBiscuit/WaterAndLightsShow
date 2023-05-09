import librosa
import numpy as np


def data_extraction(file_path):
    y, sr = librosa.load(file_path, sr=44100, mono=True, offset=0.0, duration=None, dtype=np.int8,
                         res_type='kaiser_best')
    return y


def prepare_data(data, pump_val):
    vector_init = "type hardcodedSong is array(0 to " + str(len(data)) + ") of integer;\n" \
                                                                         "variable song : hardcodedSong := ("
    for i in range(len(data)):
        vector_init += str(data[i]) + ", "
    vector_init += ");\n\n"

    vector_init += "type hardcodedPump is array(0 to " + str(len(pump_val)) + ") of integer;\n" \
                                                                              "variable pump : hardcodedPump := ("
    for i in range(len(pump_val)):
        vector_init += str(pump_values[i]) + ", "
    vector_init += ");\n\n"

    return vector_init


def write_data(code):
    f = open("hardcodedSong.vhd", "w")
    f.write(code)
    f.close()
    return 0


def pump_values(data):
    pump_val = []
    for i in range((len(data) // 4110)):
        avg = 0
        for j in range(4110):
            avg += data[i * 4110 + j]
        avg //= 4110
        pump_val.append(avg)
    return pump_val


def main():
    file_path = ""
    data = data_extraction(file_path)
    pump = pump_values(data)
    code = prepare_data(data, pump)
    write_data(code)
    return 0


main()
