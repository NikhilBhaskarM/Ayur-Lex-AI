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
        q_lower = query.lower().strip()
        
        # Greetings & Persona
        if any(q_lower == g or q_lower.startswith(g + " ") or q_lower.endswith(" " + g) for g in ["hello", "hi", "hey", "namaste", "good morning", "good afternoon", "good evening"]):
            return True
        if any(k in q_lower for k in ["who are you", "what are you", "what can you do", "help me", "introduce yourself", "how can you help"]):
            return True

        # Ayurveda Concepts
        if any(k in q_lower for k in ["what is ayurveda", "history of ayurveda", "charaka samhita", "sushruta samhita", "ashtanga hridaya", "rasa shastra", "what is shodhana", "what is bhasma", "ayurvedic formulary of india"]):
            # If not asking specifically about patenting or licensing
            if not any(k in q_lower for k in ["patent", "license", "trademark", "form iii", "rule 158"]):
                return True

        # IPR Fundamentals
        if any(k in q_lower for k in ["what is intellectual property", "what is ipr", "difference between patent and trademark", "difference between patent and copyright", "what is a copyright", "what is a trade secret", "what is a geographical indication", "what is prior art", "types of ipr", "types of intellectual property"]):
            return True

        # Biopiracy & Case Studies
        if any(k in q_lower for k in ["what is biopiracy", "examples of biopiracy", "turmeric patent", "neem patent", "basmati patent", "history of tkdl"]):
            if not any(k in q_lower for k in ["section 3(p)", "section 3(e)", "my formulation"]):
                return True

        # Regulatory Landscape
        if any(k in q_lower for k in ["what is ayush", "ministry of ayush", "cdsco vs ayush", "difference between medicine and cosmetic", "difference between food and medicine"]):
            return True

        # International Treaties
        if any(k in q_lower for k in ["what is nagoya protocol", "what is trips agreement", "what is wipo", "cbd and traditional knowledge"]):
            return True

        return False

    def synthesize_general_answer(self, query: str, conversation_history: Optional[list[dict]] = None) -> Tuple[str, list[str]]:
        """Synthesize answer and return (answer_markdown, clarification_questions)."""
        q_lower = query.lower()

        # 1. Greetings & Persona
        if any(g in q_lower for g in ["hello", "hi", "hey", "namaste", "good morning", "who are you", "what can you do", "help me", "introduce"]):
            return self._answer_greeting()

        # 2. What is Ayurveda / Classical Concepts
        if any(k in q_lower for k in ["what is ayurveda", "history of ayurveda", "charaka", "sushruta", "ashtanga", "shodhana", "bhasma", "rasa shastra"]):
            return self._answer_ayurveda_fundamentals(q_lower)

        # 3. IPR Fundamentals
        if any(k in q_lower for k in ["intellectual property", "what is ipr", "difference between patent", "copyright", "trade secret", "geographical indication", "prior art"]):
            return self._answer_ipr_fundamentals(q_lower)

        # 4. Biopiracy & Case Studies
        if any(k in q_lower for k in ["biopiracy", "turmeric", "neem", "basmati", "history of tkdl"]):
            return self._answer_biopiracy_history()

        # 5. Regulatory Landscape
        if any(k in q_lower for k in ["what is ayush", "ministry of ayush", "cdsco", "difference between medicine and cosmetic", "difference between food"]):
            return self._answer_regulatory_landscape(q_lower)

        # 6. International Treaties
        if any(k in q_lower for k in ["nagoya protocol", "trips", "what is wipo", "cbd"]):
            return self._answer_international_treaties(q_lower)

        # 7. Fallback General AI Answer
        return self._answer_general_conversational(query)

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
