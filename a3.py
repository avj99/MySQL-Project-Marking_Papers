import sqlite3  
connection = None
cursor= None

def connect(path):
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    return


#Function for the first query
def taskOne():
    global connection, cursor
    print("entered 1")
    # Getting input for the Area
    area = input("Enter the area: ")

    while len(area) < 1:
        print('Error, input is empty')
        area = input("Enter the area: ")

  
        
    # the following returns the titles of accepted papers in a specified area
    # and are ordered occording to their average overall
    cursor.execute('SELECT DISTINCT p.title FROM papers p, reviews r\
         WHERE p.area =:ar AND p.id = r.paper \
        AND p.decision = "A"\
        ORDER BY \
        (SELECT AVG(E.overall)\
        FROM reviews E\
        WHERE P.id = E.paper\
        AND p.decision = "A"\
        GROUP BY paper) DESC', {"ar":area})
    row = cursor.fetchall()
    print(row) # prints the output
    print(" ") # extra line for better displaying
    connection.commit()
    return

#Function for the second query
def taskTwo():
    '''displays the papers aftering entering the email of the reviwer. If the reviwer wasn't assigned a paper to review, then a statement informing that will be displayed '''
    
    global connection, cursor 
    print("entered Task 2") # displays the selected option
    email= input("Email:")#enter email
    cursor.execute("SELECT p.title \
                   FROM papers p, reviews r \
                   WHERE r.reviewer=:emails  AND p.id = r.paper  AND p.id BETWEEN 1 and 10", {"emails": email}) #selects papers that the input email has reviews for 

    paperTitle= (cursor.fetchall())
    
    if len(paperTitle) == 0:
        print("This user is not assigned a paper") #if the input has no papers assigned to review.
    else:
        print(*paperTitle, sep= " , " ) # displays the papers the inputted user has reviewed.

    connection.commit()
    return

    
#Function for the third query
def taskThree():
    print("entered 3")

#Function for the fourth query
def taskFour():
    global connection, cursor 

    print("entered 4")
    print("Enter a range from X to Y")
    X= input("X:")
    X= float(X) 
    assert isinstance(X,float)== True, "X has to be an integer" # makes sure the user enters an integer 
    Y= input("Y:")
    Y=float(Y)
    assert isinstance(Y,float)== True, "Y has to be an integer"# makes sure the user enters an integer 

    assert float(X) and float(Y) > 0, "X and Y have to positive" # makes sure the user enters a positive integer 
    listA=[X,Y]


    print("Searching for reviwers that have reviewed a paper with a difference score between ",X," and ",Y) 


    cursor.execute("DROP VIEW IF EXISTS DiffScore;")
    cursor.execute('''CREATE VIEW Diffscore (PaperID, PaperTitle, Difference)
                                AS SELECT p.id, p.title, abs(AVG(r.overall) - AVG(q.overall))
                                FROM reviews r, papers p,reviews q, papers d
                                WHERE p.id = r.paper
                                AND p.area = d.area
                                AND d.id = q.paper
                                GROUP by p.id, p.title ''') # creates a VIEW with three columns: paper id, paper title, and difference ( for each paper average score , in absolute value, substracted from the average score of all papers in the same area)


    cursor.execute("SELECT r.reviewer, u.name  \
                   FROM Diffscore d, reviews r , users u\
                   WHERE d.PaperId = r.paper  \
                   AND r.reviewer= u.email \
                   AND d.Difference BETWEEN ? and ?;",listA)
  
    connection.commit()
    
    finalTable= (cursor.fetchall())
    print(finalTable)
    return


def main():
    global connection, cursor
    path= "./A3.db"
    connect(path)
    
    
    #to continuously run the program
    while(True):
        print("Task 1: List the titles of accepted papers in a given area")
        print("Task 2: List only the titles of the papers a User was assigned to review.")
        print("Task 3: List the id and title of every paper with at least one inconsistent reviews")
        print("Task 4: Find the email addresses and names of the reviewers that have reviewed a paper with a difference between X (inclusive) and Y (inclusive)")
        print(" ")
        option = input("Which task would you like to perform? (Enter a number or end): ")

        # Determines what function to perform
        if(option == "1"):
            taskOne()
        
        elif(option == "2"):
            taskTwo()
        
        elif(option == "3"):
            taskThree()
        
        elif(option == "4"):
            taskFour()
        
        elif(option == "end"):
            #breaks out of loop to end program
            print("Ending Program")
            break

    connection.commit()
    connection.close()
    return

    
    
if __name__ == '__main__':
    main()