from faker import Faker
import random

fake = Faker(locale="zh_CN")
MAX_ROW = 10

def generate_random_info():    
    emp = {
        "name": fake.name(),
        "address":fake.address(),
        "phone":fake.phone_number()
    }

    return emp

if __name__ == "__main__":
    with open("fakeemployees.csv", mode="a", encoding="utf8") as f:
        for idx in range(0, MAX_ROW):
            info = generate_random_info()
            line = ",".join([str(idx+1), info.get("name"), info.get("address"), info.get("phone")])
            f.write(line+'\n')
        
