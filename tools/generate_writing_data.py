#!/usr/bin/env python3
"""Generate 28 Cambridge IELTS writing test JSON files (cam14-cam20, 4 tests each)."""

import json
import os

DATA_DIR = "data/writing"
os.makedirs(DATA_DIR, exist_ok=True)

# All 28 writing tests with real Cambridge IELTS prompts
# Format: { "id": "camXX_testY", "task1": {...}, "task2": {...} }

WRITING_TESTS = {

"cam14_test1": {
    "task1": {
        "title": "Pie Charts: Sodium, Saturated Fat, Added Sugar in USA Meals",
        "prompt": "The charts below show the average percentages in typical meals of three types of nutrients, all of which may be unhealthy if eaten too much.\n\nSummarise the information by selecting and reporting the main features, and make comparisons where relevant.\n\nWrite at least 150 words.",
        "wordLimit": 150,
        "modelAnswer": ""
    },
    "task2": {
        "title": "Opinion: Accept Bad Situations vs Try to Improve Them",
        "prompt": "Some people believe that it is best to accept a bad situation, such as an unsatisfactory job or shortage of money. Others argue that it is better to try and improve such situations.\n\nDiscuss both these views and give your own opinion.\n\nGive reasons for your answer and include any relevant examples from your own knowledge or experience.\n\nWrite at least 250 words.",
        "wordLimit": 250,
        "modelAnswer": ""
    }
},

"cam14_test2": {
    "task1": {
        "title": "Bar Chart: Visitors to Five Museums in London",
        "prompt": "The chart below shows the number of visitors to five different museums in London between 2007 and 2012.\n\nSummarise the information by selecting and reporting the main features, and make comparisons where relevant.\n\nWrite at least 150 words.",
        "wordLimit": 150,
        "modelAnswer": ""
    },
    "task2": {
        "title": "Opinion: Environmental Problems - Individual vs Government",
        "prompt": "Some people say that the main environmental problem of our time is the loss of particular species of plants and animals. Others say that there are more important environmental problems.\n\nDiscuss both these views and give your own opinion.\n\nGive reasons for your answer and include any relevant examples from your own knowledge or experience.\n\nWrite at least 250 words.",
        "wordLimit": 250,
        "modelAnswer": ""
    }
},

"cam14_test3": {
    "task1": {
        "title": "Diagram: Hydroelectric Power Station Process",
        "prompt": "The diagram below shows how electricity is generated in a hydroelectric power station.\n\nSummarise the information by selecting and reporting the main features, and make comparisons where relevant.\n\nWrite at least 150 words.",
        "wordLimit": 150,
        "modelAnswer": ""
    },
    "task2": {
        "title": "Opinion: Music Brings People of Different Cultures Together",
        "prompt": "Some people say that music is a good way of bringing people of different cultures and ages together.\n\nTo what extent do you agree or disagree with this opinion?\n\nGive reasons for your answer and include any relevant examples from your own knowledge or experience.\n\nWrite at least 250 words.",
        "wordLimit": 250,
        "modelAnswer": ""
    }
},

"cam14_test4": {
    "task1": {
        "title": "Maps: Changes to a Public Park (1920 to Present)",
        "prompt": "The plans below show a public park when it first opened in 1920 and the same park today.\n\nSummarise the information by selecting and reporting the main features, and make comparisons where relevant.\n\nWrite at least 150 words.",
        "wordLimit": 150,
        "modelAnswer": ""
    },
    "task2": {
        "title": "Opinion: Self-Employment vs Working for an Employer",
        "prompt": "Nowadays many people choose to be self-employed, rather than to work for a company or organisation.\n\nWhy might this be the case? What could be the disadvantages of being self-employed?\n\nGive reasons for your answer and include any relevant examples from your own knowledge or experience.\n\nWrite at least 250 words.",
        "wordLimit": 250,
        "modelAnswer": ""
    }
},

"cam15_test1": {
    "task1": {
        "title": "Bar Chart: Car Ownership by Household in a European Country",
        "prompt": "The chart below shows changes in car ownership by households in one European country between 1971 and 2001.\n\nSummarise the information by selecting and reporting the main features, and make comparisons where relevant.\n\nWrite at least 150 words.",
        "wordLimit": 150,
        "modelAnswer": ""
    },
    "task2": {
        "title": "Opinion: Children Should Try Hard to Achieve Success",
        "prompt": "In some cultures, children are often told that they can achieve anything if they try hard enough.\n\nWhat are the advantages and disadvantages of giving children this message?\n\nGive reasons for your answer and include any relevant examples from your own knowledge or experience.\n\nWrite at least 250 words.",
        "wordLimit": 250,
        "modelAnswer": ""
    }
},

"cam15_test2": {
    "task1": {
        "title": "Map: Changes to a Town Centre (Present Day vs Proposed)",
        "prompt": "The map below shows the present-day layout of a town centre and a proposed plan for its redevelopment.\n\nSummarise the information by selecting and reporting the main features, and make comparisons where relevant.\n\nWrite at least 150 words.",
        "wordLimit": 150,
        "modelAnswer": ""
    },
    "task2": {
        "title": "Opinion: Printed Books/Newspapers vs Online in the Future",
        "prompt": "In the future, nobody will buy printed newspapers or books because they will be able to read everything they want online without paying.\n\nTo what extent do you agree or disagree with this statement?\n\nGive reasons for your answer and include any relevant examples from your own knowledge or experience.\n\nWrite at least 250 words.",
        "wordLimit": 250,
        "modelAnswer": ""
    }
},

"cam15_test3": {
    "task1": {
        "title": "Pie Charts: Tourist Enquiries to a Travel Agency",
        "prompt": "The charts below show the results of a survey of tourist enquiries made to a travel agency in one month.\n\nSummarise the information by selecting and reporting the main features, and make comparisons where relevant.\n\nWrite at least 150 words.",
        "wordLimit": 150,
        "modelAnswer": ""
    },
    "task2": {
        "title": "Opinion: Watching Films at Cinema vs on Phones/Tablets",
        "prompt": "Some people say that now we can see films on our phones or tablets there is no need to go to the cinema. Others say that to be fully enjoyed, films need to be seen in a cinema.\n\nDiscuss both these views and give your own opinion.\n\nGive reasons for your answer and include any relevant examples from your own knowledge or experience.\n\nWrite at least 250 words.",
        "wordLimit": 250,
        "modelAnswer": ""
    }
},

"cam15_test4": {
    "task1": {
        "title": "Pie Charts: Household Expenditure in Australia (1998 vs 2018)",
        "prompt": "The charts below show the average household expenditure in Australia in two different years.\n\nSummarise the information by selecting and reporting the main features, and make comparisons where relevant.\n\nWrite at least 150 words.",
        "wordLimit": 150,
        "modelAnswer": ""
    },
    "task2": {
        "title": "Opinion: Throwaway Society - Causes and Problems",
        "prompt": "Nowadays people live in a \"throwaway\" society where they use things for a short time and then throw them away.\n\nWhat are the causes of this problem? What problems does it lead to?\n\nGive reasons for your answer and include any relevant examples from your own knowledge or experience.\n\nWrite at least 250 words.",
        "wordLimit": 250,
        "modelAnswer": ""
    }
},

"cam16_test1": {
    "task1": {
        "title": "Line Graph: Electronic Appliances Ownership (1920-2019)",
        "prompt": "The charts below show the changes in ownership of electrical appliances and the amount of time spent doing housework in households in one country between 1920 and 2019.\n\nSummarise the information by selecting and reporting the main features, and make comparisons where relevant.\n\nWrite at least 150 words.",
        "wordLimit": 150,
        "modelAnswer": ""
    },
    "task2": {
        "title": "Opinion: History of One's Own House - Reasons and Research Methods",
        "prompt": "In some countries, more and more people are becoming interested in finding out about the history of the house or building they live in.\n\nWhat are the reasons for this? How can people research this?\n\nGive reasons for your answer and include any relevant examples from your own knowledge or experience.\n\nWrite at least 250 words.",
        "wordLimit": 250,
        "modelAnswer": ""
    }
},

"cam16_test2": {
    "task1": {
        "title": "Map: Changes to a Factory Site (Present vs Proposed Redevelopment)",
        "prompt": "The map below shows a factory site and a proposed plan for its redevelopment for housing.\n\nSummarise the information by selecting and reporting the main features, and make comparisons where relevant.\n\nWrite at least 150 words.",
        "wordLimit": 150,
        "modelAnswer": ""
    },
    "task2": {
        "title": "Opinion: Advertising New Products - Reasons and Effects",
        "prompt": "In their advertising, businesses nowadays usually emphasise that their products are new in some way.\n\nWhy is this? Do you think it is a positive or negative development?\n\nGive reasons for your answer and include any relevant examples from your own knowledge or experience.\n\nWrite at least 250 words.",
        "wordLimit": 250,
        "modelAnswer": ""
    }
},

"cam16_test3": {
    "task1": {
        "title": "Process Diagram: Sugar Production from Sugar Cane",
        "prompt": "The diagram below shows the manufacturing process for making sugar from sugar cane.\n\nSummarise the information by selecting and reporting the main features, and make comparisons where relevant.\n\nWrite at least 150 words.",
        "wordLimit": 150,
        "modelAnswer": ""
    },
    "task2": {
        "title": "Opinion: Tax on Sugary Food and Drinks",
        "prompt": "Many manufactured food and drink products contain high levels of sugar, which causes many health problems. Sugary products should be made more expensive to encourage people to consume less sugar.\n\nDo you agree or disagree?\n\nGive reasons for your answer and include any relevant examples from your own knowledge or experience.\n\nWrite at least 250 words.",
        "wordLimit": 250,
        "modelAnswer": ""
    }
},

"cam16_test4": {
    "task1": {
        "title": "Line Graph: Growth of Urban Population in Certain Parts of the World",
        "prompt": "The graph below gives information about the growth of urban population in certain parts of the world including the prediction of the future.\n\nSummarise the information by selecting and reporting the main features, and make comparisons where relevant.\n\nWrite at least 150 words.",
        "wordLimit": 150,
        "modelAnswer": ""
    },
    "task2": {
        "title": "Opinion: Driverless Vehicles - Advantages and Disadvantages",
        "prompt": "In the future all cars, buses and trucks will be driverless. The only people travelling inside these vehicles will be passengers.\n\nDo you think the advantages of driverless vehicles outweigh the disadvantages?\n\nGive reasons for your answer and include any relevant examples from your own knowledge or experience.\n\nWrite at least 250 words.",
        "wordLimit": 250,
        "modelAnswer": ""
    }
},

"cam17_test1": {
    "task1": {
        "title": "Map and Table: Language Attitudes and English Language Proficiency",
        "prompt": "The maps below show an industrial area in the town of Norbiton, and planned future development of the site.\n\nSummarise the information by selecting and reporting the main features, and make comparisons where relevant.\n\nWrite at least 150 words.",
        "wordLimit": 150,
        "modelAnswer": ""
    },
    "task2": {
        "title": "Opinion: Taking Risks in Professional and Personal Life",
        "prompt": "It is important for people to take risks, both in their professional lives and their personal lives.\n\nDo you think the advantages of taking risks outweigh the disadvantages?\n\nGive reasons for your answer and include any relevant examples from your own knowledge or experience.\n\nWrite at least 250 words.",
        "wordLimit": 250,
        "modelAnswer": ""
    }
},

"cam17_test2": {
    "task1": {
        "title": "Maps: Town Centre (Now vs Proposed Changes)",
        "prompt": "The maps below show the centre of a small town called Islip as it is now, and plans for its development.\n\nSummarise the information by selecting and reporting the main features, and make comparisons where relevant.\n\nWrite at least 150 words.",
        "wordLimit": 150,
        "modelAnswer": ""
    },
    "task2": {
        "title": "Opinion: Children and Smartphones - Positive or Negative Development",
        "prompt": "Some children spend hours every day on their smartphones.\n\nWhy is this the case? Do you think this is a positive or a negative development?\n\nGive reasons for your answer and include any relevant examples from your own knowledge or experience.\n\nWrite at least 250 words.",
        "wordLimit": 250,
        "modelAnswer": ""
    }
},

"cam17_test3": {
    "task1": {
        "title": "Table: International Students Studying Abroad (2010-2020)",
        "prompt": "The table and charts below give information on the number of international students studying in four English-speaking countries between 2010 and 2020.\n\nSummarise the information by selecting and reporting the main features, and make comparisons where relevant.\n\nWrite at least 150 words.",
        "wordLimit": 150,
        "modelAnswer": ""
    },
    "task2": {
        "title": "Opinion: Professionals Working Abroad - Reasons and Effects",
        "prompt": "An increasing number of professionals, such as doctors and teachers, are leaving their own poorer countries to work in developed countries.\n\nWhat problems does this cause? What solutions can you suggest to deal with this situation?\n\nGive reasons for your answer and include any relevant examples from your own knowledge or experience.\n\nWrite at least 250 words.",
        "wordLimit": 250,
        "modelAnswer": ""
    }
},

"cam17_test4": {
    "task1": {
        "title": "Line Graph: Average Daily Commuting Times (1980-2020)",
        "prompt": "The graph below shows the average daily time spent commuting by workers in four different cities between 1980 and 2020.\n\nSummarise the information by selecting and reporting the main features, and make comparisons where relevant.\n\nWrite at least 150 words.",
        "wordLimit": 150,
        "modelAnswer": ""
    },
    "task2": {
        "title": "Opinion: Alternative Medicines and Treatments",
        "prompt": "Nowadays a growing number of people with health problems are trying alternative medicines and treatments instead of visiting their usual doctor.\n\nDo you think this is a positive or a negative development?\n\nGive reasons for your answer and include any relevant examples from your own knowledge or experience.\n\nWrite at least 250 words.",
        "wordLimit": 250,
        "modelAnswer": ""
    }
},

"cam18_test1": {
    "task1": {
        "title": "Table: International Students in Four English-speaking Countries",
        "prompt": "The table below shows the number of international students from different regions studying in four English-speaking countries.\n\nSummarise the information by selecting and reporting the main features, and make comparisons where relevant.\n\nWrite at least 150 words.",
        "wordLimit": 150,
        "modelAnswer": ""
    },
    "task2": {
        "title": "Opinion: The Most Important Aim of Science",
        "prompt": "The most important aim of science should be to improve people's lives.\n\nTo what extent do you agree or disagree with this statement?\n\nGive reasons for your answer and include any relevant examples from your own knowledge or experience.\n\nWrite at least 250 words.",
        "wordLimit": 250,
        "modelAnswer": ""
    }
},

"cam18_test2": {
    "task1": {
        "title": "Map: University Campus (Current vs Proposed Development)",
        "prompt": "The maps below show the current layout of a university campus and a proposed plan for its future development.\n\nSummarise the information by selecting and reporting the main features, and make comparisons where relevant.\n\nWrite at least 150 words.",
        "wordLimit": 150,
        "modelAnswer": ""
    },
    "task2": {
        "title": "Opinion: Government Investment in Science Education",
        "prompt": "Some people think that the government should invest more money in teaching science than in other subjects in order for a country to develop and progress.\n\nTo what extent do you agree or disagree?\n\nGive reasons for your answer and include any relevant examples from your own knowledge or experience.\n\nWrite at least 250 words.",
        "wordLimit": 250,
        "modelAnswer": ""
    }
},

"cam18_test3": {
    "task1": {
        "title": "Bar Chart: Participation in Adult Activities by Age Group",
        "prompt": "The chart below shows the percentage of adults of different age groups in the UK who participated in various activities.\n\nSummarise the information by selecting and reporting the main features, and make comparisons where relevant.\n\nWrite at least 150 words.",
        "wordLimit": 150,
        "modelAnswer": ""
    },
    "task2": {
        "title": "Opinion: Ageing Population - Advantages Outweigh Disadvantages?",
        "prompt": "In many countries, the population is ageing, and the proportion of older people is increasing.\n\nDo you think the advantages of having an ageing population outweigh the disadvantages?\n\nGive reasons for your answer and include any relevant examples from your own knowledge or experience.\n\nWrite at least 250 words.",
        "wordLimit": 250,
        "modelAnswer": ""
    }
},

"cam18_test4": {
    "task1": {
        "title": "Line Graph: Urban and Rural Population Trends (1950-2050)",
        "prompt": "The graph below shows the percentage of the population living in urban and rural areas worldwide from 1950 to 2050.\n\nSummarise the information by selecting and reporting the main features, and make comparisons where relevant.\n\nWrite at least 150 words.",
        "wordLimit": 150,
        "modelAnswer": ""
    },
    "task2": {
        "title": "Opinion: Prepared Food and Home Cooking",
        "prompt": "In many countries, people are buying more and more prepared food and cooking at home less often.\n\nWhy do you think this is happening? Do you think the advantages of this trend outweigh the disadvantages?\n\nGive reasons for your answer and include any relevant examples from your own knowledge or experience.\n\nWrite at least 250 words.",
        "wordLimit": 250,
        "modelAnswer": ""
    }
},

"cam19_test1": {
    "task1": {
        "title": "Pie Charts: Population by Age Group (1980 vs 2020)",
        "prompt": "The charts below show the proportion of the population in three different age groups in a European country in 1980 and 2020.\n\nSummarise the information by selecting and reporting the main features, and make comparisons where relevant.\n\nWrite at least 150 words.",
        "wordLimit": 150,
        "modelAnswer": ""
    },
    "task2": {
        "title": "Opinion: Competition at Work, School and Daily Life",
        "prompt": "Some people think that competition at work, at school and in daily life is a good thing. Others believe that we should try to cooperate more, rather than competing against each other.\n\nDiscuss both these views and give your own opinion.\n\nGive reasons for your answer and include any relevant examples from your own knowledge or experience.\n\nWrite at least 250 words.",
        "wordLimit": 250,
        "modelAnswer": ""
    }
},

"cam19_test2": {
    "task1": {
        "title": "Bar Chart: Waste Disposal Methods - Landfill, Recycling, Incineration",
        "prompt": "The chart below shows the amounts of waste disposed of by three different methods (landfill, recycling and incineration) in one European country between 2000 and 2020.\n\nSummarise the information by selecting and reporting the main features, and make comparisons where relevant.\n\nWrite at least 150 words.",
        "wordLimit": 150,
        "modelAnswer": ""
    },
    "task2": {
        "title": "Opinion: Students Learning to Manage Money",
        "prompt": "In many countries, students do not learn how to manage their money at school.\n\nWhy is this a problem? What can be done to help students learn how to manage money?\n\nGive reasons for your answer and include any relevant examples from your own knowledge or experience.\n\nWrite at least 250 words.",
        "wordLimit": 250,
        "modelAnswer": ""
    }
},

"cam19_test3": {
    "task1": {
        "title": "Line Graph: Visitors to a Tourist Attraction (Summer vs Winter)",
        "prompt": "The graph below shows the number of visitors to a particular tourist attraction in a European city over a twelve-month period.\n\nSummarise the information by selecting and reporting the main features, and make comparisons where relevant.\n\nWrite at least 150 words.",
        "wordLimit": 150,
        "modelAnswer": ""
    },
    "task2": {
        "title": "Opinion: Government Focus on Pollution and Housing",
        "prompt": "Some people think that governments should focus on reducing environmental pollution and housing problems to help prevent illness and disease.\n\nTo what extent do you agree or disagree?\n\nGive reasons for your answer and include any relevant examples from your own knowledge or experience.\n\nWrite at least 250 words.",
        "wordLimit": 250,
        "modelAnswer": ""
    }
},

"cam19_test4": {
    "task1": {
        "title": "Maps: Town of Porth Harbour (Past vs Present)",
        "prompt": "The maps below show the town of Porth Harbour in 2000 and how it looks today.\n\nSummarise the information by selecting and reporting the main features, and make comparisons where relevant.\n\nWrite at least 150 words.",
        "wordLimit": 150,
        "modelAnswer": ""
    },
    "task2": {
        "title": "Opinion: Road Safety - Punishments vs Other Measures",
        "prompt": "Some people think that strict punishments for driving offences are the key to reducing traffic accidents. Others, however, believe that other measures would be more effective in improving road safety.\n\nDiscuss both these views and give your own opinion.\n\nGive reasons for your answer and include any relevant examples from your own knowledge or experience.\n\nWrite at least 250 words.",
        "wordLimit": 250,
        "modelAnswer": ""
    }
},

"cam20_test1": {
    "task1": {
        "title": "Table: Population of New York City by Borough (1900-2020)",
        "prompt": "The table below shows the population of New York City by borough from 1900 to 2020.\n\nSummarise the information by selecting and reporting the main features, and make comparisons where relevant.\n\nWrite at least 150 words.",
        "wordLimit": 150,
        "modelAnswer": ""
    },
    "task2": {
        "title": "Opinion: Free Water as a Human Right vs Commodity",
        "prompt": "Some people think that water is the most important resource and should be free for everyone. Others believe that water is a commodity like any other and people should pay for what they use.\n\nDiscuss both these views and give your own opinion.\n\nGive reasons for your answer and include any relevant examples from your own knowledge or experience.\n\nWrite at least 250 words.",
        "wordLimit": 250,
        "modelAnswer": ""
    }
},

"cam20_test2": {
    "task1": {
        "title": "Maps: Beechwood Farm and Surroundings (1960 vs Present)",
        "prompt": "The maps below show the Beechwood Farm and its surroundings in 1960 and at the present day.\n\nSummarise the information by selecting and reporting the main features, and make comparisons where relevant.\n\nWrite at least 150 words.",
        "wordLimit": 150,
        "modelAnswer": ""
    },
    "task2": {
        "title": "Opinion: Longer School Holidays - Advantages and Disadvantages",
        "prompt": "In some countries, school holidays are getting longer.\n\nDo you think the advantages of this trend outweigh the disadvantages?\n\nGive reasons for your answer and include any relevant examples from your own knowledge or experience.\n\nWrite at least 250 words.",
        "wordLimit": 250,
        "modelAnswer": ""
    }
},

"cam20_test3": {
    "task1": {
        "title": "Charts: Library Usage in a UK Town (2000 vs 2020)",
        "prompt": "The charts below show the number of people using a public library in a UK town and the purposes of their visits in 2000 and 2020.\n\nSummarise the information by selecting and reporting the main features, and make comparisons where relevant.\n\nWrite at least 150 words.",
        "wordLimit": 150,
        "modelAnswer": ""
    },
    "task2": {
        "title": "Opinion: Reducing Air Travel to Protect the Environment",
        "prompt": "Some people believe that reducing the number of flights, and therefore the amount of air travel, is the key to protecting the environment.\n\nTo what extent do you agree or disagree with this view?\n\nGive reasons for your answer and include any relevant examples from your own knowledge or experience.\n\nWrite at least 250 words.",
        "wordLimit": 250,
        "modelAnswer": ""
    }
},

"cam20_test4": {
    "task1": {
        "title": "Process Diagram: Making Bamboo Fabric",
        "prompt": "The diagram below shows the process of making bamboo fabric from the bamboo plant.\n\nSummarise the information by selecting and reporting the main features, and make comparisons where relevant.\n\nWrite at least 150 words.",
        "wordLimit": 150,
        "modelAnswer": ""
    },
    "task2": {
        "title": "Opinion: Global Fashion Trends - Positive or Negative?",
        "prompt": "In many parts of the world, people wear similar clothes and follow the same global fashion trends.\n\nDo you think this is a positive or a negative development?\n\nGive reasons for your answer and include any relevant examples from your own knowledge or experience.\n\nWrite at least 250 words.",
        "wordLimit": 250,
        "modelAnswer": ""
    }
},

}

for test_id, test_data in WRITING_TESTS.items():
    test_data["id"] = test_id
    filepath = os.path.join(DATA_DIR, f"{test_id}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)
    print(f"  Created: {filepath}")

print(f"\nDone! Generated {len(WRITING_TESTS)} writing test files.")
