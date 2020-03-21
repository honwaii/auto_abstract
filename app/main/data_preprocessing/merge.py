import sys

if __name__ == "__main__":
    input_a = sys.argv[1]
    input_b = sys.argv[2]
    output_path = sys.argv[3]
    output = open(output_path, "w", encoding="utf-8")
    for i in range(1, 3):
        input_f = open(sys.argv[i], "r", encoding="utf-8")
        while True:
            line = input_f.readline()
            if line == "":
                break
            line = line.strip()
            if len(line)>0:
                output.write(line +"\n")
        output.flush()
        input_f.close()
    output.close()
