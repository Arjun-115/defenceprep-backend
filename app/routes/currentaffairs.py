from fastapi import APIRouter
from datetime import datetime, date

router = APIRouter()

CURRENT_AFFAIRS = [
    {"id": 1, "date": "2023-01-15", "category": "Defence", "headline": "India commissions INS Mormugao",
     "question": "INS Mormugao is a:", "options": ["A) Nuclear submarine", "B) Stealth guided-missile destroyer", "C) Aircraft carrier", "D) Patrol vessel"],
     "answer": "B", "explanation": "INS Mormugao (D67) is a P15B stealth guided-missile destroyer commissioned in December 2022.", "source": "PIB"},

    {"id": 2, "date": "2023-02-10", "category": "Defence", "headline": "India successfully test-fires Agni-V MIRV",
     "question": "Operation Divyastra refers to:", "options": ["A) ICBM test", "B) Agni-V MIRV test", "C) Naval exercise", "D) Space mission"],
     "answer": "B", "explanation": "Operation Divyastra was the successful test of Agni-V with Multiple Independently Targetable Re-entry Vehicle (MIRV) capability in 2024.", "source": "DRDO"},

    {"id": 3, "date": "2023-03-05", "category": "Defence", "headline": "Exercise Tiger Triumph",
     "question": "Exercise Tiger Triumph is conducted between India and:", "options": ["A) Russia", "B) France", "C) USA", "D) Australia"],
     "answer": "C", "explanation": "Tiger Triumph is a tri-service amphibious exercise between India and the USA.", "source": "Indian Navy"},

    {"id": 4, "date": "2023-04-20", "category": "Defence", "headline": "India's first indigenous aircraft carrier INS Vikrant",
     "question": "INS Vikrant was commissioned in:", "options": ["A) 2020", "B) 2021", "C) 2022", "D) 2023"],
     "answer": "C", "explanation": "INS Vikrant, India's first indigenous aircraft carrier, was commissioned on 2 September 2022.", "source": "Indian Navy"},

    {"id": 5, "date": "2023-05-12", "category": "Defence", "headline": "BrahMos missile exported to Philippines",
     "question": "BrahMos is a joint venture between India and:", "options": ["A) Russia", "B) USA", "C) Israel", "D) France"],
     "answer": "A", "explanation": "BrahMos is developed jointly by India's DRDO and Russia's NPO Mashinostroyeniya.", "source": "DRDO"},

    {"id": 6, "date": "2023-06-08", "category": "Defence", "headline": "Tejas Mk1A order placed",
     "question": "Tejas Mk1A is manufactured by:", "options": ["A) DRDO", "B) HAL", "C) BEL", "D) ISRO"],
     "answer": "B", "explanation": "Tejas Mk1A is manufactured by Hindustan Aeronautics Limited (HAL).", "source": "HAL"},

    {"id": 7, "date": "2023-07-25", "category": "Defence", "headline": "Chandrayaan-3 successful landing",
     "question": "Chandrayaan-3 landed near which lunar region?", "options": ["A) North Pole", "B) Equator", "C) South Pole", "D) Dark side"],
     "answer": "C", "explanation": "Chandrayaan-3 successfully landed near the lunar south pole on 23 August 2023, making India the first country to do so.", "source": "ISRO"},

    {"id": 8, "date": "2023-08-15", "category": "Defence", "headline": "India's defence exports reach new high",
     "question": "India's defence export target for 2024-25 is:", "options": ["A) ₹10,000 cr", "B) ₹20,000 cr", "C) ₹35,000 cr", "D) ₹50,000 cr"],
     "answer": "C", "explanation": "India aims to achieve ₹35,000 crore in defence exports by 2024-25 as part of Atmanirbhar Bharat.", "source": "Ministry of Defence"},

    {"id": 9, "date": "2023-09-10", "category": "Defence", "headline": "Exercise Tasman Saber",
     "question": "Exercise Tasman Saber is held between India, USA, and:", "options": ["A) UK", "B) Australia", "C) Japan", "D) Canada"],
     "answer": "B", "explanation": "Exercise Tasman Saber is a trilateral military exercise between India, USA, and Australia.", "source": "Indian Army"},

    {"id": 10, "date": "2023-10-05", "category": "Defence", "headline": "India joins Artemis Accords",
     "question": "The Artemis Accords are related to:", "options": ["A) Climate change", "B) Lunar and space exploration", "C) Nuclear weapons", "D) Maritime security"],
     "answer": "B", "explanation": "The Artemis Accords are a multilateral framework for peaceful exploration of the Moon, Mars, and beyond.", "source": "NASA"},

    {"id": 11, "date": "2023-11-20", "category": "Defence", "headline": "INS Imphal commissioned",
     "question": "INS Imphal belongs to which class of warships?", "options": ["A) Kolkata class", "B) Vikrant class", "C) Visakhapatnam class", "D) Shivalik class"],
     "answer": "C", "explanation": "INS Imphal is the third destroyer of the Project 15B (Visakhapatnam class).", "source": "Indian Navy"},

    {"id": 12, "date": "2023-12-01", "category": "Defence", "headline": "Exercise Shakti between India and France",
     "question": "Exercise Shakti is a bilateral exercise between India and:", "options": ["A) UK", "B) Germany", "C) France", "D) Italy"],
     "answer": "C", "explanation": "Exercise Shakti is a joint military exercise between the Indian Army and the French Army.", "source": "Indian Army"},

    {"id": 13, "date": "2024-01-10", "category": "Space", "headline": "PSLV-C58/XPoSat launched",
     "question": "XPoSat is India's first:", "options": ["A) Weather satellite", "B) Polarimetry mission", "C) Communication satellite", "D) Navigation satellite"],
     "answer": "B", "explanation": "XPoSat (X-ray Polarimeter Satellite) is India's first and world's second polarimetry mission.", "source": "ISRO"},

    {"id": 14, "date": "2024-02-15", "category": "Defence", "headline": "CDS General Anil Chauhan visits USA",
     "question": "The Chief of Defence Staff (CDS) of India in 2024 is:", "options": ["A) General MM Naravane", "B) General Bipin Rawat", "C) General Anil Chauhan", "D) Admiral R Hari Kumar"],
     "answer": "C", "explanation": "General Anil Chauhan was appointed as India's second CDS in September 2022.", "source": "Ministry of Defence"},

    {"id": 15, "date": "2024-03-20", "category": "Defence", "headline": "Pralay ballistic missile inducted",
     "question": "Pralay is classified as:", "options": ["A) ICBM", "B) Cruise missile", "C) Surface-to-Surface quasi-ballistic missile", "D) Anti-tank missile"],
     "answer": "C", "explanation": "Pralay is a surface-to-surface quasi-ballistic missile with a range of 150-500 km.", "source": "DRDO"},

    {"id": 16, "date": "2024-04-05", "category": "Defence", "headline": "India-Australia 2+2 Ministerial dialogue",
     "question": "2+2 Ministerial Dialogue involves ministers of:", "options": ["A) Finance and Home", "B) Defence and External Affairs", "C) Science and Defence", "D) Trade and Defence"],
     "answer": "B", "explanation": "2+2 Ministerial Dialogue is held between Defence and External Affairs/Foreign Ministers of the two countries.", "source": "MEA"},

    {"id": 17, "date": "2024-05-12", "category": "Defence", "headline": "Exercise Mitra Shakti with Sri Lanka",
     "question": "Exercise Mitra Shakti is held between India and:", "options": ["A) Nepal", "B) Bhutan", "C) Sri Lanka", "D) Bangladesh"],
     "answer": "C", "explanation": "Exercise Mitra Shakti is a bilateral Army exercise between India and Sri Lanka.", "source": "Indian Army"},

    {"id": 18, "date": "2024-06-18", "category": "Defence", "headline": "India signs MQ-9B drone deal with USA",
     "question": "MQ-9B SeaGuardian is a:", "options": ["A) Fighter jet", "B) Transport aircraft", "C) Unmanned Aerial Vehicle (UAV)", "D) Submarine drone"],
     "answer": "C", "explanation": "MQ-9B is a high-altitude, long-endurance remotely piloted UAV manufactured by General Atomics.", "source": "US DoD"},

    {"id": 19, "date": "2024-07-10", "category": "Defence", "headline": "Agnikul Cosmos test launch",
     "question": "Agnikul Cosmos launched the world's first rocket with:", "options": ["A) Nuclear propulsion", "B) Fully 3D-printed engine", "C) Solar sails", "D) Hybrid fuel"], 
     "answer": "B", "explanation": "Agnikul Cosmos launched Agnibaan SOrTeD with Agnilet — the world's first flight with a fully 3D-printed engine.", "source": "ISRO"},

    {"id": 20, "date": "2024-08-05", "category": "Defence", "headline": "India's first dedicated defence industrial corridors",
     "question": "India's two Defence Industrial Corridors are in:", "options": ["A) Uttar Pradesh and Tamil Nadu", "B) Gujarat and Maharashtra", "C) Rajasthan and Karnataka", "D) Odisha and AP"],
     "answer": "A", "explanation": "India has established Defence Industrial Corridors in Uttar Pradesh (Bundelkhand) and Tamil Nadu.", "source": "Ministry of Defence"},

    {"id": 21, "date": "2024-09-01", "category": "Defence", "headline": "Exercise Vinbax with Vietnam",
     "question": "Exercise Vinbax is conducted between India and:", "options": ["A) Thailand", "B) Vietnam", "C) Philippines", "D) Indonesia"],
     "answer": "B", "explanation": "Exercise Vinbax is a joint military exercise between India and Vietnam.", "source": "Indian Army"},

    {"id": 22, "date": "2024-10-10", "category": "Defence", "headline": "India successfully tests Hypersonic missile",
     "question": "India's hypersonic missile tested in 2024 has a range of:", "options": ["A) 500 km", "B) 1000 km", "C) 1500+ km", "D) 300 km"],
     "answer": "C", "explanation": "India successfully tested a hypersonic missile with a range of more than 1500 km in November 2024.", "source": "DRDO"},

    {"id": 23, "date": "2023-11-10", "category": "Defence", "headline": "INS Surat — P15B destroyer",
     "question": "INS Surat is the _____ destroyer of Project 15B.", "options": ["A) First", "B) Second", "C) Third", "D) Fourth"],
     "answer": "D", "explanation": "INS Surat is the fourth and final destroyer of the Project 15B (Visakhapatnam class).", "source": "Indian Navy"},

    {"id": 24, "date": "2023-12-15", "category": "Defence", "headline": "Exercise Vajra Prahar with USA",
     "question": "Exercise Vajra Prahar focuses on:", "options": ["A) Naval warfare", "B) Air combat", "C) Special Forces operations", "D) Cyber warfare"],
     "answer": "C", "explanation": "Exercise Vajra Prahar is a Special Forces joint exercise between India and USA.", "source": "Indian Army"},

    {"id": 25, "date": "2024-01-26", "category": "Defence", "headline": "Republic Day 2024 chief guest",
     "question": "The Chief Guest for Republic Day 2024 was:", "options": ["A) Macron of France", "B) Biden of USA", "C) Albanese of Australia", "D) Sunak of UK"],
     "answer": "A", "explanation": "French President Emmanuel Macron was the Chief Guest at India's 75th Republic Day on 26 January 2024.", "source": "PIB"},

    {"id": 26, "date": "2024-02-28", "category": "Defence", "headline": "DRDO's ASAT capability",
     "question": "Mission Shakti demonstrated India's capability to:", "options": ["A) Launch satellites", "B) Destroy satellites in space", "C) Intercept ballistic missiles", "D) Deploy space weapons"],
     "answer": "B", "explanation": "Mission Shakti in March 2019 demonstrated India's Anti-Satellite (ASAT) missile capability by shooting down a live satellite.", "source": "DRDO"},

    {"id": 27, "date": "2024-03-10", "category": "Space", "headline": "Gaganyaan crew training",
     "question": "Gaganyaan is India's:", "options": ["A) Moon mission", "B) Mars mission", "C) Human spaceflight mission", "D) Venus probe"],
     "answer": "C", "explanation": "Gaganyaan is India's first human spaceflight mission being developed by ISRO.", "source": "ISRO"},

    {"id": 28, "date": "2024-04-20", "category": "Defence", "headline": "India joins Quad security dialogue",
     "question": "QUAD (Quadrilateral Security Dialogue) comprises:", "options": ["A) India, USA, UK, France", "B) India, USA, Japan, Australia", "C) India, Russia, China, Pakistan", "D) India, USA, Israel, Japan"],
     "answer": "B", "explanation": "The Quadrilateral Security Dialogue (QUAD) is a strategic forum comprising India, USA, Japan, and Australia.", "source": "MEA"},

    {"id": 29, "date": "2024-05-25", "category": "Defence", "headline": "INS Arighaat commissioned",
     "question": "INS Arighaat is India's:", "options": ["A) Aircraft carrier", "B) Destroyer", "C) Second nuclear submarine", "D) Frigate"],
     "answer": "C", "explanation": "INS Arighaat is India's second nuclear-powered ballistic missile submarine (SSBN).", "source": "Indian Navy"},

    {"id": 30, "date": "2024-06-30", "category": "Defence", "headline": "Exercise Yudh Abhyas with USA",
     "question": "Exercise Yudh Abhyas is held between:", "options": ["A) India and France", "B) India and Russia", "C) India and USA", "D) India and Japan"],
     "answer": "C", "explanation": "Exercise Yudh Abhyas is one of the largest running joint military exercises between Indian Army and US Army.", "source": "Indian Army"},
]


@router.get("/today")
def get_today_question():
    """Return one question based on day of year."""
    day_of_year = datetime.now().timetuple().tm_yday
    idx = day_of_year % len(CURRENT_AFFAIRS)
    return CURRENT_AFFAIRS[idx]


@router.get("/all")
def get_all_questions():
    """Return all current affairs questions."""
    return {"count": len(CURRENT_AFFAIRS), "questions": CURRENT_AFFAIRS}


@router.get("/week")
def get_week_questions():
    """Return last 7 questions based on date order."""
    sorted_q = sorted(CURRENT_AFFAIRS, key=lambda x: x["date"], reverse=True)
    return {"count": 7, "questions": sorted_q[:7]}


@router.get("/{question_id}")
def get_question_by_id(question_id: int):
    """Return a specific question by ID."""
    for q in CURRENT_AFFAIRS:
        if q["id"] == question_id:
            return q
    return {"error": "Question not found"}
