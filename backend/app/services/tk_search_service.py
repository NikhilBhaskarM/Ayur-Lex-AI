import structlog
from typing import Optional, List, Dict, Any
from app.schemas.tk_search import (
    TKSearchRequest, TKSearchResponse, HerbPriorArtResult,
    ClassicalTreatiseCitation, KnownPriorArtCase
)
from app.rag.keyword_search import KeywordSearcher
from app.rag.vector_search import VectorStore
from app.rag.retriever import HybridRetriever

logger = structlog.get_logger(__name__)

HERB_PRIOR_ART_DATABASE = [
    HerbPriorArtResult(
        herb_name="Turmeric",
        sanskrit_name="Haridra / Nisha",
        botanical_name="Curcuma longa L.",
        family="Zingiberaceae",
        tkrc_class="A61K 36/9066 (Zingiberaceae medicinal preparations)",
        classical_treatises=[
            ClassicalTreatiseCitation(
                treatise="Charaka Samhita",
                verse_or_chapter="Sutra Sthana Ch. 4 (Kushthaghna Mahakashaya)",
                indications=["Vranaropana (wound healing)", "Kushthaghna (skin diseases)", "Vishaghna (anti-toxic)", "Prameha (diabetes/metabolic)"],
                sanskrit_sloka="हरिद्रा कटुतिक्तोष्णा कफपित्तविनाशिनी । त्वग्दोषहन्त्री प्रमेहाणां नाशिनी व्रणरोपणी ॥"
            ),
            ClassicalTreatiseCitation(
                treatise="Sushruta Samhita",
                verse_or_chapter="Sutra Sthana Ch. 38 (Haridradi Gana)",
                indications=["Vranashodhana (wound cleansing)", "Stanya shuddhi (breast milk purification)"]
            ),
            ClassicalTreatiseCitation(
                treatise="Ayurvedic Formulary of India (AFI)",
                verse_or_chapter="Part I, Haridra Khanda",
                indications=["Sheetapitta (urticaria)", "Kandu (pruritus)", "Allergic dermatitis"]
            )
        ],
        famous_revocation_case=KnownPriorArtCase(
            patent_number="US 5,401,504",
            patent_office="USPTO (United States Patent and Trademark Office)",
            applicant="University of Mississippi Medical Center",
            disputed_claims="Use of turmeric in powder form to promote wound healing.",
            outcome="REVOKED completely in 1997 following formal re-examination initiated by CSIR India.",
            key_prior_art_cited="Classical 18th-century Ayurvedic treatises and 1953 Indian Medical Association Journal paper establishing centuries of traditional public use."
        ),
        section_3p_rejection_risk="CRITICAL (Near 100%) for direct wound healing, anti-inflammatory, or topical antibacterial claims without demonstrated synergistic novelty.",
        defensive_search_guidance="Search TKDL database under class A61K 36/9066. Must combine with novel delivery vehicles (e.g. lipid nanoparticles) or demonstrate non-obvious synergistic bioavailability (CI < 1.0) with piperine."
    ),
    HerbPriorArtResult(
        herb_name="Neem",
        sanskrit_name="Nimba / Arishta",
        botanical_name="Azadirachta indica A. Juss.",
        family="Meliaceae",
        tkrc_class="A61K 36/58 (Meliaceae medicinal preparations)",
        classical_treatises=[
            ClassicalTreatiseCitation(
                treatise="Charaka Samhita",
                verse_or_chapter="Sutra Sthana Ch. 27 & Chikitsa Sthana Ch. 7",
                indications=["Krimighna (anthelminthic/antimicrobial)", "Kandughna (anti-pruritic)", "Kushthahara (dermatological therapeutics)"]
            ),
            ClassicalTreatiseCitation(
                treatise="Sushruta Samhita",
                verse_or_chapter="Sutra Sthana Ch. 45",
                indications=["Vranashodhana (wound sterilizing)", "Jwarahara (febrifuge)"]
            )
        ],
        famous_revocation_case=KnownPriorArtCase(
            patent_number="EP 0436257",
            patent_office="EPO (European Patent Office)",
            applicant="W.R. Grace & Co. / USDA",
            disputed_claims="Fungicidal method utilizing hydrophobic extracted neem seed oil.",
            outcome="REVOKED in 2000 (upheld on appeal in 2005) after 10-year legal battle by Indian NGOs & Ministry of Ayush.",
            key_prior_art_cited="Ancient Ayurvedic farming practices and Sanskrit prior art establishing known antifungal property of neem extracts."
        ),
        section_3p_rejection_risk="CRITICAL for pest control, antifungal, or antibacterial formulations unless standardized synthetic derivatives or unexpected synergistic mixtures are proven.",
        defensive_search_guidance="Search InPASS under IPC A01N 65/26 and TKDL A61K 36/58."
    ),
    HerbPriorArtResult(
        herb_name="Ashwagandha",
        sanskrit_name="Ashwagandha / Hayagandha",
        botanical_name="Withania somnifera (L.) Dunal",
        family="Solanaceae",
        tkrc_class="A61K 36/81 (Solanaceae medicinal preparations)",
        classical_treatises=[
            ClassicalTreatiseCitation(
                treatise="Charaka Samhita",
                verse_or_chapter="Chikitsa Sthana Ch. 1 (Rasayana Adhyaya)",
                indications=["Balya (strength promoter)", "Rasayana (rejuvenator)", "Shukrala (spermatogenic)", "Nidrajanana (adaptogenic/sleep)"]
            ),
            ClassicalTreatiseCitation(
                treatise="Bhavaprakasha Nighantu",
                verse_or_chapter="Guduchyadi Varga, Verse 189-190",
                indications=["Vatakaphahara (balancer of Vata-Kapha)", "Kshayahara (anti-wasting)"]
            )
        ],
        famous_revocation_case=KnownPriorArtCase(
            patent_number="Multiple USPTO & EPO Filings",
            patent_office="USPTO & EPO",
            applicant="Various multinational pharmaceutical applicants",
            disputed_claims="Cognitive enhancement and adaptogenic stress reduction using withanolides.",
            outcome="Repeatedly rejected or forced to narrow claims to specific withanolide-A/withaferin-A chromatographic ratios.",
            key_prior_art_cited="TKDL defensive evidence citations showing classical Medhya Rasayana (nootropic adaptogen) documentation."
        ),
        section_3p_rejection_risk="VERY HIGH for general adaptogen, anti-stress, or vitality claims. Requires Section 3(d) enhancement of efficacy proof over standardized crude root powder.",
        defensive_search_guidance="Any crude extract patent claim will face Section 3(p) objections. Focus on patented extraction processes or standardized withanolide profiles with unexpected neuroprotective synergy."
    ),
    HerbPriorArtResult(
        herb_name="Guggulu",
        sanskrit_name="Guggulu / Kaushika",
        botanical_name="Commiphora mukul (Stocks) Hook. / C. wightii",
        family="Burseraceae",
        tkrc_class="A61K 36/328 (Burseraceae medicinal preparations)",
        classical_treatises=[
            ClassicalTreatiseCitation(
                treatise="Sushruta Samhita",
                verse_or_chapter="Sutra Sthana Ch. 15",
                indications=["Medoroga (anti-obesity/anti-hyperlipidemic)", "Vatarakta (gout/inflammatory arthritis)", "Bhagna sandhana (bone fracture healing)"]
            ),
            ClassicalTreatiseCitation(
                treatise="Ayurvedic Pharmacopoeia of India (API)",
                verse_or_chapter="Part I, Vol. I",
                indications=["Sandhivata (osteoarthritis)", "Medovriddhi (dyslipidemia)"]
            )
        ],
        famous_revocation_case=KnownPriorArtCase(
            patent_number="US 6,086,889",
            patent_office="USPTO",
            applicant="Sabinsa Corporation",
            disputed_claims="Method of reducing lipid levels with guggulsterones.",
            outcome="Narrowed strictly to specific synthetic ester derivatives following CSIR prior art submission.",
            key_prior_art_cited="Sushruta Samhita references on Medohara action of purified Commiphora gum resin."
        ),
        section_3p_rejection_risk="HIGH for anti-inflammatory, lipid-lowering, or joint health indications.",
        defensive_search_guidance="Direct claims to guggulsterones E and Z are heavily anticipated. Must demonstrate unexpected formulation stabilization or pharmacokinetic enhancement."
    ),
    HerbPriorArtResult(
        herb_name="Tulsi",
        sanskrit_name="Tulasi / Surasa",
        botanical_name="Ocimum sanctum L. / Ocimum tenuiflorum",
        family="Lamiaceae",
        tkrc_class="A61K 36/53 (Lamiaceae medicinal preparations)",
        classical_treatises=[
            ClassicalTreatiseCitation(
                treatise="Charaka Samhita",
                verse_or_chapter="Sutra Sthana Ch. 27 & Chikitsa Sthana Ch. 18",
                indications=["Kasa (cough)", "Shwasa (asthma/bronchial spasms)", "Hikka (hiccough)", "Vranadoshahara (antimicrobial)"]
            ),
            ClassicalTreatiseCitation(
                treatise="Bhavaprakasha Nighantu",
                verse_or_chapter="Pushpa Varga",
                indications=["Deepana (digestive stimulant)", "Krimighna (antimicrobial)"]
            )
        ],
        famous_revocation_case=None,
        section_3p_rejection_risk="VERY HIGH for respiratory, immune-modulating, and antimicrobial teas or extracts.",
        defensive_search_guidance="Prior art is extensively documented in TKDL. Eugenol and rosmarinic acid standardizations require novel delivery carriers."
    ),
    HerbPriorArtResult(
        herb_name="Brahmi",
        sanskrit_name="Brahmi / Mandukaparni",
        botanical_name="Bacopa monnieri (L.) Wettst. / Centella asiatica",
        family="Plantaginaceae / Apiaceae",
        tkrc_class="A61K 36/68 (Plantaginaceae) & A61K 36/23 (Apiaceae)",
        classical_treatises=[
            ClassicalTreatiseCitation(
                treatise="Charaka Samhita",
                verse_or_chapter="Sutra Sthana Ch. 4 (Prajasthapana Mahakashaya) & Chikitsa Sthana Ch. 1",
                indications=["Medhya (memory/cognitive enhancer)", "Ayushya (longevity promoter)", "Apasmara (anti-epileptic)", "Unmada (psychiatric disorders)"]
            )
        ],
        famous_revocation_case=None,
        section_3p_rejection_risk="HIGH for memory, ADHD, or neuroprotective claims.",
        defensive_search_guidance="Bacoside-A and Bacoside-B fractions are codified in AFI and API. Patent claims must present quantitative cognitive enhancement synergy."
    ),
    HerbPriorArtResult(
        herb_name="Giloy",
        sanskrit_name="Guduchi / Amrita",
        botanical_name="Tinospora cordifolia (Willd.) Miers",
        family="Menispermaceae",
        tkrc_class="A61K 36/59 (Menispermaceae medicinal preparations)",
        classical_treatises=[
            ClassicalTreatiseCitation(
                treatise="Charaka Samhita",
                verse_or_chapter="Sutra Sthana Ch. 4 (Vayasthapana & Triptighna Mahakashaya)",
                indications=["Jwarahara (antipyretic)", "Rasayana (immunomodulator)", "Deepana (digestive)", "Kamala (hepatoprotective)"]
            )
        ],
        famous_revocation_case=None,
        section_3p_rejection_risk="CRITICAL for immunomodulatory, anti-fever, or hepatoprotective extracts.",
        defensive_search_guidance="Heavily cited by Indian Patent Office in examination reports during Covid-19 patent applications."
    )
]

class TKSearchService:
    def __init__(self):
        self.vector_store = VectorStore()
        self.keyword_searcher = KeywordSearcher()
        self.retriever = HybridRetriever(self.vector_store, self.keyword_searcher)

    async def search(self, request: TKSearchRequest) -> TKSearchResponse:
        logger.info("Executing Traditional Knowledge search", query=request.query)
        
        search_terms = (request.query or "") + " " + (request.herb_name or "") + " " + (request.therapeutic_claim or "")
        search_lower = search_terms.lower()
        
        # 1. Classical Pharmacopoeia Herb Matching
        matched_herbs: List[HerbPriorArtResult] = []
        for herb in HERB_PRIOR_ART_DATABASE:
            if (
                herb.herb_name.lower() in search_lower or
                herb.sanskrit_name.lower() in search_lower or
                herb.botanical_name.lower() in search_lower or
                any(any(ind.lower() in search_lower for ind in c.indications) for c in herb.classical_treatises)
            ):
                matched_herbs.append(herb)

        # 2. Hybrid RAG Search across statutory knowledge & database chunks
        retrieved_provisions = []
        try:
            chunks = await self.retriever.retrieve(
                query=search_terms,
                jurisdiction=request.jurisdiction or "India",
                filters={"topics": ["traditional_knowledge", "patents", "prior_art"]},
                top_k=request.top_k
            )
            for c in chunks[:5]:
                retrieved_provisions.append({
                    "chunk_id": c.chunk_id,
                    "content": c.content,
                    "score": round(c.score, 4),
                    "source_title": c.metadata.get("source_title", "Statutory Corpus"),
                    "section": c.metadata.get("section", ""),
                    "portal_url": c.metadata.get("portal_url", "")
                })
        except Exception as e:
            logger.warning("RAG retrieval failed during TK search", error=str(e))

        defensive_advice = (
            "Any Ayurvedic patent application must be defensively vetted against TKDL prior art. "
            "Under Section 3(p) of the Patents Act, claims will be rejected if the medicinal utility of the components "
            "is documented in classical treatises (Charaka Samhita, Sushruta Samhita, AFI). "
            "To succeed, polyherbal applications MUST establish non-obvious synergistic therapeutic efficacy (CI < 1.0) "
            "supported by empirical quantitative laboratory data."
        )

        return TKSearchResponse(
            query=request.query,
            matched_herbs=matched_herbs,
            rag_retrieved_provisions=retrieved_provisions,
            total_matches=len(matched_herbs),
            defensive_advice=defensive_advice
        )
