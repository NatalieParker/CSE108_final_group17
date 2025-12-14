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

      for row in reader:
        if row["type"] != "TV Show":
          continue

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

    print("Database seeding complete!")


if __name__ == "__main__":
  seed_database()