import sqlite3, time
import twitch, json #Import twitch module to get information on twitch streamers
from datetime import datetime
from datetime import timedelta

twitch_streamers = ["trick2g",   "yassuo", "pokimane", "gmhikaru", "chess", "loltyler1", "itshafu"]

with open("streamers.json") as credentials:
    twitch_cred = json.load(credentials)
    credentials.close()
client = twitch.TwitchHelix(client_id=twitch_cred["client_id"], client_secret=twitch_cred["client_secret"], scopes=[twitch.constants.OAUTH_SCOPE_ANALYTICS_READ_EXTENSIONS])
client.get_oauth()

con= sqlite3.connect("streamer.db")
cur=con.cursor()

comparison_game = {} #Set an empty dictionary for streamers and their games
game_viewers_current_game = {}


tomorrow_date = (datetime.now()+timedelta(days=1)).strftime("%m/%d/%Y")

def streamer_info():
    for streamer in twitch_streamers:
        time.sleep(1)
        place_holder_game = {} #set an empty dicitonary to get the games and add the count value
        streamer_info = client.get_streams(user_logins = streamer) #login to Twitch streaming service
        if len(streamer_info) == 0:
            print(f"{streamer} is offline")
        else:
            print(f"{streamer} is online!")
            from_id = int(streamer_info[0]['user_id'])#Get the ID of the streamer
            streamer_following = client.get_user_follows(from_id = from_id) #Use the ID to get information on the current stream
            count_games= 1 #set the count value to 1
            if len(comparison_game) ==0: #if the comparison_dctionary is empty, it will start adding games
                place_holder_game = {"game name": streamer_info[0]["game_name"], "Play Time": count_games, "started at": (streamer_info[0]["started_at"].strftime("%H:%M:%S"))} #use the place_holder_games dictionary to add the count value and the game
                comparison_game[streamer] = place_holder_game
                game_viewers_current_game[streamer] = {"current game" : streamer_info[0]["game_name"]}
                print("Created Dictionary!")
            else:
                for i in list(comparison_game.keys()): #Compares the dictionary and looks at the keys to see if the user exists in this dictionary, if they do not, they are added into the dictionary
                    if str(i) != streamer:
                        place_holder_game= {"current game" : streamer_info[0]["game_name"], "Play Time": count_games, "started at": (streamer_info[0]["started_at"].strftime("%H:%M:%S"))} #
                        comparison_game[streamer] = place_holder_game
        #The statements below looks into a dictionary called game_viewers_current_game and looks at the streamer and logs what game they are playing
        if len(streamer_info) == 0:
            print("can't compare game")
        else:
            
            for person in list(game_viewers_current_game.keys()):
                if str(person) != streamer: #if the streamer does not exist in the dictionary, then they are added in
                    game_viewers_current_game[streamer] = {"current game" : streamer_info[0]["game_name"]}
                else:
                    #If the streamer does exist, it checks the current game they are playing with the game logged in the dictionary and if they are different, it adds an end time to the previous game
                    if game_viewers_current_game[streamer]["current game"] != streamer_info[0]["game_name"]:
                        endtime(streamer, streamer_info) #This is the end time added into the main dictionary of comparison_game
        print(comparison_game)
def streamer_viewers(): #This definition checks the streamers view count
        for streamer in twitch_streamers:
            time.sleep(1)
            place_holder_game = {} #set an empty dicitonary to get the games and add the count value
            streamer_info = client.get_streams(user_logins = streamer) #login to Twitch streaming service
            print(streamer_info)
            if len(streamer_info) == 0:
                print(f"{streamer} is offline for views")
            else:
                print(f"{streamer} is online for views!")
                from_id = int(streamer_info[0]['user_id'])#Get the ID of the streamer
                streamer_following = client.get_user_follows(from_id = from_id) #Use the ID to get information on the current stream     
                if game_viewers_current_game[streamer] != streamer:#these two statements will go ahead and cehck to see if a viewer count exists for a game. If it doesn't, it adds the viewers into the game. If it does have the viewers, it will compare to see which is greater.
                    comparison_game[streamer]["viewers"] =  streamer_info[0]["viewer_count"]
                elif comparison_game[streamer]["viewers"] <= streamer_info[0]["viewer_count"]:
                            comparison_game[streamer]["viewers"] = streamer_info[0]["viewer_count"]        

def endtime(streamer):
    end_time = (datetime.now()).strftime("%H:%M:%S")
    comparison_game[streamer] = {"ended_at": end_time}
    comparison_game[streamer]["total playtime"] = str(datetime.strptime(comparison_gamne[streamer]["end time"], "%H:%M:%S")-datetime.strptime(comparison_gamne[streamer]["started at"], "%H:%M:%S")).total_seconds()#turns the start time and the end time into seconds to add to database
    games_database(streamer)
    
def games_database(streamer):#adds the comparison_dictionary into the database.
    game_database = con.execute("SELECT EXISTS(SELECT  Games FROM streamers WHERE Games = '{comparison_game['streamer']['current game']})")
    if len((i[0] for i in game_database)) == 0: #This checks to see if the streamer exists in the data base. If it doesn't, it will add the data into SQL database
        for k in comparison_game():
            con.execute(f"INSTERT INTO streamers (Streamer, Games, Number of Times Played, Date, Length Played,  Number of Views) VALUES (?, ?, ?, ?, ?)" ,(k, k["game name"], k["Play Time"], k["viewers"], k,["total playtime"]))
            con.commit()
    else:
            con.execute(f"SELECT Length Played + comparison_game['streamer'][total playtime'] FROM testing WHERE Games = '{comparison_game['streamer']['current game']})'") #This adds the total time if a streamer is playing a game that exists within the database
            con.execute(f"SELECT Number of Times Played + 1 FROM testing WHERE Games = '{comparison_game['streamer']['current game']})'") #this adds the playtime as one each time the above is executed.
            con.commit()
    game_comparison.pop(streamer)
while True: #This runes the functions above.
        today_date = (datetime.today()).strftime('%Y-%m-%d')
        try:
            con.execute("CREATE TABLE streamers (id INTEGER PRIMARY KEY AUTOINCREMENT, Streamer TEXT, Games TEXT, Number of Times Played,Date INTEGER, Length Played INTEGER, Number of Views INTEGER)")#Checks to see if the sql database is created.
            conn.close
            streamer_info()
            streamer_viewers()
            
        except sqlite3.OperationalError:
            print("table already exists")
            streamer_info()
            streamer_viewers()
            print(comparison_game)
            if today_date == tomorrow_date:#if today's date and tomorrows date are the same, this clears the current dictionary and adds the date again for tomorrow
                game_comparison.clear()
                tomorrow_date = (datetime.now()+timedelta(days=1)).strftime("%m/%d/%Y")
