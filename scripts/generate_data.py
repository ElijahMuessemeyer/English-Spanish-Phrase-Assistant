#!/usr/bin/env python3
"""
Generate phrase and test datasets.

Creates:
- data/phrases.json: 250+ travel phrases with translations
- data/tests.json: 120+ test queries for evaluation
"""

import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from phrasebot.config import default_config


# Complete phrase database organized by category
PHRASES_DATA = [
    # ESSENTIALS (40 phrases)
    {"id": "essentials_001", "english": "Where is the bathroom?", "spanish": "¿Dónde está el baño?", "pronunciation": "DOHN-deh es-TAH el BAN-yoh", "category": "essentials", "alts": ["Where's the restroom?", "Where is the restroom?", "Bathroom?", "Restroom?", "Can you tell me where the bathroom is?"]},
    {"id": "essentials_002", "english": "Do you speak English?", "spanish": "¿Habla inglés?", "pronunciation": "AH-blah een-GLAYS", "category": "essentials", "alts": ["Do you speak english", "Can you speak English?", "Do you understand English?", "English?"]},
    {"id": "essentials_003", "english": "I don't understand.", "spanish": "No entiendo.", "pronunciation": "noh en-tee-EN-doh", "category": "essentials", "alts": ["I don't get it", "I do not understand", "Sorry I don't understand", "What?"]},
    {"id": "essentials_004", "english": "Please speak slowly.", "spanish": "Por favor, hable despacio.", "pronunciation": "por fah-VOR AH-bleh des-PAH-see-oh", "category": "essentials", "alts": ["Can you speak slower?", "Speak slowly please", "Slower please", "Could you speak more slowly?"]},
    {"id": "essentials_005", "english": "Thank you.", "spanish": "Gracias.", "pronunciation": "GRAH-see-ahs", "category": "essentials", "alts": ["Thanks", "Thank you very much", "Thanks a lot", "Many thanks"]},
    {"id": "essentials_006", "english": "You're welcome.", "spanish": "De nada.", "pronunciation": "deh NAH-dah", "category": "essentials", "alts": ["No problem", "It's nothing", "Don't mention it"]},
    {"id": "essentials_007", "english": "Excuse me.", "spanish": "Disculpe.", "pronunciation": "dees-KOOL-peh", "category": "essentials", "alts": ["Pardon me", "Sorry", "Excuse me please"]},
    {"id": "essentials_008", "english": "I'm sorry.", "spanish": "Lo siento.", "pronunciation": "loh see-EN-toh", "category": "essentials", "alts": ["Sorry", "I apologize", "My apologies", "Forgive me"]},
    {"id": "essentials_009", "english": "Yes.", "spanish": "Sí.", "pronunciation": "see", "category": "essentials", "alts": ["Yeah", "Yep", "Correct", "That's right"]},
    {"id": "essentials_010", "english": "No.", "spanish": "No.", "pronunciation": "noh", "category": "essentials", "alts": ["Nope", "No thanks", "Not really"]},
    {"id": "essentials_011", "english": "Hello.", "spanish": "Hola.", "pronunciation": "OH-lah", "category": "essentials", "alts": ["Hi", "Hey", "Good day", "Greetings"]},
    {"id": "essentials_012", "english": "Goodbye.", "spanish": "Adiós.", "pronunciation": "ah-dee-OHS", "category": "essentials", "alts": ["Bye", "See you later", "Bye bye", "Take care"]},
    {"id": "essentials_013", "english": "Good morning.", "spanish": "Buenos días.", "pronunciation": "BWEH-nohs DEE-ahs", "category": "essentials", "alts": ["Morning", "Good day"]},
    {"id": "essentials_014", "english": "Good afternoon.", "spanish": "Buenas tardes.", "pronunciation": "BWEH-nahs TAR-des", "category": "essentials", "alts": ["Afternoon", "Good day"]},
    {"id": "essentials_015", "english": "Good evening.", "spanish": "Buenas noches.", "pronunciation": "BWEH-nahs NOH-ches", "category": "essentials", "alts": ["Evening", "Good night"]},
    {"id": "essentials_016", "english": "How are you?", "spanish": "¿Cómo está?", "pronunciation": "KOH-moh es-TAH", "category": "essentials", "alts": ["How are you doing?", "How's it going?", "How do you do?"]},
    {"id": "essentials_017", "english": "I'm fine, thank you.", "spanish": "Estoy bien, gracias.", "pronunciation": "es-TOY bee-EN GRAH-see-ahs", "category": "essentials", "alts": ["I'm good thanks", "Fine thank you", "I'm doing well"]},
    {"id": "essentials_018", "english": "What is your name?", "spanish": "¿Cómo se llama?", "pronunciation": "KOH-moh seh YAH-mah", "category": "essentials", "alts": ["What's your name?", "Your name?", "May I know your name?"]},
    {"id": "essentials_019", "english": "My name is...", "spanish": "Me llamo...", "pronunciation": "meh YAH-moh", "category": "essentials", "alts": ["I'm called...", "I am..."]},
    {"id": "essentials_020", "english": "Nice to meet you.", "spanish": "Mucho gusto.", "pronunciation": "MOO-choh GOOS-toh", "category": "essentials", "alts": ["Pleased to meet you", "It's nice to meet you", "Good to meet you"]},
    {"id": "essentials_021", "english": "Please.", "spanish": "Por favor.", "pronunciation": "por fah-VOR", "category": "essentials", "alts": ["If you please", "Kindly"]},
    {"id": "essentials_022", "english": "Can you help me?", "spanish": "¿Puede ayudarme?", "pronunciation": "PWEH-deh ah-yoo-DAR-meh", "category": "essentials", "alts": ["Could you help me?", "Help me please", "I need help", "Would you help me?"]},
    {"id": "essentials_023", "english": "I need...", "spanish": "Necesito...", "pronunciation": "neh-seh-SEE-toh", "category": "essentials", "alts": ["I require...", "I want..."]},
    {"id": "essentials_024", "english": "I would like...", "spanish": "Quisiera...", "pronunciation": "kee-see-EH-rah", "category": "essentials", "alts": ["I'd like...", "I want...", "May I have..."]},
    {"id": "essentials_025", "english": "How much does this cost?", "spanish": "¿Cuánto cuesta esto?", "pronunciation": "KWAN-toh KWES-tah ES-toh", "category": "essentials", "alts": ["How much is this?", "What's the price?", "Price?", "How much?"]},
    {"id": "essentials_026", "english": "What time is it?", "spanish": "¿Qué hora es?", "pronunciation": "keh OH-rah es", "category": "essentials", "alts": ["What's the time?", "Do you have the time?", "Time please?"]},
    {"id": "essentials_027", "english": "I don't know.", "spanish": "No sé.", "pronunciation": "noh seh", "category": "essentials", "alts": ["I have no idea", "Not sure", "I'm not sure"]},
    {"id": "essentials_028", "english": "Can you repeat that?", "spanish": "¿Puede repetir?", "pronunciation": "PWEH-deh reh-peh-TEER", "category": "essentials", "alts": ["Please repeat", "Say that again", "Could you repeat?", "Repeat please"]},
    {"id": "essentials_029", "english": "Where is...?", "spanish": "¿Dónde está...?", "pronunciation": "DOHN-deh es-TAH", "category": "essentials", "alts": ["Where can I find...?", "Location of...?"]},
    {"id": "essentials_030", "english": "I am from the United States.", "spanish": "Soy de los Estados Unidos.", "pronunciation": "soy deh los es-TAH-dohs oo-NEE-dohs", "category": "essentials", "alts": ["I'm American", "I come from the US", "I'm from America"]},
    {"id": "essentials_031", "english": "I am a tourist.", "spanish": "Soy turista.", "pronunciation": "soy too-REES-tah", "category": "essentials", "alts": ["I'm a visitor", "I'm traveling", "Just visiting"]},
    {"id": "essentials_032", "english": "I am here on vacation.", "spanish": "Estoy aquí de vacaciones.", "pronunciation": "es-TOY ah-KEE deh vah-kah-see-OH-nes", "category": "essentials", "alts": ["I'm on holiday", "I'm vacationing here", "Here for vacation"]},
    {"id": "essentials_033", "english": "Wait a moment.", "spanish": "Espere un momento.", "pronunciation": "es-PEH-reh oon moh-MEN-toh", "category": "essentials", "alts": ["Wait please", "Just a moment", "One moment", "Hold on"]},
    {"id": "essentials_034", "english": "I have a question.", "spanish": "Tengo una pregunta.", "pronunciation": "TEN-goh OO-nah preh-GOON-tah", "category": "essentials", "alts": ["May I ask something?", "Quick question"]},
    {"id": "essentials_035", "english": "Can you write it down?", "spanish": "¿Puede escribirlo?", "pronunciation": "PWEH-deh es-kree-BEER-loh", "category": "essentials", "alts": ["Write it please", "Could you write that?"]},
    {"id": "essentials_036", "english": "I don't speak Spanish.", "spanish": "No hablo español.", "pronunciation": "noh AH-bloh es-pahn-YOL", "category": "essentials", "alts": ["I can't speak Spanish", "My Spanish is bad", "I don't know Spanish"]},
    {"id": "essentials_037", "english": "I speak a little Spanish.", "spanish": "Hablo un poco de español.", "pronunciation": "AH-bloh oon POH-koh deh es-pahn-YOL", "category": "essentials", "alts": ["I know some Spanish", "A little Spanish", "My Spanish is limited"]},
    {"id": "essentials_038", "english": "What does this mean?", "spanish": "¿Qué significa esto?", "pronunciation": "keh seeg-NEE-fee-kah ES-toh", "category": "essentials", "alts": ["What is this?", "What's this mean?"]},
    {"id": "essentials_039", "english": "How do you say...?", "spanish": "¿Cómo se dice...?", "pronunciation": "KOH-moh seh DEE-seh", "category": "essentials", "alts": ["What's the word for...?", "How to say...?"]},
    {"id": "essentials_040", "english": "Is there someone who speaks English?", "spanish": "¿Hay alguien que hable inglés?", "pronunciation": "eye al-GEE-en keh AH-bleh een-GLAYS", "category": "essentials", "alts": ["Anyone speak English?", "English speaker?", "Does anyone here speak English?"]},

    # DINING (50 phrases)
    {"id": "dining_001", "english": "I have an allergy to peanuts.", "spanish": "Soy alérgico/a a los cacahuetes.", "pronunciation": "soy ah-LAIR-hee-koh ah los kah-kah-WEH-tes", "category": "dining", "alts": ["I'm allergic to peanuts", "Peanut allergy", "I can't eat peanuts"]},
    {"id": "dining_002", "english": "A table for two, please.", "spanish": "Una mesa para dos, por favor.", "pronunciation": "OO-nah MEH-sah PAH-rah dohs por fah-VOR", "category": "dining", "alts": ["Table for 2", "Two people", "Party of two"]},
    {"id": "dining_003", "english": "The menu, please.", "spanish": "El menú, por favor.", "pronunciation": "el meh-NOO por fah-VOR", "category": "dining", "alts": ["Can I see the menu?", "Menu please", "May I have the menu?"]},
    {"id": "dining_004", "english": "What do you recommend?", "spanish": "¿Qué recomienda?", "pronunciation": "keh reh-koh-mee-EN-dah", "category": "dining", "alts": ["What's good here?", "What should I order?", "Your recommendation?"]},
    {"id": "dining_005", "english": "I am vegetarian.", "spanish": "Soy vegetariano/a.", "pronunciation": "soy veh-heh-tah-ree-AH-noh", "category": "dining", "alts": ["I'm a vegetarian", "I don't eat meat", "Vegetarian please"]},
    {"id": "dining_006", "english": "I am vegan.", "spanish": "Soy vegano/a.", "pronunciation": "soy veh-GAH-noh", "category": "dining", "alts": ["I'm vegan", "No animal products", "I don't eat animal products"]},
    {"id": "dining_007", "english": "The check, please.", "spanish": "La cuenta, por favor.", "pronunciation": "lah KWEN-tah por fah-VOR", "category": "dining", "alts": ["Bill please", "Check please", "Can I have the bill?", "The bill"]},
    {"id": "dining_008", "english": "I would like to order.", "spanish": "Quisiera ordenar.", "pronunciation": "kee-see-EH-rah or-deh-NAR", "category": "dining", "alts": ["I'd like to order", "Ready to order", "Can I order?"]},
    {"id": "dining_009", "english": "Water, please.", "spanish": "Agua, por favor.", "pronunciation": "AH-gwah por fah-VOR", "category": "dining", "alts": ["Can I have water?", "Some water please", "Glass of water"]},
    {"id": "dining_010", "english": "Is this spicy?", "spanish": "¿Está picante?", "pronunciation": "es-TAH pee-KAHN-teh", "category": "dining", "alts": ["Is it spicy?", "Is this hot?", "Spicy?"]},
    {"id": "dining_011", "english": "No spicy, please.", "spanish": "Sin picante, por favor.", "pronunciation": "seen pee-KAHN-teh por fah-VOR", "category": "dining", "alts": ["Not spicy please", "No hot peppers", "Mild please"]},
    {"id": "dining_012", "english": "This is delicious!", "spanish": "¡Está delicioso!", "pronunciation": "es-TAH deh-lee-see-OH-soh", "category": "dining", "alts": ["It's delicious", "Very tasty", "So good!"]},
    {"id": "dining_013", "english": "I have a food allergy.", "spanish": "Tengo alergia alimentaria.", "pronunciation": "TEN-goh ah-LAIR-hee-ah ah-lee-men-TAH-ree-ah", "category": "dining", "alts": ["I'm allergic to some foods", "Food allergy"]},
    {"id": "dining_014", "english": "I am allergic to shellfish.", "spanish": "Soy alérgico/a a los mariscos.", "pronunciation": "soy ah-LAIR-hee-koh ah los mah-REES-kohs", "category": "dining", "alts": ["Shellfish allergy", "I can't eat shellfish", "No shellfish"]},
    {"id": "dining_015", "english": "I am allergic to gluten.", "spanish": "Soy alérgico/a al gluten.", "pronunciation": "soy ah-LAIR-hee-koh al GLOO-ten", "category": "dining", "alts": ["Gluten allergy", "I can't eat gluten", "Gluten free please"]},
    {"id": "dining_016", "english": "I am allergic to dairy.", "spanish": "Soy alérgico/a a los lácteos.", "pronunciation": "soy ah-LAIR-hee-koh ah los LAK-teh-ohs", "category": "dining", "alts": ["Dairy allergy", "I can't have milk", "No dairy please"]},
    {"id": "dining_017", "english": "Does this contain nuts?", "spanish": "¿Contiene nueces?", "pronunciation": "kon-tee-EH-neh NWEH-ses", "category": "dining", "alts": ["Are there nuts in this?", "Any nuts?", "Nut-free?"]},
    {"id": "dining_018", "english": "Can I pay by card?", "spanish": "¿Puedo pagar con tarjeta?", "pronunciation": "PWEH-doh pah-GAR kon tar-HEH-tah", "category": "dining", "alts": ["Do you take cards?", "Credit card ok?", "Card payment?"]},
    {"id": "dining_019", "english": "Cash only?", "spanish": "¿Solo efectivo?", "pronunciation": "SOH-loh eh-fek-TEE-voh", "category": "dining", "alts": ["Only cash?", "Do you only take cash?"]},
    {"id": "dining_020", "english": "Keep the change.", "spanish": "Quédese con el cambio.", "pronunciation": "KEH-deh-seh kon el KAM-bee-oh", "category": "dining", "alts": ["Keep the rest", "That's for you"]},
    {"id": "dining_021", "english": "A coffee, please.", "spanish": "Un café, por favor.", "pronunciation": "oon kah-FEH por fah-VOR", "category": "dining", "alts": ["Coffee please", "Can I have a coffee?", "One coffee"]},
    {"id": "dining_022", "english": "A beer, please.", "spanish": "Una cerveza, por favor.", "pronunciation": "OO-nah ser-VEH-sah por fah-VOR", "category": "dining", "alts": ["Beer please", "Can I have a beer?", "One beer"]},
    {"id": "dining_023", "english": "A glass of wine, please.", "spanish": "Una copa de vino, por favor.", "pronunciation": "OO-nah KOH-pah deh VEE-noh por fah-VOR", "category": "dining", "alts": ["Wine please", "Glass of wine", "Red wine please"]},
    {"id": "dining_024", "english": "Is the tip included?", "spanish": "¿Está incluida la propina?", "pronunciation": "es-TAH een-kloo-EE-dah lah proh-PEE-nah", "category": "dining", "alts": ["Is tip included?", "Does this include tip?", "Tip included?"]},
    {"id": "dining_025", "english": "I would like breakfast.", "spanish": "Quisiera desayuno.", "pronunciation": "kee-see-EH-rah deh-sah-YOO-noh", "category": "dining", "alts": ["Breakfast please", "For breakfast"]},
    {"id": "dining_026", "english": "I would like lunch.", "spanish": "Quisiera almuerzo.", "pronunciation": "kee-see-EH-rah al-MWER-soh", "category": "dining", "alts": ["Lunch please", "For lunch"]},
    {"id": "dining_027", "english": "I would like dinner.", "spanish": "Quisiera cenar.", "pronunciation": "kee-see-EH-rah seh-NAR", "category": "dining", "alts": ["Dinner please", "For dinner"]},
    {"id": "dining_028", "english": "Is this gluten-free?", "spanish": "¿Es sin gluten?", "pronunciation": "es seen GLOO-ten", "category": "dining", "alts": ["Gluten free?", "Does this have gluten?"]},
    {"id": "dining_029", "english": "More bread, please.", "spanish": "Más pan, por favor.", "pronunciation": "mahs pahn por fah-VOR", "category": "dining", "alts": ["Extra bread please", "Can we have more bread?"]},
    {"id": "dining_030", "english": "The food is cold.", "spanish": "La comida está fría.", "pronunciation": "lah koh-MEE-dah es-TAH FREE-ah", "category": "dining", "alts": ["This is cold", "My food is cold"]},
    {"id": "dining_031", "english": "This is not what I ordered.", "spanish": "Esto no es lo que pedí.", "pronunciation": "ES-toh noh es loh keh peh-DEE", "category": "dining", "alts": ["I didn't order this", "Wrong order", "This is wrong"]},
    {"id": "dining_032", "english": "Can I have a fork?", "spanish": "¿Me da un tenedor?", "pronunciation": "meh dah oon teh-neh-DOR", "category": "dining", "alts": ["Fork please", "I need a fork"]},
    {"id": "dining_033", "english": "Can I have a knife?", "spanish": "¿Me da un cuchillo?", "pronunciation": "meh dah oon koo-CHEE-yoh", "category": "dining", "alts": ["Knife please", "I need a knife"]},
    {"id": "dining_034", "english": "Can I have a spoon?", "spanish": "¿Me da una cuchara?", "pronunciation": "meh dah OO-nah koo-CHAH-rah", "category": "dining", "alts": ["Spoon please", "I need a spoon"]},
    {"id": "dining_035", "english": "Can I have napkins?", "spanish": "¿Me da servilletas?", "pronunciation": "meh dah ser-vee-YEH-tahs", "category": "dining", "alts": ["Napkins please", "I need napkins"]},
    {"id": "dining_036", "english": "I would like ice.", "spanish": "Quisiera hielo.", "pronunciation": "kee-see-EH-rah YEH-loh", "category": "dining", "alts": ["With ice please", "Ice please", "Can I have ice?"]},
    {"id": "dining_037", "english": "No ice, please.", "spanish": "Sin hielo, por favor.", "pronunciation": "seen YEH-loh por fah-VOR", "category": "dining", "alts": ["Without ice", "Hold the ice"]},
    {"id": "dining_038", "english": "What are the specials?", "spanish": "¿Cuáles son los especiales?", "pronunciation": "KWAH-les son los es-peh-see-AH-les", "category": "dining", "alts": ["Daily specials?", "What's on special?"]},
    {"id": "dining_039", "english": "Is this fresh?", "spanish": "¿Está fresco?", "pronunciation": "es-TAH FRES-koh", "category": "dining", "alts": ["Is it fresh?", "Fresh today?"]},
    {"id": "dining_040", "english": "To go, please.", "spanish": "Para llevar, por favor.", "pronunciation": "PAH-rah yeh-VAR por fah-VOR", "category": "dining", "alts": ["Takeaway please", "For takeout", "To take away"]},
    {"id": "dining_041", "english": "For here.", "spanish": "Para comer aquí.", "pronunciation": "PAH-rah koh-MER ah-KEE", "category": "dining", "alts": ["Eating here", "Dine in"]},
    {"id": "dining_042", "english": "Can I see the dessert menu?", "spanish": "¿Puedo ver el menú de postres?", "pronunciation": "PWEH-doh ver el meh-NOO deh POHS-tres", "category": "dining", "alts": ["Dessert menu please", "What desserts do you have?"]},
    {"id": "dining_043", "english": "I'm still looking.", "spanish": "Todavía estoy mirando.", "pronunciation": "toh-dah-VEE-ah es-TOY mee-RAHN-doh", "category": "dining", "alts": ["Still deciding", "Give me a minute", "I need more time"]},
    {"id": "dining_044", "english": "Can I have the same?", "spanish": "¿Puedo tener lo mismo?", "pronunciation": "PWEH-doh teh-NER loh MEES-moh", "category": "dining", "alts": ["Same for me", "I'll have what they're having"]},
    {"id": "dining_045", "english": "Is there a children's menu?", "spanish": "¿Hay menú para niños?", "pronunciation": "eye meh-NOO PAH-rah NEE-nyohs", "category": "dining", "alts": ["Kids menu?", "Menu for children?"]},
    {"id": "dining_046", "english": "Can you make it less salty?", "spanish": "¿Puede hacerlo menos salado?", "pronunciation": "PWEH-deh ah-SER-loh MEH-nohs sah-LAH-doh", "category": "dining", "alts": ["Less salt please", "Not too salty"]},
    {"id": "dining_047", "english": "I'm full.", "spanish": "Estoy lleno/a.", "pronunciation": "es-TOY YEH-noh", "category": "dining", "alts": ["I'm stuffed", "I can't eat more", "No more thanks"]},
    {"id": "dining_048", "english": "Can I have a box?", "spanish": "¿Me da una caja?", "pronunciation": "meh dah OO-nah KAH-hah", "category": "dining", "alts": ["Box for leftovers", "Takeaway box please", "To-go box"]},
    {"id": "dining_049", "english": "Do you have WiFi?", "spanish": "¿Tienen WiFi?", "pronunciation": "tee-EH-nen WEE-fee", "category": "dining", "alts": ["Is there WiFi?", "WiFi password?", "What's the WiFi?"]},
    {"id": "dining_050", "english": "Where is the restroom?", "spanish": "¿Dónde está el baño?", "pronunciation": "DOHN-deh es-TAH el BAN-yoh", "category": "dining", "alts": ["Bathroom?", "Restroom please", "Where's the toilet?"]},

    # TRANSPORTATION (40 phrases)
    {"id": "transportation_001", "english": "How much is a taxi to downtown?", "spanish": "¿Cuánto cuesta un taxi al centro?", "pronunciation": "KWAN-toh KWES-tah oon TAK-see al SEN-troh", "category": "transportation", "alts": ["Taxi to downtown price", "How much for a taxi to the center?", "Taxi fare to downtown?"]},
    {"id": "transportation_002", "english": "Where is the bus stop?", "spanish": "¿Dónde está la parada de autobús?", "pronunciation": "DOHN-deh es-TAH lah pah-RAH-dah deh ow-toh-BOOS", "category": "transportation", "alts": ["Bus stop?", "Where can I catch the bus?", "Where's the bus station?"]},
    {"id": "transportation_003", "english": "Where is the train station?", "spanish": "¿Dónde está la estación de tren?", "pronunciation": "DOHN-deh es-TAH lah es-tah-see-ON deh tren", "category": "transportation", "alts": ["Train station?", "Where's the train?", "How to get to the train station?"]},
    {"id": "transportation_004", "english": "I need a taxi.", "spanish": "Necesito un taxi.", "pronunciation": "neh-seh-SEE-toh oon TAK-see", "category": "transportation", "alts": ["Call me a taxi", "Can you get me a taxi?", "Taxi please"]},
    {"id": "transportation_005", "english": "How do I get to the airport?", "spanish": "¿Cómo llego al aeropuerto?", "pronunciation": "KOH-moh YEH-goh al ah-eh-roh-PWER-toh", "category": "transportation", "alts": ["Directions to the airport", "Airport please", "How to get to the airport?"]},
    {"id": "transportation_006", "english": "One ticket, please.", "spanish": "Un billete, por favor.", "pronunciation": "oon bee-YEH-teh por fah-VOR", "category": "transportation", "alts": ["Single ticket", "One fare please"]},
    {"id": "transportation_007", "english": "Round trip ticket, please.", "spanish": "Billete de ida y vuelta, por favor.", "pronunciation": "bee-YEH-teh deh EE-dah ee VWEL-tah por fah-VOR", "category": "transportation", "alts": ["Return ticket please", "Two way ticket"]},
    {"id": "transportation_008", "english": "What time does the bus leave?", "spanish": "¿A qué hora sale el autobús?", "pronunciation": "ah keh OH-rah SAH-leh el ow-toh-BOOS", "category": "transportation", "alts": ["When does the bus depart?", "Bus departure time?"]},
    {"id": "transportation_009", "english": "What time does the train leave?", "spanish": "¿A qué hora sale el tren?", "pronunciation": "ah keh OH-rah SAH-leh el tren", "category": "transportation", "alts": ["When does the train depart?", "Train departure time?"]},
    {"id": "transportation_010", "english": "Is this the right bus?", "spanish": "¿Es este el autobús correcto?", "pronunciation": "es ES-teh el ow-toh-BOOS koh-REK-toh", "category": "transportation", "alts": ["Is this the correct bus?", "Does this bus go to...?"]},
    {"id": "transportation_011", "english": "Where can I rent a car?", "spanish": "¿Dónde puedo alquilar un coche?", "pronunciation": "DOHN-deh PWEH-doh al-kee-LAR oon KOH-cheh", "category": "transportation", "alts": ["Car rental?", "Where to rent a car?", "Rent a car?"]},
    {"id": "transportation_012", "english": "I have a reservation.", "spanish": "Tengo una reservación.", "pronunciation": "TEN-goh OO-nah reh-ser-vah-see-ON", "category": "transportation", "alts": ["I booked already", "I made a reservation"]},
    {"id": "transportation_013", "english": "Stop here, please.", "spanish": "Pare aquí, por favor.", "pronunciation": "PAH-reh ah-KEE por fah-VOR", "category": "transportation", "alts": ["Here is fine", "This is my stop", "Drop me here"]},
    {"id": "transportation_014", "english": "How long is the trip?", "spanish": "¿Cuánto dura el viaje?", "pronunciation": "KWAN-toh DOO-rah el vee-AH-heh", "category": "transportation", "alts": ["How long does it take?", "Trip duration?", "How many hours?"]},
    {"id": "transportation_015", "english": "Is there a metro?", "spanish": "¿Hay metro?", "pronunciation": "eye MEH-troh", "category": "transportation", "alts": ["Is there a subway?", "Metro station?", "Underground?"]},
    {"id": "transportation_016", "english": "Which platform?", "spanish": "¿Qué andén?", "pronunciation": "keh an-DEN", "category": "transportation", "alts": ["What platform?", "Which track?"]},
    {"id": "transportation_017", "english": "Is this seat taken?", "spanish": "¿Está ocupado este asiento?", "pronunciation": "es-TAH oh-koo-PAH-doh ES-teh ah-see-EN-toh", "category": "transportation", "alts": ["Is this seat free?", "Anyone sitting here?", "Can I sit here?"]},
    {"id": "transportation_018", "english": "Can you take me to this address?", "spanish": "¿Puede llevarme a esta dirección?", "pronunciation": "PWEH-deh yeh-VAR-meh ah ES-tah dee-rek-see-ON", "category": "transportation", "alts": ["Take me here please", "Go to this address"]},
    {"id": "transportation_019", "english": "How much do I owe you?", "spanish": "¿Cuánto le debo?", "pronunciation": "KWAN-toh leh DEH-boh", "category": "transportation", "alts": ["What do I owe?", "How much is the fare?"]},
    {"id": "transportation_020", "english": "Where is the ticket office?", "spanish": "¿Dónde está la taquilla?", "pronunciation": "DOHN-deh es-TAH lah tah-KEE-yah", "category": "transportation", "alts": ["Ticket counter?", "Where to buy tickets?"]},
    {"id": "transportation_021", "english": "The next stop, please.", "spanish": "La próxima parada, por favor.", "pronunciation": "lah PROHK-see-mah pah-RAH-dah por fah-VOR", "category": "transportation", "alts": ["I get off at the next stop", "Next stop is mine"]},
    {"id": "transportation_022", "english": "Is there a direct flight?", "spanish": "¿Hay vuelo directo?", "pronunciation": "eye VWEH-loh dee-REK-toh", "category": "transportation", "alts": ["Direct flight?", "Non-stop flight?"]},
    {"id": "transportation_023", "english": "What is the speed limit?", "spanish": "¿Cuál es el límite de velocidad?", "pronunciation": "kwal es el LEE-mee-teh deh veh-loh-see-DAD", "category": "transportation", "alts": ["Speed limit here?", "How fast can I go?"]},
    {"id": "transportation_024", "english": "Where can I park?", "spanish": "¿Dónde puedo aparcar?", "pronunciation": "DOHN-deh PWEH-doh ah-par-KAR", "category": "transportation", "alts": ["Parking?", "Where is parking?", "Is there parking?"]},
    {"id": "transportation_025", "english": "Fill it up, please.", "spanish": "Llénelo, por favor.", "pronunciation": "YEH-neh-loh por fah-VOR", "category": "transportation", "alts": ["Full tank please", "Fill the tank"]},
    {"id": "transportation_026", "english": "I need gasoline.", "spanish": "Necesito gasolina.", "pronunciation": "neh-seh-SEE-toh gah-soh-LEE-nah", "category": "transportation", "alts": ["I need gas", "Where's a gas station?", "Fuel please"]},
    {"id": "transportation_027", "english": "The car broke down.", "spanish": "El coche se averió.", "pronunciation": "el KOH-cheh seh ah-veh-ree-OH", "category": "transportation", "alts": ["My car broke down", "Car trouble", "The car won't start"]},
    {"id": "transportation_028", "english": "I have a flat tire.", "spanish": "Tengo una llanta ponchada.", "pronunciation": "TEN-goh OO-nah YAHN-tah pon-CHAH-dah", "category": "transportation", "alts": ["Flat tire", "My tire is flat"]},
    {"id": "transportation_029", "english": "Call a tow truck.", "spanish": "Llame a una grúa.", "pronunciation": "YAH-meh ah OO-nah GROO-ah", "category": "transportation", "alts": ["I need a tow", "Tow truck please"]},
    {"id": "transportation_030", "english": "Is there traffic?", "spanish": "¿Hay tráfico?", "pronunciation": "eye TRAH-fee-koh", "category": "transportation", "alts": ["How's traffic?", "Is there congestion?"]},
    {"id": "transportation_031", "english": "Take the highway.", "spanish": "Tome la autopista.", "pronunciation": "TOH-meh lah ow-toh-PEES-tah", "category": "transportation", "alts": ["Use the freeway", "Highway please"]},
    {"id": "transportation_032", "english": "Turn left.", "spanish": "Gire a la izquierda.", "pronunciation": "HEE-reh ah lah ees-kee-ER-dah", "category": "transportation", "alts": ["Go left", "Left turn"]},
    {"id": "transportation_033", "english": "Turn right.", "spanish": "Gire a la derecha.", "pronunciation": "HEE-reh ah lah deh-REH-chah", "category": "transportation", "alts": ["Go right", "Right turn"]},
    {"id": "transportation_034", "english": "Go straight.", "spanish": "Siga derecho.", "pronunciation": "SEE-gah deh-REH-choh", "category": "transportation", "alts": ["Straight ahead", "Continue straight"]},
    {"id": "transportation_035", "english": "Where is baggage claim?", "spanish": "¿Dónde está la recogida de equipaje?", "pronunciation": "DOHN-deh es-TAH lah reh-koh-HEE-dah deh eh-kee-PAH-heh", "category": "transportation", "alts": ["Baggage claim?", "Where do I get my luggage?"]},
    {"id": "transportation_036", "english": "My luggage is lost.", "spanish": "Mi equipaje se perdió.", "pronunciation": "mee eh-kee-PAH-heh seh per-dee-OH", "category": "transportation", "alts": ["I lost my luggage", "Can't find my bags", "Lost baggage"]},
    {"id": "transportation_037", "english": "Where is the departure gate?", "spanish": "¿Dónde está la puerta de embarque?", "pronunciation": "DOHN-deh es-TAH lah PWER-tah deh em-BAR-keh", "category": "transportation", "alts": ["Which gate?", "Departure gate?", "Boarding gate?"]},
    {"id": "transportation_038", "english": "Is the flight on time?", "spanish": "¿El vuelo está a tiempo?", "pronunciation": "el VWEH-loh es-TAH ah tee-EM-poh", "category": "transportation", "alts": ["Flight on schedule?", "Is my flight delayed?"]},
    {"id": "transportation_039", "english": "I missed my flight.", "spanish": "Perdí mi vuelo.", "pronunciation": "per-DEE mee VWEH-loh", "category": "transportation", "alts": ["I missed the plane", "My flight left without me"]},
    {"id": "transportation_040", "english": "Where is customs?", "spanish": "¿Dónde está la aduana?", "pronunciation": "DOHN-deh es-TAH lah ah-DWAH-nah", "category": "transportation", "alts": ["Customs?", "Where do I go through customs?"]},

    # DIRECTIONS (40 phrases)
    {"id": "directions_001", "english": "How do I get to the airport?", "spanish": "¿Cómo llego al aeropuerto?", "pronunciation": "KOH-moh YEH-goh al ah-eh-ROH-pwehr-toh", "category": "directions", "alts": ["Directions to the airport", "How can I get to the airport?", "Where is the airport?"]},
    {"id": "directions_002", "english": "Where is the nearest ATM?", "spanish": "¿Dónde está el cajero más cercano?", "pronunciation": "DOHN-deh es-TAH el kah-HEH-roh mahs ser-KAH-noh", "category": "directions", "alts": ["ATM nearby?", "Where can I find an ATM?", "Nearest cash machine?"]},
    {"id": "directions_003", "english": "Where is the pharmacy?", "spanish": "¿Dónde está la farmacia?", "pronunciation": "DOHN-deh es-TAH lah far-MAH-see-ah", "category": "directions", "alts": ["Pharmacy?", "Where's the drugstore?", "Nearest pharmacy?"]},
    {"id": "directions_004", "english": "Is it far from here?", "spanish": "¿Está lejos de aquí?", "pronunciation": "es-TAH LEH-hohs deh ah-KEE", "category": "directions", "alts": ["Is it far?", "How far is it?", "Far from here?"]},
    {"id": "directions_005", "english": "Is it nearby?", "spanish": "¿Está cerca?", "pronunciation": "es-TAH SER-kah", "category": "directions", "alts": ["Is it close?", "Nearby?", "Is it walking distance?"]},
    {"id": "directions_006", "english": "Can I walk there?", "spanish": "¿Puedo ir caminando?", "pronunciation": "PWEH-doh eer kah-mee-NAHN-doh", "category": "directions", "alts": ["Is it walkable?", "Can I get there on foot?", "Walking distance?"]},
    {"id": "directions_007", "english": "Where is the city center?", "spanish": "¿Dónde está el centro de la ciudad?", "pronunciation": "DOHN-deh es-TAH el SEN-troh deh lah see-oo-DAD", "category": "directions", "alts": ["Where's downtown?", "City center?", "How to get to downtown?"]},
    {"id": "directions_008", "english": "Where is the beach?", "spanish": "¿Dónde está la playa?", "pronunciation": "DOHN-deh es-TAH lah PLAH-yah", "category": "directions", "alts": ["Beach?", "How do I get to the beach?", "Directions to the beach?"]},
    {"id": "directions_009", "english": "I am lost.", "spanish": "Estoy perdido/a.", "pronunciation": "es-TOY per-DEE-doh", "category": "directions", "alts": ["I'm lost", "I don't know where I am", "I got lost"]},
    {"id": "directions_010", "english": "Can you show me on the map?", "spanish": "¿Puede mostrarme en el mapa?", "pronunciation": "PWEH-deh mohs-TRAR-meh en el MAH-pah", "category": "directions", "alts": ["Show me on the map", "Point it on the map", "Where on the map?"]},
    {"id": "directions_011", "english": "How many blocks?", "spanish": "¿Cuántas cuadras?", "pronunciation": "KWAN-tahs KWAH-drahs", "category": "directions", "alts": ["How many streets?", "How far in blocks?"]},
    {"id": "directions_012", "english": "At the corner.", "spanish": "En la esquina.", "pronunciation": "en lah es-KEE-nah", "category": "directions", "alts": ["On the corner", "At the intersection"]},
    {"id": "directions_013", "english": "Across the street.", "spanish": "Al otro lado de la calle.", "pronunciation": "al OH-troh LAH-doh deh lah KAH-yeh", "category": "directions", "alts": ["On the other side of the street", "Cross the street"]},
    {"id": "directions_014", "english": "Next to the bank.", "spanish": "Al lado del banco.", "pronunciation": "al LAH-doh del BAHN-koh", "category": "directions", "alts": ["Beside the bank", "By the bank"]},
    {"id": "directions_015", "english": "In front of the church.", "spanish": "Enfrente de la iglesia.", "pronunciation": "en-FREN-teh deh lah ee-GLEH-see-ah", "category": "directions", "alts": ["Opposite the church", "Facing the church"]},
    {"id": "directions_016", "english": "Behind the hotel.", "spanish": "Detrás del hotel.", "pronunciation": "deh-TRAHS del oh-TEL", "category": "directions", "alts": ["Back of the hotel", "At the back of the hotel"]},
    {"id": "directions_017", "english": "Where is the supermarket?", "spanish": "¿Dónde está el supermercado?", "pronunciation": "DOHN-deh es-TAH el soo-per-mer-KAH-doh", "category": "directions", "alts": ["Supermarket?", "Grocery store?", "Where can I buy groceries?"]},
    {"id": "directions_018", "english": "Where is the post office?", "spanish": "¿Dónde está la oficina de correos?", "pronunciation": "DOHN-deh es-TAH lah oh-fee-SEE-nah deh koh-REH-ohs", "category": "directions", "alts": ["Post office?", "Where can I mail something?"]},
    {"id": "directions_019", "english": "Where is the museum?", "spanish": "¿Dónde está el museo?", "pronunciation": "DOHN-deh es-TAH el moo-SEH-oh", "category": "directions", "alts": ["Museum?", "How to get to the museum?"]},
    {"id": "directions_020", "english": "Where is the park?", "spanish": "¿Dónde está el parque?", "pronunciation": "DOHN-deh es-TAH el PAR-keh", "category": "directions", "alts": ["Park?", "Nearest park?"]},
    {"id": "directions_021", "english": "Where is the embassy?", "spanish": "¿Dónde está la embajada?", "pronunciation": "DOHN-deh es-TAH lah em-bah-HAH-dah", "category": "directions", "alts": ["Embassy?", "US Embassy?", "American embassy?"]},
    {"id": "directions_022", "english": "Where is the police station?", "spanish": "¿Dónde está la comisaría?", "pronunciation": "DOHN-deh es-TAH lah koh-mee-sah-REE-ah", "category": "directions", "alts": ["Police station?", "Where are the police?"]},
    {"id": "directions_023", "english": "On the left.", "spanish": "A la izquierda.", "pronunciation": "ah lah ees-kee-ER-dah", "category": "directions", "alts": ["To the left", "Left side"]},
    {"id": "directions_024", "english": "On the right.", "spanish": "A la derecha.", "pronunciation": "ah lah deh-REH-chah", "category": "directions", "alts": ["To the right", "Right side"]},
    {"id": "directions_025", "english": "Go straight ahead.", "spanish": "Siga recto.", "pronunciation": "SEE-gah REK-toh", "category": "directions", "alts": ["Straight", "Keep going straight", "Continue straight"]},
    {"id": "directions_026", "english": "At the traffic light.", "spanish": "En el semáforo.", "pronunciation": "en el seh-MAH-foh-roh", "category": "directions", "alts": ["At the stoplight", "At the signal"]},
    {"id": "directions_027", "english": "What street is this?", "spanish": "¿Qué calle es esta?", "pronunciation": "keh KAH-yeh es ES-tah", "category": "directions", "alts": ["Street name?", "Which street?"]},
    {"id": "directions_028", "english": "Where is the main square?", "spanish": "¿Dónde está la plaza principal?", "pronunciation": "DOHN-deh es-TAH lah PLAH-sah preen-see-PAL", "category": "directions", "alts": ["Main plaza?", "Town square?", "Central square?"]},
    {"id": "directions_029", "english": "How do I get to the market?", "spanish": "¿Cómo llego al mercado?", "pronunciation": "KOH-moh YEH-goh al mer-KAH-doh", "category": "directions", "alts": ["Where's the market?", "Market?", "Local market?"]},
    {"id": "directions_030", "english": "Where is a good restaurant?", "spanish": "¿Dónde hay un buen restaurante?", "pronunciation": "DOHN-deh eye oon bwen res-tow-RAHN-teh", "category": "directions", "alts": ["Good restaurant nearby?", "Restaurant recommendation?"]},
    {"id": "directions_031", "english": "Where can I exchange money?", "spanish": "¿Dónde puedo cambiar dinero?", "pronunciation": "DOHN-deh PWEH-doh kahm-bee-AR dee-NEH-roh", "category": "directions", "alts": ["Money exchange?", "Currency exchange?", "Where to exchange currency?"]},
    {"id": "directions_032", "english": "Is there a gas station nearby?", "spanish": "¿Hay una gasolinera cerca?", "pronunciation": "eye OO-nah gah-soh-lee-NEH-rah SER-kah", "category": "directions", "alts": ["Gas station?", "Nearest gas station?", "Petrol station?"]},
    {"id": "directions_033", "english": "Where is the shopping mall?", "spanish": "¿Dónde está el centro comercial?", "pronunciation": "DOHN-deh es-TAH el SEN-troh koh-mer-see-AL", "category": "directions", "alts": ["Mall?", "Shopping center?"]},
    {"id": "directions_034", "english": "Take the first left.", "spanish": "Tome la primera a la izquierda.", "pronunciation": "TOH-meh lah pree-MEH-rah ah lah ees-kee-ER-dah", "category": "directions", "alts": ["First left", "Turn at the first left"]},
    {"id": "directions_035", "english": "Take the second right.", "spanish": "Tome la segunda a la derecha.", "pronunciation": "TOH-meh lah seh-GOON-dah ah lah deh-REH-chah", "category": "directions", "alts": ["Second right", "Turn at the second right"]},
    {"id": "directions_036", "english": "It's at the end of the street.", "spanish": "Está al final de la calle.", "pronunciation": "es-TAH al fee-NAL deh lah KAH-yeh", "category": "directions", "alts": ["End of the street", "At the end of this road"]},
    {"id": "directions_037", "english": "Cross the bridge.", "spanish": "Cruce el puente.", "pronunciation": "KROO-seh el PWEN-teh", "category": "directions", "alts": ["Go over the bridge", "After the bridge"]},
    {"id": "directions_038", "english": "It's on the main street.", "spanish": "Está en la calle principal.", "pronunciation": "es-TAH en lah KAH-yeh preen-see-PAL", "category": "directions", "alts": ["On the main road", "Main street"]},
    {"id": "directions_039", "english": "Do you have a map?", "spanish": "¿Tiene un mapa?", "pronunciation": "tee-EH-neh oon MAH-pah", "category": "directions", "alts": ["Map please", "Can I have a map?"]},
    {"id": "directions_040", "english": "What is the address?", "spanish": "¿Cuál es la dirección?", "pronunciation": "kwal es lah dee-rek-see-ON", "category": "directions", "alts": ["The address?", "Address please"]},

    # HOTEL (30 phrases)
    {"id": "hotel_001", "english": "I have a reservation.", "spanish": "Tengo una reservación.", "pronunciation": "TEN-goh OO-nah reh-ser-vah-see-ON", "category": "hotel", "alts": ["I booked a room", "I made a reservation", "Reservation under..."]},
    {"id": "hotel_002", "english": "Do you have any rooms available?", "spanish": "¿Tienen habitaciones disponibles?", "pronunciation": "tee-EH-nen ah-bee-tah-see-OH-nes dees-poh-NEE-bles", "category": "hotel", "alts": ["Any vacancies?", "Rooms available?", "Do you have a room?"]},
    {"id": "hotel_003", "english": "How much per night?", "spanish": "¿Cuánto cuesta por noche?", "pronunciation": "KWAN-toh KWES-tah por NOH-cheh", "category": "hotel", "alts": ["Price per night?", "Rate per night?", "Nightly rate?"]},
    {"id": "hotel_004", "english": "I would like to check in.", "spanish": "Quisiera registrarme.", "pronunciation": "kee-see-EH-rah reh-hees-TRAR-meh", "category": "hotel", "alts": ["Check in please", "Checking in"]},
    {"id": "hotel_005", "english": "I would like to check out.", "spanish": "Quisiera hacer el checkout.", "pronunciation": "kee-see-EH-rah ah-SER el CHECK-owt", "category": "hotel", "alts": ["Check out please", "Checking out", "I'm leaving"]},
    {"id": "hotel_006", "english": "What time is checkout?", "spanish": "¿A qué hora es el checkout?", "pronunciation": "ah keh OH-rah es el CHECK-owt", "category": "hotel", "alts": ["Checkout time?", "When is checkout?"]},
    {"id": "hotel_007", "english": "Can I have a wake-up call?", "spanish": "¿Puede despertarme?", "pronunciation": "PWEH-deh des-per-TAR-meh", "category": "hotel", "alts": ["Wake up call please", "Morning call please"]},
    {"id": "hotel_008", "english": "The air conditioning doesn't work.", "spanish": "El aire acondicionado no funciona.", "pronunciation": "el AY-reh ah-kon-dee-see-oh-NAH-doh noh foon-see-OH-nah", "category": "hotel", "alts": ["AC is broken", "Air conditioning is not working", "No AC"]},
    {"id": "hotel_009", "english": "I need more towels.", "spanish": "Necesito más toallas.", "pronunciation": "neh-seh-SEE-toh mahs toh-AH-yahs", "category": "hotel", "alts": ["More towels please", "Extra towels", "Can I have towels?"]},
    {"id": "hotel_010", "english": "Is breakfast included?", "spanish": "¿El desayuno está incluido?", "pronunciation": "el deh-sah-YOO-noh es-TAH een-kloo-EE-doh", "category": "hotel", "alts": ["Breakfast included?", "Does it include breakfast?"]},
    {"id": "hotel_011", "english": "What is the WiFi password?", "spanish": "¿Cuál es la contraseña del WiFi?", "pronunciation": "kwal es lah kon-trah-SEH-nyah del WEE-fee", "category": "hotel", "alts": ["WiFi password?", "Internet password?"]},
    {"id": "hotel_012", "english": "Is there a safe in the room?", "spanish": "¿Hay caja fuerte en la habitación?", "pronunciation": "eye KAH-hah FWER-teh en lah ah-bee-tah-see-ON", "category": "hotel", "alts": ["Room safe?", "Safety deposit box?"]},
    {"id": "hotel_013", "english": "Can I store my luggage?", "spanish": "¿Puedo dejar mi equipaje?", "pronunciation": "PWEH-doh deh-HAR mee eh-kee-PAH-heh", "category": "hotel", "alts": ["Luggage storage?", "Store my bags?", "Keep my luggage?"]},
    {"id": "hotel_014", "english": "The room is dirty.", "spanish": "La habitación está sucia.", "pronunciation": "lah ah-bee-tah-see-ON es-TAH SOO-see-ah", "category": "hotel", "alts": ["Room needs cleaning", "Room is not clean"]},
    {"id": "hotel_015", "english": "Can I change rooms?", "spanish": "¿Puedo cambiar de habitación?", "pronunciation": "PWEH-doh kahm-bee-AR deh ah-bee-tah-see-ON", "category": "hotel", "alts": ["Different room please", "Change my room"]},
    {"id": "hotel_016", "english": "I lost my key.", "spanish": "Perdí mi llave.", "pronunciation": "per-DEE mee YAH-veh", "category": "hotel", "alts": ["Key is lost", "Can't find my key", "Lost my room key"]},
    {"id": "hotel_017", "english": "Is there a pool?", "spanish": "¿Hay piscina?", "pronunciation": "eye pee-SEE-nah", "category": "hotel", "alts": ["Swimming pool?", "Pool available?"]},
    {"id": "hotel_018", "english": "Is there a gym?", "spanish": "¿Hay gimnasio?", "pronunciation": "eye heem-NAH-see-oh", "category": "hotel", "alts": ["Fitness center?", "Exercise room?"]},
    {"id": "hotel_019", "english": "Can you call me a taxi?", "spanish": "¿Puede llamarme un taxi?", "pronunciation": "PWEH-deh yah-MAR-meh oon TAK-see", "category": "hotel", "alts": ["Get me a taxi", "Order a taxi please"]},
    {"id": "hotel_020", "english": "Where is the elevator?", "spanish": "¿Dónde está el ascensor?", "pronunciation": "DOHN-deh es-TAH el ah-sen-SOR", "category": "hotel", "alts": ["Elevator?", "Where's the lift?"]},
    {"id": "hotel_021", "english": "Do you have a room with a view?", "spanish": "¿Tienen habitación con vista?", "pronunciation": "tee-EH-nen ah-bee-tah-see-ON kon VEES-tah", "category": "hotel", "alts": ["Room with a view?", "View room?"]},
    {"id": "hotel_022", "english": "I need an extra pillow.", "spanish": "Necesito una almohada extra.", "pronunciation": "neh-seh-SEE-toh OO-nah al-moh-AH-dah EKS-trah", "category": "hotel", "alts": ["Extra pillow please", "Another pillow"]},
    {"id": "hotel_023", "english": "I need an extra blanket.", "spanish": "Necesito una manta extra.", "pronunciation": "neh-seh-SEE-toh OO-nah MAHN-tah EKS-trah", "category": "hotel", "alts": ["Extra blanket please", "Another blanket"]},
    {"id": "hotel_024", "english": "The hot water doesn't work.", "spanish": "No hay agua caliente.", "pronunciation": "noh eye AH-gwah kah-lee-EN-teh", "category": "hotel", "alts": ["No hot water", "Hot water is broken"]},
    {"id": "hotel_025", "english": "What floor is my room on?", "spanish": "¿En qué piso está mi habitación?", "pronunciation": "en keh PEE-soh es-TAH mee ah-bee-tah-see-ON", "category": "hotel", "alts": ["Which floor?", "My room floor?"]},
    {"id": "hotel_026", "english": "Is there room service?", "spanish": "¿Hay servicio a la habitación?", "pronunciation": "eye ser-VEE-see-oh ah lah ah-bee-tah-see-ON", "category": "hotel", "alts": ["Room service?", "Can I order to my room?"]},
    {"id": "hotel_027", "english": "Can I extend my stay?", "spanish": "¿Puedo extender mi estadía?", "pronunciation": "PWEH-doh eks-ten-DER mee es-tah-DEE-ah", "category": "hotel", "alts": ["Stay longer?", "Add another night?"]},
    {"id": "hotel_028", "english": "Is parking available?", "spanish": "¿Hay estacionamiento?", "pronunciation": "eye es-tah-see-oh-nah-mee-EN-toh", "category": "hotel", "alts": ["Parking?", "Can I park here?"]},
    {"id": "hotel_029", "english": "Is there a laundry service?", "spanish": "¿Hay servicio de lavandería?", "pronunciation": "eye ser-VEE-see-oh deh lah-vahn-deh-REE-ah", "category": "hotel", "alts": ["Laundry?", "Can I wash clothes?"]},
    {"id": "hotel_030", "english": "Do not disturb.", "spanish": "No molestar.", "pronunciation": "noh moh-les-TAR", "category": "hotel", "alts": ["Don't disturb", "Privacy please"]},

    # MONEY (20 phrases)
    {"id": "money_001", "english": "Where can I exchange money?", "spanish": "¿Dónde puedo cambiar dinero?", "pronunciation": "DOHN-deh PWEH-doh kahm-bee-AR dee-NEH-roh", "category": "money", "alts": ["Money exchange?", "Currency exchange?", "Exchange rate?"]},
    {"id": "money_002", "english": "What is the exchange rate?", "spanish": "¿Cuál es el tipo de cambio?", "pronunciation": "kwal es el TEE-poh deh KAM-bee-oh", "category": "money", "alts": ["Exchange rate?", "Rate for dollars?"]},
    {"id": "money_003", "english": "Do you accept credit cards?", "spanish": "¿Aceptan tarjetas de crédito?", "pronunciation": "ah-SEP-tahn tar-HEH-tahs deh KREH-dee-toh", "category": "money", "alts": ["Credit card ok?", "Can I pay by card?", "Do you take cards?"]},
    {"id": "money_004", "english": "I need to withdraw money.", "spanish": "Necesito sacar dinero.", "pronunciation": "neh-seh-SEE-toh sah-KAR dee-NEH-roh", "category": "money", "alts": ["Withdraw cash", "Get money from ATM"]},
    {"id": "money_005", "english": "Where is the nearest ATM?", "spanish": "¿Dónde está el cajero más cercano?", "pronunciation": "DOHN-deh es-TAH el kah-HEH-roh mahs ser-KAH-noh", "category": "money", "alts": ["ATM nearby?", "Cash machine?"]},
    {"id": "money_006", "english": "Can I pay in dollars?", "spanish": "¿Puedo pagar en dólares?", "pronunciation": "PWEH-doh pah-GAR en DOH-lah-res", "category": "money", "alts": ["Accept US dollars?", "Dollars ok?"]},
    {"id": "money_007", "english": "I need change.", "spanish": "Necesito cambio.", "pronunciation": "neh-seh-SEE-toh KAM-bee-oh", "category": "money", "alts": ["Small change please", "Do you have change?"]},
    {"id": "money_008", "english": "Keep the change.", "spanish": "Quédese con el cambio.", "pronunciation": "KEH-deh-seh kon el KAM-bee-oh", "category": "money", "alts": ["That's for you", "No change needed"]},
    {"id": "money_009", "english": "This is too expensive.", "spanish": "Esto es muy caro.", "pronunciation": "ES-toh es moo-ee KAH-roh", "category": "money", "alts": ["Too expensive", "That's too much", "It's too pricey"]},
    {"id": "money_010", "english": "Can you give me a discount?", "spanish": "¿Me puede dar un descuento?", "pronunciation": "meh PWEH-deh dar oon des-KWEN-toh", "category": "money", "alts": ["Discount please?", "Any discount?", "Lower price?"]},
    {"id": "money_011", "english": "How much in total?", "spanish": "¿Cuánto es en total?", "pronunciation": "KWAN-toh es en toh-TAL", "category": "money", "alts": ["Total?", "What's the total?"]},
    {"id": "money_012", "english": "Can I get a receipt?", "spanish": "¿Me da un recibo?", "pronunciation": "meh dah oon reh-SEE-boh", "category": "money", "alts": ["Receipt please", "I need a receipt"]},
    {"id": "money_013", "english": "Is tax included?", "spanish": "¿Está incluido el impuesto?", "pronunciation": "es-TAH een-kloo-EE-doh el eem-PWES-toh", "category": "money", "alts": ["Tax included?", "Does this include tax?"]},
    {"id": "money_014", "english": "I was overcharged.", "spanish": "Me cobraron de más.", "pronunciation": "meh koh-BRAH-ron deh mahs", "category": "money", "alts": ["You charged too much", "This is wrong"]},
    {"id": "money_015", "english": "There's a mistake in the bill.", "spanish": "Hay un error en la cuenta.", "pronunciation": "eye oon eh-ROR en lah KWEN-tah", "category": "money", "alts": ["Bill is wrong", "Check the bill"]},
    {"id": "money_016", "english": "Can I pay in cash?", "spanish": "¿Puedo pagar en efectivo?", "pronunciation": "PWEH-doh pah-GAR en eh-fek-TEE-voh", "category": "money", "alts": ["Cash payment ok?", "Pay cash?"]},
    {"id": "money_017", "english": "Do you have smaller bills?", "spanish": "¿Tiene billetes más pequeños?", "pronunciation": "tee-EH-neh bee-YEH-tes mahs peh-KEN-yohs", "category": "money", "alts": ["Smaller denomination?", "Change for large bill?"]},
    {"id": "money_018", "english": "The ATM ate my card.", "spanish": "El cajero se tragó mi tarjeta.", "pronunciation": "el kah-HEH-roh seh trah-GOH mee tar-HEH-tah", "category": "money", "alts": ["ATM took my card", "Card stuck in ATM"]},
    {"id": "money_019", "english": "I need to report a lost card.", "spanish": "Necesito reportar una tarjeta perdida.", "pronunciation": "neh-seh-SEE-toh reh-por-TAR OO-nah tar-HEH-tah per-DEE-dah", "category": "money", "alts": ["Lost my card", "Card is missing"]},
    {"id": "money_020", "english": "What is the minimum purchase?", "spanish": "¿Cuál es la compra mínima?", "pronunciation": "kwal es lah KOM-prah MEE-nee-mah", "category": "money", "alts": ["Minimum for card?", "Minimum purchase?"]},

    # SHOPPING (30 phrases)
    {"id": "shopping_001", "english": "I'm just looking.", "spanish": "Solo estoy mirando.", "pronunciation": "SOH-loh es-TOY mee-RAHN-doh", "category": "shopping", "alts": ["Just browsing", "Just looking around"]},
    {"id": "shopping_002", "english": "Do you have this in a different size?", "spanish": "¿Tiene esto en otra talla?", "pronunciation": "tee-EH-neh ES-toh en OH-trah TAH-yah", "category": "shopping", "alts": ["Different size?", "Other sizes?", "Bigger/smaller size?"]},
    {"id": "shopping_003", "english": "Do you have this in a different color?", "spanish": "¿Tiene esto en otro color?", "pronunciation": "tee-EH-neh ES-toh en OH-troh koh-LOR", "category": "shopping", "alts": ["Different color?", "Other colors?"]},
    {"id": "shopping_004", "english": "Can I try this on?", "spanish": "¿Puedo probármelo?", "pronunciation": "PWEH-doh proh-BAR-meh-loh", "category": "shopping", "alts": ["Can I try it?", "Where's the fitting room?"]},
    {"id": "shopping_005", "english": "Where is the fitting room?", "spanish": "¿Dónde está el probador?", "pronunciation": "DOHN-deh es-TAH el proh-bah-DOR", "category": "shopping", "alts": ["Fitting room?", "Dressing room?", "Where can I try this?"]},
    {"id": "shopping_006", "english": "It's too big.", "spanish": "Es demasiado grande.", "pronunciation": "es deh-mah-see-AH-doh GRAHN-deh", "category": "shopping", "alts": ["Too big", "Too large"]},
    {"id": "shopping_007", "english": "It's too small.", "spanish": "Es demasiado pequeño.", "pronunciation": "es deh-mah-see-AH-doh peh-KEN-yoh", "category": "shopping", "alts": ["Too small", "Too tight"]},
    {"id": "shopping_008", "english": "I'll take it.", "spanish": "Me lo llevo.", "pronunciation": "meh loh YEH-voh", "category": "shopping", "alts": ["I'll buy it", "I want this one"]},
    {"id": "shopping_009", "english": "Can I return this?", "spanish": "¿Puedo devolver esto?", "pronunciation": "PWEH-doh deh-vol-VER ES-toh", "category": "shopping", "alts": ["Return policy?", "Can I get a refund?"]},
    {"id": "shopping_010", "english": "Do you have a bag?", "spanish": "¿Tiene una bolsa?", "pronunciation": "tee-EH-neh OO-nah BOL-sah", "category": "shopping", "alts": ["Bag please", "Shopping bag?"]},
    {"id": "shopping_011", "english": "What time do you close?", "spanish": "¿A qué hora cierran?", "pronunciation": "ah keh OH-rah see-EH-rran", "category": "shopping", "alts": ["Closing time?", "When do you close?"]},
    {"id": "shopping_012", "english": "What time do you open?", "spanish": "¿A qué hora abren?", "pronunciation": "ah keh OH-rah AH-bren", "category": "shopping", "alts": ["Opening time?", "When do you open?"]},
    {"id": "shopping_013", "english": "Is this on sale?", "spanish": "¿Esto está en oferta?", "pronunciation": "ES-toh es-TAH en oh-FER-tah", "category": "shopping", "alts": ["On sale?", "Any discount?"]},
    {"id": "shopping_014", "english": "Where is the checkout?", "spanish": "¿Dónde está la caja?", "pronunciation": "DOHN-deh es-TAH lah KAH-hah", "category": "shopping", "alts": ["Checkout?", "Where do I pay?", "Cash register?"]},
    {"id": "shopping_015", "english": "Can you wrap it as a gift?", "spanish": "¿Puede envolverlo para regalo?", "pronunciation": "PWEH-deh en-vol-VER-loh PAH-rah reh-GAH-loh", "category": "shopping", "alts": ["Gift wrap please", "Wrap it?"]},
    {"id": "shopping_016", "english": "Do you ship internationally?", "spanish": "¿Hacen envíos internacionales?", "pronunciation": "AH-sen en-VEE-ohs een-ter-nah-see-oh-NAH-les", "category": "shopping", "alts": ["Ship abroad?", "International shipping?"]},
    {"id": "shopping_017", "english": "I need a medium size.", "spanish": "Necesito talla mediana.", "pronunciation": "neh-seh-SEE-toh TAH-yah meh-dee-AH-nah", "category": "shopping", "alts": ["Medium please", "Size medium"]},
    {"id": "shopping_018", "english": "Do you have anything cheaper?", "spanish": "¿Tiene algo más barato?", "pronunciation": "tee-EH-neh AL-goh mahs bah-RAH-toh", "category": "shopping", "alts": ["Something cheaper?", "Less expensive?"]},
    {"id": "shopping_019", "english": "Is this handmade?", "spanish": "¿Es hecho a mano?", "pronunciation": "es EH-choh ah MAH-noh", "category": "shopping", "alts": ["Handmade?", "Made by hand?"]},
    {"id": "shopping_020", "english": "Is this authentic?", "spanish": "¿Es auténtico?", "pronunciation": "es ow-TEN-tee-koh", "category": "shopping", "alts": ["Is it real?", "Genuine?"]},
    {"id": "shopping_021", "english": "What is this made of?", "spanish": "¿De qué está hecho?", "pronunciation": "deh keh es-TAH EH-choh", "category": "shopping", "alts": ["Material?", "What material?"]},
    {"id": "shopping_022", "english": "I'm looking for souvenirs.", "spanish": "Busco recuerdos.", "pronunciation": "BOOS-koh reh-KWER-dohs", "category": "shopping", "alts": ["Souvenirs?", "Where are souvenirs?"]},
    {"id": "shopping_023", "english": "Can I see that one?", "spanish": "¿Puedo ver ese?", "pronunciation": "PWEH-doh ver EH-seh", "category": "shopping", "alts": ["Show me that", "That one please"]},
    {"id": "shopping_024", "english": "Do you have more in stock?", "spanish": "¿Tienen más en inventario?", "pronunciation": "tee-EH-nen mahs en een-ven-TAH-ree-oh", "category": "shopping", "alts": ["More in back?", "Any more?"]},
    {"id": "shopping_025", "english": "Is this the final price?", "spanish": "¿Es el precio final?", "pronunciation": "es el PREH-see-oh fee-NAL", "category": "shopping", "alts": ["Final price?", "Best price?"]},
    {"id": "shopping_026", "english": "Can you hold this for me?", "spanish": "¿Puede guardármelo?", "pronunciation": "PWEH-deh gwar-DAR-meh-loh", "category": "shopping", "alts": ["Hold this please", "Keep it for me"]},
    {"id": "shopping_027", "english": "I need batteries.", "spanish": "Necesito pilas.", "pronunciation": "neh-seh-SEE-toh PEE-lahs", "category": "shopping", "alts": ["Batteries?", "Where are batteries?"]},
    {"id": "shopping_028", "english": "Do you have a warranty?", "spanish": "¿Tiene garantía?", "pronunciation": "tee-EH-neh gah-rahn-TEE-ah", "category": "shopping", "alts": ["Warranty?", "Is there a guarantee?"]},
    {"id": "shopping_029", "english": "I'm just window shopping.", "spanish": "Solo estoy viendo escaparates.", "pronunciation": "SOH-loh es-TOY vee-EN-doh es-kah-pah-RAH-tes", "category": "shopping", "alts": ["Just looking at displays", "Browsing"]},
    {"id": "shopping_030", "english": "Where can I find...?", "spanish": "¿Dónde puedo encontrar...?", "pronunciation": "DOHN-deh PWEH-doh en-kon-TRAR", "category": "shopping", "alts": ["Where is...?", "Do you have...?"]},

    # HEALTH (30 phrases)
    {"id": "health_001", "english": "Where is the hospital?", "spanish": "¿Dónde está el hospital?", "pronunciation": "DOHN-deh es-TAH el os-pee-TAL", "category": "health", "alts": ["Hospital?", "Where's the hospital?", "How do I get to the hospital?"]},
    {"id": "health_002", "english": "I need a doctor.", "spanish": "Necesito un médico.", "pronunciation": "neh-seh-SEE-toh oon MEH-dee-koh", "category": "health", "alts": ["Doctor please", "I need to see a doctor", "Get me a doctor"]},
    {"id": "health_003", "english": "I don't feel well.", "spanish": "No me siento bien.", "pronunciation": "noh meh see-EN-toh bee-EN", "category": "health", "alts": ["I feel sick", "I'm not feeling well", "I feel ill"]},
    {"id": "health_004", "english": "I have a headache.", "spanish": "Tengo dolor de cabeza.", "pronunciation": "TEN-goh doh-LOR deh kah-BEH-sah", "category": "health", "alts": ["My head hurts", "Headache"]},
    {"id": "health_005", "english": "I have a stomachache.", "spanish": "Tengo dolor de estómago.", "pronunciation": "TEN-goh doh-LOR deh es-TOH-mah-goh", "category": "health", "alts": ["My stomach hurts", "Stomachache"]},
    {"id": "health_006", "english": "I have a fever.", "spanish": "Tengo fiebre.", "pronunciation": "TEN-goh fee-EH-breh", "category": "health", "alts": ["I'm feverish", "High temperature"]},
    {"id": "health_007", "english": "I have allergies.", "spanish": "Tengo alergias.", "pronunciation": "TEN-goh ah-LAIR-hee-ahs", "category": "health", "alts": ["I'm allergic", "Allergies"]},
    {"id": "health_008", "english": "I need medication.", "spanish": "Necesito medicamento.", "pronunciation": "neh-seh-SEE-toh meh-dee-kah-MEN-toh", "category": "health", "alts": ["I need medicine", "Medication please"]},
    {"id": "health_009", "english": "Where is the pharmacy?", "spanish": "¿Dónde está la farmacia?", "pronunciation": "DOHN-deh es-TAH lah far-MAH-see-ah", "category": "health", "alts": ["Pharmacy?", "Drugstore?"]},
    {"id": "health_010", "english": "I need pain medicine.", "spanish": "Necesito medicina para el dolor.", "pronunciation": "neh-seh-SEE-toh meh-dee-SEE-nah PAH-rah el doh-LOR", "category": "health", "alts": ["Painkillers?", "Something for pain"]},
    {"id": "health_011", "english": "I cut myself.", "spanish": "Me corté.", "pronunciation": "meh kor-TEH", "category": "health", "alts": ["I have a cut", "I'm bleeding"]},
    {"id": "health_012", "english": "I burned myself.", "spanish": "Me quemé.", "pronunciation": "meh keh-MEH", "category": "health", "alts": ["I got burned", "I have a burn"]},
    {"id": "health_013", "english": "I twisted my ankle.", "spanish": "Me torcí el tobillo.", "pronunciation": "meh tor-SEE el toh-BEE-yoh", "category": "health", "alts": ["Sprained ankle", "My ankle hurts"]},
    {"id": "health_014", "english": "I need a bandage.", "spanish": "Necesito una venda.", "pronunciation": "neh-seh-SEE-toh OO-nah VEN-dah", "category": "health", "alts": ["Bandage please", "Do you have bandages?"]},
    {"id": "health_015", "english": "I am diabetic.", "spanish": "Soy diabético/a.", "pronunciation": "soy dee-ah-BEH-tee-koh", "category": "health", "alts": ["I have diabetes", "Diabetic"]},
    {"id": "health_016", "english": "I take this medication.", "spanish": "Tomo este medicamento.", "pronunciation": "TOH-moh ES-teh meh-dee-kah-MEN-toh", "category": "health", "alts": ["I'm on this medicine", "This is my medication"]},
    {"id": "health_017", "english": "I need an ambulance.", "spanish": "Necesito una ambulancia.", "pronunciation": "neh-seh-SEE-toh OO-nah am-boo-LAHN-see-ah", "category": "health", "alts": ["Call an ambulance", "Ambulance please"]},
    {"id": "health_018", "english": "I have asthma.", "spanish": "Tengo asma.", "pronunciation": "TEN-goh AHS-mah", "category": "health", "alts": ["I'm asthmatic", "Asthma"]},
    {"id": "health_019", "english": "I can't breathe well.", "spanish": "No puedo respirar bien.", "pronunciation": "noh PWEH-doh res-pee-RAR bee-EN", "category": "health", "alts": ["Difficulty breathing", "Hard to breathe"]},
    {"id": "health_020", "english": "I feel dizzy.", "spanish": "Me siento mareado/a.", "pronunciation": "meh see-EN-toh mah-reh-AH-doh", "category": "health", "alts": ["I'm dizzy", "Dizzy"]},
    {"id": "health_021", "english": "I feel nauseous.", "spanish": "Tengo náuseas.", "pronunciation": "TEN-goh NOW-seh-ahs", "category": "health", "alts": ["I feel like vomiting", "Nauseous"]},
    {"id": "health_022", "english": "I have diarrhea.", "spanish": "Tengo diarrea.", "pronunciation": "TEN-goh dee-ah-REH-ah", "category": "health", "alts": ["Stomach problems", "Diarrhea"]},
    {"id": "health_023", "english": "I have a cold.", "spanish": "Tengo un resfriado.", "pronunciation": "TEN-goh oon res-free-AH-doh", "category": "health", "alts": ["I'm sick with a cold", "Cold symptoms"]},
    {"id": "health_024", "english": "I have a cough.", "spanish": "Tengo tos.", "pronunciation": "TEN-goh tohs", "category": "health", "alts": ["I'm coughing", "Cough"]},
    {"id": "health_025", "english": "It hurts here.", "spanish": "Me duele aquí.", "pronunciation": "meh DWEH-leh ah-KEE", "category": "health", "alts": ["Pain is here", "This hurts"]},
    {"id": "health_026", "english": "I need my prescription filled.", "spanish": "Necesito surtir mi receta.", "pronunciation": "neh-seh-SEE-toh soor-TEER mee reh-SEH-tah", "category": "health", "alts": ["Fill my prescription", "Prescription medicine"]},
    {"id": "health_027", "english": "Do I need a prescription?", "spanish": "¿Necesito receta médica?", "pronunciation": "neh-seh-SEE-toh reh-SEH-tah MEH-dee-kah", "category": "health", "alts": ["Prescription required?", "Is this prescription only?"]},
    {"id": "health_028", "english": "I have high blood pressure.", "spanish": "Tengo presión alta.", "pronunciation": "TEN-goh preh-see-ON AL-tah", "category": "health", "alts": ["High blood pressure", "Hypertension"]},
    {"id": "health_029", "english": "I am pregnant.", "spanish": "Estoy embarazada.", "pronunciation": "es-TOY em-bah-rah-SAH-dah", "category": "health", "alts": ["I'm pregnant", "Pregnant"]},
    {"id": "health_030", "english": "I need sunscreen.", "spanish": "Necesito protector solar.", "pronunciation": "neh-seh-SEE-toh proh-tek-TOR soh-LAR", "category": "health", "alts": ["Sunscreen?", "Sun protection?"]},

    # EMERGENCY (30 phrases)
    {"id": "emergency_001", "english": "I need help.", "spanish": "Necesito ayuda.", "pronunciation": "neh-seh-SEE-toh ah-YOO-dah", "category": "emergency", "alts": ["Help me", "Please help", "I need assistance", "Help!"]},
    {"id": "emergency_002", "english": "Call the police.", "spanish": "Llame a la policía.", "pronunciation": "YAH-meh ah lah poh-lee-SEE-ah", "category": "emergency", "alts": ["Call police", "Please call the police", "I need the police", "Police!"]},
    {"id": "emergency_003", "english": "Call an ambulance.", "spanish": "Llame a una ambulancia.", "pronunciation": "YAH-meh ah OO-nah am-boo-LAHN-see-ah", "category": "emergency", "alts": ["Ambulance!", "I need an ambulance", "Get an ambulance"]},
    {"id": "emergency_004", "english": "There's been an accident.", "spanish": "Ha habido un accidente.", "pronunciation": "ah ah-BEE-doh oon ak-see-DEN-teh", "category": "emergency", "alts": ["Accident!", "There was an accident", "Car accident"]},
    {"id": "emergency_005", "english": "I lost my passport.", "spanish": "Perdí mi pasaporte.", "pronunciation": "per-DEE mee pah-sah-POR-teh", "category": "emergency", "alts": ["My passport is lost", "Lost passport", "Can't find my passport"]},
    {"id": "emergency_006", "english": "I was robbed.", "spanish": "Me robaron.", "pronunciation": "meh roh-BAH-ron", "category": "emergency", "alts": ["I got robbed", "Someone robbed me", "I've been robbed"]},
    {"id": "emergency_007", "english": "Someone stole my wallet.", "spanish": "Alguien robó mi cartera.", "pronunciation": "AL-gee-en roh-BOH mee kar-TEH-rah", "category": "emergency", "alts": ["My wallet was stolen", "Wallet stolen", "They took my wallet"]},
    {"id": "emergency_008", "english": "Stop! Thief!", "spanish": "¡Alto! ¡Ladrón!", "pronunciation": "AL-toh lah-DRON", "category": "emergency", "alts": ["Stop thief!", "Thief!", "He stole from me"]},
    {"id": "emergency_009", "english": "Fire!", "spanish": "¡Fuego!", "pronunciation": "FWEH-goh", "category": "emergency", "alts": ["There's a fire", "Fire!", "Help, fire!"]},
    {"id": "emergency_010", "english": "I don't feel safe.", "spanish": "No me siento seguro/a.", "pronunciation": "noh meh see-EN-toh seh-GOO-roh", "category": "emergency", "alts": ["I feel unsafe", "This isn't safe", "I'm scared"]},
    {"id": "emergency_011", "english": "Leave me alone.", "spanish": "Déjeme en paz.", "pronunciation": "DEH-heh-meh en pahs", "category": "emergency", "alts": ["Go away", "Leave me", "Stop bothering me"]},
    {"id": "emergency_012", "english": "Stop!", "spanish": "¡Para!", "pronunciation": "PAH-rah", "category": "emergency", "alts": ["Stop it!", "Halt!", "No!"]},
    {"id": "emergency_013", "english": "I need to go to the embassy.", "spanish": "Necesito ir a la embajada.", "pronunciation": "neh-seh-SEE-toh eer ah lah em-bah-HAH-dah", "category": "emergency", "alts": ["Take me to the embassy", "Where is the embassy?", "US embassy"]},
    {"id": "emergency_014", "english": "Please call this number.", "spanish": "Por favor llame a este número.", "pronunciation": "por fah-VOR YAH-meh ah ES-teh NOO-meh-roh", "category": "emergency", "alts": ["Call this number", "Contact this person"]},
    {"id": "emergency_015", "english": "I lost my child.", "spanish": "Perdí a mi hijo/a.", "pronunciation": "per-DEE ah mee EE-hoh", "category": "emergency", "alts": ["My child is missing", "I can't find my child", "Lost child"]},
    {"id": "emergency_016", "english": "I'm being followed.", "spanish": "Me están siguiendo.", "pronunciation": "meh es-TAHN see-gee-EN-doh", "category": "emergency", "alts": ["Someone is following me", "I think I'm being followed"]},
    {"id": "emergency_017", "english": "There's an emergency.", "spanish": "Hay una emergencia.", "pronunciation": "eye OO-nah eh-mer-HEN-see-ah", "category": "emergency", "alts": ["Emergency!", "It's an emergency"]},
    {"id": "emergency_018", "english": "I need to make an emergency call.", "spanish": "Necesito hacer una llamada de emergencia.", "pronunciation": "neh-seh-SEE-toh ah-SER OO-nah yah-MAH-dah deh eh-mer-HEN-see-ah", "category": "emergency", "alts": ["Emergency call", "Can I use your phone for emergency?"]},
    {"id": "emergency_019", "english": "Someone is hurt.", "spanish": "Alguien está herido.", "pronunciation": "AL-gee-en es-TAH eh-REE-doh", "category": "emergency", "alts": ["Person injured", "Someone is injured"]},
    {"id": "emergency_020", "english": "I'm allergic and need medicine immediately.", "spanish": "Soy alérgico y necesito medicina inmediatamente.", "pronunciation": "soy ah-LAIR-hee-koh ee neh-seh-SEE-toh meh-dee-SEE-nah een-meh-dee-ah-tah-MEN-teh", "category": "emergency", "alts": ["Allergic reaction!", "I need my allergy medicine now"]},
    {"id": "emergency_021", "english": "Where is the nearest hospital?", "spanish": "¿Dónde está el hospital más cercano?", "pronunciation": "DOHN-deh es-TAH el os-pee-TAL mahs ser-KAH-noh", "category": "emergency", "alts": ["Nearest hospital?", "Hospital nearby?"]},
    {"id": "emergency_022", "english": "I need the fire department.", "spanish": "Necesito los bomberos.", "pronunciation": "neh-seh-SEE-toh los bom-BEH-rohs", "category": "emergency", "alts": ["Call the fire department", "Fire department!"]},
    {"id": "emergency_023", "english": "My bag was stolen.", "spanish": "Me robaron la bolsa.", "pronunciation": "meh roh-BAH-ron lah BOL-sah", "category": "emergency", "alts": ["Bag stolen", "Someone took my bag"]},
    {"id": "emergency_024", "english": "I'm having a medical emergency.", "spanish": "Tengo una emergencia médica.", "pronunciation": "TEN-goh OO-nah eh-mer-HEN-see-ah MEH-dee-kah", "category": "emergency", "alts": ["Medical emergency!", "I need medical help now"]},
    {"id": "emergency_025", "english": "I'm lost and need help.", "spanish": "Estoy perdido/a y necesito ayuda.", "pronunciation": "es-TOY per-DEE-doh ee neh-seh-SEE-toh ah-YOO-dah", "category": "emergency", "alts": ["I'm lost, help me", "Lost and need directions"]},
    {"id": "emergency_026", "english": "This is not safe.", "spanish": "Esto no es seguro.", "pronunciation": "ES-toh noh es seh-GOO-roh", "category": "emergency", "alts": ["Not safe", "Dangerous"]},
    {"id": "emergency_027", "english": "Get away from me.", "spanish": "Aléjese de mí.", "pronunciation": "ah-LEH-heh-seh deh mee", "category": "emergency", "alts": ["Stay away", "Back off", "Don't come closer"]},
    {"id": "emergency_028", "english": "Call for help.", "spanish": "Pida ayuda.", "pronunciation": "PEE-dah ah-YOO-dah", "category": "emergency", "alts": ["Get help", "Find someone to help"]},
    {"id": "emergency_029", "english": "I witnessed a crime.", "spanish": "Fui testigo de un crimen.", "pronunciation": "fwee tes-TEE-goh deh oon KREE-men", "category": "emergency", "alts": ["I saw a crime", "Report a crime"]},
    {"id": "emergency_030", "english": "Take me to the police station.", "spanish": "Lléveme a la comisaría.", "pronunciation": "YEH-veh-meh ah lah koh-mee-sah-REE-ah", "category": "emergency", "alts": ["Police station please", "I need to go to police"]},

    # SOCIAL (20 phrases)
    {"id": "social_001", "english": "Nice to meet you.", "spanish": "Mucho gusto.", "pronunciation": "MOO-choh GOOS-toh", "category": "social", "alts": ["Pleased to meet you", "It's nice to meet you"]},
    {"id": "social_002", "english": "How are you?", "spanish": "¿Cómo está?", "pronunciation": "KOH-moh es-TAH", "category": "social", "alts": ["How are you doing?", "How's it going?"]},
    {"id": "social_003", "english": "I'm fine, thanks.", "spanish": "Estoy bien, gracias.", "pronunciation": "es-TOY bee-EN GRAH-see-ahs", "category": "social", "alts": ["I'm good thanks", "Fine thank you"]},
    {"id": "social_004", "english": "What is your name?", "spanish": "¿Cómo se llama?", "pronunciation": "KOH-moh seh YAH-mah", "category": "social", "alts": ["Your name?", "What's your name?"]},
    {"id": "social_005", "english": "My name is...", "spanish": "Me llamo...", "pronunciation": "meh YAH-moh", "category": "social", "alts": ["I'm called...", "I am..."]},
    {"id": "social_006", "english": "Where are you from?", "spanish": "¿De dónde es?", "pronunciation": "deh DOHN-deh es", "category": "social", "alts": ["Where do you come from?", "Your country?"]},
    {"id": "social_007", "english": "I am from...", "spanish": "Soy de...", "pronunciation": "soy deh", "category": "social", "alts": ["I come from...", "I'm from..."]},
    {"id": "social_008", "english": "Do you want to have a drink?", "spanish": "¿Quiere tomar algo?", "pronunciation": "kee-EH-reh toh-MAR AL-goh", "category": "social", "alts": ["Want a drink?", "Let's get a drink"]},
    {"id": "social_009", "english": "Cheers!", "spanish": "¡Salud!", "pronunciation": "sah-LOOD", "category": "social", "alts": ["To your health!", "Cheers"]},
    {"id": "social_010", "english": "Have a nice day.", "spanish": "Que tenga un buen día.", "pronunciation": "keh TEN-gah oon bwen DEE-ah", "category": "social", "alts": ["Good day", "Nice day"]},
    {"id": "social_011", "english": "See you later.", "spanish": "Hasta luego.", "pronunciation": "AHS-tah LWEH-goh", "category": "social", "alts": ["Later", "See you"]},
    {"id": "social_012", "english": "See you tomorrow.", "spanish": "Hasta mañana.", "pronunciation": "AHS-tah mahn-YAH-nah", "category": "social", "alts": ["Tomorrow", "See you tomorrow"]},
    {"id": "social_013", "english": "Have a good trip.", "spanish": "Buen viaje.", "pronunciation": "bwen vee-AH-heh", "category": "social", "alts": ["Safe travels", "Good trip"]},
    {"id": "social_014", "english": "Happy birthday!", "spanish": "¡Feliz cumpleaños!", "pronunciation": "feh-LEES koom-pleh-AHN-yohs", "category": "social", "alts": ["Birthday wishes", "Happy bday"]},
    {"id": "social_015", "english": "Congratulations!", "spanish": "¡Felicidades!", "pronunciation": "feh-lee-see-DAH-des", "category": "social", "alts": ["Congrats", "Well done"]},
    {"id": "social_016", "english": "I don't understand.", "spanish": "No entiendo.", "pronunciation": "noh en-tee-EN-doh", "category": "social", "alts": ["I don't get it", "What?"]},
    {"id": "social_017", "english": "Could you speak more slowly?", "spanish": "¿Puede hablar más despacio?", "pronunciation": "PWEH-deh ah-BLAR mahs des-PAH-see-oh", "category": "social", "alts": ["Slower please", "Speak slowly"]},
    {"id": "social_018", "english": "It was nice talking to you.", "spanish": "Fue un placer hablar con usted.", "pronunciation": "fweh oon plah-SER ah-BLAR kon oos-TED", "category": "social", "alts": ["Nice chatting", "Good conversation"]},
    {"id": "social_019", "english": "Can I take a photo?", "spanish": "¿Puedo tomar una foto?", "pronunciation": "PWEH-doh toh-MAR OO-nah FOH-toh", "category": "social", "alts": ["Photo?", "Take a picture?"]},
    {"id": "social_020", "english": "Would you take a photo of us?", "spanish": "¿Nos puede tomar una foto?", "pronunciation": "nohs PWEH-deh toh-MAR OO-nah FOH-toh", "category": "social", "alts": ["Photo of us?", "Take our picture?"]},
]


def generate_tests(phrases):
    """Generate test cases from phrases."""
    tests = []

    for phrase in phrases:
        # Use alternative phrasings as test cases
        for alt in phrase.get("alts", [])[:2]:  # Take up to 2 alts per phrase
            tests.append({
                "query": alt.lower().replace("?", "").replace("!", "").strip(),
                "expected_id": phrase["id"]
            })

    # Add some typo/variation tests
    typo_tests = [
        {"query": "wheres the restroom", "expected_id": "essentials_001"},
        {"query": "bathroom", "expected_id": "essentials_001"},
        {"query": "do you speak english", "expected_id": "essentials_002"},
        {"query": "how can i get to the airport", "expected_id": "directions_001"},
        {"query": "im allergic to peanuts", "expected_id": "dining_001"},
        {"query": "help me please", "expected_id": "emergency_001"},
        {"query": "please call police", "expected_id": "emergency_002"},
        {"query": "where is the hospital", "expected_id": "health_001"},
        {"query": "i need a doctor now", "expected_id": "health_002"},
        {"query": "taxi to downtown", "expected_id": "transportation_001"},
        {"query": "how much is it", "expected_id": "essentials_025"},
        {"query": "thank you so much", "expected_id": "essentials_005"},
        {"query": "sorry i dont understand", "expected_id": "essentials_003"},
        {"query": "whats the wifi password", "expected_id": "hotel_011"},
        {"query": "can i pay with credit card", "expected_id": "money_003"},
    ]

    tests.extend(typo_tests)

    return tests


def main():
    print("Generating phrase and test datasets...")
    print()

    # Ensure data directory exists
    default_config.data_dir.mkdir(parents=True, exist_ok=True)

    # Save phrases
    phrases_path = default_config.phrases_path
    print(f"Generating {len(PHRASES_DATA)} phrases...")
    with open(phrases_path, "w", encoding="utf-8") as f:
        json.dump(PHRASES_DATA, f, indent=2, ensure_ascii=False)
    print(f"Saved to {phrases_path}")

    # Generate and save tests
    tests = generate_tests(PHRASES_DATA)
    tests_path = default_config.tests_path
    print(f"Generating {len(tests)} test cases...")
    with open(tests_path, "w", encoding="utf-8") as f:
        json.dump(tests, f, indent=2, ensure_ascii=False)
    print(f"Saved to {tests_path}")

    # Print statistics
    print()
    print("Dataset Statistics:")
    print("-" * 40)

    categories = {}
    for phrase in PHRASES_DATA:
        cat = phrase["category"]
        categories[cat] = categories.get(cat, 0) + 1

    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count} phrases")

    print("-" * 40)
    print(f"  Total phrases: {len(PHRASES_DATA)}")
    print(f"  Total test cases: {len(tests)}")
    print()
    print("Data generation complete!")


if __name__ == "__main__":
    main()
