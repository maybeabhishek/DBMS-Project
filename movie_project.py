import sqlite3
from prettytable import PrettyTable

from recommendation_system import show_predictions

# db = sqlite3.connect('movie_data.db')
# cursor = db.cursor()
# cursor.execute('''DELETE from movies;''')
#
# db.commit()
# cursor.execute('''SELECT * from movies;''')
# db.execute('''CREATE TABLE movies
#          (ID INT PRIMARY KEY  NOT NULL,
#          MOVIE_NAME TEXT NOT NULL,
#          MOVIE_RATING INT NOT NULL);''')
#
# db.execute('''CREATE TABLE projections
#          (ID INT PRIMARY KEY NOT NULL,
#          MOVIE_ID INT REFERENCES movies(id),
#          PROJECTIONS_TYPE TEXT NOT NULL,
#          PROJECTIONS_DATE  DATE NOT NULL,
#          PROJECTION_TIME TEXT NOT NULL );''')
#
# db.execute('''CREATE TABLE reservations
#          (ID INT PRIMARY KEY NOT NULL,
#          USERNAME TEXT NOT NULL,
#          PROJECTION_ID INT REFERENCES projections(ID),
#          ROW  INT NOT NULL,
#          COLUMN INT NOT NULL );''')





# db.commit()

# cursor = db.execute("select * from reservations")
# for row in cursor:
#     print("id = ", row[0])
#     print("username= ", row[1])
#     print("proj_id = ", row[0])
#     print("row = ", row[1])
#     print("col = ", row[2], "\n")
# INSERT INTO "SYSTEM"."PROJECTIONS" ("ID", "MOVIE_ID", "TYPE", "MOVIEDATE", "TIME") VALUES (9, 6, '3d', TO_DATE('2018-10-12 06:20:13', 'YYYY-MM-DD HH24:MI:SS'), '1000')
# INSERT INTO "SYSTEM"."PROJECTIONS" ("ID", "MOVIE_ID", "TYPE", "MOVIEDATE", "TIME") VALUES (10, 7, '2d', TO_DATE('2018-10-12 06:20:13', 'YYYY-MM-DD HH24:MI:SS'), '0800')
# INSERT INTO "SYSTEM"."PROJECTIONS" ("ID", "MOVIE_ID", "TYPE", "MOVIEDATE", "TIME") VALUES (11, 8, '2d', TO_DATE('2018-10-12 06:20:13', 'YYYY-MM-DD HH24:MI:SS'), '1200')
# INSERT INTO "SYSTEM"."PROJECTIONS" ("ID", "MOVIE_ID", "TYPE", "MOVIEDATE", "TIME") VALUES (12, 8, '3d', TO_DATE('2018-10-12 06:20:13', 'YYYY-MM-DD HH24:MI:SS'), '0900')
# INSERT INTO "SYSTEM"."PROJECTIONS" ("ID", "MOVIE_ID", "TYPE", "MOVIEDATE", "TIME") VALUES (13, 9, '3d', TO_DATE('2018-10-12 06:20:13', 'YYYY-MM-DD HH24:MI:SS'), '1900')
# INSERT INTO "SYSTEM"."PROJECTIONS" ("ID", "MOVIE_ID", "TYPE", "MOVIEDATE", "TIME") VALUES (14, 10, '2d', TO_DATE('2018-10-12 06:20:13', 'YYYY-MM-DD HH24:MI:SS'), '2100')
# INSERT INTO "SYSTEM"."PROJECTIONS" ("ID", "MOVIE_ID", "TYPE", "MOVIEDATE", "TIME") VALUES (15, 11, '3d', TO_DATE('2018-10-12 06:20:13', 'YYYY-MM-DD HH24:MI:SS'), '2200')
# INSERT INTO "SYSTEM"."PROJECTIONS" ("ID", "MOVIE_ID", "TYPE", "MOVIEDATE", "TIME") VALUES (16, 12, '2d', TO_DATE('2018-10-12 06:20:13', 'YYYY-MM-DD HH24:MI:SS'), '1000')
# INSERT INTO "SYSTEM"."PROJECTIONS" ("ID", "MOVIE_ID", "TYPE", "MOVIEDATE", "TIME") VALUES (17, 13, '2d', TO_DATE('2018-10-12 06:20:13', 'YYYY-MM-DD HH24:MI:SS'), '0800')
# INSERT INTO "SYSTEM"."PROJECTIONS" ("ID", "MOVIE_ID", "TYPE", "MOVIEDATE", "TIME") VALUES (18, 13, '3d', TO_DATE('2018-10-12 06:20:13', 'YYYY-MM-DD HH24:MI:SS'), '1200')
# INSERT INTO "SYSTEM"."PROJECTIONS" ("ID", "MOVIE_ID", "TYPE", "MOVIEDATE", "TIME") VALUES (19, 14, '3d', TO_DATE('2018-10-12 06:20:13', 'YYYY-MM-DD HH24:MI:SS'), '0900')
# INSERT INTO "SYSTEM"."PROJECTIONS" ("ID", "MOVIE_ID", "TYPE", "MOVIEDATE", "TIME") VALUES (20, 14, '3d', TO_DATE('2018-10-12 06:20:13', 'YYYY-MM-DD HH24:MI:SS'), '1900')

# db.close()
ticketPrice = 140


class DBCommunicator:

    def __init__(self, cursor,db):
        self.cursor = cursor
        self.db = db
    def get_movies(self):
        return self.cursor.execute('''SELECT id, movie_name, movie_rating
                                        FROM Movies
                                        ORDER BY movie_rating DESC''')

    def get_projections(self, movie_id):
        return self.cursor.execute('''SELECT Projections.id, projection_type, projection_time,
                                         projection_date, movie_id, movie_name
                                    FROM Projections
                                    JOIN Movies
                                    ON Projections.movie_id = Movies.id
                                    WHERE movie_id = ?
                                    ORDER BY projection_date''', (str(movie_id),));

    def get_projections_with_date(self, movie_id, date):
        return self.cursor.execute('''SELECT Projections.id, projection_type, projection_time,
                                             projection_date, movie_id, movie_name
                                      FROM Projections
                                      JOIN Movies
                                      ON Projections.movie_id = Movies.id
                                      WHERE movie_id = ? AND projection_date = ?
                                      ORDER BY projection_date''', (str(movie_id), str(date)))

    def get_revervations_for_projection(self, projection_id):
        return self.cursor.execute('''SELECT row, col
                                          FROM Reservations 
                                          WHERE projection_id = ?''', (projection_id,))

    def final_reservation(self, user, proj_id, row, col):
        self.cursor.execute('''INSERT INTO Reservations(
                                  username, projection_id, row, col) VALUES(?,?,?,?)''', (user, proj_id, row, col))
        self.db.commit()

    def get_movieName(self,movie_id):
        return self.cursor.execute('''SELECT movie_name from movies where id = ?''',(movie_id,))


class Controller:

    def __init__(self, db_communicator):
        self.db_communicator = db_communicator

    def generate_movies_table(self):
        table = PrettyTable(["id", "movie_name", "movie_rating"])
        for row in self.db_communicator.get_movies():
            table.add_row([row["id"], row["movie_name"], row["movie_rating"]])

        return table

    def create_cinema(self, projection_id):
        rows = 10
        cols = 10
        db_data = self.db_communicator.get_revervations_for_projection(projection_id)
        cinema = []

        row_headers = [" " if x == 0 else x for x in range(rows + 1)]
        cinema.append(row_headers)

        for row in range(rows):
            cinema.append([str(row + 1) if col == 0 else "." for col in range(cols + 1)])

        for row in db_data:
            cinema[row["row"]][row["col"]] = "X"

        return cinema

    def generate_projections_table(self, movie_id, date):
        if date is not None:
            db_result = self.db_communicator.get_projections_with_date(movie_id, date)
        else:
            db_result = self.db_communicator.get_projections(movie_id)

        table = PrettyTable(["projection_id", "projection_type", "projection_time",
                             "projection_date", "movie_id", "movie_name"])

        for row in db_result:
            table.add_row([row["id"], row["projection_type"], row["projection_time"],
                           row["projection_date"], row["movie_id"],
                           row["movie_name"]])

        return table

    def generate_reservations_table(self, data):
        table = PrettyTable(data[0])
        for row in data[1:]:
            table.add_row(row)

        return table

    def fin_reservation(self, user, projection_id, row, col):
        self.db_communicator.final_reservation(user,projection_id, row, col)

    def recommend_movies(self,movie_id):
        movie_name = self.db_communicator.get_movieName(movie_id)
        for row in movie_name:
            show_predictions(row["movie_name"])
        # show_predictions(movie_name)


class CLI:

    def __init__(self, controller):
        self.controller = controller

        self.__user_is_active = True
        self.commands = {
            "1": self.show_movies,
            "2": self.show_projections,
            "3": self.make_reservations,
            "exit": self.exit
        }

    def show_movies(self, *args):
        print(self.controller.generate_movies_table())

    def show_projections(self, *args):
        movie_id = args[0]
        date = None
        if len(args) > 1:
            date = args[1]
        print(self.controller.generate_projections_table(movie_id, date))

    def show_reservations(self, data):
        print(self.controller.generate_reservations_table(data))

    def make_reservations(self, *args):
        username = input("Enter your name: ")
        number_of_tickets = int(input("Enter number of tickets: "))
        self.show_movies()
        movie_id = int(input("Enter movie id: "))
        self.show_projections(movie_id)
        projection_id = int(input("Enter projection id: "))
        self.show_reservations(self.controller.create_cinema(projection_id))
        # ask for ticket seats

        for i in range(number_of_tickets):
            ticketR = int(input("Enter Row: "))
            ticketC = int(input("Enter Column: "))
            self.controller.fin_reservation(username, projection_id, ticketR, ticketC)
            print("The ticket is booked\n")

        print("Your total fare is: ")
        print(number_of_tickets*ticketPrice)
        print('\n')

        self.controller.recommend_movies(movie_id)
        # if finalize
        # insert query

    def exit(self, *args):
        self.__user_is_active = False

    def start(self):
        print("Hello!")
        print("Use the following commands to book a movie\n")
        print("1. show_movies")
        print("2. show_projections")
        print("3. make_reservations")
        print("exit\n\n")
        while self.__user_is_active:
            command = ""
            parameter1 = None
            parameter2 = None

            user_input = input("Enter command: ")
            user_input = user_input.split()
            command = user_input[0]
            if len(user_input) > 1:
                parameter1 = user_input[1]
                if len(user_input) > 2:
                    parameter2 = user_input[2]

            self.commands[command](parameter1, parameter2)


class Validator:
    def __init__(self):
        pass

    def validate_ticket(self):
        raise Exception("DA")


def main():
    db = sqlite3.connect("database.db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    
    db_communicator = DBCommunicator(cursor,db)
    controller = Controller(db_communicator)

    cli = CLI(controller)
    cli.start()


if __name__ == '__main__':
    main()