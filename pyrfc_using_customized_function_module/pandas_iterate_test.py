
import pandas as pd

# data = [
#     {
#         "name": "Stone",
#         "Chinese": 90,
#         "Math": 100
#     },
#     {
#         "name": "Alice",
#         "Chinese": 80,
#         "Math": 88
#     }
# ]

# df = pd.DataFrame(data)

df = pd.read_excel("AS01_data.xlsx", sheet_name="Sheet1")


if __name__ == "__main__":
    # for index, row in df.iterrows():
    #     print(row["name"], row["Chinese"], row["Math"])

    # scores = df.values.tolist()
    # print(scores)
    print(df)


