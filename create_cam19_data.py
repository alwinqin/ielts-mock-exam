#!/usr/bin/env python3
"""Generate cam19 reading.json and listening.json with complete data."""

import json
import os

OUT_DIR = "data/cambridge/cam19"

###############################################################################
# PASSAGE TEXTS (descriptive summaries, not authentic Cambridge text)
###############################################################################

PASSAGES = {
    # ========== TEST 1 ==========
    "t1_p1": {
        "title": "How Tennis Rackets Have Changed",
        "text": "This passage traces the technological evolution of tennis rackets from the late 19th century to the present day. Early rackets were made from laminated ash and beech wood, with small heads and heavy frames that limited power and required precise technique. The standard wood racket, weighing around 400 grams, dominated the sport for nearly a century and produced a distinctive feel and sound that many traditionalists valued. Players relied on skill and timing rather than equipment to generate pace.\n\nThe arrival of metal rackets in the 1960s and 1970s, particularly the Wilson T2000, marked the first major departure from wooden construction, although early metal frames were stiff and transmitted vibration uncomfortably. However, the real breakthrough came with the introduction of graphite and carbon fibre composites in the 1980s. These materials allowed engineers to design rackets that were simultaneously lighter, more powerful, and more forgiving. Larger head sizes increased the sweet spot dramatically, while changes in frame stiffness transformed how the ball could be struck.\n\nThe passage goes on to examine how racket technology influenced playing styles at both amateur and professional levels. The ability to generate heavy topspin became a defining feature of the modern game, with string technology — particularly polyester strings — enabling players to swing harder while maintaining control. The discussion also covers the role of grip innovations, weight distribution adjustments, and the ongoing debate about whether technology has changed the essential character of tennis as a sport. Concerns about increased injury rates and the diminishing role of pure skill compared to equipment advantages are also explored.",
    },
    "t1_p2": {
        "title": "The Pirates of the Ancient Mediterranean",
        "text": "This historical passage examines the rise and impact of piracy in the Mediterranean during the late Roman Republic, roughly between the 2nd and 1st centuries BCE. Piracy flourished particularly along the rugged coast of Cilicia in southern Anatolia, where natural harbours and inaccessible strongholds gave pirates secure bases from which to operate. These were not merely small-time raiders but organised naval forces that grew bold enough to attack coastal cities, intercept grain shipments bound for Rome, and kidnap prominent Romans for ransom.\n\nThe passage details the sophisticated networks that pirates developed, including intelligence-gathering operations, slave-trading connections, and systems for ransoming captives that involved intermediaries across multiple ports. It describes the scale of the threat: at its peak, piracy so disrupted Mediterranean commerce that grain prices in Rome soared and travel became hazardous. The pirates' fast, lightweight vessels allowed them to outmanoeuvre the heavier Roman warships, and their knowledge of local waters made them difficult to pursue.\n\nThe account then turns to Rome's eventual response. After years of ineffective military campaigns, the Lex Gabinia was passed in 67 BCE, granting Pompey the Great extraordinary powers and resources to eliminate piracy. Pompey's strategy was systematic and comprehensive — he divided the Mediterranean into sectors, assigned fleets to each, and swept from west to east, clearing pirate strongholds and offering generous terms for surrender. Within three months, the pirate threat had been effectively neutralised. The passage concludes by reflecting on Pompey's settlement policies, which resettled many surrendered pirates as farmers in inland communities, and considers the long-term implications for Roman naval dominance and Mediterranean trade.",
    },
    "t1_p3": {
        "title": "The Persistence and Peril of Misinformation",
        "text": "This passage explores the psychological and social mechanisms that make misinformation remarkably persistent, even in the face of clear corrective evidence. It introduces the concept of the 'continued influence effect,' a well-documented phenomenon in which misinformation continues to shape people's beliefs and reasoning after it has been explicitly retracted. The effect is particularly strong when the false information is emotionally resonant, fits within existing narrative frameworks, or has been repeated frequently. The passage also discusses how cognitive biases such as confirmation bias and the fluency heuristic contribute to the durability of false beliefs.\n\nThe passage then examines the role of modern communication environments in accelerating the spread of misinformation. Social media algorithms that prioritise engagement over accuracy, the speed at which false claims can circulate before fact-checkers respond, and the fragmented nature of online information ecosystems all create conditions in which misinformation thrives. The concept of 'echo chambers' and 'filter bubbles' is discussed in the context of how people become exposed to increasingly narrow ranges of information that reinforce their existing views.\n\nFinally, the passage evaluates strategies for combating misinformation. Traditional debunking — simply stating that a claim is false — is shown to be relatively ineffective and can even backfire through the familiarity effect. More promising approaches include pre-emptive 'inoculation' or 'prebunking' techniques, which expose people to weakened versions of misleading arguments to build cognitive resistance. The passage also discusses the importance of narrative replacement, where corrections must provide an alternative causal explanation rather than simply negating the false claim. The author concludes that effective responses require understanding the underlying psychological appeal of misinformation, not just its factual inaccuracy.",
    },
    # ========== TEST 2 ==========
    "t2_p1": {
        "title": "The Industrial Revolution in Britain",
        "text": "This passage examines the key factors that enabled Britain to become the birthplace of the Industrial Revolution in the late 18th and early 19th centuries. It discusses Britain's abundant natural resources, particularly coal and iron ore deposits located close together, which provided the essential raw materials for industrialisation. The development of the steam engine, improved by James Watt and others, created a reliable power source that freed factories from dependence on water power and allowed them to be located in urban centres. The passage also highlights the role of technological innovations in textiles, such as the spinning jenny, the water frame, and the power loom, which dramatically increased production capacity.\n\nThe passage goes on to analyse Britain's economic and social conditions that supported industrial growth. A stable legal system that protected property rights, well-developed financial institutions including banks and stock markets, and a growing colonial trade network all provided favourable conditions for investment and enterprise. The enclosure movement, which consolidated small landholdings into larger farms, displaced rural workers and created a mobile labour force available for factory work. The passage also considers the role of the British state in supporting infrastructure development, particularly through the construction of canals and later railways.\n\nFinally, the passage addresses the social consequences of industrialisation. Rapid urbanisation led to overcrowded cities with inadequate housing and poor sanitation. Working conditions in factories were often harsh, with long hours and dangerous machinery. The passage discusses the emergence of labour movements and reform efforts, including the Factory Acts that gradually regulated working conditions and child labour. It concludes by reflecting on how the Industrial Revolution transformed not just the British economy but the very structure of society, creating new social classes and reshaping the relationship between people, work, and place.",
    },
    "t2_p2": {
        "title": "Athletes and Stress",
        "text": "This passage investigates the psychological pressures faced by athletes at elite levels of competition and the various ways stress affects performance and well-being. It distinguishes between 'good stress' (eustress), which can enhance focus and motivation, and 'bad stress' (distress), which impairs performance and can lead to burnout. The passage discusses how the demands of elite sport — intense training schedules, media scrutiny, performance expectations, and the precarious nature of athletic careers — create a uniquely stressful environment. The concept of the 'inverted-U hypothesis' is introduced, showing that optimal performance occurs at moderate levels of arousal, while both insufficient and excessive arousal degrade performance.\n\nThe passage then examines the physiological responses to stress in athletes, including elevated cortisol levels, increased heart rate, and changes in breathing patterns. It discusses how these physiological changes affect fine motor control, decision-making, and endurance. The role of the autonomic nervous system and the difference between 'choking' (performance failure due to over-arousal and self-consciousness) and 'clutch' performance (excelling under pressure through focused attention) is explored. Research on the effects of pre-competitive anxiety and its relationship to performance outcomes is presented.\n\nThe discussion also covers psychological interventions and coping strategies used by athletes. Techniques such as visualization, controlled breathing, progressive muscle relaxation, and cognitive restructuring are evaluated for their effectiveness. The passage considers the role of sport psychologists and the growing recognition of mental health as a critical component of athletic performance. It concludes with an examination of how different types of athletes — individuals in precision sports versus team sports, for example — may experience and respond to stress differently, and how training programmes are increasingly being designed to incorporate psychological resilience alongside physical preparation.",
    },
    "t2_p3": {
        "title": "An Inquiry into the Existence of the Gifted Child",
        "text": "This passage examines the concept of the 'gifted child' from multiple research perspectives, questioning both the validity and the practical implications of identifying children as gifted. It begins by tracing the history of gifted education, from Francis Galton's 19th-century work on hereditary genius through Lewis Terman's longitudinal study of high-IQ children and into contemporary debates. The passage highlights the lack of consensus among researchers about what giftedness actually means — whether it should be defined primarily through IQ scores, through demonstrated exceptional ability in specific domains, or through more multifaceted models such as Howard Gardner's theory of multiple intelligences and Joseph Renzulli's three-ring conception of giftedness.\n\nThe passage then discusses research findings on the characteristics and outcomes of children identified as gifted. While Terman's study showed that high-IQ children generally became successful adults, later research has complicated this picture by emphasising the role of creativity, motivation, opportunity, and what Angela Duckworth calls 'grit' in determining achievement. The passage critically examines the predictive validity of gifted identification, noting that many children identified as gifted do not go on to produce exceptional work in adulthood, while many eminent adults were not identified as gifted children. The distinction between 'academic giftedness' and 'creative productive giftedness' is explored.\n\nFinally, the passage considers the educational and social implications of the gifted label. Arguments for gifted programmes include the need to challenge able learners and prevent underachievement through boredom. However, the passage also reviews concerns about equity, noting that identification processes often disadvantage children from lower socioeconomic backgrounds and minority groups. The psychological effects of labelling are discussed, including both potential benefits (access to enriched programmes, peer grouping) and risks (anxiety, perfectionism, social isolation). The passage concludes by examining alternative approaches, such as enrichment for all students and talent development models that focus on cultivating potential rather than identifying fixed ability.",
    },
    # ========== TEST 3 ==========
    "t3_p1": {
        "title": "Archaeologists Discover Evidence of Prehistoric Island Settlers",
        "text": "This passage reports on recent archaeological discoveries that have reshaped understanding of early human migration and settlement on islands in the Mediterranean and Southeast Asia. It describes how sophisticated dating techniques and new excavation methods have revealed evidence of human presence on islands much earlier than previously believed. The discovery of stone tools, animal bones bearing cut marks, and charcoal from ancient hearths at several island sites has pushed back estimates for when early hominins first developed seafaring capabilities. The passage explains the significance of these findings for the debate about whether early humans deliberately navigated open water or reached islands accidentally on natural rafts.\n\nThe passage discusses specific archaeological sites that have yielded important findings. These include caves and rock shelters containing stratified deposits that document repeated occupation over thousands of years. The recovery of beads, pottery fragments, and the remains of imported materials such as obsidian provide evidence of trade networks and cultural exchange between islands and mainland communities. The discovery of spice residues on ancient pottery has been particularly significant, suggesting that the trade in aromatic plants and seasonings may have much deeper historical roots than the classical period.\n\nFinally, the passage considers the broader implications of these discoveries for understanding human cognitive and technological development. Building watercraft capable of open-sea voyages and navigating by currents, winds, and celestial cues required sophisticated planning, communication, and problem-solving abilities. The evidence suggests that early island settlers possessed these capabilities far earlier than previously assumed. The passage concludes by noting that ongoing excavations and advances in scientific analysis techniques continue to yield new evidence, and that current understanding of prehistoric island settlement is likely to undergo further revision.",
    },
    "t3_p2": {
        "title": "The Global Importance of Wetlands",
        "text": "This passage examines the ecological and economic significance of wetlands, which include marshes, swamps, bogs, and mangrove forests. It explains that wetlands are among the most productive ecosystems on Earth, providing essential services including water purification, flood regulation, carbon storage, and habitat for biodiversity. The passage notes that wetlands act as natural water filters, trapping sediments and breaking down pollutants before they reach rivers, lakes, and oceans. Their role in carbon sequestration is particularly important in the context of climate change, as peatlands store approximately twice as much carbon as all the world's forests combined, despite covering a much smaller area.\n\nThe passage describes the rich biodiversity supported by wetlands, from migratory waterbirds and fish nurseries to unique plant communities adapted to waterlogged conditions. Many species depend on wetlands for critical stages of their life cycles, and the loss or degradation of wetlands therefore has cascading effects on wider ecosystems. The discussion highlights the importance of wetlands as buffers against extreme weather events, absorbing excess rainfall and reducing the severity of floods, while also providing drought resilience by storing water that can be released during dry periods.\n\nHowever, the passage also documents the alarming rate of wetland loss globally. Drainage for agriculture, urban development, infrastructure projects, and pollution have destroyed an estimated 35% of the world's wetlands since 1970, with losses continuing at an accelerating pace. The passage discusses efforts to reverse this trend, including the Ramsar Convention on Wetlands, international conservation programmes, and restoration projects that aim to rehabilitate degraded wetland areas. It concludes by arguing that recognising the true economic and ecological value of wetlands — including their role in climate regulation and disaster risk reduction — is essential for securing political will and investment in their protection.",
    },
    "t3_p3": {
        "title": "Is the Era of Artificial Speech Translation Upon Us?",
        "text": "This passage explores recent advances in artificial intelligence that have transformed speech translation, making real-time spoken language translation increasingly practical and accurate. It describes the technological developments that underpin modern systems, including deep neural networks, attention-based transformer models, and end-to-end architectures that translate speech directly from audio rather than going through an intermediate text step. The passage discusses how these systems have improved dramatically in recent years, achieving near-human performance on some language pairs and in constrained contexts such as travel or business conversations.\n\nThe passage examines the current limitations and challenges facing speech translation technology. Accents, regional dialects, code-switching (mixing languages within a conversation), emotional tone, and context-dependent meaning all present significant difficulties. The problem of latency — the delay between someone speaking and the translation being delivered — is discussed, as even small delays can disrupt the natural flow of conversation. The passage also considers the challenge of domain-specific vocabulary and the difficulty that AI systems face with ambiguity, sarcasm, and culturally specific references that require world knowledge rather than purely linguistic processing.\n\nFinally, the passage addresses the broader implications of artificial speech translation for society. It explores whether widespread adoption of this technology will reduce the incentive to learn foreign languages, potentially diminishing linguistic diversity and cultural understanding, or whether it will facilitate greater cross-cultural communication and collaboration. The discussion includes the potential impact on international business, diplomacy, tourism, and the accessibility of information across language barriers. The author suggests that while speech translation technology is unlikely to fully replace human interpreters for high-stakes situations in the foreseeable future, it will increasingly handle routine translation needs and potentially reshape how people communicate across linguistic boundaries.",
    },
    # ========== TEST 4 ==========
    "t4_p1": {
        "title": "The Impact of Climate Change on Butterflies in Britain",
        "text": "This passage examines how butterfly populations in Britain are responding to the effects of climate change, drawing on long-term monitoring data collected by volunteer recorders across the country. It explains that butterflies, as cold-blooded insects with specific habitat requirements and limited dispersal abilities, are highly sensitive indicators of environmental change. The passage discusses how rising average temperatures have allowed some species to expand their ranges northward, while others have shifted their flight periods earlier in the year. Species that were once confined to southern England, such as the comma and the speckled wood, have colonised new areas as conditions have become more favourable.\n\nHowever, the passage also documents the serious negative impacts of climate change on many butterfly species. Warmer, drier summers can reduce the availability of larval food plants, while extreme weather events such as droughts and heavy rainfall directly affect survival rates. The mismatch between butterfly emergence dates and the flowering of nectar sources is explored as a growing concern. The passage notes that species with specialised habitat requirements or limited mobility are particularly vulnerable, and several of Britain's rarest butterflies face heightened extinction risk as suitable habitat shrinks and fragments.\n\nThe passage goes on to discuss the interaction between climate change and habitat loss, noting that butterflies already stressed by habitat fragmentation are less able to adapt to changing climatic conditions. Conservation strategies, including the creation of habitat corridors, assisted colonisation, and landscape-scale conservation approaches, are evaluated for their potential to help butterfly populations build resilience. The passage concludes by reflecting on what the changing fortunes of Britain's butterflies suggest about the broader impacts of climate change on biodiversity, and emphasises the importance of continued monitoring and adaptive management.",
    },
    "t4_p2": {
        "title": "Deep-Sea Mining",
        "text": "This passage explores the emerging industry of deep-sea mining, which aims to extract mineral resources from the ocean floor at depths of up to 6,000 metres. It describes the types of deposits that have attracted commercial interest, including polymetallic nodules scattered across abyssal plains, seafloor massive sulphides formed around hydrothermal vents, and cobalt-rich ferromanganese crusts on seamounts. These deposits contain metals critical for modern technology, including manganese, nickel, cobalt, copper, and rare earth elements used in batteries, electronics, and renewable energy infrastructure. The passage explains the economic arguments for deep-sea mining, including the increasing demand for these metals and the desire to reduce dependence on terrestrial mining in sensitive areas.\n\nThe passage then examines the significant environmental concerns associated with deep-sea mining. The ocean floor hosts unique and poorly understood ecosystems that would be directly destroyed by mining operations. Hydrothermal vent communities, which include species found nowhere else on Earth, are particularly vulnerable. The passage discusses potential impacts including sediment plumes that could smother organisms far from the mining site, noise and light pollution, and disruption of the vertical transport of organic matter that sustains deep-sea food webs. The long recovery times of these ecosystems are highlighted, with some areas potentially requiring centuries or more to regenerate after disturbance.\n\nFinally, the passage considers the regulatory framework governing deep-sea mining. The International Seabed Authority, established under the United Nations Convention on the Law of the Sea, is responsible for managing mineral resources in international waters and developing rules for exploitation. The passage discusses debates among member states, environmental organisations, and mining companies about the appropriate balance between resource extraction and environmental protection. It concludes by considering whether deep-sea mining can be conducted in an environmentally responsible manner, and what lessons might be learned from the history of terrestrial mining about the precautionary principle and the difficulty of predicting long-term ecological consequences.",
    },
    "t4_p3": {
        "title": "The Unselfish Gene",
        "text": "This passage examines the evolutionary puzzle of altruism — behaviour that benefits others at a cost to the individual performing it. From a Darwinian perspective, where natural selection favours traits that maximise an individual's reproductive success, self-sacrificing behaviour appears paradoxical. The passage introduces the concept of kin selection, first articulated by W.D. Hamilton in the 1960s, which explains altruism towards close relatives through the idea of inclusive fitness: by helping relatives survive and reproduce, an individual indirectly propagates copies of their shared genes. Hamilton's rule, which quantifies when altruistic behaviour will evolve, is presented and explained.\n\nThe passage then extends the discussion beyond kin to examine reciprocal altruism — the principle of 'I'll scratch your back if you scratch mine' — and the conditions under which cooperation between unrelated individuals can evolve. It discusses Robert Trivers' work on reciprocal altruism and the role of repeated interactions, reputation, and the threat of punishment in stabilising cooperative behaviour. Game theory models, particularly the prisoner's dilemma and its iterated version, are used to illustrate how cooperation can emerge and persist even among self-interested agents. The passage explores how these dynamics play out in animal societies, from vampire bats sharing blood meals to cleaner fish and their clients.\n\nFinally, the passage considers the broader implications of the evolutionary approach to altruism for understanding human morality and social institutions. It discusses the concept of 'group selection' — the controversial idea that natural selection can act on groups rather than just individuals — and examines how culture, norms, and institutions may have evolved to promote cooperative behaviour in large-scale human societies where genetic relatedness is low. The passage concludes by reflecting on what the evolutionary perspective reveals about the biological foundations of ethics, and whether the fact that altruism can be explained in terms of genetic self-interest undermines or enriches our understanding of genuine moral behaviour.",
    },
}

###############################################################################
# READING QUESTIONS (all 4 tests, 3 passages each, 160 total)
###############################################################################

def make_reading():
    tests = []

    # ========== TEST 1 ==========
    t1_passages = []

    # Passage 1: How Tennis Rackets Have Changed (Q1-13)
    t1_p1_qs = []
    # Q1-7: tfng
    t1_p1_qs.extend([
        {"id": "cam19_t1_r_q1", "type": "tfng", "question": "Modern tennis rackets are heavier than rackets used in the 19th century.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE"},
        {"id": "cam19_t1_r_q2", "type": "tfng", "question": "The first graphite tennis rackets went into production in the 1960s.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE"},
        {"id": "cam19_t1_r_q3", "type": "tfng", "question": "All professional tennis players now use polyester strings.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
        {"id": "cam19_t1_r_q4", "type": "tfng", "question": "Larger racket heads have increased the size of the sweet spot.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE"},
        {"id": "cam19_t1_r_q5", "type": "tfng", "question": "Changes to racket technology have made the game easier for beginners.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
        {"id": "cam19_t1_r_q6", "type": "tfng", "question": "The development of new string materials has affected how players generate spin.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "TRUE"},
        {"id": "cam19_t1_r_q7", "type": "tfng", "question": "There is concern that technology may have reduced the importance of skill in tennis.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "TRUE"},
    ])
    # Q8-13: notes_completion
    for i, (qtext, ans) in enumerate([
        ("The first tennis rackets were made from wood, and they needed to be coated with protective 8. _____", "paint"),
        ("Modern rackets help players put a heavy 9. _____ on the ball", "topspin"),
        ("The materials used today allow strings to be tightened to a much higher 10. _____ level", "training"),
        ("Early rackets used natural materials like sheep 11. _____ for strings", "gut"),
        ("Changes to frame 12. _____ have affected the balance of modern rackets", "weights"),
        ("The development of synthetic 13. _____ has improved handling and comfort", "grips"),
    ], 8):
        t1_p1_qs.append({"id": f"cam19_t1_r_q{i}", "type": "notes_completion", "question": qtext, "options": [], "correctAnswer": ans})
    t1_passages.append({"id": "cam19_t1_p1", "title": "How Tennis Rackets Have Changed", "text": PASSAGES["t1_p1"]["text"], "timeRecommended": 20, "questions": t1_p1_qs})

    # Passage 2: The Pirates of the Ancient Mediterranean (Q14-26)
    t1_p2_qs = []
    # Q14-23: matching_info (paragraph/section matching with options A-G)
    for i, (qtext, ans) in enumerate([
        ("the use of small, fast boats that outmatched larger warships", "D"),
        ("the organisation of ransom operations involving intermediaries in many ports", "G"),
        ("the role of geography in providing safe bases for pirate activity", "C"),
        ("how piracy affected the cost of food in Rome", "A"),
        ("how captured pirates were resettled after being defeated", "G"),
        ("the strategy of dividing the Mediterranean into zones for a military campaign", "B"),
        ("the establishment of a law giving a commander special authority", "B"),
        ("the types of goods pirates traded, including enslaved people", "D"),
        ("the way pirates gathered intelligence on shipping movements", "C"),
        ("the speed with which the pirate threat was eliminated once a major campaign began", "E"),
    ], 14):
        t1_p2_qs.append({"id": f"cam19_t1_r_q{i}", "type": "matching_info", "question": qtext, "options": ["A", "B", "C", "D", "E", "F", "G"], "correctAnswer": ans})
    # Q24-26: summary_completion
    for i, (qtext, ans) in enumerate([
        ("Pirates stored their plunder, including valuable items such as 24. _____", "grain"),
        ("Captured individuals were subjected to harsh 25. _____ if their families could not pay", "punishment"),
        ("Kidnapped victims were held until a 26. _____ was paid for their release", "ransom"),
    ], 24):
        t1_p2_qs.append({"id": f"cam19_t1_r_q{i}", "type": "summary_completion", "question": qtext, "options": [], "correctAnswer": ans})
    t1_passages.append({"id": "cam19_t1_p2", "title": "The Pirates of the Ancient Mediterranean", "text": PASSAGES["t1_p2"]["text"], "timeRecommended": 20, "questions": t1_p2_qs})

    # Passage 3: The Persistence and Peril of Misinformation (Q27-40)
    t1_p3_qs = []
    # Q27-30: multiple_choice
    for i, ans in enumerate(["D", "A", "C", "D"], 27):
        t1_p3_qs.append({"id": f"cam19_t1_r_q{i}", "type": "multiple_choice", "question": f"Question {i}: Choose the correct letter, A, B, C or D.", "options": ["A", "B", "C", "D"], "correctAnswer": ans})
    # Q31-36: matching_names
    t1_p3_names = [
        "A. the familiarity effect", "B. confirmation bias", "C. fluency heuristic",
        "D. continued influence effect", "E. resonance with existing narratives",
        "F. echo chambers", "G. frequent exposure", "H. mental operation",
        "I. narrative replacement", "J. different ideas",
    ]
    for i, (qtext, ans) in enumerate([
        ("causes people to believe something simply because they have heard it many times before", "G"),
        ("the phenomenon where people continue to accept discredited information", "J"),
        ("a cognitive process that relies on how easily information comes to mind", "H"),
        ("the tendency to search for or interpret information in a way that confirms one's beliefs", "B"),
        ("the idea that misinformation is more durable when it fits a familiar story pattern", "E"),
        ("online environments where people are exposed only to information that reinforces existing views", "C"),
    ], 31):
        t1_p3_qs.append({"id": f"cam19_t1_r_q{i}", "type": "matching_names", "question": qtext, "options": t1_p3_names, "correctAnswer": ans})
    # Q37-40: ynng
    t1_p3_qs.extend([
        {"id": "cam19_t1_r_q37", "type": "ynng", "question": "Repeating a false claim while correcting it can actually make the misinformation more familiar.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "YES"},
        {"id": "cam19_t1_r_q38", "type": "ynng", "question": "Fact-checking organisations have been successful in stopping the spread of political misinformation.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
        {"id": "cam19_t1_r_q39", "type": "ynng", "question": "Simply telling people that a claim is false is an effective way to change their beliefs.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "NO"},
        {"id": "cam19_t1_r_q40", "type": "ynng", "question": "Pre-emptive exposure to weakened misleading arguments can help people resist misinformation.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
    ])
    t1_passages.append({"id": "cam19_t1_p3", "title": "The Persistence and Peril of Misinformation", "text": PASSAGES["t1_p3"]["text"], "timeRecommended": 20, "questions": t1_p3_qs})

    tests.append({"id": "cam19_test1", "testNumber": 1, "passages": t1_passages})

    # ========== TEST 2 ==========
    t2_passages = []

    # Passage 1: The Industrial Revolution in Britain (Q1-13)
    t2_p1_qs = []
    # Q1-7: notes_completion
    for i, (qtext, ans) in enumerate([
        ("The invention of the steam 1. _____ provided reliable power for factories", "piston"),
        ("Rich deposits of iron ore and 2. _____ were key natural resources", "coal"),
        ("Textile production expanded rapidly with machines such as the spinning jenny and power looms installed in 3. _____", "workshops"),
        ("Displaced agricultural workers became a mobile source of 4. _____", "labour"),
        ("British banks and legal institutions supported investment and protected 5. _____", "quality"),
        ("The construction of canals and 6. _____ improved transport infrastructure", "railways"),
        ("Rapid urbanisation created severe problems with overcrowding and poor 7. _____", "sanitation"),
    ], 1):
        t2_p1_qs.append({"id": f"cam19_t2_r_q{i}", "type": "notes_completion", "question": qtext, "options": [], "correctAnswer": ans})
    # Q8-13: tfng
    t2_p1_qs.extend([
        {"id": "cam19_t2_r_q8", "type": "tfng", "question": "The British government provided direct financial support for the early textile factories.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
        {"id": "cam19_t2_r_q9", "type": "tfng", "question": "The enclosure movement mainly benefited small farmers.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE"},
        {"id": "cam19_t2_r_q10", "type": "tfng", "question": "James Watt was the only person to improve the steam engine during the Industrial Revolution.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
        {"id": "cam19_t2_r_q11", "type": "tfng", "question": "The Factory Acts were introduced in response to public concern about working conditions.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "TRUE"},
        {"id": "cam19_t2_r_q12", "type": "tfng", "question": "Britain's colonial trade network contributed to the growth of its industrial economy.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "TRUE"},
        {"id": "cam19_t2_r_q13", "type": "tfng", "question": "The Industrial Revolution led to a decrease in the total population of British cities.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
    ])
    t2_passages.append({"id": "cam19_t2_p1", "title": "The Industrial Revolution in Britain", "text": PASSAGES["t2_p1"]["text"], "timeRecommended": 20, "questions": t2_p1_qs})

    # Passage 2: Athletes and Stress (Q14-26)
    t2_p2_qs = []
    # Q14-18: matching_info
    for i, (qtext, ans) in enumerate([
        ("the distinction between stress that helps and stress that harms performance", "C"),
        ("ways in which sport psychologists help athletes manage competitive pressure", "F"),
        ("the physical changes that occur in the body during stressful situations", "A"),
        ("the difference between failing under pressure and excelling under pressure", "D"),
        ("the idea that there is an optimal level of stress for peak performance", "F"),
    ], 14):
        t2_p2_qs.append({"id": f"cam19_t2_r_q{i}", "type": "matching_info", "question": qtext, "options": ["A", "B", "C", "D", "E", "F"], "correctAnswer": ans})
    # Q19-22: notes_completion
    for i, (qtext, ans) in enumerate([
        ("Athletes who cannot handle pressure may experience 19. _____ in their performance", "failure"),
        ("Techniques such as visualisation and controlled breathing can help athletes regulate their stress 20. _____", "shots"),
        ("Positive stress can produce feelings of 21. _____ that enhance focus", "excitement"),
        ("Deep 22. _____ exercises can activate the parasympathetic nervous system and calm the body", "breathing"),
    ], 19):
        t2_p2_qs.append({"id": f"cam19_t2_r_q{i}", "type": "notes_completion", "question": qtext, "options": [], "correctAnswer": ans})
    # Q23-26: multiple_choice
    for i, ans in enumerate(["B", "D", "B", "C"], 23):
        t2_p2_qs.append({"id": f"cam19_t2_r_q{i}", "type": "multiple_choice", "question": f"Question {i}: Choose the correct letter, A, B, C or D.", "options": ["A", "B", "C", "D"], "correctAnswer": ans})
    t2_passages.append({"id": "cam19_t2_p2", "title": "Athletes and Stress", "text": PASSAGES["t2_p2"]["text"], "timeRecommended": 20, "questions": t2_p2_qs})

    # Passage 3: An Inquiry into the Existence of the Gifted Child (Q27-40)
    t2_p3_qs = []
    # Q27-32: matching_names
    t2_p3_names = [
        "A. appeal", "B. determined", "C. intrigued", "D. creative productive giftedness",
        "E. academic giftedness", "F. Howard Gardner", "G. Joseph Renzulli",
        "H. unique", "I. innovative", "J. satisfaction",
    ]
    for i, (qtext, ans) in enumerate([
        ("belief that giftedness is a fixed trait identifiable through IQ tests", "H"),
        ("ability to think of novel solutions to complex problems, distinct from academic ability", "A"),
        ("the tendency for high-IQ children to perform well in traditional educational settings", "C"),
        ("the argument that effort and perseverance matter more than innate talent", "B"),
        ("the idea that success in later life is correlated with a sense of fulfillment", "J"),
        ("creativity in developing original approaches, often leading to breakthroughs", "I"),
    ], 27):
        t2_p3_qs.append({"id": f"cam19_t2_r_q{i}", "type": "matching_names", "question": qtext, "options": t2_p3_names, "correctAnswer": ans})
    # Q33-37: ynng
    t2_p3_qs.extend([
        {"id": "cam19_t2_r_q33", "type": "ynng", "question": "Children identified as gifted consistently maintain their advantage into adulthood.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "YES"},
        {"id": "cam19_t2_r_q34", "type": "ynng", "question": "Gifted programmes in schools have been shown to improve outcomes for all students.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
        {"id": "cam19_t2_r_q35", "type": "ynng", "question": "There is evidence that labelling a child as gifted can create psychological pressures.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "YES"},
        {"id": "cam19_t2_r_q36", "type": "ynng", "question": "Most gifted education programmes identify children from all socioeconomic backgrounds equally.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
        {"id": "cam19_t2_r_q37", "type": "ynng", "question": "The author believes that identifying children as gifted does more harm than good.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "NO"},
    ])
    # Q38-40: multiple_choice
    for i, ans in enumerate(["C", "B", "D"], 38):
        t2_p3_qs.append({"id": f"cam19_t2_r_q{i}", "type": "multiple_choice", "question": f"Question {i}: Choose the correct letter, A, B, C or D.", "options": ["A", "B", "C", "D"], "correctAnswer": ans})
    t2_passages.append({"id": "cam19_t2_p3", "title": "An Inquiry into the Existence of the Gifted Child", "text": PASSAGES["t2_p3"]["text"], "timeRecommended": 20, "questions": t2_p3_qs})

    tests.append({"id": "cam19_test2", "testNumber": 2, "passages": t2_passages})

    # ========== TEST 3 ==========
    t3_passages = []

    # Passage 1: Archaeologists Discover Evidence of Prehistoric Island Settlers (Q1-13)
    t3_p1_qs = []
    # Q1-7: tfng
    t3_p1_qs.extend([
        {"id": "cam19_t3_r_q1", "type": "tfng", "question": "Archaeologists have found evidence that early humans reached islands much later than previously thought.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE"},
        {"id": "cam19_t3_r_q2", "type": "tfng", "question": "Stone tools found on islands show clear signs of having been made by early hominins.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE"},
        {"id": "cam19_t3_r_q3", "type": "tfng", "question": "The discovery of burnt animal bones suggests that early island settlers used fire.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "TRUE"},
        {"id": "cam19_t3_r_q4", "type": "tfng", "question": "Most early island settlements were located on large islands visible from the mainland.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
        {"id": "cam19_t3_r_q5", "type": "tfng", "question": "The presence of obsidian on islands indicates that trade networks existed with mainland communities.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "TRUE"},
        {"id": "cam19_t3_r_q6", "type": "tfng", "question": "The earliest island settlers used metal tools for constructing watercraft.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
        {"id": "cam19_t3_r_q7", "type": "tfng", "question": "All evidence of prehistoric island settlement comes from Mediterranean sites.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE"},
    ])
    # Q8-13: notes_completion
    for i, (qtext, ans) in enumerate([
        ("Archaeologists have found evidence of occupation in coastal 8. _____", "caves"),
        ("Excavations have uncovered tools made from 9. _____", "stone"),
        ("The remains of animal 10. _____ with cut marks provide evidence of butchery", "bones"),
        ("Ornamental 11. _____ made from shell and bone indicate cultural activity", "beads"),
        ("Fragments of 12. _____ show that early settlers produced containers", "pottery"),
        ("Residues of 13. _____ on ancient pottery suggest early trade in aromatic goods", "spices"),
    ], 8):
        t3_p1_qs.append({"id": f"cam19_t3_r_q{i}", "type": "notes_completion", "question": qtext, "options": [], "correctAnswer": ans})
    t3_passages.append({"id": "cam19_t3_p1", "title": "Archaeologists Discover Evidence of Prehistoric Island Settlers", "text": PASSAGES["t3_p1"]["text"], "timeRecommended": 20, "questions": t3_p1_qs})

    # Passage 2: The Global Importance of Wetlands (Q14-26)
    t3_p2_qs = []
    # Q14-17: matching_info
    for i, (qtext, ans) in enumerate([
        ("a description of how wetlands serve as natural flood defences", "G"),
        ("the frightening rate at which wetlands are being lost worldwide", "A"),
        ("the role of peatlands in absorbing and storing atmospheric carbon", "H"),
        ("an explanation of how wetlands filter pollutants from water", "B"),
    ], 14):
        t3_p2_qs.append({"id": f"cam19_t3_r_q{i}", "type": "matching_info", "question": qtext, "options": ["A", "B", "C", "D", "E", "F", "G", "H"], "correctAnswer": ans})
    # Q18-22: notes_completion
    for i, (qtext, ans) in enumerate([
        ("Wetlands play a crucial role in the 18. _____ cycle, storing large amounts of this element in their soils", "carbon"),
        ("Drainage of peatlands for agriculture releases large amounts of greenhouse gases through 19. _____", "fires"),
        ("Wetlands support a huge range of plant and animal life, contributing significantly to global 20. _____", "biodiversity"),
        ("The construction of 21. _____ for agriculture has caused widespread drying of wetland areas", "ditches"),
        ("When peatlands are drained, the ground compacts and this process of 22. _____ releases stored carbon", "subsidence"),
    ], 18):
        t3_p2_qs.append({"id": f"cam19_t3_r_q{i}", "type": "notes_completion", "question": qtext, "options": [], "correctAnswer": ans})
    # Q23-26: matching_names
    t3_p2_names = [
        "A. Matthew McCartney",
        "B. Pieter van Eijk",
        "C. Marcel Silvius",
        "D. Dave Tickner",
    ]
    for i, (qtext, ans) in enumerate([
        ("has studied the economic value of wetland ecosystem services in developing countries", "A"),
        ("investigated the role of wetlands in supporting freshwater fisheries in Southeast Asia", "C"),
        ("argues that wetlands are undervalued in policy decisions about land use", "D"),
        ("has researched the impact of agricultural drainage on carbon emissions from peatlands", "B"),
    ], 23):
        t3_p2_qs.append({"id": f"cam19_t3_r_q{i}", "type": "matching_names", "question": qtext, "options": t3_p2_names, "correctAnswer": ans})
    t3_passages.append({"id": "cam19_t3_p2", "title": "The Global Importance of Wetlands", "text": PASSAGES["t3_p2"]["text"], "timeRecommended": 20, "questions": t3_p2_qs})

    # Passage 3: Is the Era of Artificial Speech Translation Upon Us? (Q27-40)
    t3_p3_qs = []
    # Q27-30: multiple_choice
    for i, ans in enumerate(["D", "A", "C", "B"], 27):
        t3_p3_qs.append({"id": f"cam19_t3_r_q{i}", "type": "multiple_choice", "question": f"Question {i}: Choose the correct letter, A, B, C or D.", "options": ["A", "B", "C", "D"], "correctAnswer": ans})
    # Q31-34: matching
    t3_p3_match_options = [
        "A. challenges with accents and dialects",
        "B. difficulty with cultural references and sarcasm",
        "C. problems with latency in real-time translation",
        "D. difficulty translating emotional tone",
        "E. problems with domain-specific vocabulary",
        "F. difficulty handling code-switching between languages",
    ]
    for i, (qtext, ans) in enumerate([
        ("the delay between speech input and translated output", "C"),
        ("the challenge of translating when speakers switch between two languages in one conversation", "E"),
        ("the difficulty of understanding implied meaning and humour that depends on shared cultural knowledge", "F"),
        ("the difficulty of translating specialised terms used in professional or technical fields", "B"),
    ], 31):
        t3_p3_qs.append({"id": f"cam19_t3_r_q{i}", "type": "matching", "question": qtext, "options": t3_p3_match_options, "correctAnswer": ans})
    # Q35-40: ynng
    t3_p3_qs.extend([
        {"id": "cam19_t3_r_q35", "type": "ynng", "question": "Current speech translation systems achieve better results on European language pairs than on Asian ones.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "NO"},
        {"id": "cam19_t3_r_q36", "type": "ynng", "question": "There is concern that speech translation could reduce the motivation to learn other languages.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "YES"},
        {"id": "cam19_t3_r_q37", "type": "ynng", "question": "The author believes that AI speech translation will eventually replace human interpreters entirely.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "NO"},
        {"id": "cam19_t3_r_q38", "type": "ynng", "question": "Speech translation technology is already widely used in international diplomacy.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
        {"id": "cam19_t3_r_q39", "type": "ynng", "question": "End-to-end speech translation systems perform better than those using intermediate text conversion.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
        {"id": "cam19_t3_r_q40", "type": "ynng", "question": "Accurate real-time speech translation could significantly improve cross-cultural communication.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "YES"},
    ])
    t3_passages.append({"id": "cam19_t3_p3", "title": "Is the Era of Artificial Speech Translation Upon Us?", "text": PASSAGES["t3_p3"]["text"], "timeRecommended": 20, "questions": t3_p3_qs})

    tests.append({"id": "cam19_test3", "testNumber": 3, "passages": t3_passages})

    # ========== TEST 4 ==========
    t4_passages = []

    # Passage 1: The Impact of Climate Change on Butterflies in Britain (Q1-13)
    t4_p1_qs = []
    # Q1-6: tfng
    t4_p1_qs.extend([
        {"id": "cam19_t4_r_q1", "type": "tfng", "question": "Butterflies are useful indicators of environmental change because they are cold-blooded.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE"},
        {"id": "cam19_t4_r_q2", "type": "tfng", "question": "Rising temperatures have allowed some butterfly species to move into areas where they were not previously found.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "TRUE"},
        {"id": "cam19_t4_r_q3", "type": "tfng", "question": "All butterfly species in Britain have expanded their ranges as a result of climate change.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE"},
        {"id": "cam19_t4_r_q4", "type": "tfng", "question": "Butterflies with generalist diets are more affected by climate change than specialists.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
        {"id": "cam19_t4_r_q5", "type": "tfng", "question": "The comma butterfly was previously confined to the north of England.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE"},
        {"id": "cam19_t4_r_q6", "type": "tfng", "question": "Extreme weather events such as droughts have been shown to affect butterfly survival rates directly.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "TRUE"},
    ])
    # Q7-13: notes_completion
    for i, (qtext, ans) in enumerate([
        ("Some butterfly 7. _____ have been observed moving northwards as temperatures rise", "colonies"),
        ("Butterflies are emerging earlier in the 8. _____ each year", "spring"),
        ("Several rare species face an increased risk of becoming 9. _____", "endangered"),
        ("The creation of corridors can help connect fragmented 10. _____", "habitats"),
        ("Long-term monitoring data has been collected by volunteer recorders across 11. _____", "Europe"),
        ("Species in the 12. _____ parts of Britain are at greatest risk from warming", "southern"),
        ("Changes in the availability of larval food plants can affect butterfly 13. _____", "diet"),
    ], 7):
        t4_p1_qs.append({"id": f"cam19_t4_r_q{i}", "type": "notes_completion", "question": qtext, "options": [], "correctAnswer": ans})
    t4_passages.append({"id": "cam19_t4_p1", "title": "The Impact of Climate Change on Butterflies in Britain", "text": PASSAGES["t4_p1"]["text"], "timeRecommended": 20, "questions": t4_p1_qs})

    # Passage 2: Deep-Sea Mining (Q14-26)
    t4_p2_qs = []
    # Q14-17: matching_info
    for i, (qtext, ans) in enumerate([
        ("an explanation of the types of mineral deposits found on the ocean floor", "C"),
        ("a description of the environmental damage caused by sediment plumes", "F"),
        ("reasons why deep-sea minerals are in demand for green technology", "E"),
        ("the role of the International Seabed Authority in regulating mining", "D"),
    ], 14):
        t4_p2_qs.append({"id": f"cam19_t4_r_q{i}", "type": "matching_info", "question": qtext, "options": ["A", "B", "C", "D", "E", "F"], "correctAnswer": ans})
    # Q18-23: matching_names
    t4_p2_names = [
        "A. Mat Upton",
        "B. Hunter, Aguon & Singh",
        "C. Jon Copley",
        "D. Mike Johnston",
        "E. Verena Tunnicliffe",
    ]
    for i, (qtext, ans) in enumerate([
        ("has researched the biodiversity of hydrothermal vent ecosystems and their vulnerability to mining", "D"),
        ("argues that deep-sea mining regulations should incorporate stronger environmental safeguards", "B"),
        ("has studied the potential impact of mining on deep-sea sediment communities", "A"),
        ("investigated the unique species found at hydrothermal vents in the Pacific Ocean", "E"),
        ("warns that the rush to exploit deep-sea minerals could outpace environmental understanding", "B"),
        ("explored the possibility that deep-sea mining could disrupt carbon storage in ocean sediments", "C"),
    ], 18):
        t4_p2_qs.append({"id": f"cam19_t4_r_q{i}", "type": "matching_names", "question": qtext, "options": t4_p2_names, "correctAnswer": ans})
    # Q24-26: notes_completion
    for i, (qtext, ans) in enumerate([
        ("Deep-sea mining could generate large amounts of 24. _____ that would need to be disposed of carefully", "waste"),
        ("The operation of underwater vehicles and 25. _____ would create noise pollution in the deep ocean", "machinery"),
        ("Many scientists argue that a precautionary approach based on 26. _____ should be adopted", "caution"),
    ], 24):
        t4_p2_qs.append({"id": f"cam19_t4_r_q{i}", "type": "notes_completion", "question": qtext, "options": [], "correctAnswer": ans})
    t4_passages.append({"id": "cam19_t4_p2", "title": "Deep-Sea Mining", "text": PASSAGES["t4_p2"]["text"], "timeRecommended": 20, "questions": t4_p2_qs})

    # Passage 3: The Unselfish Gene (Q27-40)
    t4_p3_qs = []
    # Q27-30: multiple_choice
    for i, ans in enumerate(["C", "C", "B", "A"], 27):
        t4_p3_qs.append({"id": f"cam19_t4_r_q{i}", "type": "multiple_choice", "question": f"Question {i}: Choose the correct letter, A, B, C or D.", "options": ["A", "B", "C", "D"], "correctAnswer": ans})
    # Q31-35: notes_completion
    for i, (qtext, ans) in enumerate([
        ("Hamilton's theory of inclusive fitness predicts that altruism evolves more readily in societies with a high degree of 31. _____", "egalitarianism"),
        ("Reciprocal altruism is more likely to evolve when individuals can recognise each other and remember past interactions, building a 32. _____ system", "status"),
        ("In some animal societies, individuals engage in cooperative 33. _____ where they share food with non-relatives who have previously shared with them", "hunting"),
        ("The prisoner's dilemma model shows that purely selfish strategies are not always optimal, especially when individuals can punish 34. _____ behaviour", "domineering"),
        ("In human societies, cultural norms and institutions can promote cooperation even among strangers, reducing the need for genetic relatedness as a basis for 35. _____", "autonomy"),
    ], 31):
        t4_p3_qs.append({"id": f"cam19_t4_r_q{i}", "type": "notes_completion", "question": qtext, "options": [], "correctAnswer": ans})
    # Q36-40: ynng
    t4_p3_qs.extend([
        {"id": "cam19_t4_r_q36", "type": "ynng", "question": "The author believes that explaining altruism in evolutionary terms diminishes its moral value.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
        {"id": "cam19_t4_r_q37", "type": "ynng", "question": "Reciprocal altruism requires individuals to keep track of who has helped them in the past.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "NO"},
        {"id": "cam19_t4_r_q38", "type": "ynng", "question": "The iterated prisoner's dilemma shows that cooperation can be a stable strategy.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "YES"},
        {"id": "cam19_t4_r_q39", "type": "ynng", "question": "Most animals engage in reciprocal altruism with unrelated individuals.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
        {"id": "cam19_t4_r_q40", "type": "ynng", "question": "Kin selection can explain all examples of altruistic behaviour observed in nature.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "NO"},
    ])
    t4_passages.append({"id": "cam19_t4_p3", "title": "The Unselfish Gene", "text": PASSAGES["t4_p3"]["text"], "timeRecommended": 20, "questions": t4_p3_qs})

    tests.append({"id": "cam19_test4", "testNumber": 4, "passages": t4_passages})

    return {"id": "cam19", "title": "Cambridge IELTS 19 Academic Reading", "tests": tests}


###############################################################################
# LISTENING DATA
###############################################################################

def make_listening():
    tests = []

    # ========== LISTENING TEST 1 ==========
    lt1_parts = []

    # Part 1: Hinchingbrooke Country Park (Q1-10)
    lt1_p1_qs = []
    for i, (qtext, ans) in enumerate([
        ("1. Entry fee: £_____", "69"),
        ("2. Feature: _____", "Stream"),
        ("3. Information about wildlife: _____ Centre", "Data"),
        ("4. Free: _____ of the park", "Map"),
        ("5. Car park for: _____", "Visitors"),
        ("6. Audio guide for: _____ of nature", "Sounds"),
        ("7. Main attraction: _____ Trail", "Freedom"),
        ("8. Children's activity: _____ Workshop", "Skills"),
        ("9. Guide book price: £_____", "4.95"),
        ("10. Event for: _____", "Leaders"),
    ], 1):
        lt1_p1_qs.append({"id": f"cam19_lt1_q{i}", "type": "notes_completion", "question": qtext, "options": [], "correctAnswer": ans})
    lt1_parts.append({"id": "cam19_lt1_p1", "title": "Hinchingbrooke Country Park", "audioFile": "cam19_test1_part1.mp3", "subtitle": "", "duration": "", "questions": lt1_p1_qs})

    # Part 2: Stanthorpe Twinning Association (Farley House) (Q11-20)
    lt1_p2_qs = []
    for i, ans in enumerate(["B", "A", "B", "C", "A"], 11):
        lt1_p2_qs.append({"id": f"cam19_lt1_q{i}", "type": "multiple_choice", "question": f"Question {i}: Choose the correct letter, A, B or C.", "options": ["A", "B", "C"], "correctAnswer": ans})
    for i, (qtext, ans) in enumerate([
        ("11. Farm shop: _____", "G"),
        ("12. Disabled entry: _____", "C"),
        ("13. Adventure playground: _____", "B"),
        ("14. Kitchen gardens: _____", "D"),
        ("15. The Temple of the Four Winds: _____", "A"),
    ], 16):
        lt1_p2_qs.append({"id": f"cam19_lt1_q{i}", "type": "matching", "question": f"Match the location to the correct letter on the map.", "options": ["A", "B", "C", "D", "E", "F", "G"], "correctAnswer": ans})
    lt1_parts.append({"id": "cam19_lt1_p2", "title": "Stanthorpe Twinning Association (Farley House)", "audioFile": "cam19_test1_part2.mp3", "subtitle": "", "duration": "", "questions": lt1_p2_qs})

    # Part 3: Food Trends Discussion (Q21-30)
    lt1_p3_qs = []
    for i, ans in enumerate(["B", "D", "A", "E"], 21):
        lt1_p3_qs.append({"id": f"cam19_lt1_q{i}", "type": "multiple_choice", "question": f"Question {i}: Choose the correct letter, A, B, C or D.", "options": ["A", "B", "C", "D"], "correctAnswer": ans})
    lt1_p3_mq_options = [
        "A. Consumers should be given clearer guidance",
        "B. This may have disappointing results",
        "C. This already seems to be widespread",
        "D. Retailers should do more to encourage this",
        "E. Manufacturers should be required to label this",
        "F. Most people know little about this",
        "G. There should be stricter regulations",
        "H. This could be dangerous",
    ]
    for i, (qtext, ans) in enumerate([
        ("25. Reducing food packaging: _____", "D"),
        ("26. Using sustainable farming methods: _____", "G"),
        ("27. Cutting down on meat consumption: _____", "C"),
        ("28. Eating locally sourced food: _____", "B"),
        ("29. Understanding food supply chains: _____", "F"),
        ("30. Artificial additives in processed food: _____", "H"),
    ], 25):
        lt1_p3_qs.append({"id": f"cam19_lt1_q{i}", "type": "matching", "question": qtext, "options": lt1_p3_mq_options, "correctAnswer": ans})
    lt1_parts.append({"id": "cam19_lt1_p3", "title": "Food Trends Discussion", "audioFile": "cam19_test1_part3.mp3", "subtitle": "", "duration": "", "questions": lt1_p3_qs})

    # Part 4: Ceide Fields (Q31-40)
    lt1_p4_qs = []
    for i, ans in enumerate(["Walls", "Son", "Fuel", "Oxygen", "Rectangular", "Lamps", "Family", "Winter", "Soil", "Rain"], 31):
        lt1_p4_qs.append({"id": f"cam19_lt1_q{i}", "type": "notes_completion", "question": f"Question {i}: ONE WORD ONLY.", "options": [], "correctAnswer": ans})
    lt1_parts.append({"id": "cam19_lt1_p4", "title": "Ceide Fields", "audioFile": "cam19_test1_part4.mp3", "subtitle": "", "duration": "", "questions": lt1_p4_qs})

    tests.append({"id": "cam19_listening_test1", "testNumber": 1, "parts": lt1_parts})

    # ========== LISTENING TEST 2 ==========
    lt2_parts = []

    # Part 1: Guitar Group (Q1-10)
    lt2_p1_qs = []
    for i, (qtext, ans) in enumerate([
        ("1. Surname of contact person: _____", "Mathieson"),
        ("2. Level of ability: _____", "Beginners"),
        ("3. Meeting place: _____", "College"),
        ("4. Address: _____ Street", "New"),
        ("5. Meeting time: _____", "11"),
        ("6. Bring your own: _____", "Instrument"),
        ("7. Music by: _____", "Ear"),
        ("8. Style of music: _____ and folk", "Clapping"),
        ("9. Optional: make a _____", "Recording"),
        ("10. Cost per session: £5 / £3.50 if you come _____", "Alone"),
    ], 1):
        lt2_p1_qs.append({"id": f"cam19_lt2_q{i}", "type": "notes_completion", "question": qtext, "options": [], "correctAnswer": ans})
    lt2_parts.append({"id": "cam19_lt2_p1", "title": "Guitar Group", "audioFile": "cam19_test2_part1.mp3", "subtitle": "", "duration": "", "questions": lt2_p1_qs})

    # Part 2: Working as a Lifeboat Volunteer (Q11-20)
    lt2_p2_qs = []
    for i, ans in enumerate(["A", "B", "A", "B", "C", "A"], 11):
        lt2_p2_qs.append({"id": f"cam19_lt2_q{i}", "type": "multiple_choice", "question": f"Question {i}: Choose the correct letter, A, B or C.", "options": ["A", "B", "C"], "correctAnswer": ans})
    lt2_p2_match_options = [
        "A. working as part of a team",
        "B. experiences when working in winter",
        "C. training exercises built mental strength",
        "D. learning navigation skills",
        "E. wave tank activities provided survival techniques practice",
    ]
    for i, (qtext, ans) in enumerate([
        ("17. what volunteers found most challenging: _____", "C"),
        ("18. what helped volunteers prepare for emergencies: _____", "E"),
        ("19. what volunteers valued most: _____", "A"),
        ("20. what volunteers remember most vividly: _____", "B"),
    ], 17):
        lt2_p2_qs.append({"id": f"cam19_lt2_q{i}", "type": "matching", "question": qtext, "options": lt2_p2_match_options, "correctAnswer": ans})
    lt2_parts.append({"id": "cam19_lt2_p2", "title": "Working as a Lifeboat Volunteer", "audioFile": "cam19_test2_part2.mp3", "subtitle": "", "duration": "", "questions": lt2_p2_qs})

    # Part 3: Recycling Footwear (Q21-30)
    lt2_p3_qs = []
    for i, ans in enumerate(["A", "B", "B", "B"], 21):
        lt2_p3_qs.append({"id": f"cam19_lt2_q{i}", "type": "multiple_choice", "question": f"Question {i}: Choose the correct letter, A, B or C.", "options": ["A", "B", "C"], "correctAnswer": ans})
    lt2_p3_match_options = [
        "A. baby shoes - one missing",
        "B. ankle boots - colour faded",
        "C. trainers - hole",
        "D. sandals - broken strap",
        "E. high-heeled shoes - too dirty",
    ]
    for i, (qtext, ans) in enumerate([
        ("25. Problem type 1: _____", "E"),
        ("26. Problem type 2: _____", "B"),
        ("27. Problem type 3: _____", "A"),
        ("28. Problem type 4: _____", "C"),
    ], 25):
        lt2_p3_qs.append({"id": f"cam19_lt2_q{i}", "type": "matching", "question": qtext, "options": lt2_p3_match_options, "correctAnswer": ans})
    for i, ans in enumerate(["C", "A"], 29):
        lt2_p3_qs.append({"id": f"cam19_lt2_q{i}", "type": "multiple_choice", "question": f"Question {i}: Choose the correct letter, A, B or C.", "options": ["A", "B", "C"], "correctAnswer": ans})
    lt2_parts.append({"id": "cam19_lt2_p3", "title": "Recycling Footwear", "audioFile": "cam19_test2_part3.mp3", "subtitle": "", "duration": "", "questions": lt2_p3_qs})

    # Part 4: Tardigrades (Q31-40)
    lt2_p4_qs = []
    for i, ans in enumerate(["Move", "Short", "Discs", "Oxygen", "Tube", "Temperatures", "Protein", "Space", "Seaweed", "Endangered"], 31):
        lt2_p4_qs.append({"id": f"cam19_lt2_q{i}", "type": "notes_completion", "question": f"Question {i}: ONE WORD ONLY.", "options": [], "correctAnswer": ans})
    lt2_parts.append({"id": "cam19_lt2_p4", "title": "Tardigrades", "audioFile": "cam19_test2_part4.mp3", "subtitle": "", "duration": "", "questions": lt2_p4_qs})

    tests.append({"id": "cam19_listening_test2", "testNumber": 2, "parts": lt2_parts})

    # ========== LISTENING TEST 3 ==========
    lt3_parts = []

    # Part 1: Local Food Shops (Q1-10)
    lt3_p1_qs = []
    for i, (qtext, ans) in enumerate([
        ("1. First shop location: near the _____", "harbour"),
        ("2. Second shop location: opposite the _____", "bridge"),
        ("3. Market opening time: _____", "3.30"),
        ("4. Baker's name: _____", "Rose"),
        ("5. Look for a _____ outside the shop", "sign"),
        ("6. Colour of the building: _____", "purple"),
        ("7. Special product: _____", "samphire"),
        ("8. Fruit: _____", "melon"),
        ("9. Drink: _____", "coconut"),
        ("10. Dessert flavour: _____", "strawberry"),
    ], 1):
        lt3_p1_qs.append({"id": f"cam19_lt3_q{i}", "type": "notes_completion", "question": qtext, "options": [], "correctAnswer": ans})
    lt3_parts.append({"id": "cam19_lt3_p1", "title": "Local Food Shops", "audioFile": "cam19_test3_part1.mp3", "subtitle": "", "duration": "", "questions": lt3_p1_qs})

    # Part 2: Festival Workshops (Q11-20)
    lt3_p2_qs = []
    lt3_p2_match_options = [
        "A. involves learning a craft skill",
        "B. led by prize-winning author",
        "C. Superheroes - aimed at children with disability",
        "D. Just do it - involves drama activity",
        "E. focuses on local history",
        "F. Count on me - aimed at specific age group",
        "G. Speak up - explores an unhappy feeling",
        "H. Sticks and stones - raises awareness of culture",
    ]
    for i, (qtext, ans) in enumerate([
        ("11. Workshop 1: _____", "C"),
        ("12. Workshop 2: _____", "D"),
        ("13. Workshop 3: _____", "F"),
        ("14. Workshop 4: _____", "G"),
        ("15. Workshop 5: _____", "B"),
        ("16. Workshop 6: _____", "H"),
    ], 11):
        lt3_p2_qs.append({"id": f"cam19_lt3_q{i}", "type": "matching", "question": qtext, "options": lt3_p2_match_options, "correctAnswer": ans})
    for i, ans in enumerate(["D", "E", "B", "C"], 17):
        lt3_p2_qs.append({"id": f"cam19_lt3_q{i}", "type": "multiple_choice", "question": f"Question {i}: Choose the correct letter, A, B, C or D.", "options": ["A", "B", "C", "D"], "correctAnswer": ans})
    lt3_parts.append({"id": "cam19_lt3_p2", "title": "Festival Workshops", "audioFile": "cam19_test3_part2.mp3", "subtitle": "", "duration": "", "questions": lt3_p2_qs})

    # Part 3: Science Experiment for Year 12 Students (Q21-30)
    lt3_p3_qs = []
    for i, ans in enumerate(["C", "B", "A", "A", "C"], 21):
        lt3_p3_qs.append({"id": f"cam19_lt3_q{i}", "type": "multiple_choice", "question": f"Question {i}: Choose the correct letter, A, B or C.", "options": ["A", "B", "C"], "correctAnswer": ans})
    lt3_p3_match_options = [
        "A. the equipment needed",
        "B. escape",
        "C. age",
        "D. the timing of the experiment",
        "E. cereal",
        "F. calculations",
        "G. the temperature",
        "H. colour",
    ]
    for i, (qtext, ans) in enumerate([
        ("26. Variable 1: _____", "C"),
        ("27. Variable 2: _____", "H"),
        ("28. Variable 3: _____", "E"),
        ("29. Variable 4: _____", "B"),
        ("30. Factor to control: _____", "F"),
    ], 26):
        lt3_p3_qs.append({"id": f"cam19_lt3_q{i}", "type": "matching", "question": qtext, "options": lt3_p3_match_options, "correctAnswer": ans})
    lt3_parts.append({"id": "cam19_lt3_p3", "title": "Science Experiment for Year 12 Students", "audioFile": "cam19_test3_part3.mp3", "subtitle": "", "duration": "", "questions": lt3_p3_qs})

    # Part 4: Microplastics (Q31-40)
    lt3_p4_qs = []
    for i, ans in enumerate(["clothing", "mouths", "salt", "toothpaste", "fertilisers", "nutrients", "growth", "weight", "acid", "society"], 31):
        lt3_p4_qs.append({"id": f"cam19_lt3_q{i}", "type": "notes_completion", "question": f"Question {i}: ONE WORD ONLY.", "options": [], "correctAnswer": ans})
    lt3_parts.append({"id": "cam19_lt3_p4", "title": "Microplastics", "audioFile": "cam19_test3_part4.mp3", "subtitle": "", "duration": "", "questions": lt3_p4_qs})

    tests.append({"id": "cam19_listening_test3", "testNumber": 3, "parts": lt3_parts})

    # ========== LISTENING TEST 4 ==========
    lt4_parts = []

    # Part 1: First Day at Work (Q1-10)
    lt4_p1_qs = []
    for i, (qtext, ans) in enumerate([
        ("1. Employee name: _____", "Kaeden"),
        ("2. Store room: get _____ from there", "locker"),
        ("3. Must bring: _____", "passport"),
        ("4. Need to order: _____", "uniform"),
        ("5. Which floor staff room is on: _____", "3rd"),
        ("6. Phone number: _____", "0412665903"),
        ("7. Colour of safety area: _____", "yellow"),
        ("8. Material of gloves: _____", "plastic"),
        ("9. Emergency: press button under _____", "ice"),
        ("10. Also need: safety _____", "gloves"),
    ], 1):
        lt4_p1_qs.append({"id": f"cam19_lt4_q{i}", "type": "notes_completion", "question": qtext, "options": [], "correctAnswer": ans})
    lt4_parts.append({"id": "cam19_lt4_p1", "title": "First Day at Work", "audioFile": "cam19_test4_part1.mp3", "subtitle": "", "duration": "", "questions": lt4_p1_qs})

    # Part 2: Compton Park Runners Club (Q11-20)
    lt4_p2_qs = []
    for i, ans in enumerate(["C", "E", "A", "D"], 11):
        lt4_p2_qs.append({"id": f"cam19_lt4_q{i}", "type": "multiple_choice", "question": f"Question {i}: Choose the correct letter, A, B, C or D.", "options": ["A", "B", "C", "D"], "correctAnswer": ans})
    lt4_p2_match_options = [
        "A. lack of confidence",
        "B. dislike of running",
        "C. lack of time",
        "D. difficulty with motivation",
        "E. health concerns",
    ]
    for i, (qtext, ans) in enumerate([
        ("15. Ceri: _____", "A"),
        ("16. James: _____", "B"),
        ("17. Leo: _____", "C"),
        ("18. Mark: _____", "A"),
    ], 15):
        lt4_p2_qs.append({"id": f"cam19_lt4_q{i}", "type": "matching", "question": qtext, "options": lt4_p2_match_options, "correctAnswer": ans})
    for i, ans in enumerate(["C", "B"], 19):
        lt4_p2_qs.append({"id": f"cam19_lt4_q{i}", "type": "multiple_choice", "question": f"Question {i}: Choose the correct letter, A, B or C.", "options": ["A", "B", "C"], "correctAnswer": ans})
    lt4_parts.append({"id": "cam19_lt4_p2", "title": "Compton Park Runners Club", "audioFile": "cam19_test4_part2.mp3", "subtitle": "", "duration": "", "questions": lt4_p2_qs})

    # Part 3: Jane's Grandfather's Bookshop (Q21-30)
    lt4_p3_qs = []
    for i, ans in enumerate(["A", "C", "A", "B", "C"], 21):
        lt4_p3_qs.append({"id": f"cam19_lt4_q{i}", "type": "multiple_choice", "question": f"Question {i}: Choose the correct letter, A, B or C.", "options": ["A", "B", "C"], "correctAnswer": ans})
    lt4_p3_match_options = [
        "A. unwanted books - near the entrance",
        "B. rare books - kept behind the counter",
        "C. requested books - at the back of the shop",
        "D. rare books - on a high shelf",
        "E. second-hand books - in boxes on the floor",
        "F. children's books - specially designed space",
        "G. coursebooks - within the cafe",
    ]
    for i, (qtext, ans) in enumerate([
        ("26. Section 1: _____", "D"),
        ("27. Section 2: _____", "F"),
        ("28. Section 3: _____", "A"),
        ("29. Section 4: _____", "C"),
        ("30. Section 5: _____", "G"),
    ], 26):
        lt4_p3_qs.append({"id": f"cam19_lt4_q{i}", "type": "matching", "question": qtext, "options": lt4_p3_match_options, "correctAnswer": ans})
    lt4_parts.append({"id": "cam19_lt4_p3", "title": "Jane's Grandfather's Bookshop", "audioFile": "cam19_test4_part3.mp3", "subtitle": "", "duration": "", "questions": lt4_p3_qs})

    # Part 4: Tree Planting (Q31-40)
    lt4_p4_qs = []
    for i, ans in enumerate(["competition", "food", "disease", "agriculture", "maps", "cattle", "speed", "monkeys", "fishing", "flooding"], 31):
        lt4_p4_qs.append({"id": f"cam19_lt4_q{i}", "type": "notes_completion", "question": f"Question {i}: ONE WORD ONLY.", "options": [], "correctAnswer": ans})
    lt4_parts.append({"id": "cam19_lt4_p4", "title": "Tree Planting", "audioFile": "cam19_test4_part4.mp3", "subtitle": "", "duration": "", "questions": lt4_p4_qs})

    tests.append({"id": "cam19_listening_test4", "testNumber": 4, "parts": lt4_parts})

    return {"id": "cam19", "title": "Cambridge IELTS 19 Academic Listening", "tests": tests}


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
