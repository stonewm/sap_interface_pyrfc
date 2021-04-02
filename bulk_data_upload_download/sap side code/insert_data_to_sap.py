from SAP.sap_systems import current_sap_connection

upload_file = "fakeemployees.csv"
batch_count = 1000

def get_data_from_file(batch_max):
    employees = []
    with open(upload_file, mode="r",encoding="utf8") as f:
        batch = 0
        for line in f:
            (id, name, addr, phone) = line.split(sep=",")
            employees.append({
                "MANDT": "001",
                "EMPID": id,
                "EMPNAME": name,
                "EMPADDR": addr,
                "PHONE": phone
            })
            batch += 1

            if batch == batch_max:
                yield employees
                employees =[]
                batch = 0
    if len(employees) > 0:
        yield employees



def insert_employee():
    sap_conn = current_sap_connection()
    for employees in get_data_from_file(batch_count):     
        rv = sap_conn.call("ZEMPLOYEE_INSERT", EMPLOYEES=employees)
        print(rv["RET"])


if __name__ == "__main__":
    insert_employee()
