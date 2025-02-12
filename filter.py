import sqlite3


class database:

    def __init__(self):
        # initial sqlite3 configurations
        self.name = "filter.db"
        self.connection = sqlite3.connect(self.name)
        self.cursor = self.connection.cursor()
        self.create_database()

    # create the database, only needs to be run once when the class is initialized 
    def create_database(self):

        # sql table with automatically increasing integer id and BLOCKED url 
        self.cursor.execute("""
                           CREATE TABLE IF NOT EXISTS blocked (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           url TEXT NOT NULL UNIQUE
                           )
                           """)

        # sql table with automatically increasing integer id and FLAGGED url
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS flagged (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            url TEXT NOT NULL UNIQUE
                            )
                            """)

        # sql table with automatically increasing integer id and WHITELISTED url
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS whitelisted (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            url TEXT NOT NULL UNIQUE
                            )
                            """)
        

        # stage the changes 
        self.connection.commit()
        print("Database " + self.name + " created")
    
    # display the entire dataset 
    def display(self):
        try:
            # list of all tables
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = self.cursor.fetchall()

            if not tables:
                print("No tables found in the database.")
                return

            # display each table
            for table in tables:
                table_name = table[0]
                print(f"Table: {table_name}")
                print("-" * 30)

                # get all the rows
                self.cursor.execute(f"SELECT * FROM {table_name};")
                rows = self.cursor.fetchall()

                # get all columns
                self.cursor.execute(f"PRAGMA table_info({table_name});")
                columns = [col[1] for col in self.cursor.fetchall()]

                # print column headers
                print(" | ".join(columns))

            # print rows
                if rows:
                    for row in rows:
                        print(" | ".join(map(str, row)))
                else:
                    print("No data in this table.")

                # add space
                print("\n")  
        except Exception as e:
            print(f"An error occurred: {e}")

    # add preliminary data to the db
    def initial_listed(self):
        # list of blocked websites
        blocked_websites = [
            ('pornhub.com',),
            ('amazon.com',),
            ('khs.kirkwoodschools.org',)
        ]

        # list of flagged websites
        flagged_websites = [
            ('chatgpt.com',),
            ('meta.com',),
            ('wikipedia.org',)
        ]

        # list of whitelisted websites
        whitelisted_websites = [
            ('x.com',),
            ('kaggle.com',),
            ('schoology.com',)
        ]

        control_sites = {
            "blocked": blocked_websites,
            "flagged": flagged_websites,
            "whitelisted": whitelisted_websites,
        }

        # add each of the urls to the corresponding tables
        for table, urls in control_sites.items():
            sql = "INSERT OR IGNORE INTO " + table + " (url) VALUES (?)"
            for url in urls:
                # this is cuz of the format of the tuples, could also do just one tuple and insert that
                self.cursor.execute(sql, url)  

        # commit changes
        self.connection.commit()
        print("Initial lists of websites added.")


    # add a website to the blocked list, notice how it says condemmed lol
    def add_blocked(self, condemned):
        sql = "INSERT OR IGNORE INTO blocked (url) VALUES ("+condemned+")"
        self.cursor.execute(sql)

        self.connection.commit()
        print("Blocked " + condemned)

    # add a website to the flagged list
    def add_flagged(self, purgatory):
        sql = "INSERT OR IGNORE INTO flagged (url) VALUES ("+purgatory+")"
        self.cursor.execute(sql)

        self.connection.commit()
        print("Flagged " + purgatory)

    # add a website to the whitelisted list (heaven)
    def add_whitelisted(self, saved):
        sql = "INSERT OR IGNORE INTO whitelisted (url) VALUES ("+saved+")"
        self.cursor.execute(sql)

        self.connection.commit()
        print("Whitelisted " + saved)

    # check from all of the lists 
    def check_lists(self, url):

        # check all of the tables
        tables = ["blocked", "flagged", "whitelisted"]
        for table in tables:

            # sql command to find the url from the table
            sql = "SELECT url FROM " +table+ " WHERE url ='"+url+"'"
            result = self.cursor.execute(sql)
            # use fetchone to get one result
            if result.fetchone() is not None:
                print(url + " found in " + table)
                # output the table name
                return table
        # if not found in a table, return not found in database 
        print("URL not found in database")
        return url + " not found in database"
    
    # open a new connection
    def open_connection(self):
        self.connection = sqlite3.connect(self.name)
        self.cursor = self.connection.cursor()

    # close the connection, has to be run everytime we use a function from this class, and when it is initialized
    def close_connection(self):
        self.connection.close()
        print("Connection closed")

        
print("sldkfjasdlfk")
# initialize, only needs to be run once        
db = database()
# db.initial_listed()
db.display()
# db.close_connection()


def ImmediateFilter(webpage):
    db.open_connection()
    db.check_lists(webpage)
    db.close_connection()

ImmediateFilter("chatgpt.com")