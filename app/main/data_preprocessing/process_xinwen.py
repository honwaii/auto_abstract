import pandas as pd
import sys
if __name__ == "__main__":
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    # f = open(input_path, encoding="gb18030")
    df = pd.read_csv(input_path, encoding="gb18030")
    output = open(output_path, "w", encoding="utf-8")
    print(df.shape)
    for i in range(df.shape[0]):
        # print(i)
        line = df.ix[i,"content"]
        line = str(line).strip()
        line = line.replace("\n", "")
        line = line.replace("\r", "")
        output.write(line+"\n")
    output.close()
    # f = open(input_path, "r", encoding="gb18030")
    # output = open(output_path, "w", encoding="utf-8")
    # count = 0
    # buff = ""
    # for line in f.readlines():
    #     buff += line
    #     count = count + line.count("\"")
    #     if count == 2:
    #         buff.replace("\n", "")
    #         buff.replace("\r", "")
    #         buff.replace("\"", "")
    #         count = 0
    #         output.write(buff + "\n")
    #         buff = ""
    # output.close()
    # f.close()
