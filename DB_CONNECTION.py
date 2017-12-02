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
        data_pt = collections.namedtuple('data_pt', ('budget', 'fb_likes', 'revenue', 'release', 'runtime'))

        # Query for revenue prediction
        query1 = ("SELECT P_ID, BUDGET, CAST_FACEBOOK_LIKES, REVENUE, RELEASE_YEAR, RUNTIME "
                  "FROM PRODUCTION, MOVIE "
                  "WHERE P_ID = MP_ID AND REVENUE IS NOT NULL AND BUDGET IS NOT NULL AND CAST_FACEBOOK_LIKES IS NOT NULL AND RELEASE_YEAR IS NOT NULL AND RUNTIME IS NOT NULL;")

        query2 = ("SELECT CATEGORY, REVENUE "
                  "FROM GENRE, MOVIE "
                  "WHERE MP_ID = GP_ID AND REVENUE IS NOT NULL; ")

        # Collect data from the first query
        cursor.execute(query1)

        budget = []
        cast_facebook_likes = []
        revenue = []
        release = []
        runtime = []
        for (P_ID, BUDGET, CAST_FACEBOOK_LIKES, REVENUE, RELEASE_YEAR, RUNTIME) in cursor:
            budget.append(BUDGET)
            cast_facebook_likes.append(CAST_FACEBOOK_LIKES)
            revenue.append(REVENUE)
            release.append(RELEASE_YEAR)
            runtime.append(RUNTIME)

        # Collect data from the second query
        cursor.execute(query2)

        genre_revenue = collections.defaultdict(list)
        for (CATEGORY, REVENUE) in cursor:
            genre_revenue[CATEGORY].append(REVENUE)

        return data_pt(budget, cast_facebook_likes, revenue, release, runtime), genre_revenue

    elif in_query == "genre_popularity":
        data_pt = collections.namedtuple('data_pt', ('user_rating', 'fb_likes', 'pts'))
        query = ("SELECT CATEGORY, USER_RATING, FACEBOOK_LIKES, RELEASE_YEAR "
                 "FROM  GENRE, PRODUCTION "
                 "WHERE P_ID = GP_ID; ")

        cursor.execute(query)

        genre_user = collections.defaultdict(list)
        genre_fb = collections.defaultdict(list)
        instances = []
        for (CATEGORY, USER_RATING, FACEBOOK_LIKES, RELEASE_YEAR) in cursor:
            genre_user[CATEGORY].append(float(USER_RATING))
            genre_fb[CATEGORY].append(int(FACEBOOK_LIKES))
            instances.append((CATEGORY, USER_RATING, FACEBOOK_LIKES, RELEASE_YEAR))

        return data_pt(genre_user, genre_fb, instances)

    elif in_query == "predict_rating":
        data_pt = collections.namedtuple('data_pt', ('budget', 'fb_likes', 'runtime', 'release', 'rating'))

        query = ("SELECT BUDGET, CAST_FACEBOOK_LIKES, USER_RATING, RUNTIME, RELEASE_YEAR "
                 "FROM  MOVIE, PRODUCTION "
                 "WHERE P_ID = MP_ID AND BUDGET IS NOT NULL AND CAST_FACEBOOK_LIKES IS NOT NULL AND USER_RATING IS NOT NULL AND RUNTIME IS NOT NULL AND RELEASE_YEAR IS NOT NULL; ")

        cursor.execute(query)

        data = []
        for (BUDGET, CAST_FACEBOOK_LIKES, USER_RATING, RUNTIME, RELEASE_YEAR) in cursor:
            data.append(data_pt(int(BUDGET), int(CAST_FACEBOOK_LIKES), int(RUNTIME), int(RELEASE_YEAR), float(USER_RATING)))

        return data

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
