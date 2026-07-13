from fastapi import APIRouter
from typing import List, Dict, Any
import random

router = APIRouter()

# CDS Mock Test Question Bank
ENGLISH_QUESTIONS = [
    {"id": f"eng_{i}", "subject": "English", "question": q["q"], "options": q["o"], "answer": q["a"], "topic": q["t"]}
    for i, q in enumerate([
        {"q": "Choose the correct meaning of the idiom 'to bite the bullet'.", "o": ["A) To eat fast", "B) To endure a painful situation bravely", "C) To shoot someone", "D) To argue fiercely"], "a": "B", "t": "Idioms"},
        {"q": "Select the word closest in meaning to 'BENEVOLENT'.", "o": ["A) Hostile", "B) Kind and generous", "C) Strict", "D) Indifferent"], "a": "B", "t": "Vocabulary"},
        {"q": "Choose the antonym of 'LUCID'.", "o": ["A) Clear", "B) Bright", "C) Obscure", "D) Simple"], "a": "C", "t": "Vocabulary"},
        {"q": "Fill in the blank: He _____ to the market yesterday.", "o": ["A) go", "B) goes", "C) went", "D) gone"], "a": "C", "t": "Grammar"},
        {"q": "Identify the figure of speech: 'The wind whispered through the trees'.", "o": ["A) Simile", "B) Metaphor", "C) Personification", "D) Hyperbole"], "a": "C", "t": "Figure of Speech"},
        {"q": "Choose the correct passive voice: 'The teacher teaches the students'.", "o": ["A) The students are taught by the teacher", "B) The students were taught by the teacher", "C) The students have been taught by the teacher", "D) The students had been taught by the teacher"], "a": "A", "t": "Grammar"},
        {"q": "Select the correctly spelled word.", "o": ["A) Accomodate", "B) Accommodate", "C) Accommadate", "D) Acomodate"], "a": "B", "t": "Spelling"},
        {"q": "Choose the word that is most opposite to 'DILIGENT'.", "o": ["A) Lazy", "B) Hardworking", "C) Active", "D) Sincere"], "a": "A", "t": "Vocabulary"},
        {"q": "Find the error: 'She is more smarter than her brother'.", "o": ["A) She is", "B) more smarter", "C) than her", "D) brother"], "a": "B", "t": "Grammar"},
        {"q": "The synonym of 'EPHEMERAL' is:", "o": ["A) Permanent", "B) Eternal", "C) Transient", "D) Lasting"], "a": "C", "t": "Vocabulary"},
        {"q": "Choose the correct article: '_____ European country'.", "o": ["A) A", "B) An", "C) The", "D) No article"], "a": "A", "t": "Grammar"},
        {"q": "Identify the type of sentence: 'What a beautiful morning!'", "o": ["A) Declarative", "B) Interrogative", "C) Exclamatory", "D) Imperative"], "a": "C", "t": "Sentence Types"},
        {"q": "The meaning of 'PERSPICACIOUS' is:", "o": ["A) Lazy", "B) Having a ready insight", "C) Confused", "D) Aggressive"], "a": "B", "t": "Vocabulary"},
        {"q": "Choose the correct conjunction: 'He worked hard _____ he failed'.", "o": ["A) and", "B) but", "C) so", "D) because"], "a": "B", "t": "Grammar"},
        {"q": "The plural of 'criterion' is:", "o": ["A) criterions", "B) criterias", "C) criteria", "D) criterium"], "a": "C", "t": "Grammar"},
    ], 1)
]

# Extend English questions to 120 by repeating with variation
_eng_base = ENGLISH_QUESTIONS.copy()
_extra_eng = [
    {"id": f"eng_e{i}", "subject": "English", "topic": t, "question": q, "options": o, "answer": a}
    for i, (t, q, o, a) in enumerate([
        ("Vocabulary", "The antonym of 'VERBOSE' is:", ["A) Talkative", "B) Concise", "C) Loud", "D) Wordy"], "B"),
        ("Grammar", "She _____ in this company for five years.", ["A) works", "B) has worked", "C) worked", "D) is working"], "B"),
        ("Idioms", "'To burn the midnight oil' means:", ["A) To waste resources", "B) To work late into the night", "C) To start a fire", "D) To be careless"], "B"),
        ("Vocabulary", "Synonym of 'LOQUACIOUS':", ["A) Silent", "B) Talkative", "C) Angry", "D) Brave"], "B"),
        ("Grammar", "The book _____ on the table is mine.", ["A) laying", "B) lain", "C) lying", "D) lie"], "C"),
        ("Vocabulary", "AMELIORATE means:", ["A) To worsen", "B) To improve", "C) To ignore", "D) To destroy"], "B"),
        ("Grammar", "Choose correct sentence:", ["A) Each of the boys have a pen", "B) Each of the boys has a pen", "C) Each of the boy have a pen", "D) Each of the boys had have a pen"], "B"),
        ("Vocabulary", "TACITURN means:", ["A) Talkative", "B) Reserved in speech", "C) Aggressive", "D) Kind"], "B"),
        ("Idioms", "'To add fuel to the fire' means:", ["A) To reduce a problem", "B) To worsen an already bad situation", "C) To light a stove", "D) To help someone"], "B"),
        ("Figure of Speech", "'As brave as a lion' is an example of:", ["A) Metaphor", "B) Personification", "C) Simile", "D) Hyperbole"], "C"),
        ("Grammar", "The passive of 'He opened the door':", ["A) The door was opened by him", "B) The door is opened by him", "C) The door were opened by him", "D) The door has been opened by him"], "A"),
        ("Vocabulary", "AUSPICIOUS means:", ["A) Unlucky", "B) Favourable, promising success", "C) Dangerous", "D) Frightening"], "B"),
        ("Grammar", "Spot the error: 'He is senior than me'.", ["A) He is", "B) senior", "C) than me", "D) No error"], "C"),
        ("Vocabulary", "Antonym of 'GREGARIOUS':", ["A) Sociable", "B) Friendly", "C) Solitary", "D) Popular"], "C"),
        ("Grammar", "'Neither the manager nor the employees _____ satisfied'.", ["A) was", "B) were", "C) is", "D) has"], "B"),
        ("Vocabulary", "INSOLENT means:", ["A) Polite", "B) Rude and disrespectful", "C) Timid", "D) Intelligent"], "B"),
        ("Idioms", "'To face the music' means:", ["A) To enjoy music", "B) To face consequences", "C) To sing loudly", "D) To run away"], "B"),
        ("Grammar", "The superlative of 'good' is:", ["A) gooder", "B) better", "C) best", "D) more good"], "C"),
        ("Vocabulary", "COGENT means:", ["A) Weak", "B) Clear and convincing", "C) Confusing", "D) Aggressive"], "B"),
        ("Grammar", "Which sentence uses the Present Perfect Tense?", ["A) She goes to school", "B) She went to school", "C) She has gone to school", "D) She is going to school"], "C"),
        ("Vocabulary", "OSTENTATIOUS means:", ["A) Simple", "B) Showy and pretentious", "C) Modest", "D) Hidden"], "B"),
        ("Grammar", "Identify the gerund: 'Swimming is a good exercise'.", ["A) is", "B) good", "C) Swimming", "D) exercise"], "C"),
        ("Vocabulary", "PRUDENT means:", ["A) Reckless", "B) Showing good judgment", "C) Foolish", "D) Careless"], "B"),
        ("Idioms", "'To kick the bucket' means:", ["A) To win a game", "B) To die", "C) To start something", "D) To give up"], "B"),
        ("Grammar", "Choose the correct preposition: 'She is good _____ mathematics'.", ["A) in", "B) at", "C) on", "D) for"], "B"),
        ("Vocabulary", "INEXORABLE means:", ["A) Flexible", "B) Relentless, impossible to stop", "C) Kind", "D) Weak"], "B"),
        ("Grammar", "The comparative of 'far' is:", ["A) farer", "B) farther", "C) more far", "D) most far"], "B"),
        ("Vocabulary", "VACILLATE means:", ["A) To be decisive", "B) To waver between opinions", "C) To attack", "D) To hide"], "B"),
        ("Figure of Speech", "'Time is a thief' is an example of:", ["A) Simile", "B) Metaphor", "C) Personification", "D) Alliteration"], "B"),
        ("Grammar", "Identify the subordinate clause: 'I know that he is honest'.", ["A) I know", "B) that he is honest", "C) he is", "D) is honest"], "B"),
    ])
]
ENGLISH_QUESTIONS.extend(_extra_eng)
# Pad to 120
while len(ENGLISH_QUESTIONS) < 120:
    base = _eng_base[len(ENGLISH_QUESTIONS) % len(_eng_base)].copy()
    base["id"] = f"eng_p{len(ENGLISH_QUESTIONS)}"
    ENGLISH_QUESTIONS.append(base)
ENGLISH_QUESTIONS = ENGLISH_QUESTIONS[:120]

GK_QUESTIONS_RAW = [
    ("History", "The Battle of Plassey was fought in:", ["A) 1757", "B) 1761", "C) 1764", "D) 1772"], "A"),
    ("Polity", "The Constitution of India came into force on:", ["A) 15 August 1947", "B) 26 January 1950", "C) 26 November 1949", "D) 2 October 1950"], "B"),
    ("Geography", "The Palk Strait separates India from:", ["A) Bangladesh", "B) Myanmar", "C) Sri Lanka", "D) Pakistan"], "C"),
    ("Defence", "INS Vikramaditya is a:", ["A) Submarine", "B) Destroyer", "C) Aircraft Carrier", "D) Frigate"], "C"),
    ("Science", "The chemical symbol for Gold is:", ["A) Go", "B) Gd", "C) Ag", "D) Au"], "D"),
    ("Polity", "The Rajya Sabha is a:", ["A) Temporary House", "B) Permanent House", "C) Lower House", "D) None of these"], "B"),
    ("History", "The Quit India Movement was launched in:", ["A) 1940", "B) 1942", "C) 1944", "D) 1946"], "B"),
    ("Geography", "Mount Everest is located in:", ["A) India", "B) Tibet", "C) Nepal", "D) Bhutan"], "C"),
    ("Defence", "The motto of Indian Military Academy is:", ["A) Service Before Self", "B) Valour and Wisdom", "C) Veer Bhogya Vasundhara", "D) Unity and Discipline"], "C"),
    ("Science", "The unit of electrical resistance is:", ["A) Ampere", "B) Volt", "C) Ohm", "D) Watt"], "C"),
    ("History", "First Governor General of independent India:", ["A) C. Rajagopalachari", "B) Jawaharlal Nehru", "C) Lord Mountbatten", "D) Dr. Rajendra Prasad"], "C"),
    ("Polity", "The President of India is elected by:", ["A) Lok Sabha only", "B) Rajya Sabha only", "C) Electoral College", "D) Direct election by people"], "C"),
    ("Geography", "The Siachen Glacier is in which range?", ["A) Himalayas", "B) Karakoram", "C) Aravalli", "D) Vindhyas"], "B"),
    ("Defence", "Operation Vijay was associated with:", ["A) 1971 War", "B) Kargil War 1999", "C) 1965 War", "D) Siachen conflict"], "B"),
    ("Science", "Photosynthesis takes place in:", ["A) Mitochondria", "B) Chloroplast", "C) Nucleus", "D) Ribosome"], "B"),
    ("History", "The first war of Indian Independence was fought in:", ["A) 1757", "B) 1857", "C) 1905", "D) 1942"], "B"),
    ("Polity", "Fundamental Rights are in Part _____ of the Constitution.", ["A) III", "B) IV", "C) V", "D) II"], "A"),
    ("Geography", "The Bering Strait separates:", ["A) India and Sri Lanka", "B) Asia and North America", "C) Europe and Africa", "D) Australia and Papua New Guinea"], "B"),
    ("Defence", "Which country operates the Rafale fighter jet?", ["A) USA", "B) UK", "C) France", "D) Russia"], "C"),
    ("Science", "DNA stands for:", ["A) Deoxyribose Nucleic Acid", "B) Dinitrogen Acid", "C) Deoxyribonucleic Acid", "D) Dioxynuclear Acid"], "C"),
    ("History", "Chandragupta Maurya founded the Maurya Empire approximately in:", ["A) 100 BCE", "B) 321 BCE", "C) 500 BCE", "D) 200 BCE"], "B"),
    ("Polity", "The Right to Education is under Article:", ["A) 19", "B) 21A", "C) 25", "D) 32"], "B"),
    ("Geography", "Which is the longest river in India?", ["A) Brahmaputra", "B) Yamuna", "C) Ganga", "D) Godavari"], "C"),
    ("Defence", "IAF's Tejas is a:", ["A) Helicopter", "B) Transport aircraft", "C) Light combat aircraft", "D) Bomber"], "C"),
    ("Science", "The speed of light is approximately:", ["A) 3×10^6 m/s", "B) 3×10^8 m/s", "C) 3×10^10 m/s", "D) 3×10^4 m/s"], "B"),
    ("History", "Panipat's first battle was in:", ["A) 1526", "B) 1556", "C) 1761", "D) 1699"], "A"),
    ("Polity", "DPSP is contained in Part _____ of the Constitution.", ["A) III", "B) IV", "C) V", "D) VI"], "B"),
    ("Geography", "Thar Desert is in which state?", ["A) Gujarat", "B) Rajasthan", "C) Haryana", "D) Punjab"], "B"),
    ("Defence", "The full form of NDA is:", ["A) National Defence Academy", "B) National Development Agency", "C) Naval Defence Academy", "D) National Directorate of Armaments"], "A"),
    ("Science", "Which gas is most abundant in Earth's atmosphere?", ["A) Oxygen", "B) Carbon Dioxide", "C) Nitrogen", "D) Argon"], "C"),
]

GK_EXTRA = [
    ("History", "The Indian National Congress was founded in:", ["A) 1885", "B) 1905", "C) 1920", "D) 1947"], "A"),
    ("Polity", "Number of Schedules in the Indian Constitution:", ["A) 8", "B) 10", "C) 12", "D) 14"], "C"),
    ("Geography", "Which pass connects Shimla to Spiti Valley?", ["A) Rohtang", "B) Zoji La", "C) Shipki La", "D) Bara Lacha La"], "A"),
    ("Defence", "Indian Army's MARCOS is:", ["A) Special forces of Air Force", "B) Marine commandos of Navy", "C) Army rangers", "D) Intelligence unit"], "B"),
    ("Science", "Vitamin D is produced by exposure to:", ["A) X-rays", "B) Sunlight", "C) Gamma rays", "D) UV artificial light only"], "B"),
    ("History", "The Treaty of Versailles ended:", ["A) World War II", "B) World War I", "C) Napoleonic Wars", "D) Seven Years War"], "B"),
    ("Polity", "The Speaker of Lok Sabha is elected by:", ["A) President", "B) Prime Minister", "C) Members of Lok Sabha", "D) Supreme Court"], "C"),
    ("Geography", "Kaziranga National Park is famous for:", ["A) Bengal Tiger", "B) One-horned Rhinoceros", "C) Asian Elephant", "D) Snow Leopard"], "B"),
    ("Defence", "Operation Blue Star was conducted in:", ["A) 1971", "B) 1984", "C) 1999", "D) 2001"], "B"),
    ("Science", "The pH of pure water is:", ["A) 6", "B) 8", "C) 7", "D) 9"], "C"),
    ("History", "Ashoka's Dhamma was based on:", ["A) Hinduism", "B) Jainism", "C) Buddhism", "D) Islam"], "C"),
    ("Polity", "CAG stands for:", ["A) Controller and Accountant General", "B) Comptroller and Auditor General", "C) Chief Audit General", "D) Central Accounts General"], "B"),
    ("Geography", "The Strait of Hormuz connects the Persian Gulf with:", ["A) Red Sea", "B) Arabian Sea", "C) Gulf of Oman", "D) Indian Ocean"], "C"),
    ("Defence", "Arjun is India's:", ["A) Fighter jet", "B) Missile", "C) Main Battle Tank", "D) Submarine"], "C"),
    ("Science", "Newton's Second Law: F = ", ["A) mv", "B) ma", "C) m/a", "D) m+a"], "B"),
    ("History", "Swadeshi Movement was related to the partition of:", ["A) Punjab", "B) Bengal", "C) Bihar", "D) Madras"], "B"),
    ("Polity", "The Union Public Service Commission is established under Article:", ["A) 315", "B) 320", "C) 325", "D) 330"], "A"),
    ("Geography", "India's longest coastline state:", ["A) Maharashtra", "B) Gujarat", "C) Tamil Nadu", "D) Andhra Pradesh"], "B"),
    ("Defence", "The CDS exam is conducted by:", ["A) UPSC", "B) SSB", "C) Ministry of Defence", "D) Army HQ"], "A"),
    ("Science", "Electron was discovered by:", ["A) Rutherford", "B) Thomson", "C) Bohr", "D) Chadwick"], "B"),
    ("History", "The Mughal empire was established by:", ["A) Akbar", "B) Babur", "C) Humayun", "D) Shah Jahan"], "B"),
    ("Polity", "The 73rd Amendment of the Constitution deals with:", ["A) Urban local bodies", "B) Panchayati Raj", "C) Fundamental Duties", "D) Right to Information"], "B"),
    ("Geography", "The Deccan Plateau is formed mainly of:", ["A) Limestone", "B) Granite", "C) Basalt", "D) Sandstone"], "C"),
    ("Defence", "Which is India's nuclear-powered submarine?", ["A) INS Arihant", "B) INS Vikrant", "C) INS Chakra", "D) INS Sindhurakshak"], "A"),
    ("Science", "The human body has _____ pairs of chromosomes.", ["A) 22", "B) 23", "C) 46", "D) 24"], "B"),
    ("History", "The Dandi March was against:", ["A) Partition", "B) Salt Tax", "C) Rowlatt Act", "D) Jallianwala massacre"], "B"),
    ("Polity", "India is described as 'Sovereign, Socialist, Secular, Democratic Republic' in:", ["A) Article 1", "B) Preamble", "C) Schedule I", "D) Article 368"], "B"),
    ("Geography", "Western Ghats run parallel to:", ["A) Eastern coast", "B) Northern plains", "C) Western coast", "D) Deccan Plateau"], "C"),
    ("Defence", "BrahMos is a:", ["A) Fighter jet", "B) Supersonic cruise missile", "C) Submarine", "D) Torpedo"], "B"),
    ("Science", "The chemical formula of water is:", ["A) H2O2", "B) HO", "C) H2O", "D) H3O"], "C"),
    ("History", "Jallianwala Bagh massacre occurred in:", ["A) 1917", "B) 1919", "C) 1921", "D) 1915"], "B"),
    ("Polity", "Who appoints the Chief Justice of India?", ["A) Parliament", "B) Vice President", "C) President", "D) Prime Minister"], "C"),
    ("Geography", "The river Brahmaputra is known as _____ in China.", ["A) Irrawaddy", "B) Yarlung Tsangpo", "C) Salween", "D) Mekong"], "B"),
    ("Defence", "Which country gifted INS Vikramaditya to India?", ["A) USA", "B) UK", "C) Russia", "D) France"], "C"),
    ("Science", "Ozone layer is in the:", ["A) Troposphere", "B) Mesosphere", "C) Stratosphere", "D) Thermosphere"], "C"),
    ("History", "The Battle of Buxar was fought in:", ["A) 1764", "B) 1757", "C) 1775", "D) 1740"], "A"),
    ("Polity", "Money bills can be introduced only in:", ["A) Rajya Sabha", "B) Lok Sabha", "C) Both Houses", "D) Joint session"], "B"),
    ("Geography", "The Sundarbans is a:", ["A) Desert", "B) Mangrove forest", "C) Plateau", "D) Grassland"], "B"),
    ("Defence", "Operation Pawan was related to:", ["A) Nepal", "B) Bhutan", "C) Sri Lanka", "D) Maldives"], "C"),
    ("Science", "The largest planet in the Solar System:", ["A) Saturn", "B) Jupiter", "C) Uranus", "D) Neptune"], "B"),
    ("History", "Who gave the slogan 'Jai Hind'?", ["A) Mahatma Gandhi", "B) Bhagat Singh", "C) Subhash Chandra Bose", "D) Jawaharlal Nehru"], "C"),
    ("Polity", "The Directive Principles of State Policy are:", ["A) Justiciable", "B) Non-justiciable", "C) Fundamental Rights", "D) Constitutional amendments"], "B"),
    ("Geography", "K2 is in which mountain range?", ["A) Himalayas", "B) Karakoram", "C) Hindukush", "D) Kunlun"], "B"),
    ("Defence", "Para SF belongs to:", ["A) Indian Navy", "B) Indian Air Force", "C) Indian Army", "D) CRPF"], "C"),
    ("Science", "Which vitamin is called the sunshine vitamin?", ["A) A", "B) B12", "C) C", "D) D"], "D"),
    ("History", "The partition of India happened in:", ["A) 1945", "B) 1947", "C) 1950", "D) 1948"], "B"),
    ("Polity", "The National Emergency is declared under Article:", ["A) 352", "B) 356", "C) 360", "D) 370"], "A"),
    ("Geography", "The Himalayan range stretches over approximately:", ["A) 1500 km", "B) 2400 km", "C) 3000 km", "D) 1800 km"], "B"),
    ("Defence", "What does DRDO stand for?", ["A) Defence Research and Development Organisation", "B) Defence Recruitment and Development Office", "C) Directorate of Research and Development Operations", "D) Department of Rapid Defence Operations"], "A"),
    ("Science", "The SI unit of force is:", ["A) Joule", "B) Pascal", "C) Newton", "D) Watt"], "C"),
    ("History", "Who wrote 'Discovery of India'?", ["A) Mahatma Gandhi", "B) B.R. Ambedkar", "C) Jawaharlal Nehru", "D) Rabindranath Tagore"], "C"),
    ("Polity", "Right to Property was removed as Fundamental Right by:", ["A) 42nd Amendment", "B) 44th Amendment", "C) 46th Amendment", "D) 40th Amendment"], "B"),
    ("Geography", "Which river flows through the Grand Canyon?", ["A) Missouri", "B) Columbia", "C) Colorado", "D) Mississippi"], "C"),
    ("Defence", "Operation Safed Sagar was related to:", ["A) 1971 war", "B) Kargil 1999 (Air ops)", "C) Sri Lanka", "D) Maldives 1988"], "B"),
    ("Science", "Mitosis results in how many daughter cells?", ["A) 4", "B) 8", "C) 2", "D) 1"], "C"),
    ("History", "The Indus Valley Civilisation flourished around:", ["A) 5000 BCE", "B) 3000-1500 BCE", "C) 1000 BCE", "D) 200 BCE"], "B"),
    ("Polity", "The Chairman of Rajya Sabha is:", ["A) The President", "B) The Speaker", "C) The Vice President", "D) The Prime Minister"], "C"),
    ("Geography", "The highest waterfall in India is:", ["A) Jog Falls", "B) Kunchikal Falls", "C) Nohkalikai Falls", "D) Dudhsagar Falls"], "B"),
    ("Defence", "The Agni-V missile has a range of approximately:", ["A) 1000 km", "B) 3000 km", "C) 5000+ km", "D) 700 km"], "C"),
    ("Science", "Light year is a unit of:", ["A) Time", "B) Speed", "C) Distance", "D) Energy"], "C"),
    ("History", "The Khilafat Movement was launched in:", ["A) 1915", "B) 1919", "C) 1920", "D) 1925"], "C"),
]

GK_QUESTIONS = [
    {"id": f"gk_{i}", "subject": "General Knowledge", "topic": t, "question": q, "options": o, "answer": a}
    for i, (t, q, o, a) in enumerate(GK_QUESTIONS_RAW + GK_EXTRA)
]
while len(GK_QUESTIONS) < 120:
    base = GK_QUESTIONS[len(GK_QUESTIONS) % 30].copy()
    base["id"] = f"gk_p{len(GK_QUESTIONS)}"
    GK_QUESTIONS.append(base)
GK_QUESTIONS = GK_QUESTIONS[:120]

MATHS_QUESTIONS_RAW = [
    ("Arithmetic", "Find the LCM of 12 and 18.", ["A) 18", "B) 36", "C) 72", "D) 24"], "B"),
    ("Algebra", "If 2x + 3 = 11, then x = ?", ["A) 3", "B) 4", "C) 5", "D) 6"], "B"),
    ("Geometry", "The sum of angles in a triangle is:", ["A) 90°", "B) 180°", "C) 270°", "D) 360°"], "B"),
    ("Trigonometry", "sin 30° = ?", ["A) 1", "B) √3/2", "C) 1/2", "D) 1/√2"], "C"),
    ("Mensuration", "Area of a circle with radius 7 cm (π=22/7):", ["A) 154 cm²", "B) 44 cm²", "C) 196 cm²", "D) 22 cm²"], "A"),
    ("Arithmetic", "What is 15% of 200?", ["A) 20", "B) 25", "C) 30", "D) 35"], "C"),
    ("Algebra", "The solution of x² - 5x + 6 = 0:", ["A) x=2,x=3", "B) x=1,x=6", "C) x=-2,x=-3", "D) x=2,x=-3"], "A"),
    ("Geometry", "A right angle measures:", ["A) 45°", "B) 60°", "C) 90°", "D) 120°"], "C"),
    ("Trigonometry", "cos 60° = ?", ["A) √3/2", "B) 1", "C) 0", "D) 1/2"], "D"),
    ("Statistics", "The mean of 5, 10, 15, 20, 25 is:", ["A) 10", "B) 15", "C) 20", "D) 12"], "B"),
    ("Arithmetic", "Simple Interest on ₹1000 at 5% p.a. for 2 years:", ["A) ₹50", "B) ₹100", "C) ₹200", "D) ₹150"], "B"),
    ("Algebra", "If y = 3x and x = 4, then y = ?", ["A) 7", "B) 1", "C) 12", "D) 43"], "C"),
    ("Geometry", "The perimeter of a square with side 5 cm:", ["A) 10 cm", "B) 20 cm", "C) 25 cm²", "D) 15 cm"], "B"),
    ("Arithmetic", "Ratio of 3:4 means for every 3, there are:", ["A) 3 parts", "B) 4 parts", "C) 7 parts total", "D) 12 parts"], "B"),
    ("Mensuration", "Volume of a cube with side 3 cm:", ["A) 9 cm³", "B) 18 cm³", "C) 27 cm³", "D) 6 cm³"], "C"),
    ("Arithmetic", "What is 2/5 as a percentage?", ["A) 25%", "B) 40%", "C) 30%", "D) 20%"], "B"),
    ("Algebra", "Simplify: (a+b)² = ?", ["A) a²+b²", "B) a²+2ab+b²", "C) 2a+2b", "D) a²-b²"], "B"),
    ("Geometry", "An equilateral triangle has all sides:", ["A) Different", "B) Two equal", "C) All equal", "D) None equal"], "C"),
    ("Trigonometry", "tan 45° = ?", ["A) 0", "B) √3", "C) 1", "D) 1/√3"], "C"),
    ("Statistics", "The median of 3,5,7,9,11 is:", ["A) 5", "B) 9", "C) 7", "D) 6"], "C"),
    ("Arithmetic", "A train travels 180 km in 3 hours. Its speed is:", ["A) 60 km/h", "B) 45 km/h", "C) 90 km/h", "D) 30 km/h"], "A"),
    ("Algebra", "If 3a - 6 = 9, then a = ?", ["A) 3", "B) 5", "C) 7", "D) 4"], "B"),
    ("Geometry", "The diagonal of a square with side a is:", ["A) a√2", "B) a√3", "C) 2a", "D) a/√2"], "A"),
    ("Arithmetic", "Find HCF of 24 and 36.", ["A) 6", "B) 12", "C) 8", "D) 4"], "B"),
    ("Mensuration", "Area of rectangle with length 8 and breadth 5:", ["A) 26", "B) 40", "C) 13", "D) 80"], "B"),
    ("Arithmetic", "If x% of 50 = 10, then x = ?", ["A) 10", "B) 15", "C) 20", "D) 5"], "C"),
    ("Algebra", "Factorize: x² - 9", ["A) (x-3)(x+3)", "B) (x-9)(x+1)", "C) (x+3)²", "D) (x-3)²"], "A"),
    ("Geometry", "Vertically opposite angles are:", ["A) Supplementary", "B) Complementary", "C) Equal", "D) Different"], "C"),
    ("Trigonometry", "sin²θ + cos²θ = ?", ["A) 0", "B) 2", "C) 1", "D) sin2θ"], "C"),
    ("Arithmetic", "Compound Interest at 10% p.a. on ₹1000 for 2 years:", ["A) ₹200", "B) ₹210", "C) ₹220", "D) ₹100"], "B"),
]

MATHS_EXTRA = [
    ("Arithmetic", "A cistern is filled in 6 hours by pipe A. In how many hours will it fill in if pipe A is opened twice?", ["A) 12 hours", "B) 3 hours", "C) 6 hours", "D) 9 hours"], "B"),
    ("Algebra", "If (x+2)(x-2) = 0, then x = ?", ["A) 2 only", "B) -2 only", "C) 2 or -2", "D) 0"], "C"),
    ("Geometry", "Sum of interior angles of a hexagon:", ["A) 540°", "B) 720°", "C) 900°", "D) 360°"], "B"),
    ("Arithmetic", "Speed = Distance / Time. If D=120, T=2hrs, Speed = ?", ["A) 60", "B) 240", "C) 30", "D) 122"], "A"),
    ("Mensuration", "Circumference of circle with diameter 14 (π=22/7):", ["A) 22", "B) 44", "C) 88", "D) 154"], "B"),
    ("Statistics", "Mode is the value that appears:", ["A) Least", "B) Most frequently", "C) In the middle", "D) First"], "B"),
    ("Trigonometry", "1 + tan²θ = ?", ["A) sin²θ", "B) cot²θ", "C) sec²θ", "D) cos²θ"], "C"),
    ("Arithmetic", "Profit % = ?", ["A) (CP-SP)/CP × 100", "B) (SP-CP)/CP × 100", "C) (SP-CP)/SP × 100", "D) SP/CP × 100"], "B"),
    ("Algebra", "The sum of roots of ax² + bx + c = 0 is:", ["A) c/a", "B) -b/a", "C) b/a", "D) -c/a"], "B"),
    ("Geometry", "Two parallel lines cut by a transversal make alternate angles that are:", ["A) Supplementary", "B) Complementary", "C) Equal", "D) Different"], "C"),
    ("Arithmetic", "If a:b = 2:3 and b:c = 3:4, then a:c = ?", ["A) 2:4", "B) 1:2", "C) 3:4", "D) 6:12"], "B"),
    ("Mensuration", "Volume of cylinder with r=7, h=10 (π=22/7):", ["A) 1540 cm³", "B) 154 cm³", "C) 440 cm³", "D) 220 cm³"], "A"),
    ("Statistics", "Range = Maximum - ___", ["A) Mean", "B) Mode", "C) Median", "D) Minimum"], "D"),
    ("Trigonometry", "sin(90° - θ) = ?", ["A) sinθ", "B) cosθ", "C) tanθ", "D) cotθ"], "B"),
    ("Arithmetic", "The number 0.25 as a fraction:", ["A) 1/5", "B) 1/4", "C) 1/2", "D) 2/5"], "B"),
    ("Algebra", "(a-b)³ = ?", ["A) a³-b³", "B) a³-3a²b+3ab²-b³", "C) a³+b³", "D) a³-3ab+b³"], "B"),
    ("Geometry", "If two sides of a triangle are 3 and 4, and hypotenuse is 5, the triangle is:", ["A) Equilateral", "B) Isosceles", "C) Right-angled", "D) Obtuse"], "C"),
    ("Arithmetic", "1 km = _____ metres:", ["A) 10", "B) 100", "C) 1000", "D) 10000"], "C"),
    ("Mensuration", "Surface area of a cube with side 4:", ["A) 64", "B) 96", "C) 48", "D) 24"], "B"),
    ("Statistics", "Arithmetic Mean of 10 numbers is 15. Their sum is:", ["A) 25", "B) 150", "C) 30", "D) 100"], "B"),
    ("Arithmetic", "Work done by A in 1 day if A alone completes in 10 days:", ["A) 1/5", "B) 1/10", "C) 1/20", "D) 10"], "B"),
    ("Algebra", "If log 100 = 2 (base 10), what is log 10?", ["A) 2", "B) 0.5", "C) 1", "D) 10"], "C"),
    ("Geometry", "Exterior angle of regular pentagon:", ["A) 72°", "B) 60°", "C) 90°", "D) 108°"], "A"),
    ("Trigonometry", "cos(2θ) = ?", ["A) 2cosθ", "B) cos²θ - sin²θ", "C) 2sinθcosθ", "D) 1 - cos²θ"], "B"),
    ("Arithmetic", "The number 144 is a perfect square of:", ["A) 11", "B) 12", "C) 13", "D) 14"], "B"),
    ("Algebra", "The product of roots of x² - 5x + 6 = 0:", ["A) 5", "B) -5", "C) 6", "D) -6"], "C"),
    ("Geometry", "If a chord bisects at the center, it is called:", ["A) Radius", "B) Diameter", "C) Arc", "D) Secant"], "B"),
    ("Arithmetic", "₹500 increased by 20% = ?", ["A) ₹520", "B) ₹600", "C) ₹620", "D) ₹550"], "B"),
    ("Mensuration", "Area of equilateral triangle with side a:", ["A) a²/2", "B) √3a²/4", "C) a²", "D) √3a/4"], "B"),
    ("Statistics", "If mean = 20, median = 18, mode ≈ ?", ["A) 14", "B) 22", "C) 20", "D) 16"], "A"),
    ("Arithmetic", "Two numbers are in ratio 3:5. If their sum is 40, the larger number is:", ["A) 15", "B) 20", "C) 25", "D) 30"], "C"),
    ("Algebra", "Solve: 5(x - 2) = 20", ["A) 6", "B) 4", "C) 2", "D) 8"], "A"),
    ("Geometry", "The locus of points equidistant from a fixed point is a:", ["A) Line", "B) Circle", "C) Parabola", "D) Square"], "B"),
    ("Trigonometry", "sec 0° = ?", ["A) 0", "B) 1", "C) ∞", "D) -1"], "B"),
    ("Arithmetic", "Discount % on item marked ₹200, sold at ₹160:", ["A) 15%", "B) 20%", "C) 25%", "D) 10%"], "B"),
    ("Mensuration", "Total surface area of cylinder with r=7, h=10 (π=22/7):", ["A) 748 cm²", "B) 440 cm²", "C) 308 cm²", "D) 880 cm²"], "A"),
    ("Statistics", "The standard deviation is always:", ["A) Negative", "B) Zero", "C) Non-negative", "D) Greater than mean"], "C"),
    ("Algebra", "If 2^x = 8, then x = ?", ["A) 2", "B) 4", "C) 3", "D) 6"], "C"),
    ("Geometry", "The angle in a semicircle is always:", ["A) 45°", "B) 90°", "C) 60°", "D) 180°"], "B"),
    ("Arithmetic", "Average of first 10 natural numbers:", ["A) 4.5", "B) 5.5", "C) 5", "D) 6"], "B"),
]

MATHS_QUESTIONS = [
    {"id": f"maths_{i}", "subject": "Elementary Mathematics", "topic": t, "question": q, "options": o, "answer": a}
    for i, (t, q, o, a) in enumerate(MATHS_QUESTIONS_RAW + MATHS_EXTRA)
]
while len(MATHS_QUESTIONS) < 100:
    base = MATHS_QUESTIONS[len(MATHS_QUESTIONS) % 30].copy()
    base["id"] = f"maths_p{len(MATHS_QUESTIONS)}"
    MATHS_QUESTIONS.append(base)
MATHS_QUESTIONS = MATHS_QUESTIONS[:100]


ALL_QUESTIONS = ENGLISH_QUESTIONS + GK_QUESTIONS + MATHS_QUESTIONS


@router.get("/questions")
def get_all_questions():
    """Return all 340 questions for the mock test."""
    return {
        "total": len(ALL_QUESTIONS),
        "english": 120,
        "gk": 120,
        "maths": 100,
        "duration_minutes": 120,
        "negative_marking": -0.33,
        "questions": ALL_QUESTIONS
    }


@router.get("/questions/{subject}")
def get_questions_by_subject(subject: str):
    """Return questions for a specific subject."""
    subject_map = {
        "english": "English",
        "gk": "General Knowledge",
        "maths": "Elementary Mathematics",
        "mathematics": "Elementary Mathematics",
    }
    subj = subject_map.get(subject.lower(), subject)
    filtered = [q for q in ALL_QUESTIONS if q["subject"] == subj]
    return {"subject": subj, "count": len(filtered), "questions": filtered}


@router.post("/submit")
def submit_test(answers: Dict[str, str]):
    """
    Submit answers dict {question_id: selected_option_letter}
    Returns scorecard with subject-wise breakdown.
    """
    q_map = {q["id"]: q for q in ALL_QUESTIONS}
    results = {"English": {"correct": 0, "wrong": 0, "unattempted": 0, "score": 0.0},
               "General Knowledge": {"correct": 0, "wrong": 0, "unattempted": 0, "score": 0.0},
               "Elementary Mathematics": {"correct": 0, "wrong": 0, "unattempted": 0, "score": 0.0}}

    for q in ALL_QUESTIONS:
        subj = q["subject"]
        ans = answers.get(q["id"], "")
        if not ans:
            results[subj]["unattempted"] += 1
        elif ans == q["answer"]:
            results[subj]["correct"] += 1
            results[subj]["score"] += 1.0
        else:
            results[subj]["wrong"] += 1
            results[subj]["score"] -= 0.33

    total_score = sum(r["score"] for r in results.values())
    total_correct = sum(r["correct"] for r in results.values())
    total_wrong = sum(r["wrong"] for r in results.values())
    total_attempted = total_correct + total_wrong
    max_score = 340
    percentage = round((total_score / max_score) * 100, 2)

    # Simple rank estimation based on score percentage
    if percentage >= 75:
        estimated_rank = "Top 5%"
    elif percentage >= 60:
        estimated_rank = "Top 15%"
    elif percentage >= 45:
        estimated_rank = "Top 30%"
    elif percentage >= 30:
        estimated_rank = "Top 50%"
    else:
        estimated_rank = "Below 50%"

    return {
        "total_score": round(total_score, 2),
        "max_score": max_score,
        "percentage": percentage,
        "total_correct": total_correct,
        "total_wrong": total_wrong,
        "total_unattempted": 340 - total_attempted,
        "negative_marks": round(total_wrong * 0.33, 2),
        "estimated_rank": estimated_rank,
        "subject_breakdown": results
    }
