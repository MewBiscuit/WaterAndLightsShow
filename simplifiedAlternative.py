import librosa
import numpy as np


def data_extraction(file_path):
    y, sr = librosa.load(file_path, sr=44100, mono=True, offset=0.0, duration=None)

    for i in range(len(y)):
        y[i] = int(y[i] * 100000)
        y[i] //= 1

    return y


def prepare_data(data, pump_val):
    vector_init = "type hardcodedSong is array(0 to " + str(len(data)-1) + ") of integer;\n" \
                                                                         "variable song : hardcodedSong := ("
    for i in range(len(data)):
        vector_init += str(data[i]) + ", "
        if i % 15 == 0:
            vector_init += "\n"
    vector_init += ");\n\n"

    vector_init += "type hardcodedPump is array(0 to " + str(len(pump_val)-1) + ") of integer;\n" \
                                                                              "variable pump : hardcodedPump := ("
    for i in range(len(pump_val)):
        vector_init += str(pump_val[i]) + ", "
        if i % 15 == 0:
            vector_init += "\n"
    vector_init += ");\n\n"

    return vector_init


def write_data(code):
    f = open("hardcode.vhd", "x")
    f.write(code)
    f.close()
    return 0


def pump_values(data):
    pump_val = []
    for i in range((len(data) // 411)):
        avg = 0
        for j in range(411):
            if data[i * 411 + j] < 0:
                avg += (-1*data[i * 411 + j])
            else:
                avg += data[i * 411 + j]
        avg //= 411
        #Adjust avg to a range from 0 to 255
        avg = (avg * 255) // 100000
        #Make average an integer using numpy
        avg = np.uint(avg)
        pump_val.append(avg)
    return pump_val


def main():
    file_path = "Songpath"
    data = data_extraction(file_path)
    pump = pump_values(data)
    code = prepare_data(data, pump)
    write_data(code)
    return 0


main()
