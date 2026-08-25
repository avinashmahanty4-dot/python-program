import sqlite3

def create_database():
    try:
        conn = sqlite3.connect('fantasy.db')
        cursor = conn.cursor()
        
        # 1. Stats Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stats (
                player TEXT PRIMARY KEY,
                matches INTEGER,
                runs INTEGER,
                hundreds INTEGER,
                fifties INTEGER,
                value INTEGER,
                ctg TEXT
            )
        ''')
        
        # 2. Match Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS match (
                player TEXT PRIMARY KEY,
                scored INTEGER,
                faced INTEGER,
                fours INTEGER,
                sixes INTEGER,
                bowled INTEGER,
                maiden INTEGER,
                given INTEGER,
                wkts INTEGER,
                catches INTEGER,
                stumping INTEGER,
                ro INTEGER
            )
        ''')
        
        # 3. Teams Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS teams (
                name TEXT,
                players TEXT,
                value INTEGER
            )
        ''')
        
        # Insert Sample Data safely if table is empty
        cursor.execute("SELECT COUNT(*) FROM stats")
        if cursor.fetchone()[0] == 0:
            sample_stats = [
                ('Virat Kohli', 10, 550, 2, 3, 10, 'BAT'),
                ('Rohit Sharma', 10, 480, 1, 4, 9, 'BAT'),
                ('MS Dhoni', 10, 350, 0, 2, 9, 'WK'),
                ('Jasprit Bumrah', 10, 20, 0, 0, 10, 'BWL'),
                ('Hardik Pandya', 10, 250, 0, 1, 9, 'AR'),
                ('Ravindra Jadeja', 10, 200, 0, 1, 9, 'AR'),
                ('R Ashwin', 10, 80, 0, 0, 8, 'BWL'),
                ('KL Rahul', 10, 400, 1, 2, 8, 'WK'),
                ('Suryakumar Yadav', 10, 420, 1, 3, 9, 'BAT'),
                ('Shami Ahmed', 10, 15, 0, 0, 8, 'BWL'),
                ('Yuzvendra Chahal', 10, 5, 0, 0, 8, 'BWL'),
                ('Shubman Gill', 10, 380, 1, 2, 8, 'BAT')
            ]
            cursor.executemany("INSERT INTO stats VALUES (?,?,?,?,?,?,?)", sample_stats)
            
            # Sample match performance for Score Evaluation
            sample_match = [
                ('Virat Kohli', 102, 80, 8, 2, 0, 0, 0, 0, 1, 0, 0),
                ('Rohit Sharma', 45, 30, 4, 1, 0, 0, 0, 0, 0, 0, 0),
                ('MS Dhoni', 28, 15, 2, 1, 0, 0, 0, 0, 1, 1, 0),
                ('Jasprit Bumrah', 0, 0, 0, 0, 60, 2, 35, 4, 0, 0, 0),
                ('Hardik Pandya', 35, 20, 3, 1, 30, 0, 25, 1, 1, 0, 0),
                ('Ravindra Jadeja', 15, 10, 1, 0, 60, 1, 40, 2, 2, 0, 0),
                ('R Ashwin', 5, 5, 0, 0, 60, 0, 45, 1, 0, 0, 0),
                ('KL Rahul', 62, 50, 5, 0, 0, 0, 0, 0, 0, 0, 1),
                ('Suryakumar Yadav', 85, 40, 6, 4, 0, 0, 0, 0, 1, 0, 0),
                ('Shami Ahmed', 0, 0, 0, 0, 50, 0, 42, 3, 0, 0, 0),
                ('Yuzvendra Chahal', 0, 0, 0, 0, 60, 0, 55, 2, 0, 0, 0),
                ('Shubman Gill', 12, 15, 1, 0, 0, 0, 0, 0, 0, 0, 0)
            ]
            cursor.executemany("INSERT INTO match VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", sample_match)
            
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database Error: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    create_database()