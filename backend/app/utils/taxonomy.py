"""
Botanical & Ayurvedic Taxonomy Engine
Connects classical Sanskrit Ayurvedic botanical nomenclature with Latin binomials,
botanical families, common English designations, and key bioactive chemical markers.
"""

from typing import Dict, Any, Optional, List
import re

# Comprehensive taxonomy database linking Sanskrit vernacular to Latin binomials
AYURVEDIC_TAXONOMY: Dict[str, Dict[str, Any]] = {
    "ashwagandha": {
        "sanskrit_name": "Ashwagandha",
        "latin_binomial": "Withania somnifera",
        "family": "Solanaceae",
        "common_name": "Indian Ginseng / Winter Cherry",
        "vernacular_synonyms": ["asgandh", "hayagandha", "vajigandha"],
        "parts_used": ["Roots", "Leaves"],
        "active_markers": ["Withaferin A", "Withanolide A", "Withanolide D", "Withanone"],
        "api_monograph_ref": "API Part I, Vol I, Page 15",
        "tkdl_citation": "TKDL Formulation Key: RS/1024, JA/452",
        "classical_texts": ["Charaka Samhita (Chikitsa Sthana 1.1)", "Bhavaprakasha Nighantu"]
    },
    "guduchi": {
        "sanskrit_name": "Guduchi",
        "latin_binomial": "Tinospora cordifolia",
        "family": "Menispermaceae",
        "common_name": "Heart-leaved Moonseed / Giloy",
        "vernacular_synonyms": ["giloy", "amrita", "chinnaruha", "gurcha"],
        "parts_used": ["Stem"],
        "active_markers": ["Tinosporoside", "Cordifolioside A", "Berberine", "Magnoflorine"],
        "api_monograph_ref": "API Part I, Vol I, Page 41",
        "tkdl_citation": "TKDL Formulation Key: MH1/123, AM/214",
        "classical_texts": ["Charaka Samhita (Sutra Sthana 4)", "Sushruta Samhita"]
    },
    "haridra": {
        "sanskrit_name": "Haridra",
        "latin_binomial": "Curcuma longa",
        "family": "Zingiberaceae",
        "common_name": "Turmeric / Indian Saffron",
        "vernacular_synonyms": ["haldi", "nisha", "rajani", "gauri"],
        "parts_used": ["Rhizome"],
        "active_markers": ["Curcumin", "Demethoxycurcumin", "Bisdemethoxycurcumin", "Turmerones"],
        "api_monograph_ref": "API Part I, Vol I, Page 45",
        "tkdl_citation": "TKDL Formulation Key: HA/01, BP/98",
        "classical_texts": ["Charaka Samhita", "Sushruta Samhita", "Ashtanga Hridaya"]
    },
    "pippali": {
        "sanskrit_name": "Pippali",
        "latin_binomial": "Piper longum",
        "family": "Piperaceae",
        "common_name": "Indian Long Pepper",
        "vernacular_synonyms": ["magadhi", "krishna", "chapa"],
        "parts_used": ["Dried fruit / Root"],
        "active_markers": ["Piperine", "Piperlongumine", "Piperlonguminine", "Sylvatin"],
        "api_monograph_ref": "API Part I, Vol IV, Page 91",
        "tkdl_citation": "TKDL Formulation Key: PL/44, Trikatu component",
        "classical_texts": ["Charaka Samhita (Trikatu yoga)", "Sushruta Samhita"]
    },
    "maricha": {
        "sanskrit_name": "Maricha",
        "latin_binomial": "Piper nigrum",
        "family": "Piperaceae",
        "common_name": "Black Pepper",
        "vernacular_synonyms": ["kali mirch", "vellaja", "krishna"],
        "parts_used": ["Dried fruit"],
        "active_markers": ["Piperine", "Chavicine", "Piperidine"],
        "api_monograph_ref": "API Part I, Vol III, Page 115",
        "tkdl_citation": "TKDL Formulation Key: MN/88, Trikatu component",
        "classical_texts": ["Charaka Samhita", "Ashtanga Sangraha"]
    },
    "shunti": {
        "sanskrit_name": "Shunti",
        "latin_binomial": "Zingiber officinale",
        "family": "Zingiberaceae",
        "common_name": "Ginger / Dry Ginger",
        "vernacular_synonyms": ["sonth", "adrak", "vishwabhesaj", "nagar"],
        "parts_used": ["Rhizome"],
        "active_markers": ["6-Gingerol", "6-Shogaol", "8-Gingerol", "Zingiberene"],
        "api_monograph_ref": "API Part I, Vol I, Page 103",
        "tkdl_citation": "TKDL Formulation Key: ZO/12, Trikatu component",
        "classical_texts": ["Charaka Samhita", "Sushruta Samhita"]
    },
    "amalaki": {
        "sanskrit_name": "Amalaki",
        "latin_binomial": "Phyllanthus emblica",
        "family": "Phyllanthaceae",
        "common_name": "Indian Gooseberry / Amla",
        "vernacular_synonyms": ["amla", "dhatri", "vayastha", "amritaphala"],
        "parts_used": ["Pericarp / Dried fruit"],
        "active_markers": ["Ascorbic acid", "Gallic acid", "Ellagic acid", "Emblicanin A & B"],
        "api_monograph_ref": "API Part I, Vol I, Page 4",
        "tkdl_citation": "TKDL Formulation Key: PE/99, Triphala component",
        "classical_texts": ["Charaka Samhita (Rasayana Adhyaya)", "Chyawanprash root text"]
    },
    "haritaki": {
        "sanskrit_name": "Haritaki",
        "latin_binomial": "Terminalia chebula",
        "family": "Combretaceae",
        "common_name": "Chebulic Myrobalan / Harad",
        "vernacular_synonyms": ["harad", "abhaya", "pathya", "shiva"],
        "parts_used": ["Pericarp of dried fruit"],
        "active_markers": ["Chebulic acid", "Chebulagic acid", "Corilagin", "Tannins"],
        "api_monograph_ref": "API Part I, Vol I, Page 47",
        "tkdl_citation": "TKDL Formulation Key: TC/72, Triphala component",
        "classical_texts": ["Charaka Samhita (Chikitsa 1.1)", "Sushruta Samhita"]
    },
    "bibhitaki": {
        "sanskrit_name": "Bibhitaki",
        "latin_binomial": "Terminalia bellirica",
        "family": "Combretaceae",
        "common_name": "Belleric Myrobalan / Baheda",
        "vernacular_synonyms": ["baheda", "vibheeta", "akshaphala"],
        "parts_used": ["Dried fruit pericarp"],
        "active_markers": ["Gallic acid", "Ellagic acid", "Belleric acid", "Chebulagic acid"],
        "api_monograph_ref": "API Part I, Vol I, Page 17",
        "tkdl_citation": "TKDL Formulation Key: TB/33, Triphala component",
        "classical_texts": ["Charaka Samhita", "Sushruta Samhita"]
    },
    "brahmi": {
        "sanskrit_name": "Brahmi",
        "latin_binomial": "Bacopa monnieri",
        "family": "Plantaginaceae",
        "common_name": "Water Hyssop",
        "vernacular_synonyms": ["jalnaveri", "medhya", "saraswati"],
        "parts_used": ["Whole plant"],
        "active_markers": ["Bacoside A", "Bacoside B", "Bacopaside I & II"],
        "api_monograph_ref": "API Part I, Vol II, Page 25",
        "tkdl_citation": "TKDL Formulation Key: BM/501",
        "classical_texts": ["Charaka Samhita (Sutra 4 - Medhya Rasayana)", "Bhavaprakasha"]
    },
    "tulsi": {
        "sanskrit_name": "Tulsi",
        "latin_binomial": "Ocimum tenuiflorum",
        "family": "Lamiaceae",
        "common_name": "Holy Basil",
        "vernacular_synonyms": ["vrinda", "surasa", "manjari"],
        "parts_used": ["Leaves", "Seeds"],
        "active_markers": ["Eugenol", "Ursolic acid", "Rosmarinic acid", "Caryophyllene"],
        "api_monograph_ref": "API Part I, Vol II, Page 165",
        "tkdl_citation": "TKDL Formulation Key: OT/77",
        "classical_texts": ["Sushruta Samhita", "Dhanvantari Nighantu"]
    },
    "neem": {
        "sanskrit_name": "Nimba",
        "latin_binomial": "Azadirachta indica",
        "family": "Meliaceae",
        "common_name": "Neem / Indian Lilac",
        "vernacular_synonyms": ["neem", "pichumarda", "arishta"],
        "parts_used": ["Leaves", "Bark", "Seeds"],
        "active_markers": ["Azadirachtin", "Nimbin", "Nimbidin", "Salannin"],
        "api_monograph_ref": "API Part I, Vol II, Page 129",
        "tkdl_citation": "TKDL Formulation Key: AI/009 (EPO Neem Patent Revocation landmark)",
        "classical_texts": ["Charaka Samhita", "Sushruta Samhita"]
    },
    "shatavari": {
        "sanskrit_name": "Shatavari",
        "latin_binomial": "Asparagus racemosus",
        "family": "Asparagaceae",
        "common_name": "Wild Asparagus",
        "vernacular_synonyms": ["satavar", "bahuputri", "atirasa"],
        "parts_used": ["Tuberous roots"],
        "active_markers": ["Shatavarin I-IV", "Sarsasapogenin", "Isoflavones"],
        "api_monograph_ref": "API Part I, Vol IV, Page 108",
        "tkdl_citation": "TKDL Formulation Key: AR/321",
        "classical_texts": ["Charaka Samhita", "Ashtanga Hridaya"]
    },
    "guggulu": {
        "sanskrit_name": "Guggulu",
        "latin_binomial": "Commiphora mukul",
        "family": "Burseraceae",
        "common_name": "Indian Bdellium",
        "vernacular_synonyms": ["guggal", "puram", "kaushika"],
        "parts_used": ["Exudate / Oleo-gum-resin"],
        "active_markers": ["E-Guggulsterone", "Z-Guggulsterone", "Mukulol"],
        "api_monograph_ref": "API Part I, Vol I, Page 43",
        "tkdl_citation": "TKDL Formulation Key: CM/81",
        "classical_texts": ["Sushruta Samhita (Medoroga Chikitsa)", "Bhavaprakasha"]
    },
    "kalamegha": {
        "sanskrit_name": "Kalamegha",
        "latin_binomial": "Andrographis paniculata",
        "family": "Acanthaceae",
        "common_name": "King of Bitters / Kiryat",
        "vernacular_synonyms": ["kiryat", "bhu-nimba", "yavatikta"],
        "parts_used": ["Aerial parts"],
        "active_markers": ["Andrographolide", "Neoandrographolide", "14-Deoxyandrographolide"],
        "api_monograph_ref": "API Part I, Vol II, Page 78",
        "tkdl_citation": "TKDL Formulation Key: AP/412",
        "classical_texts": ["Bhavaprakasha Nighantu", "Raja Nighantu"]
    },
    "yashtimadhu": {
        "sanskrit_name": "Yashtimadhu",
        "latin_binomial": "Glycyrrhiza glabra",
        "family": "Fabaceae",
        "common_name": "Licorice / Mulethi",
        "vernacular_synonyms": ["mulethi", "madhuka", "jalayashti"],
        "parts_used": ["Roots / Stolons"],
        "active_markers": ["Glycyrrhizin", "Glabridin", "Liquiritin", "Isoliquiritigenin"],
        "api_monograph_ref": "API Part I, Vol I, Page 113",
        "tkdl_citation": "TKDL Formulation Key: GG/65",
        "classical_texts": ["Charaka Samhita", "Sushruta Samhita"]
    }
}


def lookup_herb(query: str) -> Optional[Dict[str, Any]]:
    """
    Looks up botanical metadata from Sanskrit, Hindi, vernacular, or Latin name.
    """
    q_norm = query.strip().lower()
    
    # Direct Sanskrit match
    if q_norm in AYURVEDIC_TAXONOMY:
        return AYURVEDIC_TAXONOMY[q_norm]
    
    # Match against synonyms, Latin binomials, or vernacular terms
    for herb_key, data in AYURVEDIC_TAXONOMY.items():
        if q_norm == data["latin_binomial"].lower():
            return data
        if q_norm in [s.lower() for s in data["vernacular_synonyms"]]:
            return data
        if q_norm in data["common_name"].lower():
            return data
            
    return None


def enrich_query_with_taxonomy(user_text: str) -> str:
    """
    Scans a free-text legal question and annotates Ayurvedic terms with
    their formal Latin binomials and family identifiers for patent clarity.
    """
    enriched_text = user_text
    words = re.findall(r'\b[A-Za-z\-]+\b', user_text)
    
    seen_herbs = set()
    for word in words:
        herb_data = lookup_herb(word)
        if herb_data and herb_data["sanskrit_name"] not in seen_herbs:
            seen_herbs.add(herb_data["sanskrit_name"])
            pattern = re.compile(rf'\b{re.escape(word)}\b', re.IGNORECASE)
            replacement = f"{word} (botanical source: {herb_data['latin_binomial']}, Family: {herb_data['family']})"
            enriched_text = pattern.sub(replacement, enriched_text, count=1)
            
    return enriched_text


def generate_standardized_claim_terms(herbs: List[str]) -> List[Dict[str, Any]]:
    """
    Transforms informal herb names into precise patent specification claim language.
    """
    standardized = []
    for h in herbs:
        meta = lookup_herb(h)
        if meta:
            standardized.append({
                "input_term": h,
                "botanical_species": meta["latin_binomial"],
                "family": meta["family"],
                "active_markers": meta["active_markers"],
                "recommended_claim_clause": (
                    f"a standardized extract of {meta['latin_binomial']} ({meta['family']}) "
                    f"characterized by a quantified content of {meta['active_markers'][0]}"
                ),
                "tkdl_prior_art_reference": meta["tkdl_citation"],
                "api_reference": meta["api_monograph_ref"]
            })
        else:
            standardized.append({
                "input_term": h,
                "botanical_species": "Unknown Botanical Entity",
                "family": "Unspecified",
                "active_markers": [],
                "recommended_claim_clause": f"a biological extract of {h}",
                "tkdl_prior_art_reference": "N/A",
                "api_reference": "Unlisted"
            })
    return standardized
