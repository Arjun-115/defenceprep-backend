from fastapi import APIRouter

router = APIRouter()

SSB_STAGES = [
    {
        "stage": 1,
        "name": "Screening Test",
        "duration": "Day 1",
        "tests": [
            {"name": "Officer Intelligence Rating (OIR)", "description": "Verbal and non-verbal reasoning tests"},
            {"name": "Picture Perception & Description Test (PPDT)", "description": "Write a story on a hazy picture, then discuss in group"}
        ]
    },
    {
        "stage": 2,
        "name": "Psychology Tests",
        "duration": "Day 2",
        "tests": [
            {"name": "Thematic Apperception Test (TAT)", "description": "12 pictures + 1 blank, write stories showing OLQs"},
            {"name": "Word Association Test (WAT)", "description": "60 words, write first sentence that comes to mind"},
            {"name": "Situation Reaction Test (SRT)", "description": "60 situations, write natural responses"},
            {"name": "Self Description Test (SD)", "description": "What you, parents, friends, teachers think about you"}
        ]
    },
    {
        "stage": 3,
        "name": "GTO Tasks",
        "duration": "Day 3-4",
        "tests": [
            {"name": "Group Discussion (GD)", "description": "Discussion on 2 topics, show leadership and communication"},
            {"name": "Group Planning Exercise (GPE)", "description": "Solve a model problem as a group"},
            {"name": "Progressive Group Task (PGT)", "description": "Cross obstacles as a group with helping material"},
            {"name": "Half Group Task (HGT)", "description": "Same as PGT but with half the group"},
            {"name": "Individual Obstacles", "description": "10 obstacles, each with different points"},
            {"name": "Command Task", "description": "You are commander, choose 2 subordinates and cross obstacle"},
            {"name": "Final Group Task (FGT)", "description": "Full group crosses final obstacle together"},
            {"name": "Lecturette", "description": "3-minute talk on a topic you choose from 4 given"}
        ]
    },
    {
        "stage": 4,
        "name": "Personal Interview",
        "duration": "Day 3-5",
        "tests": [
            {"name": "Interview with Interviewing Officer (IO)", "description": "In-depth personal interview covering life history, PIQ form, current affairs, motivation"}
        ]
    },
    {
        "stage": 5,
        "name": "Conference",
        "duration": "Day 5",
        "tests": [
            {"name": "Final Conference", "description": "All assessors meet, candidate is called in briefly, final recommendation made"}
        ]
    }
]

OLQ_LIST = [
    {"name": "Effective Intelligence", "description": "Ability to utilize knowledge practically"},
    {"name": "Reasoning Ability", "description": "Logical thinking and problem solving"},
    {"name": "Organizing Ability", "description": "Planning and organizing tasks efficiently"},
    {"name": "Power of Expression", "description": "Clearly expressing thoughts verbally and in writing"},
    {"name": "Social Adaptability", "description": "Adjusting and cooperating in social situations"},
    {"name": "Cooperation", "description": "Working harmoniously with others toward a common goal"},
    {"name": "Sense of Responsibility", "description": "Owning tasks and fulfilling commitments"},
    {"name": "Initiative", "description": "Taking action without being told"},
    {"name": "Self Confidence", "description": "Belief in own abilities and judgment"},
    {"name": "Speed of Decision", "description": "Making quick and sound decisions"},
    {"name": "Ability to Influence the Group", "description": "Motivating and guiding others"},
    {"name": "Liveliness", "description": "Being energetic and enthusiastic"},
    {"name": "Determination", "description": "Persisting despite obstacles"},
    {"name": "Courage", "description": "Facing danger or difficulty with bravery"},
    {"name": "Stamina", "description": "Physical and mental endurance"}
]

SSB_TIPS = [
    "Be natural and consistent across all tests — assessors look for a consistent personality.",
    "Show OLQs (Officer Like Qualities) organically, don't fake them.",
    "In GTO tasks, help the group achieve the goal — don't be a lone ranger.",
    "Read newspapers daily for at least 3 months before SSB.",
    "Fill your PIQ form honestly — the IO will grill you on everything you write.",
    "Physical fitness matters — start running and working out 3 months before.",
    "Practice storytelling for TAT — stories should have a positive, decisive hero.",
    "In WAT, write sentences that reflect positive, action-oriented thinking.",
    "Don't try to dominate in GD — facilitate and build on others' ideas.",
    "Know your home state, district, and local issues thoroughly for the interview."
]

@router.get("/stages")
def get_ssb_stages():
    return {"stages": SSB_STAGES}

@router.get("/olq")
def get_olq():
    return {"total": len(OLQ_LIST), "olqs": OLQ_LIST}

@router.get("/tips")
def get_ssb_tips():
    return {"tips": SSB_TIPS}

@router.get("/")
def get_ssb_overview():
    return {
        "overview": "SSB (Services Selection Board) is the interview process for joining the Indian Armed Forces as an officer.",
        "duration": "5 days",
        "total_stages": len(SSB_STAGES),
        "stages": [{"stage": s["stage"], "name": s["name"], "duration": s["duration"]} for s in SSB_STAGES]
    }
