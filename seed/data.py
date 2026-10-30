# Structured Agricultural Educational Seed Data
# Sources: ICAR (Indian Council of Agricultural Research), TNAU Agritech Portal, 
# State Agricultural Universities and National Horticulture Board.

LOOKUP_DATA = {
    "soils": [
        {"name": "Alluvial", "description": "Fertile river valley soil rich in potash and humus; excellent water retention."},
        {"name": "Black", "description": "Clay-rich regur soil with high moisture retention; ideal for cotton and pulses."},
        {"name": "Red", "description": "Porous, friable loamy-to-sandy soil with iron oxide; responsive to irrigation and manure."},
        {"name": "Loamy", "description": "Balanced mixture of sand, silt, and clay; high fertility and optimal aeration."},
        {"name": "Clay", "description": "Fine-textured soil with very high water-holding capacity; suitable for wetland paddy."},
        {"name": "Sandy", "description": "Coarse-textured, rapid-draining soil suitable for deep-rooted and tuber/pod crops."}
    ],
    "seasons": [
        {"name": "Kharif", "period": "June to October (Monsoon)", "description": "Sown at the onset of the southwest monsoon and harvested in autumn."},
        {"name": "Rabi", "period": "October to April (Winter)", "description": "Sown after the monsoon retreats and harvested in spring/early summer."},
        {"name": "Zaid", "period": "March to June (Summer)", "description": "Short duration summer crops grown under assured irrigation."},
        {"name": "Year-round", "period": "Perennial / Multi-season", "description": "Crops cultivated or yielding continuously across multiple seasons."}
    ],
    "regions": [
        {"name": "Tamil Nadu (Cauvery Delta)", "state": "Tamil Nadu", "zone": "Delta Agrocimatic Zone"},
        {"name": "Tamil Nadu (Western Zone - Coimbatore/Erode)", "state": "Tamil Nadu", "zone": "Western Agroclimatic Zone"},
        {"name": "Tamil Nadu (Southern Zone - Madurai/Tirunelveli)", "state": "Tamil Nadu", "zone": "Southern Agroclimatic Zone"},
        {"name": "Punjab & Haryana (Indo-Gangetic Plain)", "state": "Punjab", "zone": "Trans-Gangetic Plain"},
        {"name": "Maharashtra (Deccan Plateau)", "state": "Maharashtra", "zone": "Western Plateau & Hills"},
        {"name": "Karnataka (Southern Plateau)", "state": "Karnataka", "zone": "Southern Transition Zone"},
        {"name": "Uttar Pradesh (Central Plain)", "state": "Uttar Pradesh", "zone": "Middle Gangetic Plain"},
        {"name": "Andhra Pradesh (Coastal Zone)", "state": "Andhra Pradesh", "zone": "East Coast Plains & Hills"}
    ]
}

CROPS_DATA = [
    {
        "slug": "rice-paddy",
        "name": "Rice (Paddy)",
        "scientific_name": "Oryza sativa",
        "category": "Cereal",
        "description": "Primary staple food crop feeding over half the world's population. Cultivated predominantly in flooded wetland conditions across diverse agro-climatic zones.",
        "water_requirement": "High",
        "season_summary": "Kharif (main crop), Rabi/Navarai (irrigated winter)",
        "soil_climate_summary": "Heavy clay, clay-loam, and alluvial soils with impervious subsoil layers. Warm, humid climate with prolonged sunshine.",
        "image_path": "/static/img/rice.svg",
        "min_temp": 20.0,
        "max_temp": 38.0,
        "min_rainfall": 1000.0,
        "max_rainfall": 2500.0,
        "climate_source_note": "TNAU Agritech Portal & ICAR Directorate of Rice Research",
        "difficulty_level": "Intermediate",
        "soils": ["Clay", "Alluvial", "Loamy"],
        "seasons": ["Kharif", "Rabi"],
        "regions": ["Tamil Nadu (Cauvery Delta)", "Andhra Pradesh (Coastal Zone)", "Punjab & Haryana (Indo-Gangetic Plain)", "Uttar Pradesh (Central Plain)"],
        "cultivation_guide": {
            "seed_selection": "Choose certified disease-free seeds with high germination rate (above 80%). Treat seeds with Trichoderma viride (4 g/kg) or Pseudomonas fluorescens (10 g/kg) to prevent seed-borne pathogens.",
            "land_preparation": "Plough 2-3 times followed by thorough puddling in standing water (5-10 cm depth) to destroy weeds and create an impervious hard pan that prevents deep water percolation.",
            "sowing_method": "Nursery bed transplanting (wet nursery or mat nursery for mechanical transplanter) at 14-21 days seedling age. Maintain 2-3 seedlings per hill at 20 cm x 10 cm or 15 cm x 10 cm spacing.",
            "irrigation": "Maintain shallow standing water (2-5 cm) from transplanting until panicle initiation. Adopt Alternate Wetting and Drying (AWD) to save 20-30% water without reducing yield. Drain fields 10 days before harvest.",
            "nutrient_management": "Apply well-decomposed FYM or compost (12.5 t/ha) before final puddling. Apply nitrogen in 3 split doses (basal, active tillering, and panicle initiation) adjusted strictly to local soil test recommendations.",
            "weed_management": "Adopt integrated weed management: manual cono-weeder at 15 and 30 days after transplanting in saturated conditions, which aerates roots and incorporates weeds into the soil.",
            "growth_stages": "Seedling (0-20 days) -> Active Tillering (20-45 days) -> Panicle Initiation (45-65 days) -> Flowering/Heading (65-80 days) -> Grain Filling/Milking (80-105 days) -> Maturity (105-135 days).",
            "common_mistakes": "Transplanting over-aged seedlings (>30 days); continuous deep flooding that suffocates roots; applying all nitrogen fertilizer at transplanting causing leaching losses.",
            "source_reference": "TNAU Agritech Portal (Crop Production Guide) & ICAR-NRRI Cuttack",
            "last_reviewed_at": "2026-03-15"
        },
        "pests_diseases": [
            {
                "name": "Yellow Stem Borer (Scirpophaga incertulas)",
                "type": "pest",
                "symptoms": "Larvae bore into stem center causing 'dead heart' during vegetative stage (central leaf sheath dries up) and 'white ear head' during reproductive stage (chaffy, upright empty panicles).",
                "contributing_conditions": "High nitrogen fertilization, humid overcast weather, standing water continuously without drainage.",
                "prevention": "Clip seedling leaf tips before transplanting to eliminate egg masses. Install pheromone traps at 12 traps/ha for monitoring. Conserve natural predators like spiders and dragonflies.",
                "management": "Release egg parasitoid Trichogramma japonicum at 100,000/ha at weekly intervals. Apply neem seed kernel extract (NSKE 5%) during early emergence.",
                "source_reference": "ICAR-Indian Institute of Rice Research (IIRR), Hyderabad",
                "last_reviewed_at": "2026-02-10"
            },
            {
                "name": "Blast Disease (Magnaporthe oryzae)",
                "type": "disease",
                "symptoms": "Spindle-shaped elliptical lesions on leaves with brown margins and grey-white centers. Neck blast causes blackening of node below panicle, causing it to break and hang down.",
                "contributing_conditions": "High relative humidity (>90%), night temperatures around 20-24°C, prolonged dew, excessive nitrogen fertilizer.",
                "prevention": "Treat seeds with Pseudomonas fluorescens. Avoid excessive nitrogenous fertilizers; balance with potassium and silica. Grow resistant locally adapted varieties.",
                "management": "Spray Pseudomonas fluorescens or bio-fungicide formulations at onset of disease. Consult local extension officer for verified field treatment thresholds.",
                "source_reference": "TNAU Department of Plant Pathology",
                "last_reviewed_at": "2026-02-15"
            }
        ],
        "harvest_guide": {
            "maturity_indicators": "Over 80-85% of grains in the panicles turn golden yellow. Moisture content in grain drops to 20-22%. Lower grains are hard and cannot be dented with fingernail.",
            "approximate_harvest_period": "110-140 days after sowing, depending on short, medium, or long duration cultivar.",
            "harvesting_method": "Manual sickle harvesting close to ground level or mechanical combine harvesting during clear sunny weather.",
            "handling_precautions": "Avoid delayed harvesting which causes grain shattering and cracking. Thresh immediately to avoid mold development.",
            "storage_preparation": "Dry threshed paddy under gradual sun drying or mechanical dryer down to 12-14% moisture content before storage. Store in moisture-proof hermetic bags or ventilated metal bins.",
            "source_reference": "ICAR Central Institute of Post-Harvest Engineering & Technology (CIPHET)",
            "last_reviewed_at": "2026-01-20"
        },
        "post_harvest_guide": {
            "cleaning_and_grading": "Clean harvested paddy with air screen cleaners to remove straw, stones, dust, and immature light grains before parboiling or milling.",
            "storage_method": "Store clean dried paddy in dry, rodent-proof granaries on wooden pallets away from walls. Maintain bag moisture under 14% to prevent Aspergillus mold.",
            "preservation_method": "Hermetic storage bags (Purdue Improved Crop Storage - PICS bags) or inert gas aeration for seed and commercial grain.",
            "processing_method": "Dehusking (removing the outer husk) -> Polishing/Whitening (removing bran layer) -> Grading according to broken grain percentage.",
            "packaging_method": "BOPP laminated bags or multi-wall food grade paper bags with moisture barriers.",
            "food_uses": "Table cooked rice, idli/dosa batter, rice noodles, puffed rice (pori), beaten rice (poha).",
            "industrial_uses": "Rice starch for pharmaceutical binding, cosmetic powders, brewing, and bioethanol.",
            "by_products": "Rice husk (biofuel, silica generation, boiler fuel), rice bran (edible oil, defatted bran animal feed), broken rice (starch and poultry feed).",
            "source_reference": "ICAR-CIPHET & Indian Institute of Food Processing Technology (IIFPT) Thanjavur",
            "last_reviewed_at": "2026-03-01"
        },
        "products": [
            {
                "product_name": "Stone-Ground Rice Flour",
                "product_category": "Food Product",
                "raw_material": "Broken and whole polished or unpolished rice grains",
                "processing_overview": "Grain cleaning -> Soaking (for wet milling) or pneumatic dry cleaning -> Grinding in micro-pulverizer or stone mill -> Sifting through 80-mesh sieve -> Moisture adjustment and packing.",
                "common_uses": "Gluten-free baking, snacks (murukku, sev), sweet desserts, noodle formulations, infant complementary foods.",
                "storage_considerations": "Store in sealed airtight bags in a cool dry area. Shelf life: 4-6 months under ambient room temperature.",
                "value_addition_notes": "Upgrades broken grains (which sell at 50% discount) into premium gluten-free culinary flour with 40-70% value addition."
            },
            {
                "product_name": "Flattened Rice (Flakes / Poha / Aval)",
                "product_category": "Food Product",
                "raw_material": "Paddy with moderate amylose content",
                "processing_overview": "Paddy soaking in warm water -> Roasting in sand pan at 200°C for seconds -> Immediate flaking in roller mill -> Winnowing husk -> Cooling and grading.",
                "common_uses": "Breakfast cereals, instant snacks, traditional convalescent foods, ready-to-eat savory mixes.",
                "storage_considerations": "Moisture must be under 12%. Keep in moisture-proof poly pouches away from odors.",
                "value_addition_notes": "Traditional value-addition turning raw paddy into nutritious convenience food with high digestive digestibility and strong local demand."
            },
            {
                "product_name": "Refined Rice Bran Oil",
                "product_category": "By-Product",
                "raw_material": "Freshly separated rice bran from modern rice mills",
                "processing_overview": "Bran stabilization (heating to deactivate lipase enzyme within 24h) -> Solvent extraction -> Degumming -> Dewaxing -> Deodorization.",
                "common_uses": "Heart-healthy cooking oil containing natural antioxidants (Oryzanol), bakery fats, blended cooking oils.",
                "storage_considerations": "Store in dark amber or tin containers away from direct sunlight to preserve antioxidants.",
                "value_addition_notes": "Extracts high-value culinary oil (16-20% oil in bran) from a former waste stream or low-cost feed by-product."
            }
        ],
        "quiz": [
            {
                "question": "What is the recommended grain moisture content before storing paddy safely?",
                "option_a": "22% to 25%",
                "option_b": "12% to 14%",
                "option_c": "5% to 8%",
                "option_d": "Above 30%",
                "correct_option": "B",
                "explanation": "Paddy must be dried down to 12-14% moisture content to prevent mold growth, heating, insect infestation, and seed degradation during storage."
            },
            {
                "question": "What symptom indicates Yellow Stem Borer infestation during the reproductive stage of rice?",
                "option_a": "Silver shoot",
                "option_b": "Dead heart",
                "option_c": "White ear head",
                "option_d": "Leaf bronzing",
                "correct_option": "C",
                "explanation": "Stem borer feeding inside the culm severs vascular bundles, resulting in empty, chaffy white panicles known as 'white ear head'."
            },
            {
                "question": "Why is the Alternate Wetting and Drying (AWD) irrigation method practiced in paddy?",
                "option_a": "It increases pesticide absorption",
                "option_b": "It reduces water consumption by 20-30% without cutting yield",
                "option_c": "It forces plants to flower twice",
                "option_d": "It eliminates the need for any fertilizer",
                "correct_option": "B",
                "explanation": "AWD allows the field to dry down to 15 cm below soil surface before re-flooding, saving substantial water and reducing methane emissions."
            }
        ]
    },
    {
        "slug": "wheat",
        "name": "Wheat",
        "scientific_name": "Triticum aestivum",
        "category": "Cereal",
        "description": "Crucial winter rabi cereal crop that is the cornerstone of food security and bread-making across northern and central plains.",
        "water_requirement": "Medium",
        "season_summary": "Rabi (sown November, harvested March-April)",
        "soil_climate_summary": "Well-drained fertile loamy and clay-loam soils. Cool winter growing season with bright sunny warm days during ripening.",
        "image_path": "/static/img/wheat.svg",
        "min_temp": 10.0,
        "max_temp": 28.0,
        "min_rainfall": 450.0,
        "max_rainfall": 950.0,
        "climate_source_note": "ICAR-Indian Institute of Wheat and Barley Research (IIWBR)",
        "difficulty_level": "Beginner",
        "soils": ["Loamy", "Alluvial", "Clay"],
        "seasons": ["Rabi"],
        "regions": ["Punjab & Haryana (Indo-Gangetic Plain)", "Uttar Pradesh (Central Plain)", "Maharashtra (Deccan Plateau)"],
        "cultivation_guide": {
            "seed_selection": "Use certified seed of rust-resistant varieties recommended for your agro-climatic subzone. Treat seeds with Carboxin or Trichoderma.",
            "land_preparation": "Plough 1 deep ploughing followed by 2-3 harrowing passes and planking to create a fine, weed-free, firm seedbed.",
            "sowing_method": "Sow using a zero-till seed-cum-fertilizer drill at 20-22.5 cm row spacing and 4-5 cm depth. Sowing between Nov 1 to Nov 20 ensures optimum cool-period growth.",
            "irrigation": "4 to 6 irrigations at critical growth stages: Crown Root Initiation (CRI at 20-25 DAS, most critical), Tillering, Late Jointing, Flowering, Milking, and Dough stage.",
            "nutrient_management": "Apply well-rotted farmyard manure (10 t/ha). Split nitrogen applications into basal, first irrigation, and second irrigation stages according to soil test recommendations.",
            "weed_management": "Maintain early canopy closure. Hand weeding at 30-35 DAS or use integrated mechanical rotary hoes before root canopy fills.",
            "growth_stages": "Germination (0-7 days) -> Crown Root Initiation (20-25 days) -> Tillering (30-45 days) -> Jointing (45-60 days) -> Booting/Flowering (65-80 days) -> Grain Filling (80-110 days) -> Ripening (110-135 days).",
            "common_mistakes": "Missing the Crown Root Initiation irrigation; delayed sowing into late December leading to terminal heat stress during grain filling.",
            "source_reference": "ICAR-IIWBR Karnal Advisory Handbook",
            "last_reviewed_at": "2026-02-28"
        },
        "pests_diseases": [
            {
                "name": "Yellow Rust (Puccinia striiformis)",
                "type": "disease",
                "symptoms": "Yellowish-orange pustules arranged in linear stripes on leaves, shedding yellow powder when brushed.",
                "contributing_conditions": "Cool temperatures (10-15°C) coupled with high humidity and morning dew.",
                "prevention": "Grow recommended rust-resistant varieties; avoid excessive nitrogen fertilizer; monitor northern foothills early.",
                "management": "Spray recommended bio-agents or verified triazole fungicides immediately on symptom appearance under extension supervision.",
                "source_reference": "ICAR-IIWBR Karnal Wheat Protection Bulletin",
                "last_reviewed_at": "2026-02-12"
            },
            {
                "name": "Wheat Aphid (Sitobion avenae)",
                "type": "pest",
                "symptoms": "Small green or brownish insects congregating on ears and flag leaves, sucking sap and causing shriveled grains.",
                "contributing_conditions": "Cloudy, calm weather during late February and March during ear-emergence.",
                "prevention": "Conserve ladybird beetles and syrphid fly predators; maintain balanced fertilizer.",
                "management": "Spray 5% neem seed kernel extract or soap solution when aphid counts exceed economic threshold (10-15 aphids/ear head).",
                "source_reference": "Punjab Agricultural University (PAU) Farm Bulletin",
                "last_reviewed_at": "2026-01-18"
            }
        ],
        "harvest_guide": {
            "maturity_indicators": "Straw and spikes turn golden yellow-brown. Leaves dry out completely and grains become hard with moisture below 15%.",
            "approximate_harvest_period": "115-135 days depending on cultivar and sowing date.",
            "harvesting_method": "Reaper binder or combine harvester during morning or mid-day under dry weather.",
            "handling_precautions": "Ensure threshing drum speeds are adjusted to prevent broken wheat grains (which accelerate insect damage).",
            "storage_preparation": "Sun-dry grains to 10-12% moisture. Clean thoroughly and treat bins with neem oil or diatomaceous earth.",
            "source_reference": "ICAR-CIPHET Grain Storage Guidelines",
            "last_reviewed_at": "2026-02-05"
        },
        "post_harvest_guide": {
            "cleaning_and_grading": "Sieve to remove chaff, weed seeds, stones, and foreign matter. Grade by test weight and grain vitreousness.",
            "storage_method": "Store in galvanized iron silos, RCC silos, or hermetic bags with airtight closures to prevent Khapra beetle.",
            "preservation_method": "Hermetic sealing; aerate bins during cool, low-humidity days.",
            "processing_method": "Roller milling (separation into semolina, flour, maida, and bran) or chakki stone milling for whole wheat atta.",
            "packaging_method": "Food-grade HDPE woven bags or consumer multi-layer moisture-proof pouches.",
            "food_uses": "Chapatis/roti, sourdough bread, biscuits, pasta/semolina (from durum wheat), cookies.",
            "industrial_uses": "Wheat gluten extraction for meat analogues, starch for paper coatings and biodegradable films.",
            "by_products": "Wheat bran (high-fiber dietary supplement, ruminant cattle feed), wheat germ (vitamin E cosmetic and health oil).",
            "source_reference": "Central Food Technological Research Institute (CFTRI) Mysore",
            "last_reviewed_at": "2026-03-05"
        },
        "products": [
            {
                "product_name": "Whole Wheat Chakki Atta",
                "product_category": "Food Product",
                "raw_material": "Cleaned sound whole wheat grains",
                "processing_overview": "Aspiration cleaning -> Magnetic separator -> Stone grinding ensuring slow cool milling -> Sifting with bran retention -> Packing.",
                "common_uses": "Daily staple flatbreads (roti, paratha), healthy whole-grain baked goods.",
                "storage_considerations": "Keep in airtight containers in dry conditions; use within 3 months to prevent natural oil rancidity.",
                "value_addition_notes": "Retains all bran and germ fiber, fetching higher health premiums than mass refined flours."
            },
            {
                "product_name": "Toasted Wheat Bran Fiber Mix",
                "product_category": "By-Product",
                "raw_material": "Separated outer wheat pericarp (bran)",
                "processing_overview": "Bran separation -> Steam stabilization to destroy lipase -> Gentle dry toasting -> Sizing -> Vacuum packaging.",
                "common_uses": "Dietary fiber supplement for digestive health, addition to breakfast cereals and artisan breads.",
                "storage_considerations": "Dry conditions in nitrogen-flushed packages to prevent rancidity.",
                "value_addition_notes": "Converts animal feed by-product into a premium dietary fiber wellness item."
            }
        ],
        "quiz": [
            {
                "question": "Which growth stage in wheat is considered the most critical for the first irrigation?",
                "option_a": "Milking stage",
                "option_b": "Crown Root Initiation (CRI)",
                "option_c": "Hard dough stage",
                "option_d": "Harvest ripening",
                "correct_option": "B",
                "explanation": "Crown Root Initiation (CRI) occurring 20-25 days after sowing is critical; water deficit at this stage severely reduces tiller formation."
            },
            {
                "question": "What is the primary indicator of Yellow Rust infection in wheat?",
                "option_a": "Stripes of bright yellow pustules on leaves",
                "option_b": "Black sticky exudate on the stem",
                "option_c": "White powdery mildew on roots",
                "option_d": "Holes drilled in the ear head",
                "correct_option": "A",
                "explanation": "Yellow rust produces distinctive bright yellow-orange pustules aligned in parallel linear stripes along leaf veins."
            },
            {
                "question": "To what moisture level should wheat grains be dried before long-term bin storage?",
                "option_a": "20%",
                "option_b": "10% to 12%",
                "option_c": "2% to 4%",
                "option_d": "Above 25%",
                "correct_option": "B",
                "explanation": "Grain moisture must be at or below 10-12% to prevent heating, storage fungal growth, and insect attack."
            }
        ]
    },
    {
        "slug": "maize-corn",
        "name": "Maize (Corn)",
        "scientific_name": "Zea mays",
        "category": "Cereal",
        "description": "The 'Queen of Cereals', versatile C4 plant having the highest genetic yield potential among food grain crops, used for food, animal feed, and industrial starch.",
        "water_requirement": "Medium",
        "season_summary": "Kharif (rainfed), Rabi (irrigated high yielding), Zaid (spring)",
        "soil_climate_summary": "Deep, fertile, well-drained loamy soils rich in organic matter. Warm temperate to tropical climate.",
        "image_path": "/static/img/maize.svg",
        "min_temp": 18.0,
        "max_temp": 35.0,
        "min_rainfall": 500.0,
        "max_rainfall": 1000.0,
        "climate_source_note": "ICAR-Indian Institute of Maize Research (IIMR) Ludhiana",
        "difficulty_level": "Beginner",
        "soils": ["Loamy", "Alluvial", "Red"],
        "seasons": ["Kharif", "Rabi", "Zaid"],
        "regions": ["Tamil Nadu (Western Zone - Coimbatore/Erode)", "Karnataka (Southern Plateau)", "Maharashtra (Deccan Plateau)", "Punjab & Haryana (Indo-Gangetic Plain)"],
        "cultivation_guide": {
            "seed_selection": "Select certified high-yielding single-cross hybrids. Treat seed with cyantraniliprole + thiamethoxam or bio-inoculants for early fall armyworm protection.",
            "land_preparation": "Plough 2-3 times to achieve friable tilth. Form ridges and furrows at 60 cm spacing to prevent waterlogging, as maize cannot tolerate standing water.",
            "sowing_method": "Dibble one seed per hill on the side of the ridge at 60 cm x 20 cm spacing, 3-4 cm deep.",
            "irrigation": "Irrigate immediately after sowing, life irrigation on day 3, then once every 10-12 days. Critical stages: knee-high, tasseling/silking, and grain milking.",
            "nutrient_management": "Apply 12.5 t/ha FYM. Nitrogen is applied in 3 splits (basal, knee-high stage at 30 DAS, and tasseling stage at 45 DAS). Zinc deficiency is common; apply zinc sulphate based on soil test.",
            "weed_management": "Hand hoeing and earthing-up at 30 days after sowing. Earthing up strengthens root lodging resistance.",
            "growth_stages": "Emergence (0-5 days) -> Knee-high (20-30 days) -> Tasseling (45-55 days) -> Silking (50-60 days) -> Milk stage (65-75 days) -> Dough stage (75-90 days) -> Black layer maturity (95-115 days).",
            "common_mistakes": "Waterlogging in early seedling stage; delayed control of Fall Armyworm; planting on flat ground in heavy rainfall areas.",
            "source_reference": "TNAU Crop Production Manual & ICAR-IIMR",
            "last_reviewed_at": "2026-03-10"
        },
        "pests_diseases": [
            {
                "name": "Fall Armyworm (Spodoptera frugiperda)",
                "type": "pest",
                "symptoms": "Ragged whorl feeding holes, sawdust-like fecal matter in the central leaf whorl, defoliation and feeding on developing cobs.",
                "contributing_conditions": "Continuous monocropping, warm dry spells followed by rain.",
                "prevention": "Intercrop with pulses (cowpea or pigeonpea); install pheromone traps (12/ha); apply neem cake in soil.",
                "management": "Whorl application of sand + lime mix (9:1) or Bacillus thuringiensis (Bt) spray; spray NPV (nucleopolyhedrovirus) formulations.",
                "source_reference": "ICAR-National Bureau of Agricultural Insect Resources (NBAIR)",
                "last_reviewed_at": "2026-02-20"
            },
            {
                "name": "Maydis Leaf Blight (Bipolaris maydis)",
                "type": "disease",
                "symptoms": "Elongated rectangular grayish-tan lesions between leaf veins, causing premature leaf drying.",
                "contributing_conditions": "High temperatures (25-30°C) with high relative humidity and frequent showers.",
                "prevention": "Use resistant single cross hybrids; rotate with non-host crops like pulses; balance potassium nutrition.",
                "management": "Foliar spray with Trichoderma viride or copper-based bioformulations at disease onset.",
                "source_reference": "ICAR-IIMR Disease Advisory",
                "last_reviewed_at": "2026-01-25"
            }
        ],
        "harvest_guide": {
            "maturity_indicators": "Cob husks turn dry and papery white; kernels are hard and shiny; dark black layer forms at the base of the kernel where it attaches to the cob.",
            "approximate_harvest_period": "95-115 days depending on hybrid and season.",
            "harvesting_method": "Manual plucking of cobs from standing stalks or mechanical corn combine harvesters.",
            "handling_precautions": "Dry cobs in sun immediately; never heap wet cobs under plastic covers to avoid aflatoxin mold contamination.",
            "storage_preparation": "Shell cobs at 13-14% grain moisture. Clean and store in hermetic bins with moisture below 12%.",
            "source_reference": "ICAR-CIPHET & TNAU Post-Harvest Centre",
            "last_reviewed_at": "2026-02-14"
        },
        "post_harvest_guide": {
            "cleaning_and_grading": "De-husk, shell with rotary maize sheller, screen out cob dust and broken chips.",
            "storage_method": "Hermetic silos or palletized gunny bags with moisture monitored under 12%.",
            "preservation_method": "Aeration with cool ambient air; phosphine fumigation under certified warehouse protocol.",
            "processing_method": "Dry milling (corn grits, corn flour, hominy feed) or wet milling (pure corn starch, corn gluten, corn oil).",
            "packaging_method": "Multi-ply paper bags or polypropylene woven bags with polyethylene lining.",
            "food_uses": "Cornflakes, corn tortilla, polenta, sweet corn roasted cobs, popcorn.",
            "industrial_uses": "Native and modified starches for textiles, bio-plastics, adhesives, high-fructose corn syrup.",
            "by_products": "Maize stover/stalks (valuable cattle fodder and silage), corn cobs (furfural synthesis, mushroom substrate), corn germ oil.",
            "source_reference": "IIFPT Thanjavur & CFTRI Mysore",
            "last_reviewed_at": "2026-03-02"
        },
        "products": [
            {
                "product_name": "Premium Corn Starch",
                "product_category": "Industrial Product",
                "raw_material": "Cleaned sound yellow or white maize grain",
                "processing_overview": "Grain steeping in warm water -> Germ separation -> Fine grinding -> Fiber screening -> Centrifugal starch-protein separation -> Flash drying.",
                "common_uses": "Food thickener, confectionery dusting, textile sizing, paper manufacturing, pharmaceutical tablet disintegrant.",
                "storage_considerations": "Keep strictly dry in sealed bags away from moisture; store off ground on wooden pallets.",
                "value_addition_notes": "Converts raw grain into a high-demand commodity servicing food, packaging, and pharmaceutical sectors."
            },
            {
                "product_name": "Coarse Corn Grits & Cornmeal",
                "product_category": "Food Product",
                "raw_material": "Flint corn or semi-dent maize",
                "processing_overview": "Cleaning -> Tempering with water -> Degerming to remove fat-rich germ -> Roller crushing -> Air classifier grading -> Packaging.",
                "common_uses": "Extruded breakfast cereals, crispy snack pellets, brewery adjunct, traditional polenta dishes.",
                "storage_considerations": "Store in cool dry conditions; degermed grits have low oil and resist rancidity for 6-9 months.",
                "value_addition_notes": "Key raw material for booming ready-to-eat extruded snack industries."
            }
        ],
        "quiz": [
            {
                "question": "What is the unmistakable indicator that a maize kernel has reached physiological maturity?",
                "option_a": "Leaves become dark purple",
                "option_b": "A black layer forms at the kernel base attachment point",
                "option_c": "The cob starts weeping milky sap",
                "option_d": "The root system dies off completely",
                "correct_option": "B",
                "explanation": "A black layer (placental tissue death) forms at the kernel base, indicating nutrient translocation into the grain has ceased."
            },
            {
                "question": "Which invasive pest causes characteristic windowpane feeding and sawdust-like frass in maize whorls?",
                "option_a": "Whitefly",
                "option_b": "Fall Armyworm (Spodoptera frugiperda)",
                "option_c": "Aphids",
                "option_d": "Termites",
                "correct_option": "B",
                "explanation": "Fall armyworm larvae feed heavily in leaf whorls, depositing extensive coarse frass resembling sawdust."
            },
            {
                "question": "Why is maize typically planted on ridges and furrows rather than flat soil?",
                "option_a": "To allow roots to grow above ground",
                "option_b": "Because maize is highly sensitive to waterlogging",
                "option_c": "To prevent exposure to sunlight",
                "option_d": "To harvest grains without bending",
                "correct_option": "B",
                "explanation": "Maize roots suffer rapid asphyxiation and yield collapse under waterlogged conditions; ridges ensure aeration and rapid drainage."
            }
        ]
    },
    {
        "slug": "tomato",
        "name": "Tomato",
        "scientific_name": "Solanum lycopersicum",
        "category": "Vegetable",
        "description": "High-value commercial solanaceous vegetable with extensive culinary, fresh market, and processing applications worldwide.",
        "water_requirement": "Medium",
        "season_summary": "Kharif, Rabi, and Summer (in frost-free irrigated zones)",
        "soil_climate_summary": "Well-drained rich sandy loam or loamy soils with pH 6.0-7.0. Warm, frost-free climate with moderate humidity.",
        "image_path": "/static/img/tomato.svg",
        "min_temp": 16.0,
        "max_temp": 32.0,
        "min_rainfall": 400.0,
        "max_rainfall": 800.0,
        "climate_source_note": "ICAR-Indian Institute of Vegetable Research (IIVR) Varanasi",
        "difficulty_level": "Intermediate",
        "soils": ["Loamy", "Red", "Alluvial", "Sandy"],
        "seasons": ["Kharif", "Rabi", "Zaid"],
        "regions": ["Tamil Nadu (Western Zone - Coimbatore/Erode)", "Karnataka (Southern Plateau)", "Maharashtra (Deccan Plateau)", "Andhra Pradesh (Coastal Zone)"],
        "cultivation_guide": {
            "seed_selection": "Choose determinate or indeterminate F1 hybrids with resistance to Tomato Leaf Curl Virus (ToLCV) and Bacterial Wilt. Treat with Trichoderma.",
            "land_preparation": "Plough to fine tilth, incorporate 25 t/ha well-rotted FYM. Form raised beds (1 m width) with drip lateral lines and silver-black polyethylene mulch.",
            "sowing_method": "Raise seedlings in pro-trays (98 cells) with sterilized cocopeat. Transplant sturdy 25-30 day-old seedlings at 60 cm x 45 cm or 90 cm x 60 cm spacing.",
            "irrigation": "Adopt drip irrigation to supply uniform moisture and prevent foliar wetting which causes fungal blight. Irrigate every 1-2 days based on evapotranspiration.",
            "nutrient_management": "Apply 50% phosphorus and potassium as basal. Apply remaining nitrogen and potassium via weekly fertigation through drip irrigation, adjusted to fruit set stage.",
            "weed_management": "Silver-black plastic mulch suppresses virtually all weeds while conserving soil moisture and repelling aphid/thrip vectors.",
            "growth_stages": "Nursery (0-25 days) -> Vegetative (25-45 days) -> Flowering/Fruit Set (45-65 days) -> Fruit Development (65-90 days) -> Harvesting flush (90-140 days).",
            "common_mistakes": "Overhead sprinkler irrigation causing severe early/late blight; irregular watering leading to Blossom End Rot and fruit cracking.",
            "source_reference": "TNAU Agritech Portal & ICAR-IIVR Varanasi",
            "last_reviewed_at": "2026-03-01"
        },
        "pests_diseases": [
            {
                "name": "Fruit Borer (Helicoverpa armigera)",
                "type": "pest",
                "symptoms": "Larvae bore circular holes into developing green and red fruits, feeding with part of body inside and contaminating fruit with frass.",
                "contributing_conditions": "Warm days followed by mild nights, proximity to alternate hosts (cotton, chickpea).",
                "prevention": "Plant African Marigold as a trap crop (1 row of marigold for every 16 rows of tomato). Install pheromone traps at 12/ha.",
                "management": "Spray Helicoverpa NPV (HaNPV) at 250 LE/ha or Bacillus thuringiensis (Bt) at 2 g/L. Pick and destroy bored fruits.",
                "source_reference": "ICAR-NBAIR Pest Management Series",
                "last_reviewed_at": "2026-02-18"
            },
            {
                "name": "Early Blight (Alternaria solani)",
                "type": "disease",
                "symptoms": "Concentric rings ('target board' appearance) on lower leaves, progressing upwards; leaves turn yellow and drop.",
                "contributing_conditions": "Frequent rains, heavy morning dew, warm temperatures (24-30°C), wet foliage.",
                "prevention": "Use drip irrigation; avoid splash watering; remove lower senescent leaves (pruning); apply Trichoderma soil treatment.",
                "management": "Foliar spray of copper oxychloride (2.5 g/L) or neem-based formulations at the first sight of circular leaf spots.",
                "source_reference": "TNAU Plant Pathology Department",
                "last_reviewed_at": "2026-01-30"
            }
        ],
        "harvest_guide": {
            "maturity_indicators": "Color break stage (pinkish blush at blossom end) for long-distance transport; firm full red-ripe stage for local retail and processing.",
            "approximate_harvest_period": "First harvest at 65-75 days after transplanting; continue multiple pickings over 6-8 weeks.",
            "harvesting_method": "Hand pick with gentle twist retaining the calyx in early morning or late afternoon.",
            "handling_precautions": "Handle in rigid plastic crates (not deep gunny bags) stacked no more than 3-4 layers high to prevent crushing.",
            "storage_preparation": "Store at 12-15°C with 85-90% relative humidity. Never store under 10°C as chilling injury prevents normal ripening.",
            "source_reference": "National Horticulture Board (NHB) Post-Harvest Guidelines",
            "last_reviewed_at": "2026-02-22"
        },
        "post_harvest_guide": {
            "cleaning_and_grading": "Wash in chlorinated water (50-100 ppm chlorine) to remove field dirt and fungal spores. Grade by size, color uniformity, and skin firmness.",
            "storage_method": "Cold storage at 12-13°C for breaker stage (extends shelf life up to 3 weeks); evaporative zero-energy cool chambers (ZECC) for small farms.",
            "preservation_method": "Thermal canning, pasteurized aseptic puree bags, dehydration, brine/oil pickling.",
            "processing_method": "Hot-break or cold-break pulping -> Seed and skin separation through finisher sieves -> Vacuum concentration.",
            "packaging_method": "Corrugated fiberboard (CFB) cartons with aeration holes for fresh market; glass bottles and retort pouches for puree/sauce.",
            "food_uses": "Fresh salads, curries, soups, tomato puree, ketchup, sun-dried snacks, tomato pickles.",
            "industrial_uses": "Lycopene extraction for nutraceutical capsules, tomato seed oil for cosmetic anti-aging formulations.",
            "by_products": "Tomato pomace (skins and seeds) processed into high-protein ruminant feed and dietary lycopene powder.",
            "source_reference": "IIFPT Thanjavur & CFTRI",
            "last_reviewed_at": "2026-03-08"
        },
        "products": [
            {
                "product_name": "Aseptic Tomato Puree & Paste",
                "product_category": "Food Product",
                "raw_material": "Uniformly ripe red processing tomatoes",
                "processing_overview": "Sorting and washing -> Hot break heating (90°C to preserve pectin) -> Pulping and refining through 0.8 mm sieve -> Vacuum evaporation to 24-28° Brix -> Flash pasteurization -> Aseptic bag filling.",
                "common_uses": "Base for culinary curries, pizza/pasta sauces, ready-to-eat gravies, soups.",
                "storage_considerations": "Aseptic sealed packs store 12-18 months at room temperature; refrigerate after opening.",
                "value_addition_notes": "Prevents catastrophic market gluts when fresh prices crash below production cost."
            },
            {
                "product_name": "Spiced Traditional Tomato Pickle",
                "product_category": "Food Product",
                "raw_material": "Semi-ripe and ripe firm tomatoes, sesame oil, mustard, fenugreek, chili powder",
                "processing_overview": "Washing and drying -> Slicing -> Salting and sun/solar drying to reduce moisture -> Cooking with spiced gingelly oil -> Jarring.",
                "common_uses": "Shelf-stable savory condiment paired with rice, flatbreads, and snacks.",
                "storage_considerations": "Keep oil layer over surface; shelf life 9-12 months in airtight glass or PET jars.",
                "value_addition_notes": "Low-capital cottage industry with 100%+ value addition using simple kitchen or micro-enterprise equipment."
            },
            {
                "product_name": "Sun-Dried / Solar Dehydrated Tomatoes",
                "product_category": "Food Product",
                "raw_material": "Plum/Roma type tomatoes with high soluble solids",
                "processing_overview": "Halving -> Removal of excess seeds -> Light sulfur/salt pretreating -> Solar dehydrator drying at 55-60°C to 14% moisture -> Olive/sunflower oil herbal immersion or dry vacuum packing.",
                "common_uses": "Gourmet pasta dishes, bakery toppings, specialty pestos, healthy snacks.",
                "storage_considerations": "Dry packs in vacuum pouches; oil jars kept away from sunlight.",
                "value_addition_notes": "High export and specialty gourmet demand commanding premium prices."
            }
        ],
        "quiz": [
            {
                "question": "Which companion flower crop is widely planted as a trap crop to divert fruit borer from tomato?",
                "option_a": "African Marigold",
                "option_b": "Rose",
                "option_c": "Jasmine",
                "option_d": "Sunflower",
                "correct_option": "A",
                "explanation": "African marigold attracts Helicoverpa moths for oviposition, allowing targeted monitoring and protecting the primary tomato crop."
            },
            {
                "question": "Why should fresh harvested tomatoes never be stored below 10°C in standard refrigeration?",
                "option_a": "They will burst instantly",
                "option_b": "They suffer chilling injury leading to loss of flavor, pitting, and failure to ripen",
                "option_c": "The seeds will begin germinating inside the fruit",
                "option_d": "The skin turns completely black within an hour",
                "correct_option": "B",
                "explanation": "Tomatoes are tropical fruits sensitive to chilling below 10-12°C, which halts enzymatic ripening and damages cell membranes."
            },
            {
                "question": "What is the primary visual symptom of Blossom End Rot in tomato?",
                "option_a": "White mildew on stems",
                "option_b": "Water-soaked dark sunken patch at the bottom (blossom end) of fruit",
                "option_c": "Yellow stripes on leaves only",
                "option_d": "Root nodules developing",
                "correct_option": "B",
                "explanation": "Blossom End Rot is a physiological disorder caused by calcium deficiency and irregular watering, creating a sunken dark leathery rot at the fruit tip."
            }
        ]
    },
    {
        "slug": "cotton",
        "name": "Cotton",
        "scientific_name": "Gossypium hirsutum",
        "category": "Cash Crop",
        "description": "'White Gold', the pre-eminent natural textile fiber crop providing livelihood to millions across agriculture and textile processing sectors.",
        "water_requirement": "Medium",
        "season_summary": "Kharif (main commercial season)",
        "soil_climate_summary": "Deep black cotton soils (regur) with high clay content and water retention, or deep fertile alluvial soils. Warm, semi-arid climate with abundant sunshine.",
        "image_path": "/static/img/cotton.svg",
        "min_temp": 20.0,
        "max_temp": 38.0,
        "min_rainfall": 500.0,
        "max_rainfall": 1000.0,
        "climate_source_note": "ICAR-Central Institute for Cotton Research (CICR) Nagpur",
        "difficulty_level": "Intermediate",
        "soils": ["Black", "Alluvial", "Red"],
        "seasons": ["Kharif"],
        "regions": ["Tamil Nadu (Western Zone - Coimbatore/Erode)", "Maharashtra (Deccan Plateau)", "Punjab & Haryana (Indo-Gangetic Plain)", "Andhra Pradesh (Coastal Zone)"],
        "cultivation_guide": {
            "seed_selection": "Use certified hybrid seed with delinting and fungicide/insecticide seed treatment. Choose varieties suitable for local staple length requirements.",
            "land_preparation": "Deep summer ploughing followed by 2 harrowing rounds to break clods. Form ridges and furrows at 90 cm to 120 cm spacing.",
            "sowing_method": "Dibble 1-2 seeds per hill at 90 cm x 45 cm or 120 cm x 60 cm spacing depending on hybrid canopy architecture.",
            "irrigation": "Avoid waterlogging. Critical stages: square formation, flowering, and boll development. Cease irrigation when bolls begin opening.",
            "nutrient_management": "Apply 10 t/ha farmyard manure. Split nitrogen into 3 doses (basal, square formation, and peak boll development). Foliar spray of magnesium sulphate (1%) prevents leaf reddening.",
            "weed_management": "Maintain weed-free field for the first 60 days using inter-cultivation with bullock or power weeder between rows, followed by hand weeding.",
            "growth_stages": "Germination (0-7 days) -> Square formation (35-50 days) -> Flowering (55-70 days) -> Boll development (70-110 days) -> Boll bursting & harvest (110-160 days).",
            "common_mistakes": "Excessive early nitrogen leading to vegetative leafy growth at the expense of fruiting bolls; spraying broad-spectrum chemicals killing natural predators of bollworms.",
            "source_reference": "ICAR-CICR Nagpur & TNAU Agritech Portal",
            "last_reviewed_at": "2026-02-15"
        },
        "pests_diseases": [
            {
                "name": "Pink Bollworm (Pectinophora gossypiella)",
                "type": "pest",
                "symptoms": "Rosetted flowers that fail to open properly; larvae bore into young bolls, damaging lint and feeding on immature seeds, staining lint brownish.",
                "contributing_conditions": "Late season extensions, ratooning, lack of crop residue destruction after harvest.",
                "prevention": "Strictly observe closed season (do not extend crop past 150 days); install pheromone traps at 12/ha; destroy cotton stalks immediately.",
                "management": "Mass trapping with gossyplure pheromone traps; release Trichogrammatoidea bactrae parasitoid; apply neem oil formulation.",
                "source_reference": "ICAR-CICR Nagpur Advisory",
                "last_reviewed_at": "2026-01-28"
            },
            {
                "name": "Bacterial Blight (Xanthomonas citri pv. malvacearum)",
                "type": "disease",
                "symptoms": "Water-soaked angular leaf spots bordered by leaf veins, progressing to 'black arm' on stems and boll rot.",
                "contributing_conditions": "Warm humid weather with intermittent driving rains and high wind.",
                "prevention": "Acid delinting of seed; treat seeds with Pseudomonas; avoid excessive irrigation.",
                "management": "Spray copper oxychloride (2.5 g/L) with bio-bactericide under agricultural extension guidance.",
                "source_reference": "TNAU Department of Plant Pathology",
                "last_reviewed_at": "2026-02-02"
            }
        ],
        "harvest_guide": {
            "maturity_indicators": "Bolls burst open completely, exposing dry, fluffy, clean white lint.",
            "approximate_harvest_period": "120-160 days in 3-4 picking flushes spaced 15 days apart.",
            "harvesting_method": "Hand pick clean seed cotton (kapas) in bright dry morning sun after dew evaporates.",
            "handling_precautions": "Keep trash, dried bracts, and stained bolls separate from clean white grade. Never use polyproylene bags that leave synthetic fiber contaminants.",
            "storage_preparation": "Sun dry kapas to reduce moisture below 8-9% before storage or ginning.",
            "source_reference": "ICAR-CIRCOT Mumbai (Central Institute for Research on Cotton Technology)",
            "last_reviewed_at": "2026-01-15"
        },
        "post_harvest_guide": {
            "cleaning_and_grading": "Pre-cleaning to remove leaf fragments, sticks, and dirt before feeding into the gin.",
            "storage_method": "Store in clean, dry covered warehouses on raised platforms away from fire hazards and moisture.",
            "preservation_method": "Keep moisture under 8.5% to prevent discoloration and bacterial degradation of lint.",
            "processing_method": "Saw ginning or roller ginning (separates lint from fuzzy seed) -> Lint baling into 170 kg standard bales -> Seed delinting.",
            "packaging_method": "Cotton cloth-wrapped pressed bales strapped with steel or high-tensile wire.",
            "food_uses": "Refined cottonseed edible oil (after complete gossypol removal), vanaspati manufacturing.",
            "industrial_uses": "Yarn spinning, woven/knitted textiles, medical absorbent cotton, cellulose nitrocellulose.",
            "by_products": "Cottonseed cake (protein-rich cattle feed), cotton linters (high-grade paper, cellulose acetate), cotton stalks for particle board.",
            "source_reference": "ICAR-CIRCOT Mumbai",
            "last_reviewed_at": "2026-03-01"
        },
        "products": [
            {
                "product_name": "Refined Cottonseed Cooking Oil",
                "product_category": "By-Product",
                "raw_material": "Cotton seeds separated during ginning",
                "processing_overview": "Seed cleaning -> Delinting -> Dehulling -> Expeller pressing -> Solvent extraction of cake -> Alkali refining to remove toxic gossypol -> Bleaching -> Deodorizing.",
                "common_uses": "Commercial deep frying (high smoke point), blended edible oils, snacks manufacturing.",
                "storage_considerations": "Store in opaque tin or food-grade HDPE drums away from heat.",
                "value_addition_notes": "Extracts high-value clear frying oil from byproduct seeds containing 18-24% oil."
            },
            {
                "product_name": "High-Protein Cottonseed Oil Cake",
                "product_category": "By-Product",
                "raw_material": "Deoiled or expeller pressed cottonseed meal",
                "processing_overview": "Hydraulic or expeller pressing of seed meats -> Heat conditioning -> Slicing into cakes -> Cooling -> Packing.",
                "common_uses": "High-protein supplement feed for milch cattle, boosting milk fat percentage.",
                "storage_considerations": "Keep in dry ventilated godowns off floor to prevent Aspergillus mold.",
                "value_addition_notes": "Essential feed ingredient yielding high local demand across dairy farming belts."
            }
        ],
        "quiz": [
            {
                "question": "What is the key danger of packing raw seed cotton (kapas) in synthetic polypropylene bags?",
                "option_a": "The bags will melt under sunlight",
                "option_b": "Polypropylene fibers shed and contaminate cotton lint, severely degrading yarn quality in textile mills",
                "option_c": "It causes the seeds to ferment into alcohol",
                "option_d": "It attracts mice and birds",
                "correct_option": "B",
                "explanation": "Plastic twine and PP bag fibers contaminate raw cotton; they cannot be removed during spinning and do not take cotton dyes, causing massive defects in woven fabric."
            },
            {
                "question": "Which pest causes 'rosetted flower' symptoms in cotton fields?",
                "option_a": "Pink Bollworm",
                "option_b": "Aphid",
                "option_c": "Red cotton bug",
                "option_d": "Grasshopper",
                "correct_option": "A",
                "explanation": "Pink bollworm larvae web flower petals together so they cannot open normally, forming a distinctive rosetted blossom."
            },
            {
                "question": "What is the recommended seed cotton moisture level before baling or ginning?",
                "option_a": "Above 20%",
                "option_b": "Below 8% to 9%",
                "option_c": "15% to 18%",
                "option_d": "0%",
                "correct_option": "B",
                "explanation": "Cotton moisture must be below 8.5-9% to prevent fiber heating, discoloration, and mold inside compressed bales."
            }
        ]
    },
    {
        "slug": "banana",
        "name": "Banana",
        "scientific_name": "Musa acuminata / Musa balbisiana",
        "category": "Fruit",
        "description": "One of the most important tropical fruit crops and high-yield perennials, yielding nutritious fresh fruit, culinary raw bananas, and industrial fiber.",
        "water_requirement": "High",
        "season_summary": "Year-round (planted in spring or monsoon depending on zone)",
        "soil_climate_summary": "Deep, rich, well-drained loamy soil with high organic matter and good drainage. Warm humid tropical climate with frost-free conditions.",
        "image_path": "/static/img/banana.svg",
        "min_temp": 18.0,
        "max_temp": 38.0,
        "min_rainfall": 1200.0,
        "max_rainfall": 2200.0,
        "climate_source_note": "ICAR-National Research Centre for Banana (NRCB) Tiruchirappalli",
        "difficulty_level": "Intermediate",
        "soils": ["Alluvial", "Clay", "Loamy"],
        "seasons": ["Year-round", "Kharif"],
        "regions": ["Tamil Nadu (Cauvery Delta)", "Tamil Nadu (Southern Zone - Madurai/Tirunelveli)", "Maharashtra (Deccan Plateau)", "Andhra Pradesh (Coastal Zone)"],
        "cultivation_guide": {
            "seed_selection": "Use virus-indexed tissue-cultured plants or disease-free sword suckers (weighing 1.5 to 2.0 kg) free from rhizome weevils and nematodes.",
            "land_preparation": "Plough deeply 3-4 times. Dig pits of 45 cm x 45 cm x 45 cm size. Fill with topsoil mixed with 10 kg FYM and 250 g neem cake per pit.",
            "sowing_method": "Plant tissue culture plantlets or suckers upright in pit centers at 1.8 m x 1.8 m spacing (Grand Naine) or 2.1 m x 2.1 m (Poovan, Nendran).",
            "irrigation": "Drip irrigation with 15-20 liters/plant/day during vegetative stage, rising to 25-30 liters during bunch development. Banana has high water consumption and shallow roots.",
            "nutrient_management": "Apply balanced N-P-K fertigation weekly through drip. Apply micronutrient foliar spray (Banana Special developed by NRCB) at 5th and 7th month.",
            "weed_management": "Clean weeding in early months. Intercrop with short duration green gram or sunnhemp. Mulching with dried leaves or paddy straw suppresses weeds.",
            "growth_stages": "Establishment (0-3 months) -> Rapid vegetative & shooting (3-7 months) -> Inflorescence / Bunch emergence (7-9 months) -> Bunch development & filling (9-12 months).",
            "common_mistakes": "Allowing multiple water suckers to compete with mother plant; planting uncertified suckers infected with Panama wilt or Bunchy Top Virus; poor drainage causing root rot.",
            "source_reference": "ICAR-NRCB Tiruchirappalli Guidelines & TNAU Horticulture Portal",
            "last_reviewed_at": "2026-03-05"
        },
        "pests_diseases": [
            {
                "name": "Sigatoka Leaf Spot (Pseudocercospora musae)",
                "type": "disease",
                "symptoms": "Yellowish streaks on leaves expanding into elliptical dark brown lesions with grey center, causing rapid premature leaf death and un-filled bunches.",
                "contributing_conditions": "High humidity, prolonged leaf wetness from rain or overhead fog, warm tropical temperatures (23-28°C).",
                "prevention": "Maintain proper drainage and plant spacing; prune severely affected leaves and burn them outside plantation.",
                "management": "Foliar spray of mineral oil (1%) or bio-fungicide like Bacillus subtilis; consult local extension officer for seasonal spray schedules.",
                "source_reference": "ICAR-NRCB Disease Advisory",
                "last_reviewed_at": "2026-02-14"
            },
            {
                "name": "Banana Pseudostem Borer (Odoiporus longicollis)",
                "type": "pest",
                "symptoms": "Small pinholes on pseudostem with transparent jelly exudate; yellowing and withering of leaves; pseudostem snaps during high winds.",
                "contributing_conditions": "Poor orchard sanitation, old uncleared plantations, high density.",
                "prevention": "Prune dried leaves; field sanitation; install longitudinal split pseudostem traps (20-25 traps/ha) to collect and destroy adult weevils.",
                "management": "Swab pseudostem with neem oil (3%) or Beauveria bassiana entomopathogenic fungus slurry.",
                "source_reference": "TNAU Agritech Portal Horticulture",
                "last_reviewed_at": "2026-01-20"
            }
        ],
        "harvest_guide": {
            "maturity_indicators": "Fingers become rounded (losing sharp ridges/angles); floral remnants at tip drop off readily; top leaves dry out.",
            "approximate_harvest_period": "11-13 months after planting; 90-110 days after bunch emergence.",
            "harvesting_method": "Cut pseudostem half-way to lower the bunch gently without dropping; harvest bunch with 30-40 cm peduncle handle.",
            "handling_precautions": "Avoid dragging or dropping bunches on ground; carry in padded trays to prevent friction bruising.",
            "storage_preparation": "Wash bunches in clean water to remove latex exudate; store at 13-14°C with 90% RH. Never store below 12°C.",
            "source_reference": "NHB Post Harvest Technology Banana",
            "last_reviewed_at": "2026-02-18"
        },
        "post_harvest_guide": {
            "cleaning_and_grading": "De-handing bunches into hands and clusters -> Washing in alum/chlorinated water bath to remove latex stain -> Sorting by finger caliber and length.",
            "storage_method": "Cold storage at 13-14°C in ethylene-free chambers with air scrubbing; ripening rooms with controlled 100 ppm ethylene gas.",
            "preservation_method": "Controlled Atmosphere (CA) storage (2% O2, 5% CO2); vacuum dehydration; frying for crisps.",
            "processing_method": "Ripening under controlled temperature and humidity -> Peeling -> Slicing -> Solar drying or hot air blast.",
            "packaging_method": "Telescopic corrugated fiberboard boxes (13 kg standard) with perforated polyethylene liners.",
            "food_uses": "Fresh fruit, culinary banana curries, banana chips, baby weaning foods, bakery purees.",
            "industrial_uses": "Extraction of natural textile and paper pulp fiber from pseudostem pseudo-bark; starch extraction.",
            "by_products": "Pseudostem sap (natural organic dye and mordant), banana central core (culinary fiber vegetable), peel compost.",
            "source_reference": "ICAR-NRCB & IIFPT Thanjavur",
            "last_reviewed_at": "2026-03-02"
        },
        "products": [
            {
                "product_name": "Crispy Nendran Banana Chips",
                "product_category": "Food Product",
                "raw_material": "Mature unripe green Nendran or culinary plantain bananas",
                "processing_overview": "Peeling underwater -> Immersion in turmeric brine -> Mechanical cross slicing directly into hot coconut or vegetable oil (170-180°C) -> Frying until crisp -> De-oiling -> Salting -> Nitrogen packaging.",
                "common_uses": "Crispy savory snack, tea-time accompaniment, export retail snack packs.",
                "storage_considerations": "Keep in airtight nitrogen-flushed multi-layer pouches away from light to prevent fat rancidity.",
                "value_addition_notes": "Converts raw green bananas into a high-demand premium snack with 80-120% value appreciation."
            },
            {
                "product_name": "Green Banana Resistant Starch Flour",
                "product_category": "Food Product",
                "raw_material": "Unripe green bananas with high amylose content",
                "processing_overview": "Washing -> Peeling -> Citric acid anti-browning dip -> Slicing -> Low-temperature drying (50°C to preserve resistant starch) -> Pulverizing to 100 mesh -> Sifting -> Packaging.",
                "common_uses": "Prebiotic dietary supplement, gut-health smoothie additive, gluten-free baking blend.",
                "storage_considerations": "Store in moisture-proof vacuum pouches in cool dry conditions.",
                "value_addition_notes": "Emerging functional health food commanding high margins in urban wellness markets."
            }
        ],
        "quiz": [
            {
                "question": "What is the primary sign that banana fingers on a bunch are ready for harvest?",
                "option_a": "Fingers turn completely black",
                "option_b": "Fingers become plump and round, losing their sharp angular ridges",
                "option_c": "The whole tree falls over naturally",
                "option_d": "Fruit exudes milk continuously",
                "correct_option": "B",
                "explanation": "As banana fingers fill with starch, the distinctive sharp angular facets round out, indicating physiological maturity for harvest."
            },
            {
                "question": "Why is de-handing washed in a clean water/alum bath immediately after cutting?",
                "option_a": "To dissolve the peel completely",
                "option_b": "To arrest and wash away milky latex exudate that otherwise stains and blackens the peel",
                "option_c": "To make fingers taste sweeter",
                "option_d": "To kill all seeds",
                "correct_option": "B",
                "explanation": "Severing banana hands releases sticky latex sap; if not washed immediately, it drips onto peel, causing unsightly permanent black stains."
            },
            {
                "question": "Which viral disease in banana is transmitted by the banana aphid (Pentalonia nigronervosa)?",
                "option_a": "Banana Bunchy Top Virus (BBTV)",
                "option_b": "Downy mildew",
                "option_c": "Stem rust",
                "option_d": "Ergot",
                "correct_option": "A",
                "explanation": "Banana Bunchy Top Virus is a devastating stunted viral disease vectored by aphids, characterized by narrow, crowded, upright leaves."
            }
        ]
    },
    {
        "slug": "sugarcane",
        "name": "Sugarcane",
        "scientific_name": "Saccharum officinarum",
        "category": "Cash Crop",
        "description": "High-biomass C4 perennial grass crop providing sugar, traditional jaggery, bio-fuel ethanol, and paper pulp bagasse.",
        "water_requirement": "High",
        "season_summary": "Early (Dec-Jan), Mid (Feb-Mar), Late (Apr-May), Special (Jun-Jul in South India)",
        "soil_climate_summary": "Deep, well-drained fertile loamy, alluvial, or clay-loam soils with good moisture retention. Tropical warm sunny climate.",
        "image_path": "/static/img/sugarcane.svg",
        "min_temp": 20.0,
        "max_temp": 40.0,
        "min_rainfall": 1000.0,
        "max_rainfall": 2000.0,
        "climate_source_note": "ICAR-Sugarcane Breeding Institute (SBI) Coimbatore",
        "difficulty_level": "Intermediate",
        "soils": ["Alluvial", "Clay", "Loamy", "Black"],
        "seasons": ["Year-round", "Kharif"],
        "regions": ["Tamil Nadu (Western Zone - Coimbatore/Erode)", "Tamil Nadu (Cauvery Delta)", "Uttar Pradesh (Central Plain)", "Maharashtra (Deccan Plateau)"],
        "cultivation_guide": {
            "seed_selection": "Use 8-10 month old disease-free seed setts having vigorous buds. Dip setts in Carbendazim (1 g/L) or Trichoderma solution.",
            "land_preparation": "Deep chiseling followed by 2-3 deep ploughings to break hard pan. Form deep furrows at 90-120 cm or wide-row spacing (150 cm for mechanical harvesting).",
            "sowing_method": "Plant two-budded or single-budded chip setts end-to-end in furrows, covering with 2-3 cm fine soil. Sustainable Sugarcane Initiative (SSI) uses raised bud nursery.",
            "irrigation": "Irrigate immediately after planting, life irrigation on day 4-5. Adopt drip irrigation for 35-45% water saving and uniform cane girth.",
            "nutrient_management": "Apply 25 t/ha FYM or pressmud. Apply nitrogen and potassium in splits: basal, 30, 60, and 90 days. Avoid late nitrogen which reduces juice sucrose percentage.",
            "weed_management": "Hand weeding at 30, 60, and 90 days. Earthing up at 90-120 days strengthens root hold against lodging.",
            "growth_stages": "Germination (0-35 days) -> Tillering / Formative (35-100 days) -> Grand Growth (100-270 days) -> Maturation / Ripening (270-360 days).",
            "common_mistakes": "Over-irrigation in early germination; late nitrogen application reducing sugar content; harvesting immature cane before peak Brix.",
            "source_reference": "ICAR-SBI Coimbatore Cultivation Guide",
            "last_reviewed_at": "2026-03-01"
        },
        "pests_diseases": [
            {
                "name": "Early Shoot Borer (Chilo infuscatellus)",
                "type": "pest",
                "symptoms": "Larvae bore into young shoots during formative stage, producing dead hearts that can be pulled out easily and emit offensive odor.",
                "contributing_conditions": "High temperatures (above 35°C), low relative humidity, dry soil conditions during summer months.",
                "prevention": "Trash mulching in furrows at 3 days after planting; release egg parasitoid Trichogramma chilonis at 50,000/ha.",
                "management": "Earthing up at 30-45 days; light frequent irrigations to lower soil temperature; apply granulosis virus (GV).",
                "source_reference": "ICAR-SBI Coimbatore Pest Series",
                "last_reviewed_at": "2026-02-12"
            },
            {
                "name": "Red Rot (Colletotrichum falcatum)",
                "type": "disease",
                "symptoms": "Third and fourth leaf show yellowing and drying along midrib; split cane shows red tissue with diagnostic white cross-bands and alcoholic smell.",
                "contributing_conditions": "Monoculture of susceptible varieties, waterlogging, contaminated seed setts.",
                "prevention": "Strictly plant certified disease-free setts of resistant varieties; avoid ratooning infected fields; hot water treatment of seed setts (52°C for 30 min).",
                "management": "Uproot and burn diseased clumps immediately; do not run irrigation water from infected fields into healthy crops.",
                "source_reference": "ICAR-Indian Institute of Sugarcane Research (IISR) Lucknow",
                "last_reviewed_at": "2026-01-25"
            }
        ],
        "harvest_guide": {
            "maturity_indicators": "Hand refractometer Brix reading reaches 18-20% at middle internodes; cane base metallic sound when tapped; flowering/tassel emergence in some varieties.",
            "approximate_harvest_period": "10-12 months for early varieties; 12-14 months for mid/late varieties.",
            "harvesting_method": "Cut cane flush with ground level with sharp cane knives or mechanical harvester; lowest internodes contain highest sugar concentration.",
            "handling_precautions": "Transport cut cane to mill or crusher within 24-36 hours; delays cause rapid inversion of sucrose into non-crystallizing glucose.",
            "storage_preparation": "Raw sugarcane cannot be stored long post-harvest; crush immediately to preserve juice recovery.",
            "source_reference": "ICAR-IISR Post-Harvest Manual",
            "last_reviewed_at": "2026-02-10"
        },
        "post_harvest_guide": {
            "cleaning_and_grading": "Strip dry trash, roots, and green tops thoroughly before feeding into crusher rollers.",
            "storage_method": "Process fresh immediately; jaggery product stored in airtight polythene-lined bins in cool dry room.",
            "preservation_method": "Thermal evaporation into solid or liquid jaggery; sulfur dioxide or vacuum pan crystallization for white sugar.",
            "processing_method": "Crushing -> Juice filtration -> Heating and clarification with plant mucilages (okra stem extract) -> Concentration to strike point (118°C) -> Cooling in cooling pans.",
            "packaging_method": "Solid blocks wrapped in food-grade film and corrugated boxes; granulated jaggery in zip pouches.",
            "food_uses": "White refined sugar, jaggery (gur), brown sugar, confectionery sweets, beverage sweetening.",
            "industrial_uses": "Molasses fermentation into fuel-grade ethanol, bio-chemical solvents, potable spirits.",
            "by_products": "Bagasse (co-generation steam and electric power, paper manufacturing), pressmud/filter-cake (rich organic bio-fertilizer), molasses (distillery feed).",
            "source_reference": "ICAR-IISR Lucknow & TNAU Post-Harvest Centre",
            "last_reviewed_at": "2026-03-04"
        },
        "products": [
            {
                "product_name": "Chemical-Free Granular Jaggery (Gur Powder)",
                "product_category": "Food Product",
                "raw_material": "Freshly extracted clean sugarcane juice",
                "processing_overview": "Crushing juice -> Clarification with botanical mucilage (Lady's Finger / Deola extract) without chemical hydros -> Boiling in open pans -> Crystallization stirring -> Granulation -> Sifting -> Moisture drying to <2% -> Pouch packing.",
                "common_uses": "Natural iron-rich sweetener for tea, coffee, baby foods, traditional sweets, healthy baking.",
                "storage_considerations": "Must have <2% moisture. Store in moisture-barrier aluminum foil laminate pouches away from humidity.",
                "value_addition_notes": "Premium organic health food selling at 2-3x the price of conventional white crystal sugar."
            },
            {
                "product_name": "Sugarcane Blackstrap Molasses",
                "product_category": "By-Product",
                "raw_material": "Viscous syrup remaining after repeated sugar crystallization cycles",
                "processing_overview": "Cane juice clarification -> Multiple evaporation stages -> Centrifugal separation of crystal sugar -> Molasses cooling and concentration -> Drum filling.",
                "common_uses": "Livestock feed sweetener, silage fermentation enhancer, commercial ethanol fermentation, microbial yeast growth medium.",
                "storage_considerations": "Store in clean steel or HDPE tanks away from rain to prevent spontaneous fermentation.",
                "value_addition_notes": "Core industrial byproduct driving India's biofuel ethanol blending mandate."
            }
        ],
        "quiz": [
            {
                "question": "Why is sugarcane always harvested flush with the ground level?",
                "option_a": "To prevent people from tripping on stalks",
                "option_b": "Because the bottom-most internodes contain the highest concentration of sucrose",
                "option_c": "To ensure roots never grow back",
                "option_d": "To dry the soil faster",
                "correct_option": "B",
                "explanation": "The basal internodes close to ground level have the maximum sugar content; leaving tall stumps causes significant sugar loss."
            },
            {
                "question": "What is the critical risk if harvested sugarcane is left in the sun for more than 48 hours before crushing?",
                "option_a": "The stalk turns to wood completely",
                "option_b": "Sucrose rapidly inverts into reducing sugars (glucose/fructose), drastically reducing sugar recovery",
                "option_c": "The cane becomes toxic to humans",
                "option_d": "It catches fire automatically",
                "correct_option": "B",
                "explanation": "Post-harvest staling triggers invertase enzymes that split sucrose into glucose and fructose, causing severe weight loss and sugar recovery drops."
            },
            {
                "question": "Which diagnostic symptom characterizes Red Rot disease when a sugarcane stalk is split open?",
                "option_a": "Solid black charcoal inside",
                "option_b": "Red internal tissue interrupted by characteristic white horizontal patches with an alcoholic odor",
                "option_c": "Bright green liquid flowing out",
                "option_d": "Completely hollow empty stem with no discoloration",
                "correct_option": "B",
                "explanation": "Red rot produces reddish pith with distinctive white transverse bands and a fermenting acidic or alcoholic smell."
            }
        ]
    },
    {
        "slug": "groundnut",
        "name": "Groundnut (Peanut)",
        "scientific_name": "Arachis hypogaea",
        "category": "Pulse",
        "description": "Valuable dual-purpose oilseed and legume crop enriching soil through atmospheric nitrogen fixation while providing edible oil and protein-rich meal.",
        "water_requirement": "Low",
        "season_summary": "Kharif (rainfed), Rabi/Summer (irrigated)",
        "soil_climate_summary": "Well-drained light-textured sandy loam or red loamy soils with loose friable surface. Warm climate with moderate rainfall.",
        "image_path": "/static/img/groundnut.svg",
        "min_temp": 20.0,
        "max_temp": 35.0,
        "min_rainfall": 450.0,
        "max_rainfall": 750.0,
        "climate_source_note": "ICAR-Directorate of Groundnut Research (DGR) Junagadh",
        "difficulty_level": "Beginner",
        "soils": ["Sandy", "Red", "Loamy"],
        "seasons": ["Kharif", "Rabi", "Zaid"],
        "regions": ["Tamil Nadu (Western Zone - Coimbatore/Erode)", "Tamil Nadu (Southern Zone - Madurai/Tirunelveli)", "Andhra Pradesh (Coastal Zone)", "Maharashtra (Deccan Plateau)"],
        "cultivation_guide": {
            "seed_selection": "Shell pods 1-2 weeks before sowing. Select bold, healthy kernels with intact seed coats. Treat with Trichoderma (4 g/kg) and Rhizobium bio-fertilizer.",
            "land_preparation": "Plough 2-3 times to create a loose, pulverized, friable seedbed which is vital for easy peg penetration into the soil.",
            "sowing_method": "Sow kernels at 30 cm x 10 cm spacing at a depth of 4-5 cm using a seed drill or hand dibbling.",
            "irrigation": "Critical water stages: flowering, pegging (35-50 DAS), and pod development (55-75 DAS). Avoid moisture stress during peg penetration.",
            "nutrient_management": "Apply 10 t/ha compost. Apply gypsum (400 kg/ha) at 40-45 DAS around pegging stage; calcium is essential for pod filling and prevents 'pops' (empty pods).",
            "weed_management": "Keep field clean during the first 35 days. Crucial: strictly avoid any hoeing or mechanical weeding after 45 days, as it snaps delicate entering pegs.",
            "growth_stages": "Germination (0-7 days) -> Flowering (25-35 days) -> Pegging (35-50 days) -> Pod development (50-80 days) -> Pod maturation (80-105 days).",
            "common_mistakes": "Disturbing soil with hoes during peg penetration; neglecting gypsum application leading to hollow unfilled pods; storing wet pods causing aflatoxin.",
            "source_reference": "ICAR-DGR Junagadh & TNAU Pulses & Oilseeds Manual",
            "last_reviewed_at": "2026-03-02"
        },
        "pests_diseases": [
            {
                "name": "Tikka Leaf Spot (Cercospora arachidicola / C. personata)",
                "type": "disease",
                "symptoms": "Early leaf spot produces small circular reddish-brown spots with yellow halos; late leaf spot produces darker circular spots without halo on lower leaf surface.",
                "contributing_conditions": "Prolonged leaf wetness, high humidity (>85%), temperatures around 25-28°C.",
                "prevention": "Crop rotation with cereals; seed treatment with Trichoderma; avoid dense planting.",
                "management": "Foliar spray of neem seed kernel extract (5%) or copper oxychloride at early lesion appearance under guidance.",
                "source_reference": "ICAR-DGR Pathology Bulletin",
                "last_reviewed_at": "2026-02-08"
            },
            {
                "name": "Red Hairy Caterpillar (Amsacta albistriga)",
                "type": "pest",
                "symptoms": "Gregarious caterpillars defoliate young plants completely, leaving only bare stems.",
                "contributing_conditions": "Emergence of adult moths immediately after the first heavy monsoon soaking shower.",
                "prevention": "Set up light traps (1/ha) immediately after first monsoon rain to attract and destroy adult moths before egg laying; dig boundary trenches.",
                "management": "Collect and destroy egg masses on weeds; spray neem oil or Bacillus thuringiensis when caterpillars are in early instars.",
                "source_reference": "TNAU Entomology Portal",
                "last_reviewed_at": "2026-01-18"
            }
        ],
        "harvest_guide": {
            "maturity_indicators": "Vines turn yellowish; leaves begin to drop; inner shell of opened pods develops dark brownish-black veins and kernels possess distinctive pink seed coats.",
            "approximate_harvest_period": "100-115 days depending on bunch or spreading variety.",
            "harvesting_method": "Pull plants manually when soil is moist or use tractor-drawn groundnut digger. In dry soils, give light irrigation before pulling.",
            "handling_precautions": "Shake plants to dislodge soil from pods. Strip pods immediately and spread out in thin layers under sun.",
            "storage_preparation": "Dry pods thoroughly in sun until pod moisture drops below 8-9% (pods rattle when shaken) to strictly prevent Aspergillus flavus mold growth.",
            "source_reference": "ICAR-CIPHET Groundnut Handling",
            "last_reviewed_at": "2026-02-15"
        },
        "post_harvest_guide": {
            "cleaning_and_grading": "De-stoning, winnowing to remove dust and unfilled 'pops', mechanical grading by pod size.",
            "storage_method": "Store in dry, well-ventilated godowns in gunny bags stacked on wooden dunnage away from masonry walls.",
            "preservation_method": "Maintain moisture strictly below 8% to prevent toxic Aflatoxin contamination.",
            "processing_method": "Decortication (pod shelling) -> Kernel grading -> Expeller or cold wood-press (marachekku) crushing.",
            "packaging_method": "Jute bags for in-shell pods; nitrogen-flushed poly pouches for roasted or blanched kernels.",
            "food_uses": "Edible cooking oil, peanut butter, roasted salted snacks, peanut brittle (chikki), confectionery paste.",
            "industrial_uses": "Protein isolates, cosmetic soaps, pharmaceutical carriers.",
            "by_products": "Groundnut oil cake (rich 45% protein dairy and poultry feed), groundnut shells (bio-fuel briquettes, mushroom bedding).",
            "source_reference": "IIFPT Thanjavur & ICAR-DGR",
            "last_reviewed_at": "2026-03-01"
        },
        "products": [
            {
                "product_name": "Cold-Pressed Virgin Groundnut Oil",
                "product_category": "Food Product",
                "raw_material": "Clean, sorted sound groundnut kernels",
                "processing_overview": "Pod shelling -> Optical color sorting to eliminate moldy kernels -> Slow traditional wood-press (ghani/chekkau) cold crushing without chemical heat -> Natural sedimentation filtration -> Glass or tin bottling.",
                "common_uses": "Traditional stir-frying, deep frying, salad dressings, authentic regional tempering.",
                "storage_considerations": "Store in dark amber glass or tin containers away from heat. Shelf life 9-12 months.",
                "value_addition_notes": "Sells at 50-80% premium over industrially solvent-refined oils due to retained aroma and antioxidants."
            },
            {
                "product_name": "Roasted Salted Peanuts & Chikki",
                "product_category": "Food Product",
                "raw_material": "Bold-sized uniform groundnut kernels, jaggery",
                "processing_overview": "Rotary sand roasting at 140°C -> Blanching to remove seed coat -> Brine salting or combining with boiled jaggery syrup -> Rolling into chikki slabs -> Cooling and wrapper packing.",
                "common_uses": "High-protein wholesome snacks, sports nutrition bars, school child nutrition.",
                "storage_considerations": "Moisture barrier metalized polyester pouches to preserve crispness.",
                "value_addition_notes": "Very popular cottage industry product transforming raw farm kernels into high-margin ready-to-eat confections."
            }
        ],
        "quiz": [
            {
                "question": "Why is gypsum (calcium sulphate) applied to groundnut crops at the pegging stage?",
                "option_a": "To make leaves turn bright blue",
                "option_b": "Because developing pods absorb calcium directly from soil to ensure proper kernel filling and avoid 'pops'",
                "option_c": "To stop weeds from flowering",
                "option_d": "To sweeten the oil",
                "correct_option": "B",
                "explanation": "Groundnut pods absorb calcium directly through shell tissue from surrounding soil; lack of calcium results in empty, unfilled pods known as 'pops'."
            },
            {
                "question": "What is the critical danger of storing damp groundnut pods above 9% moisture?",
                "option_a": "The pods will turn into stone",
                "option_b": "Growth of Aspergillus flavus mold producing carcinogenic aflatoxins",
                "option_c": "Kernels will turn into cotton fibers",
                "option_d": "The shells will dissolve completely",
                "correct_option": "B",
                "explanation": "Damp pods quickly harbor Aspergillus flavus, a mold that produces potent aflatoxins that make the crop unsafe for humans and animals."
            },
            {
                "question": "Why should farmers avoid mechanical inter-cultivation or hoeing after 45 days in groundnut?",
                "option_a": "It attracts birds",
                "option_b": "It severs and destroys the fragile pegs entering the soil to form pods",
                "option_c": "It causes sudden rainfall",
                "option_d": "It makes roots grow upward",
                "correct_option": "B",
                "explanation": "After pollination, pegs elongate downward into the soil to develop pods; any mechanical tillage at this stage tears these pegs off the plant."
            }
        ]
    },
    {
        "slug": "finger-millet-ragi",
        "name": "Finger Millet (Ragi)",
        "scientific_name": "Eleusine coracana",
        "category": "Millets",
        "description": "Climate-resilient 'Nutri-cereal' boasting thirty times the calcium of rice, exceptional drought tolerance, and high dietary fiber.",
        "water_requirement": "Low",
        "season_summary": "Kharif (rainfed), Rabi/Summer (irrigated)",
        "soil_climate_summary": "Porous red loamy, sandy loam, or alluvial soils with good drainage. Warm climate, remarkably drought hardy.",
        "image_path": "/static/img/ragi.svg",
        "min_temp": 15.0,
        "max_temp": 35.0,
        "min_rainfall": 400.0,
        "max_rainfall": 800.0,
        "climate_source_note": "ICAR-Indian Institute of Millets Research (IIMR) Hyderabad",
        "difficulty_level": "Beginner",
        "soils": ["Red", "Sandy", "Loamy"],
        "seasons": ["Kharif", "Rabi", "Zaid"],
        "regions": ["Tamil Nadu (Western Zone - Coimbatore/Erode)", "Karnataka (Southern Plateau)", "Tamil Nadu (Southern Zone - Madurai/Tirunelveli)"],
        "cultivation_guide": {
            "seed_selection": "Select certified varieties resistant to blast (e.g., GPU series or CO series). Treat seeds with Azospirillum and Trichoderma.",
            "land_preparation": "Plough 2-3 times to obtain a fine, firm seedbed. Soil compaction should be minimized.",
            "sowing_method": "Transplanting 18-20 day-old seedlings at 22.5 cm x 10 cm spacing produces significantly higher yields than direct broadcasting.",
            "irrigation": "Highly drought-tolerant; needs only 2-3 protective irrigations at tillering and grain filling during dry spells in rainfed conditions.",
            "nutrient_management": "Apply 10 t/ha farmyard manure. Split nitrogen into basal and top dressing at tillering stage.",
            "weed_management": "First weeding at 15-20 days; second weeding at 30-35 days using hand hoe or dryland weeder.",
            "growth_stages": "Seedling (0-20 days) -> Tillering (20-40 days) -> Panicle initiation (40-60 days) -> Flowering (60-75 days) -> Maturity (90-115 days).",
            "common_mistakes": "Broadcasting seeds too densely without thinning; planting in poorly drained waterlogged soils; delayed harvest leading to bird damage.",
            "source_reference": "ICAR-IIMR & TNAU Department of Millets",
            "last_reviewed_at": "2026-03-05"
        },
        "pests_diseases": [
            {
                "name": "Finger Millet Blast (Magnaporthe grisea)",
                "type": "disease",
                "symptoms": "Spindle-shaped lesions on leaves; neck blast blackens peduncle and breaks earheads; finger blast produces unfilled chaffy fingers.",
                "contributing_conditions": "Overcast humid weather, dense planting, excessive nitrogen.",
                "prevention": "Grow blast-resistant varieties; seed treatment with bio-agents; balance nitrogen with potassium.",
                "management": "Foliar spray with Pseudomonas fluorescens (0.2%) at ear emergence.",
                "source_reference": "ICAR-IIMR Pathology",
                "last_reviewed_at": "2026-02-10"
            },
            {
                "name": "Shoot Fly (Atherigona soccata)",
                "type": "pest",
                "symptoms": "Maggots feed on growing tip of young seedlings causing dead heart symptoms in first 4 weeks.",
                "contributing_conditions": "Delayed sowing, overcast conditions during early seedling stage.",
                "prevention": "Sow early at monsoon onset; use higher seed rate and thin seedlings; adopt seedling transplanting.",
                "management": "Spray neem seed kernel extract (5%) on young seedlings if shoot fly symptoms appear.",
                "source_reference": "TNAU Entomology Advisory",
                "last_reviewed_at": "2026-01-22"
            }
        ],
        "harvest_guide": {
            "maturity_indicators": "Earheads turn brown and dry; seeds are hard and turn dark brown/brick-red.",
            "approximate_harvest_period": "95-120 days depending on variety.",
            "harvesting_method": "Cut mature earheads with sickle in two pickings, or harvest entire plant at ground level.",
            "handling_precautions": "Heap earheads under cover for 2-3 days for curing before threshing to facilitate easy seed detachment.",
            "storage_preparation": "Thresh and dry seeds in sun to 10-12% moisture. Ragi grain has a hard seed coat and naturally resists storage insect pests for years.",
            "source_reference": "ICAR-CIPHET Millet Processing Handbook",
            "last_reviewed_at": "2026-02-18"
        },
        "post_harvest_guide": {
            "cleaning_and_grading": "Aspiration cleaning, destoning, and gravity separation of small seeds.",
            "storage_method": "Traditional earthen pots, metal bins, or hermetic bags. Grains can safely store for 2-5 years under dry conditions.",
            "preservation_method": "Solar drying down to 10% moisture.",
            "processing_method": "Dehulling -> Malting (germination, drying, roasting) -> Roller or attrition milling.",
            "packaging_method": "Moisture-proof pouch laminates or vacuum-packed bags.",
            "food_uses": "Ragi kali / mudde (steamed dumpling), ragi malt porridge, ragi roti, idli/dosa mix, bakery cookies.",
            "industrial_uses": "Malting and brewing adjunct, weaning food formulations, composite baking flours.",
            "by_products": "Ragi straw (highly palatable, digestible cattle fodder), bran husk.",
            "source_reference": "ICAR-IIMR & CFTRI Mysore",
            "last_reviewed_at": "2026-03-01"
        },
        "products": [
            {
                "product_name": "Sprouted Ragi Malt Health Mix",
                "product_category": "Food Product",
                "raw_material": "Cleaned sound finger millet grains",
                "processing_overview": "Grain cleaning -> Soaking for 12 hours -> Germination for 24-36 hours (enhances bio-available iron and calcium) -> Kiln drying -> Gentle roasting -> Pulverizing -> Blending with cardamom -> Pouch packaging.",
                "common_uses": "Nutritious breakfast porridge, weaning food for infants, convalescent drink for elderly.",
                "storage_considerations": "Keep in airtight containers; use within 6 months.",
                "value_addition_notes": "Converts inexpensive grain into a high-value nutritional drink fetching 3-4x raw price."
            },
            {
                "product_name": "Ragi Millet Bakery & Cookie Blend",
                "product_category": "Food Product",
                "raw_material": "Malted ragi flour, whole wheat flour, natural jaggery",
                "processing_overview": "Flour blending -> Micro-sifting -> Nitrogen packaging in ready-to-bake pre-mix packs.",
                "common_uses": "Healthy gluten-reduced cookies, cakes, and artisan crackers.",
                "storage_considerations": "Store in cool dry conditions in sealed moisture-proof bags.",
                "value_addition_notes": "Taps into strong consumer demand for wholesome traditional millets in modern bakery formats."
            }
        ],
        "quiz": [
            {
                "question": "Why is Finger Millet (Ragi) hailed as an exceptionally resilient security crop during droughts?",
                "option_a": "It produces underground tubers",
                "option_b": "It has an efficient C4 photosynthetic system, low water requirement, and produces grain even with minimal rainfall",
                "option_c": "It does not need any sunshine",
                "option_d": "It can be harvested in 10 days",
                "correct_option": "B",
                "explanation": "Finger millet is a drought-hardy C4 plant that tolerates prolonged dry spells and yields nutritious grain with modest moisture."
            },
            {
                "question": "What nutritional mineral is Finger Millet particularly famous for containing at 30 times the concentration of polished rice?",
                "option_a": "Calcium",
                "option_b": "Mercury",
                "option_c": "Sodium",
                "option_d": "Lead",
                "correct_option": "A",
                "explanation": "Ragi is one of the richest plant sources of calcium (~344 mg/100 g), making it ideal for bone health and infant nutrition."
            },
            {
                "question": "Why does sprouted (malted) ragi flour have superior nutritional value over raw ragi flour?",
                "option_a": "It doubles the amount of oil",
                "option_b": "Germination activates enzymes that reduce phytates and significantly enhance the bioavailability of iron and calcium",
                "option_c": "It removes all carbohydrates",
                "option_d": "It turns the grain bright green",
                "correct_option": "B",
                "explanation": "Malting breaks down anti-nutritional phytates, liberating bound minerals and making iron, calcium, and proteins much easier to digest."
            }
        ]
    },
    {
        "slug": "green-gram-pulses",
        "name": "Green Gram (Mung Bean)",
        "scientific_name": "Vigna radiata",
        "category": "Pulse",
        "description": "Short-duration, protein-rich legume crop ideal for crop rotations, summer catch cropping, and green manuring.",
        "water_requirement": "Low",
        "season_summary": "Kharif, Rabi (rice fallows), and Summer (Zaid)",
        "soil_climate_summary": "Well-drained fertile loamy or alluvial soils. Sensitive to waterlogging and saline conditions.",
        "image_path": "/static/img/greengram.svg",
        "min_temp": 20.0,
        "max_temp": 38.0,
        "min_rainfall": 350.0,
        "max_rainfall": 600.0,
        "climate_source_note": "ICAR-Indian Institute of Pulses Research (IIPR) Kanpur",
        "difficulty_level": "Beginner",
        "soils": ["Loamy", "Alluvial", "Red"],
        "seasons": ["Kharif", "Rabi", "Zaid"],
        "regions": ["Tamil Nadu (Cauvery Delta)", "Punjab & Haryana (Indo-Gangetic Plain)", "Maharashtra (Deccan Plateau)", "Andhra Pradesh (Coastal Zone)"],
        "cultivation_guide": {
            "seed_selection": "Use certified seed of synchronous maturity varieties resistant to Yellow Mosaic Virus (YMV). Treat seeds with Rhizobium and Trichoderma.",
            "land_preparation": "Plough 1-2 times to obtain loose tilth. In rice fallows, seeds are broadcast directly into moist stubble without tillage.",
            "sowing_method": "Sow at 30 cm x 10 cm spacing at 3-4 cm depth with seed drill or hand dibbling.",
            "irrigation": "Needs 1-2 irrigations only. Critical stages: flowering and pod development. Never allow standing water.",
            "nutrient_management": "Apply 20 kg N and 40 kg P2O5 per ha as basal. Foliar spray of 2% DAP or pulse wonder at flowering enhances pod setting.",
            "weed_management": "One hand weeding at 15-20 DAS. Crop rapidly closes canopy to suppress later weeds.",
            "growth_stages": "Germination (0-5 days) -> Vegetative (5-25 days) -> Flowering (25-40 days) -> Pod development (40-55 days) -> Maturity (60-75 days).",
            "common_mistakes": "Over-watering leading to collar rot; delayed picking causing pod shattering in fields; neglecting whitefly management.",
            "source_reference": "ICAR-IIPR Kanpur Pulse Production Manual",
            "last_reviewed_at": "2026-03-02"
        },
        "pests_diseases": [
            {
                "name": "Mungbean Yellow Mosaic Virus (MYMV)",
                "type": "disease",
                "symptoms": "Yellow patches on young leaves alternating with green tissue, progressing to complete yellowing of foliage and stunted sterile pods.",
                "contributing_conditions": "High populations of whitefly (Bemisia tabaci) vector during warm, dry weather.",
                "prevention": "Grow MYMV-resistant varieties (e.g., CO 8, VBN 4); install yellow sticky traps (12/ha); seed treatment with thiamethoxam/bio-agents.",
                "management": "Spray neem oil (3%) or recommended botanicals to control the whitefly insect vector early.",
                "source_reference": "TNAU Pulses Department",
                "last_reviewed_at": "2026-02-12"
            },
            {
                "name": "Pod Borer Complex (Maruca vitrata / Helicoverpa)",
                "type": "pest",
                "symptoms": "Larvae web flowers and young pods together with silk, feeding inside pods on developing green seeds.",
                "contributing_conditions": "High humidity, overcast days during peak flowering and pod initiation.",
                "prevention": "Intercrop with sorghum or maize; install pheromone traps; conserve predatory wasps.",
                "management": "Foliar spray of Bacillus thuringiensis (Bt) or NSKE 5% at early flower budding.",
                "source_reference": "ICAR-IIPR Kanpur",
                "last_reviewed_at": "2026-01-20"
            }
        ],
        "harvest_guide": {
            "maturity_indicators": "Over 80-85% of pods turn dark brown or blackish-brown and dry.",
            "approximate_harvest_period": "65-75 days after sowing (rapid maturity).",
            "harvesting_method": "Hand pick pods or uproot entire plant in morning hours to prevent shatter loss.",
            "handling_precautions": "Avoid harvesting during mid-day heat when brittle pods shatter and scatter seeds on the ground.",
            "storage_preparation": "Sun dry threshed seeds down to 9-10% moisture before bagging. Add neem leaves to deter pulse beetle.",
            "source_reference": "ICAR-CIPHET Pulse Processing Manual",
            "last_reviewed_at": "2026-02-15"
        },
        "post_harvest_guide": {
            "cleaning_and_grading": "De-stoning, aspiration, grading by seed size and luster.",
            "storage_method": "Store in clean metal drums, hermetic PICS bags, or lined gunny bags on raised dunnage.",
            "preservation_method": "Hermetic storage to suffocate bruchid pulse beetles (Callosobruchus maculatus).",
            "processing_method": "Dehulling -> Splitting -> Water or oil conditioning -> Dal polishing.",
            "packaging_method": "Multi-layer poly pouches or vacuum-packed nitrogen flush packs.",
            "food_uses": "Yellow split moong dal, sprouted salads, sweet moong halwa, crispy namkeen snacks, papad.",
            "industrial_uses": "Extracted pulse protein concentrate, glass noodles (cellophane noodles).",
            "by_products": "Dal chuni / husk (high-protein cattle feed), crop residue for soil organic incorporation.",
            "source_reference": "IIFPT Thanjavur & CFTRI",
            "last_reviewed_at": "2026-03-02"
        },
        "products": [
            {
                "product_name": "Premium Polished Moong Dal (Split Pulse)",
                "product_category": "Food Product",
                "raw_material": "Cleaned sound whole green gram seeds",
                "processing_overview": "Grading -> Pitting/scratching seed coat -> Water/oil conditioning -> Dehulling through emery rollers -> Split dal separation -> Air aspiration -> Packing.",
                "common_uses": "Daily staple lentil soups (dal tadka, sambar), khichdi, healthy easily digestible convalescent diet.",
                "storage_considerations": "Keep strictly dry in hermetic packs; protect from bruchid beetles.",
                "value_addition_notes": "Essential national staple with steady high turnover and predictable margin."
            },
            {
                "product_name": "Roasted Crispy Moong Dal Namkeen",
                "product_category": "Food Product",
                "raw_material": "Split dehulled moong dal, vegetable oil, salt",
                "processing_overview": "Soaking split moong dal -> Surface moisture drying -> Quick flash frying or hot air roasting -> Spin de-oiling -> Salt dusting -> Nitrogen pouch packing.",
                "common_uses": "Protein-rich savory teatime snack, ready-to-eat convenience food.",
                "storage_considerations": "Nitrogen-flushed laminate bags; store away from sunlight.",
                "value_addition_notes": "Transforms raw pulses into a consumer snack with 100%+ value addition."
            }
        ],
        "quiz": [
            {
                "question": "Which insect vector is responsible for transmitting the devastating Yellow Mosaic Virus in green gram?",
                "option_a": "Whitefly (Bemisia tabaci)",
                "option_b": "Mosquito",
                "option_c": "Honeybee",
                "option_d": "Earthworm",
                "correct_option": "A",
                "explanation": "Whiteflies suck sap and transmit the Mungbean Yellow Mosaic Virus between plants, causing severe leaf yellowing and yield loss."
            },
            {
                "question": "Why is harvesting green gram pods performed during morning hours rather than hot mid-day?",
                "option_a": "To avoid sunburn on hands",
                "option_b": "To prevent pods from bursting open and shattering seeds on the ground under mid-day heat",
                "option_c": "Because plants sleep in the morning",
                "option_d": "To harvest wet seeds",
                "correct_option": "B",
                "explanation": "Under dry, hot mid-day sun, mature legume pods become brittle and easily shatter, shedding seeds onto the soil where they cannot be recovered."
            },
            {
                "question": "What is the duration from sowing to harvest for typical green gram varieties?",
                "option_a": "300 to 365 days",
                "option_b": "60 to 75 days",
                "option_c": "150 to 180 days",
                "option_d": "20 to 30 days",
                "correct_option": "B",
                "explanation": "Green gram is an exceptionally fast-maturing pulse, reaching harvest in 60-75 days, making it ideal for summer catch cropping."
            }
        ]
    }
]

TRANSLATION_RECORDS = [
    # Tamil translations
    {"entity_type": "crop", "slug": "rice-paddy", "field": "name", "lang": "ta", "title": "நெல்", "content": "நெல் (அரிசி)"},
    {"entity_type": "crop", "slug": "rice-paddy", "field": "description", "lang": "ta", "title": "நெல் விவரம்", "content": "உலக மக்கள் தொகையில் பாதியளவினர் உண்ணும் முதன்மை தானியப் பயிர். பல்வேறு தட்பவெப்ப மண்டலங்களில் நீர் தேங்கிய நன்செய் நிலங்களில் பெருமளவில் பயிரிடப்படுகிறது."},
    {"entity_type": "crop", "slug": "wheat", "field": "name", "lang": "ta", "title": "கோதுமை", "content": "கோதுமை"},
    {"entity_type": "crop", "slug": "wheat", "field": "description", "lang": "ta", "title": "கோதுமை விவரம்", "content": "இந்தியாவின் முதன்மையான குளிர்கால ரபி தானியப் பயிர். ரொட்டி, சப்பாத்தி மற்றும் பேக்கரி தயாரிப்புகளுக்கு முக்கிய மூலப்பொருள்."},
    {"entity_type": "crop", "slug": "maize-corn", "field": "name", "lang": "ta", "title": "மக்காச்சோளம்", "content": "மக்காச்சோளம்"},
    {"entity_type": "crop", "slug": "maize-corn", "field": "description", "lang": "ta", "title": "மக்காச்சோளம் விவரம்", "content": "'தானியங்களின் ராணி' என்று அழைக்கப்படும் அதிக மகசூல் திறன் கொண்ட தானியம். உணவு, கால்நடை தீவனம் மற்றும் தொழில்துறை மாவுச்சத்துக்கு பயன்படுகிறது."},
    {"entity_type": "crop", "slug": "tomato", "field": "name", "lang": "ta", "title": "தக்காளி", "content": "தக்காளி"},
    {"entity_type": "crop", "slug": "tomato", "field": "description", "lang": "ta", "title": "தக்காளி விவரம்", "content": "சமையல் மற்றும் மதிப்புக்கூட்டலுக்கு பயன்படும் முக்கிய பணப்பயிர் காய்கறி. உலகளவில் பரவலாக பயிரிடப்படும் சத்துமிக்க தக்காளி."},
    {"entity_type": "crop", "slug": "cotton", "field": "name", "lang": "ta", "title": "பருத்தி", "content": "பருத்தி"},
    {"entity_type": "crop", "slug": "cotton", "field": "description", "lang": "ta", "title": "பருத்தி விவரம்", "content": "'வெள்ளைத் தங்கம்' எனப்படும் முதன்மையான இயற்கை நெசவு நார் பயிர். ஆடை உற்பத்திக்கும் பருத்தி விதை எண்ணெய் உற்பத்திக்கும் முக்கியமானது."},
    {"entity_type": "crop", "slug": "banana", "field": "name", "lang": "ta", "title": "வாழை", "content": "வாழை"},
    {"entity_type": "crop", "slug": "banana", "field": "description", "lang": "ta", "title": "வாழை விவரம்", "content": "சத்துமிக்க பழங்கள், காய் வாழை மற்றும் இயற்கை நார் வழங்கும் வெப்பமண்டல பல்லாண்டு பழப்பயிர்."},
    {"entity_type": "crop", "slug": "sugarcane", "field": "name", "lang": "ta", "title": "கரும்பு", "content": "கரும்பு"},
    {"entity_type": "crop", "slug": "sugarcane", "field": "description", "lang": "ta", "title": "கரும்பு விவரம்", "content": "சர்க்கரை, நாட்டு வெல்லம் மற்றும் எத்தனால் எரிபொருள் வழங்கும் உயர் பயோமாஸ் பணப்பயிர்."},
    {"entity_type": "crop", "slug": "groundnut", "field": "name", "lang": "ta", "title": "நிலக்கடலை", "content": "நிலக்கடலை (வேர்க்கடலை)"},
    {"entity_type": "crop", "slug": "groundnut", "field": "description", "lang": "ta", "title": "நிலக்கடலை விவரம்", "content": "மண்ணிற்கு தழைச்சத்தை நிலைநிறுத்தி, உயர் சமையல் எண்ணெய் மற்றும் புரதத்தை வழங்கும் இருபயன் எண்ணெய்வித்து பயிர்."},
    {"entity_type": "crop", "slug": "finger-millet-ragi", "field": "name", "lang": "ta", "title": "கேழ்வரகு", "content": "கேழ்வரகு (ராகி)"},
    {"entity_type": "crop", "slug": "finger-millet-ragi", "field": "description", "lang": "ta", "title": "கேழ்வரகு விவரம்", "content": "அரிசியை விட முப்பது மடங்கு அதிக சுண்ணாம்புச்சத்து (கால்சியம்) கொண்ட காலநிலை மாற்றத்தை தாங்கி வளரும் சத்துமிக்க சிறுதானியம்."},
    {"entity_type": "crop", "slug": "green-gram-pulses", "field": "name", "lang": "ta", "title": "பாசிப்பயறு", "content": "பாசிப்பயறு (பச்சைப்பயறு)"},
    {"entity_type": "crop", "slug": "green-gram-pulses", "field": "description", "lang": "ta", "title": "பாசிப்பயறு விவரம்", "content": "குறுகிய காலத்தில் அறுவடைக்கு வரும் புரதச்சத்து நிறைந்த பயறு வகை பயிர். நெல் தரிசு மற்றும் பயிர் சுழற்சிக்கு மிகவும் ஏற்றது."},

    # Hindi translations
    {"entity_type": "crop", "slug": "rice-paddy", "field": "name", "lang": "hi", "title": "चावल / धान", "content": "धान (चावल)"},
    {"entity_type": "crop", "slug": "rice-paddy", "field": "description", "lang": "hi", "title": "धान का विवरण", "content": "विश्व की आधी से अधिक आबादी का मुख्य खाद्यान्न। जलभराव वाले खेतों में उगाई जाने वाली प्रमुख खरीफ फसल।"},
    {"entity_type": "crop", "slug": "wheat", "field": "name", "lang": "hi", "title": "गेहूँ", "content": "गेहूँ"},
    {"entity_type": "crop", "slug": "wheat", "field": "description", "lang": "hi", "title": "गेहूँ का विवरण", "content": "भारत की सबसे महत्वपूर्ण रबी खाद्यान्न फसल जो खाद्य सुरक्षा और चपाती व ब्रेड निर्माण का मुख्य आधार है।"},
    {"entity_type": "crop", "slug": "maize-corn", "field": "name", "lang": "hi", "title": "मक्का", "content": "मक्का"},
    {"entity_type": "crop", "slug": "maize-corn", "field": "description", "lang": "hi", "title": "मक्का का विवरण", "content": "'अनाजों की रानी' कही जाने वाली बहुमुखी फसल, जिसका उपयोग भोजन, पशु आहार और औद्योगिक स्टार्च के लिए किया जाता है।"},
    {"entity_type": "crop", "slug": "tomato", "field": "name", "lang": "hi", "title": "टमाटर", "content": "टमाटर"},
    {"entity_type": "crop", "slug": "tomato", "field": "description", "lang": "hi", "title": "टमाटर का विवरण", "content": "व्यावसायिक रूप से अत्यंत लोकप्रिय सब्जी फसल, जो ताजे उपभोग और प्रसंस्करण (सॉस, प्यूरी) के लिए महत्वपूर्ण है।"},
    {"entity_type": "crop", "slug": "cotton", "field": "name", "lang": "hi", "title": "कपास", "content": "कपास"},
    {"entity_type": "crop", "slug": "cotton", "field": "description", "lang": "hi", "title": "कपास का विवरण", "content": "'सफेद सोना' कही जाने वाली प्राकृतिक वस्त्र रेशा फसल जो लाखों किसानों और वस्त्र उद्योगों को सहारा देती है।"},
    {"entity_type": "crop", "slug": "banana", "field": "name", "lang": "hi", "title": "केला", "content": "केला"},
    {"entity_type": "crop", "slug": "banana", "field": "description", "lang": "hi", "title": "केला का विवरण", "content": "सदाबहार उष्णकटिबंधीय फल फसल जो पौष्टिक फल, सब्जी और प्राकृतिक रेशा प्रदान करती है।"},
    {"entity_type": "crop", "slug": "sugarcane", "field": "name", "lang": "hi", "title": "गन्ना", "content": "गन्ना"},
    {"entity_type": "crop", "slug": "sugarcane", "field": "description", "lang": "hi", "title": "गन्ना का विवरण", "content": "चीनी, गुड़ और जैव-ईंधन इथेनॉल का मुख्य स्रोत प्रदान करने वाली उच्च बायोमास नकदी फसल।"},
    {"entity_type": "crop", "slug": "groundnut", "field": "name", "lang": "hi", "title": "मूंगफली", "content": "मूंगफली"},
    {"entity_type": "crop", "slug": "groundnut", "field": "description", "lang": "hi", "title": "मूंगफली का विवरण", "content": "मिट्टी की उर्वरता बढ़ाने वाली और खाद्य तेल व उच्च प्रोटीन खली प्रदान करने वाली महत्वपूर्ण तिलहन फसल।"},
    {"entity_type": "crop", "slug": "finger-millet-ragi", "field": "name", "lang": "hi", "title": "रागी / मडुआ", "content": "रागी (मडुआ)"},
    {"entity_type": "crop", "slug": "finger-millet-ragi", "field": "description", "lang": "hi", "title": "रागी का विवरण", "content": "चावल से तीस गुना अधिक कैल्शियम और प्रचुर आहार फाइबर युक्त सूखा-सहिष्णु पोषक अनाज।"},
    {"entity_type": "crop", "slug": "green-gram-pulses", "field": "name", "lang": "hi", "title": "मूंग (दाल)", "content": "मूंग (हरी दाल)"},
    {"entity_type": "crop", "slug": "green-gram-pulses", "field": "description", "lang": "hi", "title": "मूंग का विवरण", "content": "कम अवधि (60-70 दिन) में पकने वाली दलहनी फसल, जो फसल चक्र और मिट्टी संवर्धन के लिए सर्वोत्तम है।"}
]
