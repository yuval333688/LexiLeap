# Database_Manager.py
import psycopg2
from psycopg2 import OperationalError

class DatabaseManager:
    conn = None

    @staticmethod
    def init():
        DatabaseManager.connect()
        #DatabaseManager.ensure_schema_and_seed()

    @staticmethod
    def connect():
        if DatabaseManager.conn is not None:
            return
        try:
            DatabaseManager.conn = psycopg2.connect(
                host="aws-1-eu-north-1.pooler.supabase.com",
                port=5432,
                dbname="postgres",
                user="postgres.lyjhhxkhhnbidfzdtviv",
                password="A$B@*bXtxEKgQT4",
                sslmode="require",
            )
            DatabaseManager.conn.autocommit = False
            print("✅ Connected to database")
        except OperationalError as e:
            print(f"❌ DB connection error: {e}")
            raise

    @staticmethod
    def ensure_schema_and_seed():
        with DatabaseManager.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS public.lessons (
                    id     SERIAL PRIMARY KEY,
                    score  INT     NOT NULL DEFAULT 0,
                    locked BOOLEAN NOT NULL DEFAULT TRUE
                );
            """)
            # אם הטבלה ריקה – נאתחל 7 רשומות כמו בדוגמה שלך
            cur.execute("SELECT COUNT(*) FROM public.lessons;")
            count = cur.fetchone()[0]
            if count == 0:
                # שורה 1: score=80, locked=false; שורה 2: 0,false; היתר: 0,true
                cur.execute("""
                    INSERT INTO public.lessons (score, locked) VALUES
                    (80, FALSE),
                    (0,  FALSE),
                    (0,  TRUE),
                    (0,  TRUE),
                    (0,  TRUE),
                    (0,  TRUE),
                    (0,  TRUE);
                """)
        DatabaseManager.conn.commit()

    @staticmethod
    def get_lessons():
        if DatabaseManager.conn is None:
            DatabaseManager.init()
        with DatabaseManager.conn.cursor() as cur:
            cur.execute("SELECT id, score, locked FROM public.lessons ORDER BY id ASC;")
            rows = cur.fetchall()
        return [{"id": r[0], "score": r[1], "locked": r[2]} for r in rows]

    @staticmethod
    def update_lesson(id: int, score: int) -> bool:
        if DatabaseManager.conn is None:
            DatabaseManager.init()
        try:
            with DatabaseManager.conn.cursor() as cur:
                # read current score
                cur.execute("SELECT score FROM public.lessons WHERE id = %s;", (id,))
                row = cur.fetchone()
                if row is None:
                    print(f"❌ Lesson {id} not found.")
                    return False
                current_score = row[0] or 0

                # update only if higher
                if score <= current_score:
                    print(f"ℹ️ No update. New {score} <= current {current_score}.")
                    return False

                cur.execute("UPDATE public.lessons SET score = %s WHERE id = %s;", (score, id))
                if score >= 60:
                    # unlock next lesson (safe even if it doesn't exist)
                    cur.execute("UPDATE public.lessons SET locked = false WHERE id = %s;", (id + 1,))

            DatabaseManager.conn.commit()
            print(f"✅ Lesson {id} updated {current_score} → {score}" + (" and next unlocked" if score >= 60 else ""))
            return True
        except Exception as e:
            DatabaseManager.conn.rollback()
            print(f"❌ Update failed: {e}")
            return False
