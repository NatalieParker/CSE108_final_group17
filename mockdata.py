# ONLY RUN ONCE IF NEEDED, CREATES DATA FOR DATABASE

import csv
import random
from app import app
from data_structure import db, Show, Episode, User, Watched, Review

CSV_PATH = "netflix_titles.csv"

def seed_database():
  with app.app_context():
    db.drop_all()
    db.create_all()

    shows = []

    with open(CSV_PATH, newline="", encoding="utf-8") as csvfile:
      reader = csv.DictReader(csvfile)

      showCount = 0
      maxShows = 100
      for row in reader:
        if row["type"] != "TV Show":
          continue

        if showCount >= maxShows:
          break

        show = Show(
          title=row["title"],
          director=row["director"] or None,
          cast=row["cast"] or None,
          release_year=int(row["release_year"]) if row["release_year"] else None,
          rating=row["rating"] or None,
          seasons=row["duration"] or None,
          genres=row["listed_in"] or None,
          description=row["description"] or None
        )

        db.session.add(show)
        shows.append(show)
        showCount += 1

    db.session.commit()
    print(f"Imported {len(shows)} TV shows")

    episodes = []

    for show in shows:
        for i in range(1, 11):
            ep = Episode(
                show_id=show.id,
                episode_number=i
            )
            db.session.add(ep)
            episodes.append(ep)

    db.session.commit()
    print(f"Created {len(episodes)} episodes")

    users = []

    usernames = ["alice", "bob", "charlie", "diana"]

    for name in usernames:
      user = User(
        username=name,
        password="password"
      )
      db.session.add(user)
      users.append(user)

    admin = User(
      username = "admin",
      password = "admin123",
      is_admin = 1
    )
    db.session.add(admin)
    users.append(admin)

    db.session.commit()
    print(f"Created {len(users)} users")

    watched_entries = 0

    for user in users:
      watched_eps = random.sample(episodes, 15)

      for ep in watched_eps:
        watch = Watched(
          user_id=user.id,
          episode_id=ep.id
        )
        db.session.add(watch)
        watched_entries += 1

    db.session.commit()
    print(f"Created {watched_entries} watch log entries")

    review_count = 0

    reviewed_shows = random.sample(shows, 10)

    for show in reviewed_shows:
      reviewer = random.choice(users)
      review = Review(
        user_id=reviewer.id,
        show_id=show.id,
        rating=random.randint(1, 5),
        review_text="Really enjoyed this show!"
      )
      db.session.add(review)
      review_count += 1

    db.session.commit()
    print(f"Created {review_count} reviews")

    add_cover_images()

    print("Database seeding complete!")


def add_cover_images():
  with app.app_context():

    # All TV show cover images
    cover_images = {
      "Angry Birds": "https://m.media-amazon.com/images/M/MV5BMTY3MjU0NDA0OF5BMl5BanBnXkFtZTgwNTc0MTU3OTE@._V1_FMjpg_UX1000_.jpg",
      "Bangkok Breaking": "https://m.media-amazon.com/images/M/MV5BZjdkODlhMTgtNGEzNi00YjdiLTk4ZjEtNjc4MjdkYTllYTExXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
      "Blood & Water": "https://m.media-amazon.com/images/M/MV5BYjUxN2E2MWYtYTFiNi00YmJiLTkzOGMtNGRhYmI3ZGM4ZmQ0XkEyXkFqcGc@._V1_.jpg",
      "Brand New Cherry Flavor": "https://m.media-amazon.com/images/M/MV5BNDZjNTJmMmEtZjYwOS00MTYzLTgwYTYtYWJiMDkxNDMzMDAyXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
      "Brave Animated Series": "https://m.media-amazon.com/images/M/MV5BMDlmNGNiNWMtNWNmYi00MGQ5LThkZDctMjQzMDE0N2IxNWQ2XkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
      "Bread Barbershop": "https://m.media-amazon.com/images/M/MV5BYzIyMmQzNzQtOWI1MC00MjQ0LWE2MjctNDE5MzA0MzFjNmI5XkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
      "Bunk'd": "https://m.media-amazon.com/images/M/MV5BYWEwZWZmMGItYjAzZi00ODFiLTk1YWQtNTVkMDNmYWY5MDg5XkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
      "Castle and Castle": "https://m.media-amazon.com/images/M/MV5BM2VkNDAwZTAtMWRmYi00NWE0LTg2ZWMtNjZhOGVjZTUxOGUwXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
      "Chhota Bheem": "https://m.media-amazon.com/images/M/MV5BZDgzZWJmYWUtNTA2NC00MDNkLWIxZjUtMGMzNjAzMGI4NGJkXkEyXkFqcGc@._V1_.jpg",
      "Chicago Party Aunt": "https://m.media-amazon.com/images/M/MV5BYzUyODk0YTQtZDliYy00NTI2LWJhMjEtZDJhM2M4MmZkNWY1XkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
      "Clickbait": "https://m.media-amazon.com/images/M/MV5BZmVhMjY0YmYtMTk0YS00NzU2LTg3MTEtOWZlZjAxNDBlOTM2XkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
      "Comedy Premium League": "https://image.tmdb.org/t/p/original/tnRQIeZGWParKSNCkKi1tcncwnY.jpg",
      "Countdown: Inspiration4 Mission to Space": "https://m.media-amazon.com/images/M/MV5BYWZlMjEwNTQtNDc5NC00ZGVkLWFjNmMtNWI4ZWY4YTdjZGZiXkEyXkFqcGc@._V1_.jpg",
      "Crime Stories: India Detectives": "https://m.media-amazon.com/images/M/MV5BMjYwYjM0M2QtZjRmMC00OWI1LWFmY2EtNjQzOTIxODFjYmQ2XkEyXkFqcGc@._V1_QL75_UY281_CR46,0,190,281_.jpg",
      "D.P.": "https://m.media-amazon.com/images/M/MV5BYzcyYmNjYmUtYzYzMy00ODJjLWI1MmUtY2Y3MmMyMzgwZTM3XkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
      "Deadly Sins": "https://m.media-amazon.com/images/M/MV5BZGM2MTY5NTYtYjlkYi00NTIyLTk1M2QtN2MzN2RmZTQ2M2E1XkEyXkFqcGc@._V1_.jpg",
      "Dear White People": "https://m.media-amazon.com/images/M/MV5BMjMzMjc5MjIzNV5BMl5BanBnXkFtZTgwNTY4OTQ2MjE@._V1_FMjpg_UX1000_.jpg",
      "Dharmakshetra": "https://m.media-amazon.com/images/M/MV5BMDUwZjNlOTItZTA4ZS00ZDI4LTgxMDEtZmQ3ZWQxYjQ5ZjJiXkEyXkFqcGc@._V1_.jpg",
      "Dive Club": "https://m.media-amazon.com/images/M/MV5BYmFlYTlkZDEtNTMzMS00ZWUwLTgyZGEtNzE2ODUyMjY5Njg5XkEyXkFqcGc@._V1_.jpg",
      "EDENS ZERO": "https://m.media-amazon.com/images/M/MV5BMjhlYWVlN2ItZDg3Yy00NGYxLWJkODYtMjFjZTE1YzVlYjdjXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
      "Everything Will Be Fine": "https://m.media-amazon.com/images/M/MV5BNzQ2OTg1MTYwOF5BMl5BanBnXkFtZTgwMTY3MDA2NjE@._V1_.jpg",
      "Falsa identidad": "https://m.media-amazon.com/images/M/MV5BNGFmODBkODAtMGUyMy00YTIzLTgxYWUtYjkyNjFjZWFlMjNiXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
      "Family Reunion": "https://m.media-amazon.com/images/M/MV5BNmVhZDU2ZjEtZDMzOS00ZmYxLTg5ODYtZWFhZmUyNmIxNDdkXkEyXkFqcGc@._V1_.jpg",
      "Fast & Furious Spy Racers": "https://m.media-amazon.com/images/M/MV5BMzdmNzZjYWQtNzYyNi00YTNlLWEyMzgtMDI2NjcyMDRkYmE5XkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
      "Ganglands": "https://m.media-amazon.com/images/M/MV5BYWJkOWM3NDQtYmQ0Mi00MzliLTg4YzctNDk2ZjY4NDQwYTRmXkEyXkFqcGc@._V1_.jpg",
      "Go! Go! Cory Carson": "https://m.media-amazon.com/images/M/MV5BZjQxMTQ3M2ItZTNiOS00OGVmLWE5NDUtNmQ4MmVjNTllNDcyXkEyXkFqcGc@._V1_.jpg",
      "Gone for Good": "https://upload.wikimedia.org/wikipedia/en/thumb/c/c5/Gone_for_Good_%28TV_series%29.jpg/250px-Gone_for_Good_%28TV_series%29.jpg",
      "Grace and Frankie": "https://m.media-amazon.com/images/M/MV5BNjgwMTg2NTAzOV5BMl5BanBnXkFtZTgwOTc0MTI1NTE@._V1_FMjpg_UX1000_.jpg",
      "HQ Barbers": "https://m.media-amazon.com/images/I/51tZRectDiL._AC_UF894,1000_QL80_.jpg",
      "He-Man and the Masters of the Universe": "https://m.media-amazon.com/images/M/MV5BOGM4ZDMxMjMtMmFhYi00OGJhLThiYzktMTVmYTgwNTk4ZDJhXkEyXkFqcGc@._V1_.jpg",
      "Heroes of Goo Jit Zu": "https://m.media-amazon.com/images/M/MV5BZDk0YjJkM2EtODY1Ni00MzZmLThmYzEtOGNjOGI2YWFlZTkzXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
      "Hometown Cha-Cha-Cha": "https://upload.wikimedia.org/wikipedia/en/3/3e/Hometown_Cha-Cha-Cha.jpg",
      "Hotel Del Luna": "https://m.media-amazon.com/images/M/MV5BZmFmYTU0YTItZTk4ZS00ZWMzLThmOTgtOGIyOTBkY2QwZjc0XkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
      "How to Be a Cowboy": "https://m.media-amazon.com/images/M/MV5BNzViNTYwZDQtYzI1YS00YjdhLWI3YjktNTdmZWZjMjAxYzAzXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
      "I Heart Arlo": "https://m.media-amazon.com/images/M/MV5BZTg4MDRiMTktOWYyZS00YTIwLTg5ODItYWFmNGExZTg1NWEzXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
      "Into the Night": "https://m.media-amazon.com/images/M/MV5BZmNiMTNmZDUtYzk3YS00OWNjLTkwNjEtMzI0YWJjYzFmY2I5XkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
      "Jack Whitehall: Travels with My Father": "https://m.media-amazon.com/images/M/MV5BNzYwNzgwNDk2M15BMl5BanBnXkFtZTgwNzIyNTIzNjM@._V1_FMjpg_UX1000_.jpg",
      "Jaguar": "https://m.media-amazon.com/images/M/MV5BYzkxNTgwNjktODhjMi00Mzc1LWJkYzAtYzgzYjFmZmVkNzg0XkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
      "Jailbirds New Orleans": "https://m.media-amazon.com/images/M/MV5BNTI0OGJjMGItZjNmMC00NWQ5LTk5M2QtNjIwZmI3ZGE1OWYzXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
      "John of God: The Crimes of a Spiritual Healer": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR9tqJoUL6FNuqWzJbIkuVc9IYnnKpFneBtLw&s",
      "Kid Cosmic": "https://m.media-amazon.com/images/M/MV5BYTgzZGIwYjEtMzZhOC00ZTJhLWFhYWQtNTU3MTM4MDRiZjZiXkEyXkFqcGc@._V1_.jpg",
      "Kid-E-Cats": "https://m.media-amazon.com/images/M/MV5BYTU3MGQ0NGUtZDUxYi00NzZjLTkwN2MtY2ViYWM4ZWYzYjQwXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
      "King of Boys: The Return of the King": "https://m.media-amazon.com/images/M/MV5BMTY5MjBiZTItNDY3NC00OTVhLThkMDUtZTgyNjI4MDgyNWY5XkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
      "Korean Cold Noodle Rhapsody": "https://m.media-amazon.com/images/M/MV5BOWM4YWJhZjMtNWEwMS00ZmY4LWJiOGEtNzgxYzFlYmFiZDI4XkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
      "Kota Factory": "https://m.media-amazon.com/images/M/MV5BY2U5MjY1NWEtZDI2MS00NTlhLWEyODQtYzE0MzY3NDUyNzE3XkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
      "Kuroko's Basketball": "https://m.media-amazon.com/images/M/MV5BMWM5M2NkNDctZmZmYy00ZmM2LWEzNDEtZWUzMjM5ZmFhOTFiXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
      "La casa de papel": "https://lh3.googleusercontent.com/proxy/3l7sfchuzPcDVV4ubyBM2QIzjXiff6NmGWB_LY5dkssmRLVJC1Z9VaBcYd11fRKxCaQEjaCltfpttxZgPq2PIli1qmcfMwU5kjhegI2GQH7Nak48zHQDVnXA",
      "Love on the Spectrum": "https://m.media-amazon.com/images/M/MV5BYmU3NTE2MzMtNTQ4OC00MjE1LWFiYjAtYjc5OTBjNmQyY2FjXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
      "Lucifer": "https://m.media-amazon.com/images/M/MV5BMGY4MzhkY2ItNWViMi00YTQ1LTg4ODAtMTEyNWM5ZjFkYjU1XkEyXkFqcGc@._V1_.jpg",
      "Luv Kushh": "https://m.media-amazon.com/images/M/MV5BNmM2YWRmMDktZjJjNS00ZmIxLWI4MzktYmYyNGE0MGQ4MWM5XkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
      "Major Dad": "https://m.media-amazon.com/images/M/MV5BNjM5OWVkNWQtMjYzNy00NWE0LWEyOTUtZTRhMjkwMDk2OWI5XkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
      "Manifest": "https://m.media-amazon.com/images/M/MV5BMTFlNjg0YjAtYzMwOC00Zjc0LTkwYjAtZmRiYzdjNjcyYjc2XkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
      "Metal Shop Masters": "https://m.media-amazon.com/images/M/MV5BNzdiOTYyYWQtMmE3ZS00MDg2LWE1MTAtZmE3ODNlNjIyYWIxXkEyXkFqcGc@._V1_.jpg",
      "Midnight Mass": "https://m.media-amazon.com/images/M/MV5BNDdiOWE3Y2QtOGYxZi00OTlmLWEwOTktNGE4Y2JkMjdlMDU3XkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
      "Mighty Raju": "https://m.media-amazon.com/images/M/MV5BMTcxYjg0OGUtYzUxZi00MGE5LTg0ZDktOTFiYjZjMTBkZDUwXkEyXkFqcGc@._V1_.jpg",
      "Money Heist: From Tokyo to Berlin": "https://m.media-amazon.com/images/M/MV5BODcwNjQzODUtOTBmNS00Yzg2LTk2OWEtMWQzNzdkYzY1YWZlXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
      "Monsters Inside: The 24 Faces of Billy Milligan": "https://m.media-amazon.com/images/M/MV5BZDY4MjQ0MWUtZWVlMi00OTM2LThkOTgtNTkwYzZkN2I4ZDExXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
      "Motel Makeover": "https://m.media-amazon.com/images/M/MV5BNWQzM2E4NjItMTYxMy00NTYxLWE4YmMtYWQyZDM1MzIyZmExXkEyXkFqcGc@._V1_.jpg",
      "Mother Goose Club": "https://m.media-amazon.com/images/M/MV5BMTczMDMzNzQ3Ml5BMl5BanBnXkFtZTgwNDU2ODczMDE@._V1_.jpg",
      "Nailed It": "https://m.media-amazon.com/images/M/MV5BMDRkN2M2NDYtM2U4Yy00NDQwLWFjZDUtNTI0OTE5MmM4ZTMzXkEyXkFqcGc@._V1_.jpg",
      "Numberblocks": "https://m.media-amazon.com/images/I/71izhN6kD4L._AC_UF894,1000_QL80_.jpg",
      "Octonauts: Above & Beyond": "https://upload.wikimedia.org/wikipedia/en/f/fb/Octonauts_%E2%80%94_Above_%26_Beyond.jpg",
      "Oggy Oggy": "https://resizing.flixster.com/-XZAfHZM39UwaGJIFWKAE8fS0ak=/v3/t/assets/p20466737_b_v13_aa.jpg",
      "Oldsters": "https://occ-0-2433-2430.1.nflxso.net/dnm/api/v6/mAcAr9TxZIVbINe88xb3Teg5_OA/AAAABVpsPPKRii1mWVUsUy_SjccQ-SYlINDfQ6chSGsPrst-EVQO6N8ITPyqZsh3mxn4ZagW6kL9ic0KuOxhZ4uETe823M0EbYhRGu_W.jpg?r=d56",
      "On the Verge": "https://m.media-amazon.com/images/M/MV5BZmE1NjY0NTItZjU3YS00NTM1LThjODQtYTU2Y2FhNDU4NTc3XkEyXkFqcGc@._V1_QL75_UX190_CR0,2,190,281_.jpg",
      "Open Your Eyes": "https://m.media-amazon.com/images/M/MV5BY2M3OWNmOTgtNzgzOC00YmFjLWFmMGYtMDc1ZTkzY2QxZTIxXkEyXkFqcGc@._V1_.jpg",
      "Pokémon Master Journeys: The Series": "https://m.media-amazon.com/images/M/MV5BMDA0ZGMzNWUtM2JmYy00MWY1LTg4NzktNTFjMzIyNTE3NjA4XkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
      "Pororo - The Little Penguin": "https://m.media-amazon.com/images/M/MV5BM2M4NDUyYzYtYmQyNi00MTA2LTg3NzYtYzA0ZDViMDVjZDYwXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
      "Post Mortem: No One Dies in Skarnes": "https://upload.wikimedia.org/wikipedia/en/1/12/Post_Mortem_-_No_One_Dies_in_Skarnes.jpg",
      "Q-Force": "https://m.media-amazon.com/images/M/MV5BM2Q5ODVkYjMtZGMxYy00MzNhLWJhYWQtNzAzMTM2MTc5ZmU0XkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
      "RIDE ON TIME": "https://images.justwatch.com/poster/309487635/s332/season-5",
      "Raja Rasoi Aur Anya Kahaniyan": "https://m.media-amazon.com/images/M/MV5BODMyM2E1MjAtNDkxOC00MTUxLTljMTYtNTM2NTg1ZDM1NDMwXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
      "Rascal Does Not Dream of Bunny Girl Senpai": "https://m.media-amazon.com/images/I/81vuj1JYidL._AC_UF1000,1000_QL80_.jpg",
      "Rebellion": "https://m.media-amazon.com/images/M/MV5BOGNkNDc3MmItZTlkZS00ZjE0LWJmZTgtMGM2OWRhOTJjZDNiXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
      "Resurrection: Ertugrul": "https://m.media-amazon.com/images/M/MV5BOGI3NzE1ZWMtMDNlNS00MGFkLTk1OGQtNDFhNTEzNjU3MTRiXkEyXkFqcGc@._V1_.jpg",
      "Saved by the Bell": "https://m.media-amazon.com/images/M/MV5BNzEzMzM2ODc1Ml5BMl5BanBnXkFtZTcwMTg2MjAzMQ@@._V1_.jpg",
      "Sex Education": "https://m.media-amazon.com/images/M/MV5BOTE0MjQ1NDU3OV5BMl5BanBnXkFtZTgwNTI4MTgwNzM@._V1_.jpg",
      "Sharkdog": "https://m.media-amazon.com/images/M/MV5BNDQ1YjFkZWQtZDI2Zi00MTAzLWI4ZjctNmIzYTliZjdiZGJlXkEyXkFqcGc@._V1_.jpg",
      "Sparking Joy": "https://m.media-amazon.com/images/M/MV5BMjEwZDU2ZGMtYjgxZi00MGEwLWExM2YtOTcyOWFkMjU0Yjg1XkEyXkFqcGc@._V1_.jpg",
      "Squid Game": "https://m.media-amazon.com/images/M/MV5BYTU3ZDVhNmMtMDVlNC00MDc0LTgwNDMtYWE5MTI2ZGI4YWIwXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
      "Stories by Rabindranath Tagore": "https://m.media-amazon.com/images/M/MV5BNjhiYjNkNTMtZWEzNi00MzUzLWExMmItNDgyN2MxZGNhM2E0XkEyXkFqcGc@._V1_.jpg",
      "Tayo and Little Wizards": "https://img.rgstatic.com/content/show/e7a5b5ae-27fb-42e9-a4c9-73223657572d/poster-342.jpg",
      "Tayo the Little Bus": "https://m.media-amazon.com/images/M/MV5BZTc3NDFmZWUtN2VhOC00MzA0LWFmM2EtNjZjMTVkMmRkODY2XkEyXkFqcGc@._V1_.jpg",
      "The Chair": "https://m.media-amazon.com/images/M/MV5BNzgxZjk4MDUtZWE4ZS00MTIzLWJmNWQtMjA4MGNkMWM1M2YwXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
      "The Circle": "https://m.media-amazon.com/images/M/MV5BZjFlY2RjMDUtZTA4OC00YjM3LWIxZTQtZWFiYjMwNjRiY2ZlXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
      "The Creative Indians": "https://m.media-amazon.com/images/M/MV5BYmUyNTM0ZTItODVjNy00NDBmLTlhYmEtNTRjZGQxOTViOGM3XkEyXkFqcGc@._V1_.jpg",
      "The Defeated": "https://m.media-amazon.com/images/M/MV5BZDEzODk5ODItMzE3My00MTBiLWI5ZDgtYmVmY2U4NTVjZWE4XkEyXkFqcGc@._V1_.jpg",
      "The Great British Baking Show": "https://dnm.nflximg.net/api/v6/2DuQlx0fM4wd1nzqm5BFBi6ILa8/AAAAQZpCDVunFWjffZqT_85Cj3ZiasvSoGgldisgObTFqJ5-lVwUEBkodQUfqoKZjJaN2HcnAmdZPK1mcJPukAKOyC0TJNPB-SBwjpjRPwobe6OP1ifQK9nfgvNvXrzoMs1-jmM5c1AjsuXzK_e3V2La7_CC.jpg?r=12a",
      "The Ingenuity of the Househusband": "https://m.media-amazon.com/images/M/MV5BMWNmNDc5MDktNzc5Mi00ZTQ3LThhODktMjRjMzc2NzMxYzg5XkEyXkFqcGc@._V1_QL75_UY207_CR4,0,140,207_.jpg",
      "The Smart Money Woman": "https://m.media-amazon.com/images/I/61PtrLADPVL._AC_UF1000,1000_QL80_.jpg",
      "The World's Most Amazing Vacation Rentals": "https://m.media-amazon.com/images/M/MV5BN2I2YmI2ZDktNjkzMi00YjdiLWIzYTQtZDBjODQ2OWMwOWVhXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
      "Titipo Titipo": "https://m.media-amazon.com/images/M/MV5BNGMxMGI4ZTItOGQ3Ny00Y2M0LWE3ZGUtNWRhZWVhMDY4YmE3XkEyXkFqcGc@._V1_QL75_UY281_CR155,0,190,281_.jpg",
      "Titletown High": "https://m.media-amazon.com/images/M/MV5BZjg1Yzg1NDYtYWFlYS00ZjZiLTkzMjktMGFjNGY0OWRkZDdhXkEyXkFqcGc@._V1_.jpg",
      "Tobot Galaxy Detectives": "https://m.media-amazon.com/images/M/MV5BM2Y1YWE3YzAtMGM2OS00ZjA4LWFmNmQtZmY5MjZmOGRhY2Y5XkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
      "Too Hot To Handle: Latino": "https://m.media-amazon.com/images/M/MV5BM2VjMmRjMDAtZDYxZS00YTYwLTk3MmUtMGU1MTc0MzkzMjJiXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
      "Turning Point: 9/11 and the War on Terror": "https://upload.wikimedia.org/wikipedia/en/9/9c/Turning_Point_9-11_Poster.jpeg",
      "Vendetta: Truth, Lies and The Mafia": "https://m.media-amazon.com/images/M/MV5BMjliNjljN2QtNTc3NS00OGE4LWE0YTYtNTZkMGU0ZDZhMjQ2XkEyXkFqcGc@._V1_.jpg",
      "Wheel of Fortune": "https://m.media-amazon.com/images/M/MV5BYzMzNjVkYzQtZjNlMS00OTc1LTljOTktYzM3MzZkMmEzZjZhXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
      "Winx Club": "https://m.media-amazon.com/images/I/518DX9PTBZL._AC_UF894,1000_QL80_.jpg",
      "Yowamushi Pedal": "https://m.media-amazon.com/images/M/MV5BZmIzMDcyZjctZDI1ZS00YjVmLWI5ZjItODg2ZDY5ZWU5NmUyXkEyXkFqcGc@._V1_.jpg"
    }

    updated = 0

    for title, url in cover_images.items():
      if not url:
        continue

      show = Show.query.filter_by(title=title).first()
      if show:
        show.cover = url
        updated += 1

    db.session.commit()
    print(f"Updated {updated} show cover images.")

if __name__ == "__main__":
  seed_database()