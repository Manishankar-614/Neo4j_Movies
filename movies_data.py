"""
Neo4j Movies Dataset definition.
Contains the official Neo4j :play movies Cypher query and structured graph definitions
used for database seeding and built-in local graph fallback.
"""

# Official Neo4j Movies Cypher script
OFFICIAL_MOVIES_CYPHER = """
CREATE (TheMatrix:Movie {title:'The Matrix', released:1999, tagline:'Welcome to the Real World'})
CREATE (Keanu:Person {name:'Keanu Reeves', born:1964})
CREATE (Carrie:Person {name:'Carrie-Anne Moss', born:1967})
CREATE (Laurence:Person {name:'Laurence Fishburne', born:1961})
CREATE (Hugo:Person {name:'Hugo Weaving', born:1960})
CREATE (LillyW:Person {name:'Lilly Wachowski', born:1967})
CREATE (LanaW:Person {name:'Lana Wachowski', born:1965})
CREATE (JoelS:Person {name:'Joel Silver', born:1952})
CREATE
  (Keanu)-[:ACTED_IN {roles:['Neo']}]->(TheMatrix),
  (Carrie)-[:ACTED_IN {roles:['Trinity']}]->(TheMatrix),
  (Laurence)-[:ACTED_IN {roles:['Morpheus']}]->(TheMatrix),
  (Hugo)-[:ACTED_IN {roles:['Agent Smith']}]->(TheMatrix),
  (LillyW)-[:DIRECTED]->(TheMatrix),
  (LanaW)-[:DIRECTED]->(TheMatrix),
  (JoelS)-[:PRODUCED]->(TheMatrix)

CREATE (Emil:Person {name:'Emil Eifrem', born:1978})
CREATE (Emil)-[:ACTED_IN {roles:['Emil']}]->(TheMatrix)

CREATE (TheMatrixReloaded:Movie {title:'The Matrix Reloaded', released:2003, tagline:'Free your mind'})
CREATE
  (Keanu)-[:ACTED_IN {roles:['Neo']}]->(TheMatrixReloaded),
  (Carrie)-[:ACTED_IN {roles:['Trinity']}]->(TheMatrixReloaded),
  (Laurence)-[:ACTED_IN {roles:['Morpheus']}]->(TheMatrixReloaded),
  (Hugo)-[:ACTED_IN {roles:['Agent Smith']}]->(TheMatrixReloaded),
  (LillyW)-[:DIRECTED]->(TheMatrixReloaded),
  (LanaW)-[:DIRECTED]->(TheMatrixReloaded),
  (JoelS)-[:PRODUCED]->(TheMatrixReloaded)

CREATE (TheMatrixRevolutions:Movie {title:'The Matrix Revolutions', released:2003, tagline:'Everything that has a beginning has an end'})
CREATE
  (Keanu)-[:ACTED_IN {roles:['Neo']}]->(TheMatrixRevolutions),
  (Carrie)-[:ACTED_IN {roles:['Trinity']}]->(TheMatrixRevolutions),
  (Laurence)-[:ACTED_IN {roles:['Morpheus']}]->(TheMatrixRevolutions),
  (Hugo)-[:ACTED_IN {roles:['Agent Smith']}]->(TheMatrixRevolutions),
  (LillyW)-[:DIRECTED]->(TheMatrixRevolutions),
  (LanaW)-[:DIRECTED]->(TheMatrixRevolutions),
  (JoelS)-[:PRODUCED]->(TheMatrixRevolutions)

CREATE (TheDevilsAdvocate:Movie {title:"The Devil's Advocate", released:1997, tagline:'Evil has its winning ways'})
CREATE (Charlize:Person {name:'Charlize Theron', born:1975})
CREATE (Al:Person {name:'Al Pacino', born:1940})
CREATE (Taylor:Person {name:'Taylor Hackford', born:1944})
CREATE
  (Keanu)-[:ACTED_IN {roles:['Kevin Lomax']}]->(TheDevilsAdvocate),
  (Charlize)-[:ACTED_IN {roles:['Mary Ann Lomax']}]->(TheDevilsAdvocate),
  (Al)-[:ACTED_IN {roles:['John Milton']}]->(TheDevilsAdvocate),
  (Taylor)-[:DIRECTED]->(TheDevilsAdvocate)

CREATE (AFewGoodMen:Movie {title:'A Few Good Men', released:1992, tagline:"In the heart of the nation's capital, in a courthouse of the U.S. government, one man will stop at nothing to keep his honor, and one will stop at nothing to find the truth."})
CREATE (TomC:Person {name:'Tom Cruise', born:1962})
CREATE (JackN:Person {name:'Jack Nicholson', born:1937})
CREATE (DemiM:Person {name:'Demi Moore', born:1962})
CREATE (KevinB:Person {name:'Kevin Bacon', born:1958})
CREATE (KieferS:Person {name:'Kiefer Sutherland', born:1966})
CREATE (NoahW:Person {name:'Noah Wyle', born:1971})
CREATE (CubaG:Person {name:'Cuba Gooding Jr.', born:1968})
CREATE (KevinP:Person {name:'Kevin Pollak', born:1957})
CREATE (JTW:Person {name:'J.T. Walsh', born:1943})
CREATE (JamesM:Person {name:'James Marshall', born:1967})
CREATE (ChristopherG:Person {name:'Christopher Guest', born:1948})
CREATE (RobR:Person {name:'Rob Reiner', born:1947})
CREATE (AaronS:Person {name:'Aaron Sorkin', born:1961})
CREATE
  (TomC)-[:ACTED_IN {roles:['Lt. Daniel Kaffee']}]->(AFewGoodMen),
  (JackN)-[:ACTED_IN {roles:['Col. Nathan R. Jessep']}]->(AFewGoodMen),
  (DemiM)-[:ACTED_IN {roles:['Lt. Cdr. JoAnne Galloway']}]->(AFewGoodMen),
  (KevinB)-[:ACTED_IN {roles:['Capt. Jack Challee']}]->(AFewGoodMen),
  (KieferS)-[:ACTED_IN {roles:['Lt. Jonathan Kendrick']}]->(AFewGoodMen),
  (NoahW)-[:ACTED_IN {roles:['Cpl. Jeffrey Barnes']}]->(AFewGoodMen),
  (CubaG)-[:ACTED_IN {roles:['Cpl. Carl Hammaker']}]->(AFewGoodMen),
  (KevinP)-[:ACTED_IN {roles:['Lt. Sam Weinberg']}]->(AFewGoodMen),
  (JTW)-[:ACTED_IN {roles:['Lt. Col. Matthew Andrew Markinson']}]->(AFewGoodMen),
  (JamesM)-[:ACTED_IN {roles:['Pfc. Louden Downey']}]->(AFewGoodMen),
  (ChristopherG)-[:ACTED_IN {roles:['Dr. Stone']}]->(AFewGoodMen),
  (AaronS)-[:ACTED_IN {roles:['Man in Bar']}]->(AFewGoodMen),
  (RobR)-[:DIRECTED]->(AFewGoodMen),
  (AaronS)-[:WROTE]->(AFewGoodMen)

CREATE (TopGun:Movie {title:'Top Gun', released:1986, tagline:'I feel the need, the need for speed.'})
CREATE (KellyM:Person {name:'Kelly McGillis', born:1957})
CREATE (ValK:Person {name:'Val Kilmer', born:1959})
CREATE (AnthonyE:Person {name:'Anthony Edwards', born:1962})
CREATE (TomS:Person {name:'Tom Skerritt', born:1933})
CREATE (MegR:Person {name:'Meg Ryan', born:1961})
CREATE (TonyS:Person {name:'Tony Scott', born:1944})
CREATE (JimC:Person {name:'Jim Cash', born:1941})
CREATE
  (TomC)-[:ACTED_IN {roles:['Maverick']}]->(TopGun),
  (KellyM)-[:ACTED_IN {roles:['Charlie']}]->(TopGun),
  (ValK)-[:ACTED_IN {roles:['Iceman']}]->(TopGun),
  (AnthonyE)-[:ACTED_IN {roles:['Goose']}]->(TopGun),
  (TomS)-[:ACTED_IN {roles:['Viper']}]->(TopGun),
  (MegR)-[:ACTED_IN {roles:['Carole']}]->(TopGun),
  (TonyS)-[:DIRECTED]->(TopGun),
  (JimC)-[:WROTE]->(TopGun)

CREATE (JerryMaguire:Movie {title:'Jerry Maguire', released:1996, tagline:'The rest of his life begins now.'})
CREATE (ReneeZ:Person {name:'Renee Zellweger', born:1969})
CREATE (KellyP:Person {name:'Kelly Preston', born:1962})
CREATE (JerryO:Person {name:"Jerry O'Connell", born:1974})
CREATE (JayM:Person {name:'Jay Mohr', born:1970})
CREATE (BonnieH:Person {name:'Bonnie Hunt', born:1961})
CREATE (ReginaK:Person {name:'Regina King', born:1971})
CREATE (JonathanL:Person {name:'Jonathan Lipnicki', born:1990})
CREATE (CameronC:Person {name:'Cameron Crowe', born:1957})
CREATE
  (TomC)-[:ACTED_IN {roles:['Jerry Maguire']}]->(JerryMaguire),
  (CubaG)-[:ACTED_IN {roles:['Rod Tidwell']}]->(JerryMaguire),
  (ReneeZ)-[:ACTED_IN {roles:['Dorothy Boyd']}]->(JerryMaguire),
  (KellyP)-[:ACTED_IN {roles:['Avery Bishop']}]->(JerryMaguire),
  (JerryO)-[:ACTED_IN {roles:['Frank Cushman']}]->(JerryMaguire),
  (JayM)-[:ACTED_IN {roles:['Bob Sugar']}]->(JerryMaguire),
  (BonnieH)-[:ACTED_IN {roles:['Laurel Boyd']}]->(JerryMaguire),
  (ReginaK)-[:ACTED_IN {roles:['Marcee Tidwell']}]->(JerryMaguire),
  (JonathanL)-[:ACTED_IN {roles:['Ray Boyd']}]->(JerryMaguire),
  (CameronC)-[:DIRECTED]->(JerryMaguire),
  (CameronC)-[:PRODUCED]->(JerryMaguire),
  (CameronC)-[:WROTE]->(JerryMaguire)

CREATE (StandByMe:Movie {title:'Stand By Me', released:1986, tagline:"For some, it's the last real adventure of a youth, for the rest, it's the first step into adulthood."})
CREATE (RiverP:Person {name:'River Phoenix', born:1970})
CREATE (CoreyF:Person {name:'Corey Feldman', born:1971})
CREATE (WilW:Person {name:'Wil Wheaton', born:1972})
CREATE (JohnC:Person {name:'John Cusack', born:1966})
CREATE (MarshallB:Person {name:'Marshall Bell', born:1942})
CREATE
  (WilW)-[:ACTED_IN {roles:['Gordie Lachance']}]->(StandByMe),
  (RiverP)-[:ACTED_IN {roles:['Chris Chambers']}]->(StandByMe),
  (JerryO)-[:ACTED_IN {roles:['Vern Tessio']}]->(StandByMe),
  (CoreyF)-[:ACTED_IN {roles:['Teddy Duchamp']}]->(StandByMe),
  (JohnC)-[:ACTED_IN {roles:['Denny Lachance']}]->(StandByMe),
  (KieferS)-[:ACTED_IN {roles:['Ace Merrill']}]->(StandByMe),
  (MarshallB)-[:ACTED_IN {roles:['Mr. Lachance']}]->(StandByMe),
  (RobR)-[:DIRECTED]->(StandByMe)

CREATE (Apollo13:Movie {title:'Apollo 13', released:1995, tagline:'Houston, we have a problem.'})
CREATE (TomH:Person {name:'Tom Hanks', born:1956})
CREATE (BillPax:Person {name:'Bill Paxton', born:1955})
CREATE (EdH:Person {name:'Ed Harris', born:1950})
CREATE (GaryS:Person {name:'Gary Sinise', born:1955})
CREATE (RonH:Person {name:'Ron Howard', born:1954})
CREATE
  (TomH)-[:ACTED_IN {roles:['Jim Lovell']}]->(Apollo13),
  (KevinB)-[:ACTED_IN {roles:['Jack Swigert']}]->(Apollo13),
  (BillPax)-[:ACTED_IN {roles:['Fred Haise']}]->(Apollo13),
  (GaryS)-[:ACTED_IN {roles:['Ken Mattingly']}]->(Apollo13),
  (EdH)-[:ACTED_IN {roles:['Gene Kranz']}]->(Apollo13),
  (RonH)-[:DIRECTED]->(Apollo13)

CREATE (CastAway:Movie {title:'Cast Away', released:2000, tagline:'At the edge of the world, his journey begins.'})
CREATE (HelenH:Person {name:'Helen Hunt', born:1963})
CREATE (RobertZ:Person {name:'Robert Zemeckis', born:1951})
CREATE
  (TomH)-[:ACTED_IN {roles:['Chuck Noland']}]->(CastAway),
  (HelenH)-[:ACTED_IN {roles:['Kelly Frears']}]->(CastAway),
  (RobertZ)-[:DIRECTED]->(CastAway)

CREATE (YouveGotMail:Movie {title:"You've Got Mail", released:1998, tagline:'At great risk of looking like a flirt.'})
CREATE (GregK:Person {name:'Greg Kinnear', born:1963})
CREATE (SteveZ:Person {name:'Steve Zahn', born:1967})
CREATE (DaveC:Person {name:'Dave Chappelle', born:1973})
CREATE (NoraE:Person {name:'Nora Ephron', born:1941})
CREATE
  (TomH)-[:ACTED_IN {roles:['Joe Fox']}]->(YouveGotMail),
  (MegR)-[:ACTED_IN {roles:['Kathleen Kelly']}]->(YouveGotMail),
  (GregK)-[:ACTED_IN {roles:['Frank Navasky']}]->(YouveGotMail),
  (SteveZ)-[:ACTED_IN {roles:['George Pappas']}]->(YouveGotMail),
  (DaveC)-[:ACTED_IN {roles:['Kevin Jackson']}]->(YouveGotMail),
  (ParkerP:Person {name:'Parker Posey', born:1968})-[:ACTED_IN {roles:['Patricia Eden']}]->(YouveGotMail),
  (NoraE)-[:DIRECTED]->(YouveGotMail),
  (NoraE)-[:WROTE]->(YouveGotMail)

CREATE (SleeplessInSeattle:Movie {title:'Sleepless in Seattle', released:1993, tagline:'What if someone you never met, someone you never saw, someone you never knew was the only someone for you?'})
CREATE (RitaW:Person {name:'Rita Wilson', born:1956})
CREATE (BillPull:Person {name:'Bill Pullman', born:1953})
CREATE (VictorG:Person {name:'Victor Garber', born:1949})
CREATE (RosieO:Person {name:"Rosie O'Donnell", born:1962})
CREATE
  (TomH)-[:ACTED_IN {roles:['Sam Baldwin']}]->(SleeplessInSeattle),
  (MegR)-[:ACTED_IN {roles:['Annie Reed']}]->(SleeplessInSeattle),
  (BillPull)-[:ACTED_IN {roles:['Walter']}]->(SleeplessInSeattle),
  (RitaW)-[:ACTED_IN {roles:['Suzy']}]->(SleeplessInSeattle),
  (RosieO)-[:ACTED_IN {roles:['Becky']}]->(SleeplessInSeattle),
  (VictorG)-[:ACTED_IN {roles:['Greg']}]->(SleeplessInSeattle),
  (NoraE)-[:DIRECTED]->(SleeplessInSeattle),
  (NoraE)-[:WROTE]->(SleeplessInSeattle)

CREATE (JoeVersusTheVolcano:Movie {title:'Joe Versus the Volcano', released:1990, tagline:'A story of love, lava and living.'})
CREATE (JohnS:Person {name:'John Patrick Shanley', born:1950})
CREATE (Nathan:Person {name:'Nathan Lane', born:1956})
CREATE
  (TomH)-[:ACTED_IN {roles:['Joe Banks']}]->(JoeVersusTheVolcano),
  (MegR)-[:ACTED_IN {roles:['DeDe', 'Angelica Graynamore', 'Patricia Graynamore']}]->(JoeVersusTheVolcano),
  (Nathan)-[:ACTED_IN {roles:['Baw']}]->(JoeVersusTheVolcano),
  (JohnS)-[:DIRECTED]->(JoeVersusTheVolcano),
  (JohnS)-[:WROTE]->(JoeVersusTheVolcano)

CREATE (WhenHarryMetSally:Movie {title:'When Harry Met Sally', released:1989, tagline:'Can two friends sleep together and still remain friends?'})
CREATE (BillyC:Person {name:'Billy Crystal', born:1948})
CREATE (CarrieF:Person {name:'Carrie Fisher', born:1956})
CREATE (BrunoK:Person {name:'Bruno Kirby', born:1949})
CREATE
  (BillyC)-[:ACTED_IN {roles:['Harry Burns']}]->(WhenHarryMetSally),
  (MegR)-[:ACTED_IN {roles:['Sally Albright']}]->(WhenHarryMetSally),
  (CarrieF)-[:ACTED_IN {roles:['Marie']}]->(WhenHarryMetSally),
  (BrunoK)-[:ACTED_IN {roles:['Jess']}]->(WhenHarryMetSally),
  (RobR)-[:DIRECTED]->(WhenHarryMetSally),
  (RobR)-[:PRODUCED]->(WhenHarryMetSally),
  (NoraE)-[:PRODUCED]->(WhenHarryMetSally),
  (NoraE)-[:WROTE]->(WhenHarryMetSally)

CREATE (ThatThingYouDo:Movie {title:'That Thing You Do', released:1996, tagline:'In every life there comes a time when that thing you dream becomes that thing you do'})
CREATE (LivT:Person {name:'Liv Tyler', born:1977})
CREATE
  (TomH)-[:ACTED_IN {roles:['Mr. White']}]->(ThatThingYouDo),
  (LivT)-[:ACTED_IN {roles:['Faye Dolan']}]->(ThatThingYouDo),
  (Charlize)-[:ACTED_IN {roles:['Tina']}]->(ThatThingYouDo),
  (TomH)-[:DIRECTED]->(ThatThingYouDo),
  (TomH)-[:WROTE]->(ThatThingYouDo)

CREATE (TheReplacements:Movie {title:'The Replacements', released:2000, tagline:'Pain heals, Chicks dig scars... Glory lasts forever'})
CREATE (Brooke:Person {name:'Brooke Langton', born:1970})
CREATE (Gene:Person {name:'Gene Hackman', born:1930})
CREATE (Orlando:Person {name:'Orlando Jones', born:1968})
CREATE (Howard:Person {name:'Howard Deutch', born:1950})
CREATE
  (Keanu)-[:ACTED_IN {roles:['Shane Falco']}]->(TheReplacements),
  (Brooke)-[:ACTED_IN {roles:['Annabelle Farrell']}]->(TheReplacements),
  (Gene)-[:ACTED_IN {roles:['Jimmy McGinty']}]->(TheReplacements),
  (Orlando)-[:ACTED_IN {roles:['Clifford Franklin']}]->(TheReplacements),
  (Howard)-[:DIRECTED]->(TheReplacements)

CREATE (Unforgiven:Movie {title:'Unforgiven', released:1992, tagline:"It's a hell of a thing, killing a man"})
CREATE (RichardH:Person {name:'Richard Harris', born:1930})
CREATE (ClintE:Person {name:'Clint Eastwood', born:1930})
CREATE
  (ClintE)-[:ACTED_IN {roles:['Bill Munny']}]->(Unforgiven),
  (Gene)-[:ACTED_IN {roles:['Little Bill Daggett']}]->(Unforgiven),
  (MorganF:Person {name:'Morgan Freeman', born:1937})-[:ACTED_IN {roles:['Ned Logan']}]->(Unforgiven),
  (RichardH)-[:ACTED_IN {roles:['English Bob']}]->(Unforgiven),
  (ClintE)-[:DIRECTED]->(Unforgiven)

CREATE (TheBirdcage:Movie {title:'The Birdcage', released:1996, tagline:'Come as you are'})
CREATE (Robin:Person {name:'Robin Williams', born:1951})
CREATE (MikeN:Person {name:'Mike Nichols', born:1931})
CREATE
  (Robin)-[:ACTED_IN {roles:['Armand Goldman']}]->(TheBirdcage),
  (Nathan)-[:ACTED_IN {roles:['Albert Goldman']}]->(TheBirdcage),
  (Gene)-[:ACTED_IN {roles:['Sen. Kevin Keeley']}]->(TheBirdcage),
  (MikeN)-[:DIRECTED]->(TheBirdcage)

CREATE (TheDaVinciCode:Movie {title:'The Da Vinci Code', released:2006, tagline:'Seek and you will find'})
CREATE (IanM:Person {name:'Ian McKellen', born:1939})
CREATE (AudreyT:Person {name:'Audrey Tautou', born:1976})
CREATE (PaulB:Person {name:'Paul Bettany', born:1971})
CREATE
  (TomH)-[:ACTED_IN {roles:['Dr. Robert Langdon']}]->(TheDaVinciCode),
  (IanM)-[:ACTED_IN {roles:['Sir Leigh Teabing']}]->(TheDaVinciCode),
  (AudreyT)-[:ACTED_IN {roles:['Sophie Neveu']}]->(TheDaVinciCode),
  (PaulB)-[:ACTED_IN {roles:['Silas']}]->(TheDaVinciCode),
  (RonH)-[:DIRECTED]->(TheDaVinciCode)

CREATE (VForVendetta:Movie {title:'V for Vendetta', released:2005, tagline:'Freedom! Forever!'})
CREATE (NatalieP:Person {name:'Natalie Portman', born:1981})
CREATE (StephenR:Person {name:'Stephen Rea', born:1946})
CREATE (JohnH:Person {name:'John Hurt', born:1940})
CREATE (BenM:Person {name:'Ben Miles', born:1967})
CREATE (JamesMct:Person {name:'James McTeigue', born:1967})
CREATE
  (Hugo)-[:ACTED_IN {roles:['V']}]->(VForVendetta),
  (NatalieP)-[:ACTED_IN {roles:['Evey Hammond']}]->(VForVendetta),
  (StephenR)-[:ACTED_IN {roles:['Eric Finch']}]->(VForVendetta),
  (JohnH)-[:ACTED_IN {roles:['Adam Sutler']}]->(VForVendetta),
  (BenM)-[:ACTED_IN {roles:['Dascomb']}]->(VForVendetta),
  (JamesMct)-[:DIRECTED]->(VForVendetta),
  (LillyW)-[:WROTE]->(VForVendetta),
  (LanaW)-[:WROTE]->(VForVendetta),
  (JoelS)-[:PRODUCED]->(VForVendetta)

CREATE (CloudAtlas:Movie {title:'Cloud Atlas', released:2012, tagline:'Everything is Connected'})
CREATE (HalleB:Person {name:'Halle Berry', born:1966})
CREATE (JimB:Person {name:'Jim Broadbent', born:1949})
CREATE (TomT:Person {name:'Tom Tykwer', born:1965})
CREATE
  (TomH)-[:ACTED_IN {roles:['Zachry', 'Dr. Henry Goose', 'Isaac Sachs', 'Dermot Hoggins']}]->(CloudAtlas),
  (Hugo)-[:ACTED_IN {roles:['Bill Smoke', 'Haskell Moore', 'Tadeusz Kesselring', 'Nurse Noakes', 'Boardman Mephi', 'Old Georgie']}]->(CloudAtlas),
  (HalleB)-[:ACTED_IN {roles:['Luisa Rey', 'Jocasta Ayrs', 'Ovid', 'Meronym']}]->(CloudAtlas),
  (JimB)-[:ACTED_IN {roles:['Vyvyan Ayrs', 'Captain Molyneux', 'Timothy Cavendish']}]->(CloudAtlas),
  (TomT)-[:DIRECTED]->(CloudAtlas),
  (LillyW)-[:DIRECTED]->(CloudAtlas),
  (LanaW)-[:DIRECTED]->(CloudAtlas)

CREATE (TheGreenMile:Movie {title:'The Green Mile', released:1999, tagline:"Walk a mile you'll never forget."})
CREATE (MichaelD:Person {name:'Michael Clarke Duncan', born:1957})
CREATE (DavidM:Person {name:'David Morse', born:1953})
CREATE (SamR:Person {name:'Sam Rockwell', born:1968})
CREATE (FrankD:Person {name:'Frank Darabont', born:1959})
CREATE
  (TomH)-[:ACTED_IN {roles:['Paul Edgecomb']}]->(TheGreenMile),
  (MichaelD)-[:ACTED_IN {roles:['John Coffey']}]->(TheGreenMile),
  (DavidM)-[:ACTED_IN {roles:['Brutus "Brutal" Howell']}]->(TheGreenMile),
  (BonnieH)-[:ACTED_IN {roles:['Jan Edgecomb']}]->(TheGreenMile),
  (JamesC:Person {name:'James Cromwell', born:1940})-[:ACTED_IN {roles:['Warden Hal Moores']}]->(TheGreenMile),
  (SamR)-[:ACTED_IN {roles:['"Wild Bill" Wharton']}]->(TheGreenMile),
  (GaryS)-[:ACTED_IN {roles:['Burt Hammersmith']}]->(TheGreenMile),
  (FrankD)-[:DIRECTED]->(TheGreenMile)

CREATE (JessicaT:Person {name:'Jessica Thompson', born:1980})
CREATE (JamesC)-[:REVIEWED {summary:'Greatest prison movie ever made', rating:95}]->(TheGreenMile)
CREATE (JessicaT)-[:REVIEWED {summary:'Heartbreaking and magical masterclass', rating:90}]->(TheGreenMile)
CREATE (JessicaT)-[:REVIEWED {summary:'An extraordinary sci-fi mind-bender', rating:95}]->(TheMatrix)
CREATE (JessicaT)-[:REVIEWED {summary:'Fun romantic chemistry between Hanks and Ryan', rating:82}]->(YouveGotMail)
"""

# Structured dictionary representation of the dataset for local fallback & in-memory graph
LOCAL_MOVIES_DATA = {
    "movies": [
        {"title": "The Matrix", "released": 1999, "tagline": "Welcome to the Real World"},
        {"title": "The Matrix Reloaded", "released": 2003, "tagline": "Free your mind"},
        {"title": "The Matrix Revolutions", "released": 2003, "tagline": "Everything that has a beginning has an end"},
        {"title": "The Devil's Advocate", "released": 1997, "tagline": "Evil has its winning ways"},
        {"title": "A Few Good Men", "released": 1992, "tagline": "In the heart of the nation's capital, in a courthouse of the U.S. government, one man will stop at nothing to keep his honor, and one will stop at nothing to find the truth."},
        {"title": "Top Gun", "released": 1986, "tagline": "I feel the need, the need for speed."},
        {"title": "Jerry Maguire", "released": 1996, "tagline": "The rest of his life begins now."},
        {"title": "Stand By Me", "released": 1986, "tagline": "For some, it's the last real adventure of a youth, for the rest, it's the first step into adulthood."},
        {"title": "Apollo 13", "released": 1995, "tagline": "Houston, we have a problem."},
        {"title": "Cast Away", "released": 2000, "tagline": "At the edge of the world, his journey begins."},
        {"title": "You've Got Mail", "released": 1998, "tagline": "At great risk of looking like a flirt."},
        {"title": "Sleepless in Seattle", "released": 1993, "tagline": "What if someone you never met, someone you never saw, someone you never knew was the only someone for you?"},
        {"title": "Joe Versus the Volcano", "released": 1990, "tagline": "A story of love, lava and living."},
        {"title": "When Harry Met Sally", "released": 1989, "tagline": "Can two friends sleep together and still remain friends?"},
        {"title": "That Thing You Do", "released": 1996, "tagline": "In every life there comes a time when that thing you dream becomes that thing you do"},
        {"title": "The Replacements", "released": 2000, "tagline": "Pain heals, Chicks dig scars... Glory lasts forever"},
        {"title": "Unforgiven", "released": 1992, "tagline": "It's a hell of a thing, killing a man"},
        {"title": "The Birdcage", "released": 1996, "tagline": "Come as you are"},
        {"title": "The Da Vinci Code", "released": 2006, "tagline": "Seek and you will find"},
        {"title": "V for Vendetta", "released": 2005, "tagline": "Freedom! Forever!"},
        {"title": "Cloud Atlas", "released": 2012, "tagline": "Everything is Connected"},
        {"title": "The Green Mile", "released": 1999, "tagline": "Walk a mile you'll never forget."}
    ],
    "people": [
        {"name": "Keanu Reeves", "born": 1964},
        {"name": "Carrie-Anne Moss", "born": 1967},
        {"name": "Laurence Fishburne", "born": 1961},
        {"name": "Hugo Weaving", "born": 1960},
        {"name": "Lana Wachowski", "born": 1965},
        {"name": "Lilly Wachowski", "born": 1967},
        {"name": "Joel Silver", "born": 1952},
        {"name": "Emil Eifrem", "born": 1978},
        {"name": "Charlize Theron", "born": 1975},
        {"name": "Al Pacino", "born": 1940},
        {"name": "Taylor Hackford", "born": 1944},
        {"name": "Tom Cruise", "born": 1962},
        {"name": "Jack Nicholson", "born": 1937},
        {"name": "Demi Moore", "born": 1962},
        {"name": "Kevin Bacon", "born": 1958},
        {"name": "Kiefer Sutherland", "born": 1966},
        {"name": "Noah Wyle", "born": 1971},
        {"name": "Cuba Gooding Jr.", "born": 1968},
        {"name": "Kevin Pollak", "born": 1957},
        {"name": "J.T. Walsh", "born": 1943},
        {"name": "James Marshall", "born": 1967},
        {"name": "Christopher Guest", "born": 1948},
        {"name": "Rob Reiner", "born": 1947},
        {"name": "Aaron Sorkin", "born": 1961},
        {"name": "Kelly McGillis", "born": 1957},
        {"name": "Val Kilmer", "born": 1959},
        {"name": "Anthony Edwards", "born": 1962},
        {"name": "Tom Skerritt", "born": 1933},
        {"name": "Meg Ryan", "born": 1961},
        {"name": "Tony Scott", "born": 1944},
        {"name": "Jim Cash", "born": 1941},
        {"name": "Renee Zellweger", "born": 1969},
        {"name": "Kelly Preston", "born": 1962},
        {"name": "Jerry O'Connell", "born": 1974},
        {"name": "Jay Mohr", "born": 1970},
        {"name": "Bonnie Hunt", "born": 1961},
        {"name": "Regina King", "born": 1971},
        {"name": "Jonathan Lipnicki", "born": 1990},
        {"name": "Cameron Crowe", "born": 1957},
        {"name": "River Phoenix", "born": 1970},
        {"name": "Corey Feldman", "born": 1971},
        {"name": "Wil Wheaton", "born": 1972},
        {"name": "John Cusack", "born": 1966},
        {"name": "Marshall Bell", "born": 1942},
        {"name": "Tom Hanks", "born": 1956},
        {"name": "Bill Paxton", "born": 1955},
        {"name": "Ed Harris", "born": 1950},
        {"name": "Gary Sinise", "born": 1955},
        {"name": "Ron Howard", "born": 1954},
        {"name": "Helen Hunt", "born": 1963},
        {"name": "Robert Zemeckis", "born": 1951},
        {"name": "Greg Kinnear", "born": 1963},
        {"name": "Steve Zahn", "born": 1967},
        {"name": "Dave Chappelle", "born": 1973},
        {"name": "Nora Ephron", "born": 1941},
        {"name": "Parker Posey", "born": 1968},
        {"name": "Rita Wilson", "born": 1956},
        {"name": "Bill Pullman", "born": 1953},
        {"name": "Victor Garber", "born": 1949},
        {"name": "Rosie O'Donnell", "born": 1962},
        {"name": "John Patrick Shanley", "born": 1950},
        {"name": "Nathan Lane", "born": 1956},
        {"name": "Billy Crystal", "born": 1948},
        {"name": "Carrie Fisher", "born": 1956},
        {"name": "Bruno Kirby", "born": 1949},
        {"name": "Liv Tyler", "born": 1977},
        {"name": "Brooke Langton", "born": 1970},
        {"name": "Gene Hackman", "born": 1930},
        {"name": "Orlando Jones", "born": 1968},
        {"name": "Howard Deutch", "born": 1950},
        {"name": "Richard Harris", "born": 1930},
        {"name": "Clint Eastwood", "born": 1930},
        {"name": "Morgan Freeman", "born": 1937},
        {"name": "Robin Williams", "born": 1951},
        {"name": "Mike Nichols", "born": 1931},
        {"name": "Ian McKellen", "born": 1939},
        {"name": "Audrey Tautou", "born": 1976},
        {"name": "Paul Bettany", "born": 1971},
        {"name": "Natalie Portman", "born": 1981},
        {"name": "Stephen Rea", "born": 1946},
        {"name": "John Hurt", "born": 1940},
        {"name": "Ben Miles", "born": 1967},
        {"name": "James McTeigue", "born": 1967},
        {"name": "Halle Berry", "born": 1966},
        {"name": "Jim Broadbent", "born": 1949},
        {"name": "Tom Tykwer", "born": 1965},
        {"name": "Michael Clarke Duncan", "born": 1957},
        {"name": "David Morse", "born": 1953},
        {"name": "Sam Rockwell", "born": 1968},
        {"name": "Frank Darabont", "born": 1959},
        {"name": "James Cromwell", "born": 1940},
        {"name": "Jessica Thompson", "born": 1980}
    ],
    "relationships": [
        # The Matrix
        {"from": "Keanu Reeves", "to": "The Matrix", "type": "ACTED_IN", "props": {"roles": ["Neo"]}},
        {"from": "Carrie-Anne Moss", "to": "The Matrix", "type": "ACTED_IN", "props": {"roles": ["Trinity"]}},
        {"from": "Laurence Fishburne", "to": "The Matrix", "type": "ACTED_IN", "props": {"roles": ["Morpheus"]}},
        {"from": "Hugo Weaving", "to": "The Matrix", "type": "ACTED_IN", "props": {"roles": ["Agent Smith"]}},
        {"from": "Emil Eifrem", "to": "The Matrix", "type": "ACTED_IN", "props": {"roles": ["Emil"]}},
        {"from": "Lana Wachowski", "to": "The Matrix", "type": "DIRECTED", "props": {}},
        {"from": "Lilly Wachowski", "to": "The Matrix", "type": "DIRECTED", "props": {}},
        {"from": "Joel Silver", "to": "The Matrix", "type": "PRODUCED", "props": {}},
        {"from": "Jessica Thompson", "to": "The Matrix", "type": "REVIEWED", "props": {"rating": 95, "summary": "An extraordinary sci-fi mind-bender"}},

        # The Matrix Reloaded
        {"from": "Keanu Reeves", "to": "The Matrix Reloaded", "type": "ACTED_IN", "props": {"roles": ["Neo"]}},
        {"from": "Carrie-Anne Moss", "to": "The Matrix Reloaded", "type": "ACTED_IN", "props": {"roles": ["Trinity"]}},
        {"from": "Laurence Fishburne", "to": "The Matrix Reloaded", "type": "ACTED_IN", "props": {"roles": ["Morpheus"]}},
        {"from": "Hugo Weaving", "to": "The Matrix Reloaded", "type": "ACTED_IN", "props": {"roles": ["Agent Smith"]}},
        {"from": "Lana Wachowski", "to": "The Matrix Reloaded", "type": "DIRECTED", "props": {}},
        {"from": "Lilly Wachowski", "to": "The Matrix Reloaded", "type": "DIRECTED", "props": {}},
        {"from": "Joel Silver", "to": "The Matrix Reloaded", "type": "PRODUCED", "props": {}},

        # The Matrix Revolutions
        {"from": "Keanu Reeves", "to": "The Matrix Revolutions", "type": "ACTED_IN", "props": {"roles": ["Neo"]}},
        {"from": "Carrie-Anne Moss", "to": "The Matrix Revolutions", "type": "ACTED_IN", "props": {"roles": ["Trinity"]}},
        {"from": "Laurence Fishburne", "to": "The Matrix Revolutions", "type": "ACTED_IN", "props": {"roles": ["Morpheus"]}},
        {"from": "Hugo Weaving", "to": "The Matrix Revolutions", "type": "ACTED_IN", "props": {"roles": ["Agent Smith"]}},
        {"from": "Lana Wachowski", "to": "The Matrix Revolutions", "type": "DIRECTED", "props": {}},
        {"from": "Lilly Wachowski", "to": "The Matrix Revolutions", "type": "DIRECTED", "props": {}},
        {"from": "Joel Silver", "to": "The Matrix Revolutions", "type": "PRODUCED", "props": {}},

        # The Devil's Advocate
        {"from": "Keanu Reeves", "to": "The Devil's Advocate", "type": "ACTED_IN", "props": {"roles": ["Kevin Lomax"]}},
        {"from": "Charlize Theron", "to": "The Devil's Advocate", "type": "ACTED_IN", "props": {"roles": ["Mary Ann Lomax"]}},
        {"from": "Al Pacino", "to": "The Devil's Advocate", "type": "ACTED_IN", "props": {"roles": ["John Milton"]}},
        {"from": "Taylor Hackford", "to": "The Devil's Advocate", "type": "DIRECTED", "props": {}},

        # A Few Good Men
        {"from": "Tom Cruise", "to": "A Few Good Men", "type": "ACTED_IN", "props": {"roles": ["Lt. Daniel Kaffee"]}},
        {"from": "Jack Nicholson", "to": "A Few Good Men", "type": "ACTED_IN", "props": {"roles": ["Col. Nathan R. Jessep"]}},
        {"from": "Demi Moore", "to": "A Few Good Men", "type": "ACTED_IN", "props": {"roles": ["Lt. Cdr. JoAnne Galloway"]}},
        {"from": "Kevin Bacon", "to": "A Few Good Men", "type": "ACTED_IN", "props": {"roles": ["Capt. Jack Challee"]}},
        {"from": "Kiefer Sutherland", "to": "A Few Good Men", "type": "ACTED_IN", "props": {"roles": ["Lt. Jonathan Kendrick"]}},
        {"from": "Noah Wyle", "to": "A Few Good Men", "type": "ACTED_IN", "props": {"roles": ["Cpl. Jeffrey Barnes"]}},
        {"from": "Cuba Gooding Jr.", "to": "A Few Good Men", "type": "ACTED_IN", "props": {"roles": ["Cpl. Carl Hammaker"]}},
        {"from": "Kevin Pollak", "to": "A Few Good Men", "type": "ACTED_IN", "props": {"roles": ["Lt. Sam Weinberg"]}},
        {"from": "Rob Reiner", "to": "A Few Good Men", "type": "DIRECTED", "props": {}},
        {"from": "Aaron Sorkin", "to": "A Few Good Men", "type": "WROTE", "props": {}},
        {"from": "Aaron Sorkin", "to": "A Few Good Men", "type": "ACTED_IN", "props": {"roles": ["Man in Bar"]}},

        # Top Gun
        {"from": "Tom Cruise", "to": "Top Gun", "type": "ACTED_IN", "props": {"roles": ["Maverick"]}},
        {"from": "Kelly McGillis", "to": "Top Gun", "type": "ACTED_IN", "props": {"roles": ["Charlie"]}},
        {"from": "Val Kilmer", "to": "Top Gun", "type": "ACTED_IN", "props": {"roles": ["Iceman"]}},
        {"from": "Anthony Edwards", "to": "Top Gun", "type": "ACTED_IN", "props": {"roles": ["Goose"]}},
        {"from": "Tom Skerritt", "to": "Top Gun", "type": "ACTED_IN", "props": {"roles": ["Viper"]}},
        {"from": "Meg Ryan", "to": "Top Gun", "type": "ACTED_IN", "props": {"roles": ["Carole"]}},
        {"from": "Tony Scott", "to": "Top Gun", "type": "DIRECTED", "props": {}},
        {"from": "Jim Cash", "to": "Top Gun", "type": "WROTE", "props": {}},

        # Jerry Maguire
        {"from": "Tom Cruise", "to": "Jerry Maguire", "type": "ACTED_IN", "props": {"roles": ["Jerry Maguire"]}},
        {"from": "Cuba Gooding Jr.", "to": "Jerry Maguire", "type": "ACTED_IN", "props": {"roles": ["Rod Tidwell"]}},
        {"from": "Renee Zellweger", "to": "Jerry Maguire", "type": "ACTED_IN", "props": {"roles": ["Dorothy Boyd"]}},
        {"from": "Kelly Preston", "to": "Jerry Maguire", "type": "ACTED_IN", "props": {"roles": ["Avery Bishop"]}},
        {"from": "Jerry O'Connell", "to": "Jerry Maguire", "type": "ACTED_IN", "props": {"roles": ["Frank Cushman"]}},
        {"from": "Jay Mohr", "to": "Jerry Maguire", "type": "ACTED_IN", "props": {"roles": ["Bob Sugar"]}},
        {"from": "Bonnie Hunt", "to": "Jerry Maguire", "type": "ACTED_IN", "props": {"roles": ["Laurel Boyd"]}},
        {"from": "Regina King", "to": "Jerry Maguire", "type": "ACTED_IN", "props": {"roles": ["Marcee Tidwell"]}},
        {"from": "Jonathan Lipnicki", "to": "Jerry Maguire", "type": "ACTED_IN", "props": {"roles": ["Ray Boyd"]}},
        {"from": "Cameron Crowe", "to": "Jerry Maguire", "type": "DIRECTED", "props": {}},
        {"from": "Cameron Crowe", "to": "Jerry Maguire", "type": "WROTE", "props": {}},

        # Stand By Me
        {"from": "Wil Wheaton", "to": "Stand By Me", "type": "ACTED_IN", "props": {"roles": ["Gordie Lachance"]}},
        {"from": "River Phoenix", "to": "Stand By Me", "type": "ACTED_IN", "props": {"roles": ["Chris Chambers"]}},
        {"from": "Jerry O'Connell", "to": "Stand By Me", "type": "ACTED_IN", "props": {"roles": ["Vern Tessio"]}},
        {"from": "Corey Feldman", "to": "Stand By Me", "type": "ACTED_IN", "props": {"roles": ["Teddy Duchamp"]}},
        {"from": "John Cusack", "to": "Stand By Me", "type": "ACTED_IN", "props": {"roles": ["Denny Lachance"]}},
        {"from": "Kiefer Sutherland", "to": "Stand By Me", "type": "ACTED_IN", "props": {"roles": ["Ace Merrill"]}},
        {"from": "Rob Reiner", "to": "Stand By Me", "type": "DIRECTED", "props": {}},

        # Apollo 13
        {"from": "Tom Hanks", "to": "Apollo 13", "type": "ACTED_IN", "props": {"roles": ["Jim Lovell"]}},
        {"from": "Kevin Bacon", "to": "Apollo 13", "type": "ACTED_IN", "props": {"roles": ["Jack Swigert"]}},
        {"from": "Bill Paxton", "to": "Apollo 13", "type": "ACTED_IN", "props": {"roles": ["Fred Haise"]}},
        {"from": "Gary Sinise", "to": "Apollo 13", "type": "ACTED_IN", "props": {"roles": ["Ken Mattingly"]}},
        {"from": "Ed Harris", "to": "Apollo 13", "type": "ACTED_IN", "props": {"roles": ["Gene Kranz"]}},
        {"from": "Ron Howard", "to": "Apollo 13", "type": "DIRECTED", "props": {}},

        # Cast Away
        {"from": "Tom Hanks", "to": "Cast Away", "type": "ACTED_IN", "props": {"roles": ["Chuck Noland"]}},
        {"from": "Helen Hunt", "to": "Cast Away", "type": "ACTED_IN", "props": {"roles": ["Kelly Frears"]}},
        {"from": "Robert Zemeckis", "to": "Cast Away", "type": "DIRECTED", "props": {}},

        # You've Got Mail
        {"from": "Tom Hanks", "to": "You've Got Mail", "type": "ACTED_IN", "props": {"roles": ["Joe Fox"]}},
        {"from": "Meg Ryan", "to": "You've Got Mail", "type": "ACTED_IN", "props": {"roles": ["Kathleen Kelly"]}},
        {"from": "Greg Kinnear", "to": "You've Got Mail", "type": "ACTED_IN", "props": {"roles": ["Frank Navasky"]}},
        {"from": "Steve Zahn", "to": "You've Got Mail", "type": "ACTED_IN", "props": {"roles": ["George Pappas"]}},
        {"from": "Dave Chappelle", "to": "You've Got Mail", "type": "ACTED_IN", "props": {"roles": ["Kevin Jackson"]}},
        {"from": "Parker Posey", "to": "You've Got Mail", "type": "ACTED_IN", "props": {"roles": ["Patricia Eden"]}},
        {"from": "Nora Ephron", "to": "You've Got Mail", "type": "DIRECTED", "props": {}},
        {"from": "Nora Ephron", "to": "You've Got Mail", "type": "WROTE", "props": {}},
        {"from": "Jessica Thompson", "to": "You've Got Mail", "type": "REVIEWED", "props": {"rating": 82, "summary": "Fun romantic chemistry between Hanks and Ryan"}},

        # Sleepless in Seattle
        {"from": "Tom Hanks", "to": "Sleepless in Seattle", "type": "ACTED_IN", "props": {"roles": ["Sam Baldwin"]}},
        {"from": "Meg Ryan", "to": "Sleepless in Seattle", "type": "ACTED_IN", "props": {"roles": ["Annie Reed"]}},
        {"from": "Bill Pullman", "to": "Sleepless in Seattle", "type": "ACTED_IN", "props": {"roles": ["Walter"]}},
        {"from": "Rita Wilson", "to": "Sleepless in Seattle", "type": "ACTED_IN", "props": {"roles": ["Suzy"]}},
        {"from": "Rosie O'Donnell", "to": "Sleepless in Seattle", "type": "ACTED_IN", "props": {"roles": ["Becky"]}},
        {"from": "Victor Garber", "to": "Sleepless in Seattle", "type": "ACTED_IN", "props": {"roles": ["Greg"]}},
        {"from": "Nora Ephron", "to": "Sleepless in Seattle", "type": "DIRECTED", "props": {}},
        {"from": "Nora Ephron", "to": "Sleepless in Seattle", "type": "WROTE", "props": {}},

        # Joe Versus the Volcano
        {"from": "Tom Hanks", "to": "Joe Versus the Volcano", "type": "ACTED_IN", "props": {"roles": ["Joe Banks"]}},
        {"from": "Meg Ryan", "to": "Joe Versus the Volcano", "type": "ACTED_IN", "props": {"roles": ["DeDe", "Angelica Graynamore", "Patricia Graynamore"]}},
        {"from": "Nathan Lane", "to": "Joe Versus the Volcano", "type": "ACTED_IN", "props": {"roles": ["Baw"]}},
        {"from": "John Patrick Shanley", "to": "Joe Versus the Volcano", "type": "DIRECTED", "props": {}},

        # When Harry Met Sally
        {"from": "Billy Crystal", "to": "When Harry Met Sally", "type": "ACTED_IN", "props": {"roles": ["Harry Burns"]}},
        {"from": "Meg Ryan", "to": "When Harry Met Sally", "type": "ACTED_IN", "props": {"roles": ["Sally Albright"]}},
        {"from": "Carrie Fisher", "to": "When Harry Met Sally", "type": "ACTED_IN", "props": {"roles": ["Marie"]}},
        {"from": "Bruno Kirby", "to": "When Harry Met Sally", "type": "ACTED_IN", "props": {"roles": ["Jess"]}},
        {"from": "Rob Reiner", "to": "When Harry Met Sally", "type": "DIRECTED", "props": {}},
        {"from": "Nora Ephron", "to": "When Harry Met Sally", "type": "WROTE", "props": {}},

        # That Thing You Do
        {"from": "Tom Hanks", "to": "That Thing You Do", "type": "ACTED_IN", "props": {"roles": ["Mr. White"]}},
        {"from": "Liv Tyler", "to": "That Thing You Do", "type": "ACTED_IN", "props": {"roles": ["Faye Dolan"]}},
        {"from": "Charlize Theron", "to": "That Thing You Do", "type": "ACTED_IN", "props": {"roles": ["Tina"]}},
        {"from": "Tom Hanks", "to": "That Thing You Do", "type": "DIRECTED", "props": {}},
        {"from": "Tom Hanks", "to": "That Thing You Do", "type": "WROTE", "props": {}},

        # The Replacements
        {"from": "Keanu Reeves", "to": "The Replacements", "type": "ACTED_IN", "props": {"roles": ["Shane Falco"]}},
        {"from": "Brooke Langton", "to": "The Replacements", "type": "ACTED_IN", "props": {"roles": ["Annabelle Farrell"]}},
        {"from": "Gene Hackman", "to": "The Replacements", "type": "ACTED_IN", "props": {"roles": ["Jimmy McGinty"]}},
        {"from": "Orlando Jones", "to": "The Replacements", "type": "ACTED_IN", "props": {"roles": ["Clifford Franklin"]}},
        {"from": "Howard Deutch", "to": "The Replacements", "type": "DIRECTED", "props": {}},

        # Unforgiven
        {"from": "Clint Eastwood", "to": "Unforgiven", "type": "ACTED_IN", "props": {"roles": ["Bill Munny"]}},
        {"from": "Gene Hackman", "to": "Unforgiven", "type": "ACTED_IN", "props": {"roles": ["Little Bill Daggett"]}},
        {"from": "Morgan Freeman", "to": "Unforgiven", "type": "ACTED_IN", "props": {"roles": ["Ned Logan"]}},
        {"from": "Richard Harris", "to": "Unforgiven", "type": "ACTED_IN", "props": {"roles": ["English Bob"]}},
        {"from": "Clint Eastwood", "to": "Unforgiven", "type": "DIRECTED", "props": {}},

        # The Birdcage
        {"from": "Robin Williams", "to": "The Birdcage", "type": "ACTED_IN", "props": {"roles": ["Armand Goldman"]}},
        {"from": "Nathan Lane", "to": "The Birdcage", "type": "ACTED_IN", "props": {"roles": ["Albert Goldman"]}},
        {"from": "Gene Hackman", "to": "The Birdcage", "type": "ACTED_IN", "props": {"roles": ["Sen. Kevin Keeley"]}},
        {"from": "Mike Nichols", "to": "The Birdcage", "type": "DIRECTED", "props": {}},

        # The Da Vinci Code
        {"from": "Tom Hanks", "to": "The Da Vinci Code", "type": "ACTED_IN", "props": {"roles": ["Dr. Robert Langdon"]}},
        {"from": "Ian McKellen", "to": "The Da Vinci Code", "type": "ACTED_IN", "props": {"roles": ["Sir Leigh Teabing"]}},
        {"from": "Audrey Tautou", "to": "The Da Vinci Code", "type": "ACTED_IN", "props": {"roles": ["Sophie Neveu"]}},
        {"from": "Paul Bettany", "to": "The Da Vinci Code", "type": "ACTED_IN", "props": {"roles": ["Silas"]}},
        {"from": "Ron Howard", "to": "The Da Vinci Code", "type": "DIRECTED", "props": {}},

        # V for Vendetta
        {"from": "Hugo Weaving", "to": "V for Vendetta", "type": "ACTED_IN", "props": {"roles": ["V"]}},
        {"from": "Natalie Portman", "to": "V for Vendetta", "type": "ACTED_IN", "props": {"roles": ["Evey Hammond"]}},
        {"from": "Stephen Rea", "to": "V for Vendetta", "type": "ACTED_IN", "props": {"roles": ["Eric Finch"]}},
        {"from": "John Hurt", "to": "V for Vendetta", "type": "ACTED_IN", "props": {"roles": ["Adam Sutler"]}},
        {"from": "Ben Miles", "to": "V for Vendetta", "type": "ACTED_IN", "props": {"roles": ["Dascomb"]}},
        {"from": "James McTeigue", "to": "V for Vendetta", "type": "DIRECTED", "props": {}},
        {"from": "Lana Wachowski", "to": "V for Vendetta", "type": "WROTE", "props": {}},
        {"from": "Lilly Wachowski", "to": "V for Vendetta", "type": "WROTE", "props": {}},
        {"from": "Joel Silver", "to": "V for Vendetta", "type": "PRODUCED", "props": {}},

        # Cloud Atlas
        {"from": "Tom Hanks", "to": "Cloud Atlas", "type": "ACTED_IN", "props": {"roles": ["Zachry", "Dr. Henry Goose", "Isaac Sachs", "Dermot Hoggins"]}},
        {"from": "Hugo Weaving", "to": "Cloud Atlas", "type": "ACTED_IN", "props": {"roles": ["Bill Smoke", "Haskell Moore", "Tadeusz Kesselring", "Nurse Noakes", "Boardman Mephi", "Old Georgie"]}},
        {"from": "Halle Berry", "to": "Cloud Atlas", "type": "ACTED_IN", "props": {"roles": ["Luisa Rey", "Jocasta Ayrs", "Ovid", "Meronym"]}},
        {"from": "Jim Broadbent", "to": "Cloud Atlas", "type": "ACTED_IN", "props": {"roles": ["Vyvyan Ayrs", "Captain Molyneux", "Timothy Cavendish"]}},
        {"from": "Tom Tykwer", "to": "Cloud Atlas", "type": "DIRECTED", "props": {}},
        {"from": "Lana Wachowski", "to": "Cloud Atlas", "type": "DIRECTED", "props": {}},
        {"from": "Lilly Wachowski", "to": "Cloud Atlas", "type": "DIRECTED", "props": {}},

        # The Green Mile
        {"from": "Tom Hanks", "to": "The Green Mile", "type": "ACTED_IN", "props": {"roles": ["Paul Edgecomb"]}},
        {"from": "Michael Clarke Duncan", "to": "The Green Mile", "type": "ACTED_IN", "props": {"roles": ["John Coffey"]}},
        {"from": "David Morse", "to": "The Green Mile", "type": "ACTED_IN", "props": {"roles": ["Brutus 'Brutal' Howell"]}},
        {"from": "Bonnie Hunt", "to": "The Green Mile", "type": "ACTED_IN", "props": {"roles": ["Jan Edgecomb"]}},
        {"from": "James Cromwell", "to": "The Green Mile", "type": "ACTED_IN", "props": {"roles": ["Warden Hal Moores"]}},
        {"from": "Sam Rockwell", "to": "The Green Mile", "type": "ACTED_IN", "props": {"roles": ["'Wild Bill' Wharton"]}},
        {"from": "Gary Sinise", "to": "The Green Mile", "type": "ACTED_IN", "props": {"roles": ["Burt Hammersmith"]}},
        {"from": "Frank Darabont", "to": "The Green Mile", "type": "DIRECTED", "props": {}},
        {"from": "James Cromwell", "to": "The Green Mile", "type": "REVIEWED", "props": {"rating": 95, "summary": "Greatest prison movie ever made"}},
        {"from": "Jessica Thompson", "to": "The Green Mile", "type": "REVIEWED", "props": {"rating": 90, "summary": "Heartbreaking and magical masterclass"}}
    ]
}
