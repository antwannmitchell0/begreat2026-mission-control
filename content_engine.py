#!/usr/bin/env python3
"""
BeGreat2026 Content Engine
Generates your daily content plan — what to post, when, captions, hashtags.
Run: python3 content_engine.py
"""

import random
from datetime import datetime, timedelta

# ─── IDEA VAULT (500+ topics) ────────────────────────────────
TOPICS = {
    "personal_story": [
        "The day I decided to drop out of school",
        "What prison really taught me",
        "The moment I got my college acceptance letter",
        "How I survived my first year out of prison",
        "The biggest mistake I made and what I learned",
        "Why I started B.E.G.R.E.A.T.",
        "The person who believed in me when I didn't",
        "What I wish someone had told me at 13",
        "The day I stopped making excuses",
        "How I studied with no foundation",
        "What I told myself in the darkest moments",
        "The phone call that changed everything",
        "How I got my first speaking opportunity",
        "The moment I realized my story could help someone",
        "What my family thinks of my journey",
    ],
    "mindset": [
        "Why most people quit 3 feet from gold",
        "The truth about motivation nobody talks about",
        "How to reprogram your mind after trauma",
        "Why discipline beats motivation every time",
        "The dangerous lie of 'I'll start Monday'",
        "How to silence the voice that says you can't",
        "Why your environment is killing your dreams",
        "The power of deciding who you want to be",
        "Why failure is just feedback in disguise",
        "How to stop being your own worst enemy",
        "The difference between excuses and reasons",
        "Why your past does not determine your future",
        "How to build mental toughness from nothing",
        "The one thing every successful person does differently",
        "Why small wins matter more than big goals",
    ],
    "statistics": [
        "73% of Americans say they want to write a book but never do",
        "Less than 1% of incarcerated people pursue higher education",
        "92% of people abandon their goals within 3 months",
        "People with written goals are 42% more likely to achieve them",
        "80% of millionaires experienced major failure before success",
        "Only 8% of people follow through on resolutions",
        "67% of employees are disengaged at work — are you living your purpose?",
        "The average person spends 147 minutes daily on social media — use it to grow",
        "People who read 30 minutes a day are 2.5x more successful",
        "43% of formerly incarcerated people are re-arrested within a year — choose different",
        "Children of incarcerated parents are 70% less likely to finish high school — break the cycle",
        "It takes 66 days to build a new habit, not 21",
        "95% of our behavior is subconscious — reprogram it intentionally",
        "People with mentors are 5x more likely to reach their goals",
        "The average millionaire has 7 streams of income — start building",
    ],
    "begreat_principles": [
        "B is for BELIEVE — even when the evidence says otherwise",
        "E is for ENDURE — pain is temporary, quitting is permanent",
        "G is for GRIND — show up even when you don't feel like it",
        "R is for RESILIENCE — bounce back harder every time",
        "E is for EDUCATE — never stop learning, never stop growing",
        "A is for ADAPT — the world changes, so must you",
        "T is for TRANSFORM — the goal is to become, not just achieve",
        "Which letter of B.E.G.R.E.A.T. do you struggle with most?",
        "B.E.G.R.E.A.T. is not a slogan — it's a survival guide",
        "The acronym that saved my life",
    ],
    "challenge_content": [
        "The 7-day B.E.G.R.E.A.T. challenge — Day 1: BELIEVE",
        "Drop your one goal for 2026 in the comments",
        "Tag someone who needs to hear this today",
        "What's the one thing holding you back? Be honest.",
        "If you gave up on something, what was it?",
        "Name one person who believed in you when you didn't believe in yourself",
        "What does greatness mean to YOU?",
        "Share your comeback story below",
        "Rate your mindset right now from 1-10",
        "What would you attempt if failure wasn't an option?",
    ],
    "motivational_hooks": [
        "Nobody claps for you when you're in the dark. That's when you clap for yourself.",
        "The version of you that gives up and the version that doesn't — they have the same 24 hours.",
        "Your struggle is someone else's testimony. Don't waste it.",
        "I didn't have a plan. I had a decision. That was enough.",
        "Poverty is not just money. It's a mindset. Change the mind, change the life.",
        "Prison tried to write my ending. I rewrote the whole story.",
        "The hardest degree I earned wasn't from any college.",
        "You don't need a perfect past to build a perfect future.",
        "The people who bet against you are watching. Keep going.",
        "Every great comeback started with someone who refused to stay down.",
        "Your setback has a purpose you can't see yet.",
        "Greatness doesn't require permission from anyone.",
        "The world needs your story. Not your highlight reel. Your real story.",
        "Stop comparing your chapter 1 to someone else's chapter 20.",
        "You survived everything that was supposed to break you. That's power.",
    ],
}

PLATFORM_HASHTAGS = {
    "instagram": "#BeGreat2026 #Motivation #Mindset #Inspire #MotivatioNation #Success #GrowthMindset #Hustle #PersonalDevelopment #Overcoming #BeGreat #InspirationalQuotes #LifeCoach #Transformation #NeverGiveUp #FromPrisonToSuccess #SecondChances #Greatness #Believe #Grind",
    "tiktok": "#BeGreat2026 #MotivationTikTok #Fyp #Foryou #Inspire #Success #Mindset #Transformation #LifeCoach #Hustle #GrindSeason #BeGreat #NeverQuit #SecondChances #TikTokMotivation",
    "facebook": "#BeGreat2026 #Motivation #Inspire #Success #Mindset #PersonalDevelopment #BeGreat #Transformation",
    "youtube": "BeGreat2026, Motivation, Mindset, Success, Inspiration, Personal Development, Overcome, Resilience, Second Chances, Life Coach",
}

CAPTION_TEMPLATES = {
    "stat": [
        "📊 {stat}\n\n{context}\n\nDon't be a statistic. Be the exception.\n\n👇 Drop a 🔥 if this hit different.\n\n{hashtags}",
        "The numbers don't lie. 📊\n\n{stat}\n\n{context}\n\nYour story doesn't have to end that way.\n\n{hashtags}",
        "This stopped me in my tracks. 👇\n\n{stat}\n\n{context}\n\nShare this with someone who needs a push today.\n\n{hashtags}",
    ],
    "quote": [
        "💬 \"{quote}\"\n\n{context}\n\nDouble tap if this spoke to you. ❤️\n\n{hashtags}",
        "Read this twice. 👇\n\n\"{quote}\"\n\n{context}\n\nTag someone who needs to see this today.\n\n{hashtags}",
        "This one is personal. 🙏\n\n\"{quote}\"\n\n{context}\n\nDrop a ✅ if you're committed to being great.\n\n{hashtags}",
    ],
    "story": [
        "Real talk. 👇\n\n{hook}\n\n{story}\n\nIf my story can help even one person, it was worth sharing.\n\nFollow for more. 🔥 @begreat2026\n\n{hashtags}",
        "I've never talked about this publicly. But here it is. 👇\n\n{hook}\n\n{story}\n\nLike if you needed to hear this today.\n\n{hashtags}",
        "This is why I do this. 🙏\n\n{hook}\n\n{story}\n\nShare this. Someone out there needs it.\n\n{hashtags}",
    ],
    "challenge": [
        "🎯 {challenge}\n\nI'll go first: {answer}\n\nYour turn 👇\n\n{hashtags}",
        "Be honest. 👇\n\n{challenge}\n\nDrop your answer below. We're all in this together. 💪\n\n{hashtags}",
    ]
}

POSTING_SCHEDULE = [
    {"time": "7:00 AM",  "platform": "TikTok",    "type": "hook_video",   "note": "Morning scroll traffic peak"},
    {"time": "9:00 AM",  "platform": "Instagram",  "type": "stat_flyer",   "note": "Working commute audience"},
    {"time": "12:00 PM", "platform": "Facebook",   "type": "quote_flyer",  "note": "Lunch break scroll"},
    {"time": "12:30 PM", "platform": "TikTok",     "type": "story_clip",   "note": "Lunch TikTok traffic"},
    {"time": "5:00 PM",  "platform": "Instagram",  "type": "story_clip",   "note": "After-work peak"},
    {"time": "6:00 PM",  "platform": "YouTube",    "type": "long_form",    "note": "Evening YouTube traffic (weekly)"},
    {"time": "7:00 PM",  "platform": "Facebook",   "type": "stat_flyer",   "note": "Prime evening audience"},
    {"time": "8:00 PM",  "platform": "TikTok",     "type": "quote_clip",   "note": "Night owl TikTok peak"},
    {"time": "9:00 PM",  "platform": "Instagram",  "type": "quote_flyer",  "note": "Late evening engagement"},
]


def generate_daily_brief(day_number=1):
    today = datetime.now()
    date_str = today.strftime("%A, %B %d, %Y")
    
    print(f"""
╔══════════════════════════════════════════════════════════╗
║          BeGreat2026 — Daily Content Brief               ║
║          Day {day_number:3d} | {date_str:<31} ║
╚══════════════════════════════════════════════════════════╝
""")

    # Pick today's content mix
    all_topics = []
    for category, items in TOPICS.items():
        for item in items:
            all_topics.append((category, item))
    
    random.shuffle(all_topics)
    today_picks = all_topics[:9]  # One for each post slot

    print("📋 TODAY'S POSTING SCHEDULE:\n")
    print(f"{'TIME':<10} {'PLATFORM':<12} {'TYPE':<15} {'CONTENT'}")
    print("─" * 80)

    for i, post in enumerate(POSTING_SCHEDULE):
        category, topic = today_picks[i] if i < len(today_picks) else ("mindset", "Stay focused")
        print(f"{post['time']:<10} {post['platform']:<12} {post['type']:<15} {topic[:45]}")

    print(f"""
─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─
📝 TODAY'S FEATURED CONTENT:
─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─
""")

    # Feature 3 fully written posts
    print("POST 1 — INSTAGRAM (9:00 AM) — Stat Flyer Caption:")
    print("─" * 50)
    stat = random.choice(TOPICS["statistics"])
    caption = random.choice(CAPTION_TEMPLATES["stat"]).format(
        stat=stat,
        context="Your story doesn't have to be defined by where you started.",
        hashtags=PLATFORM_HASHTAGS["instagram"]
    )
    print(caption)

    print("\n\nPOST 2 — TIKTOK (12:30 PM) — Video Hook:")
    print("─" * 50)
    hook = random.choice(TOPICS["motivational_hooks"])
    story_topic = random.choice(TOPICS["personal_story"])
    print(f"🎬 HOOK (first 3 seconds — say this to camera):")
    print(f'   "{hook}"')
    print(f"\n📖 THEN TALK ABOUT:")
    print(f'   {story_topic}')
    print(f"\n📱 CAPTION:")
    caption2 = random.choice(CAPTION_TEMPLATES["story"]).format(
        hook=hook,
        story=f"Today I want to talk about: {story_topic.lower()}",
        hashtags=PLATFORM_HASHTAGS["tiktok"]
    )
    print(caption2)

    print("\n\nPOST 3 — FACEBOOK (7:00 PM) — Quote Flyer Caption:")
    print("─" * 50)
    quote, author = random.choice(TOPICS["motivational_hooks"]), "Antwann Mitchell Sr."
    caption3 = random.choice(CAPTION_TEMPLATES["quote"]).format(
        quote=quote,
        context="From someone who lost everything and built it back from zero.",
        hashtags=PLATFORM_HASHTAGS["facebook"]
    )
    print(caption3)

    print(f"""
─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─
🎯 TODAY'S VIDEO TOPIC (record anytime, post tonight):
─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

Topic: {random.choice(TOPICS["personal_story"])}
Hook:  {random.choice(TOPICS["motivational_hooks"])}
Stat to include: {random.choice(TOPICS["statistics"])}
B.E.G.R.E.A.T. angle: {random.choice(TOPICS["begreat_principles"])}

📌 REMEMBER:
  • Reply to ALL comments within 60 minutes of posting
  • End every video with: "Follow @BeGreat2026 — link in bio"
  • Add your booking link to every bio: [your booking link]
  • Goal today: 9 posts across 4 platforms

💪 YOU GOT THIS. B.E.G.R.E.A.T. ⚡
""")

    print(f"\n💡 GENERATE FLYERS FOR TODAY:")
    print(f"   python3 flyer_factory.py 10")
    print(f"\n📅 GENERATE TOMORROW'S BRIEF:")
    print(f"   python3 content_engine.py {day_number + 1}")


if __name__ == "__main__":
    import sys
    day = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    generate_daily_brief(day)
