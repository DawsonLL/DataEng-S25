import time
import psycopg2
import argparse
import csv
from io import StringIO

DBname = "postgres"
DBuser = "postgres"
DBpwd = "616298"
TableName = 'censusdata'
Datafile = "filedoesnotexist"
CreateDB = False

def initialize():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--datafile", required=True)
    parser.add_argument("-c", "--createtable", action="store_true")
    args = parser.parse_args()
    global Datafile, CreateDB
    Datafile = args.datafile
    CreateDB = args.createtable

def dbconnect():
    connection = psycopg2.connect(
        host="localhost",
        database=DBname,
        user=DBuser,
        password=DBpwd,
    )
    connection.autocommit = True
    return connection

def createTable(conn):
    with conn.cursor() as cursor:
        cursor.execute(f"""
            DROP TABLE IF EXISTS {TableName};
            CREATE TABLE {TableName} (
                TractId             NUMERIC,
                State               TEXT,
                County              TEXT,
                TotalPop            INTEGER,
                Men                 INTEGER,
                Women               INTEGER,
                Hispanic            DECIMAL,
                White               DECIMAL,
                Black               DECIMAL,
                Native              DECIMAL,
                Asian               DECIMAL,
                Pacific             DECIMAL,
                VotingAgeCitizen    DECIMAL,
                Income              DECIMAL,
                IncomeErr           DECIMAL,
                IncomePerCap        DECIMAL,
                IncomePerCapErr     DECIMAL,
                Poverty             DECIMAL,
                ChildPoverty        DECIMAL,
                Professional        DECIMAL,
                Service             DECIMAL,
                Office              DECIMAL,
                Construction        DECIMAL,
                Production          DECIMAL,
                Drive               DECIMAL,
                Carpool             DECIMAL,
                Transit             DECIMAL,
                Walk                DECIMAL,
                OtherTransp         DECIMAL,
                WorkAtHome          DECIMAL,
                MeanCommute         DECIMAL,
                Employed            INTEGER,
                PrivateWork         DECIMAL,
                PublicWork          DECIMAL,
                SelfEmployed        DECIMAL,
                FamilyWork          DECIMAL,
                Unemployment        DECIMAL
            );
        """)
        print(f"Created table {TableName} (without constraints/indexes)")

def addConstraintsAndIndexes(conn):
    with conn.cursor() as cursor:
        cursor.execute(f"""
            ALTER TABLE {TableName} ADD PRIMARY KEY (TractId);
            CREATE INDEX idx_{TableName}_State ON {TableName}(State);
        """)
        print(f"Added PRIMARY KEY and index to {TableName}")

def clean_row(row):
    for key in row:
        if not row[key]:
            row[key] = '0'
    row['County'] = row['County'].replace("'", "")
    return row

def copy_data(conn, datafile):
    with open(datafile, 'r') as f:
        reader = csv.DictReader(f)
        output = StringIO()
        for row in reader:
            row = clean_row(row)
            vals = [row[key] for key in reader.fieldnames]
            output.write('\t'.join(vals) + '\n')
        output.seek(0)

        with conn.cursor() as cursor:
            start = time.perf_counter()
            cursor.copy_from(output, TableName, sep='\t', null='')
            elapsed = time.perf_counter() - start
            print(f'Loaded data with COPY in {elapsed:0.4f} seconds')

def main():
    initialize()
    conn = dbconnect()

    if CreateDB:
        createTable(conn)

    copy_data(conn, Datafile)

    if CreateDB:
        addConstraintsAndIndexes(conn)

if __name__ == "__main__":
    main()

