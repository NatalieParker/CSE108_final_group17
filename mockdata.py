
from data_structure import db, User, Show, Episode, Watched, Review


def mockData():
    if User.query.first(): return
    
    u1 = User(username="alice", password="123456")
    u2 = User(username="bob", password="123456")
    u3 = User(username="tanya", password="123456")
    u4 = User(username="lily", password="123456")
    admin = User(username="admin", password="admin123", is_admin=True)

    db.session.add_all([u1, u2, u3, u4, admin])
    db.session.commit()

    s1 = Show(
        title="Breaking Bad",
        description="A chemistry teacher turns to crime.",
        release_year=2008
    )

    s2 = Show(
        title="Stranger Things",
        description="Supernatural events in a small town.",
        release_year=2016
    )

    s3 = Show(
        title="The Office",
        description="A mockumentary about office life.",
        release_year=2005
    )

    db.session.add_all([s1, s2, s3])
    db.session.commit()

    e1 = Episode(show_id=s1.id, episode_number=1, title="Pilot")
    e2 = Episode(show_id=s1.id, episode_number=2, title="Cat's in the Bag...")

    e3 = Episode(show_id=s2.id, episode_number=1, title="The Vanishing of Will Byers")
    e4 = Episode(show_id=s2.id, episode_number=2, title="The Weirdo on Maple Street")

    e5 = Episode(show_id=s3.id, episode_number=1, title="Pilot")
    e6 = Episode(show_id=s3.id, episode_number=2, title="Diversity Day")

    e7 = Episode(show_id=s1.id, episode_number=3, title="...And the Bag's in the River")
    e8 = Episode(show_id=s1.id, episode_number=4, title="Cancer Man")

    e9 = Episode(show_id=s2.id, episode_number=3, title="Holly, Jolly")
    e10 = Episode(show_id=s2.id, episode_number=4, title="The Body")

    e11 = Episode(show_id=s3.id, episode_number=3, title="Health Care")
    e12 = Episode(show_id=s3.id, episode_number=4, title="The Alliance")

    db.session.add_all([e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12])
    db.session.commit()

    w1 = Watched(user_id=u1.id, episode_id=e1.id)
    w2 = Watched(user_id=u1.id, episode_id=e2.id)
    w3 = Watched(user_id=u2.id, episode_id=e1.id)

    w4 = Watched(user_id=u3.id, episode_id=e3.id)
    w5 = Watched(user_id=u3.id, episode_id=e4.id)
    w6 = Watched(user_id=u3.id, episode_id=e5.id)

    db.session.add_all([w1, w2, w3, w4, w5, w6])
    db.session.commit()

    r1 = Review(
        user_id=u1.id,
        show_id=s1.id,
        rating=5,
        review_text="One of the best TV shows ever made."
    )

    r2 = Review(
        user_id=u2.id,
        show_id=s2.id,
        rating=4,
        review_text="Very engaging, especially the first season."
    )

    r3 = Review(
        user_id=u3.id,
        show_id=s3.id,
        rating=5,
        review_text="Hilarious and endlessly rewatchable."
    )

    r4 = Review(
        user_id=u3.id,
        show_id=s2.id,
        rating=5,
        review_text="A great show to watch with the family."
    )

    db.session.add_all([r1, r2, r3, r4])
    db.session.commit()