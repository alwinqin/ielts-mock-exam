#!/usr/bin/env python3
"""Generate cam20 reading.json and listening.json with complete data."""

import json
import os

OUT_DIR = "data/cambridge/cam20"

###############################################################################
# PASSAGE TEXTS (descriptive summaries)
###############################################################################

PASSAGES = {
    # TEST 1
    "t1_p1": {
        "title": "The Kakapo",
        "text": "The Kakapo is a flightless, nocturnal parrot native to New Zealand. Once widespread across the North and South Islands, the species has been pushed to the brink of extinction due to habitat destruction and predation by introduced mammals including stoats, cats, rats, and possums. The kakapo possesses several unique traits: it is the world's heaviest parrot, it cannot fly, and it has a distinct musky odour. Males produce a low-frequency booming call during the breeding season that can travel several kilometres through the forest. The species' unusual biology and behaviour have made it a subject of intense scientific interest.\n\nConservation efforts for the kakapo have been underway for decades, with the Kakapo Recovery Programme established to protect remaining individuals. The programme has relocated surviving birds to predator-free offshore islands where they receive intensive management including supplementary feeding, nest monitoring, and artificial incubation. However, the recovery has faced significant challenges. The kakapo population suffers from extremely low genetic diversity, and breeding is closely tied to the intermittent fruiting of native rimu trees, which only occurs every two to four years. These constraints have limited the speed at which the population can grow.\n\nThe recovery programme involves collaboration between government agencies, conservation organisations, local communities, and iwi (Maori tribes). Funding has been a persistent concern, as the intensive management required for each bird is costly. Researchers and conservationists continue to develop new strategies to support the kakapo's recovery, including advances in artificial insemination, smart nest monitoring technology, and genetic management. The long-term goal remains the establishment of a self-sustaining kakapo population that can survive without intensive human intervention.",
    },
    "t1_p2": {
        "title": "Bringing Elms Back to Britain (Return of the Elm)",
        "text": "Dutch elm disease devastated Britain's elm population during the second half of the 20th century, killing an estimated 25 million trees and transforming the character of the British countryside and urban landscapes. The disease is caused by a fungus (Ophiostoma novo-ulmi) that is spread by elm bark beetles. The fungus blocks the tree's water-conducting vessels, causing wilting and rapid death. For decades, it seemed that the majestic English elm, which had been a defining feature of the landscape for centuries, would become little more than a memory.\n\nHowever, a small number of elms survived the epidemic. Some of these survivors had grown in isolation, far from the bark beetles that spread the fungus. Others appeared to possess a degree of natural resistance to the disease. Researchers and conservationists launched a project to locate, document, and propagate these surviving elms. By collecting cuttings from the hardiest mature trees, they have been able to clone them and grow new saplings. Some of the most promising specimens have been planted in trial sites across the country to assess their long-term resilience. These efforts aim to restore the elm to its place in the British landscape.\n\nThe project has involved collaboration between botanical gardens, university researchers, and local conservation groups. The work has progressed methodically: identifying candidate trees, testing their resistance to the fungus, establishing clonal orchards, and eventually replanting in suitable locations. While a full-scale return of the elm remains a long-term aspiration, the results so far have been encouraging. The effort also carries broader significance as a model for how societies might respond to large-scale ecological losses and attempt to restore species that have been virtually lost from the landscape.",
    },
    "t1_p3": {
        "title": "How Stress Affects Our Judgement",
        "text": "Scientific research has increasingly demonstrated that stress fundamentally alters the way people make decisions and judge situations. When individuals are under acute or chronic stress, their cognitive processes shift in predictable ways. Studies have found that stressed individuals tend to focus on short-term outcomes while discounting long-term consequences, take greater risks, and show reduced ability to weigh evidence objectively. This has important implications for everything from personal financial decisions to professional performance in high-stakes environments.\n\nNeurobiologically, stress triggers the release of hormones such as cortisol and adrenaline, which affect brain function. The prefrontal cortex, which governs higher-order reasoning, impulse control, and rational decision-making, becomes less active under stress. At the same time, brain regions associated with emotional responses and habitual behaviour become more dominant. This neurological shift helps explain why stressed individuals may behave impulsively, rely on mental shortcuts, or make choices that seem irrational in hindsight. Research also suggests that the effects of stress on judgement can persist even after the stressful situation has passed.\n\nThe implications of this research extend across multiple domains. In healthcare, stressed medical professionals may be more prone to diagnostic errors. In finance, stressed investors may make poor trading decisions. In everyday life, people under stress may misjudge social situations or make unwise personal choices. Understanding the mechanisms through which stress impairs judgement has become an important area of psychological and neurological research, with potential applications in workplace design, education, and public policy aimed at reducing the harmful effects of stress on decision-making.",
    },
    # TEST 2
    "t2_p1": {
        "title": "Manatees",
        "text": "Manatees, also known as sea cows, are large, slow-moving marine mammals belonging to the order Sirenia. They inhabit the warm coastal waters, rivers, and springs of the Caribbean Sea, the Gulf of Mexico, the Amazon Basin, and West Africa. Three species exist: the West Indian manatee, the Amazonian manatee, and the West African manatee. These gentle herbivores can grow up to four metres in length and weigh over 1,500 kilograms. Their anatomy is uniquely adapted to an aquatic lifestyle, with a large, rounded tail for propulsion, powerful flippers for steering and manoeuvring, and a flexible, prehensile upper lip that is split in the middle and used for grasping vegetation.\n\nManatees feed primarily on seagrasses and other aquatic plants, consuming up to 10 percent of their body weight daily. Their slow metabolism means they are adapted to warm waters, and they must migrate to heated areas such as natural springs during cold weather. Manatees have small, widely spaced eyes with limited vision, but they compensate with excellent hearing and sensitive body hair that may detect vibrations in the water. Their teeth are continuously replaced throughout their lives as the front ones wear down from grinding vegetation. They communicate through a range of vocalisations including squeaks and chirps.\n\nManatees face numerous threats from human activity. Collisions with boats and ships are a leading cause of injury and death, as manatees are slow-moving and spend much of their time near the surface. They also suffer from entanglement in fishing gear, habitat destruction due to coastal development, and cold stress as warm-water refuges become scarcer. Conservation measures have included boat speed restrictions in manatee habitats, the establishment of protected areas and sanctuaries, rescue and rehabilitation programmes for injured animals, and public education campaigns. While some populations have shown signs of recovery, the species remains vulnerable and dependent on continued conservation efforts.",
    },
    "t2_p2": {
        "title": "Procrastination",
        "text": "Procrastination, the voluntary delay of an intended task despite expecting to be worse off for the delay, affects a large proportion of the population. It is estimated that around 15 to 20 percent of adults engage in chronic procrastination, with even higher rates among students and young adults. Procrastination has been linked to negative outcomes including lower academic achievement, reduced career success, poorer financial management, and diminished psychological well-being. Despite the obvious costs of delaying important tasks, the behaviour remains stubbornly persistent.\n\nPsychological research has reshaped our understanding of procrastination. Far from being simply a time-management problem or a matter of laziness, procrastination is now understood as a problem of emotional regulation. People delay tasks not because they cannot organise their time, but because the tasks trigger negative feelings such as anxiety, boredom, or self-doubt, and putting them off provides temporary relief. This perspective explains why procrastination is strongly correlated with personality traits such as high impulsivity and low conscientiousness, and with conditions such as anxiety and depression.\n\nResearch has identified a range of strategies that can help reduce procrastination. One effective approach involves self-forgiveness — acknowledging past procrastination without self-blame, which reduces the guilt that can fuel further avoidance. Breaking tasks into smaller, manageable steps and reducing distractions in the environment have also been shown to help. Identifying the specific fears or threats that trigger avoidance can allow individuals to address the underlying emotional obstacles. The most successful interventions tend to combine cognitive behavioural techniques with practical strategies for managing the immediate environment.",
    },
    "t2_p3": {
        "title": "Invasion of the Robot Umpires",
        "text": "Technology is increasingly being deployed to assist or replace human officials in professional sports, a development that has provoked both enthusiasm and controversy. In tennis, the Hawk-Eye system tracks ball trajectories using multiple cameras to determine whether a shot is in or out with an accuracy far exceeding human perception. In cricket, similar ball-tracking technology is used for leg-before-wicket decisions. In baseball, automated strike-zone systems have been introduced in some leagues to call balls and strikes. These systems promise greater accuracy, consistency, and fairness, removing the human error that can decide the outcome of crucial matches.\n\nHowever, the invasion of robot umpires has generated significant debate about the nature of sport itself. Critics argue that human officiating, with all its imperfections, is part of the fabric of athletic competition. The judgement calls made by referees and umpires, the strategic considerations that arise from knowing a call might go either way, and even the occasional controversial decision that becomes part of sporting lore are, for many fans, inseparable from the experience of watching sport. There are also concerns about the cost and accessibility of such technologies, which may create a two-tier system where elite competitions benefit from advanced technology while lower-level games do not.\n\nProponents counter that athletes and fans deserve the most accurate decisions possible, and that the purity of competition is better served by getting calls right than by preserving tradition. They point to the growing number of disputes over calls in fast-paced modern sports and argue that technology can resolve ambiguities that human officials cannot. The debate continues over where to draw the line: should technology simply assist officials, or should it have the final word? Different sports and leagues have arrived at different answers, and the conversation remains active as technology continues to advance.",
    },
    # TEST 3
    "t3_p1": {
        "title": "Frozen Food",
        "text": "The development of frozen food technology in the early 20th century revolutionised the global food industry. The American inventor Clarence Birdseye is credited as the pioneer of modern frozen food after observing that fish caught in Arctic waters froze rapidly in the extreme cold and retained their freshness and flavour when thawed. He developed the quick-freezing process, which involved pressing packaged food between refrigerated metal plates at very low temperatures. This rapid freezing prevented the formation of large ice crystals that would puncture cell walls and damage the food's texture, flavour, and nutritional value. Birdseye's innovations led to the founding of what became a global frozen food empire.\n\nThe frozen food industry grew rapidly as technology improved and infrastructure expanded. Early products included frozen vegetables such as peas and potatoes, as well as fish, meat, fruit, and prepared meals. Packaging evolved from waxed paper and cardboard to moisture-proof materials such as cellophane, and later to boil-in-bag pouches and microwave-safe containers. The development of the home refrigerator and freezer was critical to the industry's success, as consumers needed a way to store frozen products. Tin cans and other containers were also important in the processing and storage of frozen foods.\n\nThe impact of frozen food on everyday life has been profound. It has enabled households to store a wide variety of foods for extended periods, reducing food waste and the need for frequent shopping. It has transformed eating habits by making seasonal foods available year-round and by enabling the creation of ready meals that require minimal preparation. The global supply chain for frozen food now spans continents, with specialised refrigerated transport and storage facilities ensuring that products reach consumers in optimal condition. Despite ongoing debates about nutritional quality and processing, frozen food remains a staple of modern diets around the world.",
    },
    "t3_p2": {
        "title": "Can the Planet's Coral Reefs Be Saved?",
        "text": "Coral reefs are among the most biodiverse and productive ecosystems on Earth, supporting an estimated 25 percent of all marine species despite covering less than one percent of the ocean floor. They provide food, coastal protection, and livelihoods for hundreds of millions of people worldwide. However, coral reefs are facing an existential crisis driven primarily by climate change. Rising sea temperatures cause mass coral bleaching events, in which corals expel the symbiotic algae (zooxanthellae) living in their tissues, turning white and becoming vulnerable to disease and death. Ocean acidification, caused by increased carbon dioxide absorption, further weakens coral skeletons and impairs growth.\n\nThe scale of the problem is staggering. Scientists estimate that half of the world's coral reefs have already been lost, and without urgent action, up to 90 percent could be gone by mid-century. Local stressors compound the global threats: pollution from agricultural runoff and coastal development, overfishing that disrupts reef ecosystems, and physical damage from tourism and boat anchors all contribute to reef degradation. The loss of coral reefs would have devastating consequences for marine biodiversity, fisheries, coastal communities, and economies that depend on reef tourism.\n\nIn response, scientists and conservation organisations are pursuing a range of interventions. Researchers are working to identify and propagate coral strains that show natural resistance to heat and bleaching, with the aim of restoring degraded reefs with hardier stock. Assisted gene flow and selective breeding programmes seek to enhance the resilience of coral populations. New techniques for speeding up coral reproduction, including larval propagation and microfragmentation, are being developed and tested. Marine protected areas, improved water quality management, and sustainable fishing practices all contribute to reef conservation. Ultimately, however, most experts agree that the long-term survival of coral reefs depends on rapid and substantial reductions in global carbon emissions.",
    },
    "t3_p3": {
        "title": "Robots and Us",
        "text": "The accelerating pace of advances in artificial intelligence and robotics has raised profound questions about the future relationship between humans and machines. Different experts bring sharply different perspectives to these questions. The astronomer and cosmologist Martin Rees has written extensively about the long-term trajectory of intelligence, both biological and electronic. He argues that machine intelligence is likely to surpass human capabilities in many domains within decades, and that this development could be as transformative as the emergence of life itself. Rees warns that we need to think carefully about the risks as well as the opportunities presented by advanced AI.\n\nKathleen Richardson, a professor of ethics and culture of robots and AI, brings a different perspective. She has raised ethical concerns about the development of robots designed for companionship and care, arguing that these technologies risk dehumanising relationships and may reflect troubling attitudes about human connection. Richardson suggests that the drive to create artificial companions may stem from a desire to control relationships rather than engage with the unpredictability and messiness of genuine human interaction. Her work highlights the social and ethical dimensions of robotics that are often overlooked in purely technical discussions.\n\nDaniel Wolpert, a neuroscientist, offers yet another viewpoint. He argues that the brain's primary purpose is to produce complex, adaptive movement, and that understanding how the human brain controls movement is essential to building truly intelligent and capable robots. Wolpert's research on motor control and the cerebellum suggests that many of the challenges in robotics — particularly those involving dexterity, balance, and interaction with the physical world — will only be solved by understanding the neural mechanisms that enable biological movement. Together, these diverse perspectives illustrate the complex interplay between technological capability, ethical consideration, and scientific understanding that will shape the future of humans and robots.",
    },
    # TEST 4
    "t4_p1": {
        "title": "Georgia O'Keeffe",
        "text": "Georgia O'Keeffe (1887-1986) was one of the most significant and influential American artists of the 20th century. Born in Wisconsin, she initially trained as a teacher before committing herself fully to a career as an artist. She studied at the Art Institute of Chicago and the Art Students League in New York, developing her skills in drawing and painting. Her early work, executed in charcoal and watercolour, demonstrated an original approach to abstraction that caught the attention of the prominent photographer and art dealer Alfred Stieglitz, who became her husband and greatest supporter.\n\nO'Keeffe is best known for her large-scale, close-up paintings of natural forms, particularly flowers, animal bones, and desert landscapes. During her time in New York, she also painted a series of works depicting skyscrapers, capturing the energy and verticality of the modern city. Later, she moved permanently to New Mexico, where she found lifelong inspiration in the dramatic desert landscape. Her paintings of bleached animal bones against vivid Southwestern skies, and her evocative representations of the region's rivers, mesas, and rock formations, became iconic images of American modernism.\n\nO'Keeffe's work is characterised by bold compositions, subtle gradations of colour, and a distinctive ability to transform ordinary natural subjects into powerful abstract forms. She rejected the labels and categories that critics and curators attempted to apply to her work, insisting on her independence as an artist. Over a career spanning more than six decades, she produced a body of work that continues to influence artists and captivate audiences worldwide. Her legacy includes not only her paintings but also her role in shaping the identity of American modern art and her enduring status as a pioneering female artist in a field dominated by men.",
    },
    "t4_p2": {
        "title": "Adapting to the Effects of Climate Change",
        "text": "As the impacts of climate change become increasingly visible and severe, communities around the world are being forced to adapt. Rising sea levels threaten coastal cities and low-lying islands; more frequent and intense extreme weather events — including hurricanes, floods, droughts, and heatwaves — are straining infrastructure and endangering lives; and shifts in temperature and precipitation patterns are disrupting agriculture and natural ecosystems. Adaptation has therefore become a central pillar of climate policy, alongside efforts to reduce greenhouse gas emissions.\n\nThe specific adaptation measures required vary greatly depending on local conditions. In coastal areas, cities are building sea walls, improving drainage systems with powerful pumps, and constructing dams and barriers to protect against storm surges. Some communities are experimenting with floating homes and buildings that can rise with floodwaters. In agriculture, researchers are developing crop varieties and tree species that are more resistant to drought, heat, and salt. Urban planners are redesigning cities with more green spaces, permeable surfaces, and improved water management systems to cope with heavier rainfall and higher temperatures.\n\nThe question of who bears responsibility for funding and implementing adaptation measures remains contentious. Some argue that governments must take the lead, given the scale of investment required. Others point to the role of international bodies in supporting vulnerable developing nations that have contributed least to climate change but face its worst effects. Individuals and businesses are also taking action, from retrofitting buildings to changing land management practices. The challenge is immense and the costs are high, but the alternative — failing to adapt — would be far more costly in both human and economic terms.",
    },
    "t4_p3": {
        "title": "Livestock Guard Dogs (A New Role for Livestock Guard Dogs)",
        "text": "Livestock guard dogs have been used for centuries to protect sheep, goats, and other herd animals from predators. Traditionally, these dogs were employed to defend against large carnivores such as wolves, bears, and coyotes. Breeds such as the Great Pyrenees, Anatolian Shepherd, and Maremma Sheepdog have been developed specifically for this purpose, possessing the size, strength, and territorial instincts needed to deter predators. These dogs live among the livestock, forming bonds with the animals they protect and using barking, posturing, and physical intervention to drive away threats.\n\nRecent research has expanded our understanding of what livestock guard dogs can achieve. Studies have shown that their presence does not simply protect livestock from large predators but also deters a wider range of smaller predators and scavengers including jackals and foxes. This has important ecological implications: by reducing the need for lethal predator control methods such as trapping and poisoning, guard dogs can contribute to the conservation of biodiversity. The dogs' constant presence and territorial behaviour create a zone of protection around livestock that also benefits other wildlife sharing the same landscape.\n\nHowever, the integration of guard dogs into farming systems requires careful management. Not all dogs are suited to the work; breed selection, early training, and the quality of the bond formed with the livestock are critical factors influencing success. There are also risks that need to be managed: guard dogs may themselves pose a threat to native wildlife if not properly trained and supervised, and their welfare must be ensured through appropriate veterinary care and working conditions. Nevertheless, for many farmers and conservationists, the use of livestock guard dogs represents a practical and ecologically sound alternative to conventional predator management.",
    },
}

###############################################################################
# READING QUESTIONS
###############################################################################

def make_reading():
    tests = []

    # ========== TEST 1 ==========
    t1_passages = []

    # Passage 1: The Kakapo (Q1-13)
    t1_p1_qs = []
    # Q1-6: tfng
    t1_p1_qs.extend([
        {"id": "cam20_t1_r_q1", "type": "tfng", "question": "The kakapo was once found on all three main islands of New Zealand.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE"},
        {"id": "cam20_t1_r_q2", "type": "tfng", "question": "The kakapo was hunted to extinction on the main islands by Maori settlers.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE"},
        {"id": "cam20_t1_r_q3", "type": "tfng", "question": "The male kakapo is significantly larger than the female.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE"},
        {"id": "cam20_t1_r_q4", "type": "tfng", "question": "Kakapos were frequently kept as pets by European settlers.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
        {"id": "cam20_t1_r_q5", "type": "tfng", "question": "The kakapo's inability to fly makes it especially vulnerable to introduced predators.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "TRUE"},
        {"id": "cam20_t1_r_q6", "type": "tfng", "question": "The kakapo recovery programme has involved moving birds to predator-free islands.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "TRUE"},
    ])
    # Q7-13: notes_completion
    for i, (qtext, ans) in enumerate([
        ("The kakapo's diet includes fruit, seeds, roots and 7. _____", "bulbs"),
        ("Kakapos build their nests in burrows or under rocks on the 8. _____", "soil"),
        ("The kakapo's soft, green and brown 9. _____ help camouflage it.", "feathers"),
        ("Introduced predators include stoats, cats and 10. _____", "deer"),
        ("The Kakapo Recovery Programme was formally established in 11. _____", "1980"),
        ("The programme has persistently struggled to obtain adequate 12. _____", "funding"),
        ("The programme depends on collaboration with a wide range of 13. _____", "stakeholders"),
    ], 7):
        t1_p1_qs.append({"id": f"cam20_t1_r_q{i}", "type": "notes_completion", "question": qtext, "options": [], "correctAnswer": ans})
    t1_passages.append({"id": "cam20_t1_p1", "title": "The Kakapo", "text": PASSAGES["t1_p1"]["text"], "timeRecommended": 20, "questions": t1_p1_qs})

    # Passage 2: Bringing Elms Back to Britain (Q14-26)
    t1_p2_qs = []
    # Q14-18: matching_info
    for i, (qtext, ans) in enumerate([
        ("how the disease that killed the elms spreads", "C"),
        ("the writer's optimism about the long-term prospects for the elm", "G"),
        ("a description of the effect of the disease on Britain's elm trees", "B"),
        ("a project to reproduce elms that survived the disease", "E"),
        ("how the writer describes the scale of the destruction", "C"),
    ], 14):
        t1_p2_qs.append({"id": f"cam20_t1_r_q{i}", "type": "matching_info", "question": qtext, "options": ["A", "B", "C", "D", "E", "F", "G"], "correctAnswer": ans})
    # Q19-23: matching_names
    for i, (qtext, ans) in enumerate([
        ("believes the main goal is to restore the elm to the British landscape", "A"),
        ("co-ordinates the fieldwork involved in locating surviving elms", "B"),
        ("emphasises the importance of testing the resistance of potential trees", "B"),
        ("considers the elm project a model for future conservation work", "C"),
        ("has collected cuttings from elms that showed signs of resistance", "A"),
    ], 19):
        t1_p2_qs.append({
            "id": f"cam20_t1_r_q{i}", "type": "matching_names",
            "question": qtext,
            "options": ["A. Matt Elliot", "B. Karen Russell", "C. Peter Bourne"],
            "correctAnswer": ans,
        })
    # Q24-26: summary_completion
    for i, (qtext, ans) in enumerate([
        ("The new trees are being planted in former 24. _____ woodlands.", "oak"),
        ("Some of the timber from the new trees may be used for 25. _____", "flooring"),
        ("The project aims to develop elms that can withstand the disease known as 26. _____", "keel"),
    ], 24):
        t1_p2_qs.append({"id": f"cam20_t1_r_q{i}", "type": "summary_completion", "question": qtext, "options": [], "correctAnswer": ans})
    t1_passages.append({"id": "cam20_t1_p2", "title": "Bringing Elms Back to Britain (Return of the Elm)", "text": PASSAGES["t1_p2"]["text"], "timeRecommended": 20, "questions": t1_p2_qs})

    # Passage 3: How Stress Affects Our Judgement (Q27-40)
    t1_p3_qs = []
    # Q27-35: matching_info
    for i, (qtext, ans) in enumerate([
        ("research findings concerning individuals who were actually experiencing stress", "C"),
        ("a biological explanation of why the brain responds to stress in a particular way", "A"),
        ("an account of how stress influences people's thinking in a financial context", "D"),
        ("examples of how people's behaviour under stress is counterproductive", "C"),
        ("research that compared the behaviour of people under stress with those who were not", "B"),
        ("a reference to the persistence of the effects of stress on judgement", "G"),
        ("findings relating to people who were not able to detect a difference in their behaviour", "F"),
        ("how participants were made to feel stressed during a study", "E"),
        ("the occupations of the people who took part in one study", "D"),
    ], 27):
        t1_p3_qs.append({"id": f"cam20_t1_r_q{i}", "type": "matching_info", "question": qtext, "options": ["A", "B", "C", "D", "E", "F", "G"], "correctAnswer": ans})
    # Q36-40: ynng
    t1_p3_qs.extend([
        {"id": "cam20_t1_r_q36", "type": "ynng", "question": "Stressed individuals are generally unaware of the effects that stress is having on their decision-making.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "YES"},
        {"id": "cam20_t1_r_q37", "type": "ynng", "question": "Stressed individuals are less capable of distinguishing between important and unimportant information.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
        {"id": "cam20_t1_r_q38", "type": "ynng", "question": "Stress is more likely to affect men's judgement than women's.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "NO"},
        {"id": "cam20_t1_r_q39", "type": "ynng", "question": "The stress caused by time pressure can reduce a person's ability to think creatively.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "YES"},
        {"id": "cam20_t1_r_q40", "type": "ynng", "question": "Understanding how stress affects judgement can help improve performance in certain professions.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "YES"},
    ])
    t1_passages.append({"id": "cam20_t1_p3", "title": "How Stress Affects Our Judgement", "text": PASSAGES["t1_p3"]["text"], "timeRecommended": 20, "questions": t1_p3_qs})

    tests.append({"id": "cam20_test1", "testNumber": 1, "passages": t1_passages})

    # ========== TEST 2 ==========
    t2_passages = []

    # Passage 1: Manatees (Q1-13)
    t2_p1_qs = []
    # Q1-6: notes_completion
    for i, (qtext, ans) in enumerate([
        ("Manatees propel themselves through the water using their 1. _____", "tail"),
        ("They steer and manoeuvre using their 2. _____", "flippers"),
        ("Manatees have sensitive 3. _____ on their bodies that can detect vibrations.", "hair"),
        ("Their diet consists mainly of 4. _____ and other aquatic plants.", "seagrasses"),
        ("They grasp vegetation using their flexible upper 5. _____", "lips"),
        ("Manatees control their position in the water through 6. _____", "buoyancy"),
    ], 1):
        t2_p1_qs.append({"id": f"cam20_t2_r_q{i}", "type": "notes_completion", "question": qtext, "options": [], "correctAnswer": ans})
    # Q7-13: tfng
    t2_p1_qs.extend([
        {"id": "cam20_t2_r_q7", "type": "tfng", "question": "Manatees need to eat a very large amount of food each day to survive.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "TRUE"},
        {"id": "cam20_t2_r_q8", "type": "tfng", "question": "Manatees rely mainly on their eyesight to find food.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
        {"id": "cam20_t2_r_q9", "type": "tfng", "question": "Manatees are more active at night than during the day.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE"},
        {"id": "cam20_t2_r_q10", "type": "tfng", "question": "Manatees migrate over long distances every year.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
        {"id": "cam20_t2_r_q11", "type": "tfng", "question": "The greatest threat to manatees comes from collisions with boats.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "TRUE"},
        {"id": "cam20_t2_r_q12", "type": "tfng", "question": "Some manatees have adapted to living in cold water.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
        {"id": "cam20_t2_r_q13", "type": "tfng", "question": "Manatees have been known to survive for many years in captivity.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "TRUE"},
    ])
    t2_passages.append({"id": "cam20_t2_p1", "title": "Manatees", "text": PASSAGES["t2_p1"]["text"], "timeRecommended": 20, "questions": t2_p1_qs})

    # Passage 2: Procrastination (Q14-26)
    t2_p2_qs = []
    # Q14-16: matching_info
    for i, (qtext, ans) in enumerate([
        ("the reason why procrastinators often continue to delay despite knowing the consequences", "B"),
        ("the claim that procrastination can sometimes be beneficial", "F"),
        ("a problem with how some people label procrastinators", "B"),
    ], 14):
        t2_p2_qs.append({"id": f"cam20_t2_r_q{i}", "type": "matching_info", "question": qtext, "options": ["A", "B", "C", "D", "E", "F"], "correctAnswer": ans})
    # Q17-22: notes_completion
    for i, (qtext, ans) in enumerate([
        ("Procrastination is often wrongly assumed to be a sign of 17. _____", "laziness"),
        ("Delaying tasks can trigger feelings of being overwhelmed and 18. _____", "anxious"),
        ("Many procrastinators worry about being unable to cope with certain 19. _____", "threats"),
        ("Academic procrastination is commonly associated with studying for 20. _____", "exams"),
        ("Procrastination affects people who describe themselves as 21. _____", "perfectionists"),
        ("The emotional consequence of putting things off often includes 22. _____", "guilt"),
    ], 17):
        t2_p2_qs.append({"id": f"cam20_t2_r_q{i}", "type": "notes_completion", "question": qtext, "options": [], "correctAnswer": ans})
    # Q23-26: matching_names
    for i, (qtext, ans) in enumerate([
        ("those who tend to procrastinate generally earn less", "A"),
        ("chronic procrastinators tend to have less stable jobs", "C"),
        ("advises people to forgive themselves for procrastinating", "A"),
        ("suggests avoiding distractions", "E"),
    ], 23):
        t2_p2_qs.append({
            "id": f"cam20_t2_r_q{i}", "type": "matching_names",
            "question": qtext,
            "options": ["A", "B", "C", "D", "E"],
            "correctAnswer": ans,
        })
    t2_passages.append({"id": "cam20_t2_p2", "title": "Procrastination", "text": PASSAGES["t2_p2"]["text"], "timeRecommended": 20, "questions": t2_p2_qs})

    # Passage 3: Invasion of the Robot Umpires (Q27-40)
    t2_p3_qs = []
    # Q27-32: ynng
    t2_p3_qs.extend([
        {"id": "cam20_t2_r_q27", "type": "ynng", "question": "Robot umpires have been adopted by all major professional sports leagues.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "NO"},
        {"id": "cam20_t2_r_q28", "type": "ynng", "question": "The use of technology in sports has reduced the number of disputes during matches.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "YES"},
        {"id": "cam20_t2_r_q29", "type": "ynng", "question": "Professional athletes generally prefer robot umpires to human officials.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
        {"id": "cam20_t2_r_q30", "type": "ynng", "question": "Controversial refereeing decisions are part of what makes sport appealing to many fans.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "NO"},
        {"id": "cam20_t2_r_q31", "type": "ynng", "question": "Robot umpires have made sport more accessible to lower-level competitions.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
        {"id": "cam20_t2_r_q32", "type": "ynng", "question": "The use of technology has removed all human error from top-level sport.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "YES"},
    ])
    # Q33-37: matching_info
    for i, (qtext, ans) in enumerate([
        ("what people think about the roles of officials", "F"),
        ("the argument that accuracy is more important than tradition", "D"),
        ("the area of the field that is monitored by a particular technology", "H"),
        ("how disagreements over decisions have increased", "B"),
        ("the complete quiet needed by a particular technology", "G"),
    ], 33):
        t2_p3_qs.append({"id": f"cam20_t2_r_q{i}", "type": "matching_info", "question": qtext, "options": ["A", "B", "C", "D", "E", "F", "G", "H"], "correctAnswer": ans})
    # Q38-40: multiple_choice
    t2_p3_qs.append({"id": "cam20_t2_r_q38", "type": "multiple_choice", "question": "What is the main reason the writer gives for the introduction of robot umpires?", "options": ["A. They are cheaper than human officials in the long term.", "B. They offer greater accuracy than human officials.", "C. They are favoured by the majority of sports fans.", "D. They speed up the pace of the game."], "correctAnswer": "B"})
    t2_p3_qs.append({"id": "cam20_t2_r_q39", "type": "multiple_choice", "question": "What concern does the writer raise about the cost of technological officiating?", "options": ["A. It may mean fewer resources for player development.", "B. It could create inequality between wealthy and less wealthy competitions.", "C. It discourages investment in grassroots sport.", "D. It is too expensive for most professional leagues."], "correctAnswer": "D"})
    t2_p3_qs.append({"id": "cam20_t2_r_q40", "type": "multiple_choice", "question": "What is the writer's overall conclusion about robot umpires?", "options": ["A. They will eventually replace human officials entirely.", "B. Their introduction has been too rapid.", "C. They are here to stay but the limits of their use are still being debated.", "D. They should only be used as a backup for human officials."], "correctAnswer": "C"})
    t2_passages.append({"id": "cam20_t2_p3", "title": "Invasion of the Robot Umpires", "text": PASSAGES["t2_p3"]["text"], "timeRecommended": 20, "questions": t2_p3_qs})

    tests.append({"id": "cam20_test2", "testNumber": 2, "passages": t2_passages})

    # ========== TEST 3 ==========
    t3_passages = []

    # Passage 1: Frozen Food (Q1-13)
    t3_p1_qs = []
    # Q1-7: notes_completion
    for i, (qtext, ans) in enumerate([
        ("The first products to be frozen included peas and 1. _____", "potatoes"),
        ("Birdseye used 2. _____ to prevent the formation of large ice crystals.", "butter"),
        ("Frozen 3. _____ was also an early commercially available product.", "meat"),
        ("The quick-freezing process prevented the formation of large ice 4. _____", "crystals"),
        ("Early packaging materials included waxed paper and 5. _____", "cellophane"),
        ("Frozen products were also stored in 6. _____ containers.", "tin"),
        ("The development of the home 7. _____ was crucial for the frozen food industry.", "refrigerator"),
    ], 1):
        t3_p1_qs.append({"id": f"cam20_t3_r_q{i}", "type": "notes_completion", "question": qtext, "options": [], "correctAnswer": ans})
    # Q8-13: tfng
    t3_p1_qs.extend([
        {"id": "cam20_t3_r_q8", "type": "tfng", "question": "Birdseye's quick-freezing method was based on techniques used by Arctic communities.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
        {"id": "cam20_t3_r_q9", "type": "tfng", "question": "The quick-freezing process helped preserve the nutritional value of food.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "TRUE"},
        {"id": "cam20_t3_r_q10", "type": "tfng", "question": "Frozen food was more expensive than fresh food when it was first introduced.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE"},
        {"id": "cam20_t3_r_q11", "type": "tfng", "question": "The availability of frozen food has reduced the need for frequent shopping.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "TRUE"},
        {"id": "cam20_t3_r_q12", "type": "tfng", "question": "Frozen food always has lower nutritional value than fresh food.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE"},
        {"id": "cam20_t3_r_q13", "type": "tfng", "question": "The frozen food industry now relies on global supply chains.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
    ])
    t3_passages.append({"id": "cam20_t3_p1", "title": "Frozen Food", "text": PASSAGES["t3_p1"]["text"], "timeRecommended": 20, "questions": t3_p1_qs})

    # Passage 2: Can the Planet's Coral Reefs Be Saved? (Q14-26)
    t3_p2_qs = []
    # Q14-19: matching_headings
    headings = [
        "i. A common interest in survival",
        "ii. Cooperation beneath the waves",
        "iii. Working to lessen the problems",
        "iv. Disagreement about accuracy of a phrase",
        "v. Two clear educational goals",
        "vi. Promoting hope",
        "vii. A warning of further trouble ahead",
    ]
    for i, ans in enumerate(["v", "ii", "iv", "vii", "iii", "vi"], 14):
        t3_p2_qs.append({"id": f"cam20_t3_r_q{i}", "type": "matching_headings", "question": f"Section {chr(64+i-13)}", "options": headings, "correctAnswer": ans})
    # Q20-23: matching_info
    for i, (qtext, ans) in enumerate([
        ("contamination of the sea from waste", "C"),
        ("alterations in the usual flow of water in the seas", "E"),
        ("identify corals that can cope with changed conditions", "B"),
        ("trying methods to speed up reproduction", "D"),
    ], 20):
        t3_p2_qs.append({"id": f"cam20_t3_r_q{i}", "type": "matching_info", "question": qtext, "options": ["A", "B", "C", "D", "E", "F"], "correctAnswer": ans})
    # Q24-26: notes_completion
    for i, (qtext, ans) in enumerate([
        ("Coral polyps have stinging 24. _____ that they use to capture food.", "tentacles"),
        ("The algae living in coral tissues provide them with 25. _____", "protection"),
        ("When corals bleach, they lose their 26. _____", "colour"),
    ], 24):
        t3_p2_qs.append({"id": f"cam20_t3_r_q{i}", "type": "notes_completion", "question": qtext, "options": [], "correctAnswer": ans})
    t3_passages.append({"id": "cam20_t3_p2", "title": "Can the Planet's Coral Reefs Be Saved?", "text": PASSAGES["t3_p2"]["text"], "timeRecommended": 20, "questions": t3_p2_qs})

    # Passage 3: Robots and Us (Q27-40)
    t3_p3_qs = []
    # Q27-33: matching_names
    for i, (qtext, ans) in enumerate([
        ("believes machine intelligence will eventually overpower human intelligence", "A"),
        ("claims that human-like robots may cause people to treat each other less well", "C"),
        ("argues that the main role of the brain is to enable us to move", "B"),
        ("believes we must consider both the benefits and dangers of AI", "A"),
        ("states that understanding how the brain controls movement can help improve robot design", "B"),
        ("says machine intelligence could be as momentous as the origin of life", "A"),
        ("suggests that the desire to create companions reflects a desire for control", "C"),
    ], 27):
        t3_p3_qs.append({
            "id": f"cam20_t3_r_q{i}", "type": "matching_names",
            "question": qtext,
            "options": ["A. Martin Rees", "B. Daniel Wolpert", "C. Kathleen Richardson"],
            "correctAnswer": ans,
        })
    # Q34-36: matching_info
    for i, (qtext, ans) in enumerate([
        ("changes made to other planets for our own benefit", "C"),
        ("advances made in machine intelligence so far", "B"),
        ("the harm already done by artificial intelligence", "D"),
    ], 34):
        t3_p3_qs.append({"id": f"cam20_t3_r_q{i}", "type": "matching_info", "question": qtext, "options": ["A", "B", "C", "D", "E"], "correctAnswer": ans})
    # Q37-40: multiple_choice
    t3_p3_qs.append({"id": "cam20_t3_r_q37", "type": "multiple_choice", "question": "What does Martin Rees say about the future of machine intelligence?", "options": ["A. It will not happen in our lifetime.", "B. It could be the most important event in human history.", "C. It will mainly benefit wealthy countries.", "D. It poses a greater risk than climate change."], "correctAnswer": "B"})
    t3_p3_qs.append({"id": "cam20_t3_r_q38", "type": "multiple_choice", "question": "What is Kathleen Richardson's main concern about companion robots?", "options": ["A. They are too expensive for most people.", "B. They may replace human relationships.", "C. They could make people less able to relate to others.", "D. They are not sophisticated enough to be useful."], "correctAnswer": "C"})
    t3_p3_qs.append({"id": "cam20_t3_r_q39", "type": "multiple_choice", "question": "According to Daniel Wolpert, what is the main purpose of the brain?", "options": ["A. To process sensory information.", "B. To generate complex movement.", "C. To enable conscious thought.", "D. To store and retrieve memories."], "correctAnswer": "B"})
    t3_p3_qs.append({"id": "cam20_t3_r_q40", "type": "multiple_choice", "question": "What is the main point the writer makes in the passage?", "options": ["A. Robots will eventually replace humans in most jobs.", "B. The development of AI should be restricted.", "C. Different experts hold contrasting views on the future of AI and robotics.", "D. Humans and robots will learn to coexist peacefully."], "correctAnswer": "C"})
    t3_passages.append({"id": "cam20_t3_p3", "title": "Robots and Us", "text": PASSAGES["t3_p3"]["text"], "timeRecommended": 20, "questions": t3_p3_qs})

    tests.append({"id": "cam20_test3", "testNumber": 3, "passages": t3_passages})

    # ========== TEST 4 ==========
    t4_passages = []

    # Passage 1: Georgia O'Keeffe (Q1-13)
    t4_p1_qs = []
    # Q1-7: notes_completion
    for i, (qtext, ans) in enumerate([
        ("O'Keeffe began her professional life as a 1. _____", "teacher"),
        ("Her early work was executed primarily in 2. _____", "charcoal"),
        ("While living in New York, she painted a series of 3. _____", "skyscrapers"),
        ("She is best known for her large-scale paintings of 4. _____", "flowers"),
        ("In New Mexico, she painted images of animal 5. _____", "bones"),
        ("Her work was deeply influenced by the Southwestern 6. _____", "landscape"),
        ("Her paintings of the region included images of 7. _____", "rivers"),
    ], 1):
        t4_p1_qs.append({"id": f"cam20_t4_r_q{i}", "type": "notes_completion", "question": qtext, "options": [], "correctAnswer": ans})
    # Q8-13: tfng
    t4_p1_qs.extend([
        {"id": "cam20_t4_r_q8", "type": "tfng", "question": "O'Keeffe trained as an artist before she became a teacher.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE"},
        {"id": "cam20_t4_r_q9", "type": "tfng", "question": "Alfred Stieglitz was instrumental in promoting O'Keeffe's work.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "TRUE"},
        {"id": "cam20_t4_r_q10", "type": "tfng", "question": "O'Keeffe's flower paintings were her most commercially successful works.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE"},
        {"id": "cam20_t4_r_q11", "type": "tfng", "question": "O'Keeffe deliberately avoided being classified by artistic movements.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "TRUE"},
        {"id": "cam20_t4_r_q12", "type": "tfng", "question": "O'Keeffe's work was initially more popular in Europe than in the United States.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
        {"id": "cam20_t4_r_q13", "type": "tfng", "question": "O'Keeffe stopped painting in the final years of her life.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "NOT GIVEN"},
    ])
    t4_passages.append({"id": "cam20_t4_p1", "title": "Georgia O'Keeffe", "text": PASSAGES["t4_p1"]["text"], "timeRecommended": 20, "questions": t4_p1_qs})

    # Passage 2: Adapting to the Effects of Climate Change (Q14-26)
    t4_p2_qs = []
    # Q14-17: matching_info
    for i, (qtext, ans) in enumerate([
        ("how the effects of climate change are becoming more intense", "C"),
        ("the need to balance adaptation with emission reduction", "A"),
        ("examples of different adaptation methods used in different parts of the world", "D"),
        ("a description of specific urban adaptation strategies", "F"),
    ], 14):
        t4_p2_qs.append({"id": f"cam20_t4_r_q{i}", "type": "matching_info", "question": qtext, "options": ["A", "B", "C", "D", "E", "F"], "correctAnswer": ans})
    # Q18-22: notes_completion
    for i, (qtext, ans) in enumerate([
        ("In coastal cities, 18. _____ are being installed to improve drainage.", "pumps"),
        ("Some regions are building 19. _____ to manage water resources.", "dams"),
        ("New homes designed to 20. _____ on water are being developed.", "float"),
        ("Drought-resistant 21. _____ are being developed for agriculture.", "crops"),
        ("Flood-resistant 22. _____ are also being planted.", "trees"),
    ], 18):
        t4_p2_qs.append({"id": f"cam20_t4_r_q{i}", "type": "notes_completion", "question": qtext, "options": [], "correctAnswer": ans})
    # Q23-26: matching_names
    for i, (qtext, ans) in enumerate([
        ("says we need to rethink how we build homes in flood-prone areas", "B"),
        ("believes cities need to invest more in green infrastructure", "E"),
        ("argues that adaptation should focus on protecting the most vulnerable communities", "A"),
        ("emphasises the need for international funding for adaptation", "C"),
    ], 23):
        t4_p2_qs.append({
            "id": f"cam20_t4_r_q{i}", "type": "matching_names",
            "question": qtext,
            "options": ["A. Yanira Pineda", "B. Susanna Tol", "C. Elizabeth English", "D", "E. Greg Spotts"],
            "correctAnswer": ans,
        })
    t4_passages.append({"id": "cam20_t4_p2", "title": "Adapting to the Effects of Climate Change", "text": PASSAGES["t4_p2"]["text"], "timeRecommended": 20, "questions": t4_p2_qs})

    # Passage 3: Livestock Guard Dogs (Q14-26)
    # Note: Q33-36 answers are not available - skip those questions
    t4_p3_qs = []
    # Q27-32: matching_info
    for i, (qtext, ans) in enumerate([
        ("why some guard dogs may pose a risk to wildlife", "D"),
        ("the type of training guard dogs need", "G"),
        ("the fact that guard dogs also protect against smaller predators", "B"),
        ("a comparison between modern and traditional uses of guard dogs", "C"),
        ("the importance of the bond between the dog and the livestock", "B"),
        ("the role of barking in the guard dog's behaviour", "D"),
    ], 27):
        t4_p3_qs.append({"id": f"cam20_t4_r_q{i}", "type": "matching_info", "question": qtext, "options": ["A", "B", "C", "D", "E", "F", "G"], "correctAnswer": ans})
    # Q33-36: SKIPPED (answers not available)
    # Q37-40: notes_completion
    for i, (qtext, ans) in enumerate([
        ("Guard dogs protect livestock from predators such as wolves, coyotes and 37. _____", "jackals"),
        ("Their presence can reduce the spread of 38. _____ among livestock.", "diseases"),
        ("The dogs help ensure a more reliable supply of 39. _____", "food"),
        ("They have also been shown to deter 40. _____ from the area.", "foxes"),
    ], 37):
        t4_p3_qs.append({"id": f"cam20_t4_r_q{i}", "type": "notes_completion", "question": qtext, "options": [], "correctAnswer": ans})
    t4_passages.append({"id": "cam20_t4_p3", "title": "Livestock Guard Dogs (A New Role for Livestock Guard Dogs)", "text": PASSAGES["t4_p3"]["text"], "timeRecommended": 20, "questions": t4_p3_qs})

    tests.append({"id": "cam20_test4", "testNumber": 4, "passages": t4_passages})

    return {"id": "cam20", "title": "Cambridge IELTS 20 Academic Reading", "tests": tests}


###############################################################################
# LISTENING DATA
###############################################################################

def make_listening():
    tests = []

    # ========== LISTENING TEST 1 ==========
    lt1_parts = []
    # Part 1: Restaurant Recommendations (Q1-10)
    lt1_p1_qs = []
    for i, (qtext, ans) in enumerate([
        ("1. Type of food: _____", "fish"),
        ("2. Atmosphere: _____ restaurant", "roof"),
        ("3. Cuisine: _____", "Spanish"),
        ("4. Dietary option: _____", "vegetarian"),
        ("5. Name of restaurant: _____", "Audley"),
        ("6. Location: inside a _____", "hotel"),
        ("7. Check online _____", "reviews"),
        ("8. Ingredients: _____ produce", "local"),
        ("9. Price range: under £_____", "30"),
        ("10. Rating: _____", "average"),
    ], 1):
        lt1_p1_qs.append({"id": f"cam20_lt1_q{i}", "type": "notes_completion", "question": qtext, "options": [], "correctAnswer": ans})
    lt1_parts.append({"id": "cam20_lt1_p1", "title": "Restaurant Recommendations", "audioFile": "cam20_test1_part1.mp3", "subtitle": "", "duration": "", "questions": lt1_p1_qs})

    # Part 2: Heather and Pottery (Q11-20)
    lt1_p2_qs = []
    for i, (qtext, ans) in enumerate([
        ("Heather chose to work with clay because", "A"),
        ("What does Heather say about the identification marks on her pots?", "B"),
        ("Heather says that what she values most about her work is the opportunity to", "C"),
        ("What does Heather say about the effect of working with clay?", "A"),
        ("Most people who attend Heather's classes", "B"),
        ("What does Heather recommend that participants do before a class?", "C"),
    ], 11):
        lt1_p2_qs.append({"id": f"cam20_lt1_q{i}", "type": "multiple_choice", "question": qtext, "options": ["A", "B", "C"], "correctAnswer": ans})
    # Q17-20: matching
    for i, (qtext, ans) in enumerate([
        ("Choose the correct letter: What does Heather say about each item?", "A"),
        ("Choose the correct letter: What does Heather say about each item?", "E"),
        ("Choose the correct letter: What does Heather say about each item?", "C"),
        ("Choose the correct letter: What does Heather say about each item?", "E"),
    ], 17):
        lt1_p2_qs.append({"id": f"cam20_lt1_q{i}", "type": "matching", "question": qtext, "options": ["A. what their function is", "B", "C. Some are essential items", "D", "E. Some are available for use by participants"], "correctAnswer": ans})
    lt1_parts.append({"id": "cam20_lt1_p2", "title": "Heather and Pottery", "audioFile": "cam20_test1_part2.mp3", "subtitle": "", "duration": "", "questions": lt1_p2_qs})

    # Part 3: Loneliness (Q21-30)
    lt1_p3_qs = []
    # Q21-26: matching
    for i, (qtext, ans) in enumerate([
        ("Factor that may cause loneliness: urban design", "C"),
        ("Factor that may cause loneliness: a mobile workforce", "E"),
        ("Possible consequence of loneliness: a weakened immune system", "A"),
        ("Possible consequence of loneliness: cancer", "C"),
        ("Previous research on loneliness: has little practical relevance", "A"),
        ("Previous research on loneliness: needs further investigation", "B"),
    ], 21):
        lt1_p3_qs.append({"id": f"cam20_lt1_q{i}", "type": "matching", "question": qtext, "options": ["A. a weakened immune system", "B. needs further investigation", "C. urban design", "D. cancer", "E. a mobile workforce"], "correctAnswer": ans})
    # Q27-30: multiple_choice
    for i, ans in enumerate(["A", "B", "A", "C"], 27):
        lt1_p3_qs.append({"id": f"cam20_lt1_q{i}", "type": "multiple_choice", "question": f"Question {i}: Choose the correct letter.", "options": ["A", "B", "C"], "correctAnswer": ans})
    lt1_parts.append({"id": "cam20_lt1_p3", "title": "Loneliness", "audioFile": "cam20_test1_part3.mp3", "subtitle": "", "duration": "", "questions": lt1_p3_qs})

    # Part 4: Reclaiming Urban Rivers (Q31-40)
    lt1_p4_qs = []
    for i, ans in enumerate(["factories", "dead", "whale", "apartments", "park", "art", "beaches", "ferry", "bikes", "drone"], 31):
        lt1_p4_qs.append({"id": f"cam20_lt1_q{i}", "type": "notes_completion", "question": f"Question {i}: ONE WORD ONLY.", "options": [], "correctAnswer": ans})
    lt1_parts.append({"id": "cam20_lt1_p4", "title": "Reclaiming Urban Rivers", "audioFile": "cam20_test1_part4.mp3", "subtitle": "", "duration": "", "questions": lt1_p4_qs})

    tests.append({"id": "cam20_listening_test1", "testNumber": 1, "parts": lt1_parts})

    # ========== LISTENING TEST 2 ==========
    lt2_parts = []
    # Part 1: Help for Carers (Q1-10)
    lt2_p1_qs = []
    for i, (qtext, ans) in enumerate([
        ("1. Need a _____ from caring duties", "break"),
        ("2. Help with managing _____", "time"),
        ("3. Need help with taking a _____", "shower"),
        ("4. Financial advice about _____", "money"),
        ("5. Support for problems with _____", "memory"),
        ("6. Help with _____ heavy items", "lifting"),
        ("7. Risk of _____", "fall"),
        ("8. Transport: _____ service", "taxi"),
        ("9. Advice about _____", "insurance"),
        ("10. Help dealing with _____", "stress"),
    ], 1):
        lt2_p1_qs.append({"id": f"cam20_lt2_q{i}", "type": "notes_completion", "question": qtext, "options": [], "correctAnswer": ans})
    lt2_parts.append({"id": "cam20_lt2_p1", "title": "Help for Carers", "audioFile": "cam20_test2_part1.mp3", "subtitle": "", "duration": "", "questions": lt2_p1_qs})

    # Part 2: Community Volunteering (Q11-20)
    lt2_p2_qs = []
    # Q11-16: matching
    for i, (qtext, ans) in enumerate([
        ("Volunteer role: giving advice to visitors", "D"),
        ("Volunteer role: helping people find their seats", "I"),
        ("Volunteer role: encouraging cooperation between local organisations", "H"),
        ("Volunteer role: collecting feedback on events", "E"),
        ("Volunteer role: providing entertainment", "A"),
        ("Volunteer role: providing publicity about a council service", "B"),
    ], 11):
        lt2_p2_qs.append({"id": f"cam20_lt2_q{i}", "type": "matching", "question": qtext, "options": ["A", "B", "C", "D", "E", "F", "G", "H", "I"], "correctAnswer": ans})
    # Q17-20: multiple_choice
    for i, (qtext, ans) in enumerate([
        ("Which event is the speaker recommending?", "B"),
        ("What skill is most needed for volunteering?", "A"),
        ("When is the volunteer training session?", "B"),
        ("What does the volunteer package include?", "A"),
    ], 17):
        lt2_p2_qs.append({"id": f"cam20_lt2_q{i}", "type": "multiple_choice", "question": qtext, "options": ["A", "B", "C"], "correctAnswer": ans})
    lt2_parts.append({"id": "cam20_lt2_p2", "title": "Community Volunteering", "audioFile": "cam20_test2_part2.mp3", "subtitle": "", "duration": "", "questions": lt2_p2_qs})

    # Part 3: Human Geography Discussion (Q21-30)
    lt2_p3_qs = []
    # Q21-26: matching
    for i, (qtext, ans) in enumerate([
        ("Matching question 21", "D"),
        ("Matching question 22", "G"),
        ("Matching question 23", "B"),
        ("Matching question 24", "A"),
        ("Matching question 25", "E"),
        ("Matching question 26: unemployment", "C"),
    ], 21):
        lt2_p3_qs.append({"id": f"cam20_lt2_q{i}", "type": "matching", "question": qtext, "options": ["A", "B", "C", "D", "E", "F", "G"], "correctAnswer": ans})
    # Q27-30: multiple_choice
    for i, (qtext, ans) in enumerate([
        ("What does the student say about conference centres?", "A"),
        ("What problem do new developments face?", "A"),
        ("What aspect of the development is the student most interested in?", "B"),
        ("What does the tutor say about the student's research?", "C"),
    ], 27):
        lt2_p3_qs.append({"id": f"cam20_lt2_q{i}", "type": "multiple_choice", "question": qtext, "options": ["A", "B", "C"], "correctAnswer": ans})
    lt2_parts.append({"id": "cam20_lt2_p3", "title": "Human Geography Discussion", "audioFile": "cam20_test2_part3.mp3", "subtitle": "", "duration": "", "questions": lt2_p3_qs})

    # Part 4: Developing Food Trends (Q31-40)
    lt2_p4_qs = []
    for i, (qtext, ans) in enumerate([
        ("31. Sharing _____ of food online", "photos"),
        ("32. Rise of _____ diet", "vegan"),
        ("33. Influence of famous _____", "chefs"),
        ("34. Coverage by food _____", "journalists"),
        ("35. Focus on _____ benefits", "health"),
        ("36. Popularity of speciality _____", "coffee"),
        ("37. Concern about the _____", "environment"),
        ("38. Importance of brand _____", "reputation"),
        ("39. Sensitivity to _____", "price"),
        ("40. Condition of the _____", "soil"),
    ], 31):
        lt2_p4_qs.append({"id": f"cam20_lt2_q{i}", "type": "notes_completion", "question": qtext, "options": [], "correctAnswer": ans})
    lt2_parts.append({"id": "cam20_lt2_p4", "title": "Developing Food Trends", "audioFile": "cam20_test2_part4.mp3", "subtitle": "", "duration": "", "questions": lt2_p4_qs})

    tests.append({"id": "cam20_listening_test2", "testNumber": 2, "parts": lt2_parts})

    # ========== LISTENING TEST 3 ==========
    lt3_parts = []
    # Part 1: Furniture Rental Companies (Q1-10)
    lt3_p1_qs = []
    for i, (qtext, ans) in enumerate([
        ("1. Customer reference: _____", "239"),
        ("2. Style required: _____", "modern"),
        ("3. Item needed: _____", "lamp"),
        ("4. Contact person: _____", "Aaron"),
        ("5. Concern about: _____", "damage"),
        ("6. Need for _____ equipment", "electronic"),
        ("7. Take out _____", "insurance"),
        ("8. Company name: _____", "Space"),
        ("9. Use their _____ to browse items", "app"),
        ("10. Option for _____", "exchanges"),
    ], 1):
        lt3_p1_qs.append({"id": f"cam20_lt3_q{i}", "type": "notes_completion", "question": qtext, "options": [], "correctAnswer": ans})
    lt3_parts.append({"id": "cam20_lt3_p1", "title": "Furniture Rental Companies", "audioFile": "cam20_test3_part1.mp3", "subtitle": "", "duration": "", "questions": lt3_p1_qs})

    # Part 2: Archaeology at Bidcaster Castle (Q11-20)
    lt3_p2_qs = []
    # Q11-16: multiple_choice
    for i, (qtext, ans) in enumerate([
        ("The archaeological project is run by", "B"),
        ("What initially exposed the archaeological site?", "A"),
        ("What helped the archaeologists identify the site?", "A"),
        ("What was the most surprising find?", "C"),
        ("What did the geophysical survey reveal?", "B"),
        ("What is the project's main educational aim?", "C"),
    ], 11):
        lt3_p2_qs.append({"id": f"cam20_lt3_q{i}", "type": "multiple_choice", "question": qtext, "options": ["A", "B", "C"], "correctAnswer": ans})
    # Q17-20: matching (map)
    for i, (qtext, ans) in enumerate([
        ("bridge foundations", "B"),
        ("rubbish pit - near castle walls NW corner", "A"),
        ("meeting hall - central area next to excavation", "G"),
        ("fish pond - turn right at first info board, into trees", "E"),
    ], 17):
        lt3_p2_qs.append({"id": f"cam20_lt3_q{i}", "type": "matching", "question": qtext, "options": ["A", "B", "C", "D", "E", "F", "G", "H"], "correctAnswer": ans})
    lt3_parts.append({"id": "cam20_lt3_p2", "title": "Archaeology at Bidcaster Castle (Community Project)", "audioFile": "cam20_test3_part2.mp3", "subtitle": "", "duration": "", "questions": lt3_p2_qs})

    # Part 3: Theatre Programmes (Playbills) Research (Q21-30)
    lt3_p3_qs = []
    # Q21-26: multiple_choice
    for i, ans in enumerate(["B", "A", "C", "A", "C", "B"], 21):
        lt3_p3_qs.append({"id": f"cam20_lt3_q{i}", "type": "multiple_choice", "question": f"Question {i}: Choose the correct letter.", "options": ["A", "B", "C"], "correctAnswer": ans})
    # Q27-30: matching
    for i, (qtext, ans) in enumerate([
        ("Ruy Blas - resembles an artwork", "F"),
        ("Man of La Mancha - contains insights into the show", "E"),
        ("The Tragedy of Jane Shore - historically significant for Australia", "B"),
        ("The Sailors' Festival - included in recent British Library project", "D"),
    ], 27):
        lt3_p3_qs.append({"id": f"cam20_lt3_q{i}", "type": "matching", "question": qtext, "options": ["A", "B", "C", "D", "E", "F"], "correctAnswer": ans})
    lt3_parts.append({"id": "cam20_lt3_p3", "title": "Theatre Programmes (Playbills) Research", "audioFile": "cam20_test3_part3.mp3", "subtitle": "", "duration": "", "questions": lt3_p3_qs})

    # Part 4: Inclusive Design (Q31-40)
    lt3_p4_qs = []
    for i, ans in enumerate(["adaptation", "cognitive", "desks", "taps", "blue", "voice", "pregnant", "shoulders", "police", "temperature"], 31):
        lt3_p4_qs.append({"id": f"cam20_lt3_q{i}", "type": "notes_completion", "question": f"Question {i}: ONE WORD ONLY.", "options": [], "correctAnswer": ans})
    lt3_parts.append({"id": "cam20_lt3_p4", "title": "Inclusive Design", "audioFile": "cam20_test3_part4.mp3", "subtitle": "", "duration": "", "questions": lt3_p4_qs})

    tests.append({"id": "cam20_listening_test3", "testNumber": 3, "parts": lt3_parts})

    # ========== LISTENING TEST 4 ==========
    lt4_parts = []
    # Part 1: Travel Information (Kings Hotel) (Q1-10)
    lt4_p1_qs = []
    for i, (qtext, ans) in enumerate([
        ("1. Name of hotel: _____", "Kings"),
        ("2. Room cost: £_____", "125"),
        ("3. Activity: _____ tour", "walking"),
        ("4. Travel by _____ to the old fort", "boat"),
        ("5. Best day to visit Science Museum: _____", "Tuesday"),
        ("6. Exhibition about _____", "space"),
        ("7. Food type at Clacton Market: _____", "vegetarian"),
        ("8. Lunch deadline: _____", "2.30"),
        ("9. Discount on theatre tickets: _____%", "75"),
        ("10. View from Telegraph Hill: _____", "port"),
    ], 1):
        lt4_p1_qs.append({"id": f"cam20_lt4_q{i}", "type": "notes_completion", "question": qtext, "options": [], "correctAnswer": ans})
    lt4_parts.append({"id": "cam20_lt4_p1", "title": "Travel Information (Kings Hotel)", "audioFile": "cam20_test4_part1.mp3", "subtitle": "", "duration": "", "questions": lt4_p1_qs})

    # Part 2: Football Stadium Tour (Q11-20)
    lt4_p2_qs = []
    # Q11-14: multiple_choice
    for i, (qtext, ans) in enumerate([
        ("What can children do during the stadium tour?", "A"),
        ("What is available for children to take part in today?", "B"),
        ("Which tour option does the speaker recommend?", "A"),
        ("What is included with the audio guide?", "C"),
    ], 11):
        lt4_p2_qs.append({"id": f"cam20_lt4_q{i}", "type": "multiple_choice", "question": qtext, "options": ["A", "B", "C"], "correctAnswer": ans})
    # Q15-20: matching
    for i, (qtext, ans) in enumerate([
        ("1870 - introduction of goalkeepers", "D"),
        ("1874 - two changes to the rules", "F"),
        ("1875 - change to design of the goal", "B"),
        ("1877 - agreement on length of game", "H"),
        ("1878 - first use of lights for matches", "C"),
        ("1880 - introduction of fee for spectators", "G"),
    ], 15):
        lt4_p2_qs.append({"id": f"cam20_lt4_q{i}", "type": "matching", "question": qtext, "options": ["A", "B", "C", "D", "E", "F", "G", "H"], "correctAnswer": ans})
    lt4_parts.append({"id": "cam20_lt4_p2", "title": "Football Stadium Tour", "audioFile": "cam20_test4_part2.mp3", "subtitle": "", "duration": "", "questions": lt4_p2_qs})

    # Part 3: Handwriting and Learning (Q21-30)
    lt4_p3_qs = []
    # Q21-24: matching
    for i, (qtext, ans) in enumerate([
        ("improved concentration", "C"),
        ("improved spatial awareness", "E"),
        ("not spacing letters correctly", "A"),
        ("applying too much pressure when writing", "C"),
    ], 21):
        lt4_p3_qs.append({"id": f"cam20_lt4_q{i}", "type": "matching", "question": qtext, "options": ["A. not spacing letters correctly", "B", "C. improved concentration", "D", "E. improved spatial awareness"], "correctAnswer": ans})
    # Q25-30: multiple_choice
    for i, ans in enumerate(["C", "A", "A", "B", "B", "C"], 25):
        lt4_p3_qs.append({"id": f"cam20_lt4_q{i}", "type": "multiple_choice", "question": f"Question {i}: Choose the correct letter.", "options": ["A", "B", "C"], "correctAnswer": ans})
    lt4_parts.append({"id": "cam20_lt4_p3", "title": "Handwriting and Learning", "audioFile": "cam20_test4_part3.mp3", "subtitle": "", "duration": "", "questions": lt4_p3_qs})

    # Part 4: Birds of Prey (conservation) (Q31-40)
    lt4_p4_qs = []
    for i, (qtext, ans) in enumerate([
        ("31. Threat from: _____", "rats"),
        ("32. Threat from: _____", "snakes"),
        ("33. Impact of _____ on habitats", "tourism"),
        ("34. Danger from _____", "traffic"),
        ("35. Problem with _____", "rain"),
        ("36. Use of _____ by farmers", "poison"),
        ("37. Loss of _____ sites", "building"),
        ("38. Attacks by _____", "dog"),
        ("39. Disturbance from _____", "noise"),
        ("40. The main threat is a _____ of factors", "combination"),
    ], 31):
        lt4_p4_qs.append({"id": f"cam20_lt4_q{i}", "type": "notes_completion", "question": qtext, "options": [], "correctAnswer": ans})
    lt4_parts.append({"id": "cam20_lt4_p4", "title": "Birds of Prey (conservation)", "audioFile": "cam20_test4_part4.mp3", "subtitle": "", "duration": "", "questions": lt4_p4_qs})

    tests.append({"id": "cam20_listening_test4", "testNumber": 4, "parts": lt4_parts})

    return {"id": "cam20", "title": "Cambridge IELTS 20 Academic Listening", "tests": tests}


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
