#!/usr/bin/env python3
"""Generate complete Cambridge IELTS 17 Test 1 JSON data."""

import json
import os

OUT_DIR = "data/cambridge/cam17"
os.makedirs(OUT_DIR, exist_ok=True)


def create_reading_json():
    """Create reading.json with Test 1 passages and questions."""
    passage1_text = (
        "In the first half of the 1800s, London's population grew at an astonishing rate, and the central "
        "area became increasingly congested. In addition, the expansion of the overground railway "
        "network resulted in more and more passengers arriving in the capital. However, in 1846, a Royal "
        "Commission decided that the railways should not be allowed to enter the City, the capital's "
        "historic and business centre. The result was that the overground railway stations formed a ring "
        "around the City. The area within consisted of poorly built, overcrowded slums and the streets were "
        "full of horse-drawn traffic. Crossing the City became a nightmare. It could take an hour and a half "
        "to travel 8 km by horse-drawn carriage or bus. Numerous schemes were proposed to resolve these "
        "problems, but few succeeded.\n\n"
        "Amongst the most vocal advocates for a solution to London's traffic problems was Charles "
        "Pearson, who worked as a solicitor for the City of London. He saw both social and economic "
        "advantages in building an underground railway that would link the overground railway stations "
        "together and clear London slums at the same time. His idea was to relocate the poor workers who "
        "lived in the inner-city slums to newly constructed suburbs, and to provide cheap rail travel for "
        "them to get to work. Pearson's ideas gained support amongst some businessmen and in 1851 he "
        "submitted a plan to Parliament. It was rejected, but coincided with a proposal from another group "
        "for an underground connecting line, which Parliament passed.\n\n"
        "The two groups merged and established the Metropolitan Railway Company in August 1854. The "
        "company's plan was to construct an underground railway line from the Great Western Railway's "
        "(GWR) station at Paddington to the edge of the City at Farringdon Street – a distance of almost "
        "5 km. The organisation had difficulty in raising the funding for such a radical and expensive "
        "scheme, not least because of the critical articles printed by the press. Objectors argued that the "
        "tunnels would collapse under the weight of traffic overhead, buildings would be shaken and "
        "passengers would be poisoned by the emissions from the train engines. However, Pearson and his "
        "partners persisted.\n\n"
        "The GWR, aware that the new line would finally enable them to run trains into the heart of "
        "the City, invested almost £250,000 in the scheme. Eventually, over a five-year period, £1m "
        "was raised. The chosen route ran beneath existing main roads to minimise the expense of "
        "demolishing buildings. Originally scheduled to be completed in 21 months, the construction of "
        "the underground line took three years. It was built just below street level using a technique known "
        "as 'cut and cover'. A trench about ten metres wide and six metres deep was dug, and the sides "
        "temporarily held up with timber beams. Brick walls were then constructed, and finally a brick "
        "arch was added to create a tunnel. A two-metre-deep layer of soil was laid on top of the tunnel "
        "and the road above rebuilt.\n\n"
        "The Metropolitan line, which opened on 10 January 1863, was the world's first underground "
        "railway. On its first day, almost 40,000 passengers were carried between Paddington and "
        "Farringdon, the journey taking about 18 minutes. By the end of the Metropolitan's first year of "
        "operation, 9.5 million journeys had been made.\n\n"
        "Even as the Metropolitan began operation, the first extensions to the line were being authorised; "
        "these were built over the next five years, reaching Moorgate in the east of London and "
        "Hammersmith in the west. The original plan was to pull the trains with steam locomotives, using "
        "firebricks in the boilers to provide steam, but these engines were never introduced. Instead, the "
        "line used specially designed locomotives that were fitted with water tanks in which steam could "
        "be condensed. However, smoke and fumes remained a problem, even though ventilation shafts "
        "were added to the tunnels.\n\n"
        "Despite the extension of the underground railway, by the 1880s, congestion on London's streets "
        "had become worse. The problem was partly that the existing underground lines formed a circuit "
        "around the centre of London and extended to the suburbs, but did not cross the capital's centre. "
        "The 'cut and cover' method of construction was not an option in this part of the capital. The only "
        "alternative was to tunnel deep underground.\n\n"
        "Although the technology to create these tunnels existed, steam locomotives could not be used in "
        "such a confined space. It wasn't until the development of a reliable electric motor, and a means of "
        "transferring power from the generator to a moving train, that the world's first deep-level electric "
        "railway, the City & South London, became possible. The line opened in 1890, and ran from the "
        "City to Stockwell, south of the River Thames. The trains were made up of three carriages and "
        "driven by electric engines. The carriages were narrow and had tiny windows just below the roof "
        "because it was thought that passengers would not want to look out at the tunnel walls. The line "
        "was not without its problems, mainly caused by an unreliable power supply. Although the City & "
        "South London Railway was a great technical achievement, it did not make a profit. Then, in 1900, "
        "the Central London Railway, known as the 'Tuppenny Tube', began operation using new electric "
        "locomotives. It was very popular and soon afterwards new railways and extensions were added to "
        "the growing tube network. By 1907, the heart of today's Underground system was in place."
    )

    passage2_text = (
        "A\n"
        "Stadiums are among the oldest forms of urban architecture: vast stadiums where the public "
        "could watch sporting events were at the centre of western city life as far back as the ancient "
        "Greek and Roman Empires, well before the construction of the great medieval cathedrals and "
        "the grand 19th- and 20th-century railway stations which dominated urban skylines in later eras.\n\n"
        "Today, however, stadiums are regarded with growing scepticism. Construction costs can soar "
        "above £1 billion, and stadiums finished for major events such as the Olympic Games or the "
        "FIFA World Cup have notably fallen into disuse and disrepair.\n\n"
        "But this need not be the case. History shows that stadiums can drive urban development and "
        "adapt to the culture of every age. Even today, architects and planners are finding new ways "
        "to adapt the mono-functional sports arenas which became emblematic of modernisation "
        "during the 20th century.\n\n"
        "B\n"
        "The amphitheatre* of Arles in southwest France, with a capacity of 25,000 spectators, "
        "is perhaps the best example of just how versatile stadiums can be. Built by the Romans in "
        "90 AD, it became a fortress with four towers after the fifth century, and was then "
        "transformed into a village containing more than 200 houses. With the growing interest in "
        "conservation during the 19th century, it was converted back into an arena for the staging of "
        "bullfights, thereby returning the structure to its original use as a venue for public spectacles.\n\n"
        "Another example is the imposing arena of Verona in northern Italy, with space for 30,000 "
        "spectators, which was built 60 years before the Arles amphitheatre and 40 years before "
        "Rome's famous Colosseum. It has endured the centuries and is currently considered one of "
        "the world's prime sites for opera, thanks to its outstanding acoustics.\n\n"
        "C\n"
        "The area in the centre of the Italian town of Lucca, known as the Piazza dell'Anfiteatro, "
        "is yet another impressive example of an amphitheatre becoming absorbed into the fabric "
        "of the city. The site evolved in a similar way to Arles and was progressively filled with "
        "buildings from the Middle Ages until the 19th century, variously used as houses, a salt depot "
        "and a prison. But rather than reverting to an arena, it became a market square, designed "
        "by Romanticist architect Lorenzo Nottolini. Today, the ruins of the amphitheatre remain "
        "embedded in the various shops and residences surrounding the public square.\n\n"
        "D\n"
        "There are many similarities between modern stadiums and the ancient amphitheatres "
        "intended for games. But some of the flexibility was lost at the beginning of the 20th century, "
        "as stadiums were developed using new products such as steel and reinforced concrete, and "
        "made use of bright lights for night-time matches.\n\n"
        "Many such stadiums are situated in suburban areas, designed for sporting use only and "
        "surrounded by parking lots. These factors mean that they may not be as accessible to the "
        "general public, require more energy to run and contribute to urban heat.\n\n"
        "E\n"
        "But many of today's most innovative architects see scope for the stadium to help improve the "
        "city. Among the current strategies, two seem to be having particular success: the stadium as "
        "an urban hub, and as a power plant.\n\n"
        "There's a growing trend for stadiums to be equipped with public spaces and services that "
        "serve a function beyond sport, such as hotels, retail outlets, conference centres, restaurants "
        "and bars, children's playgrounds and green space. Creating mixed-use developments such as "
        "this reinforces compactness and multi-functionality, making more efficient use of land and "
        "helping to regenerate urban spaces.\n\n"
        "This opens the space up to families and a wider cross-section of society, instead of catering "
        "only to sportspeople and supporters. There have been many examples of this in the UK: the "
        "mixed-use facilities at Wembley and Old Trafford have become a blueprint for many other "
        "stadiums in the world.\n\n"
        "F\n"
        "The phenomenon of stadiums as power stations has arisen from the idea that energy "
        "problems can be overcome by integrating interconnected buildings by means of a smart grid, "
        "which is an electricity supply network that uses digital communications technology to detect "
        "and react to local changes in usage, without significant energy losses. Stadiums are ideal "
        "for these purposes, because their canopies have a large surface area for fitting photovoltaic "
        "panels and rise high enough (more than 40 metres) to make use of micro wind turbines.\n\n"
        "Freiburg Mage Solar Stadium in Germany is the first of a new wave of stadiums as power "
        "plants, which also includes the Amsterdam Arena and the Kaohsiung Stadium. The latter, "
        "inaugurated in 2009, has 8,844 photovoltaic panels producing up to 1.14 GWh of electricity "
        "annually. This reduces the annual output of carbon dioxide by 660 tons and supplies up "
        "to 80 percent of the surrounding area when the stadium is not in use. This is proof that a "
        "stadium can serve its city, and have a decidedly positive impact in terms of reduction of CO2 "
        "emissions.\n\n"
        "G\n"
        "Sporting arenas have always been central to the life and culture of cities. In every era, the "
        "stadium has acquired new value and uses: from military fortress to residential village, public "
        "space to theatre and most recently a field for experimentation in advanced engineering. "
        "The stadium of today now brings together multiple functions, thus helping cities to create a "
        "sustainable future."
    )

    passage3_text = (
        "Anna Keay reviews Charles Spencer's book about the hunt for King Charles II "
        "during the English Civil War of the seventeenth century\n\n"
        "Charles Spencer's latest book, To Catch a King, tells us the story of the hunt for King "
        "Charles II in the six weeks after his resounding defeat at the Battle of Worcester in September "
        "1651. And what a story it is. After his father was executed by the Parliamentarians in 1649, "
        "the young Charles II sacrificed one of the very principles his father had died for and "
        "did a deal with the Scots, thereby accepting Presbyterianism* as the national religion in "
        "return for being crowned King of Scots. His arrival in Edinburgh prompted the English "
        "Parliamentary army to invade Scotland in a pre-emptive strike. This was followed by a "
        "Scottish invasion of England. The two sides finally faced one another at Worcester in "
        "the west of England in 1651. After being comprehensively defeated on the meadows "
        "outside the city by the Parliamentarian army, the 21-year-old king found himself the subject "
        "of a national manhunt, with a huge sum offered for his capture. Over the following "
        "six weeks he managed, through a series of heart-poundingly close escapes, to evade the "
        "Parliamentarians before seeking refuge in France. For the next nine years, the penniless "
        "and defeated Charles wandered around Europe with only a small group of loyal supporters.\n\n"
        "Years later, after his restoration as king, the 50-year-old Charles II requested a meeting "
        "with the writer and diarist Samuel Pepys. His intention when asking Pepys to commit his "
        "story to paper was to ensure that this most extraordinary episode was never forgotten. "
        "Over two three-hour sittings, the king related to him in great detail his personal recollections "
        "of the six weeks he had spent as a fugitive. As the king and secretary settled down (a scene "
        "that is surely a gift for a future scriptwriter), Charles commenced his story: 'After the battle "
        "was so absolutely lost as to be beyond hope of recovery, I began to think of the best way of "
        "saving myself.'\n\n"
        "One of the joys of Spencer's book, a result not least of its use of Charles II's own narrative "
        "as well as those of his supporters, is just how close the reader gets to the action. The day-by-"
        "day retelling of the fugitives' doings provides delicious details: the cutting of the king's long "
        "hair with agricultural shears, the use of walnut leaves to dye his pale skin, and the day Charles "
        "spent lying on a branch of the great oak tree in Boscobel Wood as the Parliamentary soldiers "
        "scoured the forest floor below. Spencer draws out both the humour – such as the preposterous "
        "refusal of Charles's friend Henry Wilmot to adopt disguise on the grounds that it was "
        "beneath his dignity – and the emotional tension when the secret of the king's presence was "
        "cautiously revealed to his supporters.\n\n"
        "Charles's adventures after losing the Battle of Worcester hide the uncomfortable truth that "
        "whilst almost everyone in England had been appalled by the execution of his father, they "
        "had not welcomed the arrival of his son with the Scots army, but had instead firmly bolted "
        "their doors. This was partly because he rode at the head of what looked like a foreign invasion "
        "force and partly because, after almost a decade of civil war, people were desperate to avoid "
        "it beginning again. This makes it all the more interesting that Charles II himself loved the "
        "story so much ever after. As well as retelling it to anyone who would listen, causing eye-"
        "rolling among courtiers, he set in train a series of initiatives to memorialise it. There was to "
        "be a new order of chivalry, the Knights of the Royal Oak. A series of enormous oil paintings "
        "depicting the episode were produced, including a two-metre-wide canvas of Boscobel Wood "
        "and a set of six similarly enormous paintings of the king on the run. In 1660, Charles II "
        "commissioned the artist John Michael Wright to paint a flying squadron of cherubs* carrying "
        "an oak tree to the heavens on the ceiling of his bedchamber. It is hard to imagine many other "
        "kings marking the lowest point in their life so enthusiastically, or indeed pulling off such an "
        "escape in the first place.\n\n"
        "Charles Spencer is the perfect person to pass the story on to a new generation. His "
        "pacey, readable prose steers deftly clear of modern idioms and elegantly brings to life the "
        "details of the great tale. He has even-handed sympathy for both the fugitive king and the "
        "fierce republican regime that hunted him, and he succeeds in his desire to explore far "
        "more of the background of the story than previous books on the subject have done. Indeed, "
        "the opening third of the book is about how Charles II found himself at Worcester in the first "
        "place, which for some will be reason alone to read To Catch a King.\n\n"
        "The tantalising question left, in the end, is that of what it all meant. Would Charles II have "
        "been a different king had these six weeks never happened? The days and nights spent in hiding "
        "must have affected him in some way. Did the need to assume disguises, to survive on wit and "
        "charm alone, to use trickery and subterfuge to escape from tight corners help form him? This "
        "is the one area where the book doesn't quite hit the mark. Instead its depiction of Charles II in "
        "his final years as an ineffective, pleasure-loving monarch doesn't do justice to the man (neither "
        "is it accurate), or to the complexity of his character. But this one niggle aside, To Catch a "
        "King is an excellent read, and those who come to it knowing little of the famous tale will find "
        "they have a treat in store."
    )

    return {
        "id": "cam17",
        "title": "Cambridge IELTS 17 Academic Reading",
        "totalQuestions": 40,
        "passages": [
            {
                "id": "cam17_p1",
                "title": "The development of the London underground railway",
                "text": passage1_text,
                "timeRecommended": 20,
                "questions": [
                    # Questions 1-6: notes completion (ONE WORD ONLY)
                    {"id": "cam17_r_q1", "type": "notes_completion", "question": "The 1. _____ of London increased rapidly between 1800 and 1850", "options": [], "correctAnswer": "population",
                     "explanation": "EN: The first sentence states 'London's population grew at an astonishing rate'.|CN: 第一句提到'伦敦的人口以惊人的速度增长'。"},
                    {"id": "cam17_r_q2", "type": "notes_completion", "question": "Building the railway would make it possible to move people to better housing in the 2. _____", "options": [], "correctAnswer": "suburbs",
                     "explanation": "EN: Pearson's idea was 'to relocate the poor workers who lived in the inner-city slums to newly constructed suburbs'.|CN: Pearson的想法是'将住在市中心贫民窟的贫困工人迁往新建的郊区'。"},
                    {"id": "cam17_r_q3", "type": "notes_completion", "question": "A number of 3. _____ agreed with Pearson's idea", "options": [], "correctAnswer": "businessmen",
                     "explanation": "EN: 'Pearson's ideas gained support amongst some businessmen'.|CN: 'Pearson的想法得到了一些商人的支持'。"},
                    {"id": "cam17_r_q4", "type": "notes_completion", "question": "The company initially had problems getting the 4. _____ needed for the project", "options": [], "correctAnswer": "funding",
                     "explanation": "EN: 'The organisation had difficulty in raising the funding'.|CN: '该组织难以筹集资金'。"},
                    {"id": "cam17_r_q5", "type": "notes_completion", "question": "Negative articles about the project appeared in the 5. _____", "options": [], "correctAnswer": "press",
                     "explanation": "EN: 'not least because of the critical articles printed by the press'.|CN: '尤其是因为媒体刊登的批评文章'。"},
                    {"id": "cam17_r_q6", "type": "notes_completion", "question": "With the completion of the brick arch, the tunnel was covered with 6. _____", "options": [], "correctAnswer": "soil",
                     "explanation": "EN: 'A two-metre-deep layer of soil was laid on top of the tunnel'.|CN: '隧道顶部铺设了两米深的土层'。"},
                    # Questions 7-13: TRUE/FALSE/NOT GIVEN
                    {"id": "cam17_r_q7", "type": "tfng", "question": "Other countries had built underground railways before the Metropolitan line opened.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE",
                     "explanation": "EN: The passage states the Metropolitan line 'was the world's first underground railway', contradicting this claim.|CN: 文章指出Metropolitan线是'世界上第一条地下铁路'，与此说法矛盾。"},
                    {"id": "cam17_r_q8", "type": "tfng", "question": "More people than predicted travelled on the Metropolitan line on the first day.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "NOT GIVEN",
                     "explanation": "EN: The passage gives passenger numbers (40,000) but does not mention any predictions to compare against.|CN: 文章给出了乘客人数(40,000)，但未提及任何预测数据可作比较。"},
                    {"id": "cam17_r_q9", "type": "tfng", "question": "The use of ventilation shafts failed to prevent pollution in the tunnels.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "TRUE",
                     "explanation": "EN: 'smoke and fumes remained a problem, even though ventilation shafts were added to the tunnels'.|CN: '尽管在隧道中增加了通风井，烟雾和废气仍然是一个问题'。"},
                    {"id": "cam17_r_q10", "type": "tfng", "question": "A different approach from the 'cut and cover' technique was required in London's central area.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "TRUE",
                     "explanation": "EN: 'The \"cut and cover\" method of construction was not an option in this part of the capital. The only alternative was to tunnel deep underground.'|CN: '在首都的这一地区，\"挖填\"施工方法不可行。唯一的替代方案是深挖地下隧道'。"},
                    {"id": "cam17_r_q11", "type": "tfng", "question": "The windows on City & South London trains were at eye level.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE",
                     "explanation": "EN: 'The carriages were narrow and had tiny windows just below the roof', meaning they were NOT at eye level.|CN: '车厢很窄，窗户很小，就在车顶下方'，说明窗户不在视线高度。"},
                    {"id": "cam17_r_q12", "type": "tfng", "question": "The City & South London Railway was a financial success.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "FALSE",
                     "explanation": "EN: 'Although the City & South London Railway was a great technical achievement, it did not make a profit.'|CN: '尽管City & South London Railway是一项伟大的技术成就，但它并没有盈利'。"},
                    {"id": "cam17_r_q13", "type": "tfng", "question": "Trains on the 'Tuppenny Tube' nearly always ran on time.", "options": ["TRUE", "FALSE", "NOT GIVEN"], "correctAnswer": "NOT GIVEN",
                     "explanation": "EN: The passage says the Tuppenny Tube was 'very popular' but does not mention punctuality.|CN: 文章说Tuppenny Tube'非常受欢迎'，但未提及其是否准时。"},
                ]
            },
            {
                "id": "cam17_p2",
                "title": "Stadiums: past, present and future",
                "text": passage2_text,
                "timeRecommended": 20,
                "questions": [
                    # Questions 14-17: matching paragraph information
                    {"id": "cam17_r_q14", "type": "matching_info", "question": "a mention of negative attitudes towards stadium building projects (Section ___)", "options": ["A", "B", "C", "D", "E", "F", "G"], "correctAnswer": "A",
                     "explanation": "EN: Section A states 'Today, however, stadiums are regarded with growing scepticism'.|CN: A段提到'然而，如今人们对体育场越来越持怀疑态度'。"},
                    {"id": "cam17_r_q15", "type": "matching_info", "question": "figures demonstrating the environmental benefits of a certain stadium (Section ___)", "options": ["A", "B", "C", "D", "E", "F", "G"], "correctAnswer": "F",
                     "explanation": "EN: Section F provides figures: '8,844 photovoltaic panels producing up to 1.14 GWh... reduces the annual output of carbon dioxide by 660 tons'.|CN: F段提供了数据：'8,844块光伏板每年产生高达1.14 GWh...每年减少660吨二氧化碳排放'。"},
                    {"id": "cam17_r_q16", "type": "matching_info", "question": "examples of the wide range of facilities available at some new stadiums (Section ___)", "options": ["A", "B", "C", "D", "E", "F", "G"], "correctAnswer": "E",
                     "explanation": "EN: Section E lists 'hotels, retail outlets, conference centres, restaurants and bars, children's playgrounds and green space'.|CN: E段列出'酒店、零售店、会议中心、餐厅和酒吧、儿童游乐场和绿地'。"},
                    {"id": "cam17_r_q17", "type": "matching_info", "question": "reference to the disadvantages of the stadiums built during a certain era (Section ___)", "options": ["A", "B", "C", "D", "E", "F", "G"], "correctAnswer": "D",
                     "explanation": "EN: Section D mentions 'some of the flexibility was lost at the beginning of the 20th century' and lists disadvantages of modern stadiums.|CN: D段提到'在20世纪初，一些灵活性丧失了'并列出问题。"},
                    # Questions 18-22: sentence completion (ONE WORD ONLY)
                    {"id": "cam17_r_q18", "type": "summary_completion", "question": "The amphitheatre of Arles was converted first into a 18. _____", "options": [], "correctAnswer": "fortress",
                     "explanation": "EN: 'it became a fortress with four towers after the fifth century'.|CN: '公元五世纪后，它成为了一座带有四座塔楼的堡垒'。"},
                    {"id": "cam17_r_q19", "type": "summary_completion", "question": "and finally into an arena where spectators could watch 19. _____", "options": [], "correctAnswer": "bullfights",
                     "explanation": "EN: 'it was converted back into an arena for the staging of bullfights'.|CN: '它被改回为斗牛场'。"},
                    {"id": "cam17_r_q20", "type": "summary_completion", "question": "the arena in Verona is famous today as a venue where 20. _____ is performed", "options": [], "correctAnswer": "opera",
                     "explanation": "EN: 'one of the world's prime sites for opera'.|CN: '世界上最重要的歌剧演出场地之一'。"},
                    {"id": "cam17_r_q21", "type": "summary_completion", "question": "Lucca's amphitheatre has been used including the storage of 21. _____", "options": [], "correctAnswer": "salt",
                     "explanation": "EN: 'variously used as houses, a salt depot and a prison'.|CN: '被用作房屋、盐仓和监狱'。"},
                    {"id": "cam17_r_q22", "type": "summary_completion", "question": "It is now a market square with 22. _____ and homes incorporated into the remains", "options": [], "correctAnswer": "shops",
                     "explanation": "EN: 'the ruins of the amphitheatre remain embedded in the various shops and residences'.|CN: '竞技场的废墟仍然镶嵌在各类商店和住宅之中'。"},
                    # Questions 23-24: TWO correct answers
                    {"id": "cam17_r_q23", "type": "multiple_choice_multi", "question": "Which TWO negative features does the writer mention when comparing twentieth-century stadiums to ancient amphitheatres? (Choose TWO)", "options": ["A. They are less imaginatively designed.", "B. They are less spacious.", "C. They are in less convenient locations.", "D. They are less versatile.", "E. They are made of less durable materials."], "correctAnswer": "C,D",
                     "explanation": "EN: Section D mentions they are in 'suburban areas' (less convenient, C) and that 'some of the flexibility was lost' (less versatile, D).|CN: D段提到它们位于'郊区'(交通不便，C)且'丧失了一些灵活性'(用途单一，D)。"},
                    {"id": "cam17_r_q24", "type": "multiple_choice_multi", "question": "Same as Q23 - select the second option", "options": ["A. They are less imaginatively designed.", "B. They are less spacious.", "C. They are in less convenient locations.", "D. They are less versatile.", "E. They are made of less durable materials."], "correctAnswer": "C,D",
                     "explanation": "EN: Both C and D are mentioned as negative features in Section D.|CN: C和D都是D段提到的负面特征。"},
                    # Questions 25-26: TWO correct answers
                    {"id": "cam17_r_q25", "type": "multiple_choice_multi", "question": "Which TWO advantages of modern stadium design does the writer mention? (Choose TWO)", "options": ["A. offering improved amenities for the enjoyment of sports events", "B. bringing community life back into the city environment", "C. facilitating research into solar and wind energy solutions", "D. enabling local residents to reduce their consumption of electricity", "E. providing a suitable site for the installation of renewable power generators"], "correctAnswer": "B,E",
                     "explanation": "EN: Section E discusses 'helping to regenerate urban spaces' (B) and Section F discusses fitting photovoltaic panels and wind turbines (E).|CN: E段讨论'帮助重建城市空间'(B)，F段讨论安装光伏板和风力涡轮机(E)。"},
                    {"id": "cam17_r_q26", "type": "multiple_choice_multi", "question": "Same as Q25 - select the second option", "options": ["A. offering improved amenities for the enjoyment of sports events", "B. bringing community life back into the city environment", "C. facilitating research into solar and wind energy solutions", "D. enabling local residents to reduce their consumption of electricity", "E. providing a suitable site for the installation of renewable power generators"], "correctAnswer": "B,E",
                     "explanation": "EN: Both B and E are mentioned as advantages of modern stadium design.|CN: B和E都是现代体育场设计的优势。"},
                ]
            },
            {
                "id": "cam17_p3",
                "title": "To catch a king",
                "text": passage3_text,
                "timeRecommended": 20,
                "questions": [
                    # Questions 27-31: summary completion (phrases A-J)
                    {"id": "cam17_r_q27", "type": "matching_sentence", "question": "Charles II then formed a 27. _____ with the Scots", "options": ["A. military innovation", "B. large reward", "C. widespread conspiracy", "D. relative safety", "E. new government", "F. decisive victory", "G. political debate", "H. strategic alliance", "I. popular solution", "J. religious conviction"], "correctAnswer": "H",
                     "explanation": "EN: 'did a deal with the Scots, thereby accepting Presbyterianism as the national religion in return for being crowned King of Scots' — a strategic alliance.|CN: '与苏格兰人达成协议...作为回报被加冕为苏格兰国王'——这是一个战略联盟。"},
                    {"id": "cam17_r_q28", "type": "matching_sentence", "question": "he abandoned an important 28. _____ that was held by his father", "options": ["A. military innovation", "B. large reward", "C. widespread conspiracy", "D. relative safety", "E. new government", "F. decisive victory", "G. political debate", "H. strategic alliance", "I. popular solution", "J. religious conviction"], "correctAnswer": "J",
                     "explanation": "EN: 'Charles II sacrificed one of the very principles his father had died for' — religious conviction (his father died for refusing Presbyterianism).|CN: 'Charles II牺牲了他父亲为之献身的重要原则之一'——宗教信仰。"},
                    {"id": "cam17_r_q29", "type": "matching_sentence", "question": "The battle led to a 29. _____ for the Parliamentarians", "options": ["A. military innovation", "B. large reward", "C. widespread conspiracy", "D. relative safety", "E. new government", "F. decisive victory", "G. political debate", "H. strategic alliance", "I. popular solution", "J. religious conviction"], "correctAnswer": "F",
                     "explanation": "EN: 'After being comprehensively defeated on the meadows outside the city by the Parliamentarian army' — a decisive victory for the Parliamentarians.|CN: '在城外的草地上被议会军全面击败'——议会军取得了决定性胜利。"},
                    {"id": "cam17_r_q30", "type": "matching_sentence", "question": "A 30. _____ was offered for Charles's capture", "options": ["A. military innovation", "B. large reward", "C. widespread conspiracy", "D. relative safety", "E. new government", "F. decisive victory", "G. political debate", "H. strategic alliance", "I. popular solution", "J. religious conviction"], "correctAnswer": "B",
                     "explanation": "EN: 'with a huge sum offered for his capture' — a large reward.|CN: '悬赏巨额赏金抓捕他'——巨额赏金。"},
                    {"id": "cam17_r_q31", "type": "matching_sentence", "question": "he eventually managed to reach the 31. _____ of continental Europe", "options": ["A. military innovation", "B. large reward", "C. widespread conspiracy", "D. relative safety", "E. new government", "F. decisive victory", "G. political debate", "H. strategic alliance", "I. popular solution", "J. religious conviction"], "correctAnswer": "D",
                     "explanation": "EN: 'before seeking refuge in France' — finding relative safety in continental Europe.|CN: '在寻求法国避难之前'——在欧洲大陆找到相对安全的地方。"},
                    # Questions 32-35: YES/NO/NOT GIVEN
                    {"id": "cam17_r_q32", "type": "ynng", "question": "Charles chose Pepys for the task because he considered him to be trustworthy.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "NOT GIVEN",
                     "explanation": "EN: The passage says Charles II asked Pepys to commit his story to paper, but does not state the reason for choosing Pepys.|CN: 文章说Charles II请Pepys记录他的故事，但未说明选择Pepys的原因。"},
                    {"id": "cam17_r_q33", "type": "ynng", "question": "Charles's personal recollection of the escape lacked sufficient detail.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "NO",
                     "explanation": "EN: 'the king related to him in great detail his personal recollections' — the recollection had great detail.|CN: '国王向他详细讲述了他的个人回忆'——回忆非常详细。"},
                    {"id": "cam17_r_q34", "type": "ynng", "question": "Charles indicated to Pepys that he had planned his escape before the battle.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "NO",
                     "explanation": "EN: Charles said 'After the battle was so absolutely lost... I began to think of the best way of saving myself' — he planned AFTER the battle.|CN: Charles说'战斗完全失败后...我才开始想如何自救'——他是在战斗之后才计划的。"},
                    {"id": "cam17_r_q35", "type": "ynng", "question": "The inclusion of Charles's account is a positive aspect of the book.", "options": ["YES", "NO", "NOT GIVEN"], "correctAnswer": "YES",
                     "explanation": "EN: 'One of the joys of Spencer's book, a result not least of its use of Charles II's own narrative... is just how close the reader gets to the action.'|CN: 'Spencer这本书的乐趣之一...就在于读者能如此贴近事件本身'。"},
                    # Questions 36-40: multiple choice
                    {"id": "cam17_r_q36", "type": "multiple_choice", "question": "What is the reviewer's main purpose in the first paragraph?",
                     "options": ["A. to describe what happened during the Battle of Worcester", "B. to give an account of the circumstances leading to Charles II's escape", "C. to provide details of the Parliamentarians' political views", "D. to compare Charles II's beliefs with those of his father"], "correctAnswer": "B",
                     "explanation": "EN: The first paragraph describes the events and circumstances that led to Charles II becoming a fugitive.|CN: 第一段描述了导致Charles II成为逃犯的事件和背景。"},
                    {"id": "cam17_r_q37", "type": "multiple_choice", "question": "Why does the reviewer include examples of the fugitives' behaviour in the third paragraph?",
                     "options": ["A. to explain how close Charles II came to losing his life", "B. to suggest that Charles II's supporters were badly prepared", "C. to illustrate how the events of the six weeks are brought to life", "D. to argue that certain aspects are not as well known as they should be"], "correctAnswer": "C",
                     "explanation": "EN: The paragraph states 'The day-by-day retelling of the fugitives' doings provides delicious details' — showing how the book brings events to life.|CN: 该段提到'逐日复述逃亡者的所作所为提供了生动的细节'——展示这本书如何让事件栩栩如生。"},
                    {"id": "cam17_r_q38", "type": "multiple_choice", "question": "What point does the reviewer make about Charles II in the fourth paragraph?",
                     "options": ["A. He chose to celebrate what was essentially a defeat.", "B. He misunderstood the motives of his opponents.", "C. He aimed to restore people's faith in the monarchy.", "D. He was driven by a desire to be popular."], "correctAnswer": "A",
                     "explanation": "EN: 'It is hard to imagine many other kings marking the lowest point in their life so enthusiastically' — he celebrated his defeat.|CN: '很难想象有多少国王会如此热情地纪念自己人生的最低谷'——他庆祝了自己的失败。"},
                    {"id": "cam17_r_q39", "type": "multiple_choice", "question": "What does the reviewer say about Charles Spencer in the fifth paragraph?",
                     "options": ["A. His decision to write the book comes as a surprise.", "B. He takes an unbiased approach to the subject matter.", "C. His descriptions of events would be better if they included more detail.", "D. He chooses language that is suitable for a twenty-first-century audience."], "correctAnswer": "B",
                     "explanation": "EN: 'He has even-handed sympathy for both the fugitive king and the fierce republican regime that hunted him' — showing unbiased approach.|CN: '他对逃亡的国王和追捕他的严厉共和政权都抱有公正的同情'——展示了公正的态度。"},
                    {"id": "cam17_r_q40", "type": "multiple_choice", "question": "When the reviewer says the book 'doesn't quite hit the mark', she is making the point that",
                     "options": ["A. it overlooks the impact of events on ordinary people.", "B. it lacks an analysis of prevalent views on monarchy.", "C. it omits any references to the deceit practised by Charles II during his time in hiding.", "D. it fails to address whether Charles II's experiences had a lasting influence on him."], "correctAnswer": "D",
                     "explanation": "EN: 'This is the one area where the book doesn't quite hit the mark. Instead its depiction of Charles II in his final years as an ineffective, pleasure-loving monarch doesn't do justice to the man' — failing to address the lasting influence of the experience.|CN: '这是该书唯一不太到位的地方...它把Charles II晚年描绘成一个无能、享乐的君主，对这个人和他性格的复杂性都不够公正'。"},
                ]
            }
        ]
    }


def create_listening_json():
    """Create listening.json with Test 1 sections and questions."""
    return {
        "id": "cam17",
        "title": "Cambridge IELTS 17 Listening",
        "totalQuestions": 40,
        "sections": [
            {
                "id": "cam17_l_s1",
                "title": "Part 1: Buckworth Conservation Group",
                "subtitle": "A conversation about volunteering activities at a conservation group",
                "audioFile": "cam17_s1.mp3",
                "duration": 480,
                "questions": [
                    {"id": "cam17_l_q1", "type": "form_completion", "question": "making sure the beach does not have 1. _____ on it", "options": [], "correctAnswer": "litter",
                     "explanation": "EN: The speaker mentions making sure the beach doesn't have litter.|CN: 说话者提到确保海滩没有垃圾。"},
                    {"id": "cam17_l_q2", "type": "form_completion", "question": "no 2. _____", "options": [], "correctAnswer": "dogs",
                     "explanation": "EN: Dogs are not allowed on the beach.|CN: 海滩上不允许带狗。"},
                    {"id": "cam17_l_q3", "type": "form_completion", "question": "next task is taking action to attract 3. _____ to the place", "options": [], "correctAnswer": "insects",
                     "explanation": "EN: Taking action to attract insects to the nature reserve.|CN: 采取行动吸引昆虫到自然保护区。"},
                    {"id": "cam17_l_q4", "type": "form_completion", "question": "identifying types of 4. _____", "options": [], "correctAnswer": "butterflies",
                     "explanation": "EN: Identifying different types of butterflies.|CN: 识别不同类型的蝴蝶。"},
                    {"id": "cam17_l_q5", "type": "form_completion", "question": "building a new 5. _____", "options": [], "correctAnswer": "wall",
                     "explanation": "EN: Building a new wall at the site.|CN: 在场地上建造一堵新墙。"},
                    {"id": "cam17_l_q6", "type": "form_completion", "question": "walk across the sands and reach the 6. _____", "options": [], "correctAnswer": "island",
                     "explanation": "EN: Walking across the sands to reach the island.|CN: 穿过沙滩到达岛屿。"},
                    {"id": "cam17_l_q7", "type": "form_completion", "question": "wear appropriate 7. _____", "options": [], "correctAnswer": "boots",
                     "explanation": "EN: Need to wear appropriate boots for the walk.|CN: 需要穿合适的靴子。"},
                    {"id": "cam17_l_q8", "type": "form_completion", "question": "suitable for 8. _____ to participate in", "options": [], "correctAnswer": "beginners",
                     "explanation": "EN: The woodwork session is suitable for beginners.|CN: 木工活动适合初学者参加。"},
                    {"id": "cam17_l_q9", "type": "form_completion", "question": "making 9. _____ out of wood", "options": [], "correctAnswer": "spoons",
                     "explanation": "EN: Making spoons out of wood.|CN: 用木头制作勺子。"},
                    {"id": "cam17_l_q10", "type": "form_completion", "question": "cost of session (no camping): 10. £ _____", "options": [], "correctAnswer": "35 / thirty five",
                     "explanation": "EN: The cost is 35 pounds without camping.|CN: 不含露营的费用是35英镑。"},
                ]
            },
            {
                "id": "cam17_l_s2",
                "title": "Part 2: Boat trip round Tasmania",
                "subtitle": "A tour guide introduces a boat trip around Tasmania",
                "audioFile": "cam17_s2.mp3",
                "duration": 480,
                "questions": [
                    {"id": "cam17_l_q11", "type": "multiple_choice", "question": "What is the maximum number of people who can stand on each side of the boat?",
                     "options": ["A. 9", "B. 15", "C. 18"], "correctAnswer": "A",
                     "explanation": "EN: Maximum 9 people on each side of the boat.|CN: 船的每侧最多站9人。"},
                    {"id": "cam17_l_q12", "type": "multiple_choice", "question": "What colour are the tour boats?",
                     "options": ["A. dark red", "B. jet black", "C. light green"], "correctAnswer": "C",
                     "explanation": "EN: The tour boats are light green in colour.|CN: 观光船是浅绿色的。"},
                    {"id": "cam17_l_q13", "type": "multiple_choice", "question": "Which lunchbox is suitable for someone who doesn't eat meat or fish?",
                     "options": ["A. Lunchbox 1", "B. Lunchbox 2", "C. Lunchbox 3"], "correctAnswer": "B",
                     "explanation": "EN: Lunchbox 2 is suitable for vegetarians — no meat or fish.|CN: 午餐盒2适合素食者——不含肉或鱼。"},
                    {"id": "cam17_l_q14", "type": "multiple_choice", "question": "What should people do with their litter?",
                     "options": ["A. take it home", "B. hand it to a member of staff", "C. put it in the bins provided on the boat"], "correctAnswer": "B",
                     "explanation": "EN: Hand litter to a member of staff.|CN: 将垃圾交给工作人员。"},
                    {"id": "cam17_l_q15", "type": "multiple_choice_multi", "question": "Which TWO features of the lighthouse does Lou mention? (Select TWO)",
                     "options": ["A. why it was built", "B. who built it", "C. how long it took to build", "D. who staffed it", "E. what it was built with"], "correctAnswer": "A,D",
                     "explanation": "EN: Lou mentions why the lighthouse was built (A) and who staffed it (D).|CN: Lou提到了灯塔建造的原因(A)和灯塔的工作人员(D)。"},
                    {"id": "cam17_l_q16", "type": "multiple_choice_multi", "question": "Same as Q15 — select the second option", "options": ["A. why it was built", "B. who built it", "C. how long it took to build", "D. who staffed it", "E. what it was built with"], "correctAnswer": "A,D",
                     "explanation": "EN: Both A and D are mentioned by Lou.|CN: Lou提到了A和D。"},
                    {"id": "cam17_l_q17", "type": "multiple_choice_multi", "question": "Which TWO types of creature might come close to the boat? (Select TWO)",
                     "options": ["A. sea eagles", "B. fur seals", "C. dolphins", "D. whales", "E. penguins"], "correctAnswer": "B,C",
                     "explanation": "EN: Fur seals and dolphins might come close to the boat.|CN: 海狗和海豚可能会靠近船只。"},
                    {"id": "cam17_l_q18", "type": "multiple_choice_multi", "question": "Same as Q17 — select the second option", "options": ["A. sea eagles", "B. fur seals", "C. dolphins", "D. whales", "E. penguins"], "correctAnswer": "B,C",
                     "explanation": "EN: Both B and C are mentioned as creatures that might come close.|CN: B和C都被提到可能会靠近的动物。"},
                    {"id": "cam17_l_q19", "type": "multiple_choice_multi", "question": "Which TWO points does Lou make about the caves? (Select TWO)",
                     "options": ["A. Only large tourist boats can visit them.", "B. The entrances to them are often blocked.", "C. It is too dangerous for individuals to go near them.", "D. Someone will explain what is inside them.", "E. They cannot be reached on foot."], "correctAnswer": "D,E",
                     "explanation": "EN: Someone will explain the inside (D) and they cannot be reached on foot (E).|CN: 有人会讲解里面的内容(D)，且步行无法到达(E)。"},
                    {"id": "cam17_l_q20", "type": "multiple_choice_multi", "question": "Same as Q19 — select the second option", "options": ["A. Only large tourist boats can visit them.", "B. The entrances to them are often blocked.", "C. It is too dangerous for individuals to go near them.", "D. Someone will explain what is inside them.", "E. They cannot be reached on foot."], "correctAnswer": "D,E",
                     "explanation": "EN: Both D and E are correct points made by Lou.|CN: D和E都是Lou提到的正确观点。"},
                ]
            },
            {
                "id": "cam17_l_s3",
                "title": "Part 3: Work experience for veterinary science students",
                "subtitle": "Two students discuss their work experience on farms",
                "audioFile": "cam17_s3.mp3",
                "duration": 480,
                "questions": [
                    {"id": "cam17_l_q21", "type": "multiple_choice", "question": "What problem did both Diana and Tim have when arranging their work experience?",
                     "options": ["A. making initial contact with suitable farms", "B. organising transport to and from the farm", "C. finding a placement for the required length of time"], "correctAnswer": "A",
                     "explanation": "EN: Both had difficulty making initial contact with suitable farms.|CN: 两人在联系合适的农场时都遇到了困难。"},
                    {"id": "cam17_l_q22", "type": "multiple_choice", "question": "Tim was pleased to be able to help",
                     "options": ["A. a lamb that had a broken leg.", "B. a sheep that was having difficulty giving birth.", "C. a newly born lamb that was having trouble feeding."], "correctAnswer": "B",
                     "explanation": "EN: Tim helped a sheep having difficulty giving birth (lambing).|CN: Tim帮助了一只有分娩困难的羊。"},
                    {"id": "cam17_l_q23", "type": "multiple_choice", "question": "Diana says the sheep on her farm",
                     "options": ["A. were of various different varieties.", "B. were mainly reared for their meat.", "C. had better quality wool than sheep on the hills."], "correctAnswer": "B",
                     "explanation": "EN: The sheep were mainly reared for their meat.|CN: 这些羊主要是为了肉而饲养的。"},
                    {"id": "cam17_l_q24", "type": "multiple_choice", "question": "What did the students learn about adding supplements to chicken feed?",
                     "options": ["A. These should only be given if specially needed.", "B. It is worth paying extra for the most effective ones.", "C. The amount given at one time should be limited."], "correctAnswer": "A",
                     "explanation": "EN: Supplements should only be given if specially needed.|CN: 只有在特别需要时才给予补充剂。"},
                    {"id": "cam17_l_q25", "type": "multiple_choice", "question": "What happened when Diana was working with dairy cows?",
                     "options": ["A. She identified some cows incorrectly.", "B. She accidentally threw some milk away.", "C. She made a mistake when storing milk."], "correctAnswer": "C",
                     "explanation": "EN: Diana made a mistake when storing milk.|CN: Diana在储存牛奶时犯了个错误。"},
                    {"id": "cam17_l_q26", "type": "multiple_choice", "question": "What did both farmers mention about vets and farming?",
                     "options": ["A. Vets are failing to cope with some aspects of animal health.", "B. There needs to be a fundamental change in the training of vets.", "C. Some jobs could be done by the farmer rather than by a vet."], "correctAnswer": "C",
                     "explanation": "EN: Some jobs could be done by farmers rather than vets.|CN: 一些工作可以由农场主而不是兽医来完成。"},
                    {"id": "cam17_l_q27", "type": "matching", "question": "Medical terminology module — what opinion?",
                     "options": ["A. Tim found this easier than expected.", "B. Tim thought this was not very clearly organised.", "C. Diana may do some further study on this.", "D. They both found the reading required for this was difficult.", "E. Tim was shocked at something he learned on this module.", "F. They were both surprised how little is known about some aspects of this."], "correctAnswer": "A",
                     "explanation": "EN: Tim found medical terminology easier than expected.|CN: Tim发现医学术语模块比预期的简单。"},
                    {"id": "cam17_l_q28", "type": "matching", "question": "Diet and nutrition module — what opinion?",
                     "options": ["A. Tim found this easier than expected.", "B. Tim thought this was not very clearly organised.", "C. Diana may do some further study on this.", "D. They both found the reading required for this was difficult.", "E. Tim was shocked at something he learned on this module.", "F. They were both surprised how little is known about some aspects of this."], "correctAnswer": "E",
                     "explanation": "EN: Tim was shocked at something he learned on the diet and nutrition module.|CN: Tim在饮食与营养模块中学到的东西让他感到震惊。"},
                    {"id": "cam17_l_q29", "type": "matching", "question": "Animal disease module — what opinion?",
                     "options": ["A. Tim found this easier than expected.", "B. Tim thought this was not very clearly organised.", "C. Diana may do some further study on this.", "D. They both found the reading required for this was difficult.", "E. Tim was shocked at something he learned on this module.", "F. They were both surprised how little is known about some aspects of this."], "correctAnswer": "F",
                     "explanation": "EN: They were both surprised how little is known about some aspects of animal disease.|CN: 两人都惊讶于对动物疾病某些方面的了解如此之少。"},
                    {"id": "cam17_l_q30", "type": "matching", "question": "Wildlife medication module — what opinion?",
                     "options": ["A. Tim found this easier than expected.", "B. Tim thought this was not very clearly organised.", "C. Diana may do some further study on this.", "D. They both found the reading required for this was difficult.", "E. Tim was shocked at something he learned on this module.", "F. They were both surprised how little is known about some aspects of this."], "correctAnswer": "C",
                     "explanation": "EN: Diana may do some further study on wildlife medication.|CN: Diana可能会在野生动物药物治疗方面做进一步研究。"},
                ]
            },
            {
                "id": "cam17_l_s4",
                "title": "Part 4: Labyrinths",
                "subtitle": "A lecture about the history and significance of labyrinths",
                "audioFile": "cam17_s4.mp3",
                "duration": 480,
                "questions": [
                    {"id": "cam17_l_q31", "type": "form_completion", "question": "Mazes are a type of 31. _____", "options": [], "correctAnswer": "puzzle",
                     "explanation": "EN: Mazes are a type of puzzle.|CN: 迷宫是一种谜题。"},
                    {"id": "cam17_l_q32", "type": "form_completion", "question": "32. _____ is needed to navigate through a maze", "options": [], "correctAnswer": "logic",
                     "explanation": "EN: Logic is needed to navigate through a maze.|CN: 需要通过逻辑来穿越迷宫。"},
                    {"id": "cam17_l_q33", "type": "form_completion", "question": "the word 'maze' is derived from a word meaning a feeling of 33. _____", "options": [], "correctAnswer": "confusion",
                     "explanation": "EN: 'Maze' comes from a word meaning confusion.|CN: 'Maze'源自一个表示困惑的词汇。"},
                    {"id": "cam17_l_q34", "type": "form_completion", "question": "they have frequently been used in 34. _____ and prayer", "options": [], "correctAnswer": "meditation",
                     "explanation": "EN: Labyrinths have been used in meditation and prayer.|CN: 迷宫常用于冥想和祈祷。"},
                    {"id": "cam17_l_q35", "type": "form_completion", "question": "Ancient carvings on 35. _____ have been found across many cultures", "options": [], "correctAnswer": "stone",
                     "explanation": "EN: Ancient stone carvings of labyrinth patterns have been found.|CN: 古代石刻迷宫图案已在许多文化中被发现。"},
                    {"id": "cam17_l_q36", "type": "form_completion", "question": "Ancient Greeks used the symbol on 36. _____", "options": [], "correctAnswer": "coins",
                     "explanation": "EN: Ancient Greeks used the labyrinth symbol on coins.|CN: 古希腊人在硬币上使用迷宫符号。"},
                    {"id": "cam17_l_q37", "type": "form_completion", "question": "The largest surviving example of a turf labyrinth once had a big 37. _____ at its centre", "options": [], "correctAnswer": "tree",
                     "explanation": "EN: The turf labyrinth once had a big tree at its centre.|CN: 草皮迷宫的中心曾有一棵大树。"},
                    {"id": "cam17_l_q38", "type": "form_completion", "question": "walking a maze can reduce a person's 38. _____ rate", "options": [], "correctAnswer": "breathing",
                     "explanation": "EN: Walking a labyrinth can reduce a person's breathing rate.|CN: 走迷宫可以降低人的呼吸频率。"},
                    {"id": "cam17_l_q39", "type": "form_completion", "question": "patients who can't walk can use 'finger labyrinths' made from 39. _____", "options": [], "correctAnswer": "paper",
                     "explanation": "EN: Finger labyrinths made from paper are available for those who cannot walk.|CN: 对于无法行走的患者，可以使用纸质手指迷宫。"},
                    {"id": "cam17_l_q40", "type": "form_completion", "question": "Alzheimer's sufferers experience less 40. _____", "options": [], "correctAnswer": "anxiety",
                     "explanation": "EN: Research shows Alzheimer's sufferers experience less anxiety after using labyrinths.|CN: 研究表明阿尔茨海默病患者使用迷宫后焦虑减轻。"},
                ]
            },
        ]
    }


def create_writing_json():
    """Create writing.json with Test 1 tasks."""
    return {
        "id": "cam17",
        "title": "Cambridge IELTS 17 Academic Writing",
        "task1": {
            "title": "Norbiton Industrial Area — Maps",
            "description": "The maps below show an industrial area in the town of Norbiton, and planned future development of the site.\nSummarise the information by selecting and reporting the main features, and make comparisons where relevant.",
            "wordLimit": 150,
            "suggestedTime": 20,
            "type": "map_comparison",
            "imageDescription": "Two maps showing: (1) Norbiton industrial area now — showing factories by a river with farmland to the east, separated from the town by the river; (2) Planned future development — factories replaced with housing, a medical centre, playground, school, and shops, with farmland remaining to the east."
        },
        "task2": {
            "title": "Taking Risks",
            "description": "It is important for people to take risks, both in their professional lives and their personal lives.\nDo you think the advantages of taking risks outweigh the disadvantages?",
            "wordLimit": 250,
            "suggestedTime": 40,
            "type": "opinion_essay",
            "topic": "Risk-taking in professional and personal life"
        },
        "sampleEssays": {
            "task1": "[Sample essay for Task 1 - needs extraction]",
            "task2": "[Sample essay for Task 2 - needs extraction]"
        }
    }


def create_speaking_json():
    """Create speaking.json with Test 1 topics."""
    return {
        "id": "cam17",
        "title": "Cambridge IELTS 17 Speaking",
        "part1": {
            "topic": "History",
            "questions": [
                {"id": "cam17_s_p1q1", "question": "What did you study in history lessons when you were at school?"},
                {"id": "cam17_s_p1q2", "question": "Did you enjoy studying history at school? [Why/Why not?]"},
                {"id": "cam17_s_p1q3", "question": "How often do you watch TV programmes about history now? [Why/Why not?]"},
                {"id": "cam17_s_p1q4", "question": "What period in history would you like to learn more about? [Why?]"}
            ]
        },
        "part2": {
            "topic": "Describe the neighbourhood you lived in when you were a child.",
            "prompts": [
                "where in your town/city the neighbourhood was",
                "what kind of people lived there",
                "what it was like to live in this neighbourhood",
                "and explain whether you would like to live in this neighbourhood in the future."
            ],
            "preparationTime": 60
        },
        "part3": {
            "topic": "Neighbours and Facilities in cities",
            "sections": [
                {
                    "topic": "Neighbours",
                    "questions": [
                        "What sort of things can neighbours do to help each other?",
                        "How well do people generally know their neighbours in your country?",
                        "How important do you think it is to have good neighbours?"
                    ]
                },
                {
                    "topic": "Facilities in cities",
                    "questions": [
                        "Which facilities are most important to people living in cities?",
                        "How does shopping in small local shops differ from shopping in large city centre shops?",
                        "Do you think that children should always go to the school nearest to where they live?"
                    ]
                }
            ]
        }
    }


def main():
    files = {
        "reading.json": create_reading_json(),
        "listening.json": create_listening_json(),
        "writing.json": create_writing_json(),
        "speaking.json": create_speaking_json(),
    }

    for filename, data in files.items():
        path = os.path.join(OUT_DIR, filename)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        # Count questions
        if filename == "reading.json":
            total = sum(len(p["questions"]) for p in data["passages"])
        elif filename == "listening.json":
            total = sum(len(s["questions"]) for s in data["sections"])
        else:
            total = "N/A"
        print(f"  Created {filename} ({total} questions)")


if __name__ == "__main__":
    main()
