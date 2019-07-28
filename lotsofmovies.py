from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Genre, Base, Movie, User

engine = create_engine('sqlite:///genremovie.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Create dummy user 
User1 = User(name="Joyce Yu", email="joyce.mn.yu@gmail.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()


# Movie for Action & Adventure
genre1 = Genre(user_id = 1, name="Action & Adventure")

session.add(genre1)
session.commit()

movie1 = Movie(user_id = 1, name="Jurassic World", description="Owen and Claire return to the ruins of the Jurassic World theme park to rescue the remaining dinosaurs from a looming volcanic extinction",
                     director="J.A. Bayona", starring="Chris Pratt, Bryce Dallas Howard, Rafe Spall", genre=genre1)


session.add(movie1)
session.commit()

movie2 = Movie(user_id = 1, name="Venom", description="Tom Hardy stars as the lethal protector and anti-hero Venom - one of Marvel's most enigmatic and complex characters",
                     director="Ruben Fleischer", starring="Michelle Williams, Reid Scott", genre=genre1)

session.add(movie2)
session.commit()

movie3 = Movie(user_id = 1, name="Deadpool", description="The Super Duper Cut, now with 15 minutes of brand-new action and jokes lovingly inserted throughout",
                     director="David Leitch", starring="Ryan Reynolds", genre=genre1)

session.add(movie3)
session.commit()




# Movie list for Children & Family
genre2 = Genre(user_id = 1, name="Children & Family")

session.add(genre2)
session.commit()


movie1 = Movie(user_id = 1, name="Kung Fu Panda", description="Four young pandas go on the adventure of a lifetime",
                     director="John Stevenson", starring="Jack Black, Dustin Hoffman, Angelina Jolie", genre=genre2)

session.add(movie1)
session.commit()

movie2 = Movie(user_id = 1, name="Ronja, the Robber's Daughter", description="The daughter of a professional robber, Ronja realizes the complicated nature of her father's profession when she befriends Birk, the child of a rival tribe",
                     director="Goro Miyazaki", starring="Gillian Anderson, Theresa Gallagher", genre=genre2)

session.add(movie2)
session.commit()

movie3 = Movie(user_id = 1, name="Teenage Mutant Ninja Turtles", description="The Turtles have been forced to move in with their friend the news reporter April O'Neil, because the Foot Clan knows the whereabouts of their lair in the sewers",
                     director="	Michael Pressman, Michael Pressman", starring="Paige Turco, David Warner, Michelan Sisti", genre=genre2)

session.add(movie3)
session.commit()


# Movie list for Comedy
genre3 = Genre(user_id = 1, name="Comedy")

session.add(genre3)
session.commit()


movie1 = Movie(user_id = 1, name="The Spy Who Dumped Me", description="After being dumped by her boyfriend who is a spy, a woman and her friend become embroiled in a conspiracy.",
                     director="Susanna Fogel", starring="Mila Kunis and Kate McKinnon", genre=genre3)

session.add(movie1)
session.commit()

movie2 = Movie(user_id = 1, name="Chef", description="A head chef (Jon Favreau) quits his restaurant job and buys a food truck in an effort to reclaim his creative promise, all while piecing back together his estranged family.",
                     director="Jon Favreau", starring="Robert Downey , Scarlett Johansson , Jon Favreau , et al.", genre=genre3)

session.add(movie2)
session.commit()

movie3 = Movie(user_id = 1, name="Overboard", description="A selfish, rich playboy, Leonardo, fires a hard working single mother, Kate, hired to clean his yacht. After getting amneisa Kate convinces him he is her husband as payback and puts him to work.",
                     director="Bob Fisher and Rob Greenberg", starring="Eugenio Derbez , Anna Faris , Eva Longoria and John Hannah", genre=genre3)

session.add(movie3)
session.commit()