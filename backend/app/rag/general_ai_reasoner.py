"""
Ayurvedic IPR & Regulatory AI Assistant — General AI & Conversational Reasoner

Provides rich, articulate, educational, and conversational responses for:
- Greetings & Meta inquiries ("Hello", "Who are you?", "What can you do?")
- Ayurvedic Philosophy & Historical Treatises (Charaka, Sushruta, Shodhana, Rasa Shastra)
- Intellectual Property Fundamentals (Patents vs Trademarks vs Copyrights vs Trade Secrets vs GIs)
- Biopiracy History & Landmark Cases (Turmeric, Neem, Basmati, CSIR revocations, TKDL birth)
- Regulatory Landscape (Ministry of Ayush vs CDSCO vs FSSAI, Schedule T GMP, Schedule E(1))
- International Frameworks (Nagoya Protocol, TRIPS Agreement, WIPO GRATK Treaty 2024)
- Interactive Problem Onboarding & Probing Questions
"""

from typing import Optional, Tuple


class GeneralAIReasoner:
    """Conversational AI engine for general knowledge, IPR concepts, and interactive onboarding."""

    def is_general_query(self, query: str) -> bool:
        if "User Query:" in query:
            q_clean = query.split("User Query:", 1)[1].strip()
        else:
            q_clean = query
        q_lower = q_clean.lower().strip()
        
        # Greetings & Persona
        if any(q_lower == g or q_lower.startswith(g + " ") or q_lower.endswith(" " + g) for g in ["hello", "hi", "hey", "namaste", "good morning", "good afternoon", "good evening"]):
            return True
        if any(k in q_lower for k in ["who are you", "what are you", "what can you do", "help me", "introduce yourself", "how can you help"]):
            return True

        # Definitional queries: Patent, Prior Art, Invention
        if any(k in q_lower for k in ["what is a patent", "what is patent", "define patent", "patent definition", "what can be patented", "meaning of patent", "explain patent", "what is prior art", "prior art", "what is an invention", "meaning of prior art"]):
            return True

        # Ayurveda Concepts
        if any(k in q_lower for k in ["what is ayurveda", "history of ayurveda", "charaka samhita", "sushruta samhita", "ashtanga hridaya", "rasa shastra", "what is shodhana", "what is bhasma", "ayurvedic formulary of india"]):
            # If not asking specifically about licensing
            if not any(k in q_lower for k in ["license", "trademark", "rule 158"]):
                return True

        # IPR Fundamentals
        if any(k in q_lower for k in ["what is intellectual property", "what is ipr", "difference between patent and trademark", "difference between patent and copyright", "what is a copyright", "what is a trade secret", "what is a geographical indication", "types of ipr", "types of intellectual property"]):
            return True

        # Statutory Exclusions (§3(p), §3(e), §3(d), BDA)
        if any(k in q_lower for k in ["section 3(p)", "section 3p", "section 3 (p)", "section 3(e)", "section 3e", "section 3 (e)", "section 3(d)", "section 3d", "section 3 (d)", "tkdl", "traditional knowledge"]):
            return True
        if any(k in q_lower for k in ["biological diversity act", "bda form iii", "nba approval", "section 6 bda"]):
            return True

        # Biopiracy & Case Studies
        if any(k in q_lower for k in ["what is biopiracy", "examples of biopiracy", "turmeric patent", "neem patent", "basmati patent", "history of tkdl"]):
            return True

        # Regulatory Landscape
        if any(k in q_lower for k in ["what is ayush", "ministry of ayush", "cdsco vs ayush", "difference between medicine and cosmetic", "difference between food and medicine"]):
            return True

        # International Treaties
        if any(k in q_lower for k in ["what is nagoya protocol", "what is trips agreement", "what is wipo", "cbd and traditional knowledge"]):
            return True

        return False

    def synthesize_general_answer(self, query: str, conversation_history: Optional[list[dict]] = None) -> Tuple[str, list[str]]:
        """Synthesize answer with strict Ayur-Lex-AI domain framing and return (answer_markdown, clarification_questions)."""
        if "User Query:" in query:
            q_clean = query.split("User Query:", 1)[1].strip()
        else:
            q_clean = query
        q_lower = q_clean.lower().strip()

        # 1. Patent Definition & Patentability Fundamentals
        if any(k in q_lower for k in ["what is a patent", "what is patent", "define patent", "patent definition", "what can be patented", "meaning of patent", "explain patent"]):
            return self._answer_patent_definition(q_lower)

        # 2. Prior Art Definition & Framework
        if any(k in q_lower for k in ["what is prior art", "prior art", "meaning of prior art", "explain prior art"]):
            return self._answer_prior_art_definition(q_lower)

        # 3. Section 3(p) Definitional Query
        if any(k in q_lower for k in ["section 3(p)", "section 3p", "what is 3(p)", "what is section 3(p)"]):
            return self._answer_section_3p()

        # 4. Section 3(e) Synergism vs Mere Admixture
        if any(k in q_lower for k in ["section 3(e)", "section 3e", "what is 3(e)", "mere admixture", "synergism", "combination index"]):
            return self._answer_section_3e()

        # 5. Section 3(d) Enhanced Therapeutic Efficacy (Novartis standard)
        if any(k in q_lower for k in ["section 3(d)", "section 3d", "what is 3(d)", "therapeutic efficacy", "novartis"]):
            return self._answer_section_3d()

        # 6. Biological Diversity Act & Form III NBA Clearance
        if any(k in q_lower for k in ["biological diversity act", "bda form iii", "nba approval", "form iii", "section 6 bda"]):
            return self._answer_bda_section_6()

        # 7. Greetings & Persona
        if any(g in q_lower for g in ["hello", "hi", "hey", "namaste", "good morning", "who are you", "what can you do", "help me", "introduce"]):
            return self._answer_greeting()

        # 8. What is Ayurveda / Classical Concepts
        if any(k in q_lower for k in ["what is ayurveda", "history of ayurveda", "charaka", "sushruta", "ashtanga", "shodhana", "bhasma", "rasa shastra"]):
            return self._answer_ayurveda_fundamentals(q_lower)

        # 9. IPR Fundamentals (Trademarks, Copyrights, GIs, Trade Secrets)
        if any(k in q_lower for k in ["intellectual property", "what is ipr", "difference between patent", "copyright", "trade secret", "geographical indication"]):
            return self._answer_ipr_fundamentals(q_lower)

        # 10. Biopiracy & Case Studies
        if any(k in q_lower for k in ["biopiracy", "turmeric", "neem", "basmati", "history of tkdl"]):
            return self._answer_biopiracy_history()

        # 11. Regulatory Landscape
        if any(k in q_lower for k in ["what is ayush", "ministry of ayush", "cdsco", "difference between medicine and cosmetic", "difference between food"]):
            return self._answer_regulatory_landscape(q_lower)

        # 12. International Treaties
        if any(k in q_lower for k in ["nagoya protocol", "trips", "what is wipo", "cbd"]):
            return self._answer_international_treaties(q_lower)

        # Default Fallback: Always strictly contextualized conversational analysis
        return self._answer_general_conversational(q_clean)

    def _answer_patent_definition(self, query: str = "") -> Tuple[str, list[str]]:
        ans = (
            "### Patent Law Definition & High-Value Patentability Framework (Ayur-Lex-AI Engine)\n\n"
            "Under Indian jurisprudence, a **Patent** is an exclusive statutory monopoly granted under **The Patents Act, 1970** "
            "(Section 2(1)(m)) for a statutory term of **20 years** in exchange for full enabling disclosure of an invention. "
            "Under Sections 2(1)(j) and 2(1)(ja), a patentable invention must meet three universal criteria: **Novelty**, **Inventive Step** (non-obviousness), "
            "and **Industrial Applicability** [patents-act-1970].\n\n"
            "However, under **Ayur-Lex-AI's specialized statutory framework**, patenting botanical, herbal, and Ayurvedic innovations is strictly conditioned on navigating **negative statutory exclusions** and mandatory regulatory safe-gates:\n\n"
            "#### 1. Indian Patents Act, 1970 — Mandatory Statutory Exclusions:\n"
            "- **Section 3(p) — Traditional Knowledge Bar**:\n"
            "  Statutorily excludes an invention which in effect is traditional knowledge or which is an aggregation or duplication of known properties of traditionally known components [patents-act-3p]. Formulations documented in classical treatises (*Charaka Samhita*, *Sushruta Samhita*, *Ashtanga Hridaya*) and the 4.5+ lakh formulations indexed in the **Traditional Knowledge Digital Library (TKDL)** belong to the public domain and are excluded from patent monopolies [tkdl-prior-art].\n"
            "- **Section 3(e) — Mere Admixture Bar vs Synergism**:\n"
            "  Bars substances obtained by a mere admixture resulting only in the aggregation of the properties of the components thereof [patents-act-3e]. To patent a polyherbal composition, applicants MUST establish **demonstrable supra-additive synergism** through empirical pharmacological proof, such as a **Chou-Talalay Combination Index ($CI < 1.0$)** or isobolographic analysis proving that the whole is significantly greater than the additive sum of its individual parts.\n"
            "- **Section 3(d) — Enhanced Therapeutic Efficacy (*Novartis* Standard)**:\n"
            "  Bars the mere discovery of a new form or delivery modification of a known substance unless it demonstrates a statistically significant enhancement of **known therapeutic efficacy** (*Novartis AG v. Union of India, 2013*) [patents-act-3d]. Mere pharmacokinetic variations or bioavailability increases without demonstrated clinical superiority do not satisfy Section 3(d).\n\n"
            "#### 2. Biological Diversity Act, 2002 — Mandatory Form III NBA Clearance:\n"
            "- Under **Section 6 of the Biological Diversity Act, 2002**, any person applying for an intellectual property right (in India or abroad) for any invention based on research or information on a biological resource obtained from India MUST obtain **mandatory prior approval on Form III** from the **National Biodiversity Authority (NBA)** [bd-act-sec-6].\n"
            "- Under Section 10(4)(d)(ii) of The Patents Act, 1970, failure to produce the NBA clearance certificate is a non-waivable statutory defect barring patent grant or warranting post-grant revocation.\n\n"
            "#### 3. High-Value Patentability Thresholds (How to Qualify):\n"
            "To successfully clear §3(p) and §3(e) hurdles and secure an enforceable patent in India, the application must establish:\n"
            "1. **Standardized Extraction Fractions**: Supercritical $CO_2$ extraction fractions, targeted chromatographic solvent cuts, or enriched bio-active marker fractions distinct from traditional aqueous/decoction extracts (*Kashayam* / *Kwath*).\n"
            "2. **Novel Stoichiometric Ratios**: Non-classical ratios delivering verified supra-additive synergism ($CI < 1.0$).\n"
            "3. **Synergistic Bio-Enhancement**: Quantifiable pharmacokinetic AUC enhancement (e.g. piperine or bio-enhancing adjuvants) coupled with demonstrable clinical disease efficacy.\n\n"
            "*(Statutory Authorities: The Patents Act, 1970 §§ 2(1)(j), 3(p), 3(e), 3(d); Biological Diversity Act, 2002 § 6 [bd-act-sec-6]; TKDL Prior Art Database [tkdl-prior-art])* "
        )
        questions = [
            "How do I prove synergism under Section 3(e) to overcome Section 3(p)?",
            "What is the step-by-step process to file NBA Form III clearance?",
            "What evidence does the Indian Patent Office require for herbal extract novelty?",
            "Can I patent a polyherbal formulation of Withania somnifera and Curcuma longa?"
        ]
        return ans, questions

    def _answer_prior_art_definition(self, query: str = "") -> Tuple[str, list[str]]:
        ans = (
            "### Prior Art Framework in Indian Patent Law & Ayurvedic Knowledge (Ayur-Lex-AI Engine)\n\n"
            "Under Indian patent law, **Prior Art** encompasses any public knowledge, published document, or public use preceding the priority filing date of a patent application. Under Sections 13 and 29-34 of **The Patents Act, 1970**, prior art invalidates **Novelty** (§2(1)(j)) and **Inventive Step** (§2(1)(ja)) [patents-act-1970].\n\n"
            "In Ayurvedic and herbal innovation, prior art operates under a strict statutory regime:\n\n"
            "#### 1. Codified Traditional Treatises & The TKDL Defensive Shield:\n"
            "- Classical Sanskrit and regional treatises recognized under the **First Schedule to the Drugs and Cosmetics Act, 1940** (*Charaka Samhita*, *Sushruta Samhita*, *Ashtanga Hridaya*, etc.) constitute published prior art in the public domain.\n"
            "- The **Traditional Knowledge Digital Library (TKDL)** indexes over 4.5 lakh classical formulations in 5 international languages, providing patent examiners worldwide with instant prior art citations to defeat biopiracy and unauthorized patents [tkdl-prior-art].\n\n"
            "#### 2. Statutory Exclusions Triggered by Botanical Prior Art:\n"
            "- **Section 3(p)**: Excludes traditional knowledge and duplication of traditionally known properties as non-patentable subject matter [patents-act-3p].\n"
            "- **Section 3(e)**: Aggregation of known prior-art herbs is barred as a mere admixture unless empirical supra-additive synergism ($CI < 1.0$) is proven [patents-act-3e].\n"
            "- **Section 3(d)**: New forms or delivery modifications of documented prior art must prove statistically enhanced therapeutic efficacy under the *Novartis* standard [patents-act-3d].\n\n"
            "#### 3. Overcoming Prior Art & Mandatory NBA Approval:\n"
            "- **High-Value Novelty**: Overcome prior art through standardized extraction fractions (e.g. supercritical $CO_2$) and synergistic bio-enhancement.\n"
            "- **Biological Diversity Act, 2002**: Prior to patent grant, obtain mandatory **Form III approval** from the National Biodiversity Authority under Section 6 [bd-act-sec-6].\n\n"
            "*(Statutory Authorities: The Patents Act, 1970 §§ 2(1)(j), 3(p), 3(e), 3(d), 13; Biological Diversity Act, 2002 § 6; TKDL Prior Art)*"
        )
        questions = [
            "How does the Indian Patent Office search the TKDL for prior art?",
            "Can a classical formulation in Charaka Samhita be modified to overcome prior art?",
            "What is Section 3(e) synergism proof under Chou-Talalay equations?",
            "Do I need NBA Form III clearance if my biological resource is in the public domain?"
        ]
        return ans, questions

    def _answer_section_3e(self) -> Tuple[str, list[str]]:
        ans = (
            "### Section 3(e) of The Patents Act, 1970 — Mere Admixture Bar vs Synergism\n\n"
            "Under **Section 3(e) of the Indian Patents Act, 1970**, the following is declared not an invention:\n\n"
            "> *\"a substance obtained by a mere admixture resulting only in the aggregation of the properties of the components thereof or a process for producing such substance.\"*\n\n"
            "#### Key Statutory Requirements for Ayurvedic Innovations:\n"
            "1. **The Polyherbal Admixture Bar**: Simply combining known Ayurvedic herbs (e.g., *Withania somnifera* with *Curcuma longa*) is presumed to be a mere aggregation of known therapeutic properties.\n"
            "2. **Establishing Supra-Additive Synergism**: To overcome Section 3(e), applicants must submit quantifiable pharmacological data demonstrating that the combination exhibits **statistically significant synergism** ($1 + 1 > 2$) rather than mere additivity [patents-act-3e].\n"
            "3. **Empirical Standards Accepted by IPO**:\n"
            "   - **Chou-Talalay Combination Index ($CI < 1.0$)**: $CI < 0.8$ demonstrates moderate to strong synergism; $CI < 0.5$ confirms potent synergism.\n"
            "   - **Isobolographic Analysis**: Statistically validated shift in dose-response curves.\n"
            "   - **Pharmacokinetic Bio-Enhancement**: Significant increase in bioavailability (e.g., 3x AUC enhancement using piperine or bio-enhancer adjuvants).\n"
            "4. **Interplay with Section 3(p) & NBA Clearance**:\n"
            "   - Overcoming §3(e) synergism is the primary legal mechanism to defeat Section 3(p) traditional knowledge rejections [patents-act-3p].\n"
            "   - Mandatory prior clearance on **Form III** from the National Biodiversity Authority (NBA) under Section 6 of the Biological Diversity Act, 2002 must still be secured [bd-act-sec-6].\n\n"
            "*(Statutory Authority: The Patents Act, 1970, Section 3(e) [patents-act-3e]; Biological Diversity Act, 2002, Section 6 [bd-act-sec-6])*"
        )
        questions = [
            "How do I calculate the Chou-Talalay Combination Index (CI) for herbal extracts?",
            "What pharmacological models does the Indian Patent Office accept for synergism?",
            "Do I need NBA Form III clearance if my formulation is synergistic?"
        ]
        return ans, questions

    def _answer_section_3d(self) -> Tuple[str, list[str]]:
        ans = (
            "### Section 3(d) of The Patents Act, 1970 — Enhanced Therapeutic Efficacy (*Novartis* Standard)\n\n"
            "Under **Section 3(d) of the Indian Patents Act, 1970**, the following is excluded from patentability:\n\n"
            "> *\"the mere discovery of a new form of a known substance which does not result in the enhancement of the known efficacy of that substance or the mere discovery of any new property or new use for a known substance...\"*\n\n"
            "#### The Supreme Court Landmark Benchmark (*Novartis AG v. Union of India, 2013*):\n"
            "1. **Therapeutic Efficacy Strictness**: The Supreme Court held that 'efficacy' under Section 3(d) strictly means **therapeutic efficacy** (healing or disease-curing capacity), not mere physical, chemical, or pharmacokinetic changes [patents-act-3d].\n"
            "2. **Bioavailability vs Efficacy**: A mere enhancement in bioavailability (e.g. higher blood plasma concentration) does NOT satisfy Section 3(d) unless it translates into a proven, statistically significant improvement in therapeutic outcome or reduction in toxicity.\n"
            "3. **Relevance to Ayurveda & Phytopharmaceuticals**:\n"
            "   - Novel delivery systems (nano-emulsions, liposomes, phytosomes) of known Ayurvedic actives (like curcumin, withanolides, or berberine) must prove enhanced clinical efficacy over the baseline classical decoction.\n"
            "   - Standardized solvent fractions must substantiate superior physiological biomarker regulation.\n"
            "4. **Biological Diversity Act Mandate**: Compliance with Section 6 of the Biological Diversity Act, 2002 (Form III NBA approval) is mandatory prior to patent grant [bd-act-sec-6].\n\n"
            "*(Statutory Authority: The Patents Act, 1970, Section 3(d) [patents-act-3d]; Novartis AG v. Union of India (2013) 6 SCC 1)*"
        )
        questions = [
            "What clinical evidence is needed to prove enhanced therapeutic efficacy under Section 3(d)?",
            "Can a nano-curcumin formulation be patented under Section 3(d)?",
            "What is the difference between pharmacokinetic bioavailability and therapeutic efficacy?"
        ]
        return ans, questions

    def _answer_bda_section_6(self) -> Tuple[str, list[str]]:
        ans = (
            "### Biological Diversity Act, 2002 — Section 6 Mandatory Form III NBA Clearance\n\n"
            "Under **Section 6 of the Biological Diversity Act, 2002 (BDA)**, a strict statutory safe-gate governs all intellectual property rights involving Indian biological resources:\n\n"
            "> *\"No person shall apply for any intellectual property right, by whatever name called, in or outside India for any invention based on any research or information on a biological resource obtained from India without obtaining the previous approval of the National Biodiversity Authority.\"*\n\n"
            "#### Key Compliance & Enforcement Requirements:\n"
            "1. **Mandatory Form III Application**: Any inventor filing an Indian or international (PCT/foreign) patent application based on Indian biological resources must apply to the National Biodiversity Authority (NBA, Chennai) on **Form III** [bd-act-sec-6].\n"
            "2. **Timing of Approval**: While the patent application can be filed before the Indian Patent Office, the patent **CANNOT be granted or sealed** until the NBA issues the formal approval certificate and Benefit Sharing Agreement.\n"
            "3. **Statutory Consequences of Non-Compliance**:\n"
            "   - Under **Section 10(4)(d)(ii) of The Patents Act, 1970**, non-production of NBA clearance is a statutory ground for rejection in the First Examination Report (FER).\n"
            "   - Under Section 64(1)(p) of The Patents Act, it is an irrevocable ground for patent revocation.\n"
            "4. **2023 Biological Diversity (Amendment) Act Key Updates**:\n"
            "   - Codified AYUSH practitioners (Vaidyas and Hakims) and local communities are exempted from ABS payment under Section 7 [bd-act-sec-7-2023].\n"
            "   - Normally Traded Commodities (Section 40) cultivated and sold for commercial consumption are exempted, but patent applications covering extracted formulations still require NBA review.\n\n"
            "*(Statutory Authority: Biological Diversity Act, 2002 §§ 6, 7, 40 [bd-act-sec-6]; Patents Act, 1970 §§ 10(4)(d)(ii), 64(1)(p))*"
        )
        questions = [
            "What is the timeline and fee for NBA Form III approval?",
            "What are the ABS benefit-sharing percentage rates under Indian law?",
            "Does the 2023 BDA Amendment exempt Indian AYUSH companies from Form III?"
        ]
        return ans, questions

    def _answer_section_3p(self) -> Tuple[str, list[str]]:
        ans = (
            "### Section 3(p) of The Patents Act, 1970 — Traditional Knowledge Exclusion\n\n"
            "Under **Section 3(p) of the Indian Patents Act, 1970**, the following subject matter is explicitly declared as **not an invention**:\n\n"
            "> *\"an invention which in effect is traditional knowledge or which is an aggregation or duplication of known properties of traditionally known component or components.\"*\n\n"
            "#### Key Statutory Implications for Ayurveda:\n"
            "1. **Public Domain Inventions Barred**: Formulations, single herbs, and traditional uses documented in ancient classical treatises (such as Charaka Samhita, Sushruta Samhita, and Ashtanga Hridaya) belong to the public domain and cannot be monopolized by patent monopolies.\n"
            "2. **Bar on Mere Duplication / Aggregation**: Merely grinding, blending, or bottling known herbs (e.g., Turmeric for wound healing, Neem for antifungal use, or Ashwagandha for stress relief) is barred under Section 3(p) as a duplication of traditionally known properties.\n"
            "3. **The TKDL Defensive Shield**: The Traditional Knowledge Digital Library (TKDL) contains over 4.5 lakh classical formulations across 5 international languages, providing patent examiners worldwide with instant prior art evidence to reject patent claims under Section 3(p) [tkdl-prior-art].\n"
            "4. **Pathways to Overcome Section 3(p)**:\n"
            "   - **Section 3(e) Synergistic Combinations**: Prove unexpected non-additive synergism with empirical data and Chou-Talalay Combination Index ($CI < 1.0$) [patents-act-3e];\n"
            "   - **Section 3(d) Enhanced Therapeutic Efficacy**: Demonstrate significant, verifiable increase in therapeutic efficacy over the known baseline (*Novartis* standard) [patents-act-3d];\n"
            "   - **Novel Processing/Extraction**: Patented supercritical solvent fractions or novel standardized extract delivery matrices.\n\n"
            "*(Statutory Authority: The Patents Act, 1970, Section 3(p) [patents-act-3p]; TKDL Prior Art Database [tkdl-prior-art])*"
        )
        questions = [
            "How do I prove synergism under Section 3(e) to overcome Section 3(p)?",
            "What evidence does the Indian Patent Office require for herbal novelty?",
            "Do I need NBA approval on Form III before applying for a patent?"
        ]
        return ans, questions

    def _answer_greeting(self) -> Tuple[str, list[str]]:
        ans = (
            "### Welcome to the Ayurvedic IPR & Regulatory AI Assistant\n\n"
            "Hello! I am your specialized AI legal and regulatory pair-assistant, designed to help researchers, entrepreneurs, Vaidyas, "
            "and manufacturers navigate the legal landscape of Indian traditional medicine, intellectual property rights, and regulatory compliance.\n\n"
            "**Here is how I can assist you:**\n"
            "- **Patentability & Traditional Knowledge**: Evaluate whether your formulation satisfies Section 3(p), Section 3(e) (synergy $CI < 1.0$), "
            "and Section 3(d) of The Patents Act, 1970 [patents-act-3p, patents-act-3e].\n"
            "- **Biodiversity & ABS Approvals**: Guide you through National Biodiversity Authority (NBA) approvals on Form III, the 2023 Amendment exemptions, "
            "and Section 40 Normally Traded Commodities [bd-act-sec-6, bd-act-sec-7-2023].\n"
            "- **Manufacturing Licensing (AYUSH)**: Differentiate between Classical ASU Drugs (Form 25-D, no clinical trials) and Patent or Proprietary (P&P) "
            "medicines under Rule 158-B, including Schedule T GMP and Schedule E(1) poisonous herbs [dc-act-classical-3a, dc-act-prop-3h].\n"
            "- **Trademarks & Brand Strategy**: Overcome Section 9 *publici juris* generic exclusions for classical names (Triphala, Chyawanprash) and apply the Supreme Court *Cadila* standard [trademarks-ayurveda-names].\n"
            "- **Ayurveda Aahara (FSSAI)**: Advise on Schedule A recipes, mandatory logo rules, and the strict prohibition of therapeutic disease claims [fssai-ayurveda-aahara].\n"
            "- **International Disclosures**: Comply with the WIPO GRATK Treaty (2024) and the Nagoya Protocol [wipo-gratk-treaty-2024].\n\n"
            "**How can I help you today?** Tell me about your specific formulation, product concept, or regulatory question!"
        )
        questions = [
            "Can I patent an Ayurvedic formulation?",
            "Do I need clinical trials for classical medicine?",
            "Can I register a trademark for Triphala?",
            "Do I need NBA approval before filing a patent?"
        ]
        return ans, questions

    def _answer_ayurveda_fundamentals(self, q_lower: str) -> Tuple[str, list[str]]:
        ans = (
            "### Fundamentals of Ayurveda & Its Codified Classical Framework\n\n"
            "**Ayurveda** (*Ayur* = Life, *Veda* = Science or Knowledge) is the traditional Indian system of holistic health and medicine "
            "dating back over 3,000 years. It views health as a dynamic equilibrium between the body, mind, spirit, and environment.\n\n"
            "**1. Core Classical Treatises (*Brihat Trayi* & *Laghut Trayi*)**:\n"
            "Ayurveda is anchored in authoritative classical Sanskrit treatises formally recognized in the **First Schedule to the Drugs and Cosmetics Act, 1940**:\n"
            "- **Charaka Samhita**: The primary authority on internal medicine (*Kayachikitsa*), diagnosis, and herbal formulations.\n"
            "- **Sushruta Samhita**: The pioneer text on surgery (*Shalya Chikitsa*), anatomy, and surgical instruments.\n"
            "- **Ashtanga Hridaya & Ashtanga Samgraha**: Comprehensive syntheses by Vagbhata covering all 8 branches of Ayurveda.\n"
            "- **Sharangadhara Samhita & Bhaishajya Ratnavali**: Key authorities on pharmaceutical compounding (*Bhaishajya Kalpana*) and Rasa Shastra.\n\n"
            "**2. Classical Shodhana (Purification & Detoxification)**:\n"
            "Potent or toxic botanical, mineral, and metallic ingredients (listed under **Schedule E(1)**, such as *Vatsanabha*, *Bhallataka*, *Kupilu*, and *Parada*) "
            "must undergo classical Shodhana processes to eliminate toxicity and enhance bio-compatibility [dc-act-schedule-e1].\n\n"
            "**3. Legal & IPR Significance**:\n"
            "Because these classical treatises are published, public-domain ancient authorities, all formulations verbatim derived from them are "
            "**codified traditional knowledge**. Under **Section 3(p) of The Patents Act, 1970**, they cannot be monopolized by any individual or corporation [patents-act-3p]. "
            "Over 4.5 lakh classical formulations have been cataloged in the **Traditional Knowledge Digital Library (TKDL)** [tkdl-prior-art]."
        )
        questions = [
            "Are classical formulations documented in Charaka Samhita patentable?",
            "What license is required to manufacture a classical Ayurvedic medicine?",
            "What is Schedule E(1) for poisonous botanicals?"
        ]
        return ans, questions

    def _answer_ipr_fundamentals(self, q_lower: str) -> Tuple[str, list[str]]:
        ans = (
            "### Intellectual Property Rights (IPR) Overview for Herbal & Ayurvedic Innovations\n\n"
            "Intellectual Property Rights are legally enforceable property rights granted over intangible creations of the human mind. "
            "In the Ayurvedic and herbal sector, multiple distinct forms of IPR apply:\n\n"
            "| IPR Category | What It Protects | Term | Applicability to Ayurveda |\n"
            "| :--- | :--- | :--- | :--- |\n"
            "| **Patents** | Novel, non-obvious inventions & processes | 20 Years | Novel proprietary combinations with proven synergy ($CI < 1.0$) [patents-act-3e], isolated phytopharmaceuticals [patents-act-3d]. Classical recipes are excluded [patents-act-3p]. |\n"
            "| **Trademarks** | Distinctive brand names, logos, slogans | 10 Years (Renewable) | Protects unique brand names (e.g. *'[Brand] Triphala'*). Classical names like *Triphala* or *Chyawanprash* alone are public domain [trademarks-ayurveda-names]. |\n"
            "| **Copyrights** | Original literary, dramatic, software works | Life + 60 Years | Protects training manuals, proprietary databases, mobile apps, educational books. Does NOT protect recipes or therapeutic methods. |\n"
            "| **Trade Secrets** | Confidential formulation processes & Know-how | Indefinite | Useful for proprietary manufacturing extraction temperatures, yields, or specialized blending techniques kept strictly confidential. |\n"
            "| **Geographical Indications (GI)**| Goods with unique characteristics due to geographic origin | 10 Years (Renewable) | Protects regional botanical origins (e.g., Kashmir Saffron, Malabar Pepper, Navara Rice, Darjeeling Tea). |\n\n"
            "**Key Boundary**: Traditional knowledge cannot be patented (§3(p)). However, you can protect your enterprise through **distinctive trademark branding** "
            "and secure patents for **novel synergistic formulations** with empirical proof [patents-act-3e]."
        )
        questions = [
            "How do I prove synergism to patent an herbal mixture under Section 3(e)?",
            "Can I register a trademark for an Ayurvedic product name?",
            "What is Section 3(p) for traditional knowledge?"
        ]
        return ans, questions

    def _answer_biopiracy_history(self) -> Tuple[str, list[str]]:
        ans = (
            "### Biopiracy & India's Landmark Defense of Traditional Knowledge\n\n"
            "**Biopiracy** refers to the commercial exploitation of naturally occurring biological resources or indigenous traditional knowledge "
            "by individuals, corporations, or foreign research institutions without authorization, compensation, or benefit-sharing with the indigenous custodian communities.\n\n"
            "**Landmark Case Studies of Biopiracy Against Indian Heritage:**\n"
            "1. **The Turmeric Patent (*Curcuma longa*, US Patent 5,401,504)**:\n"
            "   - In 1995, the University of Mississippi Medical Center was granted a US patent for the use of turmeric powder to heal wounds.\n"
            "   - India's Council of Scientific and Industrial Research (CSIR) filed a formal legal challenge, presenting 32 authoritative classical Sanskrit, "
            "Urdu, and Hindi references documenting centuries of traditional wound-healing use.\n"
            "   - In 1997, the USPTO completely revoked all patent claims—marking the first time a developing country successfully challenged a granted foreign patent based on traditional knowledge.\n"
            "2. **The Neem Patent (*Azadirachta indica*, European Patent 436,257)**:\n"
            "   - Granted by the European Patent Office (EPO) to W.R. Grace for the fungicidal properties of neem seeds.\n"
            "   - Challenged by Indian activists and CSIR. In 2005, the EPO Technical Board of Appeal revoked the patent for total lack of novelty and inventive step.\n"
            "3. **The Basmati Rice Patent (US Patent 5,663,484)**:\n"
            "   - RiceTec Inc. attempted to patent basmati rice lines. India successfully defended its heritage, resulting in RiceTec withdrawing most claims.\n\n"
            "**India's Defensive Shield: The TKDL & Biodiversity Act**:\n"
            "- **Traditional Knowledge Digital Library (TKDL, tkdl.res.in)**: Created in 2001 by CSIR and Ministry of Ayush, documenting 4.5+ lakh classical formulations in 5 foreign languages to give international patent examiners instant prior art evidence [tkdl-prior-art].\n"
            "- **Biological Diversity Act, 2002**: Section 6 mandates prior approval from the National Biodiversity Authority (NBA) on Form III before applying for any IPR based on Indian biological resources [bd-act-sec-6]."
        )
        questions = [
            "How does the TKDL prevent foreign biopiracy patents?",
            "What is Section 6 of the Biological Diversity Act?",
            "What is the WIPO GRATK Treaty on genetic resources?"
        ]
        return ans, questions

    def _answer_regulatory_landscape(self, q_lower: str) -> Tuple[str, list[str]]:
        ans = (
            "### The Indian Regulatory Landscape: AYUSH vs CDSCO vs FSSAI\n\n"
            "In India, botanical, herbal, and Ayurvedic products are categorized into three distinct regulatory jurisdictions depending on their formulation, purpose, and claims:\n\n"
            "**1. Ayurvedic Medicines (Ministry of Ayush / State Licensing Authorities)**:\n"
            "- **Governing Law**: The Drugs and Cosmetics Act, 1940 & Rules, 1945 [dc-act-classical-3a].\n"
            "- **Classical ASU Medicines (§3(a))**: Exact First Schedule recipes. License on Form 25-D. No clinical trials required.\n"
            "- **Patent or Proprietary (P&P) Medicines (§3(h))**: Modified recipes or novel indications under Rule 158-B. Form 25-E license. Requires safety and pilot clinical data [dc-act-prop-3h].\n"
            "- **Permissible Claims**: Legally permitted to make disease diagnosis, treatment, and therapeutic cure claims.\n\n"
            "**2. Ayurveda Aahara (Food Safety and Standards Authority of India - FSSAI)**:\n"
            "- **Governing Law**: Food Safety and Standards (Ayurveda Aahara) Regulations, 2022 [fssai-ayurveda-aahara].\n"
            "- **Scope**: Foods prepared according to classical treatises in Schedule A.\n"
            "- **Mandatory Labelling**: Distinctive Ayurveda Aahara logo and front-of-pack advisory text (*'Ayurveda Aahara - Not for medicinal use'*).\n"
            "- **Strict Ban on Drug Claims**: Strictly prohibited from claiming to cure, treat, or prevent human diseases [fssai-ayurveda-aahara].\n\n"
            "**3. Herbal / Ayurvedic Cosmetics (State Drug Licensing Authorities)**:\n"
            "- Regulated under Cosmetics rules. Formulated for cleansing, beautifying, or altering appearance. Cannot make therapeutic medicinal claims."
        )
        questions = [
            "What are the rules and labelling for Ayurveda Aahara?",
            "What is the difference between classical and proprietary medicine?",
            "Do I need clinical trials for classical medicine?"
        ]
        return ans, questions

    def _answer_international_treaties(self, q_lower: str) -> Tuple[str, list[str]]:
        ans = (
            "### International Treaties on Traditional Knowledge, Biodiversity & IPR\n\n"
            "Cross-border trade and patenting of herbal innovations are regulated by key international agreements:\n\n"
            "**1. WIPO GRATK Treaty (Adopted May 2024)**:\n"
            "- The **Treaty on Intellectual Property, Genetic Resources and Associated Traditional Knowledge** is a landmark international agreement adopted in Geneva [wipo-gratk-treaty-2024].\n"
            "- **Article 3 Mandatory Disclosure**: Patent applicants worldwide must declare the country of origin of genetic resources and identify indigenous communities providing associated traditional knowledge [wipo-gratk-treaty-2024].\n\n"
            "**2. Convention on Biological Diversity (CBD) & Nagoya Protocol (2010)**:\n"
            "- Establishes the sovereign rights of nations over their biological diversity.\n"
            "- Mandates **Prior Informed Consent (PIC)** and **Mutually Agreed Terms (MAT)** before accessing genetic resources, ensuring fair and equitable sharing of benefits (ABS) [nba-abs-regulations-2014].\n\n"
            "**3. WTO TRIPS Agreement**:\n"
            "- Establishes minimum international standards for intellectual property.\n"
            "- Article 27.3(b) allows member states to exclude plants, animals, and biological processes from patentability, which India implements through Section 3(j) and Section 3(p) [patents-act-3p]."
        )
        questions = [
            "What are the mandatory disclosure rules under WIPO GRATK Treaty?",
            "How does NBA Form I work for foreign companies?",
            "What is the ABS benefit-sharing percentage under Indian law?"
        ]
        return ans, questions

    def _answer_general_conversational(self, query: str) -> Tuple[str, list[str]]:
        ans = (
            f"### Conversational Legal Analysis: {query.strip(' ?.')}\n\n"
            "Thank you for your question. As your Ayurvedic IPR & Regulatory AI Assistant, I analyze every inquiry through the three core pillars of Indian herbal regulation:\n\n"
            "1. **Intellectual Property Protection**: Whether your idea is eligible for patents under The Patents Act, 1970 (clearing Section 3(p) traditional knowledge exclusions and satisfying Section 3(e) synergy or Section 3(d) therapeutic efficacy) or is best protected as a distinctive Trademark under the Trade Marks Act, 1999 [patents-act-3p, patents-act-3e, trademarks-ayurveda-names].\n"
            "2. **Biodiversity & ABS Compliance**: Whether your biological resources require mandatory prior approval from the National Biodiversity Authority (NBA) on Form III under Section 6 of the Biological Diversity Act, 2002, or qualify for Section 7 exemptions under the 2023 Amendment [bd-act-sec-6, bd-act-sec-7-2023].\n"
            "3. **Manufacturing & Market Licensing**: Whether your product is classified as a Classical ASU Drug (§3(a), Form 25-D), a Patent or Proprietary Medicine (§3(h), Rule 158-B), or an Ayurveda Aahara dietary food under FSSAI 2022 Regulations [dc-act-classical-3a, dc-act-prop-3h, fssai-ayurveda-aahara].\n\n"
            "**To help me give you specific legal guidance and tailored reasoning, could you share a bit more about your project?**"
        )
        questions = [
            "I want to know if my formulation can be patented",
            "What license is required to manufacture and sell?",
            "Can I register a trademark for my herbal product?",
            "Do I need NBA biodiversity approval?"
        ]
        return ans, questions
