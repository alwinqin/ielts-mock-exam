#!/usr/bin/env python3
"""Generate cam15 reading.json and listening.json with complete data."""

import json
import os

OUT_DIR = "data/cambridge/cam15"

###############################################################################
# PASSAGE TEXTS (descriptive summaries, not authentic Cambridge text)
###############################################################################

PASSAGES = {
    # TEST 1
    "t1_p1": {
        "title": "Nutmeg - a valuable spice",
        "text": "Nutmeg was once one of the most valuable commodities in the world, prized for its distinctive flavour and medicinal properties. The nutmeg tree, Myristica fragrans, is native to the Banda Islands in Indonesia, which were the world's sole source of this precious spice for centuries. The fruit of the tree contains both nutmeg (the seed) and mace (the aril surrounding the seed), making it a uniquely dual-purpose spice. European explorers and traders, particularly the Portuguese, Dutch, and British, competed fiercely for control of the nutmeg trade, with the Dutch East India Company eventually establishing a brutal monopoly.\n\nThe Dutch employed extreme measures to maintain their monopoly, including limiting cultivation to a few islands and destroying nutmeg trees in other locations. They also engaged in violent conflict with the indigenous population and rival European powers. The value of nutmeg was so great that it drove expeditions, shaped colonial policies, and influenced the course of European history. The spice was believed to have medicinal benefits, including the ability to treat stomach ailments and, during the plague, was thought to offer protection against infection.\n\nUltimately, the Dutch monopoly was broken when nutmeg trees were successfully transplanted to other locations, including Grenada and Mauritius. The value of nutmeg declined significantly as supply increased and competition grew. Today, nutmeg is a common household spice, but its remarkable history as a driver of global exploration and colonial ambition remains one of the most fascinating chapters in the story of the spice trade.",
    },
    "t1_p2": {
        "title": "Driverless cars",
        "text": "The development of autonomous vehicles represents one of the most significant technological transformations in modern transportation. Driverless cars rely on a combination of sensors, cameras, radar, and artificial intelligence to navigate roads without human input. The potential benefits are substantial: the vast majority of road accidents are caused by human error, so removing the human driver could dramatically reduce collisions, injuries, and fatalities. Autonomous vehicles could also provide mobility for the elderly, disabled, and those too young to drive, while potentially reducing traffic congestion and emissions through more efficient driving patterns.\n\nHowever, the path to widespread adoption of driverless cars faces numerous challenges. Technical hurdles include navigating complex and unpredictable environments, handling adverse weather conditions, and ensuring the reliability of safety-critical systems. Legal and regulatory frameworks need to be developed to determine liability in the event of accidents and to establish safety standards. Ethical questions also arise, such as how autonomous vehicles should be programmed to make decisions in unavoidable crash scenarios. The transition period, when autonomous and human-driven vehicles share the roads, presents additional complexities.\n\nThe social and economic implications of driverless cars are far-reaching. Industries such as insurance, taxi services, and freight transportation would be transformed. The concept of car ownership itself might shift, with people potentially opting for shared autonomous vehicle services rather than owning private cars. Urban planning could change, with reduced need for parking spaces in city centres. While the promise of driverless technology is immense, the timeline for full autonomy remains uncertain, with experts disagreeing on when truly self-driving vehicles will become commonplace on public roads.",
    },
    "t1_p3": {
        "title": "What is exploration?",
        "text": "The word 'exploration' traditionally conjures images of intrepid adventurers setting foot in uncharted territories - remote jungles, polar ice caps, or the surface of the moon. This classical view of exploration emphasises physical discovery, of going where no one has gone before. However, the passage challenges readers to reconsider this narrow definition. It questions whether exploration necessarily requires geographical discovery, or whether it can encompass the pursuit of knowledge and understanding in any domain. The author argues that true exploration involves pushing the boundaries of human knowledge, whether through scientific research, intellectual inquiry, or personal growth.\n\nThe passage examines different perspectives on what constitutes genuine exploration. Some argue that in an age where every corner of the globe has supposedly been mapped, the age of exploration is over. Others contend that exploration continues in new forms - deep ocean research, space exploration, advances in medicine, and the study of human consciousness. The author explores the motivations behind exploration, from simple curiosity and the desire for adventure to commercial opportunity and national prestige. The relationship between exploration and tourism is also examined, with the question of whether travelling to well-known destinations can ever be considered true exploration.\n\nThe text also considers the personalities and characteristics of famous explorers throughout history, examining what drove them to undertake dangerous journeys into the unknown. It reflects on the tension between the romantic ideal of exploration and its often harsh reality, including the physical dangers, the impact on indigenous populations, and the complex legacies that explorers leave behind. Ultimately, the passage invites readers to form their own understanding of what it means to explore, suggesting that the spirit of exploration may be more about mindset and attitude than about geographical location.",
    },
    # TEST 2
    "t2_p1": {
        "title": "Could Urban Engineers Learn from Dance?",
        "text": "This article proposes that urban planners and engineers could gain valuable insights from the principles of dance and choreography. The central idea is that dance involves the coordinated movement of bodies through space, responding to rhythm, each other, and the environment - concepts that have direct parallels in how people move through urban spaces. The author argues that cities designed purely for efficiency, with a focus on vehicle traffic and rigid infrastructure, often fail to accommodate the natural flow of human movement and social interaction. By studying how dancers move in relation to each other and their surroundings, engineers might learn to create urban environments that feel more intuitive and harmonious.\n\nThe passage explores specific ways in which choreographic principles could be applied to urban design. For example, the concept of 'ensemble' in dance - where individual performers adjust their movements in relation to the group - could inform the design of intersections and public spaces where pedestrians, cyclists, and vehicles interact. The timing and rhythm that are fundamental to dance could help engineers think about traffic flow and pedestrian movement in new ways. The piece also discusses how the work of specific choreographers and dance companies has inspired architectural and urban design projects.\n\nThe article also acknowledges the limitations of this approach. Urban engineering deals with variables that dance does not, such as infrastructure costs, safety regulations, and the needs of diverse populations. The author does not suggest that dance provides a complete solution, but rather that it offers a fresh perspective that can complement traditional engineering approaches. By incorporating principles of flow, rhythm, and coordination from dance, urban spaces might become more pleasant, efficient, and responsive to the people who use them.",
    },
    "t2_p2": {
        "title": "Should We Try to Bring Extinct Species Back to Life?",
        "text": "De-extinction - the process of resurrecting species that have died out - was once the stuff of science fiction, but advances in genetic technology have made it a serious scientific possibility. The passage examines the arguments for and against bringing back extinct species such as the woolly mammoth, the passenger pigeon, and the Tasmanian tiger. Proponents argue that de-extinction could restore biodiversity, repair damaged ecosystems, and correct past human-caused extinctions. They also suggest that the technologies developed for de-extinction could aid in the conservation of currently endangered species. The scientific challenges are considerable, involving the reconstruction of ancient genomes, cloning, and the ethical question of where resurrected animals would live.\n\nCritics of de-extinction raise several objections. They argue that the considerable financial resources required would be better spent on preventing the extinction of living species, many of which are critically endangered. Furthermore, even if scientists could recreate the genetic blueprint of an extinct species, the resulting animals would lack the learned behaviours, social structures, and ecological context of their ancestors. There are also concerns about animal welfare, as the first resurrected individuals might suffer from health problems or struggle to adapt to modern environments that differ significantly from their historical habitats.\n\nThe passage presents the views of several scientists working in this field. Some are optimistic, pointing to successful examples of genetic rescue in endangered species and the potential for de-extinction to capture the public imagination and galvanise conservation efforts. Others are more cautious, emphasising the complexity of ecosystems and the unpredictable consequences of reintroducing long-extinct species. The debate ultimately reflects deeper questions about humanity's relationship with nature, our responsibility for past extinctions, and how we should approach emerging biotechnologies.",
    },
    "t2_p3": {
        "title": "Having a Laugh",
        "text": "Laughter is a universal human behaviour that plays a far more significant role in social interaction than is commonly recognised. The passage examines the scientific study of laughter and humour, exploring what makes things funny and why laughter evolved. Research suggests that laughter serves important social functions, including bonding between individuals, signalling shared understanding, and defusing tension in group situations. Far from being a trivial or frivolous activity, laughter appears to be deeply embedded in human communication and social organisation. Brain imaging studies have shown that laughter activates areas of the brain associated with reward, emotion, and social cognition.\n\nThe passage also explores the evolutionary origins of laughter. While humans are the only species that produces laughter in the complex social contexts that characterise humour, other animals, particularly primates and rats, produce vocalisations during social play that resemble laughter. This suggests that the evolutionary roots of laughter lie in play behaviour and social bonding. The text discusses how laughter in humans has evolved from these origins into a sophisticated social tool that can convey complex information about relationships, status, and emotional states. The ability to produce and appreciate humour is closely tied to cognitive development and social intelligence.\n\nThe article examines different types of humour and their effects on individuals and groups. It considers why some people find certain things funny while others do not, and how humour styles relate to personality and social position. The research indicates that laughter in conversation is much more about social signalling than about responding to jokes - people laugh more in social situations than when alone, and laughter is often used to smooth interactions and express agreement or affiliation. The passage concludes by considering the health benefits of laughter, including its effects on stress reduction, immune function, and pain tolerance.",
    },
    # TEST 3
    "t3_p1": {
        "title": "Henry Moore (1898-1986)",
        "text": "Henry Moore was one of the most influential British sculptors of the twentieth century. Born in Castleford, Yorkshire, in 1898, he was the seventh child of a coal miner. After serving in World War I, Moore studied at the Leeds School of Art and later at the Royal College of Art in London. His early work was influenced by pre-Columbian art, African sculpture, and the work of artists such as Picasso and Brancusi. Moore developed a distinctive style characterised by abstract, organic forms that often evoked the human body, particularly the reclining female figure. His sculptures frequently featured holes and voids, creating a dynamic relationship between solid mass and empty space.\n\nMoore's career rose to prominence in the post-war period, when he received numerous major commissions for public spaces. His works can be found in cities around the world, from London's Westminster Abbey to the grounds of the United Nations in New York. He also produced a significant body of drawings, including his famous 'Shelter Drawings' depicting Londoners sheltering in Tube stations during the Blitz. Moore's approach to materials was innovative; he worked directly with stone, wood, bronze, and other materials, developing techniques that allowed him to express his vision of organic abstraction. His large-scale bronze sculptures became particularly famous for their monumental presence and their ability to engage with the surrounding landscape.\n\nThe passage also discusses Moore's artistic philosophy and his approach to education. He was a dedicated teacher at the Royal College of Art and later at the Chelsea School of Art, where he influenced a generation of British sculptors. Moore was deeply interested in the relationship between sculpture and nature, often placing his works outdoors where they could interact with natural light and the changing environment. His legacy includes not only his vast body of work but also the Henry Moore Foundation, which continues to promote sculpture and support artists. Moore's death in 1986 marked the end of an era, but his influence on modern sculpture remains profound.",
    },
    "t3_p2": {
        "title": "The Desolenator: Producing Clean Water",
        "text": "The Desolenator is an innovative solar-powered device designed to address one of the world's most pressing problems: the lack of access to clean drinking water. Developed by a team of engineers and entrepreneurs, the device uses solar thermal energy to distil water from virtually any source, including seawater, brackish water, and contaminated freshwater. Unlike conventional desalination technologies such as reverse osmosis, which require significant electrical power and complex infrastructure, the Desolenator operates entirely on solar energy, making it suitable for off-grid communities in developing countries and disaster-stricken areas.\n\nThe technology behind the Desolenator involves capturing solar heat to evaporate water, which is then condensed to produce pure, drinkable water. This process effectively removes salts, heavy metals, bacteria, viruses, and other contaminants. The device is designed to be durable, low-maintenance, and scalable, with the capacity to produce a meaningful quantity of clean water per day. The developers have focused on making the technology affordable and accessible, with a business model that balances commercial viability with social impact. The passage describes the inspiration behind the invention and the journey from initial concept to working prototype.\n\nThe potential impact of the Desolenator is significant. An estimated two billion people worldwide lack access to safely managed drinking water, and climate change is expected to exacerbate water scarcity in many regions. The device could provide a sustainable solution for communities that currently rely on bottled water, untreated sources, or energy-intensive purification methods. The passage also discusses the challenges faced in bringing the technology to scale, including manufacturing costs, distribution logistics, and competition from established water treatment technologies. Despite these challenges, the Desolenator represents an innovative approach to using renewable energy to meet a fundamental human need.",
    },
    "t3_p3": {
        "title": "Why Fairy Tales are Really Scary Tales",
        "text": "Fairy tales are among the most enduring stories in human culture, passed down through generations in various forms. The passage examines the dark origins of these tales and the reasons why they contain such frightening elements. Contrary to the sanitised, Disneyfied versions that many people are familiar with today, the original versions of stories such as Little Red Riding Hood, Cinderella, and Snow White were considerably darker, featuring violence, cruelty, and disturbing themes. The passage explores why these elements were present and what functions they served in the societies that first told these stories.\n\nScholars have proposed various theories to explain the enduring appeal and purpose of fairy tales. Some argue that the frightening elements served as cautionary warnings, teaching children about real dangers in the world. Others suggest that fairy tales provided a way for communities to process collective anxieties and social tensions. The passage discusses the work of folklorists such as the Brothers Grimm, who collected and published traditional stories from oral sources, often adapting them for a reading audience. The transition from oral tradition to written text fundamentally changed many tales, as did later adaptations for children's literature and film.\n\nThe passage also considers the cultural and psychological significance of fairy tales. Despite their scary content - or perhaps because of it - these stories have proven remarkably resilient across cultures and historical periods. Researchers have found that fairy tales from different parts of the world share common themes and structures, suggesting that they speak to universal human concerns. The text discusses how modern research in fields such as evolutionary psychology and literary studies has shed light on why these ancient stories continue to captivate audiences, and why their dark elements may be essential to their power and longevity.",
    },
    # TEST 4
    "t4_p1": {
        "title": "The Return of the Huarango",
        "text": "The huarango tree once formed vast, dense forests in the coastal deserts of Peru, particularly in the Ica Valley region. This remarkable tree species is superbly adapted to extreme arid conditions, with roots that can extend deep into the ground to access groundwater, and a canopy that provides shade and helps retain moisture. The huarango played a crucial ecological role: it prevented soil erosion, improved soil fertility by fixing nitrogen, and supported a diverse range of plant and animal species. For centuries, the tree was a keystone species in one of the world's most fragile ecosystems, creating patches of green in an otherwise barren landscape.\n\nHowever, centuries of human activity, particularly the clearing of land for agriculture, led to the dramatic decline of the huarango forests. The introduction of intensive farming, especially cotton cultivation, required vast areas of land and large quantities of water, which depleted the water table and made it difficult for huarango trees to survive. By the time scientists and conservationists recognised the scale of the problem, the huarango forests had been reduced to a tiny fraction of their original extent. The loss of the trees had severe environmental consequences, including accelerated desertification, loss of biodiversity, and increased vulnerability to drought.\n\nThe passage describes the concerted efforts of scientists, local communities, and conservation organisations to restore the huarango. These efforts involve collecting seeds from surviving trees, growing saplings in nurseries, and planting them in carefully selected locations. Local farmers have been enlisted as partners in the restoration effort, learning about the ecological benefits of the huarango and how to integrate the trees into their agricultural systems. The passage highlights the importance of combining scientific knowledge with traditional local practices, and the challenges of restoring a keystone species in an environment that has been fundamentally altered by human activity.",
    },
    "t4_p2": {
        "title": "Silbo Gomero - the Whistle 'Language' of the Canary Islands",
        "text": "Silbo Gomero is a unique whistled language used on the island of La Gomera in the Canary Islands. The language works by replacing the vowels and consonants of spoken Spanish with whistled tones, creating a system of communication that can be heard over distances of up to several kilometres. This remarkable adaptation was developed by the island's early inhabitants as a practical solution to the island's challenging geography, which features steep ravines, deep valleys, and narrow paths that make travel difficult. The whistled language allowed people to communicate across these obstacles, conveying complex messages including news, warnings, and greetings, without the need to travel.\n\nThe passage explains how Silbo Gomero functions as a linguistic system. Despite being based on whistles rather than spoken sounds, it preserves the essential phonetic structure of Spanish, allowing skilled whistlers to communicate virtually any message. Two distinct whistled tones represent the five Spanish vowels, while the consonants are indicated by variations in pitch and rhythm. Mastery of Silbo Gomero requires considerable practice; experienced whistlers can hold conversations at a remarkable speed, and the language can be understood even when the speakers are not visible to each other. The passage describes how the language was traditionally learned within families and communities.\n\nSilbo Gomero faced decline in the twentieth century as modern communication technologies such as telephones and mobile phones reduced the practical need for whistled communication. However, recognition of its unique cultural value led to efforts to preserve and revitalise it. In 2009, UNESCO designated Silbo Gomero as a Masterpiece of the Oral and Intangible Heritage of Humanity. The language is now taught in local schools, and there are initiatives to promote its use in cultural events and tourism. The passage discusses the challenges of preserving an oral tradition in the modern world and the importance of maintaining linguistic diversity.",
    },
    "t4_p3": {
        "title": "Environmental Practices of Big Businesses",
        "text": "This passage critically examines the environmental practices of large corporations, exploring the gap between their public statements about sustainability and their actual behaviour. Many major companies have adopted environmental policies, published sustainability reports, and made public commitments to reducing their carbon footprint. However, researchers have found significant discrepancies between what companies say and what they do. The passage discusses various factors that influence corporate environmental behaviour, including government regulation, consumer pressure, shareholder activism, and economic incentives.\n\nThe text distinguishes between different levels of corporate environmental engagement. Some companies genuinely integrate environmental considerations into their core business strategy, investing in clean technologies, improving resource efficiency, and developing sustainable products. Others engage primarily in 'greenwashing' - using marketing and public relations to create a misleading impression of environmental responsibility without making substantial changes to their operations. The passage examines case studies of both approaches and discusses how to distinguish genuine commitment from superficial gestures. The role of third-party certifications, environmental audits, and NGO monitoring is also explored.\n\nThe passage concludes by considering what meaningful corporate environmental responsibility looks like and what conditions are necessary for it to flourish. It discusses the tension between short-term profitability and long-term sustainability, and the role of different stakeholders in holding corporations accountable. The author argues that without strong regulation and effective enforcement, voluntary corporate initiatives are unlikely to produce the scale of change needed to address environmental challenges. However, companies that do embrace genuine environmental responsibility may find competitive advantages through innovation, cost savings, and enhanced reputation.",
    },
}

###############################################################################
# READING QUESTIONS
###############################################################################

def make_reading():
    tests = []

    # ========== TEST 1 ==========
    t1_passages = []

    # Passage 1: Nutmeg - a valuable spice (Q1-13)
    t1_p1_qs = []
    # Q1-4: notes_completion
    for i, (qtext, ans) in enumerate([
        ("The fruit of the nutmeg tree is 1. _____ in shape", "oval"),
        ("The outer covering of the fruit is called the 2. _____", "husk"),
        ("The 3. _____ of the fruit produces nutmeg", "seed"),
        ("The spice 4. _____ comes from the covering of the nutmeg seed", "mace"),
    ], 1):
        t1_p1_qs.append({
            "id": f"cam15_t1_r_q{i}",
            "type": "notes_completion",
            "question": qtext,
            "options": [],
            "correctAnswer": ans,
        })
    # Q5-7: tfng
    t1_p1_qs.extend([
        {"id": "cam15_t1_r_q5", "type": "tfng", "question": "The Portuguese were the first Europeans to control the nutmeg trade.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE"},
        {"id": "cam15_t1_r_q6", "type": "tfng", "question": "Nutmeg was believed to be effective against certain diseases.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
        {"id": "cam15_t1_r_q7", "type": "tfng", "question": "The Dutch destroyed nutmeg trees on islands they did not control.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "TRUE"},
    ])
    # Q8-13: table_completion
    for i, (qtext, ans) in enumerate([
        ("8. _____ traders controlled the supply of nutmeg in the 17th century", "Arabs"),
        ("Nutmeg was believed to be a cure for the 9. _____", "plague"),
        ("The Dutch used 10. _____ to treat the nutmeg seed before export", "lime"),
        ("The ship '11. _____' carried nutmeg trees from the Banda Islands", "Run"),
        ("Nutmeg trees were successfully grown on the island of 12. _____", "Mauritius"),
        ("The decline in nutmeg's value was accelerated by a 13. _____", "tsunami"),
    ], 8):
        t1_p1_qs.append({
            "id": f"cam15_t1_r_q{i}",
            "type": "table_completion",
            "question": qtext,
            "options": [],
            "correctAnswer": ans,
        })
    t1_passages.append({"id": "cam15_t1_p1", "title": "Nutmeg - a valuable spice", "text": PASSAGES["t1_p1"]["text"], "timeRecommended": 20, "questions": t1_p1_qs})

    # Passage 2: Driverless cars (Q14-26)
    t1_p2_qs = []
    # Q14-18: matching_info
    for i, (qtext, ans) in enumerate([
        ("how autonomous vehicles could help those who cannot drive", "C"),
        ("a reference to the challenge of sharing roads with human drivers", "B"),
        ("the potential financial benefits of autonomous vehicles", "E"),
        ("the variety of technologies that work together in driverless cars", "G"),
        ("the need for new laws to govern autonomous vehicles", "D"),
    ], 14):
        t1_p2_qs.append({"id": f"cam15_t1_r_q{i}", "type": "matching_info", "question": qtext, "options": ["A", "B", "C", "D", "E", "F", "G"], "correctAnswer": ans})
    # Q19-22: summary_completion - NO MORE THAN TWO WORDS
    for i, (qtext, ans) in enumerate([
        ("The most significant benefit of driverless cars is the reduction of 19. _____", "human error"),
        ("People may choose services based on 20. _____ rather than owning vehicles", "car-sharing"),
        ("The concept of 21. _____ itself may change", "ownership"),
        ("Autonomous driving patterns could reduce fuel consumption and 22. _____", "mileage"),
    ], 19):
        t1_p2_qs.append({"id": f"cam15_t1_r_q{i}", "type": "summary_completion", "question": qtext, "options": [], "correctAnswer": ans})
    # Q23-24: multiple_choice_multi TWO benefits
    t1_p2_qs.append({"id": "cam15_t1_r_q23", "type": "multiple_choice_multi", "question": "Which TWO benefits of driverless cars are mentioned?\nA. reduced parking space requirements\nB. lower vehicle manufacturing costs\nC. fewer road accidents\nD. increased mobility for non-drivers\nE. elimination of traffic congestion", "options": ["A", "B", "C", "D", "E"], "correctAnswer": "C, D"})
    # Q25-26: multiple_choice_multi TWO challenges
    t1_p2_qs.append({"id": "cam15_t1_r_q24", "type": "multiple_choice_multi", "question": "Which TWO challenges to the adoption of driverless cars are mentioned?\nA. ethical dilemmas about decision-making\nB. lack of public interest\nC. insufficient battery technology\nD. high cost of sensors\nE. difficulty handling bad weather", "options": ["A", "B", "C", "D", "E"], "correctAnswer": "A, E"})
    t1_passages.append({"id": "cam15_t1_p2", "title": "Driverless cars", "text": PASSAGES["t1_p2"]["text"], "timeRecommended": 20, "questions": t1_p2_qs})

    # Passage 3: What is exploration? (Q27-40)
    t1_p3_qs = []
    # Q27-30: multiple_choice
    for i, ans in enumerate(["A", "C", "C", "D"], 27):
        t1_p3_qs.append({
            "id": f"cam15_t1_r_q{i}",
            "type": "multiple_choice",
            "question": f"Question {i}: Choose the correct letter, A, B, C or D.",
            "options": ["A", "B", "C", "D"],
            "correctAnswer": ans,
        })
    # Q31-32: multiple_choice
    for i, ans in enumerate(["A", "B"], 31):
        t1_p3_qs.append({
            "id": f"cam15_t1_r_q{i}",
            "type": "multiple_choice",
            "question": f"Question {i}: Choose the correct letter, A, B, C or D.",
            "options": ["A", "B", "C", "D"],
            "correctAnswer": ans,
        })
    # Q33-37: matching_names to explorers
    for i, (qtext, ans) in enumerate([
        ("who believed exploration involves immersing oneself in a foreign culture", "E"),
        ("who warned against mistaking travel for genuine exploration", "A"),
        ("who argued that exploration requires purpose and planning", "D"),
        ("whose exploration was driven by a desire to document disappearing ways of life", "E"),
        ("who thought exploration was primarily about personal challenge", "B"),
    ], 33):
        t1_p3_qs.append({
            "id": f"cam15_t1_r_q{i}",
            "type": "matching_names",
            "question": qtext,
            "options": ["A. Peter Fleming", "B. Ran Fiennes", "C. Sara Wheeler", "D. Robin Hanbury-Tenison", "E. Wilfred Thesiger"],
            "correctAnswer": ans,
        })
    # Q38-40: summary_completion - NO MORE THAN TWO WORDS
    for i, (qtext, ans) in enumerate([
        ("Some believe that undertaking 38. _____ to remote places qualifies as exploration", "expeditions"),
        ("Geniune exploration can involve studying 39. _____ peoples and their cultures", "uncontacted"),
        ("Others argue that you cannot call something exploration when the entire 40. _____ has already been mapped", "(land) surface"),
    ], 38):
        t1_p3_qs.append({"id": f"cam15_t1_r_q{i}", "type": "summary_completion", "question": qtext, "options": [], "correctAnswer": ans})
    t1_passages.append({"id": "cam15_t1_p3", "title": "What is exploration?", "text": PASSAGES["t1_p3"]["text"], "timeRecommended": 20, "questions": t1_p3_qs})

    tests.append({"id": "cam15_test1", "testNumber": 1, "passages": t1_passages})

    # ========== TEST 2 ==========
    t2_passages = []

    # Passage 1: Could Urban Engineers Learn from Dance? (Q1-13)
    t2_p1_qs = []
    # Q1-6: matching_info (statements to paragraphs)
    for i, (qtext, ans) in enumerate([
        ("a description of how dance movements relate to urban planning concepts", "B"),
        ("how the idea of ensemble performance could improve intersection design", "C"),
        ("the limitations of applying dance principles to engineering problems", "F"),
        ("an example of a dance company that inspired an architectural project", "D"),
        ("how studying dance can change engineers' thinking about city spaces", "E"),
        ("the suggestion that current approaches to urban design are too rigid", "A"),
    ], 1):
        t2_p1_qs.append({"id": f"cam15_t2_r_q{i}", "type": "matching_info", "question": qtext, "options": ["A", "B", "C", "D", "E", "F", "G"], "correctAnswer": ans})
    # Q7-13: sentence_completion
    for i, (qtext, ans) in enumerate([
        ("One benefit of applying dance principles to urban design is improved pedestrian 7. _____", "Safety"),
        ("Dance concepts could help reduce 8. _____ congestion in city centres", "Traffic"),
        ("The design of the 9. _____ should consider how people naturally move through a space", "Carriageway"),
        ("Dancers adjust their movements in response to each other - a concept that relates to 10. _____ phone use while walking", "Mobile"),
        ("Without careful design, certain urban spaces can become 11. _____ for pedestrians", "Dangerous"),
        ("Dance-inspired design could help strengthen local 12. _____", "Communities"),
        ("Urban planners should aim to create environments that are both functional and 13. _____", "Healthy"),
    ], 7):
        t2_p1_qs.append({"id": f"cam15_t2_r_q{i}", "type": "sentence_completion", "question": qtext, "options": [], "correctAnswer": ans})
    t2_passages.append({"id": "cam15_t2_p1", "title": "Could Urban Engineers Learn from Dance?", "text": PASSAGES["t2_p1"]["text"], "timeRecommended": 20, "questions": t2_p1_qs})

    # Passage 2: Should We Try to Bring Extinct Species Back to Life? (Q14-26)
    t2_p2_qs = []
    # Q14-17: matching_info
    for i, (qtext, ans) in enumerate([
        ("the argument that de-extinction technology could help endangered species", "F"),
        ("the view that the money spent on de-extinction could be used more productively elsewhere", "A"),
        ("the idea that resurrected animals might struggle in today's environment", "D"),
        ("an example of genetic rescue already being used successfully", "A"),
    ], 14):
        t2_p2_qs.append({"id": f"cam15_t2_r_q{i}", "type": "matching_info", "question": qtext, "options": ["A", "B", "C", "D", "E", "F", "G"], "correctAnswer": ans})
    # Q18-22: summary_completion
    for i, (qtext, ans) in enumerate([
        ("the animal's distinctive 18. _____", "genetic traits"),
        ("adaptations that helped minimise 19. _____", "heat loss"),
        ("the size and shape of their 20. _____", "ears"),
        ("the presence of 21. _____ beneath the skin", "insulating fat"),
        ("reducing 22. _____ through improved digestion", "emissions"),
    ], 18):
        t2_p2_qs.append({"id": f"cam15_t2_r_q{i}", "type": "summary_completion", "question": qtext, "options": [], "correctAnswer": ans})
    # Q23-26: matching_names
    for i, (qtext, ans) in enumerate([
        ("emphasised the importance of public engagement in de-extinction projects", "B"),
        ("expressed concern about the ecological risks of reintroducing extinct species", "C"),
        ("highlighted the technological breakthroughs that have made de-extinction possible", "A"),
        ("argued that de-extinction should not distract from current conservation needs", "C"),
    ], 23):
        t2_p2_qs.append({
            "id": f"cam15_t2_r_q{i}",
            "type": "matching_names",
            "question": qtext,
            "options": ["A. Ben Novak", "B. Michael Archer", "C. Beth Shapiro", "D. George Church", "E. Svante Paabo"],
            "correctAnswer": ans,
        })
    t2_passages.append({"id": "cam15_t2_p2", "title": "Should We Try to Bring Extinct Species Back to Life?", "text": PASSAGES["t2_p2"]["text"], "timeRecommended": 20, "questions": t2_p2_qs})

    # Passage 3: Having a Laugh (Q27-40)
    t2_p3_qs = []
    # Q27-31: multiple_choice
    for i, ans in enumerate(["A", "A", "B", "B", "D"], 27):
        t2_p3_qs.append({
            "id": f"cam15_t2_r_q{i}",
            "type": "multiple_choice",
            "question": f"Question {i}: Choose the correct letter, A, B, C or D.",
            "options": ["A", "B", "C", "D"],
            "correctAnswer": ans,
        })
    # Q32-36: summary_completion with letter options A-I
    for i, (qtext, ans) in enumerate([
        ("Laughter is often linked to the experience of 32. _____", "F"),
        ("The quality of being 33. _____ is what makes humour effective", "H"),
        ("Some researchers argue that a 34. _____ joke cannot be truly funny", "C"),
        ("Humour can serve as a way to cope with feelings of 35. _____", "D"),
        ("People often find 36. _____ situations to be the most humorous", "E"),
    ], 32):
        t2_p3_qs.append({
            "id": f"cam15_t2_r_q{i}",
            "type": "summary_completion",
            "question": qtext,
            "options": ["A. unexpected", "B. emotional", "C. boring", "D. anxiety", "E. stimulating", "F. emotion", "G. surprise", "H. amusing", "I. connection"],
            "correctAnswer": ans,
        })
    # Q37-40: ynng
    t2_p3_qs.extend([
        {"id": "cam15_t2_r_q37", "type": "ynng", "question": "Laughter is primarily a response to jokes and humour.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
        {"id": "cam15_t2_r_q38", "type": "ynng", "question": "The ability to laugh evolved from social play behaviour in animals.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "YES"},
        {"id": "cam15_t2_r_q39", "type": "ynng", "question": "People who laugh frequently tend to have more friends.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "NO"},
        {"id": "cam15_t2_r_q40", "type": "ynng", "question": "Laughter has measurable physiological benefits.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "NO"},
    ])
    t2_passages.append({"id": "cam15_t2_p3", "title": "Having a Laugh", "text": PASSAGES["t2_p3"]["text"], "timeRecommended": 20, "questions": t2_p3_qs})

    tests.append({"id": "cam15_test2", "testNumber": 2, "passages": t2_passages})

    # ========== TEST 3 ==========
    t3_passages = []

    # Passage 1: Henry Moore (1898-1986) (Q1-13)
    t3_p1_qs = []
    # Q1-7: tfng
    t3_p1_qs.extend([
        {"id": "cam15_t3_r_q1", "type": "tfng", "question": "Henry Moore's father worked as a coal miner.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "TRUE"},
        {"id": "cam15_t3_r_q2", "type": "tfng", "question": "Moore was influenced by ancient Greek sculpture.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE"},
        {"id": "cam15_t3_r_q3", "type": "tfng", "question": "Moore's 'Shelter Drawings' were commissioned by the government.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
        {"id": "cam15_t3_r_q4", "type": "tfng", "question": "Moore is known for including empty spaces in his sculptures.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "TRUE"},
        {"id": "cam15_t3_r_q5", "type": "tfng", "question": "Moore preferred bronze over all other materials.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
        {"id": "cam15_t3_r_q6", "type": "tfng", "question": "Moore's sculptures were never displayed indoors.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE"},
        {"id": "cam15_t3_r_q7", "type": "tfng", "question": "The Henry Moore Foundation continues to support sculptors.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "TRUE"},
    ])
    # Q8-13: notes_completion - one word only
    for i, (qtext, ans) in enumerate([
        ("Moore submitted his 8. _____ from his teaching position at the Royal College", "resignation"),
        ("He experimented with a wide range of 9. _____", "materials"),
        ("His working-class background was reflected in his depictions of 10. _____", "miners"),
        ("Moore came from a large 11. _____", "family"),
        ("His works were purchased by wealthy 12. _____", "collectors"),
        ("Teaching provided a steady 13. _____ while he developed his art", "income"),
    ], 8):
        t3_p1_qs.append({"id": f"cam15_t3_r_q{i}", "type": "notes_completion", "question": qtext, "options": [], "correctAnswer": ans})
    t3_passages.append({"id": "cam15_t3_p1", "title": "Henry Moore (1898-1986)", "text": PASSAGES["t3_p1"]["text"], "timeRecommended": 20, "questions": t3_p1_qs})

    # Passage 2: The Desolenator (Q14-26)
    t3_p2_qs = []
    # Q14-20: matching_headings
    headings = [
        "i. Getting the finance for production",
        "ii. How existing water purification technologies compare",
        "iii. From initial inspiration to new product",
        "iv. The range of potential customers for the device",
        "v. What makes the device different from alternatives",
        "vi. Cleaning water from a range of sources",
        "vii. The environmental impact of desalination",
        "viii. Profit not the primary goal",
        "ix. The challenge of scaling up",
        "x. The number of people affected by water shortages",
    ]
    for i, ans in enumerate(["iii", "vi", "v", "x", "iv", "viii", "i"], 14):
        t3_p2_qs.append({"id": f"cam15_t3_r_q{i}", "type": "matching_headings", "question": f"Paragraph {chr(64+i-13)}", "options": headings, "correctAnswer": ans})
    # Q21-26: summary_completion - one word only
    for i, (qtext, ans) in enumerate([
        ("The device uses 21. _____ to move across the water surface", "wheels"),
        ("A protective 22. _____ prevents salt from damaging internal components", "film"),
        ("Water passes through a 23. _____ to remove particles before distillation", "filter"),
        ("The system produces very little 24. _____ material", "waste"),
        ("Solar intensity directly affects the device's 25. _____", "performance"),
        ("The company provides training for ongoing 26. _____ of the equipment", "servicing"),
    ], 21):
        t3_p2_qs.append({"id": f"cam15_t3_r_q{i}", "type": "summary_completion", "question": qtext, "options": [], "correctAnswer": ans})
    t3_passages.append({"id": "cam15_t3_p2", "title": "The Desolenator: Producing Clean Water", "text": PASSAGES["t3_p2"]["text"], "timeRecommended": 20, "questions": t3_p2_qs})

    # Passage 3: Why Fairy Tales are Really Scary Tales (Q27-40)
    t3_p3_qs = []
    # Q27-31: sentence_completion (A-F)
    for i, (qtext, ans) in enumerate([
        ("Fairy tales from different cultures tend to 27. _____", "C"),
        ("The frightening elements in traditional fairy tales 28. _____", "B"),
        ("The modern, sanitised versions of fairy tales 29. _____", "F"),
        ("Insights into the origins of fairy tales 30. _____", "A"),
        ("The earliest versions of many fairy tales 31. _____", "E"),
    ], 27):
        t3_p3_qs.append({
            "id": f"cam15_t3_r_q{i}",
            "type": "sentence_completion",
            "question": qtext,
            "options": ["A. may be provided through methods used in biological research", "B. are the reason for their survival", "C. show considerable global variation", "D. are more popular among adults than children", "E. were originally spoken rather than written", "F. have been developed without factual basis"],
            "correctAnswer": ans,
        })
    # Q32-36: summary_completion (A-I)
    for i, (qtext, ans) in enumerate([
        ("Scholars have studied the 32. _____ between different versions of the same tale", "D"),
        ("Regional 33. _____ in the telling of fairy tales reveal cultural differences", "F"),
        ("The 34. _____ described in fairy tales often reflect real historical concerns", "B"),
        ("Many tales served as a 35. _____ about genuine dangers children might face", "C"),
        ("The element of 36. _____ in these stories ensured children remained attentive", "G"),
    ], 32):
        t3_p3_qs.append({
            "id": f"cam15_t3_r_q{i}",
            "type": "summary_completion",
            "question": qtext,
            "options": ["A. characters", "B. events", "C. warning", "D. links", "E. animals", "F. variations", "G. horror", "H. tradition", "I. morality"],
            "correctAnswer": ans,
        })
    # Q37-40: multiple_choice
    for i, ans in enumerate(["B", "D", "A", "A"], 37):
        t3_p3_qs.append({
            "id": f"cam15_t3_r_q{i}",
            "type": "multiple_choice",
            "question": f"Question {i}: Choose the correct letter, A, B, C or D.",
            "options": ["A", "B", "C", "D"],
            "correctAnswer": ans,
        })
    t3_passages.append({"id": "cam15_t3_p3", "title": "Why Fairy Tales are Really Scary Tales", "text": PASSAGES["t3_p3"]["text"], "timeRecommended": 20, "questions": t3_p3_qs})

    tests.append({"id": "cam15_test3", "testNumber": 3, "passages": t3_passages})

    # ========== TEST 4 ==========
    t4_passages = []

    # Passage 1: The Return of the Huarango (Q1-13)
    t4_p1_qs = []
    # Q1-5: notes_completion - one word only
    for i, (qtext, ans) in enumerate([
        ("The huarango tree is adapted to thrive with very little 1. _____", "water"),
        ("The tree provided an important part of the local 2. _____", "diet"),
        ("Loss of the huarango increased the severity of 3. _____", "drought"),
        ("The tree's roots helped prevent soil 4. _____", "erosion"),
        ("Without the huarango, the land turned into 5. _____", "desert"),
    ], 1):
        t4_p1_qs.append({"id": f"cam15_t4_r_q{i}", "type": "notes_completion", "question": qtext, "options": [], "correctAnswer": ans})
    # Q6-8: notes_completion - no more than two words
    for i, (qtext, ans) in enumerate([
        ("The huarango's long roots could reach far below 6. _____", "(its) branches"),
        ("The tree provided 7. _____ that enriched the soil", "leaves (and) bark"),
        ("Moisture was stored in 8. _____ of the tree", "(its) trunk"),
    ], 6):
        t4_p1_qs.append({"id": f"cam15_t4_r_q{i}", "type": "notes_completion", "question": qtext, "options": [], "correctAnswer": ans})
    # Q9-13: tfng
    t4_p1_qs.extend([
        {"id": "cam15_t4_r_q9", "type": "tfng", "question": "The huarango tree was once found throughout South America.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
        {"id": "cam15_t4_r_q10", "type": "tfng", "question": "Cotton farming had little effect on the huarango population.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE"},
        {"id": "cam15_t4_r_q11", "type": "tfng", "question": "Local farmers have participated in the huarango restoration project.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "TRUE"},
        {"id": "cam15_t4_r_q12", "type": "tfng", "question": "The huarango has been successfully reintroduced to all of its former range.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE"},
        {"id": "cam15_t4_r_q13", "type": "tfng", "question": "Traditional farming methods are always compatible with huarango conservation.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
    ])
    t4_passages.append({"id": "cam15_t4_p1", "title": "The Return of the Huarango", "text": PASSAGES["t4_p1"]["text"], "timeRecommended": 20, "questions": t4_p1_qs})

    # Passage 2: Silbo Gomero (Q14-26)
    t4_p2_qs = []
    # Q14-19: tfng
    t4_p2_qs.extend([
        {"id": "cam15_t4_r_q14", "type": "tfng", "question": "Silbo Gomero is easier to learn for children than for adults.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
        {"id": "cam15_t4_r_q15", "type": "tfng", "question": "Silbo Gomero can only be used to communicate simple messages.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE"},
        {"id": "cam15_t4_r_q16", "type": "tfng", "question": "The geography of La Gomera was a factor in the development of Silbo Gomero.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "TRUE"},
        {"id": "cam15_t4_r_q17", "type": "tfng", "question": "Silbo Gomero is based on the indigenous language of the Canary Islands.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE"},
        {"id": "cam15_t4_r_q18", "type": "tfng", "question": "The invention of the telephone made Silbo Gomero completely obsolete.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE"},
        {"id": "cam15_t4_r_q19", "type": "tfng", "question": "Silbo Gomero is now taught in schools on La Gomera.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "TRUE"},
    ])
    # Q20-26: notes_completion - one word only
    for i, (qtext, ans) in enumerate([
        ("The whistled language is used to represent spoken Spanish 20. _____", "words"),
        ("The whistler uses one 21. _____ to produce different tones", "finger"),
        ("The 22. _____ of the whistle can indicate the meaning of the message", "direction"),
        ("Silbo Gomero was traditionally used to convey simple 23. _____", "commands"),
        ("It was particularly useful for warning of approaching 24. _____", "fires"),
        ("Modern 25. _____ has reduced the practical need for the whistled language", "technology"),
        ("UNESCO gave the language an important cultural 26. _____", "award"),
    ], 20):
        t4_p2_qs.append({"id": f"cam15_t4_r_q{i}", "type": "notes_completion", "question": qtext, "options": [], "correctAnswer": ans})
    t4_passages.append({"id": "cam15_t4_p2", "title": "Silbo Gomero - the Whistle 'Language' of the Canary Islands", "text": PASSAGES["t4_p2"]["text"], "timeRecommended": 20, "questions": t4_p2_qs})

    # Passage 3: Environmental Practices of Big Businesses (Q27-40)
    t4_p3_qs = []
    # Q27-31: summary_completion (A-I)
    for i, (qtext, ans) in enumerate([
        ("Some corporations have genuinely adopted higher 27. _____ in their operations", "D"),
        ("However, others resist external 28. _____ over their environmental impact", "E"),
        ("Meaningful environmental 29. _____ requires commitment from senior management", "F"),
        ("One industry particularly criticised for its practices is 30. _____", "H"),
        ("Companies that plant 31. _____ to offset emissions may still cause environmental harm", "B"),
    ], 27):
        t4_p3_qs.append({
            "id": f"cam15_t4_r_q{i}",
            "type": "summary_completion",
            "question": qtext,
            "options": ["A. regulations", "B. trees", "C. transparency", "D. moral standards", "E. control", "F. involvement", "G. reporting", "H. overfishing", "I. innovation"],
            "correctAnswer": ans,
        })
    # Q32-34: multiple_choice
    for i, ans in enumerate(["C", "D", "B"], 32):
        t4_p3_qs.append({
            "id": f"cam15_t4_r_q{i}",
            "type": "multiple_choice",
            "question": f"Question {i}: Choose the correct letter, A, B, C or D.",
            "options": ["A", "B", "C", "D"],
            "correctAnswer": ans,
        })
    # Q35-39: ynng
    t4_p3_qs.extend([
        {"id": "cam15_t4_r_q35", "type": "ynng", "question": "Companies that voluntarily adopt environmental policies are more successful than those that do not.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "YES"},
        {"id": "cam15_t4_r_q36", "type": "ynng", "question": "Most consumers are willing to pay more for environmentally friendly products.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
        {"id": "cam15_t4_r_q37", "type": "ynng", "question": "Government regulation is sufficient to ensure good environmental practices in business.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "NO"},
        {"id": "cam15_t4_r_q38", "type": "ynng", "question": "Companies that genuinely commit to sustainability can benefit financially.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "YES"},
        {"id": "cam15_t4_r_q39", "type": "ynng", "question": "Small businesses are generally more environmentally responsible than large corporations.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
    ])
    # Q40: multiple_choice - best subheading
    t4_p3_qs.append({
        "id": "cam15_t4_r_q40",
        "type": "multiple_choice",
        "question": "Which of the following is the best subheading for the passage?",
        "options": ["A. The limits of corporate sustainability", "B. How to make businesses greener", "C. Why consumers should boycott unethical companies", "D. Measuring corporate environmental commitment"],
        "correctAnswer": "D",
    })
    t4_passages.append({"id": "cam15_t4_p3", "title": "Environmental Practices of Big Businesses", "text": PASSAGES["t4_p3"]["text"], "timeRecommended": 20, "questions": t4_p3_qs})

    tests.append({"id": "cam15_test4", "testNumber": 4, "passages": t4_passages})

    return {"id": "cam15", "title": "Cambridge IELTS 15 Academic Reading", "tests": tests}


###############################################################################
# LISTENING DATA
###############################################################################

def make_listening():
    tests = []

    # ========== LISTENING TEST 1 ==========
    lt1_parts = []

    # Part 1: Bankside Recruitment Agency (Q1-10)
    lt1_p1_qs = []
    for i, (qtext, ans) in enumerate([
        ("1. Surname: _____", "Jamieson"),
        ("2. Preferred time: _____", "afternoon"),
        ("3. Good at: _____", "communication"),
        ("4. Available from: next _____", "week"),
        ("5. Experience: _____ years", "10"),
        ("6. Need to have a _____", "suit"),
        ("7. Must bring: _____", "passport"),
        ("8. Important quality: _____", "personality"),
        ("9. They will provide: _____", "feedback"),
        ("10. Interview duration: one hour and the candidate arrived on _____", "time"),
    ], 1):
        lt1_p1_qs.append({"id": f"cam15_lt1_q{i}", "type": "notes_completion", "question": qtext, "options": [], "correctAnswer": ans})
    lt1_parts.append({"id": "cam15_lt1_p1", "title": "Bankside Recruitment Agency", "audioFile": "cam15_test1_part1.mp3", "subtitle": "", "duration": "", "questions": lt1_p1_qs})

    # Part 2: Matthews Island Holidays (Q11-20)
    lt1_p2_qs = []
    for i, ans in enumerate(["A", "B", "A", "C"], 11):
        lt1_p2_qs.append({"id": f"cam15_lt1_q{i}", "type": "multiple_choice", "question": f"Question {i}: Choose the correct letter, A, B or C.", "options": ["A", "B", "C"], "correctAnswer": ans})
    for i, (qtext, ans) in enumerate([
        ("15. The holiday company recommends taking a trip along the _____", "river"),
        ("16. The hotel room number is _____", "1422"),
        ("17. Guests should meet at the _____ of the hotel for excursions", "top"),
        ("18. Visitors need to show their _____ to get discounts on boat trips", "pass"),
        ("19. The island's transport includes a _____ railway", "steam"),
        ("20. The tour includes a visit to the _____ city", "capital"),
    ], 15):
        lt1_p2_qs.append({"id": f"cam15_lt1_q{i}", "type": "notes_completion", "question": qtext, "options": [], "correctAnswer": ans})
    lt1_parts.append({"id": "cam15_lt1_p2", "title": "Matthews Island Holidays", "audioFile": "cam15_test1_part2.mp3", "subtitle": "", "duration": "", "questions": lt1_p2_qs})

    # Part 3: Birth Order and Personality (Q21-30)
    lt1_p3_qs = []
    for i, (qtext, ans) in enumerate([
        ("21. the oldest children", "G"),
        ("22. the middle children", "F"),
        ("23. the youngest children", "A"),
        ("24. twins", "E"),
        ("25. only children", "B"),
        ("26. children with much older siblings", "C"),
    ], 21):
        lt1_p3_qs.append({
            "id": f"cam15_lt1_q{i}",
            "type": "matching",
            "question": qtext,
            "options": ["A. tend to be creative and attention-seeking", "B. often behave like adults from an early age",
                         "C. may feel overshadowed by their siblings", "D. are usually very organised and responsible",
                         "E. develop strong negotiation skills", "F. are often mediators in family conflicts",
                         "G. are typically confident and achievement-oriented"],
            "correctAnswer": ans,
        })
    for i, ans in enumerate(["C", "A", "B", "D"], 27):
        lt1_p3_qs.append({"id": f"cam15_lt1_q{i}", "type": "multiple_choice", "question": f"Question {i}: Choose the correct letter, A, B, C or D.", "options": ["A", "B", "C", "D"], "correctAnswer": ans})
    lt1_parts.append({"id": "cam15_lt1_p3", "title": "Birth Order and Personality", "audioFile": "cam15_test1_part3.mp3", "subtitle": "", "duration": "", "questions": lt1_p3_qs})

    # Part 4: Eucalyptus Trees (Q31-40)
    lt1_p4_qs = []
    for i, ans in enumerate(["shelter", "oil", "roads", "insects", "grass", "water", "nutrients", "dry", "simple", "nests"], 31):
        lt1_p4_qs.append({"id": f"cam15_lt1_q{i}", "type": "notes_completion", "question": f"Question {i}: ONE WORD ONLY.", "options": [], "correctAnswer": ans})
    lt1_parts.append({"id": "cam15_lt1_p4", "title": "Eucalyptus Trees", "audioFile": "cam15_test1_part4.mp3", "subtitle": "", "duration": "", "questions": lt1_p4_qs})

    tests.append({"id": "cam15_listening_test1", "testNumber": 1, "parts": lt1_parts})

    # ========== LISTENING TEST 2 ==========
    lt2_parts = []

    # Part 1: Festival Information (Q1-10)
    lt2_p1_qs = []
    for i, (qtext, ans) in enumerate([
        ("1. Name of the festival: _____", "Eustatis"),
        ("2. The organiser asks for a _____ of the event", "review"),
        ("3. Type of performance: _____", "dance"),
        ("4. Communication platform: _____", "Chat"),
        ("5. Food available: _____ options", "healthy"),
        ("6. They need to put up _____", "posters"),
        ("7. Stage material: _____", "wood"),
        ("8. Activities near the _____", "lake"),
        ("9. Problem with: _____", "insects"),
        ("10. More details on the _____", "blog"),
    ], 1):
        lt2_p1_qs.append({"id": f"cam15_lt2_q{i}", "type": "notes_completion", "question": qtext, "options": [], "correctAnswer": ans})
    lt2_parts.append({"id": "cam15_lt2_p1", "title": "Festival Information", "audioFile": "cam15_test2_part1.mp3", "subtitle": "", "duration": "", "questions": lt2_p1_qs})

    # Part 2: Minster Park (Q11-20)
    lt2_p2_qs = []
    for i, ans in enumerate(["C", "A", "B", "C"], 11):
        lt2_p2_qs.append({"id": f"cam15_lt2_q{i}", "type": "multiple_choice", "question": f"Question {i}: Choose the correct letter, A, B or C.", "options": ["A", "B", "C"], "correctAnswer": ans})
    for i, ans in enumerate(["E", "C", "B", "A", "G", "D"], 15):
        lt2_p2_qs.append({"id": f"cam15_lt2_q{i}", "type": "matching", "question": f"Match the location on the map (items 15-20) to the correct letter.", "options": ["A", "B", "C", "D", "E", "F", "G", "H"], "correctAnswer": ans})
    lt2_parts.append({"id": "cam15_lt2_p2", "title": "Minster Park", "audioFile": "cam15_test2_part2.mp3", "subtitle": "", "duration": "", "questions": lt2_p2_qs})

    # Part 3: Dickens Display (Q21-30)
    lt2_p3_qs = []
    lt2_p3_qs.append({"id": "cam15_lt2_q21", "type": "multiple_choice_multi", "question": "Which TWO groups of people is the Dickens display aimed at?\nA. school children\nB. local residents\nC. overseas tourists\nD. potential new students\nE. academic researchers", "options": ["A", "B", "C", "D", "E"], "correctAnswer": "B, D"})
    lt2_p3_qs.append({"id": "cam15_lt2_q22", "type": "multiple_choice_multi", "question": "Which TWO types of items are included in the display?\nA. original letters\nB. social problems publications\nC. well-known novels\nD. personal photographs\nE. film adaptations", "options": ["A", "B", "C", "D", "E"], "correctAnswer": "B, C"})
    for i, (qtext, ans) in enumerate([
        ("25. Pickwick Papers", "G"),
        ("26. Oliver Twist", "B"),
        ("27. Nicholas Nickleby", "D"),
        ("28. Martin Chuzzlewit", "C"),
        ("29. Bleak House", "H"),
        ("30. Little Dorrit", "F"),
    ], 25):
        lt2_p3_qs.append({
            "id": f"cam15_lt2_q{i}",
            "type": "matching",
            "question": qtext,
            "options": ["A. poverty", "B. education", "C. Dickens's travels", "D. entertainment", "E. crime", "F. wealth", "G. medicine", "H. a woman's life"],
            "correctAnswer": ans,
        })
    lt2_parts.append({"id": "cam15_lt2_p3", "title": "Dickens Display", "audioFile": "cam15_test2_part3.mp3", "subtitle": "", "duration": "", "questions": lt2_p3_qs})

    # Part 4: Agricultural Programme in Mozambique (Q31-40)
    lt2_p4_qs = []
    for i, ans in enumerate(["Irrigation", "women", "wire(s)", "seed(s)", "posts", "transport", "preservation", "fish(es)", "bees", "design"], 31):
        lt2_p4_qs.append({"id": f"cam15_lt2_q{i}", "type": "notes_completion", "question": f"Question {i}: ONE WORD ONLY.", "options": [], "correctAnswer": ans})
    lt2_parts.append({"id": "cam15_lt2_p4", "title": "Agricultural Programme in Mozambique", "audioFile": "cam15_test2_part4.mp3", "subtitle": "", "duration": "", "questions": lt2_p4_qs})

    tests.append({"id": "cam15_listening_test2", "testNumber": 2, "parts": lt2_parts})

    # ========== LISTENING TEST 3 ==========
    lt3_parts = []

    # Part 1: Employment Agency (Possible Jobs) (Q1-10)
    lt3_p1_qs = []
    for i, (qtext, ans) in enumerate([
        ("1. First job involves moving _____", "furniture"),
        ("2. Must be good at organising _____", "meetings"),
        ("3. Must keep a _____", "diary"),
        ("4. Must pay attention to _____", "detail"),
        ("5. Length of contract: _____", "1 year"),
        ("6. Job involves helping with _____", "deliveries"),
        ("7. Must keep the office _____", "tidy"),
        ("8. Must be able to work in a _____", "team"),
        ("9. Must be able to lift _____ items", "heavy"),
        ("10. Must enjoy dealing with the _____", "customer"),
    ], 1):
        lt3_p1_qs.append({"id": f"cam15_lt3_q{i}", "type": "notes_completion", "question": qtext, "options": [], "correctAnswer": ans})
    lt3_parts.append({"id": "cam15_lt3_p1", "title": "Employment Agency (Possible Jobs)", "audioFile": "cam15_test3_part1.mp3", "subtitle": "", "duration": "", "questions": lt3_p1_qs})

    # Part 2: Street Play Scheme (Q11-20)
    lt3_p2_qs = []
    for i, ans in enumerate(["B", "A", "C", "B", "C", "B"], 11):
        lt3_p2_qs.append({"id": f"cam15_lt3_q{i}", "type": "multiple_choice", "question": f"Question {i}: Choose the correct letter, A, B or C.", "options": ["A", "B", "C"], "correctAnswer": ans})
    lt3_p2_qs.append({"id": "cam15_lt3_q17", "type": "multiple_choice_multi", "question": "Which TWO benefits of the Street Play scheme for children are mentioned?\nA. better physical fitness\nB. independence\nC. improved social skills\nD. part of a community\nE. less screen time", "options": ["A", "B", "C", "D", "E"], "correctAnswer": "B, D"})
    lt3_p2_qs.append({"id": "cam15_lt3_q18", "type": "multiple_choice_multi", "question": "Which TWO benefits of the Street Play scheme for the local area are mentioned?\nA. more shoppers\nB. lower crime rates\nC. better air quality\nD. stronger community spirit\nE. less noise pollution", "options": ["A", "B", "C", "D", "E"], "correctAnswer": "A, E"})
    lt3_parts.append({"id": "cam15_lt3_p2", "title": "Street Play Scheme", "audioFile": "cam15_test3_part2.mp3", "subtitle": "", "duration": "", "questions": lt3_p2_qs})

    # Part 3: Media Studies Assignment (Q21-30)
    lt3_p3_qs = []
    for i, (qtext, ans) in enumerate([
        ("21. The design of the magazine _____", "page"),
        ("22. The _____ of the publication", "size"),
        ("23. Use of _____ in the layout", "graphics"),
        ("24. The _____ of the articles", "structure"),
        ("25. The _____ of the writing", "purpose"),
        ("26. The _____ the author makes", "assumptions"),
    ], 21):
        lt3_p3_qs.append({"id": f"cam15_lt3_q{i}", "type": "notes_completion", "question": qtext, "options": [], "correctAnswer": ans})
    for i, (qtext, ans) in enumerate([
        ("27. national news: the student will definitely look at this", "A"),
        ("28. editorial: the student will not bother with this", "C"),
        ("29. human interest: the student will avoid this", "C"),
        ("30. arts: the student may choose this", "B"),
    ], 27):
        lt3_p3_qs.append({
            "id": f"cam15_lt3_q{i}",
            "type": "matching",
            "question": qtext,
            "options": ["A. will definitely look", "B. may choose", "C. will not bother", "D. undecided"],
            "correctAnswer": ans,
        })
    lt3_parts.append({"id": "cam15_lt3_p3", "title": "Media Studies Assignment", "audioFile": "cam15_test3_part3.mp3", "subtitle": "", "duration": "", "questions": lt3_p3_qs})

    # Part 4: Early History of Keeping Clean (Q31-40)
    lt3_p4_qs = []
    for i, ans in enumerate(["mud", "clay", "metal", "hair", "baths", "disease(s)", "perfume", "salt", "science", "tax"], 31):
        lt3_p4_qs.append({"id": f"cam15_lt3_q{i}", "type": "notes_completion", "question": f"Question {i}: ONE WORD ONLY.", "options": [], "correctAnswer": ans})
    lt3_parts.append({"id": "cam15_lt3_p4", "title": "Early History of Keeping Clean", "audioFile": "cam15_test3_part4.mp3", "subtitle": "", "duration": "", "questions": lt3_p4_qs})

    tests.append({"id": "cam15_listening_test3", "testNumber": 3, "parts": lt3_parts})

    # ========== LISTENING TEST 4 ==========
    lt4_parts = []

    # Part 1: Customer Satisfaction Survey (Q1-10)
    lt4_p1_qs = []
    for i, (qtext, ans) in enumerate([
        ("1. Occupation: _____", "journalist"),
        ("2. Reason for visit: _____", "shopping"),
        ("3. Name of store: _____", "Staunfirth"),
        ("4. Willing to _____", "return"),
        ("5. Total spent: £_____", "23.70"),
        ("6. Preferred shopping method: _____", "online"),
        ("7. Complaint about: _____", "delay"),
        ("8. Need more: _____", "information"),
        ("9. Suggestion about _____", "platforms"),
        ("10. Problem with: _____", "parking"),
    ], 1):
        lt4_p1_qs.append({"id": f"cam15_lt4_q{i}", "type": "notes_completion", "question": qtext, "options": [], "correctAnswer": ans})
    lt4_parts.append({"id": "cam15_lt4_p1", "title": "Customer Satisfaction Survey", "audioFile": "cam15_test4_part1.mp3", "subtitle": "", "duration": "", "questions": lt4_p1_qs})

    # Part 2: Croft Valley Park (Q11-20)
    lt4_p2_qs = []
    for i, ans in enumerate(["D", "C", "G", "H", "A", "E"], 11):
        lt4_p2_qs.append({"id": f"cam15_lt4_q{i}", "type": "matching", "question": f"Match the location on the park map (items 11-16) to the correct letter.", "options": ["A", "B", "C", "D", "E", "F", "G", "H"], "correctAnswer": ans})
    lt4_p2_qs.append({"id": "cam15_lt4_q17", "type": "multiple_choice_multi", "question": "Which TWO features of the adventure playground are mentioned?\nA. supervised at all times\nB. suitable for all ages\nC. has a separate toddler area\nD. free to use\nE. booking required", "options": ["A", "B", "C", "D", "E"], "correctAnswer": "A, D"})
    lt4_p2_qs.append({"id": "cam15_lt4_q18", "type": "multiple_choice_multi", "question": "Which TWO facts are given about the glass houses?\nA. closed at weekends\nB. admission charge\nC. damaged by fire\nD. originally used for growing fruit\nE. built in the 19th century", "options": ["A", "B", "C", "D", "E"], "correctAnswer": "A, C"})
    lt4_parts.append({"id": "cam15_lt4_p2", "title": "Croft Valley Park", "audioFile": "cam15_test4_part2.mp3", "subtitle": "", "duration": "", "questions": lt4_p2_qs})

    # Part 3: Presentation about Refrigeration (Q21-30)
    lt4_p3_qs = []
    for i, ans in enumerate(["B", "A", "B", "A"], 21):
        lt4_p3_qs.append({"id": f"cam15_lt4_q{i}", "type": "multiple_choice", "question": f"Question {i}: Choose the correct letter, A, B or C.", "options": ["A", "B", "C"], "correctAnswer": ans})
    for i, (qtext, ans) in enumerate([
        ("25. goods that are refrigerated", "A"),
        ("26. effects on health", "A"),
        ("27. impact on food producers", "B"),
        ("28. impact on cities", "B"),
        ("29. refrigerated transport", "A"),
        ("30. domestic fridges", "C"),
    ], 25):
        lt4_p3_qs.append({
            "id": f"cam15_lt4_q{i}",
            "type": "matching",
            "question": qtext,
            "options": ["A. Annie", "B. Jack", "C. Both"],
            "correctAnswer": ans,
        })
    lt4_parts.append({"id": "cam15_lt4_p3", "title": "Presentation about Refrigeration", "audioFile": "cam15_test4_part3.mp3", "subtitle": "", "duration": "", "questions": lt4_p3_qs})

    # Part 4: Industrial Revolution in Britain (Q31-40)
    lt4_p4_qs = []
    for i, ans in enumerate(["wealth", "technology", "power", "textile(s)", "machines", "newspapers", "local", "lighting", "windows", "advertising"], 31):
        lt4_p4_qs.append({"id": f"cam15_lt4_q{i}", "type": "notes_completion", "question": f"Question {i}: ONE WORD ONLY.", "options": [], "correctAnswer": ans})
    lt4_parts.append({"id": "cam15_lt4_p4", "title": "Industrial Revolution in Britain", "audioFile": "cam15_test4_part4.mp3", "subtitle": "", "duration": "", "questions": lt4_p4_qs})

    tests.append({"id": "cam15_listening_test4", "testNumber": 4, "parts": lt4_parts})

    return {"id": "cam15", "title": "Cambridge IELTS 15 Academic Listening", "tests": tests}


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
