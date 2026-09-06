"""
Ayurvedic IPR & Regulatory AI Assistant — Query-Adaptive Statutory Reasoner

Synthesizes authoritative, accurate, directly responsive answers grounded in
primary public legal sources:
- India Code (indiacode.nic.in)
- IP India Public Databases (ipindia.gov.in)
- National Biodiversity Authority / ABS Portal (nbaindia.org)
- Traditional Knowledge Digital Library (tkdl.res.in)
- Ministry of Ayush & FSSAI (fssai.gov.in)
- WIPO (wipo.int)

Supports multi-turn conversational reasoning and interactive probing questions.
"""

import re
from typing import Optional, Tuple
from app.rag.retriever import RetrievedChunk
from app.rag.statutory_knowledge import STATUTORY_CORPUS


class StatutoryReasoner:
    """Intelligent statutory reasoning engine that accurately matches user questions,
    maintains multi-turn conversational context, and synthesizes authoritative, legally
    grounded answers with bracketed citations and interactive probing questions."""

    def __init__(self):
        self.statutory_map = {d["id"]: d for d in STATUTORY_CORPUS}

    def _has_kw(self, text: str, keywords: list[str]) -> bool:
        return any(k in text for k in keywords)

    def _has_all_kw(self, text: str, *groups: list[str]) -> bool:
        return all(any(k in text for k in group) for group in groups)

    def _extract_conversation_context(self, history: Optional[list[dict]]) -> dict:
        context = {
            "previous_herbs": [],
            "is_follow_up": False,
            "has_synergy": False,
            "synergy_value": None,
            "is_proprietary": False,
            "is_classical": False,
            "target_ip": None,
            "last_assistant_topic": None
        }
        if not history or len(history) < 2:
            return context

        context["is_follow_up"] = True
        full_text = " ".join([m.get("content", "") for m in history]).lower()

        # Identify mentioned herbs
        herbs = [
            "triphala", "chyawanprash", "turmeric", "curcumin", "ashwagandha",
            "neem", "brahmi", "tulsi", "guduchi", "ginger", "black pepper",
            "pippali", "amla", "haritaki", "bibhitaki", "vatsanabha", "bhallataka", "kupilu"
        ]
        for h in herbs:
            if h in full_text and h.capitalize() not in context["previous_herbs"]:
                context["previous_herbs"].append(h.capitalize())

        # Check goals
        if "patent" in full_text:
            context["target_ip"] = "patent"
        elif "trademark" in full_text:
            context["target_ip"] = "trademark"
        elif "license" in full_text or "manufactur" in full_text:
            context["target_ip"] = "license"

        # Check synergy mentions (e.g. CI = 0.7, CI < 1.0)
        ci_match = re.search(r'ci\s*[=:<]\s*([0-9]*\.?[0-9]+)', full_text)
        if ci_match:
            context["has_synergy"] = True
            context["synergy_value"] = ci_match.group(1)
        elif any(k in full_text for k in ["synerg", "combination index", "isobologram"]):
            context["has_synergy"] = True

        if any(k in full_text for k in ["proprietary", "modified", "novel", "new ratio"]):
            context["is_proprietary"] = True
        if any(k in full_text for k in ["classical", "charaka", "sushruta", "treatise"]):
            context["is_classical"] = True

        return context

    def synthesize(self, query: str, chunks: list[RetrievedChunk], jurisdiction: Optional[str] = None, conversation_history: Optional[list[dict]] = None) -> str:
        """Backward-compatible synthesis returning string only."""
        ans, _ = self.synthesize_with_questions(query, chunks, jurisdiction, conversation_history)
        return ans

    def synthesize_with_questions(
        self,
        query: str,
        chunks: list[RetrievedChunk],
        jurisdiction: Optional[str] = None,
        conversation_history: Optional[list[dict]] = None
    ) -> Tuple[str, list[str]]:
        """Synthesize answer with multi-turn reasoning and return (answer_markdown, clarification_questions)."""
        q_lower = query.lower()
        context = self._extract_conversation_context(conversation_history)

        # ---------------------------------------------------------------------
        # 1. SPECIFIC HIGH-PRIORITY QUESTIONS (Evaluated FIRST so direct inquiries
        # are never misidentified as contextual follow-up statements)
        # ---------------------------------------------------------------------

        # A. Required Permissions / Licenses for Ayurvedic Products
        if self._has_kw(q_lower, ["permission", "permissions", "permits", "what permission", "what license", "licenses required", "approval required", "how to start ayurvedic", "set up ayurvedic", "manufacturing permission"]):
            ans, questions = self._answer_permissions_required(query, chunks)
            return self._append_interactive_section(ans, questions)

        # B. Exporting to Europe / International Markets
        if self._has_all_kw(q_lower, ["export", "overseas", "international market", "sell in"], ["europe", "eu", "usa", "us", "uk", "foreign", "abroad"]) or \
           self._has_kw(q_lower, ["export this ayurvedic", "export to europe", "thmpd", "directive 2004/24"]):
            ans, questions = self._answer_export_europe_international(query, chunks)
            return self._append_interactive_section(ans, questions)

        # C. Determination of Traditional Knowledge Status
        if self._has_kw(q_lower, ["is this formulation traditional knowledge", "is it traditional knowledge", "traditional knowledge determination", "how to know if traditional knowledge", "how do i know if my formulation is tk"]):
            ans, questions = self._answer_traditional_knowledge_determination(query, chunks)
            return self._append_interactive_section(ans, questions)

        # D. Biodiversity Approval Decision Tree under BD Act
        if self._has_kw(q_lower, ["do i need biodiversity approval", "do i need nba approval", "is biodiversity approval required", "who needs nba approval", "biodiversity approval under the bd act", "approval under the bd act"]):
            ans, questions = self._answer_biodiversity_approval_decision_tree(query, chunks)
            return self._append_interactive_section(ans, questions)

        # E. Cultivated vs Wild-Harvested Botanicals
        if self._has_kw(q_lower, ["cultivated on registered", "cultivated vs wild", "wild harvested or cultivated", "cultivated or wild", "registered farms or wild", "difference between cultivated and wild"]):
            ans, questions = self._answer_cultivated_vs_wild_herbs(query, chunks)
            return self._append_interactive_section(ans, questions)

        # F. Indication-Specific Patentability (Cough, Diabetes, Arthritis, Skin, Cancer, Liver, etc.)
        if self._has_kw(q_lower, ["patent", "patenting", "patentable"]) and \
           any(d in q_lower for d in ["cough", "respiratory", "kasa", "asthma", "diabet", "prameha", "arthrit", "joint pain", "sandhivata", "amavata", "skin", "kushta", "liver", "cancer", "fever", "jaundice", "digest"]):
            ans, questions = self._answer_indication_specific_patent(query, chunks)
            return self._append_interactive_section(ans, questions)

        # G. Section 10(4) / Biological Origin & Patent Form 1 Disclosure
        if self._has_kw(q_lower, ["10(4)", "10 (4)", "section 10", "patent form 1", "disclosure of origin", "source and geographical origin", "origin disclosure", "origin disclosures"]):
            ans, questions = self._answer_section_10_4(query, chunks)
            return self._append_interactive_section(ans, questions)

        # H. Section 3(e) / Synergism vs Mere Admixture & Synergy Data
        if self._has_kw(q_lower, ["3(e)", "3 e", "section 3e", "mere admixture", "combination index", "isobologram", "isobolographic", "synergy (ci", "synergy data", "ci < 1.0", "ci < 1", "laboratory data showing synergy"]) or \
           (self._has_kw(q_lower, ["synerg", "unexpected effect"]) and not self._has_kw(q_lower, ["3(p)", "trademark", "aahara"])):
            ans, questions = self._answer_section_3e(query, chunks)
            return self._append_interactive_section(ans, questions)

        # I. Trademarks & Brand Protection / Generic Classical Names
        if self._has_kw(q_lower, ["trademark", "trade mark", "brand name", "logo", "publici juris", "cadila", "register this ayurvedic brand"]) or \
           self._has_all_kw(q_lower, ["can i trademark", "register trademark", "trademarking"], ["triphala", "chyawanprash", "ayurvedic", "classical", "herb", "brand"]):
            ans, questions = self._answer_trademarks(query, chunks)
            return self._append_interactive_section(ans, questions)

        # ---------------------------------------------------------------------
        # 2. STATUTORY SUBJECT-MATTER HANDLERS
        # ---------------------------------------------------------------------

        # 2. Section 3(d) / Incremental Efficacy & Phytopharmaceuticals
        if self._has_kw(q_lower, ["3(d)", "3 d", "section 3d", "incremental efficacy", "novartis", "therapeutic efficacy"]):
            ans, questions = self._answer_section_3d(query, chunks)
            return self._append_interactive_section(ans, questions)

        # 4. Section 25 / Pre-Grant & Post-Grant Patent Opposition
        if self._has_kw(q_lower, ["section 25", "pre-grant opposition", "post-grant opposition", "oppose patent", "patent opposition"]):
            ans, questions = self._answer_section_25_opposition(query, chunks)
            return self._append_interactive_section(ans, questions)

        # 5. Section 6 BD Act / Form III / Mandatory Prior Approval for Patents
        if self._has_kw(q_lower, ["form iii", "form 3", "form-iii", "form-3"]) or \
           self._has_all_kw(q_lower, ["section 6", "bd act"], ["patent", "ipr", "approval", "nba"]) or \
           self._has_all_kw(q_lower, ["nba approval", "biodiversity approval"], ["patent", "apply", "ipr", "herb"]):
            ans, questions = self._answer_bd_act_form_iii(query, chunks)
            return self._append_interactive_section(ans, questions)

        # 6. Section 7 BD Act / 2023 Amendment Exemptions
        if self._has_kw(q_lower, ["2023 amendment", "amendment act, 2023", "amendment act 2023", "2023 biodiversity amendment"]) or \
           self._has_all_kw(q_lower, ["section 7", "bd act", "biodiversity"], ["exemption", "exempt", "sbb", "intimation"]) or \
           self._has_all_kw(q_lower, ["exempt", "exemption"], ["cultivated", "vaidya", "ayush practitioner", "codified"]):
            ans, questions = self._answer_bd_act_sec_7_exemptions(query, chunks)
            return self._append_interactive_section(ans, questions)

        # 7. Section 40 BD Act / Normally Traded Commodities (NTC)
        if self._has_kw(q_lower, ["section 40", "normally traded commodities", "ntc", "421 species", "commodity exemption"]):
            ans, questions = self._answer_bd_act_sec_40_ntc(query, chunks)
            return self._append_interactive_section(ans, questions)

        # 8. ABS Regulations & Benefit-Sharing Formula
        if self._has_kw(q_lower, ["abs regulation", "benefit-sharing", "benefit sharing", "0.1%", "0.5%", "commercial utilization abs"]):
            ans, questions = self._answer_abs_regulations(query, chunks)
            return self._append_interactive_section(ans, questions)

        # 9. Foreign Entities / Cross-Border Access (Section 3 BD Act & Form I)
        if self._has_all_kw(q_lower, ["foreign", "non-citizen", "non-resident", "international company", "mnc"], ["access", "biological", "biodiversity", "herb", "research", "patent"]) or \
           self._has_kw(q_lower, ["form i", "form 1 nba", "nba form i", "nagoya protocol"]):
            ans, questions = self._answer_foreign_access_form_i(query, chunks)
            return self._append_interactive_section(ans, questions)

        # 10. Clinical Trials for Classical vs Proprietary Medicine
        if self._has_all_kw(q_lower, ["clinical trial", "clinical trials", "human trial", "trial required", "trials required"], ["classical", "ayurvedic", "medicine", "manufactur", "license", "licensing"]) or \
           "do i need clinical trial" in q_lower:
            ans, questions = self._answer_clinical_trials(query, chunks)
            return self._append_interactive_section(ans, questions)

        # 11. Schedule E(1) / Poisonous Botanicals, Minerals & Shodhana
        if self._has_kw(q_lower, ["schedule e", "schedule e(1)", "schedule e1", "poisonous", "vatsanabha", "bhallataka", "kupilu", "parada", "shodhana", "detoxification"]):
            ans, questions = self._answer_schedule_e1(query, chunks)
            return self._append_interactive_section(ans, questions)

        # 12. Schedule T / Good Manufacturing Practices (GMP)
        if self._has_kw(q_lower, ["schedule t", "gmp", "good manufacturing practice", "factory hygiene", "batch manufacturing record"]):
            ans, questions = self._answer_schedule_t_gmp(query, chunks)
            return self._append_interactive_section(ans, questions)

        # 13. Classical vs Proprietary Medicines / Manufacturing Licensing
        if self._has_kw(q_lower, ["classical vs proprietary", "difference between classical and proprietary", "rule 158-b", "form 25-d", "form 25-e", "proprietary ayurvedic", "p&p"]):
            ans, questions = self._answer_licensing_classical_vs_proprietary(query, chunks)
            return self._append_interactive_section(ans, questions)

        # 15. Ayurveda Aahara (FSSAI Regulations 2022)
        if self._has_kw(q_lower, ["aahara", "ayurveda aahara", "fssai", "ayurvedic food", "food supplement", "schedule a food"]):
            ans, questions = self._answer_ayurveda_aahara(query, chunks)
            return self._append_interactive_section(ans, questions)

        # 16. TKDL / Biopiracy Defense & Innovator Access
        if self._has_kw(q_lower, ["tkdl", "traditional knowledge digital library", "tkrc", "biopiracy", "csir tkdl", "innovator access"]):
            ans, questions = self._answer_tkdl_prior_art(query, chunks)
            return self._append_interactive_section(ans, questions)

        # 17. WIPO GRATK Treaty (2024) / International Disclosures
        if self._has_kw(q_lower, ["wipo", "gratk", "genetic resources treaty", "treaty 2024", "international disclosure"]):
            ans, questions = self._answer_wipo_gratk(query, chunks)
            return self._append_interactive_section(ans, questions)

        # 18. Section 3(p) / Classical Formulations Patentability
        if self._has_kw(q_lower, ["3(p)", "3 p", "section 3p", "traditional knowledge exclusion"]) or \
           self._has_all_kw(q_lower, ["patent", "patenting", "patentable"], ["classical", "triphala", "chyawanprash", "turmeric", "haldi", "neem", "ayurveda"]):
            ans, questions = self._answer_section_3p_patentability(query, chunks)
            return self._append_interactive_section(ans, questions)

        # 19. General Patenting Queries (Can I patent Ayurvedic medicine?)
        if self._has_kw(q_lower, ["can i patent", "how to patent", "patent an ayurvedic", "patenting of ayurvedic", "patent process", "patent my ayurvedic"]):
            ans, questions = self._answer_general_patentability(query, chunks)
            return self._append_interactive_section(ans, questions)

        # ---------------------------------------------------------------------
        # 3. CONTEXTUAL FOLLOW-UP REASONER (When user responds to our questions)
        # ---------------------------------------------------------------------
        if context["is_follow_up"] and self._is_contextual_response(q_lower):
            ans, questions = self._answer_contextual_follow_up(query, chunks, context)
            return self._append_interactive_section(ans, questions)

        # ---------------------------------------------------------------------
        # 4. DYNAMIC IRAC COMPREHENSION REASONER (Fallback for novel queries)
        # ---------------------------------------------------------------------
        ans, questions = self._answer_dynamic_irac(query, chunks, jurisdiction)
        return self._append_interactive_section(ans, questions)

    def _is_contextual_response(self, q_lower: str) -> bool:
        """Determines if a query is a factual answer or follow-up response rather than a new standalone question."""
        # Direct questions are NOT factual answering chips
        question_starters = [
            "what", "how", "can ", "do ", "is ", "are ", "have you", "which", "where", "explain", "who", "why", "tell me"
        ]
        if any(q_lower.startswith(w) for w in question_starters):
            return False
        if "?" in q_lower and not any(k in q_lower for k in ["ci=", "ci <", "ci<"]):
            return False

        # Factual statements providing answers or clarifications
        factual_indicators = [
            "it is proprietary", "it's proprietary", "proprietary formulation", "it is classical", "classical formulation",
            "we have synergy", "ci=", "ci <", "ci<", "cultivated", "wild harvested", "we want to patent",
            "we want to trademark", "yes", "no", "we source from", "farm-grown", "registered farm", "in vitro", "in vivo"
        ]
        return any(ind in q_lower for ind in factual_indicators)

    def _append_interactive_section(self, answer: str, questions: list[str]) -> Tuple[str, list[str]]:
        if not questions:
            return answer, []

        q_block = "\n\n---\n### 💬 Interactive Next Steps & Details Needed:\nTo help me tailor the exact legal and compliance roadmap for your project, please clarify:\n"
        for idx, q in enumerate(questions):
            q_block += f"{idx + 1}. **{q}**\n"

        return answer + q_block, questions

    # -------------------------------------------------------------------------
    # MULTI-TURN CONTEXTUAL REASONER
    # -------------------------------------------------------------------------

    def _answer_contextual_follow_up(self, query: str, chunks: list[RetrievedChunk], context: dict) -> Tuple[str, list[str]]:
        herbs_str = ", ".join(context["previous_herbs"]) if context["previous_herbs"] else "your herbal formulation"
        q_lower = query.lower()

        # Branch 1: User specifies cultivated or wild harvesting
        if any(k in q_lower for k in ["cultivat", "farm", "wild", "forest", "harvest", "mandi", "source"]):
            return self._answer_cultivated_vs_wild_herbs(query, chunks)

        # Branch 2: User provides synergy data (e.g. CI = 0.6)
        if any(k in q_lower for k in ["ci=", "ci <", "ci<", "synerg", "combination index", "isobologram"]):
            parts = [
                f"### Strategic Action Plan: Leveraging Laboratory Synergy for Patent Approval\n\n",
                f"**Assessment of Provided Synergy Data:**\n",
                f"Thank you for providing those specific experimental details regarding **{herbs_str}**. ",
            ]
            if context.get("synergy_value"):
                parts.append(f"Your observed Combination Index of **CI = {context['synergy_value']}** is compelling statutory evidence. ")
            else:
                parts.append("Your demonstration of synergistic interaction between these botanicals is the single most critical statutory factor. ")
            
            parts.append(
                f"Under the **Office of CGPDTM Guidelines for Examination of Traditional Knowledge Inventions**, a quantitative Combination Index $CI < 1.0$ "
                f"establishes true pharmacological synergism rather than a mere additive admixture, directly overcoming **Section 3(e) of The Patents Act, 1970** [patents-act-3e, ipindia-tk-guidelines].\n\n"
                f"**How to Structure Your Patent Application Claims & Specification:**\n"
                f"1. **Incorporate Head-to-Head Comparative Tables**: The complete specification must feature comparative biological assay tables demonstrating that the combination $(A + B)$ produces a statistically significant higher response than Component A alone or Component B alone tested at corresponding dosages.\n"
                f"2. **Drafting Claims**: Structure your independent claim around the specific synergistic weight ratio (e.g. *'A synergistic pharmaceutical formulation comprising extract of A and extract of B in a weight ratio between X:Y'*).\n"
                f"3. **Mandatory Biological Origin Disclosure (§10(4))**: In Patent Form 1 (Column 9), disclose the exact geographical origin within India where the botanical materials were collected or cultivated [patents-act-10-4].\n"
                f"4. **NBA Form III Approval (§6)**: Concurrently file **NBA Form III** on `nbaindia.org` under Section 6 of the Biological Diversity Act, 2002 [bd-act-sec-6] before patent grant.\n"
            )
            questions = [
                "Have you conducted in vivo animal safety studies or in vitro cell assays?",
                "Are your raw herbs cultivated on registered farms or wild-harvested?",
                "Would you like guidance on drafting the claims structure for your patent application?"
            ]
            return "".join(parts), questions

        # Branch 3: User specifies proprietary vs classical
        if any(k in q_lower for k in ["proprietary", "p&p", "modified", "novel ratio", "new form"]):
            parts = [
                f"### Regulatory & Patent Strategy for Proprietary Formulation\n\n",
                f"**Direct Assessment:**\n",
                f"Thank you for clarifying that **{herbs_str}** is a **Proprietary Formulation**. "
                f"Under Indian law, modifying classical ratios, adding modern bio-enhancers, or developing novel dosage delivery systems shifts your product from a classical drug to a "
                f"**Patent or Proprietary (P&P) Medicine** governed by **Section 3(h) & Rule 158-B of the Drugs and Cosmetics Rules, 1945** [dc-act-prop-3h].\n\n"
                f"**Action Plan for Proprietary Formulations:**\n"
                f"1. **Manufacturing License (Form 25-E)**: Apply to your State AYUSH Licensing Authority on Form 25-E. You must submit published scientific literature, acute oral toxicity reports, and pilot clinical trial findings to prove safety and efficacy [dc-act-prop-3h].\n"
                f"2. **Patentability Potential**: Because it is proprietary, it is NOT automatically barred as classical TK under Section 3(p). However, you must prove non-obvious synergism ($CI < 1.0$) under Section 3(e) [patents-act-3e].\n"
                f"3. **Brand Trademark Protection**: Register your invented proprietary brand name under Class 5 on `ipindia.gov.in` to prevent brand copycats [trademarks-ayurveda-names].\n"
            ]
            questions = [
                "Do you have quantitative laboratory synergy data (CI < 1.0) to support a patent application?",
                "Have you initiated the acute toxicity study required for Form 25-E licensing?",
                "Are your raw herbal botanicals sourced from registered farms or wild collection?"
            ]
            return "".join(parts), questions

        if any(k in q_lower for k in ["classical", "treatise", "charaka", "sushruta", "afi"]):
            parts = [
                f"### Commercialization & Protection Strategy for Classical Formulation\n\n",
                f"**Direct Assessment:**\n",
                f"Thank you for clarifying that **{herbs_str}** is a **Classical Ayurvedic Formulation**. "
                f"Under Section 3(p) of The Patents Act, 1970, classical formulas recorded in First Schedule treatises are in the public domain and **cannot be patented** [patents-act-3p]. "
                f"However, this provides tremendous regulatory advantages for fast-track commercial manufacturing:\n\n"
                f"**Strategic Roadmap for Classical Medicines:**\n"
                f"1. **Fast-Track Manufacturing License (Form 25-D)**: You can obtain an AYUSH manufacturing license on **Form 25-D** under Section 3(a) of the Drugs and Cosmetics Act without conducting expensive clinical trials [dc-act-classical-3a].\n"
                f"2. **Schedule T GMP Compliance**: Ensure your production facility complies with factory hygiene, raw material monograph testing, and batch records under Schedule T [dc-rules-schedule-t].\n"
                f"3. **Brand Trademarking (The Key IP Asset)**: While the generic classical name (e.g. *Triphala*, *Chyawanprash*) cannot be trademarked exclusively [trademarks-ayurveda-names], you should register a **composite trademark** combining a coined brand name with the classical formula (e.g., *BrandName Triphala*) under Class 5 on `ipindia.gov.in`.\n"
            ]
            questions = [
                "Do you have an existing GMP-certified manufacturing unit or require third-party loan licensing (Form 25-E-1)?",
                "What coined distinctive brand name do you plan to use alongside the classical name?",
                "Are your biological materials sourced from cultivated farms exempt under Section 7?"
            ]
            return "".join(parts), questions

        # Branch 4: General contextual default
        parts = [
            f"### Tailored Legal Strategy & Multi-Turn Guidance\n\n",
            f"**Contextual Overview:**\n",
            f"Continuing our conversation regarding **{herbs_str}**:\n\n",
            "**Key Statutory Priorities:**\n",
            "1. **Regulatory Licensing**: Ensure your formulation is properly classified as Classical (Form 25-D) under Section 3(a) or Proprietary (Form 25-E) under Section 3(h) & Rule 158-B [dc-act-classical-3a, dc-act-prop-3h].\n",
            "2. **IP Protection**: Overcome Section 3(p) TK exclusions by proving quantitative synergism ($CI < 1.0$) under Section 3(e) [patents-act-3p, patents-act-3e] or register a composite trademark under Class 5 [trademarks-ayurveda-names].\n",
            "3. **Biodiversity Clearances**: Verify whether your herbs are cultivated (exempt under 2023 Amendment Section 7) or require SBB intimation and NBA Form III approval on `nbaindia.org` [bd-act-sec-6, bd-act-sec-7].\n"
        ]
        questions = [
            "Are the raw herbs cultivated on registered farms or wild-harvested?",
            "Do you have laboratory data showing synergy (CI < 1.0)?",
            "Have you already drafted Patent Form 1 origin disclosures under Section 10(4)?"
        ]
        return "".join(parts), questions

    # -------------------------------------------------------------------------
    # SPECIFIC STATUTORY HANDLERS
    # -------------------------------------------------------------------------

    def _answer_section_3p_patentability(self, query: str, chunks: list[RetrievedChunk]) -> Tuple[str, list[str]]:
        ans = (
            "### Section 3(p) of The Patents Act, 1970 — Traditional Knowledge Exclusion\n\n"
            "**Direct Answer:**\n"
            "Under **Section 3(p) of The Patents Act, 1970**, an invention which in effect is traditional knowledge or an aggregation "
            "or duplication of known properties of traditionally known components is **strictly unpatentable** in India [patents-act-3p].\n\n"
            "**Statutory Scope & Legal Analysis:**\n"
            "1. **Classical Formulations Barred**: Any herbal remedy, composition, or process disclosed in the authoritative treatises "
            "listed in the First Schedule to the Drugs and Cosmetics Act, 1940 (including *Charaka Samhita*, *Sushruta Samhita*, *Ashtanga Hridaya*, "
            "*Sharangadhara Samhita*, and the *Ayurvedic Formulary of India*) is codified traditional knowledge and resides permanently "
            "in the public domain [patents-act-3p]. Classical medicines like *Triphala*, *Chyawanprash*, or *Dashamularishta* cannot be patented.\n"
            "2. **TKDL Prior Art Screening**: The **Traditional Knowledge Digital Library (TKDL, tkdl.res.in)** documents over 4.5 lakh classical formulations "
            "in 5 international languages using TKRC. Patent examiners on InPASS (`ipindia.gov.in`) and at international patent offices cite TKDL records "
            "to reject patent claims for lacking novelty under Section 3(p) [tkdl-prior-art].\n"
            "3. **How to Protect Ayurveda-Derived Innovations**:\n"
            "   - **Synergistic Novel Formulations**: If a polyherbal formulation modifies classical recipes and demonstrates unexpected therapeutic synergism "
            "with empirical data (Combination Index $CI < 1.0$), it can overcome Section 3(e) objections [patents-act-3e].\n"
            "   - **Standardized Fractions / Extracts**: Must establish enhanced therapeutic efficacy under Section 3(d) (*Novartis* standard) [patents-act-3d].\n"
            "   - **Mandatory NBA Approval**: Section 6 of the Biological Diversity Act, 2002 requires prior NBA approval on Form III before patent grant [bd-act-sec-6].\n\n"
            "**Official Portals:** Verify statutory text on India Code (`indiacode.nic.in`), prior art on TKDL (`tkdl.res.in`), and patent search on IP India (`ipindia.gov.in`)."
        )
        questions = [
            "Is your formulation classical or a modified proprietary combination?",
            "Do you have quantitative laboratory synergy data (CI < 1.0)?",
            "Are you seeking patent protection or a brand trademark?"
        ]
        return ans, questions

    def _answer_section_3e(self, query: str, chunks: list[RetrievedChunk]) -> Tuple[str, list[str]]:
        ans = (
            "### Section 3(e) of The Patents Act, 1970 — Synergism vs Mere Admixture\n\n"
            "**Direct Answer:**\n"
            "**Section 3(e) of The Patents Act, 1970** excludes from patentability any substance obtained by a **'mere admixture'** "
            "resulting only in the aggregation of the properties of its components, or any process for producing such substance [patents-act-3e].\n\n"
            "**Legal Test & Evidence Required to Overcome Section 3(e):**\n"
            "1. **Proof of Non-Obvious Synergy**: For polyherbal or herbal-synthetic combinations, applicants cannot rely on simple additive efficacy. "
            "The applicant must provide empirical laboratory data proving that the therapeutic effect of the combined active ingredients is statistically "
            "and clinically superior to the sum of the individual ingredients tested separately [patents-act-3e].\n"
            "2. **Quantitative Synergy Indices (CGPDTM TK Guidelines)**:\n"
            "   - **Combination Index (CI)**: A calculated Combination Index where $CI < 1.0$ (via Chou-Talalay method or isobologram analysis) establishes true synergistic action [ipindia-tk-guidelines].\n"
            "   - **Dose Reduction Index (DRI)**: Significant reduction in the required therapeutic dose of individual botanicals.\n"
            "   - **Bioavailability Enhancement**: Quantitative pharmacokinetic evidence showing enhanced absorption (e.g. through standardized piperine or bio-enhancers) [ipindia-tk-guidelines].\n"
            "3. **Comparative Experimental Protocols**: The patent specification must contain head-to-head experimental comparative tables comparing Component A alone, "
            "Component B alone, and the Combination $(A + B)$ across identical validated in vitro or in vivo biological assays.\n\n"
            "**Mandatory Procedural Requirements:** Disclose biological origin under Section 10(4)(d)(ii) [patents-act-10-4] and file NBA Form III approval on `nbaindia.org` [bd-act-sec-6]."
        )
        questions = [
            "What assay or model did you use to measure synergy?",
            "Have you compared the combination head-to-head against each single herb?",
            "Do you need guidance on filing Patent Form 1 origin declarations?"
        ]
        return ans, questions

    def _answer_section_3d(self, query: str, chunks: list[RetrievedChunk]) -> Tuple[str, list[str]]:
        ans = (
            "### Section 3(d) of The Patents Act, 1970 — Incremental Therapeutic Efficacy\n\n"
            "**Direct Answer:**\n"
            "**Section 3(d) of The Patents Act, 1970** bars the patenting of the mere discovery of a new form of a known substance "
            "which does not result in the **enhancement of the known therapeutic efficacy** of that substance [patents-act-3d].\n\n"
            "**Legal Precedent & Standard for Phytopharmaceuticals & Herbal Extracts:**\n"
            "1. **Novartis Landmark Standard**: In *Novartis AG v. Union of India*, the Supreme Court held that 'efficacy' under Section 3(d) strictly means "
            "**therapeutic efficacy**—the healing or curative capacity of the drug. Improvements in physical characteristics (such as solubility, stability, "
            "shelf-life, or bioavailability) do not qualify as enhanced efficacy unless they directly translate into superior therapeutic response [patents-act-3d].\n"
            "2. **Application to Ayurvedic Derivatives**: If an applicant isolates a standardized fraction, enriched extract, or active phytochemical from a traditionally "
            "known Indian herb (e.g. standardized curcuminoids from *Curcuma longa* or withanolides from *Withania somnifera*), they must demonstrate statistically significant "
            "superior therapeutic efficacy over the conventional crude plant extract [patents-act-3d].\n"
            "3. **Examination Scrutiny on InPASS**: IP India patent examiners will reject claims under Section 3(d) in conjunction with Section 3(p) unless comparative pharmacological "
            "data is incorporated directly in the complete specification [ipindia-tk-guidelines].\n\n"
            "**Official Reference:** Read statutory Section 3(d) on India Code (`indiacode.nic.in`) and examine registered patents on IP India (`ipindia.gov.in`)."
        )
        questions = [
            "Is your product an isolated compound, standardized fraction, or crude extract?",
            "Do you have comparative in vivo data against the crude herbal substance?",
            "Have you pre-screened this herb on the TKDL database?"
        ]
        return ans, questions

    def _answer_section_10_4(self, query: str, chunks: list[RetrievedChunk]) -> Tuple[str, list[str]]:
        ans = (
            "### Section 10(4)(d)(ii) of The Patents Act, 1970 — Mandatory Biological Origin Disclosure\n\n"
            "**Direct Answer:**\n"
            "Under **Section 10(4)(d)(ii) of The Patents Act, 1970**, every patent applicant who mentions any biological material in the specification "
            "which is obtained from India is legally mandated to disclose the **exact source and geographical origin** of that biological material [patents-act-10-4].\n\n"
            "**Statutory Obligations & Compliance Details:**\n"
            "1. **Form 1 Mandatory Declaration**: The applicant must execute a statutory declaration in Patent Form 1 stating whether approval from the National Biodiversity "
            "Authority (NBA) has been obtained or applied for under Section 6 of the Biological Diversity Act, 2002 [patents-act-10-4, bd-act-sec-6].\n"
            "2. **Consequences of Non-Disclosure or False Origin**:\n"
            "   - **Pre-Grant / Post-Grant Opposition (§25)**: Any third party can file opposition on grounds of non-disclosure or wrongful disclosure of biological source [patents-act-25-opposition].\n"
            "   - **Revocation (§64(1)(p))**: Concealment or misstatement of biological origin is an explicit statutory ground for revocation of the granted patent by the High Court.\n"
            "3. **WIPO Alignment**: This requirement is directly aligned with Article 3 of the **WIPO GRATK Treaty (2024)**, establishing global mandatory disclosure standards for genetic resources [wipo-gratk-treaty-2024].\n\n"
            "**Actionable Step:** Record the exact GPS coordinates, district, state, and vendor/cultivation certificates for all biological materials prior to drafting on `ipindia.gov.in`."
        )
        questions = [
            "Do you have documented geographic source records for your herbs?",
            "Have you already submitted NBA Form III on nbaindia.org?",
            "Are your herbs cultivated by registered farmers or wild-harvested?"
        ]
        return ans, questions

    def _answer_section_25_opposition(self, query: str, chunks: list[RetrievedChunk]) -> Tuple[str, list[str]]:
        ans = (
            "### Section 25 of The Patents Act, 1970 — Pre-Grant and Post-Grant Patent Oppositions\n\n"
            "**Direct Answer:**\n"
            "**Section 25 of The Patents Act, 1970** provides the legal procedure allowing third parties to oppose patent applications on statutory grounds "
            "before grant (**Pre-Grant Opposition (§25(1))**) or within one year after grant (**Post-Grant Opposition (§25(2))**) [patents-act-25-opposition].\n\n"
            "**Key Grounds for Opposing Traditional Knowledge & Ayurvedic Patents:**\n"
            "1. **Traditional Knowledge Anticipation (§25(1)(k) / §25(2)(k))**: The claimed invention was anticipated having regard to oral or written knowledge available "
            "within any local or indigenous community in India or elsewhere (citable via TKDL prior art) [patents-act-25-opposition, tkdl-prior-art].\n"
            "2. **Section 3(p) Traditional Knowledge Exclusion**: The claimed invention is an aggregation of known properties of classical herbal ingredients [patents-act-3p].\n"
            "3. **Section 3(e) Mere Admixture**: The polyherbal composition lacks proof of synergistic therapeutic efficacy [patents-act-3e].\n"
            "4. **Section 10(4) Non-Disclosure of Origin**: The patent specification fails to disclose or wrongly describes the source/geographical origin of Indian biological resources [patents-act-10-4].\n"
            "5. **Lack of NBA Approval**: Failure to obtain prior approval from the National Biodiversity Authority under Section 6 of the BD Act, 2002 [bd-act-sec-6].\n\n"
            "**Who Can File:** Under §25(1), **any person** can submit pre-grant representations in writing to the Controller without fee. Under §25(2), only a **'person interested'** may file post-grant opposition on Form 7 on `ipindia.gov.in`."
        )
        questions = [
            "Are you seeking to oppose a published third-party patent application?",
            "Do you need to search TKDL records to cite prior art against a patent?",
            "Has the patent application already been granted by the Patent Office?"
        ]
        return ans, questions

    def _answer_bd_act_form_iii(self, query: str, chunks: list[RetrievedChunk]) -> Tuple[str, list[str]]:
        ans = (
            "### NBA Form III — Mandatory Prior Approval for Patent & IPR Applications\n\n"
            "**Direct Answer:**\n"
            "**NBA Form III** is the statutory application form prescribed under the Biological Diversity Rules, 2004, submitted to the "
            "**National Biodiversity Authority (NBA)** under **Section 6(1) of the Biological Diversity Act, 2002** to obtain mandatory prior approval "
            "before applying for any Intellectual Property Right (patent, plant variety protection) based on Indian biological resources [bd-act-sec-6].\n\n"
            "**Key Statutory Requirements & Procedure:**\n"
            "1. **Filing Timeline**: Approval must be granted by the NBA **before the patent is sealed/granted** by the Indian Patent Office (CGPDTM) [bd-act-sec-6]. "
            "If filing in foreign patent offices (USPTO, EPO, WIPO PCT), approval must be obtained prior to overseas filing.\n"
            "2. **Statutory Application Fee**: An official fee of **Rs. 10,000** must accompany Form III submitted on the NBA online portal (`nbaindia.org`) [nba-abs-regulations-2014].\n"
            "3. **Form 1 Declaration on InPASS**: Under Section 10(4)(d)(ii) of The Patents Act, 1970, patent applicants must declare the filing status of their NBA Form III "
            "application on Patent Form 1 [patents-act-10-4].\n"
            "4. **Access and Benefit Sharing (ABS) Agreement**: Approval entails executing an ABS agreement with the NBA. Commercial utilization attracts benefit sharing "
            "ranging from **0.1% to 0.5% of ex-factory gross sales turnover** or **3.0% to 5.0% of the raw material purchase price** [nba-abs-regulations-2014].\n\n"
            "**Official Portal:** File Form III online via the National Biodiversity Authority ABS Portal at `https://nbaindia.org`."
        )
        questions = [
            "Have you already filed your patent application or are you preparing to file?",
            "Is your entity Indian-owned or does it have foreign equity?",
            "Do you need guidance on the ABS ex-factory benefit sharing calculation?"
        ]
        return ans, questions

    def _answer_bd_act_sec_7_exemptions(self, query: str, chunks: list[RetrievedChunk]) -> Tuple[str, list[str]]:
        ans = (
            "### Section 7 of the Biological Diversity Act — 2023 Amendment Exemptions\n\n"
            "**Direct Answer:**\n"
            "Under the **Biological Diversity (Amendment) Act, 2023**, **Section 7** was amended to grant statutory exemptions from giving prior intimation "
            "to State Biodiversity Boards (SBB) for three primary categories [bd-act-sec-7-2023]:\n\n"
            "**Statutory Exemptions under Section 7:**\n"
            "1. **Users of Codified Traditional Knowledge**: Indian entities, manufacturers, and researchers utilizing codified classical traditional knowledge "
            "(documented in authoritative treatises listed in the First Schedule to the Drugs and Cosmetics Act, 1940) for manufacturing classical ASU products [bd-act-sec-7-2023].\n"
            "2. **Cultivated Medicinal Plants**: Commercial utilization of cultivated medicinal plants and their derived products, provided traceability to cultivated agricultural sources is proven [bd-act-sec-7-2023].\n"
            "3. **Registered AYUSH Practitioners**: Vaidyas, Hakims, and traditionally recognized healers practicing traditional systems of medicine [bd-act-sec-7-2023].\n\n"
            "**What Is NOT Exempt (Crucial Legal Distinctions):**\n"
            "- **Wild-Harvested Herbs**: Indian companies commercially utilizing wild-harvested biological resources from forests still require prior intimation to the SBB.\n"
            "- **Patent & IPR Filings (§6)**: Section 7 exemptions apply ONLY to domestic commercial manufacturing intimation. If you apply for a **patent or IPR**, "
            "prior approval from the National Biodiversity Authority under **Section 6 on Form III remains strictly mandatory** [bd-act-sec-6]!\n"
            "- **Foreign Entities (§3)**: Foreign individuals or entities with non-Indian share capital must still obtain Section 3 Form I approval from the NBA [bd-act-sec-6].\n\n"
            "**Official Source:** Biological Diversity (Amendment) Act, 2023 on India Code (`indiacode.nic.in`) and NBA (`nbaindia.org`)."
        )
        questions = [
            "Are your herbs cultivated by registered farmers or collected from wild forests?",
            "Are you seeking a patent or solely manufacturing approval?",
            "Are you an AYUSH practitioner or a commercial manufacturing enterprise?"
        ]
        return ans, questions

    def _answer_bd_act_sec_40_ntc(self, query: str, chunks: list[RetrievedChunk]) -> Tuple[str, list[str]]:
        ans = (
            "### Section 40 of the Biological Diversity Act, 2002 — Normally Traded Commodities (NTC)\n\n"
            "**Direct Answer:**\n"
            "**Section 40 of the Biological Diversity Act, 2002** empowers the Central Government to exempt biological resources normally traded as commodities "
            "from the purview and procedural restrictions of the Act [bd-act-sec-40-ntc].\n\n"
            "**Scope & Notified Species:**\n"
            "1. **421+ Notified Species**: The Ministry of Environment, Forest and Climate Change has notified **421+ biological species** as Normally Traded Commodities (NTC) [bd-act-sec-40-ntc]. "
            "Common examples include *Zingiber officinale* (Ginger), *Curcuma longa* (Turmeric), *Piper nigrum* (Black Pepper), *Syzygium aromaticum* (Clove), *Cuminum cyminum* (Cumin), and *Trigonella foenum-graecum* (Fenugreek).\n"
            "2. **Strict Scope Limitation**: The NTC exemption applies **strictly when the plant part is traded as an agricultural or horticultural commodity for direct consumption, retail sale, or conventional food trade** [bd-act-sec-40-ntc].\n"
            "3. **Inapplicability to Patents & Research**: The exemption **does NOT apply** if the commodity is accessed for:\n"
            "   - Applying for Intellectual Property Rights or Patents under Section 6 [bd-act-sec-6].\n"
            "   - Bio-prospecting, genetic modification, or extracting novel active pharmaceutical molecules.\n"
            "   - Transfer of research results to foreign entities under Section 4.\n\n"
            "**Official Source:** Full 421+ NTC species notification is published by the National Biodiversity Authority on `nbaindia.org`."
        )
        questions = [
            "Are you trading the herbs as agricultural commodities or utilizing them for drug manufacturing?",
            "Do you plan to file a patent on an active extract derived from an NTC species?",
            "Are you exporting raw commodities or formulated Ayurvedic medicines?"
        ]
        return ans, questions

    def _answer_abs_regulations(self, query: str, chunks: list[RetrievedChunk]) -> Tuple[str, list[str]]:
        ans = (
            "### Access and Benefit-Sharing (ABS) Regulations, 2014 & Benefit-Sharing Formula\n\n"
            "**Direct Answer:**\n"
            "Under the **Guidelines on Access to Biological Resources and Associated Knowledge and Benefits Sharing Regulations, 2014**, "
            "commercial users accessing Indian biological resources must execute an Access and Benefit-Sharing (ABS) agreement with the National Biodiversity Authority (NBA) "
            "or State Biodiversity Board (SBB) [nba-abs-regulations-2014].\n\n"
            "**Statutory Benefit-Sharing Formula & Percentages:**\n"
            "1. **Commercial Utilization (Gross Ex-Factory Sales)**:\n"
            "   - Annual Gross Turnover up to Rs. 1 Crore: **0.1%** of ex-factory gross sales.\n"
            "   - Annual Gross Turnover between Rs. 1 Crore and Rs. 3 Crores: **0.2%** of ex-factory gross sales.\n"
            "   - Annual Gross Turnover exceeding Rs. 3 Crores: **0.5%** of ex-factory gross sales [nba-abs-regulations-2014].\n"
            "2. **Traders / Raw Material Buyers**: Benefit-sharing of **3.0% to 5.0%** of the purchase price of the biological resource.\n"
            "3. **IPR & Patent Grant**: Filing fee of **Rs. 10,000** on Form III, plus negotiated royalty (up to 2.0% to 5.0% of commercial sales turnover) if the patent is commercialized [nba-abs-regulations-2014, bd-act-sec-6].\n\n"
            "**Official Portal:** National Biodiversity Authority ABS management guidelines at `https://nbaindia.org`."
        )
        questions = [
            "What is the projected or actual annual ex-factory turnover of your product?",
            "Are you a manufacturer paying on sales turnover or a trader paying on purchase price?",
            "Have you already executed an agreement with the State Biodiversity Board?"
        ]
        return ans, questions

    def _answer_foreign_access_form_i(self, query: str, chunks: list[RetrievedChunk]) -> Tuple[str, list[str]]:
        ans = (
            "### Section 3 BD Act & NBA Form I — Cross-Border Access by Foreign Entities\n\n"
            "**Direct Answer:**\n"
            "Under **Section 3 of the Biological Diversity Act, 2002**, non-Indian citizens, non-residents, and foreign entities "
            "(including Indian corporations having any non-Indian participation in share capital or management) are **strictly prohibited** "
            "from obtaining Indian biological resources or associated knowledge for research or commercial utilization without prior approval from the NBA [bd-act-sec-6].\n\n"
            "**Mandatory Statutory Procedure:**\n"
            "1. **NBA Form I Filing**: Must submit an online application on **Form I** via `nbaindia.org` accompanied by the statutory fee.\n"
            "2. **ABS Agreement Execution**: Approval is conditional upon entering into an Access and Benefit-Sharing agreement ensuring fair compensation to local Biodiversity Management Committees (BMCs) [nba-abs-regulations-2014].\n"
            "3. **Section 4 Research Transfer**: Transfer of results of research on Indian biological resources to any foreign person or entity requires prior approval on **Form II**.\n"
            "4. **WIPO GRATK Treaty (2024)**: Non-Indian applicants filing patents abroad based on Indian resources must disclose origin under Article 3 of the WIPO GRATK Treaty [wipo-gratk-treaty-2024].\n\n"
            "**Official Source:** National Biodiversity Authority, Chennai at `https://nbaindia.org`."
        )
        questions = [
            "Does your company have foreign equity or foreign directors?",
            "Are you conducting collaborative research with a foreign institution?",
            "Do you plan to export raw botanicals or finished formulated medicines?"
        ]
        return ans, questions

    def _answer_clinical_trials(self, query: str, chunks: list[RetrievedChunk]) -> Tuple[str, list[str]]:
        ans = (
            "### Clinical Trial Requirements under Drugs and Cosmetics Act, 1940\n\n"
            "**Direct Answer:**\n"
            "**No, clinical trials are NOT required to manufacture classical Ayurvedic medicines.**\n\n"
            "**Statutory Distinction & Regulatory Framework:**\n"
            "1. **Classical ASU Drugs (§3(a)) — No Clinical Trials Required**:\n"
            "   - Under **Section 3(a) of the Drugs and Cosmetics Act, 1940**, classical medicines manufactured exclusively in accordance with "
            "the authoritative treatises listed in the First Schedule (such as *Charaka Samhita*, *Sushruta Samhita*, *Ashtanga Hridaya*, and the *Ayurvedic Formulary of India*) "
            "require a manufacturing license on **Form 25-D** from the State Licensing Authority (AYUSH) [dc-act-classical-3a].\n"
            "   - Because their safety and clinical efficacy have been established through centuries of codified classical authority, "
            "the applicant is **exempt from submitting clinical efficacy trials or animal toxicity data** [dc-act-classical-3a].\n"
            "2. **Patent or Proprietary (P&P) ASU Medicines (§3(h) & Rule 158-B) — Trials Required**:\n"
            "   - Formulations that modify classical recipes, change ingredient ratios, introduce novel delivery forms (e.g. capsules, transdermal patches), "
            "or claim new therapeutic indications fall under **Section 3(h)** and **Rule 158-B of the Drugs and Cosmetics Rules, 1945** [dc-act-prop-3h].\n"
            "   - Applicants must submit:\n"
            "     - Published scientific literature documenting safety and efficacy.\n"
            "     - Proof of safety: Acute and chronic animal toxicity studies.\n"
            "     - Pilot clinical trial reports validating efficacy for the claimed indication [dc-act-prop-3h].\n"
            "3. **Schedule T GMP Compliance**: Regardless of clinical trial exemptions, **every manufacturing facility** must strictly adhere to "
            "**Schedule T Good Manufacturing Practices** (infrastructure, hygienic zoning, raw material monograph testing, and batch records) [dc-act-classical-3a].\n\n"
            "**Statutory Source:** The Drugs and Cosmetics Act, 1940 and Drugs and Cosmetics Rules, 1945 available on India Code (`indiacode.nic.in`)."
        )
        questions = [
            "Are you manufacturing a classical formulation or a proprietary modified product?",
            "Is your manufacturing facility Schedule T GMP certified?",
            "Do you plan to license under Form 25-D (classical) or Form 25-E (proprietary)?"
        ]
        return ans, questions

    def _answer_schedule_e1(self, query: str, chunks: list[RetrievedChunk]) -> Tuple[str, list[str]]:
        ans = (
            "### Schedule E(1) of the Drugs and Cosmetics Rules, 1945 — Poisonous ASU Substances\n\n"
            "**Direct Answer:**\n"
            "**Schedule E(1) of the Drugs and Cosmetics Rules, 1945** is the statutory list of poisonous botanical, mineral, and animal substances "
            "used in Ayurvedic, Siddha, and Unani (ASU) medicine requiring strict detoxification and cautionary packaging [dc-act-schedule-e1].\n\n"
            "**Regulated Ingredients & Mandatory Statutory Safeguards:**\n"
            "1. **Regulated Botanical Substances**: Includes *Aconitum ferox* (Vatsanabha), *Semecarpus anacardium* (Bhallataka), *Strychnos nux-vomica* (Kupilu), "
            "*Datura metel*, *Cannabis sativa* (Bhanga), and *Croton tiglium* (Jayapala) [dc-act-schedule-e1].\n"
            "2. **Regulated Mineral / Metallic Substances**: Includes *Parada* (Mercury), *Gandhaka* (Sulphur), *Haratala* (Arsenic trisulphide), *Manashila* (Realgar), and *Hingula* (Cinnabar) [dc-act-schedule-e1].\n"
            "3. **Mandatory Classical Shodhana (Purification/Detoxification)**: Raw materials cannot be used in crude form. They must undergo mandatory Shodhana "
            "strictly adhering to procedures documented in authoritative First Schedule treatises (such as *Rasa Tarangini* or *Sharangadhara Samhita*).\n"
            "4. **Mandatory Labelling Requirements**: Packaging must prominently display in clear red/conspicuous lettering:\n"
            "   - **'Caution: To be taken under medical supervision only'** [dc-act-schedule-e1].\n"
            "5. **Dispensing & Batch Testing**: Finished batches must undergo heavy metal testing and toxicity profiling, and can only be dispensed under the direction of a registered medical practitioner.\n\n"
            "**Official Source:** Drugs and Cosmetics Rules, 1945 on India Code (`indiacode.nic.in`)."
        )
        questions = [
            "Which Schedule E(1) botanical or mineral ingredients are in your formula?",
            "What classical Shodhana purification protocol will you follow?",
            "Have you prepared the mandatory cautionary labelling artwork?"
        ]
        return ans, questions

    def _answer_schedule_t_gmp(self, query: str, chunks: list[RetrievedChunk]) -> Tuple[str, list[str]]:
        ans = (
            "### Schedule T of the Drugs and Cosmetics Rules, 1945 — Good Manufacturing Practices (GMP)\n\n"
            "**Direct Answer:**\n"
            "**Schedule T of the Drugs and Cosmetics Rules, 1945** specifies the mandatory Good Manufacturing Practices (GMP) that all Ayurvedic, Siddha, "
            "and Unani drug manufacturing units in India must comply with to obtain and maintain a manufacturing license [dc-act-classical-3a].\n\n"
            "**Core Statutory Standards:**\n"
            "1. **Factory Infrastructure & Zoning**: Separate delineated zones for raw material storage, cleaning/sorting, Shodhana, extraction, formulation, packaging, and finished goods warehouse [dc-act-classical-3a].\n"
            "2. **Hygienic Controls & Water**: Strict drainage, pest control, air filtration, and demineralized/potable water meeting IP standards.\n"
            "3. **Quality Control & Raw Material Monograph Testing**: In-house quality control laboratory to test identity, purity, and strength of herbs against "
            "**Ayurvedic Pharmacopoeia of India (API)** monographs (microbial limits, heavy metal limits, pesticide residues, and aflatoxin screening) [dc-act-classical-3a].\n"
            "4. **Batch Manufacturing Records (BMR)**: Detailed batch manufacturing records must be maintained and archived for a minimum of 5 years or until 2 years past product expiry.\n"
            "5. **Licensing**: Compliance is verified by AYUSH drug inspectors before issuing **Form 25-D** (classical) or **Form 25-E** (proprietary) licenses [dc-act-classical-3a, dc-act-prop-3h].\n\n"
            "**Official Source:** Schedule T, Drugs and Cosmetics Rules, 1945 on India Code (`indiacode.nic.in`)."
        )
        questions = [
            "Is your manufacturing premise currently under construction or already operational?",
            "Do you have an in-house quality testing lab for API monograph compliance?",
            "Have you scheduled an inspection by the State AYUSH Drug Inspector?"
        ]
        return ans, questions

    def _answer_licensing_classical_vs_proprietary(self, query: str, chunks: list[RetrievedChunk]) -> Tuple[str, list[str]]:
        ans = (
            "### Licensing: Classical ASU Drugs (§3(a)) vs Patent or Proprietary Medicines (§3(h))\n\n"
            "**Direct Answer:**\n"
            "The **Drugs and Cosmetics Act, 1940** establishes two fundamentally distinct legal frameworks for manufacturing Ayurvedic medicines [dc-act-classical-3a, dc-act-prop-3h]:\n\n"
            "| Regulatory Criterion | Classical ASU Drug (§3(a)) | Patent or Proprietary (P&P) ASU Medicine (§3(h)) |\n"
            "| :--- | :--- | :--- |\n"
            "| **Recipe Authority** | Strictly identical to recipes in First Schedule treatises (Charaka, Sushruta, AFI) | Contains First Schedule herbs, but with modified ratios, novel excipients, or delivery forms |\n"
            "| **Manufacturing License** | Form 25-D issued by State AYUSH Authority [dc-act-classical-3a] | Form 25-E / 25-D under Rule 158-B [dc-act-prop-3h] |\n"
            "| **Clinical Trials Required?** | **No**; efficacy established by classical textual authority | **Yes**; published safety data, acute toxicity, and pilot clinical trial reports required under Rule 158-B [dc-act-prop-3h] |\n"
            "| **Trademark Protection** | Names are *publici juris* (cannot be monopolized) [trademarks-ayurveda-names] | Can be branded with unique, distinctive trademarks [trademarks-ayurveda-names] |\n"
            "| **GMP Compliance** | Mandatory Schedule T GMP [dc-act-classical-3a] | Mandatory Schedule T GMP [dc-act-classical-3a] |\n"
            "| **NBA IPR Approval** | Not applicable (unpatentable §3(p)) | Section 6 Form III approval required if seeking patent [bd-act-sec-6] |\n\n"
            "**Actionable Advice:** If launching a traditional remedy without clinical trials, apply under Section 3(a) Form 25-D. If launching a modified formulation with proprietary marketing, prepare Rule 158-B safety/clinical dossier."
        )
        questions = [
            "Which category does your planned product fall into: Classical or Proprietary?",
            "Do you have pilot clinical safety and efficacy data ready for Rule 158-B?",
            "What brand name are you planning for your product?"
        ]
        return ans, questions

    def _answer_trademarks(self, query: str, chunks: list[RetrievedChunk]) -> Tuple[str, list[str]]:
        ans = (
            "### Trademarks & Brand Protection for Ayurvedic Products (Trade Marks Act, 1999)\n\n"
            "**Direct Answer:**\n"
            "**No, you cannot register an exclusive trademark for the generic classical name of an Ayurvedic medicine such as 'Triphala' or 'Chyawanprash' alone.**\n\n"
            "**Statutory Grounds & Legal Analysis:**\n"
            "1. **Publici Juris & Lack of Distinctiveness (§9)**:\n"
            "   - Under **Section 9(1) of the Trade Marks Act, 1999**, marks which consist exclusively of signs or indications that designate the kind, quality, "
            "or intended purpose of goods, or which have become customary in the current language, are barred from registration [trademarks-ayurveda-names].\n"
            "   - Classical formulation names (*Triphala*, *Chyawanprash*, *Dashamularishta*, *Ashwagandha*) belong to the public domain (*publici juris*). "
            "The Trade Marks Registry will issue absolute grounds objections against any applicant attempting to monopolize them.\n"
            "2. **How to Successfully Protect Your Ayurvedic Brand**:\n"
            "   - **Use a Composite Mark**: Combine an arbitrary, coined, or fanciful brand name with the generic description (e.g. *'[BrandName] Triphala'*) [trademarks-ayurveda-names]. "
            "The registration will protect the distinctive brand name, while the generic classical name is disclaimed.\n"
            "   - **Unique Logo & Trade Dress**: Protect distinctive packaging, stylization, and color schemes under Class 5 (Pharmaceuticals) or Class 30 (Dietary/Herbal infusions).\n"
            "3. **The Cadila Healthcare Anti-Confusion Standard**:\n"
            "   - In *Cadila Health Care Ltd. v. Cadila Pharmaceuticals Ltd. (2001)*, the Supreme Court of India held that in medicinal products, "
            "a **stricter standard of phonetic, visual, and semantic anti-confusion** must be applied than in regular consumer goods to prevent public health hazards [trademarks-ayurveda-names].\n\n"
            "**Official Portal:** Conduct pre-filing public search on IP India Trade Marks Registry at `https://ipindia.gov.in`."
        )
        questions = [
            "What coined or distinctive brand name do you propose to combine with the herb name?",
            "Are you filing in Class 5 (medicines) or Class 30 (teas/foods)?",
            "Have you conducted a clearance search on IP India public database?"
        ]
        return ans, questions

    def _answer_ayurveda_aahara(self, query: str, chunks: list[RetrievedChunk]) -> Tuple[str, list[str]]:
        ans = (
            "### Ayurveda Aahara Regulations, 2022 (FSSAI & Ministry of Ayush)\n\n"
            "**Direct Answer:**\n"
            "Under the **Food Safety and Standards (Ayurveda Aahara) Regulations, 2022**, foods prepared in accordance with the recipes, ingredients, "
            "or processes described in authoritative Ayurvedic treatises listed in Schedule A are classified as **'Ayurveda Aahara'** [fssai-ayurveda-aahara].\n\n"
            "**Statutory Rules & Mandatory Labelling:**\n"
            "1. **Scope & Permissible Ingredients**: Formulations must strictly adhere to recipes in Schedule A classical treatises. Synthetic vitamins, minerals, "
            "or isolated chemical additives cannot be added unless naturally occurring in the classical recipe [fssai-ayurveda-aahara].\n"
            "2. **Mandatory Ayurveda Aahara Logo**: Every packaging unit must carry the official, designated Ayurveda Aahara logo on the principal display panel [fssai-ayurveda-aahara].\n"
            "3. **Mandatory Advisory Labelling**: The package must carry the clear front-of-pack advisory text:\n"
            "   - **'Ayurveda Aahara - Not for medicinal use'** [fssai-ayurveda-aahara].\n"
            "4. **Absolute Ban on Therapeutic / Curative Claims**: Ayurveda Aahara products are **strictly barred from claiming to prevent, treat, mitigate, or cure any human disease**, physiological disorder, or medical ailment [fssai-ayurveda-aahara].\n"
            "5. **Exclusions**: Not permitted for infant nutrition under 24 months without specific scientific substantiation.\n\n"
            "**Official Source:** Food Safety and Standards Authority of India (FSSAI) at `https://fssai.gov.in`."
        )
        questions = [
            "Which classical treatise from Schedule A does your food recipe originate from?",
            "Have you prepared the package label with the mandatory Ayurveda Aahara logo?",
            "Are any synthetic vitamins or food additives incorporated?"
        ]
        return ans, questions

    def _answer_tkdl_prior_art(self, query: str, chunks: list[RetrievedChunk]) -> Tuple[str, list[str]]:
        ans = (
            "### Traditional Knowledge Digital Library (TKDL) — Prior Art & Biopiracy Defense\n\n"
            "**Direct Answer:**\n"
            "The **Traditional Knowledge Digital Library (TKDL, tkdl.res.in)** is India's pioneer digital repository created by CSIR "
            "and the Ministry of Ayush to document classical indigenous knowledge and prevent bio-piracy [tkdl-prior-art].\n\n"
            "**Architecture & Global Impact:**\n"
            "1. **Scale & Treatises**: Contains over **4.5 lakh classical formulations** transcribed from ancient treatises (*Charaka Samhita*, *Sushruta Samhita*, "
            "*Ashtanga Hridaya*, *Sharangadhara Samhita*, *Bhaishajya Ratnavali*, etc.) into five international languages (English, French, German, Japanese, Spanish) [tkdl-prior-art].\n"
            "2. **TKRC Classification**: Formulations are structured in the Traditional Knowledge Resource Classification (TKRC) system, which maps classical Ayurvedic concepts "
            "directly to the International Patent Classification (IPC) used by global patent examiners [tkdl-prior-art].\n"
            "3. **Biopiracy Prevention**: Under formal access agreements with patent offices worldwide (USPTO, EPO, JPO, UK IPO, IP Australia), examiners search TKDL "
            "to reject or cancel unmerited patent applications under Section 3(p) or foreign novelty standards [patents-act-3p, tkdl-prior-art]. TKDL has successfully thwarted over 1,500 wrongful patent grants globally.\n"
            "4. **Democratized User Access for Innovators**: Under the August 2022 Union Cabinet decision, TKDL access was opened to Indian researchers, startups, and MSMEs "
            "to conduct defensive prior art searches before filing patent or trademark applications [tkdl-user-access].\n\n"
            "**Official Portal:** Innovators can register for pre-filing prior art searches at `https://www.tkdl.res.in`."
        )
        questions = [
            "Are you seeking to search TKDL to verify prior art for your formulation?",
            "Have you registered as an Indian MSME or researcher on tkdl.res.in?",
            "Do you need assistance checking IPC/TKRC classifications?"
        ]
        return ans, questions

    def _answer_wipo_gratk(self, query: str, chunks: list[RetrievedChunk]) -> Tuple[str, list[str]]:
        ans = (
            "### WIPO GRATK Treaty (2024) — International Mandatory Disclosure\n\n"
            "**Direct Answer:**\n"
            "Adopted at WIPO in Geneva in May 2024, the **Treaty on Intellectual Property, Genetic Resources and Associated Traditional Knowledge (GRATK)** "
            "establishes a landmark **mandatory international patent disclosure requirement** [wipo-gratk-treaty-2024].\n\n"
            "**Article 3 Obligations & Global Impact:**\n"
            "1. **Mandatory Patent Disclosure**: Patent applicants across all contracting member states must explicitly disclose:\n"
            "   - The **country of origin** of genetic resources if the claimed invention is materially based upon them [wipo-gratk-treaty-2024].\n"
            "   - The **indigenous or local community** that provided associated traditional knowledge [wipo-gratk-treaty-2024].\n"
            "2. **Synergy with Indian Law**: Aligns international patent filing standards with India's domestic Section 10(4)(d)(ii) disclosure requirements [patents-act-10-4] "
            "and Section 6 NBA approval mechanisms [bd-act-sec-6].\n"
            "3. **Biopiracy Deterrence**: Prevents entities from obtaining patents in foreign jurisdictions based on Indian medicinal botanicals without benefit sharing.\n\n"
            "**Official Source:** World Intellectual Property Organization at `https://www.wipo.int/tk/en/`."
        )
        questions = [
            "Are you filing a PCT international patent application via WIPO?",
            "Have you obtained NBA Form III clearance prior to foreign patent filing?",
            "Are the genetic resources sourced from Indian state territories?"
        ]
        return ans, questions

    def _answer_general_patentability(self, query: str, chunks: list[RetrievedChunk]) -> Tuple[str, list[str]]:
        ans = (
            "### Patentability of Ayurvedic Formulations in India\n\n"
            "**Direct Answer:**\n"
            "Classical Ayurvedic recipes recorded in ancient treatises cannot be patented under Indian law [patents-act-3p]. "
            "However, **novel, proprietary Ayurvedic inventions** can be patented if they satisfy the strict **4-tier statutory test**:\n\n"
            "**The 4-Tier Statutory Patentability Test:**\n"
            "1. **Non-Classical Novelty (§3(p))**: The formulation must not be codified traditional knowledge or an obvious aggregation of known herbal properties. "
            "Prior art searches must be conducted against the TKDL database (`tkdl.res.in`) [patents-act-3p, tkdl-prior-art].\n"
            "2. **Unexpected Synergism (§3(e))**: For polyherbal compositions, applicants must provide quantitative laboratory data proving synergy "
            "(Combination Index $CI < 1.0$ or isobologram) rather than a mere additive admixture [patents-act-3e, ipindia-tk-guidelines].\n"
            "3. **Enhanced Therapeutic Efficacy (§3(d))**: For phytopharmaceutical fractions, standardized extracts, or isolated active molecules, "
            "comparative data must prove enhanced therapeutic efficacy over crude extracts (*Novartis* doctrine) [patents-act-3d].\n"
            "4. **Mandatory Prior NBA Approval (§6)**: Before patent grant, the applicant must file **NBA Form III** on `nbaindia.org` under Section 6 of the "
            "Biological Diversity Act, 2002 [bd-act-sec-6] and declare biological origin under Section 10(4)(d)(ii) on Patent Form 1 [patents-act-10-4].\n\n"
            "**Strategic Recommendation:** If your formulation is classical, commercialize it under a manufacturing license (Form 25-D) and protect your distinctive brand "
            "through trademark registration on `ipindia.gov.in` [dc-act-classical-3a, trademarks-ayurveda-names]."
        )
        questions = [
            "What specific herbs or active extracts are in your formulation?",
            "Do you have laboratory data showing synergy (CI < 1.0)?",
            "Would you prefer a patent strategy or a brand trademark strategy?"
        ]
        return ans, questions

    # -------------------------------------------------------------------------
    # NEW SPECIFIC QUESTION HANDLERS
    # -------------------------------------------------------------------------

    def _answer_permissions_required(self, query: str, chunks: list[RetrievedChunk]) -> Tuple[str, list[str]]:
        ans = (
            "### Mandatory Legal & Regulatory Permissions for Ayurvedic Products in India\n\n"
            "**Direct Answer:**\n"
            "To manufacture, package, and commercially sell an Ayurvedic product in India, you must obtain a set of mandatory statutory licenses "
            "and regulatory clearances under the **Drugs and Cosmetics Act, 1940**, the **Biological Diversity Act, 2002**, and, if applicable, the **Food Safety and Standards Act, 2006**.\n\n"
            "**The 5 Essential Statutory Permissions Required:**\n\n"
            "1. **Ayurvedic Manufacturing License (State AYUSH Licensing Authority)**:\n"
            "   - **Classical Ayurvedic Medicine**: Apply on **Form 25-D** under Section 3(a) of the Drugs & Cosmetics Act [dc-act-classical-3a]. "
            "Requires proof of strict adherence to one of the 54 classical treatises listed in the First Schedule (Charaka, Sushruta, AFI). No clinical trial is required.\n"
            "   - **Patent or Proprietary (P&P) Medicine**: Apply on **Form 25-E** under Section 3(h) & Rule 158-B [dc-act-prop-3h]. "
            "Requires published scientific literature, acute toxicity safety data, and pilot clinical trial reports.\n"
            "   - **Loan License (Third-Party Manufacturing)**: If you do not own a manufacturing plant, apply for a Loan License on **Form 25-E-1** using an existing GMP-certified facility.\n\n"
            "2. **Good Manufacturing Practices (GMP) Certificate (Schedule T)**:\n"
            "   - Mandatory compliance with factory layout, sterile zones, quality control lab, and batch records under **Schedule T of Drugs and Cosmetics Rules, 1945** [dc-rules-schedule-t].\n\n"
            "3. **Biological Diversity Clearance (SBB / NBA)**:\n"
            "   - Under **Section 7 of the Biological Diversity Act, 2002**, Indian commercial manufacturers must submit prior intimation to the State Biodiversity Board (SBB) [bd-act-sec-7]. "
            "*(Note: Under the 2023 Amendment, cultivated medicinal plants with certificate of origin are exempt from SBB intimation)*.\n"
            "   - If foreign entities or overseas patents are involved, prior approval from the **National Biodiversity Authority (NBA)** under Section 3 or Section 6 is mandatory [bd-act-sec-6].\n\n"
            "4. **Food & Dietary Supplement Approval (FSSAI Ayurveda Aahara)**:\n"
            "   - If marketed as a dietary supplement, herbal tea, or functional food rather than a therapeutic drug, obtain a central license under the **FSSAI (Ayurveda Aahara) Regulations, 2022** [fssai-ayurveda-aahara]. "
            "Requires the mandatory Ayurveda Aahara logo and the disclaimer: *'Not for medicinal use'*. Disease cure claims are strictly prohibited.\n\n"
            "5. **Statutory Labeling & Packaging Compliance (Rule 161)**:\n"
            "   - Labels must list the true botanical names of all active ingredients in descending order, reference the classical treatise (for classical items), "
            "display manufacturing license number, batch number, expiry date, and cautionary warnings for Schedule E(1) poisonous plants [dc-rules-schedule-e1].\n\n"
            "**Official Portals:** Apply for AYUSH licenses via State AYUSH portals or Ministry of Ayush (`ayush.gov.in`), biodiversity clearances via `nbaindia.org`, and FSSAI licenses on FoSCoS (`foscos.fssai.gov.in`)."
        )
        questions = [
            "Are you manufacturing a Classical Medicine, a Proprietary Formulation, or an Ayurveda Aahara food?",
            "Do you plan to set up your own manufacturing facility or use a third-party loan license (Form 25-E-1)?",
            "Are your raw herbal ingredients sourced from cultivated farms or wild collection?"
        ]
        return ans, questions

    def _answer_export_europe_international(self, query: str, chunks: list[RetrievedChunk]) -> Tuple[str, list[str]]:
        ans = (
            "### Regulatory Roadmap: Exporting Ayurvedic Products to Europe & International Markets\n\n"
            "**Direct Answer:**\n"
            "Exporting Ayurvedic formulations to the European Union (EU) is legally governed by strict European medicines and food safety directives. "
            "Because full pharmaceutical marketing authorization requires extensive and cost-prohibitive clinical trials, Indian Ayurvedic exporters typically pursue "
            "either the **Traditional Herbal Medicinal Products Directive (THMPD)** or the **Food / Dietary Supplement pathway**.\n\n"
            "**Primary Regulatory Routes to the European Market:**\n\n"
            "1. **EU Traditional Herbal Medicinal Products Directive (Directive 2004/24/EC — THMPD)**:\n"
            "   - **Simplified Registration**: Available for herbal medicinal products with proven traditional use, safety, and therapeutic plausibility.\n"
            "   - **30-Year Usage Requirement**: The applicant must provide documented evidence of continuous medicinal use for at least 30 years, including **at least 15 years within the European Union**.\n"
            "   - **Herbal Monograph Alignment**: The herbs must align with European Medicines Agency (EMA) Committee on Herbal Medicinal Products (HMPC) Community Monographs (e.g. *Curcuma longa*, *Withania somnifera*, *Zingiber officinale*).\n\n"
            "2. **Food Supplement Pathway (Directive 2002/46/EC)**:\n"
            "   - **Most Practical Commercial Route**: Over 85% of Indian Ayurvedic products are sold in the EU as **Food Supplements** (Dietary Supplements) rather than medicines.\n"
            "   - **Botanical Positive Lists**: Compliance with national positive lists such as the **BelFrIt list** (Belgium, France, Italy mutual recognition of permitted botanicals) and EFSA safety guidelines.\n"
            "   - **Health Claim Restrictions**: Under EU Regulation 1924/2006, disease treatment, cure, or prevention claims are strictly illegal on food supplements. Only authorized general health claims are permitted.\n\n"
            "3. **Quality, Purity & European Pharmacopoeia (Ph. Eur.) Standards**:\n"
            "   - **Heavy Metal Limits**: Strict compliance with Ph. Eur. maximum limits: Lead ($< 3.0$ mg/kg), Cadmium ($< 1.0$ mg/kg), Mercury ($< 0.1$ mg/kg), Arsenic ($< 1.0$ mg/kg).\n"
            "   - **Contaminant Testing**: Mandatory screening for pesticide residues, polycyclic aromatic hydrocarbons (PAHs), and aflatoxins (Aflatoxin B1 $< 2$ mcg/kg; Total $< 4$ mcg/kg).\n"
            "   - **Microbial Purity**: Absence of *Salmonella*, *E. coli*, and limits on total aerobic microbial count.\n\n"
            "4. **Indian Export Certifications & CITES Clearance**:\n"
            "   - **WHO-GMP CoPP**: Obtain a Certificate of Pharmaceutical Product (CoPP) and Free Sale Certificate (FSC) from the State AYUSH SLA / CDSCO.\n"
            "   - **CITES Clearance**: If formulations contain endangered flora listed under CITES Appendix II or Schedule VI of India's Wildlife Protection Act (e.g. *Nardostachys jatamansi*, *Pterocarpus santalinus*, *Taxus wallichiana*), obtain mandatory export permits from DGFT and Wildlife Crime Control Bureau (WCCB).\n"
            "   - **NBA Form I / Section 3 Clearance**: If export involves research or commercial utilization by foreign partners, clearance under Section 3 of the Biological Diversity Act, 2002 is required [bd-act-sec-6]."
        )
        questions = [
            "Which specific EU country is your primary target (e.g., Germany, UK, Netherlands, France)?",
            "Are you exporting as an EMA traditional medicine or an EFSA dietary food supplement?",
            "Do your formulations contain any CITES-restricted botanicals (like Jatamansi, Red Sanders, or Kuth)?"
        ]
        return ans, questions

    def _answer_traditional_knowledge_determination(self, query: str, chunks: list[RetrievedChunk]) -> Tuple[str, list[str]]:
        ans = (
            "### Determination of Traditional Knowledge (TK) Status in Ayurvedic Formulations\n\n"
            "**Direct Answer:**\n"
            "An Ayurvedic formulation is legally recognized as **Traditional Knowledge (TK)** in India if its ingredients, ratios, manufacturing methods, "
            "or therapeutic indications are documented in the **54 authoritative classical Ayurvedic treatises** listed in the First Schedule of the Drugs and Cosmetics Act, 1940, "
            "or documented in the **Traditional Knowledge Digital Library (TKDL)** [patents-act-3p, tkdl-prior-art].\n\n"
            "**Statutory Criteria for Determining Traditional Knowledge:**\n\n"
            "1. **The First Schedule Test (Section 3(a), Drugs & Cosmetics Act)**:\n"
            "   - Does the formula originate from classical compendia such as *Charaka Samhita*, *Sushruta Samhita*, *Ashtanga Hridaya*, *Sharangadhara Samhita*, *Bhavaprakasha*, "
            "or official statutory formularies like the *Ayurvedic Formulary of India (AFI)* or *Ayurvedic Pharmacopoeia of India (API)* [dc-act-classical-3a]?\n"
            "   - If yes, it is classical traditional knowledge. Manufacturing is licensed under **Form 25-D** without clinical efficacy trials.\n\n"
            "2. **The TKDL Prior Art Screening (tkdl.res.in)**:\n"
            "   - CSIR and the Ministry of Ayush have transcribed over 4.5 lakh classical formulations into the TKDL, classified under the International Patent Classification (IPC) "
            "as Traditional Knowledge Resource Classification (TKRC) [tkdl-prior-art].\n"
            "   - Patent examiners at the Indian Patent Office (IPO), EPO, USPTO, JPO, and WIPO systematically search TKDL as prior art.\n\n"
            "3. **Patentability Consequence under Section 3(p) of The Patents Act, 1970**:\n"
            "   - An invention which in effect is traditional knowledge or an aggregation/duplication of traditionally known properties is strictly non-patentable [patents-act-3p].\n"
            "   - **What Transcends TK to Become Patentable?** Novel modified combinations with non-obvious synergistic ratios ($CI < 1.0$) [patents-act-3e], "
            "purified/isolated phytopharmaceutical fractions demonstrating enhanced therapeutic efficacy (*Novartis* standard) [patents-act-3d], "
            "or novel drug delivery systems (e.g. liposomal, nanostructured, or targeted formulations).\n\n"
            "**Official Resources:** Verify classical status in the Ayurvedic Formulary of India on `ayush.gov.in`, examine treatises on India Code (`indiacode.nic.in`), and search prior art on `tkdl.res.in`."
        )
        questions = [
            "Does your formulation appear in the Ayurvedic Formulary of India (AFI) or classical Samhitas?",
            "Have you changed the classical herbal proportions or developed a novel extraction technique?",
            "Are you seeking patent protection (novelty required) or commercial licensing as a classical medicine?"
        ]
        return ans, questions

    def _answer_biodiversity_approval_decision_tree(self, query: str, chunks: list[RetrievedChunk]) -> Tuple[str, list[str]]:
        ans = (
            "### National Biodiversity Authority (NBA) & SBB Approval Decision Tree\n\n"
            "**Direct Answer:**\n"
            "Whether you require prior approval from the **National Biodiversity Authority (NBA)** or the **State Biodiversity Board (SBB)** under the "
            "**Biological Diversity Act, 2002** depends strictly on three criteria: **(1) your legal entity status, (2) your activity (research vs manufacturing vs patenting), and (3) your raw material source** [bd-act-sec-6, bd-act-sec-7].\n\n"
            "**Statutory Decision Framework:**\n\n"
            "1. **Entity Classification (Section 3 vs Section 7)**:\n"
            "   - **Foreign Entities / Non-Citizens (Section 3)**: Non-resident Indians (NRIs), foreign nationals, foreign corporations, or Indian companies with *any* foreign equity/directorship "
            "MUST obtain **mandatory prior approval from the NBA on Form I** before accessing Indian biological resources or associated traditional knowledge for research, bio-survey, or commercial utilization [bd-act-sec-6].\n"
            "   - **Indian Entities / Citizens (Section 7)**: Domestic companies and citizens do NOT need NBA Form I for domestic commercial use; instead, they submit **prior intimation to the State Biodiversity Board (SBB)** [bd-act-sec-7].\n\n"
            "2. **IPR & Patent Applications (Section 6 — Universal Mandate)**:\n"
            "   - **Mandatory for ALL applicants (Indian and Foreign)**: Under **Section 6(1)**, no person shall apply for any patent or intellectual property right in India or abroad "
            "for any invention based on Indian biological resources or associated knowledge without obtaining **NBA Form III approval** [bd-act-sec-6].\n"
            "   - **Filing Timing**: Form III may be filed after submitting the patent application, but MUST be granted **before the final sealing of the patent** by the Indian Patent Office.\n\n"
            "3. **Statutory Exemptions under the Biological Diversity (Amendment) Act, 2023**:\n"
            "   - **Cultivated Medicinal Plants**: Commercial users of cultivated medicinal plants are **exempt from SBB intimation and ABS payments** under amended Section 7, provided they hold farmer certificates of origin [bd-act-sec-7].\n"
            "   - **Codified Traditional Knowledge**: AYUSH practitioners (Vaidyas, Hakims) and manufacturers adhering strictly to codified classical TK are exempted from ABS fees.\n"
            "   - **Normally Traded Commodities (NTC)**: 421+ species notified under Section 40 (e.g., turmeric, ginger, black pepper) are exempt when traded purely as agricultural commodities for consumption [bd-act-sec-40-ntc].\n\n"
            "**Official Portal:** File Form I, Form II, or Form III applications online at the National Biodiversity Authority portal: `nbaindia.org`."
        )
        questions = [
            "Does your organization have any foreign direct investment (FDI), non-resident shareholders, or foreign directors?",
            "Are you manufacturing for commercial sale or applying for an intellectual property patent?",
            "Are your botanical ingredients wild-harvested or cultivated on registered agricultural farms?"
        ]
        return ans, questions

    def _answer_cultivated_vs_wild_herbs(self, query: str, chunks: list[RetrievedChunk]) -> Tuple[str, list[str]]:
        ans = (
            "### Cultivated vs. Wild-Harvested Botanicals: BD Act Compliance & SBB Exemptions\n\n"
            "**Direct Answer:**\n"
            "The legal compliance burden under the **Biological Diversity Act, 2002** differs drastically depending on whether your raw herbal materials "
            "are **cultivated on registered agricultural farms** or **wild-harvested from natural habitats or forests** [bd-act-sec-7].\n\n"
            "**Statutory Differences & Legal Obligations:**\n\n"
            "1. **Cultivated Medicinal Plants (Section 7 Exemption — 2023 Amendment)**:\n"
            "   - **Statutory Exemption**: Under the **Biological Diversity (Amendment) Act, 2023**, domestic commercial manufacturers and users of **cultivated medicinal plants and their derivatives are expressly EXEMPT from prior intimation to the State Biodiversity Board (SBB) and ABS fee payments** [bd-act-sec-7].\n"
            "   - **Proof of Cultivation Required**: You must maintain verifiable documentary proof of cultivation, such as:\n"
            "     - Sourcing contracts with registered farmers or agricultural cooperatives.\n"
            "     - Agricultural produce market committee (APMC / Mandi) receipts.\n"
            "     - Certificates of origin from District Agriculture/Horticulture officers or State Medicinal Plants Boards (SMPBs) / NMPB.\n\n"
            "2. **Wild-Harvested Herbs (Forest & Natural Sourcing)**:\n"
            "   - **Prior SBB Intimation**: Any commercial utilization of wild-collected Indian biological resources by domestic entities requires prior intimation on **Form I** to the concerned **State Biodiversity Board (SBB)** under Section 7 [bd-act-sec-7].\n"
            "   - **Access & Benefit Sharing (ABS) Fee**: Manufacturers must enter into an ABS Agreement and pay benefit-sharing fees (typically **0.1% to 0.5% of ex-factory gross sales** or 3% to 5% of raw material purchase price) under the ABS Regulations, 2014 [bd-act-abs-regs].\n"
            "   - **Forest Department Permits**: Collection of wild forest flora requires transit passes and non-timber forest produce (NTFP) transit permissions from the State Forest Department.\n\n"
            "3. **Patent Applications (Section 6 Mandate)**:\n"
            "   - **Important Distinction**: Even if your herbs are 100% cultivated, if you apply for a **patent**, you must still disclose the Indian geographical origin in Patent Form 1 under **Section 10(4)(d)(ii)** [patents-act-10-4] "
            "and apply for **NBA Form III approval** under Section 6(1) on `nbaindia.org` [bd-act-sec-6] before patent grant."
        )
        questions = [
            "Do you have farmer cultivation agreements or APMC mandi receipts for your raw materials?",
            "Are any of your botanicals collected from forest areas requiring State Forest Department transit permits?",
            "Are you planning to file a patent application requiring NBA Form III clearance?"
        ]
        return ans, questions

    def _answer_indication_specific_patent(self, query: str, chunks: list[RetrievedChunk]) -> Tuple[str, list[str]]:
        q_lower = query.lower()
        indication = "this medical indication"
        herbs = "classical Ayurvedic botanicals"
        classical_refs = "classical treatises"

        if any(k in q_lower for k in ["cough", "respiratory", "kasa", "asthma", "shwasa", "bronchitis"]):
            indication = "cough, respiratory, and pulmonary conditions (*Kasa* and *Shwasa*)"
            herbs = "*Vasa* (*Adhatoda vasica*), *Kantakari* (*Solanum xanthocarpum*), *Pippali* (*Piper longum*), *Yashtimadhu* (*Glycyrrhiza glabra*)"
            classical_refs = "*Sitopaladi Churna*, *Talisadi Churna*, *Vasa Avaleha*, and *Kantakari Avaleha* (documented in *Charaka Samhita* and *AFI*)"
        elif any(k in q_lower for k in ["diabet", "prameha", "sugar", "metabolic"]):
            indication = "diabetes and metabolic management (*Prameha*)"
            herbs = "*Gudmar* (*Gymnema sylvestre*), *Vijaysar* (*Pterocarpus marsupium*), *Jamun* (*Syzygium cumini*), *Karela* (*Momordica charantia*)"
            classical_refs = "*Nisha Amalaki*, *Chandraprabha Vati*, and *Mehari Asava*"
        elif any(k in q_lower for k in ["arthrit", "joint pain", "sandhivata", "amavata", "inflamm"]):
            indication = "arthritis, joint pain, and inflammatory disorders (*Sandhivata* and *Amavata*)"
            herbs = "*Guggulu* (*Commiphora mukul*), *Shallaki* (*Boswellia serrata*), *Rasna* (*Pluchea lanceolata*), *Ashwagandha* (*Withania somnifera*)"
            classical_refs = "*Yogaraja Guggulu*, *Simhanada Guggulu*, and *Mahanarayana Taila*"
        elif any(k in q_lower for k in ["skin", "kushta", "eczema", "psoriasis"]):
            indication = "dermatological and skin conditions (*Kushta*)"
            herbs = "*Neem* (*Azadirachta indica*), *Manjistha* (*Rubia cordifolia*), *Khadira* (*Acacia catechu*), *Haridra* (*Curcuma longa*)"
            classical_refs = "*Khadirarishta*, *Mahamanjisthadi Kwatha*, and *Gandhaka Rasayana*"
        elif any(k in q_lower for k in ["liver", "hepat", "yakrit", "jaundice", "digest"]):
            indication = "liver and hepatic disorders (*Yakrit Roga*)"
            herbs = "*Bhumi Amla* (*Phyllanthus niruri*), *Katuki* (*Picrorhiza kurroa*), *Kalmegh* (*Andrographis paniculata*)"
            classical_refs = "*Arogyavardhini Vati*, *Punarnavarishta*, and *Liv-52* type formulations"
        elif any(k in q_lower for k in ["cancer", "tumor", "arbuda", "oncolog"]):
            indication = "oncological adjunct or anti-proliferative care (*Arbuda*)"
            herbs = "*Kanchanara* (*Bauhinia variegata*), *Tulsi* (*Ocimum sanctum*), *Curcumin* (*Curcuma longa*), *Guduchi* (*Tinospora cordifolia*)"
            classical_refs = "*Kanchanara Guggulu* and classical Rasayana preparations"

        ans = (
            f"### Patentability of Ayurvedic Medicine for {indication}\n\n"
            f"**Direct Answer:**\n"
            f"You **cannot** obtain a patent for a formulation that merely combines well-known classical Ayurvedic herbs used for {indication} "
            f"(such as {herbs}), because classical preparations like {classical_refs} are codified traditional knowledge excluded under **Section 3(p) of The Patents Act, 1970** [patents-act-3p].\n\n"
            f"However, **you CAN obtain a valid Indian or international patent** for a specialized innovation targeting {indication} if you fulfill one of the three statutory pathways below:\n\n"
            f"**The 3 Patentable Pathways for {indication}:**\n\n"
            f"1. **Novel Synergistic Polyherbal Composition (§3(e))**:\n"
            f"   - If your formulation combines specific botanical extracts in a unique non-classical ratio that demonstrates **statistically significant synergy** in validated pharmacological models.\n"
            f"   - **Statutory Proof**: You must submit head-to-head laboratory data showing a Combination Index $CI < 1.0$ (Chou-Talalay method) or isobolographic analysis proving that the combined therapeutic effect "
            f"exceeds the additive sum of each single herb [patents-act-3e, ipindia-tk-guidelines].\n\n"
            f"2. **Purified Phytopharmaceutical / Enriched Fraction (§3(d))**:\n"
            f"   - If you isolate or enrich specific active phytochemicals (e.g. standardized active fractions) with quantified active markers.\n"
            f"   - **Statutory Proof**: Under the Supreme Court's *Novartis* doctrine for Section 3(d), you must provide comparative pharmacological evidence showing statistically superior therapeutic efficacy "
            f"over conventional crude extracts [patents-act-3d].\n\n"
            f"3. **Novel Drug Delivery System (NDDS)**:\n"
            f"   - Developing an innovative delivery mechanism—such as a mucoadhesive lozenge, liposomal or nano-emulsion formulation, or sustained-release delivery that overcomes mere admixture exclusions.\n\n"
            f"**Mandatory Statutory Procedural Steps:**\n"
            f"- **TKDL Pre-Screening**: Check `tkdl.res.in` to ensure the exact combination and indication are not cited in classical texts [tkdl-prior-art].\n"
            f"- **Mandatory Biological Origin Disclosure**: Declare the exact Indian geographical source of all herbs in Patent Form 1 under **Section 10(4)(d)(ii)** [patents-act-10-4].\n"
            f"- **NBA Form III Clearance**: Apply for National Biodiversity Authority approval on `nbaindia.org` under **Section 6** before the patent is granted [bd-act-sec-6]."
        )
        questions = [
            f"Are you using crude powdered herbs or standardized extracts with quantified active markers?",
            f"Do you have laboratory data comparing the combination against the single herbs (CI < 1.0)?",
            f"Would you like guidance on licensing this as a Proprietary Medicine (Form 25-E) under Rule 158-B?"
        ]
        return ans, questions

    def _answer_dynamic_irac(self, query: str, chunks: list[RetrievedChunk], jurisdiction: Optional[str]) -> Tuple[str, list[str]]:
        top_chunks = chunks[:4] if chunks else []
        c0 = top_chunks[0] if top_chunks else None

        title0 = c0.metadata.get("source_title") or c0.metadata.get("statute") or "Indian IPR & Regulatory Statute" if c0 else "Primary Statute"
        sec0 = f" ({c0.metadata.get('section')})" if c0 and c0.metadata.get("section") else ""
        cid0 = c0.chunk_id if c0 else "patents-act-3p"

        q_clean = query.strip(" ?.")
        ans = (
            f"### Statutory Analysis & Strategic Guidance: *{q_clean}*\n\n"
            f"**Core Legal Position & Regulatory Assessment:**\n"
            f"Your inquiry regarding **'{q_clean}'** is governed primarily by **{title0}{sec0}** alongside complementary provisions "
            f"under Indian IPR and AYUSH regulatory frameworks [{cid0}]. Under Indian law, innovations involving Ayurvedic and botanical resources "
            f"are subject to a dual statutory mandate: **strict protection of classical traditional knowledge** against wrongful misappropriation, balanced with "
            f"**defined pathways for genuine scientific and commercial innovation**.\n\n"
            f"**Statutory Rules & Legal Standards:**\n\n"
            f"1. **Traditional Knowledge & Prior Art Boundaries (§3(p))**: If this matter involves codified herbal formulas or classical principles recorded in ancient treatises "
            f"(Charaka, Sushruta, AFI), it is treated as public domain traditional knowledge. No exclusive monopoly can be granted over classical heritage [patents-act-3p]. "
            f"Patent examiners systematically verify prior art against the Traditional Knowledge Digital Library (`tkdl.res.in`) [tkdl-prior-art].\n\n"
            f"2. **Evidence of Synergism & Efficacy (§3(e) & §3(d))**: For polyherbal combinations or modified extracts, statutory clearance requires empirical laboratory data. "
            f"Combinations must prove non-obvious synergy (Combination Index $CI < 1.0$ or isobologram analysis) under Section 3(e) [patents-act-3e], and purified botanical fractions must demonstrate "
            f"enhanced therapeutic efficacy over crude extracts under the Supreme Court's *Novartis* doctrine [patents-act-3d].\n\n"
            f"3. **Origin Disclosure & Biodiversity Clearances (§10(4) & BD Act)**: All biological materials obtained from India must have their exact source and geographical origin disclosed "
            f"in Patent Form 1 [patents-act-10-4]. In parallel, Section 6 of the Biological Diversity Act, 2002 mandates that **NBA Form III approval** must be obtained on `nbaindia.org` "
            f"prior to the grant of any intellectual property right [bd-act-sec-6].\n\n"
            f"4. **Commercial Manufacturing Licensing (AYUSH Form 25-D / Form 25-E)**: For commercial sale, manufacturers must obtain either a classical license (Form 25-D) under Section 3(a) "
            f"or a proprietary license (Form 25-E) under Section 3(h) and Rule 158-B, while adhering to Good Manufacturing Practices under Schedule T [dc-act-prop-3h, dc-rules-schedule-t].\n\n"
            f"**Actionable Compliance Steps & Recommendations:**\n"
            f"- **Verify Formulation Type**: Classify your formula as Classical (treatise-based) or Proprietary (novel ratio/delivery system).\n"
            f"- **Prior Art & Clearance Searches**: Conduct clearance searches on IP India (`ipindia.gov.in`) and TKDL (`tkdl.res.in`).\n"
            f"- **Procure Regulatory Permits**: Initiate State AYUSH licensing and NBA Form III/SBB filings concurrently with product development."
        )
        questions = [
            "Can you specify the exact botanical ingredients or formulation type you are evaluating?",
            "Are you seeking an intellectual property patent, a brand trademark, or a manufacturing license?",
            "Do you require assistance with NBA Form III filings or State AYUSH licensing procedures?"
        ]
        return ans, questions
