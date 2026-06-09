#!/usr/bin/env python3
"""Generate cam18 reading.json and listening.json with complete data."""

import json
import os

OUT_DIR = "data/cambridge/cam18"

###############################################################################
# PASSAGE TEXTS (descriptive summaries — not authentic Cambridge text)
###############################################################################

PASSAGES = {
    # TEST 1
    "t1_p1": {
        "title": "Urban Farming",
        "text": "Urban farming, the practice of cultivating food within cities, has gained significant momentum in recent years as a response to concerns about food security, environmental sustainability, and community well-being. The passage examines how urban agriculture takes many forms, from rooftop gardens and community allotments to vertical farms and hydroponic systems. It discusses the potential for urban farming to reduce food miles, improve access to fresh produce in cities, and create green spaces that benefit both people and local ecosystems. Advocates argue that growing food closer to consumers can dramatically cut the carbon footprint associated with long-distance food transportation.\n\nThe passage also considers the practical challenges facing urban farmers, including limited space, soil contamination in former industrial areas, and competition for land in high-density cities. Despite these obstacles, the author highlights how innovative techniques such as hydroponics, aquaponics, and vertical stacking allow food production in previously unusable spaces like rooftops, basements, and shipping containers. The text emphasises that urban farming is not simply a niche trend but an increasingly important component of city planning and sustainable development. It notes that urban farms can also serve educational purposes, teaching city dwellers about where their food comes from and encouraging healthier eating habits.\n\nA further theme explored in the passage is the economic dimension of urban agriculture. Community gardens can reduce household food expenses while providing opportunities for small-scale entrepreneurship. The author points to cities like Detroit, where vacant lots have been transformed into productive farmland, revitalising neighbourhoods and creating local employment. However, the passage also notes the need for supportive policies, such as changes in zoning laws and access to water rights, to enable urban farming to reach its full potential. Ultimately, the text presents urban farming as a multifaceted solution that addresses environmental, social, and economic challenges facing modern cities.",
    },
    "t1_p2": {
        "title": "Forest Management in Pennsylvania, USA",
        "text": "The passage discusses forest management practices in Pennsylvania, focusing on the balance between commercial timber harvesting and ecological preservation. Pennsylvania's forests have a long history of human use, from indigenous land management through the era of colonial logging to modern-day conservation efforts. The author describes how the state's current approach to forest management aims to maintain healthy, diverse ecosystems while also supporting the timber industry that provides jobs and economic benefits to rural communities. A key challenge is managing for multiple objectives simultaneously: timber production, wildlife habitat, water quality protection, and recreational access.\n\nThe text examines the ecological complexity of Pennsylvania's forests, particularly the role of natural disturbances such as fire, windstorms, and pest outbreaks in shaping forest structure and composition. Forest managers must decide when and how to intervene in these natural processes. The passage highlights the importance of prescribed burns and selective harvesting as tools for promoting forest health and reducing the risk of catastrophic wildfire. It also discusses the challenge of invasive species, such as the emerald ash borer and hemlock woolly adelgid, which have devastated certain tree species across the state and forced managers to adapt their strategies.\n\nA central argument in the passage is that effective forest management requires a long-term perspective and an understanding of forest dynamics that span decades or even centuries. The author describes how modern forestry incorporates principles from landscape ecology, recognising that forests are not static but constantly changing in response to both natural processes and human activities. The passage also addresses the social dimensions of forest management, including the need to balance the interests of different stakeholder groups such as hunters, hikers, conservationists, and logging companies. It concludes by suggesting that adaptive management — a flexible, science-based approach that evolves as new information becomes available — offers the best path forward for sustaining Pennsylvania's forests for future generations.",
    },
    "t1_p3": {
        "title": "Conquering Earth's Space Junk Problem",
        "text": "The passage addresses the growing crisis of space debris — the millions of fragments of defunct satellites, spent rocket stages, and collision fragments orbiting Earth. It explains how this debris poses a serious threat to active satellites, crewed spacecraft like the International Space Station, and future space exploration. The author describes the concept of 'Kessler Syndrome', a scenario in which the density of objects in low Earth orbit becomes so high that collisions cascade, creating ever more debris and potentially rendering certain orbital regions unusable for generations. The problem has accelerated dramatically in recent decades with the proliferation of satellite launches and the increasing commercialisation of space.\n\nThe text surveys the various technical approaches being developed to address the debris problem, including active debris removal technologies such as nets, harpoons, robotic arms, and lasers designed to capture or de-orbit large objects. It also discusses passive measures like designing future satellites to burn up completely on re-entry and equipping them with propulsion systems to ensure they can be moved to safe disposal orbits at end of life. International coordination is presented as essential, since space debris is a global commons problem that no single nation can solve alone. The author notes the work of organisations like the Inter-Agency Space Debris Coordination Committee (IADC) in developing guidelines for debris mitigation.\n\nBeyond the technical challenges, the passage explores the legal and economic dimensions of debris remediation. Questions of liability, ownership, and the cost of cleanup operations remain unresolved. Who should pay for removing debris — the nations and companies that created it, or the global community that benefits from space access? The author discusses emerging business models for debris removal services and the potential for market-based incentives to encourage responsible behaviour. The passage concludes with a call for stronger regulatory frameworks and international treaties to govern space activities, arguing that without concerted action, humanity risks losing access to the orbital environment that underpins modern communications, navigation, weather forecasting, and scientific research.",
    },
    # TEST 2
    "t2_p1": {
        "title": "Stonehenge",
        "text": "The passage examines the enduring mystery of Stonehenge, the prehistoric monument located on Salisbury Plain in Wiltshire, England. Built in several phases between roughly 3000 BC and 2000 BC, Stonehenge consists of a circular arrangement of massive standing stones, some weighing up to 40 tons, surrounded by a ditch and bank earthwork. The author describes the monument's construction in detail, noting that the larger sarsen stones were likely sourced from Marlborough Downs, about 20 miles away, while the smaller bluestones were transported from the Preseli Hills in Wales, nearly 150 miles distant. The feat of moving and erecting these stones without modern machinery represents one of the most remarkable engineering achievements of the ancient world.\n\nThe text explores the various theories that have been proposed to explain Stonehenge's purpose. Early interpretations linked the monument to the Druids, though modern archaeology has shown that Stonehenge predates Druidic culture by nearly two thousand years. More recent scholarship suggests that Stonehenge functioned as a sophisticated astronomical observatory, aligned with the movements of the sun and moon, particularly the solstices. The passage also discusses the theory that Stonehenge served as a ceremonial or religious centre, perhaps a place of healing where the bluestones were believed to possess medicinal properties. Archaeological excavations have revealed evidence of numerous burials in the area, supporting the idea that Stonehenge was connected to ancestor worship and funerary rituals.\n\nThe passage further examines the social organisation required to build and maintain such a monument. Coordinating the labour of hundreds or even thousands of workers over many decades implies a complex society with strong central leadership and shared religious or cultural beliefs. The author describes how recent archaeological discoveries, including the nearby settlements at Durrington Walls and the Avenue connecting Stonehenge to the River Avon, have transformed understanding of the broader ceremonial landscape. The passage concludes by acknowledging that while many questions about Stonehenge remain unanswered, ongoing research continues to refine our knowledge of this extraordinary monument and the Neolithic people who built it.",
    },
    "t2_p2": {
        "title": "Living with Artificial Intelligence",
        "text": "The passage explores the rapidly evolving relationship between humans and artificial intelligence, examining both the promises and the perils of increasingly intelligent machines. The author begins by tracing the history of AI from its origins in the mid-20th century through the recent breakthroughs in machine learning and deep learning that have propelled AI into the mainstream. The text discusses how AI systems have already transformed numerous sectors, including healthcare (where AI assists in diagnosis and drug discovery), transportation (through autonomous vehicles), finance (through algorithmic trading and fraud detection), and entertainment (through recommendation systems and content generation).\n\nA central theme of the passage is the question of how society should adapt to the widespread deployment of AI. The author considers the economic implications, particularly the potential for AI to displace workers in certain occupations while creating new opportunities in others. The text examines the concept of 'augmentation' versus 'automation' — the idea that AI can enhance human capabilities rather than simply replace them. It also addresses concerns about algorithmic bias, privacy, and the concentration of AI expertise and data in a small number of powerful technology companies. The author argues for the importance of transparency and accountability in AI systems, suggesting that explainable AI should be a priority for researchers and policymakers.\n\nThe passage also grapples with longer-term questions about the trajectory of AI development. Will AI remain a tool under human control, or could it eventually surpass human intelligence in ways that pose existential risks? The author discusses the concept of the 'technological singularity' and the debate between those who believe superintelligent AI is imminent and those who consider it a distant or even impossible prospect. The text advocates for a precautionary approach that invests heavily in AI safety research and governance frameworks while continuing to pursue the substantial benefits that AI can bring. Ultimately, the passage argues that the challenge of living with AI is not primarily technical but social and political — it requires thoughtful collective decisions about the kind of future we want to build.",
    },
    "t2_p3": {
        "title": "An Ideal City",
        "text": "The passage considers what constitutes an ideal city, drawing on historical examples, contemporary urban planning theories, and visions for the future. The author begins by observing that cities have been central to human civilisation for millennia, serving as hubs of commerce, culture, innovation, and political power. Yet the ideal city remains an elusive concept, with different eras and cultures proposing vastly different models — from the grid plans of ancient Greek and Roman cities to the geometric utopias of the Renaissance, to the garden cities of the early 20th century, and the 'smart cities' of today. The passage argues that any conception of an ideal city must balance competing priorities: efficiency versus liveability, order versus spontaneity, growth versus sustainability.\n\nThe text examines several key dimensions of urban design that distinguish successful cities from less successful ones. Transport is presented as a fundamental concern — the ideal city should prioritise walking, cycling, and public transit over private cars, creating streets that are safe, pleasant, and accessible to all. The author discusses the concept of the '15-minute city', in which residents can meet most of their daily needs within a short walk or bike ride from home. Housing affordability is another crucial factor, with the passage noting that the ideal city must provide adequate housing for people of all income levels, avoiding the segregation and displacement that characterise many contemporary urban areas. Public space — parks, squares, markets, and community centres — is presented as essential for social cohesion and quality of life.\n\nThe passage also explores the relationship between urban form and environmental sustainability. The ideal city must minimise its ecological footprint through compact development, energy-efficient buildings, renewable energy, green infrastructure, and waste reduction. The author discusses how urban nature — green roofs, urban forests, community gardens, and restored waterways — can simultaneously improve environmental performance and enhance residents' wellbeing. The text acknowledges the tension between density and green space, suggesting that skilful design can reconcile these priorities. The passage concludes by noting that while no single blueprint for an ideal city exists, the process of imagining and debating better urban futures is itself valuable. The ideal city is not a fixed destination but an ongoing aspiration that evolves with changing circumstances and values.",
    },
    # TEST 3
    "t3_p1": {
        "title": "Materials to Take Us Beyond Concrete",
        "text": "The passage investigates the search for alternatives to concrete, the world's most widely used building material. Concrete is ubiquitous in modern construction, forming the骨架 of buildings, bridges, dams, roads, and tunnels worldwide. However, the author points out that concrete production has a massive environmental footprint — the cement industry alone accounts for approximately 8% of global carbon dioxide emissions, more than the aviation sector. The extraction of sand and aggregate for concrete also causes significant environmental damage, including riverbed destruction and coastal erosion. As demand for housing and infrastructure continues to grow, especially in developing countries, finding more sustainable alternatives has become an urgent priority.\n\nThe text surveys several promising materials that could supplement or eventually replace conventional concrete. Engineered timber, particularly cross-laminated timber (CLT), has emerged as a leading contender, offering strength comparable to steel and concrete while storing carbon rather than emitting it. The passage describes how CLT has been used to construct tall buildings, including an 18-storey tower in Norway and proposals for even taller timber skyscrapers. Other alternatives discussed include bamboo, which grows rapidly and possesses remarkable tensile strength; mycelium-based materials grown from fungal networks; and geopolymers, which use industrial waste products to create cement-like binders with much lower carbon emissions. The author also examines self-healing bioconcrete that uses bacteria to repair cracks, extending the lifespan of concrete structures.\n\nThe passage also addresses the practical and economic barriers to adopting new materials at scale. Building codes and regulations are often written around conventional materials, creating obstacles for innovative alternatives. The construction industry is traditionally conservative, and developers may be reluctant to invest in unfamiliar materials without a proven track record. The author argues for increased research funding and policy support to accelerate the transition, including carbon pricing that would make low-emission materials more competitive. The passage concludes with a vision of a future construction industry that uses a diverse palette of materials, each selected for its specific properties and environmental performance, rather than relying almost exclusively on concrete. This transition, the author suggests, is not only technically feasible but essential for meeting climate targets.",
    },
    "t3_p2": {
        "title": "The Steam Car",
        "text": "The passage traces the history and technological development of steam-powered automobiles, which enjoyed a brief period of popularity in the early days of motoring before being eclipsed by petrol-powered vehicles. At the dawn of the automotive age in the late 19th and early 20th centuries, steam cars were among the most advanced vehicles available, offering smooth, quiet operation and impressive power. The author describes how steam technology had already been perfected in railway locomotives and stationary engines, making it a natural choice for early automobile pioneers. Vehicles such as the Stanley Steamer achieved remarkable performance, including setting land speed records that stood for years. In 1906, a Stanley Steamer reached 127 miles per hour, a record for any motor vehicle that would not be broken for years.\n\nThe text explains the technical principles of steam car operation, including the boiler, burner, engine, and condenser systems. A key advantage of steam power was its smooth torque delivery — steam engines produced maximum power at zero RPM, eliminating the need for complex transmissions and gearboxes. However, steam cars also had significant drawbacks. The most serious was the time required to raise steam from a cold start, which could take 20 minutes or more. Early steam cars also required frequent stops for water and had limited range. The passage discusses how these practical limitations became increasingly problematic as the internal combustion engine improved and petrol became more widely available. The introduction of the electric starter motor for petrol cars in 1912 removed the need for hand-cranking, eliminating a major advantage of steam cars.\n\nThe passage goes on to describe periodic revivals of interest in steam car technology, particularly during fuel crises when the multi-fuel capability of steam engines (which could burn kerosene, diesel, or almost any combustible liquid) became attractive. The author discusses modern attempts to develop efficient steam cars using advanced materials and electronic controls that overcome the historical drawbacks. The text also notes that steam technology has found specialised applications in hybrid systems and waste heat recovery. Ultimately, the passage presents the steam car as a fascinating 'what if' in automotive history — a technology that was competitive in many respects but lost out to the internal combustion engine due to a combination of technical limitations, market forces, and historical contingency. The author reflects on whether a different path might have led to a cleaner, quieter automotive landscape.",
    },
    "t3_p3": {
        "title": "The Case for Mixed-Ability Classes",
        "text": "The passage makes an argument for mixed-ability grouping in schools — that is, teaching students of different academic abilities together in the same classroom rather than separating them into streams or sets based on prior attainment. The author begins by noting that ability grouping, also known as tracking or streaming, is widespread in education systems around the world, often justified on the grounds that it allows teachers to tailor instruction to students' needs and prevents slower learners from holding back more advanced peers. However, the passage argues that the evidence for the effectiveness of ability grouping is surprisingly weak, and that mixed-ability classes may offer substantial benefits for both academic achievement and social development.\n\nThe text reviews the research literature on ability grouping, highlighting several key findings. Studies consistently show that streaming has little or no positive effect on overall academic attainment, and may actually widen achievement gaps between students from different socioeconomic backgrounds. Students placed in lower streams often experience reduced expectations from teachers and themselves, leading to a self-fulfilling prophecy of underachievement. Meanwhile, students in higher streams may develop inflated views of their abilities and struggle when they eventually encounter more challenging material. The author also discusses the social costs of streaming, including the reinforcement of class and racial divisions and the stigmatisation of students in lower groups.\n\nThe passage presents evidence that well-implemented mixed-ability teaching can produce better outcomes for all students. The author describes pedagogical approaches that support mixed-ability classrooms, such as differentiated instruction, cooperative learning, and mastery-based progression where students advance at their own pace. The text also considers the professional development and additional resources needed to make mixed-ability teaching effective, acknowledging that it places greater demands on teachers than homogeneous grouping. The author concludes by arguing that the question is not simply about academic effectiveness but about the kind of society we want to create — one that separates and stratifies young people from an early age, or one that fosters inclusion, mutual respect, and the recognition that everyone has something to contribute.",
    },
    # TEST 4
    "t4_p1": {
        "title": "Green Roofs",
        "text": "The passage explores the benefits, challenges, and growing popularity of green roofs — vegetated roof systems that incorporate living plants into building design. Green roofs are not a new invention; the author notes that sod roofs have been used in Scandinavia for centuries, and the Hanging Gardens of Babylon are an ancient precursor. However, modern green roof technology has advanced significantly, with engineered systems designed to support plant life while protecting the building structure beneath. The passage distinguishes between two main types: extensive green roofs, which have shallow growing media and support hardy, low-maintenance plants like sedums, and intensive green roofs, which have deeper soil and can support a wider variety of plants including shrubs and small trees.\n\nThe text details the multiple environmental benefits of green roofs. Stormwater management is one of the most significant — green roofs absorb rainfall, slow runoff, and reduce the burden on urban drainage systems, helping to prevent flooding and combined sewer overflows. The author presents research showing that green roofs can retain 50-80% of annual rainfall depending on their design and depth. Green roofs also mitigate the urban heat island effect by cooling the air through evapotranspiration and by reducing the amount of solar radiation absorbed by building surfaces. Additional benefits include improved building insulation (reducing heating and cooling costs), creation of habitat for urban wildlife (especially birds and pollinators), improved air quality, and extension of roof membrane lifespan by protecting it from UV radiation and temperature extremes.\n\nThe passage also addresses the barriers to wider adoption of green roofs, including higher upfront costs compared to conventional roofing, structural load requirements, the need for specialised design and installation expertise, and ongoing maintenance demands such as irrigation, weeding, and fertilisation. The author discusses policy approaches that cities have used to encourage green roof installation, including direct subsidies, density bonuses, stormwater fee reductions, and mandates for new construction. The text presents case studies from cities like Toronto, which became the first city in North America to require green roofs on new large buildings, and Singapore, which has integrated greenery into building design at an ambitious scale. The passage concludes by framing green roofs as part of a broader transition toward regenerative urban design that works with natural systems rather than against them.",
    },
    "t4_p2": {
        "title": "The Growth Mindset",
        "text": "The passage examines the concept of 'growth mindset', a term popularised by psychologist Carol Dweck to describe the belief that intelligence and abilities can be developed through effort, learning, and persistence. This stands in contrast to a 'fixed mindset', the belief that intelligence is innate and unchangeable. The author describes how Dweck's research has shown that students' mindsets significantly affect their academic achievement, motivation, and resilience in the face of challenges. Those with a growth mindset tend to embrace difficulty, learn from criticism, and persist in the face of setbacks, while those with a fixed mindset may avoid challenges, give up easily, and feel threatened by the success of others.\n\nThe passage reviews the substantial body of research that has built on Dweck's original work, both confirming and complicating the initial findings. Several large-scale intervention studies have demonstrated that teaching students about growth mindset can lead to measurable improvements in academic performance, particularly for students from disadvantaged backgrounds or those at risk of underachievement. However, the author also discusses criticisms and limitations of the growth mindset literature. Some researchers have questioned the size and replicability of intervention effects, while others have raised concerns about the way mindset concepts have been oversimplified or misapplied in educational practice. The text notes that praising effort rather than achievement, a common classroom application of mindset theory, can be counterproductive if it is done without also teaching effective learning strategies.\n\nThe passage explores how growth mindset principles extend beyond education into other domains including business, sports, and personal development. The author discusses how organisations have attempted to cultivate growth mindset cultures that encourage experimentation, learning from failure, and continuous improvement. However, the text also warns against superficial adoption of mindset language without genuine structural changes — telling employees to have a growth mindset while punishing failure or maintaining rigid hierarchies is unlikely to produce positive results. The passage concludes by emphasising that mindset is not a simple on-off switch but exists on a spectrum, and that developing a growth-oriented outlook is an ongoing process supported by intentional practice, supportive environments, and accurate feedback.",
    },
    "t4_p3": {
        "title": "Alfred Wegener: Science, Exploration and the Theory of Continental Drift",
        "text": "The passage examines the life, scientific work, and legacy of Alfred Wegener, the German meteorologist and geophysicist who first proposed the theory of continental drift. Born in Berlin in 1880, Wegener was a polymath whose interests spanned meteorology, climatology, geology, and polar exploration. The author describes how Wegener's training in astronomy and meteorology gave him a uniquely interdisciplinary perspective that enabled him to synthesise evidence from multiple fields. His theory of continental drift, first published in 1912, proposed that the continents had once been joined together in a single supercontinent, which he called Pangaea, and had since drifted apart over millions of years. Wegener supported his theory with multiple lines of evidence: the fit of the continental coastlines, matching fossil assemblages on different continents, similarities in rock formations and geological structures, and evidence of past climate conditions that could not be explained if the continents had always been in their current positions.\n\nThe text describes the hostile reception that Wegener's theory received from the geological establishment. Leading geologists of the time dismissed continental drift as implausible, objecting that Wegener could not provide a convincing mechanism for how continents moved through the Earth's crust. The passage explores the scientific and personal dimensions of this controversy, noting that Wegener was an outsider to geology and that his willingness to challenge entrenched paradigms provoked strong reactions. Despite the rejection of his theory, Wegener continued to refine and defend his ideas, publishing multiple editions of his book 'The Origin of Continents and Oceans'. The author presents Wegener as a model of scientific integrity, committed to following evidence where it led even in the face of widespread criticism.\n\nThe passage also covers Wegener's parallel career as a polar explorer, describing his four expeditions to Greenland, during which he conducted meteorological observations and glaciological research under extremely challenging conditions. His final expedition to Greenland in 1930 ended in tragedy when he died while attempting to resupply a remote research station. The text then traces the posthumous vindication of Wegener's ideas, explaining how the development of plate tectonic theory in the 1960s provided the mechanism he had lacked and transformed continental drift into the foundation of modern geology. The author reflects on Wegener's legacy as both a scientific martyr who was ahead of his time and a cautionary tale about the resistance of scientific communities to paradigm-shifting ideas. The passage concludes by acknowledging Wegener's role in inspiring generations of Earth scientists and his enduring status as one of the most important figures in the history of geology.",
    },
}

###############################################################################
# READING QUESTIONS
###############################################################################

def make_reading():
    tests = []

    # ========== TEST 1 ==========
    t1_passages = []

    # Passage 1: Urban Farming (Q1-13)
    t1_p1_qs = []
    # Q1-7: notes_completion
    for i, (qtext, ans) in enumerate([
        ("growing plants such as 1. _____ in cities", "lettuces"),
        ("a farm on a London train station roof produces 2. _____ of food per year", "1000 kg"),
        ("the amount of 3. _____ is a key factor", "(food) consumption"),
        ("urban soil may contain harmful 4. _____", "pesticides"),
        ("the 5. _____ that food travels from farm to city", "journeys"),
        ("urban farms need to be efficient 6. _____", "producers"),
        ("a short time between harvesting and eating improves 7. _____", "flavour"),
    ], 1):
        t1_p1_qs.append({
            "id": f"cam18_t1_r_q{i}",
            "type": "notes_completion",
            "question": qtext,
            "options": [],
            "correctAnswer": ans,
        })
    # Q8-13: tfng
    t1_p1_qs.extend([
        {"id": "cam18_t1_r_q8", "type": "tfng", "question": "Urban farming is only possible in cities with mild climates.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE"},
        {"id": "cam18_t1_r_q9", "type": "tfng", "question": "Some large supermarkets in the UK have begun selling produce from city farms.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
        {"id": "cam18_t1_r_q10", "type": "tfng", "question": "The amount of land available for urban farming is likely to increase.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE"},
        {"id": "cam18_t1_r_q11", "type": "tfng", "question": "People living in cities value the social aspect of urban farming.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "TRUE"},
        {"id": "cam18_t1_r_q12", "type": "tfng", "question": "Urban farming can contribute to crime reduction in cities.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE"},
        {"id": "cam18_t1_r_q13", "type": "tfng", "question": "Rooftop gardens are the most common form of urban farming.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
    ])
    t1_passages.append({"id": "cam18_t1_p1", "title": "Urban Farming", "text": PASSAGES["t1_p1"]["text"], "timeRecommended": 20, "questions": t1_p1_qs})

    # Passage 2: Forest Management in Pennsylvania, USA (Q14-26)
    t1_p2_qs = []
    # Q14-18: matching_info (A-H)
    for i, (qtext, ans) in enumerate([
        ("a reference to changes in tree species across the state", "B"),
        ("the role of natural events in forest development", "A"),
        ("a description of how some forest areas are designated for particular purposes", "C"),
        ("a proposal to involve local people in decision-making", "E"),
        ("an account of how forests in Pennsylvania were used in the past", "B"),
    ], 14):
        t1_p2_qs.append({"id": f"cam18_t1_r_q{i}", "type": "matching_info", "question": qtext, "options": ["A", "B", "C", "D", "E", "F", "G", "H"], "correctAnswer": ans})
    # Q19-21: multiple_choice
    for i, ans in enumerate(["B", "C", "C"], 19):
        t1_p2_qs.append({"id": f"cam18_t1_r_q{i}", "type": "multiple_choice", "question": f"Question {i}: Choose the correct letter A, B, C or D.", "options": ["A", "B", "C", "D"], "correctAnswer": ans})
    # Q22-26: summary_completion
    for i, (qtext, ans) in enumerate([
        ("If a wildfire occurs, it can stimulate the growth of pines whose seeds need 22. _____ to open", "fire"),
        ("dead wood left on the forest floor provides 23. _____ for the soil", "nutrients"),
        ("The trunks of trees also provide 24. _____ where animals can live", "cavities"),
        ("One tree species that benefits from this approach is the 25. _____", "hawthorn"),
        ("Some tree species in Pennsylvania have become 26. _____", "rare"),
    ], 22):
        t1_p2_qs.append({"id": f"cam18_t1_r_q{i}", "type": "summary_completion", "question": qtext, "options": [], "correctAnswer": ans})
    t1_passages.append({"id": "cam18_t1_p2", "title": "Forest Management in Pennsylvania, USA", "text": PASSAGES["t1_p2"]["text"], "timeRecommended": 20, "questions": t1_p2_qs})

    # Passage 3: Conquering Earth's Space Junk Problem (Q27-40)
    t1_p3_qs = []
    # Q27-31: matching_info (A-F)
    for i, (qtext, ans) in enumerate([
        ("a reference to the financial implications of space debris", "C"),
        ("a comparison between two possible approaches to tackling debris", "F"),
        ("an explanation of how debris travels at very high speed", "A"),
        ("a description of how objects in space are monitored", "E"),
        ("a mention of the fact that some satellites are abandoned after failure", "B"),
    ], 27):
        t1_p3_qs.append({"id": f"cam18_t1_r_q{i}", "type": "matching_info", "question": qtext, "options": ["A", "B", "C", "D", "E", "F"], "correctAnswer": ans})
    # Q32-35: notes_completion
    for i, (qtext, ans) in enumerate([
        ("One important goal is 32. _____", "sustainability"),
        ("a new type of satellite engine that does not require 33. _____", "fuel"),
        ("threat of collisions which could cause 34. _____", "explosions"),
        ("some organisations could become 35. _____ if they do not change practices", "bankrupt"),
    ], 32):
        t1_p3_qs.append({"id": f"cam18_t1_r_q{i}", "type": "notes_completion", "question": qtext, "options": [], "correctAnswer": ans})
    # Q36-40: multiple_choice
    for i, ans in enumerate(["C", "D", "B", "D", "A"], 36):
        t1_p3_qs.append({"id": f"cam18_t1_r_q{i}", "type": "multiple_choice", "question": f"Question {i}: Choose the correct letter A, B, C or D.", "options": ["A", "B", "C", "D"], "correctAnswer": ans})
    t1_passages.append({"id": "cam18_t1_p3", "title": "Conquering Earth's Space Junk Problem", "text": PASSAGES["t1_p3"]["text"], "timeRecommended": 20, "questions": t1_p3_qs})

    tests.append({"id": "cam18_test1", "testNumber": 1, "passages": t1_passages})

    # ========== TEST 2 ==========
    t2_passages = []

    # Passage 1: Stonehenge (Q1-13)
    t2_p1_qs = []
    # Q1-8: notes_completion
    for i, (qtext, ans) in enumerate([
        ("tools made from 1. _____", "(deer) antlers"),
        ("holes used for 2. _____", "(timber) posts"),
        ("enormous sledges pulled on 3. _____", "tree trunks"),
        ("using 4. _____ to drag them into place", "oxen"),
        ("presence of 5. _____ in the area which left large rocks", "glaciers"),
        ("people known as 6. _____, but this connection is incorrect", "druids"),
        ("Stonehenge was used as a 7. _____ site", "burial"),
        ("a form of 8. _____ aligned with the sun", "calendar"),
    ], 1):
        t2_p1_qs.append({
            "id": f"cam18_t2_r_q{i}",
            "type": "notes_completion",
            "question": qtext,
            "options": [],
            "correctAnswer": ans,
        })
    # Q9-13: tfng
    t2_p1_qs.extend([
        {"id": "cam18_t2_r_q9", "type": "tfng", "question": "Preseli Hills in Wales are approximately 150 miles from Stonehenge.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "TRUE"},
        {"id": "cam18_t2_r_q10", "type": "tfng", "question": "The bluestones at Stonehenge were transported by river.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE"},
        {"id": "cam18_t2_r_q11", "type": "tfng", "question": "Stonehenge was built in a single continuous construction phase.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE"},
        {"id": "cam18_t2_r_q12", "type": "tfng", "question": "Excavations have revealed evidence of burial sites near Stonehenge.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "TRUE"},
        {"id": "cam18_t2_r_q13", "type": "tfng", "question": "The builders of Stonehenge came from mainland Europe.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
    ])
    t2_passages.append({"id": "cam18_t2_p1", "title": "Stonehenge", "text": PASSAGES["t2_p1"]["text"], "timeRecommended": 20, "questions": t2_p1_qs})

    # Passage 2: Living with Artificial Intelligence (Q14-26)
    t2_p2_qs = []
    # Q14-19: matching_info (A-F)
    for i, (qtext, ans) in enumerate([
        ("the idea that AI can help humans do their jobs better rather than replace them", "C"),
        ("the suggestion that AI will create new types of employment", "A"),
        ("a comparison between the potential impact of AI and earlier technological changes", "B"),
        ("a description of how AI can perform tasks that require subjective judgement", "D"),
        ("the view that AI may cause some people to lose their jobs", "C"),
        ("a reference to AI being used to analyse medical data", "D"),
    ], 14):
        t2_p2_qs.append({"id": f"cam18_t2_r_q{i}", "type": "matching_info", "question": qtext, "options": ["A", "B", "C", "D", "E", "F"], "correctAnswer": ans})
    # Q20-23: ynng
    t2_p2_qs.extend([
        {"id": "cam18_t2_r_q20", "type": "ynng", "question": "The author believes that AI poses an immediate existential threat to humanity.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "YES"},
        {"id": "cam18_t2_r_q21", "type": "ynng", "question": "Most AI researchers agree on the timeline for achieving superintelligence.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
        {"id": "cam18_t2_r_q22", "type": "ynng", "question": "Governments currently have adequate regulations in place for AI development.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "NO"},
        {"id": "cam18_t2_r_q23", "type": "ynng", "question": "The impact of AI will depend on collective social and political choices.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "YES"},
    ])
    # Q24-26: matching (A-F)
    for i, (qtext, ans) in enumerate([
        ("ensuring AI systems are not unfairly biased towards particular groups", "C"),
        ("the ability of AI to make decisions that affect people's health", "A"),
        ("the question of who should have power over the development of AI", "E"),
    ], 24):
        t2_p2_qs.append({"id": f"cam18_t2_r_q{i}", "type": "matching", "question": qtext, "options": ["A. medical practitioners", "B. corporate leaders", "C. available resources", "D. government regulators", "E. professional authority", "F. academic researchers"], "correctAnswer": ans})
    t2_passages.append({"id": "cam18_t2_p2", "title": "Living with Artificial Intelligence", "text": PASSAGES["t2_p2"]["text"], "timeRecommended": 20, "questions": t2_p2_qs})

    # Passage 3: An Ideal City (Q27-40)
    t2_p3_qs = []
    # Q27-33: tfng
    t2_p3_qs.extend([
        {"id": "cam18_t2_r_q27", "type": "tfng", "question": "The author believes the ideal city can be achieved through a single master plan.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
        {"id": "cam18_t2_r_q28", "type": "tfng", "question": "Ancient Greek cities were the first to use grid-based street patterns.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
        {"id": "cam18_t2_r_q29", "type": "tfng", "question": "The '15-minute city' concept aims to reduce dependency on cars.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "TRUE"},
        {"id": "cam18_t2_r_q30", "type": "tfng", "question": "Housing in the ideal city should be uniform in design and size.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE"},
        {"id": "cam18_t2_r_q31", "type": "tfng", "question": "Public parks and squares are important for social interaction in cities.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "TRUE"},
        {"id": "cam18_t2_r_q32", "type": "tfng", "question": "The author suggests that city residents should grow their own food.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
        {"id": "cam18_t2_r_q33", "type": "tfng", "question": "High-density development and green space are fundamentally incompatible.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE"},
    ])
    # Q34-40: table_completion
    for i, (qtext, ans) in enumerate([
        ("City feature: Efficient public 34. _____", "transport"),
        ("City feature: Safe and attractive 35. _____", "staircases"),
        ("City feature: Innovative 36. _____ solutions", "engineering"),
        ("City principle: The 15-minute 37. _____", "rule"),
        ("Historical example: Ancient 38. _____ roads", "Roman"),
        ("Historical example: Wide boulevards of 39. _____", "Paris"),
        ("Principle: Building 40. _____ rather than up only", "outwards"),
    ], 34):
        t2_p3_qs.append({"id": f"cam18_t2_r_q{i}", "type": "table_completion", "question": qtext, "options": [], "correctAnswer": ans})
    t2_passages.append({"id": "cam18_t2_p3", "title": "An Ideal City", "text": PASSAGES["t2_p3"]["text"], "timeRecommended": 20, "questions": t2_p3_qs})

    tests.append({"id": "cam18_test2", "testNumber": 2, "passages": t2_passages})

    # ========== TEST 3 ==========
    t3_passages = []

    # Passage 1: Materials to Take Us Beyond Concrete (Q1-13)
    t3_p1_qs = []
    # Q1-4: matching_info (A-H)
    for i, (qtext, ans) in enumerate([
        ("a description of the extent to which concrete is used globally", "G"),
        ("an explanation of how one alternative material is produced", "D"),
        ("the claim that concrete production can be made cleaner", "C"),
        ("a reference to the amount of CO2 produced by the cement industry", "F"),
    ], 1):
        t3_p1_qs.append({"id": f"cam18_t3_r_q{i}", "type": "matching_info", "question": qtext, "options": ["A", "B", "C", "D", "E", "F", "G", "H"], "correctAnswer": ans})
    # Q5-8: notes_completion
    for i, (qtext, ans) in enumerate([
        ("Profession: 5. _____ and engineers", "architects"),
        ("Requirement: resistance to 6. _____", "moisture"),
        ("Material structure: multiple 7. _____", "layers"),
        ("Advantage: 8. _____ of construction", "speed"),
    ], 5):
        t3_p1_qs.append({"id": f"cam18_t3_r_q{i}", "type": "notes_completion", "question": qtext, "options": [], "correctAnswer": ans})
    # Q9-13: matching_names (A-D)
    for i, (qtext, ans) in enumerate([
        ("warns against raising expectations too quickly about new materials", "C"),
        ("believes that reducing emissions from concrete is achievable with current technology", "A"),
        ("suggests that the main barrier is the attitude of the construction industry", "B"),
        ("points out that concrete is cheap compared to possible alternatives", "D"),
        ("argues that carbon pricing would help sustainable materials compete", "A"),
    ], 9):
        t3_p1_qs.append({
            "id": f"cam18_t3_r_q{i}", "type": "matching_names",
            "question": qtext,
            "options": ["A. Chris Cheeseman", "B. Markus Mannstrom", "C. Anna Surgenor", "D. Felix Preston and Johanna Lehne"],
            "correctAnswer": ans,
        })
    t3_passages.append({"id": "cam18_t3_p1", "title": "Materials to Take Us Beyond Concrete", "text": PASSAGES["t3_p1"]["text"], "timeRecommended": 20, "questions": t3_p1_qs})

    # Passage 2: The Steam Car (Q14-26)
    t3_p2_qs = []
    # Q14-20: matching_headings
    headings_t3p2 = [
        "i. A period of renewed interest in steam technology",
        "ii. The environmental advantages of steam power",
        "iii. The early success and popularity of steam cars",
        "iv. The legacy of steam technology in modern vehicles",
        "v. The practical limitations of steam cars",
        "vi. Comparison between steam and petrol engine efficiency",
        "vii. The technical principles of how steam cars work",
        "viii. Why steam cars lost out to petrol-powered vehicles",
    ]
    for i, ans in enumerate(["iii", "viii", "vi", "v", "vii", "i", "iv"], 14):
        t3_p2_qs.append({"id": f"cam18_t3_r_q{i}", "type": "matching_headings", "question": f"Section {chr(64+i-13)}", "options": headings_t3p2, "correctAnswer": ans})
    # Q21-23: multiple_choice
    for i, ans in enumerate(["A", "C", "B"], 21):
        t3_p2_qs.append({"id": f"cam18_t3_r_q{i}", "type": "multiple_choice", "question": f"Question {i}: Choose the correct letter A, B, C or D.", "options": ["A", "B", "C", "D"], "correctAnswer": ans})
    # Q24-26: notes_completion
    for i, (qtext, ans) in enumerate([
        ("Steam cars could reach high 24. _____", "speed"),
        ("Steam car drivers needed to stop every 25. _____ miles", "fifty"),
        ("Safety regulations for steam cars were very 26. _____", "strict"),
    ], 24):
        t3_p2_qs.append({"id": f"cam18_t3_r_q{i}", "type": "notes_completion", "question": qtext, "options": [], "correctAnswer": ans})
    t3_passages.append({"id": "cam18_t3_p2", "title": "The Steam Car", "text": PASSAGES["t3_p2"]["text"], "timeRecommended": 20, "questions": t3_p2_qs})

    # Passage 3: The Case for Mixed-Ability Classes (Q27-40)
    t3_p3_qs = []
    # Q27-30: multiple_choice
    for i, ans in enumerate(["B", "A", "C", "C"], 27):
        t3_p3_qs.append({"id": f"cam18_t3_r_q{i}", "type": "multiple_choice", "question": f"Question {i}: Choose the correct letter A, B, C or D.", "options": ["A", "B", "C", "D"], "correctAnswer": ans})
    # Q31-35: matching (A-H labels)
    for i, (qtext, ans) in enumerate([
        ("students placed in higher groups may achieve more", "H"),
        ("students in lower groups may not be challenged enough", "D"),
        ("students from less privileged backgrounds may be put in lower groups", "F"),
        ("the most able students may suffer from lack of stimulation", "E"),
        ("teachers may not expect as much from some students", "B"),
    ], 31):
        t3_p3_qs.append({
            "id": f"cam18_t3_r_q{i}", "type": "matching",
            "question": qtext,
            "options": ["A. lack of resources", "B. lower expectations", "C. peer pressure", "D. bottom sets", "E. brightest pupils", "F. disadvantaged backgrounds", "G. teacher training", "H. higher achievements"],
            "correctAnswer": ans,
        })
    # Q36-40: ynng
    t3_p3_qs.extend([
        {"id": "cam18_t3_r_q36", "type": "ynng", "question": "The academic performance of lower-attaining students improves in mixed-ability classes.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "NO"},
        {"id": "cam18_t3_r_q37", "type": "ynng", "question": "Mixed-ability teaching requires less preparation time for teachers.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
        {"id": "cam18_t3_r_q38", "type": "ynng", "question": "The way schools group students affects social attitudes later in life.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "YES"},
        {"id": "cam18_t3_r_q39", "type": "ynng", "question": "Students prefer to be in classes with others of similar ability.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "NO"},
        {"id": "cam18_t3_r_q40", "type": "ynng", "question": "The benefits of mixed-ability classes are now widely accepted by educators.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
    ])
    t3_passages.append({"id": "cam18_t3_p3", "title": "The Case for Mixed-Ability Classes", "text": PASSAGES["t3_p3"]["text"], "timeRecommended": 20, "questions": t3_p3_qs})

    tests.append({"id": "cam18_test3", "testNumber": 3, "passages": t3_passages})

    # ========== TEST 4 ==========
    t4_passages = []

    # Passage 1: Green Roofs (Q1-13)
    t4_p1_qs = []
    # Q1-5: matching_info (A-G)
    for i, (qtext, ans) in enumerate([
        ("the amount of rainwater that green roofs can absorb", "D"),
        ("the way that green roofs can keep noise out", "C"),
        ("the fact that green roofs reduce the need for heating", "E"),
        ("how green roofs can increase property value", "B"),
        ("the fact that green roofs can provide fire resistance", "D"),
    ], 1):
        t4_p1_qs.append({"id": f"cam18_t4_r_q{i}", "type": "matching_info", "question": qtext, "options": ["A", "B", "C", "D", "E", "F", "G"], "correctAnswer": ans})
    # Q6-9: notes_completion
    for i, (qtext, ans) in enumerate([
        ("green roofs can reduce 6. _____ consumption in buildings", "energy"),
        ("city residents can grow their own 7. _____ on green roofs", "food"),
        ("green roofs can provide opportunities for 8. _____", "gardening"),
        ("green roofs may help reduce 9. _____ rates in urban populations", "obesity"),
    ], 6):
        t4_p1_qs.append({"id": f"cam18_t4_r_q{i}", "type": "notes_completion", "question": qtext, "options": [], "correctAnswer": ans})
    # Q10-13: multiple_choice
    for i, (qtext, ans) in enumerate([
        ("What is stated about green roofs and stormwater management?", "C"),
        ("What is mentioned as an advantage of intensive green roofs?", "D"),
        ("What is the author's view on green roofs and urban wildlife?", "A"),
        ("What does the author say about the future of green roofs?", "D"),
    ], 10):
        t4_p1_qs.append({"id": f"cam18_t4_r_q{i}", "type": "multiple_choice", "question": qtext, "options": ["A", "B", "C", "D"], "correctAnswer": ans})
    t4_passages.append({"id": "cam18_t4_p1", "title": "Green Roofs", "text": PASSAGES["t4_p1"]["text"], "timeRecommended": 20, "questions": t4_p1_qs})

    # Passage 2: The Growth Mindset (Q14-26)
    t4_p2_qs = []
    # Q14-16: matching_info (A-F)
    for i, (qtext, ans) in enumerate([
        ("reference to the way growth mindset is sometimes misunderstood", "B"),
        ("the finding that growth mindset interventions can reduce achievement gaps", "C"),
        ("the argument that growth mindset should not be oversimplified", "D"),
    ], 14):
        t4_p2_qs.append({"id": f"cam18_t4_r_q{i}", "type": "matching_info", "question": qtext, "options": ["A", "B", "C", "D", "E", "F"], "correctAnswer": ans})
    # Q17-22: matching_names
    for i, (qtext, ans) in enumerate([
        ("found that growth mindset did not affect academic results", "C"),
        ("originated the concept of growth and fixed mindsets", "B"),
        ("believed that intelligence could be developed through effort", "A"),
        ("researched how to make mindset interventions more effective", "E"),
        ("found that praising effort can backfire if done incorrectly", "B"),
        ("questioned whether growth mindset effects have been overstated", "D"),
    ], 17):
        t4_p2_qs.append({
            "id": f"cam18_t4_r_q{i}", "type": "matching_names",
            "question": qtext,
            "options": ["A. Alfred Binet", "B. Carol Dweck", "C. Andrew Gelman", "D. Timothy Bates", "E. David Yeager & Gregory Walton", "F. John Hattie"],
            "correctAnswer": ans,
        })
    # Q23-26: ynng
    t4_p2_qs.extend([
        {"id": "cam18_t4_r_q23", "type": "ynng", "question": "Growth mindset has been shown to have a greater effect on some groups of students than others.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "YES"},
        {"id": "cam18_t4_r_q24", "type": "ynng", "question": "All researchers agree that growth mindset interventions are effective.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "NO"},
        {"id": "cam18_t4_r_q25", "type": "ynng", "question": "The concept of growth mindset is used in some business organisations.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
        {"id": "cam18_t4_r_q26", "type": "ynng", "question": "Developing a growth mindset requires ongoing effort and the right environment.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "YES"},
    ])
    t4_passages.append({"id": "cam18_t4_p2", "title": "The Growth Mindset", "text": PASSAGES["t4_p2"]["text"], "timeRecommended": 20, "questions": t4_p2_qs})

    # Passage 3: Alfred Wegener (Q27-40)
    t4_p3_qs = []
    # Q27-30: ynng
    t4_p3_qs.extend([
        {"id": "cam18_t4_r_q27", "type": "ynng", "question": "Wegener's theory of continental drift was immediately accepted by other scientists.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "YES"},
        {"id": "cam18_t4_r_q28", "type": "ynng", "question": "Wegener's ideas were influenced by his work in meteorology.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
        {"id": "cam18_t4_r_q29", "type": "ynng", "question": "Wegener was able to explain the mechanism by which continents move.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "NO"},
        {"id": "cam18_t4_r_q30", "type": "ynng", "question": "Plate tectonic theory was developed before Wegener's death.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "NO"},
    ])
    # Q31-36: matching (A-I labels)
    for i, (qtext, ans) in enumerate([
        ("explores Wegener's personal qualities as a scientist", "I"),
        ("describes the range of scientific fields Wegener worked in", "F"),
        ("notes that Wegener did not achieve widespread recognition in his lifetime", "A"),
        ("mentions a scientific achievement that went beyond Wegener's main work", "C"),
        ("describes the extreme physical challenges Wegener faced in his research", "H"),
        ("identifies the small number of scientists who supported Wegener's ideas", "E"),
    ], 31):
        t4_p3_qs.append({
            "id": f"cam18_t4_r_q{i}", "type": "matching",
            "question": qtext,
            "options": ["A. modest fame", "B. theoretical limitations", "C. record-breaking achievement", "D. controversial methods", "E. select group", "F. professional interests", "G. public recognition", "H. hazardous exploration", "I. biographer's perspective"],
            "correctAnswer": ans,
        })
    # Q37-40: multiple_choice
    for i, ans in enumerate(["B", "A", "D", "C"], 37):
        t4_p3_qs.append({"id": f"cam18_t4_r_q{i}", "type": "multiple_choice", "question": f"Question {i}: Choose the correct letter A, B, C or D.", "options": ["A", "B", "C", "D"], "correctAnswer": ans})
    t4_passages.append({"id": "cam18_t4_p3", "title": "Alfred Wegener: Science, Exploration and the Theory of Continental Drift", "text": PASSAGES["t4_p3"]["text"], "timeRecommended": 20, "questions": t4_p3_qs})

    tests.append({"id": "cam18_test4", "testNumber": 4, "passages": t4_passages})

    return {"id": "cam18", "title": "Cambridge IELTS 18 Academic Reading", "tests": tests}


###############################################################################
# LISTENING DATA
###############################################################################

def make_listening():
    tests = []

    # ========== LISTENING TEST 1 ==========
    lt1_parts = []
    # Part 1: Transport Survey (Q1-10)
    lt1_p1_qs = []
    for i, (qtext, ans) in enumerate([
        ("1. Postcode: _____", "DW30 7YZ"),
        ("2. Date of survey: _____", "24(th) April"),
        ("3. Occupation: _____", "dentist"),
        ("4. Reason for travelling: _____", "parking"),
        ("5. Street name: _____", "Claxby"),
        ("6. Time of day: _____", "late"),
        ("7. Time of journey: _____", "evening"),
        ("8. Travelling to: _____", "supermarket"),
        ("9. Main concern: _____", "pollution"),
        ("10. Suggestion for improvement: _____", "storage"),
    ], 1):
        lt1_p1_qs.append({"id": f"cam18_lt1_q{i}", "type": "notes_completion", "question": qtext, "options": [], "correctAnswer": ans})
    lt1_parts.append({"id": "cam18_lt1_p1", "title": "Transport Survey", "audioFile": "cam18_test1_part1.mp3", "subtitle": "", "duration": "", "questions": lt1_p1_qs})

    # Part 2: Becoming a Volunteer for ACE (Q11-20)
    lt1_p2_qs = []
    for i, ans in enumerate(["C", "A", "A", "B"], 11):
        lt1_p2_qs.append({"id": f"cam18_lt1_q{i}", "type": "multiple_choice", "question": f"Question {i}: Choose the correct letter.", "options": ["A", "B", "C"], "correctAnswer": ans})
    # Q15: multiple_choice (different options)
    lt1_p2_qs.append({"id": "cam18_lt1_q15", "type": "multiple_choice", "question": "Question 15: Choose the correct letter.", "options": ["A", "B", "C", "D", "E"], "correctAnswer": "E"})
    # Q16-20: matching (A-H)
    for i, ans in enumerate(["B", "G", "D", "A", "F"], 16):
        lt1_p2_qs.append({"id": f"cam18_lt1_q{i}", "type": "matching", "question": f"Question {i}: Match the person to the statement.", "options": ["A. experience on stage", "B. original, new ideas", "C. knowledge of local history", "D. an understanding of food and diet", "E. ability to work with children", "F. a good memory", "G. a good level of fitness", "H. experience of public speaking"], "correctAnswer": ans})
    lt1_parts.append({"id": "cam18_lt1_p2", "title": "Becoming a Volunteer for ACE", "audioFile": "cam18_test1_part2.mp3", "subtitle": "", "duration": "", "questions": lt1_p2_qs})

    # Part 3: Talk on Jobs in Fashion Design (Q21-30)
    lt1_p3_qs = []
    for i, ans in enumerate(["A", "B", "A", "C", "B", "A", "B"], 21):
        lt1_p3_qs.append({"id": f"cam18_lt1_q{i}", "type": "multiple_choice", "question": f"Question {i}: Choose the correct letter.", "options": ["A", "B", "C"], "correctAnswer": ans})
    # Q28-30: matching (A-H)
    for i, ans in enumerate(["E", "A", "C"], 28):
        lt1_p3_qs.append({"id": f"cam18_lt1_q{i}", "type": "matching", "question": f"Question {i}: Match the statement.", "options": ["A", "B", "C", "D", "E", "F", "G", "H"], "correctAnswer": ans})
    lt1_parts.append({"id": "cam18_lt1_p3", "title": "Talk on Jobs in Fashion Design", "audioFile": "cam18_test1_part3.mp3", "subtitle": "", "duration": "", "questions": lt1_p3_qs})

    # Part 4: Elephant Translocation (Q31-40)
    lt1_p4_qs = []
    for i, (qtext, ans) in enumerate([
        ("31. To protect crops, farmers build _____", "fences"),
        ("32. Elephants live in a _____ group", "family"),
        ("33. The capture team uses _____", "helicopters"),
        ("34. Scientists measure hormone levels to monitor _____", "stress"),
        ("35. The elephant is released on its _____", "sides"),
        ("36. The team checks the elephant's _____", "breathing"),
        ("37. The condition of its _____", "feet"),
        ("38. Local people benefit from increased _____", "employment"),
        ("39. Risk of _____ being used against elephants", "weapons"),
        ("40. Elephants can help to promote _____", "tourism"),
    ], 31):
        lt1_p4_qs.append({"id": f"cam18_lt1_q{i}", "type": "notes_completion", "question": qtext, "options": [], "correctAnswer": ans})
    lt1_parts.append({"id": "cam18_lt1_p4", "title": "Elephant Translocation", "audioFile": "cam18_test1_part4.mp3", "subtitle": "", "duration": "", "questions": lt1_p4_qs})

    tests.append({"id": "cam18_listening_test1", "testNumber": 1, "parts": lt1_parts})

    # ========== LISTENING TEST 2 ==========
    lt2_parts = []
    # Part 1: Working at Milo's Restaurants (Q1-10)
    lt2_p1_qs = []
    for i, (qtext, ans) in enumerate([
        ("1. Staff receive _____ before starting work", "training"),
        ("2. Employees get a 50% _____ on meals", "discount"),
        ("3. Free _____ home after late shifts", "taxi"),
        ("4. Important to give good customer _____", "service"),
        ("5. Must speak good _____", "English"),
        ("6. Branch location: _____", "Wivenhoe"),
        ("7. Uniform includes safety shoes and _____", "equipment"),
        ("8. Hourly pay: £_____", "9.75"),
        ("9. Also responsible for _____", "deliveries"),
        ("10. Day off: _____", "Sunday"),
    ], 1):
        lt2_p1_qs.append({"id": f"cam18_lt2_q{i}", "type": "notes_completion", "question": qtext, "options": [], "correctAnswer": ans})
    lt2_parts.append({"id": "cam18_lt2_p1", "title": "Working at Milo's Restaurants", "audioFile": "cam18_test2_part1.mp3", "subtitle": "", "duration": "", "questions": lt2_p1_qs})

    # Part 2: The New Housing Development (Q11-20)
    lt2_p2_qs = []
    for i, ans in enumerate(["B", "E", "B", "C"], 11):
        lt2_p2_qs.append({"id": f"cam18_lt2_q{i}", "type": "multiple_choice", "question": f"Question {i}: Choose the correct letter.", "options": ["A", "B", "C"], "correctAnswer": ans})
    # Q15-20: matching (A-H) map locations
    for i, (qtext, ans) in enumerate([
        ("15. School: _____", "G"),
        ("16. Sports Centre: _____", "C"),
        ("17. Clinic: _____", "D"),
        ("18. Community centre: _____", "B"),
        ("19. Supermarket: _____", "H"),
        ("20. Playground: _____", "A"),
    ], 15):
        lt2_p2_qs.append({"id": f"cam18_lt2_q{i}", "type": "matching", "question": qtext, "options": ["A. Playground", "B. Community centre", "C. Sports Centre", "D. Clinic", "E. Car park", "F. Bus stop", "G. School", "H. Supermarket"], "correctAnswer": ans})
    lt2_parts.append({"id": "cam18_lt2_p2", "title": "The New Housing Development", "audioFile": "cam18_test2_part2.mp3", "subtitle": "", "duration": "", "questions": lt2_p2_qs})

    # Part 3: The Laki Eruption (Q21-30)
    lt2_p3_qs = []
    for i, ans in enumerate(["C", "A", "B", "B", "A", "B"], 21):
        lt2_p3_qs.append({"id": f"cam18_lt2_q{i}", "type": "multiple_choice", "question": f"Question {i}: Choose the correct letter.", "options": ["A", "B", "C"], "correctAnswer": ans})
    # Q27-30: matching (A-H)
    for i, (qtext, ans) in enumerate([
        ("27. Iceland: _____", "D"),
        ("28. Egypt: _____", "A"),
        ("29. UK: _____", "C"),
        ("30. USA: _____", "F"),
    ], 27):
        lt2_p3_qs.append({"id": f"cam18_lt2_q{i}", "type": "matching", "question": qtext, "options": ["A. most severe loss of life", "B. widespread crop failure", "C. significant increase in deaths of young people", "D. animals suffered from sickness", "E. economic depression", "F. caused a particularly harsh winter", "G. major social unrest", "H. decline in trade"], "correctAnswer": ans})
    lt2_parts.append({"id": "cam18_lt2_p3", "title": "The Laki Eruption", "audioFile": "cam18_test2_part3.mp3", "subtitle": "", "duration": "", "questions": lt2_p3_qs})

    # Part 4: Pockets (Q31-40)
    lt2_p4_qs = []
    for i, (qtext, ans) in enumerate([
        ("31. Pockets are very _____", "convenient"),
        ("32. In the 17th century, pockets were separate from _____", "suits"),
        ("33. Pocket-makers were a separate _____", "tailor"),
        ("34. It was a specialised _____", "profession"),
        ("35. In the 19th century, pockets became less _____", "visible"),
        ("36. Held closed with _____", "string(s)"),
        ("37. They were tied around the _____", "waist(s)"),
        ("38. People kept smelling salts and _____ in pockets", "perfume"),
        ("39. Pockets reflected social _____", "image"),
        ("40. Modern women often carry a _____ rather than using pockets", "handbag"),
    ], 31):
        lt2_p4_qs.append({"id": f"cam18_lt2_q{i}", "type": "notes_completion", "question": qtext, "options": [], "correctAnswer": ans})
    lt2_parts.append({"id": "cam18_lt2_p4", "title": "Pockets", "audioFile": "cam18_test2_part4.mp3", "subtitle": "", "duration": "", "questions": lt2_p4_qs})

    tests.append({"id": "cam18_listening_test2", "testNumber": 2, "parts": lt2_parts})

    # ========== LISTENING TEST 3 ==========
    lt3_parts = []
    # Part 1: Wayside Camera Club (Q1-10)
    lt3_p1_qs = []
    for i, (qtext, ans) in enumerate([
        ("1. Name of street: _____", "Marrowfield"),
        ("2. Membership type: _____", "Relative"),
        ("3. Opportunity to _____", "socialise"),
        ("4. Membership fee: _____", "Full"),
        ("5. Competition theme: _____", "Domestic life"),
        ("6. Competition theme: _____", "Clouds"),
        ("7. Competition theme: _____", "Timing"),
        ("8. Competition theme: _____", "Animal magic"),
        ("9. Competition theme: _____", "(animal) movement"),
        ("10. Competition theme: _____", "Dark"),
    ], 1):
        lt3_p1_qs.append({"id": f"cam18_lt3_q{i}", "type": "notes_completion", "question": qtext, "options": [], "correctAnswer": ans})
    lt3_parts.append({"id": "cam18_lt3_p1", "title": "Wayside Camera Club", "audioFile": "cam18_test3_part1.mp3", "subtitle": "", "duration": "", "questions": lt3_p1_qs})

    # Part 2: Wild Mushrooms (Q11-20)
    lt3_p2_qs = []
    for i, ans in enumerate(["B", "C", "B", "D"], 11):
        lt3_p2_qs.append({"id": f"cam18_lt3_q{i}", "type": "multiple_choice", "question": f"Question {i}: Choose the correct letter.", "options": ["A", "B", "C", "D"], "correctAnswer": ans})
    for i, ans in enumerate(["C", "B", "B", "C", "A", "A"], 15):
        lt3_p2_qs.append({"id": f"cam18_lt3_q{i}", "type": "multiple_choice", "question": f"Question {i}: Choose the correct letter.", "options": ["A", "B", "C", "D"], "correctAnswer": ans})
    lt3_parts.append({"id": "cam18_lt3_p2", "title": "Wild Mushrooms", "audioFile": "cam18_test3_part2.mp3", "subtitle": "", "duration": "", "questions": lt3_p2_qs})

    # Part 3: Automation and the Future of Work (Q21-30)
    lt3_p3_qs = []
    for i, ans in enumerate(["A", "E", "B", "D"], 21):
        lt3_p3_qs.append({"id": f"cam18_lt3_q{i}", "type": "multiple_choice", "question": f"Question {i}: Choose the correct letter.", "options": ["A", "B", "C", "D", "E"], "correctAnswer": ans})
    # Q25-30: matching (A-H)
    for i, (qtext, ans) in enumerate([
        ("25. Accountants: _____", "G"),
        ("26. Hairdressers: _____", "E"),
        ("27. Admin staff: _____", "B"),
        ("28. Agricultural workers: _____", "C"),
        ("29. Care workers: _____", "F"),
        ("30. Bank clerks: _____", "A"),
    ], 25):
        lt3_p3_qs.append({"id": f"cam18_lt3_q{i}", "type": "matching", "question": qtext, "options": ["A. likely to be at risk", "B. role has become more interesting", "C. number has fallen dramatically", "D. working conditions have improved", "E. higher disposable income", "F. likely significant rise in demand", "G. employment and productivity risen", "H. increasingly specialised"], "correctAnswer": ans})
    lt3_parts.append({"id": "cam18_lt3_p3", "title": "Automation and the Future of Work", "audioFile": "cam18_test3_part3.mp3", "subtitle": "", "duration": "", "questions": lt3_p3_qs})

    # Part 4: Space Traffic Management (Q31-40)
    lt3_p4_qs = []
    for i, (qtext, ans) in enumerate([
        ("31. Need for _____ improvements", "Technical"),
        ("32. Satellites are becoming _____", "Cheap"),
        ("33. There are _____ of new satellites", "Thousands"),
        ("34. Problem of _____", "Identification"),
        ("35. System for _____", "Tracking"),
        ("36. Use by _____ organisations", "Military"),
        ("37. Determining _____", "Location"),
        ("38. _____ of future movements", "Prediction"),
        ("39. A shared _____", "Database"),
        ("40. Importance of _____", "Trust"),
    ], 31):
        lt3_p4_qs.append({"id": f"cam18_lt3_q{i}", "type": "notes_completion", "question": qtext, "options": [], "correctAnswer": ans})
    lt3_parts.append({"id": "cam18_lt3_p4", "title": "Space Traffic Management", "audioFile": "cam18_test3_part4.mp3", "subtitle": "", "duration": "", "questions": lt3_p4_qs})

    tests.append({"id": "cam18_listening_test3", "testNumber": 3, "parts": lt3_parts})

    # ========== LISTENING TEST 4 ==========
    lt4_parts = []
    # Part 1: Job Application - Dental Practice Receptionist (Q1-10)
    lt4_p1_qs = []
    for i, (qtext, ans) in enumerate([
        ("1. Job title: _____", "Receptionist"),
        ("2. Type of practice: _____", "Medical"),
        ("3. Name of practice: _____", "Chastons"),
        ("4. Responsible for _____", "appointments"),
        ("5. Must use a _____", "database"),
        ("6. Must have previous _____", "experience"),
        ("7. Applicant should be _____", "confident"),
        ("8. Job is initially _____", "temporary"),
        ("9. Hourly pay: £_____", "1.15"),
        ("10. Benefit: free _____", "parking"),
    ], 1):
        lt4_p1_qs.append({"id": f"cam18_lt4_q{i}", "type": "notes_completion", "question": qtext, "options": [], "correctAnswer": ans})
    lt4_parts.append({"id": "cam18_lt4_p1", "title": "Job Application", "audioFile": "cam18_test4_part1.mp3", "subtitle": "", "duration": "", "questions": lt4_p1_qs})

    # Part 2: Museum/Farm (Q11-20)
    lt4_p2_qs = []
    for i, ans in enumerate(["B", "A", "A", "C"], 11):
        lt4_p2_qs.append({"id": f"cam18_lt4_q{i}", "type": "multiple_choice", "question": f"Question {i}: Choose the correct letter.", "options": ["A", "B", "C", "D"], "correctAnswer": ans})
    # Q15-20: matching (A-H)
    for i, (qtext, ans) in enumerate([
        ("15. Four Seasons: _____", "F"),
        ("16. Farmhouse Kitchen: _____", "G"),
        ("17. A Year on the Farm: _____", "E"),
        ("18. Wagon Walk: _____", "A"),
        ("19. Bees are Magic: _____", "C"),
        ("20. The Pond: _____", "B"),
    ], 15):
        lt4_p2_qs.append({"id": f"cam18_lt4_q{i}", "type": "matching", "question": qtext, "options": ["A. parents must supervise children", "B. new things to see", "C. closed today", "D. available all year", "E. quiz for visitors", "F. features something created by students", "G. expert is here today", "H. free entry"], "correctAnswer": ans})
    lt4_parts.append({"id": "cam18_lt4_p2", "title": "Agricultural Museum", "audioFile": "cam18_test4_part2.mp3", "subtitle": "", "duration": "", "questions": lt4_p2_qs})

    # Part 3: Children's Activities (Q21-30)
    lt4_p3_qs = []
    # Q21-22: multiple_choice (A-D)
    for i, ans in enumerate(["B", "D"], 21):
        lt4_p3_qs.append({"id": f"cam18_lt4_q{i}", "type": "multiple_choice", "question": f"Question {i}: Choose the correct letter.", "options": ["A", "B", "C", "D"], "correctAnswer": ans})
    # Q23-27: matching (A-H)
    for i, (qtext, ans) in enumerate([
        ("23. Sid: _____", "D"),
        ("24. Jack: _____", "A"),
        ("25. Naomi: _____", "C"),
        ("26. Anya: _____", "G"),
        ("27. Zara: _____", "F"),
    ], 23):
        lt4_p3_qs.append({"id": f"cam18_lt4_q{i}", "type": "matching", "question": qtext, "options": ["A. demonstrated independence", "B. showed good leadership", "C. developed competitive attitude", "D. found activity calming", "E. improved concentration", "F. seemed confused", "G. found activity easy", "H. lacked confidence"], "correctAnswer": ans})
    # Q28-30: multiple_choice (A-C)
    for i, ans in enumerate(["A", "B", "C"], 28):
        lt4_p3_qs.append({"id": f"cam18_lt4_q{i}", "type": "multiple_choice", "question": f"Question {i}: Choose the correct letter.", "options": ["A", "B", "C"], "correctAnswer": ans})
    lt4_parts.append({"id": "cam18_lt4_p3", "title": "Children's Activities", "audioFile": "cam18_test4_part3.mp3", "subtitle": "", "duration": "", "questions": lt4_p3_qs})

    # Part 4: Novelist (Q31-40)
    lt4_p4_qs = []
    for i, (qtext, ans) in enumerate([
        ("31. Her first idea for a story was based on the _____", "plot"),
        ("32. She experienced _____ while growing up", "poverty"),
        ("33. She travelled around _____", "Europe"),
        ("34. She wrote _____ as an outlet for creativity", "poetry"),
        ("35. She is talented at _____", "drawings"),
        ("36. She started collecting _____", "furniture"),
        ("37. She buys old _____", "lamps"),
        ("38. She finds inspiration by the _____", "harbour"),
        ("39. Her stories often involve _____", "children"),
        ("40. Her stories explore relationships with _____", "relatives"),
    ], 31):
        lt4_p4_qs.append({"id": f"cam18_lt4_q{i}", "type": "notes_completion", "question": qtext, "options": [], "correctAnswer": ans})
    lt4_parts.append({"id": "cam18_lt4_p4", "title": "Life of a Novelist", "audioFile": "cam18_test4_part4.mp3", "subtitle": "", "duration": "", "questions": lt4_p4_qs})

    tests.append({"id": "cam18_listening_test4", "testNumber": 4, "parts": lt4_parts})

    return {"id": "cam18", "title": "Cambridge IELTS 18 Academic Listening", "tests": tests}


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

    # Count questions per test
    print("\nReading question counts:")
    for t in reading["tests"]:
        total = sum(len(p["questions"]) for p in t["passages"])
        print(f"  Test {t['testNumber']}: {total} questions")

    print("\nListening question counts:")
    for t in listening["tests"]:
        total = sum(len(p["questions"]) for p in t["parts"])
        print(f"  Test {t['testNumber']}: {total} questions")


if __name__ == "__main__":
    main()
