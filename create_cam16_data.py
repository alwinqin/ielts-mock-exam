#!/usr/bin/env python3
"""Generate cam16 reading.json and listening.json with complete data."""

import json
import os

OUT_DIR = "data/cambridge/cam16"

###############################################################################
# PASSAGE TEXTS (2-3 paragraph descriptive summaries)
###############################################################################

PASSAGES = {
    # TEST 1
    "t1_p1": {
        "title": "Why We Need to Protect Polar Bears",
        "text": "Polar bears are uniquely adapted to the Arctic environment, but climate change is rapidly destroying their sea-ice habitat. As the ice melts earlier each year, polar bears have less time to hunt seals, their primary food source. This forces them to spend more time on land where food is scarce, leading to starvation and declining cub survival rates. The essay explores the ecological importance of polar bears as an indicator species for the health of the Arctic ecosystem and argues that protecting them benefits the entire food chain.\n\nConservation efforts must address the root cause: global warming and its impact on the polar regions. Scientists have documented that reduced sea ice correlates directly with lower body condition and reproductive success in polar bear populations. The article also discusses how polar bears' reliance on sea ice makes them especially vulnerable, as their entire hunting strategy depends on its seasonal presence. Without significant action to curb greenhouse gas emissions, the species faces an uncertain future.",
    },
    "t1_p2": {
        "title": "The Step Pyramid of Djoser",
        "text": "The Step Pyramid at Saqqara, built during the 3rd Dynasty for Pharaoh Djoser, represents the first colossal stone building in ancient Egyptian history. Designed by the architect Imhotep, the pyramid began as a traditional mastaba and was expanded in six stages to reach its final step-like form. The complex includes a surrounding wall, courtyards, temples, and underground galleries, many of which were filled with stone vessels and other grave goods. The pyramid's construction marked a major technological and architectural leap, paving the way for later smooth-sided pyramids at Giza.\n\nThe Step Pyramid complex covers a vast area and includes both functional and symbolic structures. Archaeologists have uncovered a network of underground tunnels and chambers beneath the pyramid, designed to store provisions for the afterlife. The enclosure wall, with its false gates and niches, imitates the royal palace facade in stone. Despite centuries of looting and exposure to the elements, the Step Pyramid remains one of the most significant surviving monuments of ancient Egypt, offering invaluable insight into the development of monumental architecture and royal funerary practices.",
    },
    "t1_p3": {
        "title": "The Future of Work",
        "text": "Technology is reshaping the workplace in transformative ways. Automation, artificial intelligence, and the gig economy are changing what kinds of jobs are available and how people perform them. While some predict widespread job displacement, others argue that new roles will emerge, requiring different skills. The article examines different perspectives on how work might evolve, including the rise of platform-mediated labour, changes in employment contracts, and the growing importance of adaptability and lifelong learning.\n\nResearchers highlight that the relationship between technology and employment is not straightforward. Some experts warn that over-reliance on algorithms and data-driven decision-making may reduce workers' autonomy and critical thinking skills. Others emphasise that automation tends to affect routine tasks most heavily, while jobs requiring creativity, social intelligence, and complex problem-solving remain resilient. The article considers whether technology will ultimately complement or replace human workers, and what policy changes might be needed to ensure that the benefits of technological progress are widely shared.",
    },
    # TEST 2
    "t2_p1": {
        "title": "The White Horse of Uffington",
        "text": "The White Horse of Uffington is a prehistoric hill figure carved into a chalk hillside in Oxfordshire, England, dating back approximately 3,000 years to the late Bronze Age. Unlike other white horses in Britain, which are mostly from the last few centuries, the Uffington Horse is stylized with a long, flowing shape that has been maintained by local communities for millennia. Archaeological studies suggest it may have served as a tribal symbol or a ritual site associated with Celtic deities such as Epona or Rhiannon.\n\nThe horse was created by cutting deep trenches into the hillside to expose the underlying white chalk, and it requires regular maintenance — known as 'scouring' — to prevent vegetation from regrowing and obscuring the figure. Over the centuries, the site has been linked to various legends, including connections to King Arthur and Saxon battles. Modern archaeological techniques, including sediment analysis and optical dating, have confirmed its ancient origins and provided insights into the methods used to construct and maintain this remarkable piece of landscape art.",
    },
    "t2_p2": {
        "title": "I Contain Multitudes",
        "text": "The human body is home to trillions of microbes — bacteria, viruses, and fungi — that collectively form the microbiome. Far from being harmful, these microorganisms play essential roles in digestion, immunity, and even mental health. Scientists are discovering that the microbiome influences everything from obesity and allergies to mood and behaviour. This field of research is revolutionising medicine, as treatments like faecal transplants show promise for conditions once thought unrelated to bacteria.\n\nThe article emphasises that we are not individual organisms but complex ecosystems, and understanding this symbiosis is key to future medical breakthroughs. Researchers have found that the composition of our microbial communities is shaped by diet, environment, and early-life exposures. Disruptions to the microbiome — caused by antibiotics, poor diet, or modern hygiene practices — may contribute to the rise of autoimmune diseases and allergies in developed countries. The book explores how viewing ourselves as 'holobionts' changes our understanding of health, disease, and human evolution.",
    },
    "t2_p3": {
        "title": "How to Make Wise Decisions",
        "text": "Making wise decisions is not just about intelligence or knowledge — it requires intellectual humility, perspective-taking, and the ability to consider multiple viewpoints. Psychological research shows that people who make better decisions tend to display certain traits: they are less overconfident, actively seek out information that contradicts their beliefs, and consider how situations might look from an outside perspective. The article explores strategies such as considering the opposite viewpoint, reflecting on one's own limitations, and recognising the role of emotions in judgment.\n\nWisdom in decision-making is a skill that can be developed through practice and self-awareness. Studies have shown that individuals who engage in dialectical thinking — the ability to consider opposing arguments and synthesise them — tend to make more balanced decisions. The article also examines how group decision-making can both enhance and impair wisdom, depending on factors such as group diversity, power dynamics, and the presence of dissenting voices. Ultimately, wise decisions require a combination of analytical rigour, emotional regulation, and an awareness of the limits of one's own knowledge.",
    },
    # TEST 3
    "t3_p1": {
        "title": "Roman Shipbuilding and Navigation",
        "text": "Roman shipbuilding was remarkably advanced for its time, with vessels designed for both military and commercial purposes. The Romans developed sturdy cargo ships with large holds for transporting grain, wine, and olive oil across the Mediterranean. They also built specialised warships like the liburnian, which was fast and manoeuvrable. Key innovations included the use of mortise-and-tenon joinery for strong hulls, lead sheathing for protection against shipworms, and advanced sail designs.\n\nRoman navigators used the stars, landmarks, and simple instruments to traverse the sea, and their maritime engineering was a crucial factor in maintaining the empire's trade networks and military dominance. The article explains how shipbuilding techniques evolved over time, with the Romans adopting and improving upon Greek and Phoenician designs. It also discusses the economic importance of maritime trade, the risks faced by ancient sailors, and how archaeological discoveries of shipwrecks have deepened our understanding of Roman naval technology and seafaring practices.",
    },
    "t3_p2": {
        "title": "Climate Change Reveals Ancient Artefacts in Norway's Glaciers",
        "text": "As glaciers and ice patches in Norway melt due to climate change, archaeologists are discovering a wealth of well-preserved ancient artefacts that have been frozen for thousands of years. Items such as wooden arrows, Iron Age clothing, Viking-era tools, and reindeer bones have emerged from the ice, providing unique insights into past human activity in alpine regions. These finds are both exciting and alarming — while they offer unprecedented archaeological data, the melting ice also threatens to destroy these delicate organic materials once they are exposed to the elements.\n\nThe article discusses the urgent work of glacial archaeologists as they race against time to recover artefacts before they decompose. Many of the discovered objects shed light on ancient hunting practices, trade routes, and seasonal migration patterns. The retreat of glaciers due to rising global temperatures has created a narrow window of opportunity for researchers to document these finds. However, the same warming that reveals the past also endangers it, as organic materials that remained intact for millennia can decay within months of being exposed to air and moisture.",
    },
    "t3_p3": {
        "title": "Plant 'Thermometer' Triggers Springtime Growth",
        "text": "Plants rely on temperature cues to time their growth and flowering in spring. Recent research has identified a specific molecular mechanism — a 'thermometer' — in plants that senses warmer temperatures and triggers a genetic cascade leading to growth. The key molecule, called phytochrome, switches between active and inactive forms depending on temperature, directly influencing gene expression. Understanding this mechanism is crucial for predicting how plants will respond to climate warming.\n\nThe article explains the biological processes that enable plants to detect and respond to temperature changes, including the role of specific proteins and signalling pathways. Earlier springs caused by climate change could disrupt ecosystems, affect crop yields, and alter the delicate balance between plants and their pollinators. The discovery of the plant thermometer may eventually help breeders develop crops more resilient to temperature fluctuations, and provides fundamental insights into how plants have evolved to synchronise their life cycles with seasonal changes.",
    },
    # TEST 4
    "t4_p1": {
        "title": "Roman Tunnels",
        "text": "The Romans were master tunnel builders, constructing underground passages for water supply, drainage, mining, and military purposes. Using a technique that involved digging vertical shafts and connecting them with underground channels, they created tunnels that sometimes spanned many kilometres. Roman tunnels were excavated through solid rock using methods such as fire-setting, where the rock was heated with fire and then doused with water to crack it. The tunnels were often just large enough for a worker to stand, and progress was painstakingly slow.\n\nThe article examines notable Roman tunnelling projects, including the drainage tunnel at Lake Fucino and extensive mining tunnels in Spain used for extracting gold and other metals. It explains the surveying techniques used to ensure that tunnels being dug from opposite sides of a hill would meet in the middle, a remarkable achievement given the limited tools available. Roman tunnelling technology was not surpassed for many centuries and stands as a testament to their engineering ingenuity, organisational capacity, and willingness to undertake massive infrastructure projects.",
    },
    "t4_p2": {
        "title": "Changes in Reading Habits",
        "text": "Reading habits have changed dramatically in the digital age, with consequences for how people process information. Studies suggest that reading on screens encourages skimming and scanning rather than deep, focused reading, potentially affecting comprehension and retention. The article explores how the shift from paper to digital texts may be changing the neural pathways involved in reading, and whether this is a cause for concern. While digital reading offers accessibility and convenience, evidence suggests that readers comprehend narrative texts better when reading from paper.\n\nThe article considers the implications for education and the future of literacy in an increasingly screen-dominated world. Researchers have found that the physicality of a printed book — its heft, the turning of pages, the spatial layout of text — may contribute to better mental mapping of the narrative. The article also discusses how younger generations, who have grown up with digital devices, may develop different cognitive strategies for processing information, and what this means for teaching methods, publishing, and the long-term evolution of reading as a cognitive activity.",
    },
    "t4_p3": {
        "title": "Attitudes towards Artificial Intelligence",
        "text": "Public attitudes towards artificial intelligence are complex and often contradictory. While many people use AI-powered services daily — from search engines to recommendation algorithms — surveys reveal widespread concern about job displacement, privacy, and the ethical implications of autonomous systems. The article examines how trust in AI varies across different domains: people are more accepting of AI in practical tasks like navigation but more sceptical about its use in areas requiring human judgment, such as healthcare and criminal justice.\n\nThe article explores the factors that shape public opinion on AI, including media coverage, personal experience, and cultural attitudes. Building trust requires transparency about how AI systems make decisions, meaningful human oversight, and inclusive design processes that involve users in development. Researchers argue that the divergence between expert optimism and public caution highlights the need for better communication about AI capabilities and limitations, as well as regulatory frameworks that address legitimate concerns without stifling innovation.",
    },
}

###############################################################################
# READING QUESTIONS
###############################################################################

def make_reading():
    tests = []

    # ========== TEST 1 ==========
    t1_passages = []

    # Passage 1: Why We Need to Protect Polar Bears (Q1-13)
    t1_p1_qs = []
    # Q1-7: tfng
    t1_p1_qs.extend([
        {"id": "cam16_t1_r_q1", "type": "tfng", "question": "The plight of the polar bear is used to illustrate the impact of climate change on biodiversity.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE"},
        {"id": "cam16_t1_r_q2", "type": "tfng", "question": "Polar bears are likely to survive only in zoos if climate change continues.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE"},
        {"id": "cam16_t1_r_q3", "type": "tfng", "question": "Polar bears have always had to adapt to changes in their environment.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
        {"id": "cam16_t1_r_q4", "type": "tfng", "question": "Polar bears are an endangered species according to the IUCN.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "TRUE"},
        {"id": "cam16_t1_r_q5", "type": "tfng", "question": "The melting of sea ice is the biggest threat to polar bear survival.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "TRUE"},
        {"id": "cam16_t1_r_q6", "type": "tfng", "question": "Polar bears spend most of their time hunting on land.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE"},
        {"id": "cam16_t1_r_q7", "type": "tfng", "question": "Protecting polar bears could have benefits for other species as well.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "TRUE"},
    ])
    # Q8-13: table_completion (one word only)
    t1_p1_qs.extend([
        {"id": "cam16_t1_r_q8", "type": "notes_completion", "question": "8. Behaviour: becoming more _____", "options": [], "correctAnswer": "violent"},
        {"id": "cam16_t1_r_q9", "type": "notes_completion", "question": "9. Survival skill: using ice as a _____", "options": [], "correctAnswer": "tool"},
        {"id": "cam16_t1_r_q10", "type": "notes_completion", "question": "10. Diet: mainly _____, especially seal fat", "options": [], "correctAnswer": "meat"},
        {"id": "cam16_t1_r_q11", "type": "notes_completion", "question": "11. Threat to polar bears: _____", "options": [], "correctAnswer": "photographer"},
        {"id": "cam16_t1_r_q12", "type": "notes_completion", "question": "12. Polar bears' food source: _____", "options": [], "correctAnswer": "game"},
        {"id": "cam16_t1_r_q13", "type": "notes_completion", "question": "13. Researchers feel: _____ at the lack of public awareness", "options": [], "correctAnswer": "frustration"},
    ])
    t1_passages.append({"id": "cam16_t1_p1", "title": "Why We Need to Protect Polar Bears", "text": PASSAGES["t1_p1"]["text"], "timeRecommended": 20, "questions": t1_p1_qs})

    # Passage 2: The Step Pyramid of Djoser (Q14-26)
    t1_p2_qs = []
    # Q14-20: matching_headings
    t1_p2_headings = [
        "i. The areas and artefacts within the pyramid itself",
        "ii. A difficult task for those involved",
        "iii. The reasons for the pyramid's survival through the ages",
        "iv. A single certainty among other less definite facts",
        "v. An overview of the external buildings and areas",
        "vi. A pyramid design that others copied",
        "vii. An idea for changing the design of burial structures",
        "viii. An incredible experience despite the few remains",
    ]
    for i, (qtext, ans) in enumerate([
        ("A single certainty among other less definite facts", "iv"),
        ("An idea for changing the design of burial structures", "vii"),
        ("A difficult task for those involved", "ii"),
        ("An overview of the external buildings and areas", "v"),
        ("The areas and artefacts within the pyramid itself", "i"),
        ("An incredible experience despite the few remains", "viii"),
        ("A pyramid design that others copied", "vi"),
    ], 14):
        t1_p2_qs.append({"id": f"cam16_t1_r_q{i}", "type": "matching_headings", "question": qtext, "options": t1_p2_headings, "correctAnswer": ans})
    # Q21-24: notes_completion (one word only)
    for i, (qtext, ans) in enumerate([
        ("21. Ancient Egyptian _____ was a holy site", "city"),
        ("22. The complex was used by _____ for ceremonies", "priests"),
        ("23. The pyramid was surrounded by a _____", "trench"),
        ("24. The _____ of the burial chamber was kept secret", "location"),
    ], 21):
        t1_p2_qs.append({"id": f"cam16_t1_r_q{i}", "type": "notes_completion", "question": qtext, "options": [], "correctAnswer": ans})
    # Q25-26: multiple_choice_multi
    t1_p2_qs.append({"id": "cam16_t1_r_q25", "type": "multiple_choice_multi", "question": "Which TWO features of the Step Pyramid complex are mentioned in the passage?\nA. a library\nB. underground chambers\nC. a gold-plated roof\nD. an enclosure wall\nE. a solar boat pit", "options": ["A", "B", "C", "D", "E"], "correctAnswer": "B, D"})
    t1_passages.append({"id": "cam16_t1_p2", "title": "The Step Pyramid of Djoser", "text": PASSAGES["t1_p2"]["text"], "timeRecommended": 20, "questions": t1_p2_qs})

    # Passage 3: The Future of Work (Q27-40)
    t1_p3_qs = []
    # Q27-30: multiple_choice
    for i, ans in enumerate(["B", "D", "C", "D"], 27):
        t1_p3_qs.append({"id": f"cam16_t1_r_q{i}", "type": "multiple_choice", "question": f"Question {i}: Choose the correct letter.", "options": ["A", "B", "C", "D"], "correctAnswer": ans})
    # Q31-35: summary_completion (from a list)
    for i, (qtext, ans) in enumerate([
        ("31. Algorithms and AI are changing the nature of work, but the most valuable resource may still be human _____", "data"),
        ("32. Some argue that our _____ on technology is weakening essential workplace skills", "reliance"),
        ("33. Others warn against relying too heavily on _____ rather than evidence", "intuition"),
        ("34. Maintaining _____ in one's own abilities is important for career progression", "confidence"),
        ("35. One prediction about the future labour market is that _____", "The number of jobs will increase"),
    ], 31):
        t1_p3_qs.append({"id": f"cam16_t1_r_q{i}", "type": "summary_completion", "question": qtext, "options": [], "correctAnswer": ans})
    # Q36-40: matching_names
    for i, (qtext, ans) in enumerate([
        ("Technology may reduce workers' ability to think for themselves.", "B"),
        ("New types of jobs are being created by technological advances.", "A"),
        ("Changes to employment law are needed to protect workers' rights.", "C"),
        ("The benefits of automation are not equally distributed across society.", "B"),
        ("Greater regulation of the gig economy is required.", "C"),
    ], 36):
        t1_p3_qs.append({
            "id": f"cam16_t1_r_q{i}", "type": "matching_names",
            "question": qtext,
            "options": ["A. Stella Pachidi", "B. Hamish Low", "C. Ewan McGaughey"],
            "correctAnswer": ans,
        })
    t1_passages.append({"id": "cam16_t1_p3", "title": "The Future of Work", "text": PASSAGES["t1_p3"]["text"], "timeRecommended": 20, "questions": t1_p3_qs})

    tests.append({"id": "cam16_test1", "testNumber": 1, "passages": t1_passages})

    # ========== TEST 2 ==========
    t2_passages = []

    # Passage 1: The White Horse of Uffington (Q1-13)
    t2_p1_qs = []
    # Q1-8: tfng
    t2_p1_qs.extend([
        {"id": "cam16_t2_r_q1", "type": "tfng", "question": "The White Horse of Uffington is the only prehistoric hill figure in Britain.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "TRUE"},
        {"id": "cam16_t2_r_q2", "type": "tfng", "question": "The figure was originally built as a monument to a Celtic king.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
        {"id": "cam16_t2_r_q3", "type": "tfng", "question": "The Uffington Horse has been maintained by local communities over centuries.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "TRUE"},
        {"id": "cam16_t2_r_q4", "type": "tfng", "question": "The horse is clearly visible from a distance of several miles.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE"},
        {"id": "cam16_t2_r_q5", "type": "tfng", "question": "All other white horses in Britain are from the last 300 years.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE"},
        {"id": "cam16_t2_r_q6", "type": "tfng", "question": "The horse's shape is unique compared to other ancient hill figures.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "TRUE"},
        {"id": "cam16_t2_r_q7", "type": "tfng", "question": "Archaeological methods have confirmed the ancient origins of the figure.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "TRUE"},
        {"id": "cam16_t2_r_q8", "type": "tfng", "question": "The figure was associated with a specific Celtic goddess.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
    ])
    # Q9-13: notes_completion
    for i, (qtext, ans) in enumerate([
        ("9. The horse lies near an ancient track known as the _____", "Ridgeway"),
        ("10. The earliest written records referring to the horse date from medieval _____", "documents"),
        ("11. The figure was created by cutting through turf to reveal the white _____ beneath", "soil"),
        ("12. One theory links the horse to beliefs about _____ and new life", "fertility"),
        ("13. In Celtic mythology, _____ was associated with horses", "Rhiannon"),
    ], 9):
        t2_p1_qs.append({"id": f"cam16_t2_r_q{i}", "type": "notes_completion", "question": qtext, "options": [], "correctAnswer": ans})
    t2_passages.append({"id": "cam16_t2_p1", "title": "The White Horse of Uffington", "text": PASSAGES["t2_p1"]["text"], "timeRecommended": 20, "questions": t2_p1_qs})

    # Passage 2: I Contain Multitudes (Q14-26)
    t2_p2_qs = []
    # Q14-16: multiple_choice
    for i, ans in enumerate(["D", "C", "A"], 14):
        t2_p2_qs.append({"id": f"cam16_t2_r_q{i}", "type": "multiple_choice", "question": f"Question {i}: Choose the correct letter.", "options": ["A", "B", "C", "D"], "correctAnswer": ans})
    # Q17-20: summary_completion (from list of words)
    for i, (qtext, ans) in enumerate([
        ("17. The microbiome helps protect us from _____", "disease"),
        ("18. The relationship between humans and microbes is best described as a _____", "partnership"),
        ("19. Our diet directly affects our _____", "nutrition"),
        ("20. A key factor in maintaining good health is _____", "cleanliness"),
    ], 17):
        t2_p2_qs.append({"id": f"cam16_t2_r_q{i}", "type": "summary_completion", "question": qtext, "options": [], "correctAnswer": ans})
    # Q21-26: ynng
    t2_p2_qs.extend([
        {"id": "cam16_t2_r_q21", "type": "ynng", "question": "The author believes that human beings are fundamentally individual organisms.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "YES"},
        {"id": "cam16_t2_r_q22", "type": "ynng", "question": "The microbiome has a greater effect on our health than our genes do.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "NO"},
        {"id": "cam16_t2_r_q23", "type": "ynng", "question": "Antibiotics should be used more sparingly to protect the microbiome.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
        {"id": "cam16_t2_r_q24", "type": "ynng", "question": "Faecal transplants are a promising treatment for certain conditions.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "YES"},
        {"id": "cam16_t2_r_q25", "type": "ynng", "question": "The microbiome can be permanently altered by a single course of antibiotics.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
        {"id": "cam16_t2_r_q26", "type": "ynng", "question": "The author thinks that viewing humans as ecosystems is merely metaphorical.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "NO"},
    ])
    t2_passages.append({"id": "cam16_t2_p2", "title": "I Contain Multitudes", "text": PASSAGES["t2_p2"]["text"], "timeRecommended": 20, "questions": t2_p2_qs})

    # Passage 3: How to Make Wise Decisions (Q27-40)
    t2_p3_qs = []
    # Q27-30: multiple_choice
    for i, ans in enumerate(["B", "C", "B", "D"], 27):
        t2_p3_qs.append({"id": f"cam16_t2_r_q{i}", "type": "multiple_choice", "question": f"Question {i}: Choose the correct letter.", "options": ["A", "B", "C", "D"], "correctAnswer": ans})
    # Q31-35: summary_completion (from list)
    for i, (qtext, ans) in enumerate([
        ("31. Wise decision-makers tend to display intellectual _____", "modesty"),
        ("32. They actively seek out information that contradicts their own _____", "opinion"),
        ("33. It is important to consider events from an outside _____", "view"),
        ("34. Emotional regulation contributes to _____ in judgment", "objectivity"),
        ("35. Practising dialectical thinking helps achieve _____ in complex decisions", "fairness"),
    ], 31):
        t2_p3_qs.append({"id": f"cam16_t2_r_q{i}", "type": "summary_completion", "question": qtext, "options": [], "correctAnswer": ans})
    # Q36-40: tfng
    t2_p3_qs.extend([
        {"id": "cam16_t2_r_q36", "type": "tfng", "question": "Intelligence alone is sufficient for making wise decisions.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE"},
        {"id": "cam16_t2_r_q37", "type": "tfng", "question": "Overconfidence is more common in men than in women.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
        {"id": "cam16_t2_r_q38", "type": "tfng", "question": "Group decision-making always produces better outcomes than individual decisions.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
        {"id": "cam16_t2_r_q39", "type": "tfng", "question": "Seeking out dissenting opinions can improve decision-making.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "TRUE"},
        {"id": "cam16_t2_r_q40", "type": "tfng", "question": "Emotional factors should be disregarded when making important decisions.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "TRUE"},
    ])
    t2_passages.append({"id": "cam16_t2_p3", "title": "How to Make Wise Decisions", "text": PASSAGES["t2_p3"]["text"], "timeRecommended": 20, "questions": t2_p3_qs})

    tests.append({"id": "cam16_test2", "testNumber": 2, "passages": t2_passages})

    # ========== TEST 3 ==========
    t3_passages = []

    # Passage 1: Roman Shipbuilding and Navigation (Q1-13)
    t3_p1_qs = []
    # Q1-5: tfng
    t3_p1_qs.extend([
        {"id": "cam16_t3_r_q1", "type": "tfng", "question": "The Romans were the first civilisation to build large cargo ships.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE"},
        {"id": "cam16_t3_r_q2", "type": "tfng", "question": "Roman warships were faster than Greek triremes.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
        {"id": "cam16_t3_r_q3", "type": "tfng", "question": "Roman ships used only square sails.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE"},
        {"id": "cam16_t3_r_q4", "type": "tfng", "question": "Mortise-and-tenon joinery made Roman ship hulls stronger.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "TRUE"},
        {"id": "cam16_t3_r_q5", "type": "tfng", "question": "Lead sheathing was used to protect ships from marine organisms.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "TRUE"},
    ])
    # Q6-13: notes_completion (one word only)
    for i, (qtext, ans) in enumerate([
        ("6. Ship hulls were made _____ to improve speed", "lightweight"),
        ("7. Ram prows were made of _____", "bronze"),
        ("8. Water _____ in the hold affected stability", "levels"),
        ("9. The _____ was the main structural component of the ship", "hull"),
        ("10. A _____ sail was an innovation in Roman ship design", "triangular"),
        ("11. Oars were often timed by the rhythm of _____", "music"),
        ("12. Ships transported large quantities of _____ from Egypt to Rome", "grain"),
        ("13. Heavy cargo was moved using _____", "towboats"),
    ], 6):
        t3_p1_qs.append({"id": f"cam16_t3_r_q{i}", "type": "notes_completion", "question": qtext, "options": [], "correctAnswer": ans})
    t3_passages.append({"id": "cam16_t3_p1", "title": "Roman Shipbuilding and Navigation", "text": PASSAGES["t3_p1"]["text"], "timeRecommended": 20, "questions": t3_p1_qs})

    # Passage 2: Climate Change Reveals Ancient Artefacts in Norway's Glaciers (Q14-26)
    t3_p2_qs = []
    # Q14-19: matching_info
    for i, (qtext, ans) in enumerate([
        ("the need for a targeted approach to artefact recovery", "D"),
        ("examples of the types of items that have been discovered", "C"),
        ("the rate at which glacial melt is occurring", "F"),
        ("the difficulty of preserving organic materials once exposed", "H"),
        ("the range of scientific disciplines involved in the research", "G"),
        ("a reason why ancient peoples travelled through these mountain regions", "B"),
    ], 14):
        t3_p2_qs.append({"id": f"cam16_t3_r_q{i}", "type": "matching_info", "question": qtext, "options": ["A", "B", "C", "D", "E", "F", "G", "H"], "correctAnswer": ans})
    # Q20-22: summary_completion (one word only)
    for i, (qtext, ans) in enumerate([
        ("20. The objects found include ancient _____ that were frozen for millennia", "microorganisms"),
        ("21. Hunters tracked _____ across the ice for thousands of years", "reindeer"),
        ("22. Some artefacts show that _____ were collected as food", "insects"),
    ], 20):
        t3_p2_qs.append({"id": f"cam16_t3_r_q{i}", "type": "summary_completion", "question": qtext, "options": [], "correctAnswer": ans})
    # Q23-24: multiple_choice_multi
    t3_p2_qs.append({"id": "cam16_t3_r_q23", "type": "multiple_choice_multi", "question": "Which TWO types of artefacts have been found in Norway's melting glaciers?\nA. pottery vessels\nB. wooden arrows\nC. iron tools\nD. woollen clothing\nE. stone carvings", "options": ["A", "B", "C", "D", "E"], "correctAnswer": "B, C"})
    # Q25-26: multiple_choice_multi
    t3_p2_qs.append({"id": "cam16_t3_r_q25", "type": "multiple_choice_multi", "question": "Which TWO factors make glacial archaeology challenging?\nA. the short window of opportunity to recover artefacts\nB. the high cost of mounting expeditions\nC. the threat of artefacts decomposing after exposure\nD. the difficulty of obtaining permits\nE. the harsh weather conditions", "options": ["A", "B", "C", "D", "E"], "correctAnswer": "A, C"})
    t3_passages.append({"id": "cam16_t3_p2", "title": "Climate Change Reveals Ancient Artefacts in Norway's Glaciers", "text": PASSAGES["t3_p2"]["text"], "timeRecommended": 20, "questions": t3_p2_qs})

    # Passage 3: Plant 'Thermometer' Triggers Springtime Growth (Q27-40)
    t3_p3_qs = []
    # Q27-32: tfng
    t3_p3_qs.extend([
        {"id": "cam16_t3_r_q27", "type": "tfng", "question": "Plants rely solely on daylight hours to determine when to grow in spring.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
        {"id": "cam16_t3_r_q28", "type": "tfng", "question": "The phytochrome molecule is sensitive to temperature changes.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "TRUE"},
        {"id": "cam16_t3_r_q29", "type": "tfng", "question": "Warmer temperatures can trigger a cascade of genetic activity in plants.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "TRUE"},
        {"id": "cam16_t3_r_q30", "type": "tfng", "question": "The plant thermometer mechanism was first discovered in mustard plants.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
        {"id": "cam16_t3_r_q31", "type": "tfng", "question": "Climate change is likely to delay the start of the growing season for most plants.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE"},
        {"id": "cam16_t3_r_q32", "type": "tfng", "question": "Understanding plant temperature sensing could help develop more resilient crops.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE"},
    ])
    # Q33-37: matching_info (statements to letters A-H)
    for i, (qtext, ans) in enumerate([
        ("the specific protein that acts as a temperature sensor", "H"),
        ("how warmer winters affect plant pollination cycles", "D"),
        ("the risk of frost damage to early-flowering plants", "G"),
        ("the role of a particular signalling pathway in growth regulation", "C"),
        ("the impact of temperature on the shape of a key molecule", "A"),
    ], 33):
        t3_p3_qs.append({"id": f"cam16_t3_r_q{i}", "type": "matching_info", "question": qtext, "options": ["A", "B", "C", "D", "E", "F", "G", "H"], "correctAnswer": ans})
    # Q38-40: summary_completion (one word only)
    for i, (qtext, ans) in enumerate([
        ("38. The mechanism can be described as a plant 'thermometer' that detects _____ conditions", "warm"),
        ("39. Earlier spring growth may disrupt the timing of _____ activities such as pollination", "summer"),
        ("40. The study used _____ as a model organism for the experiments", "mustard plant"),
    ], 38):
        t3_p3_qs.append({"id": f"cam16_t3_r_q{i}", "type": "summary_completion", "question": qtext, "options": [], "correctAnswer": ans})
    t3_passages.append({"id": "cam16_t3_p3", "title": "Plant 'Thermometer' Triggers Springtime Growth", "text": PASSAGES["t3_p3"]["text"], "timeRecommended": 20, "questions": t3_p3_qs})

    tests.append({"id": "cam16_test3", "testNumber": 3, "passages": t3_passages})

    # ========== TEST 4 ==========
    t4_passages = []

    # Passage 1: Roman Tunnels (Q1-13)
    t4_p1_qs = []
    # Q1-6: diagram (notes_completion)
    for i, (qtext, ans) in enumerate([
        ("1. Vertical _____ were dug at intervals along the tunnel route", "posts"),
        ("2. Water was channelled into a _____", "canal"),
        ("3. Shafts were used for _____", "ventilation"),
        ("4. A _____ covered the entrance to the tunnel", "lid"),
        ("5. The _____ of the rock was used to break it apart", "weight"),
        ("6. Workers used _____ techniques to move through the rock", "climbing"),
    ], 1):
        t4_p1_qs.append({"id": f"cam16_t4_r_q{i}", "type": "notes_completion", "question": qtext, "options": [], "correctAnswer": ans})
    # Q7-10: tfng
    t4_p1_qs.extend([
        {"id": "cam16_t4_r_q7", "type": "tfng", "question": "The Romans used tunnels primarily for military purposes.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE"},
        {"id": "cam16_t4_r_q8", "type": "tfng", "question": "Roman tunnelling techniques were adopted from the Greeks.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
        {"id": "cam16_t4_r_q9", "type": "tfng", "question": "The fire-setting technique involved heating the rock face with torches.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE"},
        {"id": "cam16_t4_r_q10", "type": "tfng", "question": "Roman tunnel builders used surveying techniques to ensure tunnels met accurately.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "TRUE"},
    ])
    # Q11-13: short_answer
    for i, (qtext, ans) in enumerate([
        ("11. Which valuable metal was extracted using Roman mining tunnels?", "gold"),
        ("12. Whose name is often recorded in connection with major Roman tunnel projects?", "(the) architect('s) (name)"),
        ("13. What type of structure did Roman tunnels often lead to at coastal cities?", "(the) harbour / harbor"),
    ], 11):
        t4_p1_qs.append({"id": f"cam16_t4_r_q{i}", "type": "short_answer", "question": qtext, "options": [], "correctAnswer": ans})
    t4_passages.append({"id": "cam16_t4_p1", "title": "Roman Tunnels", "text": PASSAGES["t4_p1"]["text"], "timeRecommended": 20, "questions": t4_p1_qs})

    # Passage 2: Changes in Reading Habits (Q14-26)
    t4_p2_qs = []
    # Q14-17: multiple_choice
    for i, ans in enumerate(["A", "B", "D", "B"], 14):
        t4_p2_qs.append({"id": f"cam16_t4_r_q{i}", "type": "multiple_choice", "question": f"Question {i}: Choose the correct letter.", "options": ["A", "B", "C", "D"], "correctAnswer": ans})
    # Q18-22: summary_completion (from list of words)
    for i, (qtext, ans) in enumerate([
        ("18. Many educators find the decline in deep reading _____", "worrying"),
        ("19. Reading on screens tends to be less _____ than reading on paper", "thorough"),
        ("20. Readers find it _____ to concentrate on long digital texts", "hard"),
        ("21. Digital reading can be a more _____ experience than reading print", "isolated"),
        ("22. The shift to digital may lead to a less _____ connection with the text", "emotional"),
    ], 18):
        t4_p2_qs.append({"id": f"cam16_t4_r_q{i}", "type": "summary_completion", "question": qtext, "options": [], "correctAnswer": ans})
    # Q23-26: ynng
    t4_p2_qs.extend([
        {"id": "cam16_t4_r_q23", "type": "ynng", "question": "Reading on screens has been proven to reduce comprehension compared to reading on paper.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "YES"},
        {"id": "cam16_t4_r_q24", "type": "ynng", "question": "The physical properties of printed books aid in mental mapping of the text.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "NO"},
        {"id": "cam16_t4_r_q25", "type": "ynng", "question": "Younger readers prefer digital texts over printed ones.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
        {"id": "cam16_t4_r_q26", "type": "ynng", "question": "The author believes that reading habits are changing in ways that may affect cognitive development.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "YES"},
    ])
    t4_passages.append({"id": "cam16_t4_p2", "title": "Changes in Reading Habits", "text": PASSAGES["t4_p2"]["text"], "timeRecommended": 20, "questions": t4_p2_qs})

    # Passage 3: Attitudes towards Artificial Intelligence (Q27-40)
    t4_p3_qs = []
    # Q27-32: matching_headings
    t4_p3_headings = [
        "i. An increasing divergence of attitudes towards AI",
        "ii. Reasons why we have more faith in human judgement",
        "iii. The superiority of AI projections",
        "iv. The importance of maintaining human control over AI",
        "v. The advantages of involving users in AI processes",
        "vi. Widespread distrust of an AI innovation",
        "vii. Encouraging openness about how AI functions",
        "viii. A call for a cautious approach to AI development",
    ]
    for i, (qtext, ans) in enumerate([
        ("The superiority of AI projections", "iii"),
        ("Widespread distrust of an AI innovation", "vi"),
        ("Reasons why we have more faith in human judgement", "ii"),
        ("An increasing divergence of attitudes towards AI", "i"),
        ("Encouraging openness about how AI functions", "vii"),
        ("The advantages of involving users in AI processes", "v"),
    ], 27):
        t4_p3_qs.append({"id": f"cam16_t4_r_q{i}", "type": "matching_headings", "question": qtext, "options": t4_p3_headings, "correctAnswer": ans})
    # Q33-35: multiple_choice
    for i, ans in enumerate(["C", "B", "A"], 33):
        t4_p3_qs.append({"id": f"cam16_t4_r_q{i}", "type": "multiple_choice", "question": f"Question {i}: Choose the correct letter.", "options": ["A", "B", "C", "D"], "correctAnswer": ans})
    # Q36-40: ynng
    t4_p3_qs.extend([
        {"id": "cam16_t4_r_q36", "type": "ynng", "question": "People are more trusting of AI in areas that require subjective human judgment.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "NO"},
        {"id": "cam16_t4_r_q37", "type": "ynng", "question": "The majority of people are aware of how often they use AI-powered services.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
        {"id": "cam16_t4_r_q38", "type": "ynng", "question": "Transparency in AI decision-making can help build public trust.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "YES"},
        {"id": "cam16_t4_r_q39", "type": "ynng", "question": "Expert optimism about AI is matched by equivalent public enthusiasm.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "NO"},
        {"id": "cam16_t4_r_q40", "type": "ynng", "question": "User involvement in AI development is beneficial.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "YES"},
    ])
    t4_passages.append({"id": "cam16_t4_p3", "title": "Attitudes towards Artificial Intelligence", "text": PASSAGES["t4_p3"]["text"], "timeRecommended": 20, "questions": t4_p3_qs})

    tests.append({"id": "cam16_test4", "testNumber": 4, "passages": t4_passages})

    return {"id": "cam16", "title": "Cambridge IELTS 16 Academic Reading", "tests": tests}


###############################################################################
# LISTENING DATA
###############################################################################

def make_listening():
    tests = []

    # ========== LISTENING TEST 1 ==========
    lt1_parts = []
    # Part 1: Children's Engineering Workshops (Q1-10)
    lt1_p1_qs = []
    for i, (qtext, ans) in enumerate([
        ("1. Make a jumping frog, a _____-timer or a powered rocket", "egg"),
        ("2. Build a _____ crane or a bridge", "tower"),
        ("3. Design and build your own _____", "car"),
        ("4. Make and decorate a model of your favourite _____", "animals"),
        ("5. Build a _____ that can bear weight", "bridge"),
        ("6. Create a short _____ using stop-motion animation", "movie"),
        ("7. Learn to _____ cakes like a professional", "decorate"),
        ("8. Workshops take place on _____", "Wednesdays"),
        ("9. The course tutor is called _____", "Fradstone"),
        ("10. Parking is available at the _____ lot", "parking"),
    ], 1):
        lt1_p1_qs.append({"id": f"cam16_lt1_q{i}", "type": "notes_completion", "question": qtext, "options": [], "correctAnswer": ans})
    lt1_parts.append({"id": "cam16_lt1_p1", "title": "Children's Engineering Workshops", "audioFile": "cam16_test1_part1.mp3", "subtitle": "", "duration": "", "questions": lt1_p1_qs})

    # Part 2: Stevenson's (Company Tour) (Q11-20)
    lt1_p2_qs = []
    for i, ans in enumerate(["C", "A", "B", "C"], 11):
        lt1_p2_qs.append({"id": f"cam16_lt1_q{i}", "type": "multiple_choice", "question": f"Question {i}: Choose the correct letter.", "options": ["A", "B", "C"], "correctAnswer": ans})
    for i, ans in enumerate(["H", "C", "G", "B", "I", "A"], 15):
        lt1_p2_qs.append({"id": f"cam16_lt1_q{i}", "type": "matching", "question": f"Match the location {i-14} to the letter on the map.", "options": ["A", "B", "C", "D", "E", "F", "G", "H", "I"], "correctAnswer": ans})
    lt1_parts.append({"id": "cam16_lt1_p2", "title": "Stevenson's (Company Tour)", "audioFile": "cam16_test1_part2.mp3", "subtitle": "", "duration": "", "questions": lt1_p2_qs})

    # Part 3: Art Projects (Jess and Tom) (Q21-30)
    lt1_p3_qs = []
    lt1_p3_qs.append({"id": "cam16_lt1_q21", "type": "multiple_choice_multi", "question": "Which TWO things do Jess and Tom agree to include in their art project?\nA. photographs\nB. interviews\nC. a visit to a museum\nD. a survey\nE. handouts", "options": ["A", "B", "C", "D", "E"], "correctAnswer": "C, E"})
    lt1_p3_qs.append({"id": "cam16_lt1_q23", "type": "multiple_choice_multi", "question": "Which TWO changes do Jess and Tom make to their project plan?\nA. they decide to include more artists\nB. they will be less specific about the outcome\nC. they will focus on contemporary works\nD. they will add more evaluative notes\nE. they will change the presentation format", "options": ["A", "B", "C", "D", "E"], "correctAnswer": "B, E"})
    for i, ans in enumerate(["D", "C", "A", "H", "F", "G"], 25):
        lt1_p3_qs.append({"id": f"cam16_lt1_q{i}", "type": "matching", "question": f"Match the artwork {i-24} to the description.", "options": ["A. childhood memory", "B. urban development", "C. fast movement", "D. potential threat", "E. social change", "F. continuity of life", "G. protection of nature", "H. confused attitude to nature"], "correctAnswer": ans})
    lt1_parts.append({"id": "cam16_lt1_p3", "title": "Art Projects (Jess and Tom)", "audioFile": "cam16_test1_part3.mp3", "subtitle": "", "duration": "", "questions": lt1_p3_qs})

    # Part 4: Stoicism (Q31-40)
    lt1_p4_qs = []
    for i, ans in enumerate(["practical", "publication", "choices", "negative", "play", "capitalism", "depression", "logic", "opportunity", "practice"], 31):
        lt1_p4_qs.append({"id": f"cam16_lt1_q{i}", "type": "notes_completion", "question": f"Question {i}: ONE WORD ONLY.", "options": [], "correctAnswer": ans})
    lt1_parts.append({"id": "cam16_lt1_p4", "title": "Stoicism", "audioFile": "cam16_test1_part4.mp3", "subtitle": "", "duration": "", "questions": lt1_p4_qs})

    tests.append({"id": "cam16_listening_test1", "testNumber": 1, "parts": lt1_parts})

    # ========== LISTENING TEST 2 ==========
    lt2_parts = []
    # Part 1: Copying Photos to Digital Format (Q1-10)
    lt2_p1_qs = []
    for i, (qtext, ans) in enumerate([
        ("1. Number of photos: 200, cost per photo depends on the _____", "frame"),
        ("2. Total cost: £_____", "195"),
        ("3. Gives a discount for _____ by card", "payment"),
        ("4. These are photos of _____", "Grandparents"),
        ("5. Photo type: black and white and _____", "colour"),
        ("6. State of photos: some damage to the _____ of the photo", "hand"),
        ("7. Issue: the _____ of photos is too light", "background"),
        ("8. Camera setting: adjust the _____", "focus"),
        ("9. Delivery time: _____", "ten days"),
        ("10. Photos will be stored in a _____ box", "plastic"),
    ], 1):
        lt2_p1_qs.append({"id": f"cam16_lt2_q{i}", "type": "notes_completion", "question": qtext, "options": [], "correctAnswer": ans})
    lt2_parts.append({"id": "cam16_lt2_p1", "title": "Copying Photos to Digital Format", "audioFile": "cam16_test2_part1.mp3", "subtitle": "", "duration": "", "questions": lt2_p1_qs})

    # Part 2: Dartfield House School (Q11-20)
    lt2_p2_qs = []
    for i, ans in enumerate(["C", "B", "A", "A", "C"], 11):
        lt2_p2_qs.append({"id": f"cam16_lt2_q{i}", "type": "multiple_choice", "question": f"Question {i}: Choose the correct letter.", "options": ["A", "B", "C"], "correctAnswer": ans})
    for i, ans in enumerate(["D", "A", "B"], 16):
        lt2_p2_qs.append({"id": f"cam16_lt2_q{i}", "type": "matching", "question": f"Match the club activity {i-15} to the description.", "options": ["A. Street Life - pupils help to plan menus", "B. Speedy Italian - only vegetarian food", "C. Taste of Asia - includes cookery demonstrations", "D. World Adventures - daily change in menu", "E. Healthy Kitchen - uses local ingredients"], "correctAnswer": ans})
    lt2_p2_qs.append({"id": "cam16_lt2_q19", "type": "multiple_choice_multi", "question": "Which TWO after-school activities are mentioned?\nA. drama\nB. acting\nC. piano\nD. football\nE. dance", "options": ["A", "B", "C", "D", "E"], "correctAnswer": "B, C"})
    lt2_parts.append({"id": "cam16_lt2_p2", "title": "Dartfield House School", "audioFile": "cam16_test2_part2.mp3", "subtitle": "", "duration": "", "questions": lt2_p2_qs})

    # Part 3: Assignment on Sleep and Dreams (Q21-30)
    lt2_p3_qs = []
    for i, ans in enumerate(["B", "A", "C", "C"], 21):
        lt2_p3_qs.append({"id": f"cam16_lt2_q{i}", "type": "multiple_choice", "question": f"Question {i}: Choose the correct letter.", "options": ["A", "B", "C"], "correctAnswer": ans})
    for i, (qtext, ans) in enumerate([
        ("25. They need information about the _____ of sleep research", "history"),
        ("26. The professor recommends a particular _____ for background reading", "paper"),
        ("27. The study looked at how _____ respond to sleep deprivation", "humans"),
        ("28. A key factor affecting sleep quality is the level of _____", "stress"),
        ("29. The results can be presented using a _____", "graph"),
        ("30. They still need to _____ the data collected", "evaluate"),
    ], 25):
        lt2_p3_qs.append({"id": f"cam16_lt2_q{i}", "type": "notes_completion", "question": qtext, "options": [], "correctAnswer": ans})
    lt2_parts.append({"id": "cam16_lt2_p3", "title": "Assignment on Sleep and Dreams", "audioFile": "cam16_test2_part3.mp3", "subtitle": "", "duration": "", "questions": lt2_p3_qs})

    # Part 4: Health Benefits of Dance (Q31-40)
    lt2_p4_qs = []
    for i, ans in enumerate(["creativity", "therapy", "fitness", "balance", "brain", "motivation", "isolation", "calories", "obesity", "habit"], 31):
        lt2_p4_qs.append({"id": f"cam16_lt2_q{i}", "type": "notes_completion", "question": f"Question {i}: ONE WORD ONLY.", "options": [], "correctAnswer": ans})
    lt2_parts.append({"id": "cam16_lt2_p4", "title": "Health Benefits of Dance", "audioFile": "cam16_test2_part4.mp3", "subtitle": "", "duration": "", "questions": lt2_p4_qs})

    tests.append({"id": "cam16_listening_test2", "testNumber": 2, "parts": lt2_parts})

    # ========== LISTENING TEST 3 ==========
    lt3_parts = []
    # Part 1: Junior Cycle Camp (Q1-10)
    lt3_p1_qs = []
    for i, (qtext, ans) in enumerate([
        ("1. Camp location: Adventure _____", "park"),
        ("2. Camp colour group: _____ group", "blue"),
        ("3. Need to provide a _____ number", "reference"),
        ("4. Evening activity: listen to a _____", "story"),
        ("5. Bad weather alternative: activity _____", "rain"),
        ("6. Food provided: _____ in the afternoon", "snack"),
        ("7. Must bring own _____ (if needed)", "medication"),
        ("8. Required item: a _____ for cycling", "helmet"),
        ("9. Accommodation: sleep in a _____", "tent"),
        ("10. Total cost: $_____", "199"),
    ], 1):
        lt3_p1_qs.append({"id": f"cam16_lt3_q{i}", "type": "notes_completion", "question": qtext, "options": [], "correctAnswer": ans})
    lt3_parts.append({"id": "cam16_lt3_p1", "title": "Junior Cycle Camp", "audioFile": "cam16_test3_part1.mp3", "subtitle": "", "duration": "", "questions": lt3_p1_qs})

    # Part 2: Agriculture & Horticulture Jobs (Q11-20)
    lt3_p2_qs = []
    lt3_p2_qs.append({"id": "cam16_lt3_q11", "type": "multiple_choice_multi", "question": "Which TWO benefits of working in agriculture are mentioned?\nA. active lifestyle\nB. high salary\nC. flexible working\nD. travel opportunities\nE. job security", "options": ["A", "B", "C", "D", "E"], "correctAnswer": "A, C"})
    lt3_p2_qs.append({"id": "cam16_lt3_q13", "type": "multiple_choice_multi", "question": "Which TWO challenges of working in horticulture are mentioned?\nA. low pay\nB. quiet location\nC. difficult weather\nD. long hours\nE. physical demands", "options": ["A", "B", "C", "D", "E"], "correctAnswer": "B, C"})
    for i, ans in enumerate(["D", "F", "A", "H", "C", "G"], 15):
        lt3_p2_qs.append({"id": f"cam16_lt3_q{i}", "type": "matching", "question": f"Match the job {i-14} to the description.", "options": ["A. not a permanent job", "B. involves international travel", "C. experience not essential", "D. intensive but fun", "E. management training provided", "F. chance for rapid promotion", "G. accommodation available", "H. local travel"], "correctAnswer": ans})
    lt3_parts.append({"id": "cam16_lt3_p2", "title": "Agriculture & Horticulture Jobs", "audioFile": "cam16_test3_part2.mp3", "subtitle": "", "duration": "", "questions": lt3_p2_qs})

    # Part 3: Diet & Obesity Presentation (Q21-30)
    lt3_p3_qs = []
    lt3_p3_qs.append({"id": "cam16_lt3_q21", "type": "multiple_choice_multi", "question": "Which TWO strengths of the study do the students identify?\nA. the study was conducted over a long period\nB. the participants were from diverse backgrounds\nC. the sample size was large\nD. the participants were unaware of what they were drinking\nE. the results were consistent across all age groups", "options": ["A", "B", "C", "D", "E"], "correctAnswer": "C, D"})
    lt3_p3_qs.append({"id": "cam16_lt3_q23", "type": "multiple_choice_multi", "question": "Which TWO weaknesses of the study do the students identify?\nA. the age range of participants was too narrow\nB. the nuts were served whole rather than ground\nC. the nuts were not finely ground enough\nD. the participants' diets were not monitored\nE. the scales used for measurement were unsuitable", "options": ["A", "B", "C", "D", "E"], "correctAnswer": "C, E"})
    for i, ans in enumerate(["C", "A", "B", "A", "A", "C"], 25):
        lt3_p3_qs.append({"id": f"cam16_lt3_q{i}", "type": "multiple_choice", "question": f"Question {i}: Choose the correct letter.", "options": ["A", "B", "C"], "correctAnswer": ans})
    lt3_parts.append({"id": "cam16_lt3_p3", "title": "Diet & Obesity Presentation", "audioFile": "cam16_test3_part3.mp3", "subtitle": "", "duration": "", "questions": lt3_p3_qs})

    # Part 4: Hand Knitting (Q31-40)
    lt3_p4_qs = []
    for i, ans in enumerate(["grandmother", "decade", "equipment", "economic", "basic", "round", "bone", "rough", "style", "sheep"], 31):
        lt3_p4_qs.append({"id": f"cam16_lt3_q{i}", "type": "notes_completion", "question": f"Question {i}: ONE WORD ONLY.", "options": [], "correctAnswer": ans})
    lt3_parts.append({"id": "cam16_lt3_p4", "title": "Hand Knitting", "audioFile": "cam16_test3_part4.mp3", "subtitle": "", "duration": "", "questions": lt3_p4_qs})

    tests.append({"id": "cam16_listening_test3", "testNumber": 3, "parts": lt3_parts})

    # ========== LISTENING TEST 4 ==========
    lt4_parts = []
    # Part 1: Holiday Rental (Q1-10)
    lt4_p1_qs = []
    for i, (qtext, ans) in enumerate([
        ("1. Date available: _____ March", "28th"),
        ("2. Cost per week: £_____", "550"),
        ("3. Name of cottage: _____ Cottage", "Chervil"),
        ("4. Parking: available in the _____", "garage"),
        ("5. Garden: has a _____ with seating", "garden"),
        ("6. Parking for guests: on-street _____", "parking"),
        ("7. Heating: _____-burning stove", "wood"),
        ("8. Nearest shop: across the _____", "bridge"),
        ("9. Local attraction: the old _____", "monument"),
        ("10. Booking deposit required by _____", "March"),
    ], 1):
        lt4_p1_qs.append({"id": f"cam16_lt4_q{i}", "type": "notes_completion", "question": qtext, "options": [], "correctAnswer": ans})
    lt4_parts.append({"id": "cam16_lt4_p1", "title": "Holiday Rental", "audioFile": "cam16_test4_part1.mp3", "subtitle": "", "duration": "", "questions": lt4_p1_qs})

    # Part 2: Local Council Report on Traffic and Highways (Q11-20)
    lt4_p2_qs = []
    for i, ans in enumerate(["C", "A", "B", "B"], 11):
        lt4_p2_qs.append({"id": f"cam16_lt4_q{i}", "type": "multiple_choice", "question": f"Question {i}: Choose the correct letter.", "options": ["A", "B", "C"], "correctAnswer": ans})
    for i, ans in enumerate(["C", "F", "A", "I", "E", "H"], 15):
        lt4_p2_qs.append({"id": f"cam16_lt4_q{i}", "type": "matching", "question": f"Match the facility {i-14} to the letter on the map.", "options": ["A. Children's playground", "B. Car park extension", "C. New car park", "D. Cycle path", "E. Pavilion", "F. New cricket pitch", "G. Footpath", "H. Notice board", "I. Skateboard ramp"], "correctAnswer": ans})
    lt4_parts.append({"id": "cam16_lt4_p2", "title": "Local Council Report on Traffic and Highways", "audioFile": "cam16_test4_part2.mp3", "subtitle": "", "duration": "", "questions": lt4_p2_qs})

    # Part 3: Bike-Sharing Schemes (Q21-30)
    lt4_p3_qs = []
    lt4_p3_qs.append({"id": "cam16_lt4_q21", "type": "multiple_choice_multi", "question": "Which TWO benefits of bike-sharing schemes are mentioned as being most important?\nA. improving public health\nB. reducing traffic congestion\nC. improving air quality\nD. saving commuters money\nE. reducing noise pollution", "options": ["A", "B", "C", "D", "E"], "correctAnswer": "B, C"})
    lt4_p3_qs.append({"id": "cam16_lt4_q23", "type": "multiple_choice_multi", "question": "Which TWO factors are said to contribute to the success of bike-sharing schemes?\nA. low membership fees\nB. the app is easy to use\nC. public awareness was raised\nD. government subsidies\nE. good weather conditions", "options": ["A", "B", "C", "D", "E"], "correctAnswer": "B, C"})
    for i, ans in enumerate(["C", "F", "D", "E", "B", "A"], 25):
        lt4_p3_qs.append({"id": f"cam16_lt4_q{i}", "type": "matching", "question": f"Match the city {i-24} to the opinion about its bike-sharing scheme.", "options": ["A. has been disappointing", "B. should be cheaper", "C. surprised it has been so successful", "D. more investment required", "E. system well designed", "F. disagree about reasons for success", "G. started too late"], "correctAnswer": ans})
    lt4_parts.append({"id": "cam16_lt4_p3", "title": "Bike-Sharing Schemes", "audioFile": "cam16_test4_part3.mp3", "subtitle": "", "duration": "", "questions": lt4_p3_qs})

    # Part 4: Extinction of the Dodo Bird (Q31-40)
    lt4_p4_qs = []
    for i, ans in enumerate(["spices", "colony", "fat", "head", "movement", "balance", "brain", "smell", "rats", "forest"], 31):
        lt4_p4_qs.append({"id": f"cam16_lt4_q{i}", "type": "notes_completion", "question": f"Question {i}: ONE WORD ONLY.", "options": [], "correctAnswer": ans})
    lt4_parts.append({"id": "cam16_lt4_p4", "title": "Extinction of the Dodo Bird", "audioFile": "cam16_test4_part4.mp3", "subtitle": "", "duration": "", "questions": lt4_p4_qs})

    tests.append({"id": "cam16_listening_test4", "testNumber": 4, "parts": lt4_parts})

    return {"id": "cam16", "title": "Cambridge IELTS 16 Academic Listening", "tests": tests}


###############################################################################
# MAIN
###############################################################################

def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    reading = make_reading()
    rpath = os.path.join(OUT_DIR, "reading.json")
    with open(rpath, "w", encoding="utf-8") as f:
        json.dump(reading, f, ensure_ascii=False, indent=2)
    print(f"Wrote {rpath} ({len(reading['tests'])} tests)")

    listening = make_listening()
    lpath = os.path.join(OUT_DIR, "listening.json")
    with open(lpath, "w", encoding="utf-8") as f:
        json.dump(listening, f, ensure_ascii=False, indent=2)
    print(f"Wrote {lpath} ({len(listening['tests'])} tests)")


if __name__ == "__main__":
    main()
