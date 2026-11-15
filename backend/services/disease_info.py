"""
PlantCare AI - Plant Pathology Knowledge Base
=============================================
Comprehensive agronomic information, symptoms, causes, and integrated pest management (IPM)
recommendations for detected plant diseases.
"""

DISEASE_KNOWLEDGE_BASE = {
    "Apple___Apple_scab": {
        "plant": "Apple",
        "disease": "Apple Scab",
        "status": "Diseased",
        "severity": "Moderate to High",
        "pathogen": "Venturia inaequalis (Fungus)",
        "description": "Apple scab is a pervasive fungal disease affecting Malus species. It causes olive-green to black velvety spots on leaves and fruit, causing premature defoliation and unmarketable fruit.",
        "symptoms": [
            "Olive-green to dull brown circular spots on upper leaf surfaces.",
            "Velvety texture on active lesions due to conidial spores.",
            "Distorted or puckered leaves with yellowing halos.",
            "Cork-like scabby lesions on fruit surface leading to cracks."
        ],
        "organic_treatment": [
            "Apply liquid copper or sulfur sprays early in the growing season before bud break.",
            "Spray neem oil or Bacillus subtilis bio-fungicide at first symptom onset.",
            "Rake and destroy fallen leaves in autumn to eliminate overwintering fungal pseudothecia."
        ],
        "chemical_treatment": [
            "Apply Captan or Mancozeb protective fungicides during wet spring periods.",
            "Use DMI (Demethylation Inhibitors) or Strobilurin (QoI) systemic fungicides for active control."
        ],
        "prevention": [
            "Plant scab-resistant cultivars such as Liberty, Enterprise, or Freedom.",
            "Prune canopy annually to facilitate rapid leaf drying and sunlight penetration.",
            "Avoid overhead irrigation."
        ]
    },
    "Apple___Black_rot": {
        "plant": "Apple",
        "disease": "Black Rot",
        "status": "Diseased",
        "severity": "High",
        "pathogen": "Botryosphaeria obtusa (Fungus)",
        "description": "Black rot attacks fruit, foliage, and tree limbs. Foliar infections produce 'frogeye' leaf spots, while infected fruit becomes dark, leathery, and mummified.",
        "symptoms": [
            "Frogeye leaf spots: circular purple spots maturing with tan centers.",
            "Sunken cankers on twigs, branches, and tree trunks.",
            "Dark brown rotting rings on fruit expanding rapidly into leathery black mummies."
        ],
        "organic_treatment": [
            "Prune out dead wood, fire blight strikes, and mummified fruit from the canopy.",
            "Apply bio-fungicides containing Trichoderma or copper sulfate during dormant periods."
        ],
        "chemical_treatment": [
            "Fungicidal applications of Captan, Thiophanate-methyl, or Fludioxonil starting at pink bud stage."
        ],
        "prevention": [
            "Remove all mummies and dead limbs from the orchard before budbreak.",
            "Prevent mechanical bark injuries and control wood-boring insects."
        ]
    },
    "Apple___healthy": {
        "plant": "Apple",
        "disease": "Healthy Leaf",
        "status": "Healthy",
        "severity": "None",
        "pathogen": "None (Plant is healthy)",
        "description": "The apple foliage displays uniform vibrant green pigmentation, smooth venation, and no signs of bacterial or fungal infection.",
        "symptoms": [
            "Firm, vibrant green leaf cuticle.",
            "Unblemished surface with no lesions, pustules, or chlorosis.",
            "Healthy vascular structure and natural turgidity."
        ],
        "organic_treatment": [
            "Maintain standard balanced organic compost and mulch for moisture retention."
        ],
        "chemical_treatment": [
            "No chemical treatment required."
        ],
        "prevention": [
            "Continue periodic scouting and maintain annual balanced fertilization (N-P-K)."
        ]
    },
    "Corn___Common_rust": {
        "plant": "Corn",
        "disease": "Common Rust",
        "status": "Diseased",
        "severity": "Moderate",
        "pathogen": "Puccinia sorghi (Fungus)",
        "description": "Common rust is prevalent in sweet and field corn during moderate temperatures (16–25°C) and high humidity. It produces powdery brown-to-cinnamon pustules across leaf surfaces.",
        "symptoms": [
            "Oval to elongated golden-brown or cinnamon pustules on both upper and lower leaf surfaces.",
            "Pustules rupture epidermal tissue, releasing powdery urediniospores.",
            "Severe infections cause chlorosis, premature senescence, and reduced kernel fill."
        ],
        "organic_treatment": [
            "Apply sulfur-based fungicidal dusts or sprays early in the infection cycle.",
            "Apply compost tea rich in beneficial antagonistic bacteria."
        ],
        "chemical_treatment": [
            "Foliar fungicides such as Pyraclostrobin, Azoxystrobin, or Propiconazole applied before blister stage."
        ],
        "prevention": [
            "Plant resistant corn hybrids carrying Rp gene resistance.",
            "Ensure proper field drainage and crop rotation with non-host crops."
        ]
    },
    "Corn___Northern_Leaf_Blight": {
        "plant": "Corn",
        "disease": "Northern Corn Leaf Blight",
        "status": "Diseased",
        "severity": "High",
        "pathogen": "Exserohilum turcicum (Fungus)",
        "description": "A destructive fungal blight characterized by long, cigar-shaped grayish-green lesions that turn necrotic, significantly diminishing photosynthetic capacity.",
        "symptoms": [
            "Long (2.5 to 15 cm) elliptical or cigar-shaped lesions on lower leaves progressing upwards.",
            "Lesions transition from pale gray-green to tan and necrotic.",
            "Dark sporulation within lesion centers during humid mornings."
        ],
        "organic_treatment": [
            "Deep tillage of infected residue post-harvest to promote fungal decomposition.",
            "Bacillus subtilis applications at early vegetative stages."
        ],
        "chemical_treatment": [
            "Strobilurin and triazole fungicide mixtures (e.g., Trifloxystrobin + Prothioconazole)."
        ],
        "prevention": [
            "Utilize resistant hybrids with single-gene (Ht) or polygenic resistance.",
            "Rotate fields with legumes or non-cereal crops every 2 seasons."
        ]
    },
    "Corn___healthy": {
        "plant": "Corn",
        "disease": "Healthy Leaf",
        "status": "Healthy",
        "severity": "None",
        "pathogen": "None (Plant is healthy)",
        "description": "Corn leaves exhibit robust parallel venation, deep green chlorophyll coloration, and absence of blight or rust pustules.",
        "symptoms": [
            "Consistent emerald-green coloration.",
            "Intact leaf margins and absence of leaf spotting.",
            "Strong turgor pressure and uniform leaf blade."
        ],
        "organic_treatment": [
            "Maintain optimal soil moisture and organic nitrogen levels."
        ],
        "chemical_treatment": [
            "No chemical intervention needed."
        ],
        "prevention": [
            "Ensure adequate spacing and soil aerification."
        ]
    },
    "Grape___Black_rot": {
        "plant": "Grape",
        "disease": "Black Rot",
        "status": "Diseased",
        "severity": "High",
        "pathogen": "Guignardia bidwellii (Fungus)",
        "description": "Black rot is one of the most destructive diseases of cultivated grapes in warm humid climates, attacking leaves, shoots, tendrils, and berries.",
        "symptoms": [
            "Small circular reddish-brown leaf spots with dark margins.",
            "Black pinhead fruiting bodies (pycnidia) arranged in rings inside lesions.",
            "Infected grape berries shrivel into hard, black, wrinkled mummies."
        ],
        "organic_treatment": [
            "Copper hydroxide or Bordeaux mixture applied before bloom.",
            "Remove and incinerate all infected vine trimmings and mummified clusters."
        ],
        "chemical_treatment": [
            "Mancozeb, Ziram, or Myclobutanil fungicides applied from early bud break through verasion."
        ],
        "prevention": [
            "Trellis vines to ensure maximum air flow and canopy sun exposure.",
            "Cultivate beneath grape rows to bury overwintering mummies."
        ]
    },
    "Grape___healthy": {
        "plant": "Grape",
        "disease": "Healthy Leaf",
        "status": "Healthy",
        "severity": "None",
        "pathogen": "None (Plant is healthy)",
        "description": "Healthy palmate grape leaf with clear veins, no necrosis or fungal pycnidia, and optimal photosynthetic health.",
        "symptoms": [
            "Clean palmate lobes with sharp serrations.",
            "Uniform leaf coloration without chlorotic blotches.",
            "Supple foliage free of powdery or fungal residues."
        ],
        "organic_treatment": [
            "Continue standard vineyard canopy maintenance."
        ],
        "chemical_treatment": [
            "None required."
        ],
        "prevention": [
            "Maintain proper canopy balance and regular scouting."
        ]
    },
    "Potato___Early_blight": {
        "plant": "Potato",
        "disease": "Early Blight",
        "status": "Diseased",
        "severity": "Moderate to High",
        "pathogen": "Alternaria solani (Fungus)",
        "description": "Early blight is a common disease affecting potatoes and tomatoes, manifesting as distinctive dark, target-board concentric ring lesions on older leaves.",
        "symptoms": [
            "Target-board concentric rings inside dark brown circular spots.",
            "Yellow chlorotic halos surrounding lesions.",
            "Older lower leaves infected first, gradually progressing upwards.",
            "Premature defoliation resulting in reduced tuber yields."
        ],
        "organic_treatment": [
            "Apply copper-based fungicides (Bordeaux mixture or copper octanoate).",
            "Spray potassium bicarbonate or neem oil on initial lesion detection.",
            "Apply heavy mulch to prevent fungal soil spores splashing onto lower foliage."
        ],
        "chemical_treatment": [
            "Chlorothalonil, Mancozeb, or Difenoconazole protective foliar sprays."
        ],
        "prevention": [
            "Practice minimum 3-year crop rotation avoiding solanaceous crops (tomatoes, peppers, eggplants).",
            "Maintain adequate plant nutrition, especially potassium and nitrogen balance.",
            "Use drip irrigation rather than overhead sprinklers."
        ]
    },
    "Potato___Late_blight": {
        "plant": "Potato",
        "disease": "Late Blight",
        "status": "Diseased",
        "severity": "Severe / Critical",
        "pathogen": "Phytophthora infestans (Oomycete)",
        "description": "Late blight is the infamous water mold responsible for the Irish Potato Famine. It spreads with devastating rapidity during cool, wet weather, destroying foliage and tubers in days.",
        "symptoms": [
            "Water-soaked dark green to purplish-black lesions expanding rapidly across foliage.",
            "Delicate white cottony mildew growth on leaf undersides in high humidity.",
            "Foul rotting odor from rapidly decaying foliage.",
            "Tuber rot with brownish-red dry or wet decay beneath skin."
        ],
        "organic_treatment": [
            "Immediate copper fungicide application at preventive schedule.",
            "Destroy and bury severely infected potato vines immediately; do not compost."
        ],
        "chemical_treatment": [
            "Systemic oomycete-targeted fungicides: Metalaxyl, Cymoxanil, Mandipropamid, or Fluopicolide."
        ],
        "prevention": [
            "Plant certified disease-free seed tubers.",
            "Destroy all volunteer potato plants and cull piles.",
            "Hill soil deeply around tubers to prevent zoospore wash-in."
        ]
    },
    "Potato___healthy": {
        "plant": "Potato",
        "disease": "Healthy Leaf",
        "status": "Healthy",
        "severity": "None",
        "pathogen": "None (Plant is healthy)",
        "description": "Pinnately compound potato leaves displaying vigorous vegetative health, clean dark green leaflets, and no water-soaking or necrotic lesions.",
        "symptoms": [
            "Rich deep green leaflet surface.",
            "No necrotic spots, target rings, or mildew.",
            "Healthy apical growth and robust petioles."
        ],
        "organic_treatment": [
            "Maintain balanced watering and organic fertilization."
        ],
        "chemical_treatment": [
            "No treatment necessary."
        ],
        "prevention": [
            "Keep soil well-drained and maintain preventative pest scouting."
        ]
    },
    "Tomato___Early_blight": {
        "plant": "Tomato",
        "disease": "Early Blight",
        "status": "Diseased",
        "severity": "Moderate",
        "pathogen": "Alternaria solani (Fungus)",
        "description": "Early blight is one of the most ubiquitous tomato foliar diseases. It produces classic brown target-like concentric rings on lower leaves, causing severe defoliation and sunscald on fruit.",
        "symptoms": [
            "Concentric rings forming a target pattern inside brown necrotic spots.",
            "Yellowing (chlorosis) of surrounding leaf tissue.",
            "Lower leaves dry up, turn brown, and drop prematurely.",
            "Dark, sunken stem lesions near the soil line (collar rot in seedlings)."
        ],
        "organic_treatment": [
            "Apply liquid copper fungicide or Serenade (Bacillus subtilis) every 7-10 days.",
            "Prune off lower foliage (bottom 30 cm) to stop soil splash.",
            "Apply straw or plastic mulch to isolate soil-borne spores."
        ],
        "chemical_treatment": [
            "Chlorothalonil, Azoxystrobin, or Mancozeb sprays applied at regular intervals."
        ],
        "prevention": [
            "Ensure 3-year solanaceous crop rotation.",
            "Stake and cage tomato plants to maintain upright aeration.",
            "Water only at ground level with soaker hoses."
        ]
    },
    "Tomato___Late_blight": {
        "plant": "Tomato",
        "disease": "Late Blight",
        "status": "Diseased",
        "severity": "Severe / Critical",
        "pathogen": "Phytophthora infestans (Oomycete)",
        "description": "Late blight can decimate entire tomato fields in 7–10 days during cool, humid conditions. It produces greasy dark lesions and causes green and ripe fruit to turn brown and rot.",
        "symptoms": [
            "Greasy, water-soaked dark gray-green spots enlarging rapidly into large brown patches.",
            "White fungal-like spore growth on the underside of leaves during damp mornings.",
            "Dark brown blotches on stems and fruit rot turning greasy and firm.",
            "Rapid collapse of entire plant canopy."
        ],
        "organic_treatment": [
            "Preventative copper sprays applied prior to rain events in cool weather.",
            "Bag and destroy infected plants immediately to prevent neighborhood epidemic spread."
        ],
        "chemical_treatment": [
            "Fungicides with systemic mobility: Propamocarb, Dimethomorph, or Famoxadone + Cymoxanil."
        ],
        "prevention": [
            "Select resistant cultivars such as Mountain Magic, Defiant, or Plum Regal.",
            "Avoid planting downwind of commercial potato fields.",
            "Do not allow leaves to remain wet for more than 4 consecutive hours."
        ]
    },
    "Tomato___healthy": {
        "plant": "Tomato",
        "disease": "Healthy Leaf",
        "status": "Healthy",
        "severity": "None",
        "pathogen": "None (Plant is healthy)",
        "description": "The tomato foliage demonstrates optimal physiological vitality, rich chlorophyll concentration, and absence of blight lesions or mold.",
        "symptoms": [
            "Bright, deep green lobed leaflets with fine glandular trichomes (hairs).",
            "Smooth surfaces free of yellowing, spots, or curled margins.",
            "Strong turgidity and aromatic foliage characteristic of healthy Solanum lycopersicum."
        ],
        "organic_treatment": [
            "Continue routine organic compost tea feeding and side-dressing."
        ],
        "chemical_treatment": [
            "None needed."
        ],
        "prevention": [
            "Maintain consistent drip irrigation, proper staking, and weed control."
        ]
    }
}


def get_disease_details(raw_class_name):
    """
    Retrieve formatted disease and agronomic management information
    for a given class name. Provides a graceful fallback for unmapped classes.
    """
    if raw_class_name in DISEASE_KNOWLEDGE_BASE:
        return DISEASE_KNOWLEDGE_BASE[raw_class_name]

    # Dynamic fallback parser
    if "___" in raw_class_name:
        plant, disease = raw_class_name.split("___", 1)
        disease_clean = disease.replace("_", " ")
    else:
        plant = "Plant"
        disease_clean = raw_class_name.replace("_", " ")

    is_healthy = "healthy" in disease_clean.lower()
    status = "Healthy" if is_healthy else "Diseased"

    return {
        "plant": plant,
        "disease": disease_clean,
        "status": status,
        "severity": "None" if is_healthy else "Moderate",
        "pathogen": "None" if is_healthy else "Fungal/Bacterial pathogen",
        "description": f"Classification result indicates {disease_clean} in {plant} foliage.",
        "symptoms": [
            "Foliage characteristics consistent with identified class."
        ],
        "organic_treatment": [
            "Maintain clean foliage and consider organic bio-fungicides or neem oil if symptoms appear."
        ],
        "chemical_treatment": [
            "Consult local agricultural extension service for targeted treatments."
        ],
        "prevention": [
            "Ensure adequate spacing, morning irrigation, and sanitization of garden tools."
        ]
    }

