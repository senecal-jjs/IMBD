import mysql.connector
import collections


def retrieve_data(in_query):

    config = {
      'user': 'root',
      'password': 'password',
      'host': 'localhost',
      'database': 'mydb',
      'raise_on_warnings': True,
    }

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    if in_query == "predict_revenue":
        data_pt = collections.namedtuple('data_pt', ('budget', 'fb_likes', 'revenue'))

        # Query for revenue prediction
        query1 = ("SELECT P_ID, BUDGET, CAST_FACEBOOK_LIKES, REVENUE "
                  "FROM PRODUCTION, MOVIE "
                  "WHERE P_ID = MP_ID AND REVENUE IS NOT NULL;")

        query2 = ("SELECT CATEGORY, REVENUE "
                  "FROM GENRE, MOVIE "
                  "WHERE MP_ID = GP_ID AND REVENUE IS NOT NULL; ")

        # Collect data from the first query
        cursor.execute(query1)

        budget = []
        cast_facebook_likes = []
        revenue = []
        for (P_ID, BUDGET, CAST_FACEBOOK_LIKES, REVENUE) in cursor:
            budget.append(BUDGET)
            cast_facebook_likes.append(CAST_FACEBOOK_LIKES)
            revenue.append(REVENUE)

        # Collect data from the second query
        cursor.execute(query2)

        genre_revenue = collections.defaultdict(list)
        for (CATEGORY, REVENUE) in cursor:
            genre_revenue[CATEGORY].append(REVENUE)

        return data_pt(budget, cast_facebook_likes, revenue), genre_revenue

    elif in_query == "genre_popularity":
        data_pt = collections.namedtuple('data_pt', ('user_rating', 'fb_likes'))
        query = ("SELECT CATEGORY, USER_RATING, FACEBOOK_LIKES "
                 "FROM  GENRE, PRODUCTION "
                 "WHERE P_ID = GP_ID; ")

        cursor.execute(query)

        genre_user = collections.defaultdict(list)
        genre_fb = collections.defaultdict(list)
        for (CATEGORY, USER_RATING, FACEBOOK_LIKES) in cursor:
            genre_user[CATEGORY].append(float(USER_RATING))
            genre_fb[CATEGORY].append(int(FACEBOOK_LIKES))

        return data_pt(genre_user, genre_fb)

    elif in_query == "predict_rating":
        data_pt = collections.namedtuple('data_pt', ('budget', 'fb_likes'))

        query = ("SELECT BUDGET, CAST_FACEBOOK_LIKES "
                 "FROM  MOVIE, PRODUCTION "
                 "WHERE P_ID = MP_ID; ")

        cursor.execute(query)

        budget = []
        fb_likes = []
        for (BUDGET, CAST_FACEBOOK_LIKES) in cursor:
            budget.append(BUDGET)
            fb_likes.append(CAST_FACEBOOK_LIKES)

        return data_pt(budget, fb_likes)

    elif in_query == "content_rating":
        data_pt = collections.namedtuple('data_pt', ('budget', 'revenue'))

        query = ("SELECT BUDGET, REVENUE, CONTENT_RATING "
                 "FROM  MOVIE "
                 "WHERE CONTENT_RATING IS NOT NULL; ")

        cursor.execute(query)

        content_budget = collections.defaultdict(list)
        content_revenue = collections.defaultdict(list)
        for (BUDGET, REVENUE, CONTENT_RATING) in cursor:
            content_budget[CONTENT_RATING].append(int(BUDGET))
            content_revenue[CONTENT_RATING].append(int(REVENUE))

        return data_pt(content_budget, content_revenue)

    elif in_query == "runtime_analysis":
        data_pt = collections.namedtuple('data_pt', ('content', 'genre'))

        query = ("SELECT RUNTIME, CATEGORY, CONTENT_RATING "
                 "FROM  MOVIE, PRODUCTION, GENRE "
                 "WHERE P_ID = MP_ID AND MP_ID = GP_ID AND RUNTIME IS NOT NULL; ")

        cursor.execute(query)

        content_runtime = collections.defaultdict(list)
        genre_runtime = collections.defaultdict(list)
        for (RUNTIME, CATEGORY, CONTENT_RATING) in cursor:
            content_runtime[CONTENT_RATING].append(int(RUNTIME))
            genre_runtime[CATEGORY].append(int(RUNTIME))

        return data_pt(content_runtime, genre_runtime)

    cursor.close()
    cnx.close()
