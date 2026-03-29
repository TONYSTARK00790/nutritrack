"""Smart conversational chatbot that understands user messages and provides contextual responses."""
import re
import math
from collections import Counter

# Contextual response system: maps keywords/intents to empathetic, relevant guidance
CONTEXTUAL_RESPONSES = {
    'relationship': {
        'initial': "💙 I'm here to listen and support you through relationship challenges. Remember, all relationships go through ups and downs—that's completely normal. Let's talk about what's on your mind, and I'll do my best to help you navigate this.",
        'topics': {
            'communication|conflict|argument|fight|not talking|understand|listen': {
                'responses': [
                    "Communication is the foundation of every relationship. Try expressing your feelings without blame—use 'I feel...' instead of 'You always...' This opens dialogue instead of creating defensiveness. When they speak, listen to understand, not to reply. Often, both people need to feel heard before any resolution is possible.",
                    "Conflict is normal—healthy even. The issue isn't that you disagree; it's how you handle it. Take breaks if needed, come back when calm, focus on the specific issue (not bringing up past stuff), and aim for understanding rather than 'winning.' Sometimes you need to agree to disagree. The goal is to stay connected despite differences.",
                    "Not talking about problems is usually what makes things worse. The awkwardness feels safer than vulnerability, but it creates distance. Try: 'I want to talk about something that's been bothering me, and I need you to hear me out.' Most people appreciate directness over silence. You might be surprised how relieved they feel too.",
                ]
            },
            'trust|betrayal|lied|cheat|infidelity|broken trust': {
                'responses': [
                    "Broken trust is devastating because trust is fundamental. Before deciding anything, give yourself time to process without making major decisions immediately. Then, ask hard questions: Can they acknowledge what they did wrong? Are they genuinely remorseful? Are they willing to work to rebuild trust? If the answer is 'no,' that's important information for you.",
                    "Rebuilding trust is possible but takes time, transparency, and effort from both sides. They need to be accountable, consistent, and patient with your healing. You might need to grieve the trust that was broken before moving forward. Consider counseling—an objective third party helps immensely. Trust your gut about whether this is worth the work.",
                ]
            },
            'ghost|ignore|ghosted|left on read': {
                'responses': [
                    "Being ghosted hurts because it removes closure. It's okay to be upset—your feelings are valid. If it matters, try one calm message asking for clarity; if there's no reply, protect your time and move forward.",
                    "No reply often tells you more than silence feels comfortable admitting. You deserve people who communicate. Give yourself permission to step back and spend energy on those who show up.",
                ]
            },
            'reconcile|apologize|make up|sorry|forgive': {
                'responses': [
                    "Reconciliation is a process. A sincere apology acknowledges hurt, accepts responsibility, and offers change. If you're apologizing, be specific about what you did and how you'll avoid repeating it. If you're receiving an apology, ask for actions, not just words.",
                    "Forgiveness is for you more than them—it's a choice to release the hurt so you can move forward. It doesn't mean you forget or immediately trust again; it means you decide not to carry resentment forever.",
                ]
            },
            'boundaries|respect|no|him|her|expectations|needs|taking for granted': {
                'responses': [
                    "You teach people how to treat you through your boundaries. If you're not expressing your needs, they might not even know what they are. Be clear: 'I need X,' 'I'm uncomfortable with Y,' 'This doesn't work for me.' Healthy relationships require both people's needs to matter. You're not being selfish for having them.",
                    "Feeling taken for granted is a sign that your effort isn't being reciprocated or acknowledged. Have a calm conversation: 'I feel like my efforts aren't noticed or appreciated. I need to see more effort from your side too.' If they care, they'll listen. If they get defensive instead of hearing you, that's also important information.",
                ]
            },
            'love|care|still|future|marry|commitment|serious|leave|stay|break up|end': {
                'responses': [
                    "When deciding whether to stay or go, ask yourself: Are my core needs being met? Does this person treat me with respect? Am I growing or shrinking in this relationship? Do I feel safe, valued, and supported? Your answers matter more than how long you've been together or fear of being alone. You deserve to be with someone who's *choosing* you every day.",
                    "It's okay to grieve a relationship even if you're the one leaving. The loss is real. But sometimes the kindest thing you can do for both of you is to let go. If it's been a pattern of hurt, requests going unheard, or feeling small, staying 'to try harder' usually just extends the pain. Your mental health matters more than any relationship.",
                ]
            },
            'scared|hurt|anxious|insecure|jealous|worried': {
                'responses': [
                    "Feeling scared or anxious in a relationship often means something deep touched a wound—maybe past hurt, abandonment fears, or low self-worth. This isn't about them being untrustworthy; it's about you healing your own stuff. Therapy helps here. But also: communicate your insecurity. 'I know this is my stuff, but I need reassurance sometimes.' Real partners understand.",
                    "Jealousy tells you something about yourself, not necessarily about them. Are you insecure? Were you hurt before? Feeling replaced or less-than? Addressing jealousy is about building your own self-worth and trusting your partner. If your jealousy is based on legitimate behavior (they're flirting, hiding things), that's different—you have a right to address that.",
                ]
            },
            'default': {
                'responses': [
                    "Relationships are mirrors. When something upsets you, pause and ask: What does this reveal about me or my expectations? This doesn't mean you're wrong—it means there's an opportunity to understand yourself better and communicate more clearly. Growth happens in these moments.",
                    "Love is an action, not just a feeling. It's showing up, listening, being vulnerable, setting boundaries, and choosing them even when it's hard. If both people are doing this, the relationship strengthens. If only one person is trying, that's unsustainable. Evaluate the effort you both are making.",
                ]
            }
        }
    },
    'friendship': {
        'initial': "👥 Friendships are one of life's greatest treasures, and it hurts when they feel strained or uncertain. I'm here to talk through what's happening and help you navigate this. Good friendships are worth investing in, but they also require honesty and care from both sides.",
        'topics': {
            'distance|drift|apart|lost|close|grow|change': {
                'responses': [
                    "People naturally drift apart when life changes—new jobs, relationships, cities, or phases of life. This is normal and doesn't erase the good memories. But if this friendship matters to you, don't wait for them to reach out. Be the one who initiates. Send a message: 'I miss you. Want to catch up?' Most people appreciate the effort.",
                    "Sometimes drifting apart is just life evolving, and that's okay. You can appreciate what the friendship was without forcing it to be something it's not anymore. Real friends, even after long gaps, can pick right back up. That's how you know it was real.",
                ]
            },
            'conflict|argument|fight|upset|angry|betrayal|hurt|misunderstanding': {
                'responses': [
                    "Friendship conflicts often stem from unspoken expectations or misunderstandings. Have a direct conversation: 'I've felt hurt by X, and I want to understand your perspective.' Be specific, be honest, be willing to listen. Most friendship rifts heal when both people care enough to talk it through. Don't let pride keep you from reconnecting.",
                    "If they hurt you, let them know clearly. If they apologize genuinely and change the behavior, great. If they get defensive or dismiss your feelings repeatedly, you might have a one-sided friendship. You deserve friends who care when they hurt you.",
                ]
            },
            'ghosting|flaky|cancelled|no-show': {
                'responses': [
                    "Flaky friends are frustrating because they make you question your importance to them. Call it out gently: 'When you cancel last-minute, I feel unimportant.' If behavior continues, scale back your investment.",
                    "People cancel for many reasons. If it's rare, give grace. If it's a pattern, make choices that protect your time and joy. You deserve friends who treat your plans as worth keeping.",
                ]
            },
            'apologize|reconcile|make up|sorry': {
                'responses': [
                    "Apologies matter most when they're specific and followed by change. If you want to reconcile, say what you're sorry for, ask what they need, and show consistent effort. Healing takes time.",
                    "If someone apologizes to you, consider whether their actions change. Words are a start; actions rebuild trust. Decide what you need to see to feel safe again.",
                ]
            },
            'value|give|receive|support|one-sided|effort|energy|uneven': {
                'responses': [
                    "Friendships should feel reciprocal. If you're always initiating, always supporting, always giving, that's exhausting and unfair. Ask yourself: When you need support, are they there? Do they ask about your life or just dump their problems? If it's consistently uneven, you might need to scale back your effort or set boundaries.",
                    "Sometimes we underestimate how much friends value us. They might show love differently than we expect. But if you've clearly communicated your needs and nothing changes, it's okay to invest your energy elsewhere. You're not abandoning them; you're protecting your own wellbeing.",
                ]
            },
            'jealous|excluded|left out|group|replace|new friends': {
                'responses': [
                    "Jealousy in friendships is usually about fear of being left out or replaced. Here's the truth: your friends having other friends doesn't diminish what they have with you. Different relationships fill different needs. When you feel left out, talk about it: 'I felt excluded when...' Most friends didn't realize they were doing it.",
                    "If you're genuinely being excluded repeatedly, that's worth examining. Are you being excluded from the whole friend group, or just from certain activities? The difference matters. A real friend will make time for you, even if they're busy with others.",
                ]
            },
            'trust|honesty|secret|gossip|talk|share': {
                'responses': [
                    "Trust is everything in friendship. If a friend shared in confidence and you gossiped about it, they have a right to feel betrayed. If they shared something and you judged them harshly, that broke safety. Friendships need one thing most: the feeling that you're safe being yourself around that person. Work to rebuild that if you ruptured it.",
                    "Good friends keep your confidences and celebrate who you really are. If a friend is spreading gossip about you or constantly judging you, that's not a true friend. You deserve people who have your back and can keep private things private.",
                ]
            },
            'default': {
                'responses': [
                    "Friendships require intention. Reach out, make plans, be present when you're together, ask meaningful questions, and show up when they need you. Small, consistent efforts keep bonds alive. You're building something valuable.",
                    "Some friendships are seasonal, and that's okay. You appreciate them for the chapter they were in your life. Real friendships transcend time and distance. If a friendship needs constant effort to feel warm, it might be time to let go gently.",
                ]
            }
        }
    },
    'parents': {
        'initial': "👨‍👩‍👧 Family relationships are complex and deeply emotional. Parents are humans doing their best (even when it doesn't feel like it), and you have valid feelings about how they've treated you. Let's talk about what's happening and how you can navigate this.",
        'topics': {
            'don\'t understand|disagree|disapprove|choice|decision|path|career': {
                'responses': [
                    "When parents disapprove of your choices, it usually comes from fear, not malice. They're imagining worst-case scenarios based on their experience. Try explaining calmly: 'I know you're worried, but here's why I'm confident in this choice...' Listen to their concerns. Sometimes acknowledgment is enough, even if they never fully approve.",
                    "You don't need their permission to live your life. What you need is your own conviction. Once you're clear on why you're making a choice, their disapproval stings less. You're not responsible for making them happy with your life—you're responsible for living authentically.",
                ]
            },
            'critical|judge|lack confidence|not good enough|disappointed|expectations': {
                'responses': [
                    "Parental criticism can deeply wound us because we internalize their voice as truth. But here's the key: their judgment of you is incomplete. They see one version, one struggle, one moment. You are more complex, more capable, more worthy than any criticism suggests. Start building your own internal voice that's kinder, more accurate.",
                    "Some parents are overly critical because of their own insecurities. That doesn't make it hurt less, but it might help you depersonalize it. When they criticize, ask yourself: 'Is this actually true about me, or is this their wound speaking?' Often it's the latter.",
                ]
            },
            'emotional|unavailable|cold|don\'t care|support|there for me|absent': {
                'responses': [
                    "Having emotionally unavailable parents is its own kind of wound. You needed them and they weren't there in the way you needed. That's not your fault. Healing this means accepting you can't change them, only how you respond. Seek emotional support from friends, mentors, or a therapist who *can* be there for you.",
                    "Parents who aren't emotionally present often don't know how to be. They're not malicious; they're just limited in emotional capacity or awareness. You can grieve what you didn't get while building what you need from other relationships. You're not broken for needing that support—they were incomplete in providing it.",
                ]
            },
            'control|boundary|freedom|independence|manipulate|guilt|obligated': {
                'responses': [
                    "Parents trying to control you even into adulthood is about their need for control, not about what's best for you. Set firm boundaries: 'I appreciate your opinion, but I'm making my own decision.' Repeat as needed. They might push back, but consistency shows you're serious. Your life is yours to live.",
                    "Guilt is a tool of control. Recognize when a parent is using guilt to manipulate you. 'After all I've done...' or 'I sacrificed everything...' These statements are about their needs, not your responsibilities. You're not obligated to pay back 'debts' you didn't create.",
                ]
            },
            'abuse|toxic|hurt|harmful|safety|scared|wrong': {
                'responses': [
                    "If a parent's behavior has been harmful—emotionally, physically, or otherwise—please know this: you're not responsible for their wounds, and you're not obligated to maintain a relationship that hurts you. Your safety and mental health come first. Reaching out to a counselor or therapist is crucial here.",
                    "Abuse is never your fault. Whether it was physical, emotional, or verbal, you didn't deserve it. Healing requires professional support—a therapist who specializes in family trauma can help you process and build healthy boundaries. You deserve relationships that are safe and nurturing.",
                ]
            },
            'estranged|no contact|cut off|distance|separate': {
                'responses': [
                    "Estrangement from parents is painful and often complicated. It's okay to prioritize your wellbeing—sometimes distance is necessary. Therapists can help you process grief and conflicted feelings.",
                    "No-contact decisions are emotional and practical. If you choose distance, create a plan for support and rituals that mark transitions. You can grieve the relationship while protecting yourself.",
                ]
            },
            'default': {
                'responses': [
                    "Parental relationships often need renegotiation in adulthood. You're not children anymore; you're peers. Some parents can make this shift, and some can't. The ones who can will listen and respect your autonomy. That's what growth looks like.",
                    "You can honor your parents while also protecting your own wellbeing. These aren't mutually exclusive. Love and healthy distance can coexist. Set boundaries that work for you.",
                ]
            }
        }
    },
    'work': {
        'initial': "💼 Work stress is real and valid. Whether it's a difficult boss, toxic colleagues, burnout, or feeling undervalued, your mental and physical health matter more than any job. Let's talk about what's happening and explore ways to make this more manageable.",
        'topics': {
            'burnout|exhausted|tired|overwhelmed|stressed|can\'t handle': {
                'responses': [
                    "Burnout is a serious state where you're mentally and physically depleted. Signs: dreading work, cynicism, insomnia, irritability, feeling helpless. If this is you, something must change. Whether that's demanding time off, delegating, setting boundaries, or leaving—don't ignore it. Your health is non-negotiable.",
                    "You can't think clearly when you're burnt out. Before making major decisions, rest. Take time off if possible. Your brain needs recovery. Then, make a plan: What specifically is burning you out? Is it fixable at this job, or do you need to leave? Trust that you'll figure it out, but first, rest.",
                ]
            },
            'boss|manager|difficult|disrespect|unreasonable|unfair|manipulative': {
                'responses': [
                    "A bad boss can make even a great job unbearable. Try honest communication first: document your work, communicate clearly, be solution-focused. But if your boss is consistently disrespectful, it's a 'them' problem, not a 'you' problem. Start looking for a new job. Life's too short to spend 40 hours a week under someone who disrespects you.",
                    "Some bosses improve with clear feedback; others don't care. Pay attention: Do they listen when you speak up, or do they dismiss and blame? If it's the latter, don't waste energy. Spend that energy moving to somewhere better.",
                ]
            },
            'undervalued|unappreciated|not recognized|low pay|unfair|deserve more': {
                'responses': [
                    "You deserve to feel valued for your work. First, make your contributions visible. Document achievements, speak up in meetings, ensure your manager knows your impact. Then, have a conversation: 'I've contributed X, Y, Z, and I'd like to discuss compensation/advancement.' Be specific and professional. If they don't recognize your value, others will.",
                    "Don't wait for someone to give you what you deserve. Sometimes you need to move to a company that pays and respects you better. The biggest raises often come from switching jobs, not staying put. Your worth is real whether this company sees it or not.",
                ]
            },
            'toxic|culture|colleagues|gossip|drama|drama|hostile|negative': {
                'responses': [
                    "A toxic workplace drains your soul over time. You can't control coworkers, but you can control your boundaries. Keep conversations professional, don't engage in gossip, find allies, and protect your energy. But long-term? Don't spend 40 hours a week in a hostile environment. Make an exit plan.",
                    "Toxic company culture isn't fixed by individual effort. It requires leadership to take responsibility and change. That rarely happens. You're not failing by leaving; the system is failing you. Trust that there are better places to work.",
                ]
            },
            'harassment|discrimination|sexism|racism|bully': {
                'responses': [
                    "If you're experiencing harassment or discrimination, document everything and seek HR or legal advice. Your safety and dignity are paramount—no job is worth enduring abuse.",
                    "You don't have to tolerate bullying. Reach out to trusted colleagues, document incidents, and consider external advice if internal channels fail. Your wellbeing is the priority.",
                ]
            },
            'layoff|fired|terminated|restructuring|downsizing': {
                'responses': [
                    "Losing a job is a major life stressor, but it can also be an opening for better opportunities. Allow time to grieve, then update your resume, network, and treat job search as a project with small daily goals.",
                    "If you're facing layoff, negotiate severance if possible, ask about references, and focus on immediate needs—apply for unemployment benefits, update your LinkedIn, and reach out to your network.",
                ]
            },
            'promotion|raise|advancement|growth|career move': {
                'responses': [
                    "When asking for promotion or raise, prepare evidence: list accomplishments, metrics, and specific contributions. Set a meeting with your manager and present a concise case with desired salary or title.",
                    "Career growth sometimes requires visibility. Volunteer for projects that showcase leadership, ask for stretch assignments, and find mentors who can advocate for you.",
                ]
            },
            'overworked|too much|impossible|unrealistic|expectations|demands': {
                'responses': [
                    "If you have more work than humanely possible, speak up: 'I have X tasks with deadlines Y, Z. I can't do all of these well. What are the priorities?' Make your manager prioritize, not you. If they expect miracles with no support, that's a management problem, not you failing.",
                    "Overwork becomes normalized in some cultures, but it's still unsustainable. You will burn out. Set boundaries: clear work hours, do your best during them, log off for the day. Your worth isn't tied to how much you produce.",
                ]
            },
            'impostor syndrome|not good enough|fraud|doubt|credentials': {
                'responses': [
                    "Most high achievers feel like frauds sometimes. That feeling often means you care about doing good work. But here's the truth: you were hired for a reason. You have skills, experience, and value. Your impostor syndrome is lying to you. When doubt creeps in, list actual evidence of your competence.",
                    "If you genuinely lack a skill, learn it. But don't confuse 'I'm learning' with 'I'm a fraud.' Growth means you stretch yourself. That's healthy, not proof you don't belong.",
                ]
            },
            'default': {
                'responses': [
                    "Your job isn't your identity. Whether you love your work or hate it, remember: you are more than your career. Invest in yourself, relationships, hobbies, health. A well-rounded life is more fulfilling than climbing a ladder that's against the wrong wall.",
                    "The best time to look for a job is when you have one. Don't wait until you're desperate and burnt out. Keep growing your skills, network, and opportunities. You have more power than you think.",
                ]
            }
        }
    },
    'health': {
        'initial': "🏥 Health concerns can feel overwhelming and scary. Whether you're dealing with a new diagnosis, chronic illness, mental health challenges, or general worry, those feelings are valid. I'm here to listen and help you think through this.",
        'topics': {
            'diagnosis|test|result|waiting|uncertainty|worried': {
                'responses': [
                    "Waiting for test results or a diagnosis is the worst part because uncertainty is scarier than reality. Right now, focus on what you *can* control: sleep, hydration, nourishing food, gentle movement. Your body is trying its best. Anxiety lives in 'what-ifs'—bring yourself to the present moment. When you have answers, you'll handle them.",
                    "Once you get a diagnosis, give yourself time to process. Feel whatever emotions come—fear, anger, sadness are all normal. Then educate yourself about your condition, ask your doctor questions, find support communities. You're not the diagnosis; it's one part of your story.",
                ]
            },
            'pain|chronic|suffer|doesn\'t go away|quality of life': {
                'responses': [
                    "Chronic pain or chronic illness is grief—grief for the life you imagined and the energy you've lost. That's real and valid. Be gentle with yourself on hard days. Some days will be worse than others, and that doesn't mean you're failing. Find small joys, adapt your activities, ask for help.",
                    "Your worth isn't tied to productivity. You matter even on days you can't do much. Finding peace with your condition is a process. A good therapist or support group can help tremendously. You don't have to figure this out alone.",
                ]
            },
            'mental health|anxiety|depression|panic|therapy|mental': {
                'responses': [
                    "Mental health is health. If you're struggling with anxiety, depression, or any mental health challenge, please reach out to a professional. A therapist or counselor can provide tools that actually help. There's no shame in this—your brain is just needing support like any other body part. You deserve to feel okay.",
                    "Therapy isn't weakness; it's wisdom. You wouldn't feel bad about taking antibiotics for an infection. The same applies to mental health treatment. Start with your doctor if you're unsure who to reach out to. They can refer you to good resources.",
                ]
            },
            'eating|food|exercise|body image|disorder': {
                'responses': [
                    "If you're struggling with eating, exercise, or body image, that's serious and deserves professional support—a therapist AND a dietitian. Your body deserves nourishment and care, not punishment. Recovery is possible, and you deserve to feel peaceful around food and your body.",
                    "These struggles are real, not shallow. Your body has been trying to tell you something—through discomfort, exhaustion, or anxiety. Professional help can teach you to listen to your body with kindness instead of criticism.",
                ]
            },
            'medication|side effects|treatment|afraid|concerns': {
                'responses': [
                    "Medication can be life-changing. If your doctor recommends it, try it openly. Yes, side effects exist, but they often improve over time. If they don't, your doctor can adjust. Taking medication is not weakness—it's wisdom. Some brains need chemical support, just like some bodies need insulin.",
                    "Talk to your doctor about side effects. Don't just stop medication because of them—adjustments often help. Find the right balance between side effects and symptom management. Your doctor wants to help you find what works.",
                ]
            },
            'panic|panic attack|anxiety attack|hyperventilate': {
                'responses': [
                    "Panic attacks are terrifying but not dangerous. Grounding techniques help: 5-4-3-2-1 (name 5 things you see, 4 you can touch...). Focus on slow breaths and remind yourself this will pass. Consider therapy for long-term tools.",
                    "If panic attacks are frequent, seek professional help. Short-term breathing techniques can reduce intensity; long-term, CBT and medications can be very effective. You don't have to manage this alone.",
                ]
            },
            'substance|addiction|drink too much|using|withdrawal': {
                'responses': [
                    "Substance struggles are serious and common. Reach out to a medical professional or support group. Detoxing alone can be dangerous—seek supervised help. You're not weak for needing support.",
                    "Consider harm-reduction steps and professional resources: talk to a doctor, call local support lines, or try a peer-support group. Recovery is possible and asking for help is brave.",
                ]
            },
            'chronic fatigue|cfs|fatigued|tired all the time': {
                'responses': [
                    "Chronic fatigue can be medical and psychological. Start with a doctor's visit to rule out treatable causes (thyroid, anemia, sleep apnea). Track energy patterns and rest strategically; pacing helps.",
                    "Energy management is a skill: prioritize tasks, schedule rest, and test small routine changes. If medical tests are normal, consider a multidisciplinary approach with a doctor and therapist.",
                ]
            },
            'default': {
                'responses': [
                    "Taking care of your health isn't selfish—it's foundational. Regular checkups, sleep, movement, stress management, social connection—these enable everything else. Invest in your health fiercely.",
                    "Your body sends you messages every day. Exhaustion, pain, mood changes—these are signals, not complaints. Listen with curiosity and compassion. Small consistent actions compound into major health shifts over time.",
                ]
            }
        }
    },
    'fitness': {
        'initial': "💪 Fitness motivation can be hard, especially starting out, dealing with injury, or stuck in a plateau. You're already winning by *thinking* about your health. Let's talk about what's blocking you and make this feel less like a chore.",
        'topics': {
            'hate|don\'t like|boring|don\'t enjoy|dread|hard to start|motivation': {
                'responses': [
                    "If you hate the gym, you don't have to go! Humans thrive doing movement they enjoy. Hiking, dancing, swimming, martial arts, sports—find something that feels like play. When exercise is enjoyable, you'll actually do it. Consistency beats intensity every time.",
                    "Motivation is overrated. What matters is making movement easy and enjoyable. Do something so fun you'd do it without 'motivation.' The best workout is one you'll actually do. Build the habit first, intensity later.",
                ]
            },
            'start|beginning|beginner|never|scared|overwhelmed': {
                'responses': [
                    "Starting is the hardest part. Perfectionism is your enemy—you don't need the perfect plan, perfect body, or perfect gym. Start small: 10 minutes of movement you enjoy. Lower expectations, build consistency. Once it becomes a habit, expand. You've got this.",
                    "Every fit person started as a beginner. They didn't know what they were doing either. That awkward feeling fades. Start where you are, with what you have. Small consistent steps compound into big changes.",
                ]
            },
            'diet|nutrition|weight loss|calories|macros': {
                'responses': [
                    "Nutrition matters more than any single workout. Focus on a balanced plate: protein, veggies, whole carbs, healthy fats. Small, consistent changes beat extreme diets.",
                    "If weight loss is the goal, track portions for a short period to learn habits. Aim for sustainable calorie deficit and prioritize protein to preserve muscle. Consider a dietitian for personalized guidance.",
                ]
            },
            'injury|rehab|physio|pt|recover|recovery': {
                'responses': [
                    "Injury recovery needs patience. See a physical therapist to tailor rehab exercises. Move within pain-free ranges and progress slowly—consistency with small steps beats rushing back and reinjuring.",
                    "Don't ignore sharp or persistent pain. Modify activities, rest when needed, and seek professional assessment early. Early intervention prevents chronic problems.",
                ]
            },
            'plateau|stuck|not progressing|same|bored|no change|improvement': {
                'responses': [
                    "Plateaus mean your body has adapted—that's actually progress! Your baseline improved. Now change something: different exercises, higher intensity, different rep ranges, new environment. Your muscles need variety to keep growing. Trust the process; you'll break through.",
                    "Progress isn't just the scale. Notice energy, sleep, mood, strength gains, how clothes fit, or confidence. Celebrate small wins. You're building discipline and self-respect. That's incredible.",
                ]
            },
            'sore|pain|injury|hurt|recover|injured': {
                'responses': [
                    "Soreness after starting is normal and temporary. Stretch, hydrate, eat enough protein, sleep well. It'll fade in a few days. But sharp, acute pain is different—don't push through that. See a physical therapist if it persists. Recovery is important too.",
                    "Even injured, you can move. A PT can show you what's safe. Work around the injury. Rest matters, but complete inactivity slows recovery. Find the balance with professional guidance.",
                ]
            },
            'no time|busy|schedule|fit it in': {
                'responses': [
                    "'No time' usually means 'not a priority yet.' But here's the truth: you have time for things you decide matter. Is 20 minutes for a walk possible? That counts. Start there. You don't need an hour gym session. Consistency matters more than duration.",
                    "What would make fitness a priority for you? A health scare? A goal you care about? A friend to do it with? Sometimes we need a 'why' before the 'how' becomes easy. Find your motivation, then time becomes easier to find.",
                ]
            },
            'default': {
                'responses': [
                    "The best workout is the one you'll actually do. Find movement you enjoy, make it consistent, and let it compound. Small steps lead to big changes over time. You're closer to your goal than you think.",
                    "Your body changes when you consistently ask it to. Every workout counts, even the ones that feel small. You're training your brain to keep showing up. That builds discipline for everything in life.",
                ]
            }
        }
    },
    'other': {
        'initial': "❓ Whatever you're going through, I want you to know: your feelings matter. Stress, confusion, overwhelm—these are all valid. Sometimes life is just hard, and that's okay. Let's talk about what's on your mind.",
        'topics': {
            'overwhelmed|too much|can\'t handle|breakdown|can\'t cope': {
                'responses': [
                    "When everything feels overwhelming, you're probably trying to handle too much at once. Take a breath. Write down everything worrying you. Then prioritize: What needs attention today? What can wait? What's actually not yours to handle? You can't solve everything now. One step at a time.",
                    "Overwhelm is a sign you need to slow down and get support. Reach out to someone you trust. You don't have to figure this out alone. Even just talking about it often clarifies what matters most.",
                ]
            },
            'uncertain|don\'t know|confused|lost|what to do|help|stuck': {
                'responses': [
                    "Uncertainty is uncomfortable but it's where growth happens. You don't need all the answers right now. You can sit with the unknown while taking small steps forward. Ask for advice, gather information, talk to people you trust. You'll figure it out. You always do.",
                    "When you're stuck, sometimes the answer comes from a different perspective. Talk to someone who knows you and cares about you. Sometimes verbalizing your confusion helps clarity emerge.",
                ]
            },
            'money|financial|debt|broke|bills|budget': {
                'responses': [
                    "Financial stress is crushing—start with a simple budget: list income, fixed expenses, and non-essential spending. Prioritize essentials and reach out to local resources if you're struggling with basics.",
                    "If debt is overwhelming, contact creditors, ask for hardship plans, or connect with a free financial counselor. Small wins—like negotiating interest or creating a one-month budget—build momentum.",
                ]
            },
            'legal|court|lawyer|lawsuit|abuse protection|restraining order': {
                'responses': [
                    "Legal matters are stressful—get professional advice early. Reach out to a legal aid clinic if cost is a concern. Protect evidence, document incidents, and prioritize safety if the situation involves harm.",
                    "If you're dealing with abuse and need protection, contact local authorities or helplines who can advise on restraining orders and immediate safety planning. Your safety matters above all.",
                ]
            },
            'sad|grieve|loss|change|miss|goodbye|ending': {
                'responses': [
                    "Grief isn't just about people. You grieve relationships, jobs, phases of life, abilities, dreams that didn't happen. Whatever you're grieving, let yourself feel it fully. That's how you move through it, not around it. Sadness means something mattered to you.",
                    "Healing from loss is gradual. Some days hit harder than others, and that's okay. Gradually you integrate this loss into your story. You don't 'get over it,' you learn to carry it. That takes time, and patience, and often, community.",
                ]
            },
            'crisis|help|danger|hurt|harm|suicide|self-harm': {
                'responses': [
                    "If you're in crisis or having thoughts of self-harm, please reach out to someone immediately. National Suicide Prevention Lifeline: 988. Crisis Text Line: text HOME to 741741. Go to your nearest ER. Tell someone you trust. You deserve professional help, and it's available now. You're not alone in this.",
                    "Crises feel permanent, but they're not. With professional support, you can get through this. The pain you feel right now can be treated. Please reach out now. You matter more than you know.",
                ]
            },
            'decision|choose|hard choice|afraid|risk': {
                'responses': [
                    "Hard choices are scary because they involve risk and uncertainty. But getting stuck trying to avoid choice is also painful. Listen to your gut: what does it keep telling you? Usually, it's right. Trust yourself. Whatever you decide, you can handle the consequences and adjust as you learn.",
                    "You don't have to be certain before making a choice. Make the best decision you can with the information you have, then commit to it. Hesitation often comes from perfectionism, not from the wrong choice.",
                ]
            },
            'default': {
                'responses': [
                    "You're doing the best you can with what you have right now. That's enough. You don't have to be perfect to deserve rest, care, and compassion. Be as kind to yourself as you'd be to a friend going through this.",
                    "Tough times are temporary. You've survived 100% of your worst days. Whatever this is, you can get through it. Take it one moment, one hour, one day at a time. Better days are coming. 🌈",
                ]
            }
        }
    }
}

CHATBOT_RESPONSES = {
    'relationship': {
        'initial': "💙 I'm here to listen and support you through relationship challenges. Remember, all relationships go through ups and downs—that's completely normal. Let's talk about what's on your mind, and I'll do my best to help you navigate this.",
        'responses': [
            "I hear you. Relationships are one of the most complex parts of life. Here's something important: communicating how you feel honestly but respectfully is crucial. Try expressing your emotions without blame—use 'I feel...' instead of 'You always...' This opens dialogue instead of creating defensiveness. Also, remember that your partner isn't a mind reader; they need to understand what you need.",
            "That's really challenging to deal with. Take a moment to reflect: are you trying to change them, or are you trying to be heard? Often, relationship friction comes from unmet expectations. Have a calm conversation when you're both relaxed (not during conflict). Listen to their perspective too—understanding doesn't mean agreeing, but it builds connection. Small acts of kindness daily matter more than grand gestures.",
            "It's okay to feel hurt or disappointed. What's important now is: Do you want to work on this together, or do you need space to think? If you want to save this, consider talking to a couples therapist—that's not a sign of failure; it's a sign you care enough to get help. If you need space, that's valid too. Your mental health matters.",
            "I understand how confusing this is. Sometimes we stay in situations because of fear of change, not because things are good. Ask yourself: Are my needs being met? Am I growing or shrinking in this relationship? Do I feel respected? Your worth isn't determined by whether someone else stays—it's inherent. You deserve a relationship where you feel valued, safe, and supported.",
            "Relationships require effort from both sides. You can't pour from an empty cup—make sure you're taking care of yourself too. Spend time with friends, do things you love, maintain your hobbies. A healthy relationship enhances your life; it doesn't consume it. If you're constantly sacrificing yourself, it's worth examining whether this dynamic is sustainable.",
            "Love is important, but so is self-respect and boundaries. It's okay to say no. It's okay to need things. It's okay to walk away if it's hurting you. You're not selfish for prioritizing your wellbeing—you're wise. Whether you stay or leave, make sure it's a conscious choice, not desperation or fear. Whatever you decide, I'm here to support you.",
            "Remember: a good relationship should make you feel more like yourself, not less. If you're constantly anxious, questioning, or diminishing yourself, that's a red flag worth paying attention to. Trust your instincts. And please, if there's ever abuse (emotional, physical, or verbal), reach out to a counselor or trusted friend. You don't have to handle that alone.",
        ]
    },
    'friendship': {
        'initial': "👥 Friendships are one of life's greatest treasures, and it hurts when they feel strained or uncertain. I'm here to talk through what's happening and help you navigate this. Good friendships are worth investing in, but they also require honesty and care from both sides.",
        'responses': [
            "Friendship conflicts often come from misunderstandings or unmet expectations. The best first step? Have an honest conversation. Reach out and say something like: 'I've felt distant lately, and I miss you. Can we talk about what's going on?' Most people appreciate directness over silence. Be vulnerable about your feelings—it often opens the door for them to be vulnerable too.",
            "Sometimes friendships naturally evolve or drift apart, and that's okay. People grow in different directions, especially during life changes. But if this friendship matters to you, don't wait for them to reach out—be the one who takes the initiative. Send a message, suggest hanging out, show genuine interest in their life. Actions speak louder than words, and small, consistent efforts rebuild trust.",
            "It's painful when you feel like you're giving more than you're getting. Start by examining if your expectations are clear. Have you told them what you need? Sometimes people don't realize they're being neglectful. If you have communicated and nothing changes, you might need to accept that this friendship is in a different season. That doesn't make it less valuable; it just means it looks different now.",
            "Jealousy, competition, or feeling replaced can strain friendships deeply. Here's the truth: someone else's friendship cannot diminish the value of yours. Real friends celebrate each other's growth and additional connections. If you're worried they like someone else more, talk about it. You might discover it's just a different dynamic, not a replacement.",
            "Group friendships are tricky. Sometimes you feel left out or like the odd one out. First, check if this is real or if anxiety is amplifying things. Then, engage consistently. Join group activities, start conversations, initiate one-on-one hangouts. Show up genuinely. If the group is toxic or constantly excluding you, it's okay to spend your energy on people who reciprocate.",
            "Long-distance friendships require intention. Video calls, voice messages, sending small care packages—these keep bonds alive. But also be realistic: long-distance friendships change. You might not talk daily, and that's okay. When you do connect, make it meaningful. Quality over quantity applies to friendships too.",
            "Some friendships are seasonal, and that's not failure—it's life. You met them during a specific chapter, and whether you're still close or drifted, that friendship shaped you. Appreciate what you shared without guilt about growing apart. And remember: true friends, even if you don't talk for months, pick right back up. That's how you know it's real.",
        ]
    },
    'parents': {
        'initial': "👨‍👩‍👧 Family relationships are complex and deeply emotional. Parents are humans doing their best (even when it doesn't feel like it), and you have valid feelings about how they've treated you or are treating you. Let's talk about what's happening and how you can navigate this.",
        'responses': [
            "Parents often make mistakes because they're trying to parent the way they were parented, with their own unhealed wounds. That doesn't excuse harmful behavior, but it might help you understand it's not entirely about you. If there's a rift, consider: What do you need from them? Acknowledgment? Apology? Behavior change? Be specific. Vague hurt rarely leads to resolution.",
            "Sometimes parents just don't understand us—our choices, our values, our path. And that's hard. But here's the thing: you don't need their permission to live your life. You need their respect, and if they can't give that, you can set boundaries. Love doesn't mean accepting everything they do or say. You can love them AND maintain healthy distance if needed.",
            "Disagreements about life choices (career, relationships, lifestyle) are common. If this is your struggle, try this: Help them understand your reasoning calmly. 'I know this isn't what you wanted, but here's why this is right for me...' Listen to their concerns too. Often, parents' disapproval comes from fear, not malice. Reassure them, but stand firm in your decisions.",
            "If you're dealing with a parent's disappointment or criticism, know this: you are not responsible for their emotions. You're allowed to make choices that don't make them happy. It's their job to support you, not for you to live their unlived dreams. Set boundaries: 'I appreciate your opinion, but I need you to respect my choice.' Repeat as needed.",
            "Some parents are emotionally unavailable, critical, or even toxic. That hurts deeply—especially if you needed them and they weren't there. Healing this requires accepting you can't change them, only how you respond. Consider therapy to process this. You're not broken for needing emotional support; they were incomplete in providing it. That's their shortcoming, not yours.",
            "If you're an adult now, you can redefine your relationship with parents. You don't have to accept disrespect or control. You can set firm boundaries: 'I love you, but I won't tolerate [specific behavior].' If they can't respect that, you might need to reduce contact. Protecting your peace is not disrespect—it's self-preservation.",
            "If you're living at home or financially dependent, boundaries are trickier but still possible. Focus on what you can control. Be respectful but firm. Plan your independence so you're not trapped. And remember: moving away or creating distance doesn't mean you don't love them. Sometimes space is what relationships need to heal.",
        ]
    },
    'work': {
        'initial': "💼 Work stress is real and valid. Whether it's a difficult boss, toxic colleagues, burnout, or feeling undervalued, your mental and physical health matter more than any job. Let's talk about what's happening and explore ways to make this more manageable or decide if a change is needed.",
        'responses': [
            "Burnout is insidious—you might not even realize you have it until you're completely exhausted. Signs: dreading work, feeling cynical, losing motivation, physical symptoms like sleep issues or headaches. If this is you, something needs to change. Whether that's delegating, taking time off, setting boundaries, or finding a new job is up to you. But ignoring burnout only makes it worse. Your health comes first.",
            "A difficult boss can make or break your job satisfaction. First, try clear communication: document issues, address concerns professionally, be solution-focused. But if your boss is consistently disrespectful, manipulative, or abusive, no amount of great pay is worth it. Start looking for a new job. You'll be surprised how much lighter you feel when you're not dreading Mondays.",
            "Feeling undervalued at work is demoralizing. Step 1: Make your contributions visible. Document your achievements, speak up in meetings, ensure your boss knows what you're doing. Step 2: Have a conversation about growth and compensation. 'I've contributed X, Y, Z, and I'd like to discuss a raise/promotion.' If they don't recognize your value, other companies will. Don't stay where you're not appreciated.",
            "Toxic workplace culture drains your soul. If multiple coworkers are drama-filled or backstabbing, it's not your job to fix them. Protect your energy: keep conversations professional, don't engage in gossip, find allies, and set firm boundaries. But long-term? You shouldn't spend 40 hours a week in a hostile environment. Make an exit plan.",
            "If you're overworked with unrealistic expectations, speak up. 'I have X tasks with deadlines Y and Z. I can't do all of these well. Which are priorities?' Make them prioritize, not you. If they expect miracles with no resources, that's a management problem, not a you problem. You're not failing; the system is broken. Decide if this is worth your sanity.",
            "Imposter syndrome + work stress is a brutal combo. Remember: you were hired for a reason. You have skills and value, even if you feel like a fraud. Most high achievers feel this way—it means you care about doing good work. Trust that you belong there. If you genuinely lack skills, invest in learning. But don't let perfectionism diminish your progress.",
            "Your job is not your identity. I know society makes it feel that way, but you are more than your career. Whether you're struggling with work or thinking about making a change, remember this: you have worth regardless of productivity or achievement. Take breaks, pursue hobbies, spend time on relationships. A well-rounded life is more fulfilling than climbing a ladder that's against the wrong wall.",
        ]
    },
    'health': {
        'initial': "🏥 Health concerns can feel overwhelming and scary. Whether you're dealing with a new diagnosis, chronic illness, mental health challenges, or just general worry about your wellbeing, those feelings are completely valid. I'm here to listen and help you think through this.",
        'responses': [
            "If you're waiting for test results or a diagnosis, the uncertainty is often worse than the actual news. Right now, focus on what you *can* control: stay hydrated, sleep well, move your body gently, eat nourishing foods. Anxiety thrives on rumination—try redirecting your mind to the present moment. Your body is doing its best; trust the process and the professionals helping you.",
            "If you've received a diagnosis, take time to process. It's okay to feel scared, angry, or sad. Then, educate yourself—read about your condition, ask your doctor questions, find support communities. You're not the diagnosis; it's just one part of your health story. Many people live full, meaningful lives with various health conditions. This is manageable, even if it doesn't feel that way right now.",
            "Chronic pain or illness is grief—grief for the life you thought you'd have and the energy you've lost. That's real. Be gentle with yourself. Some days will be harder than others, and that's okay. Find small joys, adapt your activities, ask for help when you need it. Your worth isn't tied to productivity. You matter even when you're struggling with your health.",
            "Mental health is health. If you're dealing with anxiety, depression, OCD, or any mental health challenge, please, please reach out to a professional. A therapist or counselor can provide tools that actually help. There's no shame in this—it's just your brain needing support, like any other body part. You deserve to feel okay.",
            "If you're struggling with an eating disorder, body image, or unhealthy relationship with food/exercise, that's not shallow—it's serious and deeply painful. Professional help (therapist + dietitian) is crucial. Your body deserves nourishment and care, not punishment. Recovery is possible, and you deserve to feel peaceful around food and your body.",
            "Medication can be life-changing. If your doctor recommends it, try it openly. Yes, side effects are real, but they often improve over time. And if they don't, your doctor can adjust. Taking medication is not weakness—it's wisdom. Some brains need chemical support, just like some bodies need insulin or antibiotics. There's nothing wrong with that.",
            "Taking care of your health isn't selfish—it's foundational. You can't pour from an empty cup. Regular checkups, sleep, movement, stress management, social connection—these aren't luxuries; they're necessities. Your health enables everything else in your life. Invest in it fiercely. Your future self will thank you.",
        ]
    },
    'fitness': {
        'initial': "💪 Fitness motivation can be hard, especially if you're starting out, dealing with injury, or stuck in a plateau. Here's the truth: you're already winning by *thinking* about your health. Let's talk about what's blocking you and how to make this feel less like a chore and more like something you actually want to do.",
        'responses': [
            "If you're struggling to start, perfectionism is probably your enemy. You don't need the perfect plan, perfect body, or perfect gym. You need to show up imperfectly and consistently. Start with 10 minutes of movement you enjoy—a walk, dancing, yoga, whatever. The best workout is the one you'll actually do. Once it becomes a habit, you can expand.",
            "Hate the gym? You don't have to go! Humans are meant to move in ways we enjoy. Hiking, cycling, swimming, martial arts, rock climbing, soccer, dancing—find something that feels like play, not punishment. When exercise is enjoyable, you'll actually do it. Consistency beats intensity every time. A 30-minute walk you do 5 days a week beats a brutal 2-hour gym session you do once and quit.",
            "Plateau is frustrating, but it means your body has adapted. That's actually progress—your baseline improved! Now, change something: different exercises, higher intensity, different rep ranges, new environment. Your muscles need variety to keep growing. And remember: plateaus are temporary. Trust the process, stay consistent, and you'll break through.",
            "If you're dealing with injury, talk to a physical therapist before giving up. Often, you can modify exercises to work around the injury. Rest is important, but so is gentle movement. Complete inactivity actually slows recovery. A good PT can show you what's safe. You're not losing progress; you're building differently for a while.",
            "Soreness after starting is normal and temporary. Your muscles are adapting. Stretch, foam roll, get good sleep, stay hydrated, eat enough protein. Soreness will fade within a few days. But if it's pain (sharp, acute, lingering), that's different—don't push through that. There's a difference between good soreness and injury.",
            "You don't have to be 'gym-motivated' to get fit. Some people thrive with accountability (trainer, class, group fitness). Others prefer solo movement. Some need a specific goal (race, hike, belt test). Some just need to move because it feels good. Find *your* why. 'I should' never works as long-term motivation. What would make you excited to exercise?",
            "Progress isn't just aesthetic. Notice energy levels, sleep quality, mood, strength increases, or how your clothes fit. The scale is just one metric and often lies (muscle weighs more than fat). Also celebrate showing up when you didn't feel like it. That's the big win. You're building discipline, self-respect, and a healthier body. That's incredible and worth celebrating.",
        ]
    },
    'other': {
        'initial': "❓ Whatever you're going through, I want you to know: your feelings matter. Stress, confusion, overwhelm—these are all valid. Sometimes life is just hard, and that's okay. Let's talk about what's on your mind, and we'll work through it together.",
        'responses': [
            "When everything feels overwhelming, it's often because you're trying to handle too much at once. Take a breath. Write down everything that's worrying you. Then prioritize: What needs attention today? What can wait? What's actually not yours to worry about? You can't solve everything now. One step at a time. You're stronger than you think.",
            "Uncertainty is uncomfortable, but it's also where growth happens. You don't need to have all the answers right now. You can sit with the unknown while taking small steps forward. Ask for help, gather information, talk to people you trust. You don't have to figure this out alone. Asking for support is a sign of wisdom, not weakness.",
            "If you're in a crisis or having thoughts of self-harm, please reach out to a crisis helpline or mental health professional immediately. You're not alone, and you deserve help. There are people trained to support you through this: National Suicide Prevention Lifeline (988), Crisis Text Line (text HOME to 741741), or local emergency services.",
            "Grief, loss, and major life changes are hard. Whatever you're grieving—a relationship, a job, a phase of life, a person—let yourself feel it fully. Sadness isn't something to 'get over' quickly; it's something to move through. Talk about it, cry, journal, create art. And slowly, gradually, you'll integrate this into your life story.",
            "Sometimes we need to make hard choices: end something, start something, speak up, ask for help, walk away. These decisions are scary because they involve risk and uncertainty. But staying in bad situations 'to be safe' is also a risk. Listen to your gut. What does it keep telling you? Usually, it's right. Trust yourself.",
            "You're doing the best you can with what you have right now. That's enough. You don't have to be productive, perfect, or exceptional to deserve rest, care, and compassion. Please give yourself the grace you'd give a friend. You're probably harder on yourself than anyone else. Try to noticed when you're doing that and soften your self-criticism.",
            "Remember: tough times are temporary. You've survived 100% of your worst days so far. That's a 100% success rate. Whatever this is, you can get through it. Take it one moment, one hour, one day at a time. Reach out to people who care. Celebrate small wins. And trust that better days are coming. 🌈",
        ]
    }
}


def get_initial_response(reason):
    """Get the initial bot response based on the reason."""
    category = CONTEXTUAL_RESPONSES.get(reason, CONTEXTUAL_RESPONSES['other'])
    return category['initial']


def extract_keywords_from_message(message):
    """Extract relevant keywords/topics from user message for intelligent matching."""
    message_lower = message.lower()
    return message_lower


def extract_entities(message):
    """Lightweight entity extractor returning simple labels (friend, partner, boss, job, health, etc.)."""
    m = message.lower()
    entities = set()
    # relationship targets
    if re.search(r"\b(partner|boyfriend|girlfriend|husband|wife|partner|bf|gf)\b", m):
        entities.add('partner')
    if re.search(r"\b(friend|mate|buddy|pal)\b", m):
        entities.add('friend')
    if re.search(r"\b(parent|mom|dad|mother|father)\b", m):
        entities.add('parent')
    if re.search(r"\b(boss|manager|supervisor)\b", m):
        entities.add('boss')
    if re.search(r"\b(job|work|career|company|hire|fire|quit|resign)\b", m):
        entities.add('job')
    if re.search(r"\b(cheat|cheating|affair|infidelity)\b", m):
        entities.add('infidelity')
    if re.search(r"\b(break up|leave|dumped|split up|separate)\b", m):
        entities.add('breakup')
    if re.search(r"\b(health|doctor|diagnosis|medication|therapy|therapist)\b", m):
        entities.add('health')
    if re.search(r"\b(exercise|gym|fitness|workout)\b", m):
        entities.add('fitness')
    return entities


def analyze_message(message, intent_map=None):
    """Produce a lightweight structured analysis of the user's message.

    Returns a dict with: summary, entities, sentiment, likely_intent, causes, options, confidence
    """
    if intent_map is None:
        intent_map = {
            'is_question': False,
            'is_decision': False,
            'is_crisis': False,
        }
    m = message.strip()
    entities = extract_entities(m)

    # sentiment: simple heuristic
    negative_words = ['sad', 'angry', 'hurt', 'depressed', 'anxious', 'upset', 'lonely', 'stressed', 'overwhelmed', 'scared']
    positive_words = ['happy', 'good', 'better', 'relieved', 'ok', 'fine']
    neg = sum(1 for w in negative_words if re.search(r"\b" + re.escape(w) + r"\b", m.lower()))
    pos = sum(1 for w in positive_words if re.search(r"\b" + re.escape(w) + r"\b", m.lower()))
    sentiment = 'neutral'
    if neg > pos:
        sentiment = 'negative'
    elif pos > neg:
        sentiment = 'positive'

    # Likely causes: simple heuristics based on keywords
    causes = []
    if re.search(r"\b(misunderstand|miscommunication|misread|mixed signals)\b", m.lower()):
        causes.append('miscommunication')
    if re.search(r"\b(stress|work|busy|time)\b", m.lower()):
        causes.append('external stress / time pressures')
    if re.search(r"\b(jealous|insecure|self esteem|compare)\b", m.lower()):
        causes.append('internal insecurities')
    if not causes:
        causes.append('unclear — needs clarification')

    # Options: three pragmatic moves
    options = []
    if intent_map.get('is_decision'):
        options = [
            'Gather facts and pros/cons (small list).',
            'Ask for a short conversation to clarify intentions.',
            'Try a low-risk experiment (small step) to test the choice.'
        ]
    elif 'friend' in entities or 'partner' in entities or 'parent' in entities:
        options = [
            'Use an "I" statement to share how you feel.',
            'Ask a clarifying question to understand their view.',
            'If safety or abuse is present, prioritize boundaries and support.'
        ]
    elif 'job' in entities or 'boss' in entities:
        options = [
            'Document issues and set a short meeting to discuss priorities.',
            'Clarify what success looks like and ask for support.',
            'If necessary, quietly explore other roles while protecting income.'
        ]
    else:
        options = [
            'Describe the problem in one sentence to clarify it.',
            'Identify one small action you can take in the next 24 hours.',
            'If overwhelmed, ask for help or delegate one task.'
        ]

    # Confidence: how sure we are (based on explicit keywords)
    confidence = 0.5
    if entities:
        confidence += 0.2
    if intent_map.get('is_decision') or intent_map.get('is_question'):
        confidence += 0.1
    if sentiment == 'negative':
        confidence += 0.05
    confidence = min(0.95, confidence)

    # Short summary: strip to one sentence
    summary = m
    if len(summary) > 160:
        summary = summary[:157] + '...'

    return {
        'summary': summary,
        'entities': list(entities),
        'sentiment': sentiment,
        'likely_intent': ('decision' if intent_map.get('is_decision') else 'question' if intent_map.get('is_question') else 'talk'),
        'causes': causes,
        'options': options,
        'confidence': round(confidence, 2),
    }


def get_bot_response(reason, user_message, message_count=0):
    """
    Get a contextual bot response based on the user's actual message.
    Improved matching: use word-boundary regex to avoid substring false-positives,
    and combine the matched-topic responses with the broader response pool
    for the category to increase variety and coverage.
    """
    category = CONTEXTUAL_RESPONSES.get(reason, CONTEXTUAL_RESPONSES['other'])
    topics = category.get('topics', {})
    message_lower = user_message.lower()

    # Quick greeting handling: treat short 'hello' variants as a prompt to open the conversation
    try:
        if re.search(r"\b(hi|hello|hey|helo|hiya|howdy)\b", message_lower) and len(message_lower.strip()) < 40:
            greetings = [
                "Hey — I'm here. What's on your mind? How can I help?",
                "Hi there! What's the problem you'd like to talk about?",
                "Hello — I'm listening. What's been going on?",
            ]
            return greetings[message_count % len(greetings)]
    except re.error:
        pass

    # Simple intent detection
    def detect_intent(msg_l):
        intent = {
            'is_question': bool(re.search(r"\b(why|how|what|when|where|should|can|could|would)\b", msg_l)),
            'is_decision': bool(re.search(r"\b(should i|should we|leave|break up|quit|resign|ask for|tell them|confront|report|file|apply)\b", msg_l)),
            'is_crisis': bool(re.search(r"\b(suicide|kill myself|self harm|hurt myself|danger|abuse)\b", msg_l)),
        }
        return intent

    intent = detect_intent(message_lower)

    # Structured analysis of the user's message
    analysis = analyze_message(user_message, intent)

    # Small response composer to make replies more thoughtful (pros/cons, clarifying Qs, empathy)
    def compose_response(base_text, intent_map, user_msg, matched_any=False, analysis=None):
        msg = base_text.strip()
        if analysis is None:
            analysis = analyze_message(user_msg, intent_map)

        # If crisis, keep crisis override handled elsewhere
        if intent_map.get('is_crisis'):
            return msg

        # Empathy/validation for emotional words
        if re.search(r"\b(sad|upset|angry|hurt|lonely|depressed|anxious|stressed)\b", user_msg.lower()):
            empathy = "I can tell this feels heavy. It's okay to feel that way — you're not alone.\n"
            # if base_text already contains empathy, avoid duplicating
            if empathy.strip() not in msg:
                msg = empathy + msg

        # If it's a decision-style message, add short pros/cons and a next-action suggestion
        if intent_map.get('is_decision'):
            snippet = user_msg.strip()
            if len(snippet) > 100:
                snippet = snippet[:97] + '...'
            # tailor pros/cons based on entities
            entities = extract_entities(user_msg)
            if 'job' in entities or 'boss' in entities:
                pros = "Pros:\n- You might gain clarity, less stress, or a role that fits you better.\n"
                cons = "Cons:\n- Financial uncertainty, transition time, and a period of adjustment.\n"
                next_steps = "Next steps:\n1) List must-haves for a new role.\n2) Update resume and quietly explore options.\n"
            elif 'friend' in entities or 'partner' in entities or 'infidelity' in entities or 'breakup' in entities:
                pros = "Pros:\n- Opening up could restore closeness or give you peace of mind.\n"
                cons = "Cons:\n- It may feel vulnerable and could lead to hard conversations.\n"
                next_steps = "Next steps:\n1) Pick a calm time to talk.\n2) Use 'I' statements and ask for their view.\n"
            else:
                pros = "Pros:\n- What could go well if you choose this option.\n"
                cons = "Cons:\n- What might be hard or risky.\n"
                next_steps = "Next steps:\n1) Reflect briefly on which matters most to you.\n2) Try a small experiment where possible.\n"
            msg = f"I hear you're weighing: {snippet}\n\n" + pros + cons + next_steps
            # include a short structured analysis
            if analysis:
                opt_lines = '\n'.join([f"- {o}" for o in analysis.get('options', [])[:3]])
                msg += f"\nQuick options:\n{opt_lines}\n\nConfidence: {analysis.get('confidence')}"
            return msg

        # If user asked a question, provide concise answer + follow-up question
        if intent_map.get('is_question'):
            follow = "Would you like a short plan to try this?"
            msg = f"{msg}\n\n{follow}"
            if analysis:
                msg += f"\n\nSummary: {analysis.get('summary')}"
            return msg

        # If matched a keyword and base_text is short, expand with a quick actionable tip
        if matched_any and len(msg) < 120:
            action = "A simple step you can try now: pick one small action and do it within the next 24 hours."
            msg = f"{msg}\n\n{action}"
            if analysis:
                msg += f"\n\nLikely causes: {', '.join(analysis.get('causes', []))}."

        # Default: return message with an open offer to continue and structured analysis
        extra = ''
        if analysis:
            extra = f"\n\nSummary: {analysis.get('summary')}\nLikely causes: {', '.join(analysis.get('causes', []))}.\nOptions: {', '.join(analysis.get('options', [])[:3])}\nConfidence: {analysis.get('confidence')}"
        return msg + "\n\nIf you'd like, tell me more or ask a specific question." + extra

    # Build keyword -> responses and response -> keywords maps
    keyword_index = {}
    response_to_keywords = {}
    for keywords_pattern, topic_data in topics.items():
        if keywords_pattern == 'default':
            continue
        keywords = [k.strip() for k in keywords_pattern.split('|') if k.strip()]
        for keyword in keywords:
            keyword_index.setdefault(keyword, []).extend(topic_data.get('responses', []))
            for r in topic_data.get('responses', []):
                response_to_keywords.setdefault(r, set()).add(keyword)

    # Candidate responses: gather unique responses from topic order then static pool then default
    static_pool = CHATBOT_RESPONSES.get(reason, {}).get('responses', [])
    candidates = []
    for keywords_pattern, topic_data in topics.items():
        if keywords_pattern == 'default':
            continue
        for r in topic_data.get('responses', []):
            if r not in candidates:
                candidates.append(r)
    for r in static_pool:
        if r not in candidates:
            candidates.append(r)
    for r in topics.get('default', {}).get('responses', []):
        if r not in candidates:
            candidates.append(r)

    # Text utilities for similarity
    STOPWORDS = set(["the","is","and","a","an","to","it","in","on","for","of","that","this","i","you","me","my","we","they","be","are"])

    def tokenize(text):
        text = re.sub(r"[^a-z0-9\s]", " ", text.lower())
        tokens = [t for t in text.split() if t and t not in STOPWORDS]
        return tokens

    def vec_from_tokens(tokens):
        return Counter(tokens)

    def cosine_sim(c1, c2):
        if not c1 or not c2:
            return 0.0
        dot = 0
        for k, v in c1.items():
            dot += v * c2.get(k, 0)
        mag1 = math.sqrt(sum(v * v for v in c1.values()))
        mag2 = math.sqrt(sum(v * v for v in c2.values()))
        if mag1 == 0 or mag2 == 0:
            return 0.0
        return dot / (mag1 * mag2)

    msg_tokens = tokenize(user_message)
    msg_vec = vec_from_tokens(msg_tokens)

    # Score each candidate by weighted combination: 6*exact_hits + 3*sim_keywords + 1*sim_response
    best_score = 0.0
    best_candidate = None
    for cand in candidates:
        kws = response_to_keywords.get(cand, set())
        exact_hits = 0
        for kw in kws:
            try:
                if re.search(r"\b" + re.escape(kw) + r"\b", message_lower):
                    exact_hits += 1
            except re.error:
                if kw in message_lower:
                    exact_hits += 1

        kw_text = ' '.join(kws) if kws else ''
        kw_vec = vec_from_tokens(tokenize(kw_text))
        sim_kw = cosine_sim(msg_vec, kw_vec)

        cand_vec = vec_from_tokens(tokenize(cand))
        sim_resp = cosine_sim(msg_vec, cand_vec)

        score = 6 * exact_hits + 3 * sim_kw + 1 * sim_resp
        if score > best_score:
            best_score = score
            best_candidate = cand

    SCORE_THRESHOLD = 0.5
    if best_candidate and best_score >= SCORE_THRESHOLD:
        if intent.get('is_crisis'):
            crisis_msgs = CONTEXTUAL_RESPONSES['other']['topics'].get('crisis', {}).get('responses', [])
            if crisis_msgs:
                return crisis_msgs[0]
        composed = compose_response(best_candidate, intent, user_message, matched_any=(best_score >= 2), analysis=analysis)
        final = (f"Analysis:\nSummary: {analysis.get('summary')}\nEntities: {', '.join(analysis.get('entities', [])) or 'none'}\n"
             f"Likely intent: {analysis.get('likely_intent')}\nConfidence: {analysis.get('confidence')}\n\n{composed}")
        return final

    # If no exact keyword hit, fallback to previous strategy: default topic + broader static pool
    best_match_responses = topics.get('default', {}).get('responses', [])
    static_pool = CHATBOT_RESPONSES.get(reason, {}).get('responses', [])
    combined = []
    for r in (best_match_responses + static_pool):
        if r not in combined:
            combined.append(r)

    if combined:
        index = message_count % len(combined)
        chosen = combined[index]
        composed = compose_response(chosen, intent, user_message, matched_any=False, analysis=analysis)
        if intent.get('is_crisis'):
            crisis_msgs = CONTEXTUAL_RESPONSES['other']['topics'].get('crisis', {}).get('responses', [])
            if crisis_msgs:
                return crisis_msgs[0]
        final = (f"Analysis:\nSummary: {analysis.get('summary')}\nEntities: {', '.join(analysis.get('entities', [])) or 'none'}\n"
                 f"Likely intent: {analysis.get('likely_intent')}\nConfidence: {analysis.get('confidence')}\n\n{composed}")
        return final

    return "I hear you—could you tell me a bit more about that? I'm listening."
