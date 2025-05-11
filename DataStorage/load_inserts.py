import time
import psycopg2
import argparse
import csv

DBname = "postgres"
DBuser = "postgres"
DBpwd = "616298"  # insert your postgres db password here
TableName = 'censusdata'
Datafile = "filedoesnotexist"  # name of the data file to be loaded
CreateDB = False  # indicates whether the DB table should be (re)-created

def initialize():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--datafile", required=True)
    parser.add_argument("-c", "--createtable", action="store_true")
    args = parser.parse_args()

    global Datafile
    Datafile = args.datafile
    global CreateDB
    CreateDB = args.createtable

# Connect to the database
def dbconnect():
    connection = psycopg2.connect(
        host="localhost",
        database=DBname,
        user=DBuser,
        password=DBpwd,
    )
    connection.autocommit = True
    return connection

# Create the target table
def createTable(conn):
    with conn.cursor() as cursor:
        cursor.execute(f"""
            DROP TABLE IF EXISTS {TableName};
            CREATE TABLE {TableName} (
                TractId NUMERIC,
                State TEXT,
                County TEXT,
                TotalPop INTEGER,
                Men INTEGER,
                Women INTEGER,
                Hispanic DECIMAL,
                White DECIMAL,
                Black DECIMAL,
                Native DECIMAL,
                Asian DECIMAL,
                Pacific DECIMAL,
                VotingAgeCitizen DECIMAL,
                Income DECIMAL,
                IncomeErr DECIMAL,
                IncomePerCap DECIMAL,
                IncomePerCapErr DECIMAL,
                Poverty DECIMAL,
                ChildPoverty DECIMAL,
                Professional DECIMAL,
                Service DECIMAL,
                Office DECIMAL,
                Construction DECIMAL,
                Production DECIMAL,
                Drive DECIMAL,
                Carpool DECIMAL,
                Transit DECIMAL,
                Walk DECIMAL,
                OtherTransp DECIMAL,
                WorkAtHome DECIMAL,
                MeanCommute DECIMAL,
                Employed INTEGER,
                PrivateWork DECIMAL,
                PublicWork DECIMAL,
                SelfEmployed DECIMAL,
                FamilyWork DECIMAL,
                Unemployment DECIMAL
            );
            ALTER TABLE {TableName} ADD PRIMARY KEY (TractId);
            CREATE INDEX idx_{TableName}_State ON {TableName}(State);
        """)

        print(f"Created {TableName}")

# Load data using copy_from() for better performance
def load(conn, fname):
    with conn.cursor() as cursor:
        print(f"Loading data from {fname}")
        start = time.perf_counter()

        with open(fname, 'r') as f:
            # Skip the header row
            next(f)
            cursor.copy_from(f, TableName, sep=',', null='')

        elapsed = time.perf_counter() - start
        print(f'Finished Loading. Elapsed Time: {elapsed:0.4} seconds')

def main():
    initialize()
    conn = dbconnect()

    if CreateDB:
        createTable(conn)

    load(conn, Datafile)  # Use the new load function with copy_from()

if __name__ == "__main__":
    main()

