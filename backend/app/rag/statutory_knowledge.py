"""Curated statutory knowledge corpus for Ayurvedic IPR & Regulatory frameworks.

Grounded in open, authoritative public sources:
- Traditional Knowledge Digital Library (TKDL) — tkdl.res.in
- Statutes & Rules via India Code — indiacode.nic.in
- IP India Public Databases (InPASS, Trade Marks, GI Registry, Designs) — ipindia.gov.in
- National Biodiversity Authority / ABS — nbaindia.org
- Ministry of Ayush & FSSAI (Ayurveda Aahara)
- WIPO GRATK Treaty (2024) & Nagoya Protocol
"""

STATUTORY_CORPUS = [
    {
        "id": "patents-act-3p",
        "title": "The Patents Act, 1970 — Section 3(p) (Traditional Knowledge Exclusion)",
        "content": (
            "Section 3(p) of The Patents Act, 1970 provides that an invention which in effect is traditional knowledge "
            "or which is an aggregation or duplication of known properties of traditionally known component or components "
            "is not an invention within the meaning of this Act. Classical Ayurvedic formulations disclosed in authoritative "
            "treatises listed in the First Schedule to the Drugs and Cosmetics Act, 1940 (such as Charaka Samhita, Sushruta Samhita, "
            "Ashtanga Hridaya, Sharangadhara Samhita, and Ayurvedic Formulary of India) are codified traditional knowledge documented "
            "in the Traditional Knowledge Digital Library (TKDL, tkdl.res.in). Claims directed to classical recipes or known herbal properties "
            "are strictly barred from patentability and publicly searchble via InPASS (ipindia.gov.in)."
        ),
        "metadata": {
            "source_name": "The Patents Act, 1970 (India Code)",
            "statute": "The Patents Act, 1970",
            "section": "Section 3(p)",
            "authority": "Office of Controller General of Patents, Designs & Trade Marks (CGPDTM)",
            "authority_level": 1,
            "jurisdiction": "India",
            "portal_url": "https://www.indiacode.nic.in/handle/123456789/1392"
        }
    },
    {
        "id": "patents-act-3e",
        "title": "The Patents Act, 1970 — Section 3(e) (Synergism vs Mere Admixture)",
        "content": (
            "Section 3(e) of The Patents Act, 1970 excludes from patentability a substance obtained by a mere admixture "
            "resulting only in the aggregation of the properties of the components thereof or a process for producing such substance. "
            "For polyherbal Ayurvedic formulations, patent applicants must demonstrate unexpected synergistic effect "
            "with empirical quantitative laboratory data (such as Combination Index < 1.0, isobolographic analysis, or significant bio-availability enhancement) "
            "to overcome Section 3(e) objections during InPASS patent examination (ipindia.gov.in)."
        ),
        "metadata": {
            "source_name": "The Patents Act, 1970 (IP India Public Database)",
            "statute": "The Patents Act, 1970",
            "section": "Section 3(e)",
            "authority": "Office of Controller General of Patents, Designs & Trade Marks (CGPDTM)",
            "authority_level": 1,
            "jurisdiction": "India",
            "portal_url": "https://ipindia.gov.in"
        }
    },
    {
        "id": "patents-act-3d",
        "title": "The Patents Act, 1970 — Section 3(d) (Incremental Efficacy Requirement)",
        "content": (
            "Section 3(d) of The Patents Act, 1970 bars the mere discovery of a new form of a known substance which does not result "
            "in the enhancement of the known efficacy of that substance. In the context of Ayurvedic phytopharmaceuticals, standardized fractions, "
            "or isolated herbal extracts, the applicant must establish proof of enhanced therapeutic efficacy (Novartis AG v. Union of India) "
            "over conventional crude herbal extracts or known compounds."
        ),
        "metadata": {
            "source_name": "The Patents Act, 1970 (India Code)",
            "statute": "The Patents Act, 1970",
            "section": "Section 3(d)",
            "authority": "Office of Controller General of Patents, Designs & Trade Marks (CGPDTM)",
            "authority_level": 1,
            "jurisdiction": "India",
            "portal_url": "https://www.indiacode.nic.in/handle/123456789/1392"
        }
    },
    {
        "id": "bd-act-sec-6",
        "title": "The Biological Diversity Act, 2002 — Section 6 (Mandatory NBA Approval for IPR)",
        "content": (
            "Section 6(1) of the Biological Diversity Act, 2002 mandates that no person shall apply for any intellectual property right, "
            "by whatever name called, in or outside India for any invention based on any research or information on a biological resource "
            "obtained from India without obtaining the previous approval of the National Biodiversity Authority (NBA, nbaindia.org) prior to applying for such right. "
            "Mandatory application must be filed on NBA Form III (Form I for foreign entities) accessible on nbaindia.org."
        ),
        "metadata": {
            "source_name": "National Biodiversity Authority / ABS Portal",
            "statute": "The Biological Diversity Act, 2002",
            "section": "Section 6 (IPR Prior Approval)",
            "authority": "National Biodiversity Authority (NBA)",
            "authority_level": 1,
            "jurisdiction": "India",
            "portal_url": "https://nbaindia.org"
        }
    },
    {
        "id": "bd-act-sec-7-2023",
        "title": "The Biological Diversity (Amendment) Act, 2023 — Section 7 (Codified TK & Cultivated Plants Exemption)",
        "content": (
            "Under the Biological Diversity (Amendment) Act, 2023, Section 7 was amended to provide that users of codified traditional knowledge, "
            "cultivated medicinal plants, and registered AYUSH practitioners (Vaidyas and Hakims) are exempt from giving prior intimation to the "
            "State Biodiversity Board (SBB) for accessing biological resources for commercial utilization or manufacturing of classical Ayurvedic products. "
            "Verified texts and guidelines are available via India Code (indiacode.nic.in) and NBA (nbaindia.org)."
        ),
        "metadata": {
            "source_name": "India Code — Biological Diversity (Amendment) Act, 2023",
            "statute": "Biological Diversity Act, 2002 (amended 2023)",
            "section": "Section 7 (Codified TK Exemption)",
            "authority": "National Biodiversity Authority (NBA)",
            "authority_level": 1,
            "jurisdiction": "India",
            "portal_url": "https://www.indiacode.nic.in"
        }
    },
    {
        "id": "tkdl-prior-art",
        "title": "Traditional Knowledge Digital Library (TKDL) — Prior Art Pre-Screening",
        "content": (
            "The Traditional Knowledge Digital Library (TKDL, tkdl.res.in) is a pioneer database created by CSIR and the Ministry of Ayush "
            "containing over 4.5 lakh formulations from classical Ayurvedic treatises (Charaka Samhita, Sushruta Samhita, Astanga Hridaya, etc.) "
            "translated into five international languages (English, French, German, Japanese, Spanish) structured in Traditional Knowledge Resource Classification (TKRC). "
            "Under the August 2022 Union Cabinet decision, TKDL access was opened to users, researchers, and MSMEs for prior art search (tkdl.res.in)."
        ),
        "metadata": {
            "source_name": "Traditional Knowledge Digital Library (TKDL)",
            "statute": "CSIR & Ministry of Ayush Prior Art Repository",
            "section": "TKRC Classification",
            "authority": "CSIR & Ministry of Ayush",
            "authority_level": 2,
            "jurisdiction": "India",
            "portal_url": "https://www.tkdl.res.in"
        }
    },
    {
        "id": "dc-act-classical-3a",
        "title": "The Drugs and Cosmetics Act, 1940 — Section 3(a) & Schedule T (GMP)",
        "content": (
            "Section 3(a) of the Drugs and Cosmetics Act, 1940 (available on indiacode.nic.in) defines Ayurvedic, Siddha or Unani (ASU) drugs "
            "manufactured exclusively in accordance with the formulae described in authoritative books specified in the First Schedule. "
            "Classical formulations require manufacturing license on Form 25-D from State Licensing Authority (AYUSH) "
            "and mandatory compliance with Schedule T Good Manufacturing Practices (GMP)."
        ),
        "metadata": {
            "source_name": "The Drugs and Cosmetics Act, 1940 (India Code)",
            "statute": "Drugs and Cosmetics Act, 1940",
            "section": "Section 3(a) & Schedule T",
            "authority": "Ministry of Ayush / State Licensing Authorities",
            "authority_level": 1,
            "jurisdiction": "India",
            "portal_url": "https://www.indiacode.nic.in"
        }
    },
    {
        "id": "dc-act-prop-3h",
        "title": "The Drugs and Cosmetics Act, 1940 — Section 3(h) & Rule 158-B (Patent or Proprietary Medicine)",
        "content": (
            "Section 3(h) of Drugs and Cosmetics Act defines Patent or Proprietary (P&P) Ayurvedic Medicine containing ingredients "
            "from First Schedule treatises but not manufactured verbatim to classical recipes. Rule 158-B of the Drugs and Cosmetics Rules, 1945 "
            "governs licensing, requiring textual citations, pilot safety studies, and published scientific literature."
        ),
        "metadata": {
            "source_name": "Drugs and Cosmetics Rules, 1945 (India Code)",
            "statute": "Drugs and Cosmetics Rules, 1945",
            "section": "Rule 158-B & Section 3(h)",
            "authority": "Ministry of Ayush",
            "authority_level": 1,
            "jurisdiction": "India",
            "portal_url": "https://www.indiacode.nic.in"
        }
    },
    {
        "id": "fssai-ayurveda-aahara",
        "title": "Food Safety and Standards (Ayurveda Aahara) Regulations, 2022",
        "content": (
            "Under the Food Safety and Standards (Ayurveda Aahara) Regulations, 2022 (fssai.gov.in), foods prepared in accordance with "
            "authoritative Ayurvedic treatises listed in Schedule A are classified as 'Ayurveda Aahara'. Such products must carry the mandatory "
            "Ayurveda Aahara logo and clear front-of-pack advisory, and are strictly prohibited from making therapeutic drug claims."
        ),
        "metadata": {
            "source_name": "Food Safety and Standards Authority of India (FSSAI)",
            "statute": "Food Safety and Standards Act, 2006",
            "section": "Ayurveda Aahara Regulations, 2022",
            "authority": "Food Safety and Standards Authority of India (FSSAI)",
            "authority_level": 2,
            "jurisdiction": "India",
            "portal_url": "https://fssai.gov.in"
        }
    },
    {
        "id": "trademarks-ayurveda-names",
        "title": "The Trade Marks Act, 1999 — Classical Names Publici Juris & IP India Registry",
        "content": (
            "Under Section 9 of the Trade Marks Act, 1999 (indiacode.nic.in & ipindia.gov.in), descriptive and generic terms lack distinctiveness. "
            "Names of classical Ayurvedic medicines (e.g., Triphala, Chyawanprash, Dashamularishta) are publici juris and cannot be registered as an exclusive "
            "monopoly trademark. Trademark public search on ipindia.gov.in applies the Supreme Court's Cadila Healthcare standard to medicinal marks."
        ),
        "metadata": {
            "source_name": "IP India Public Databases — Trade Marks Registry",
            "statute": "Trade Marks Act, 1999",
            "section": "Section 9 & Section 11",
            "authority": "Trade Marks Registry / CGPDTM",
            "authority_level": 1,
            "jurisdiction": "India",
            "portal_url": "https://ipindia.gov.in"
        }
    },
    {
        "id": "wipo-gratk-treaty-2024",
        "title": "WIPO Treaty on Intellectual Property, Genetic Resources and Associated Traditional Knowledge (2024)",
        "content": (
            "Adopted at WIPO in Geneva in May 2024, the Treaty on Intellectual Property, Genetic Resources and Associated Traditional Knowledge establishes "
            "a mandatory international disclosure requirement for patent applications. Patent applicants in contracting parties must disclose the country of origin "
            "of genetic resources or the indigenous community that provided associated traditional knowledge if claimed inventions are materially based upon them."
        ),
        "metadata": {
            "source_name": "World Intellectual Property Organization (WIPO)",
            "statute": "WIPO Treaty on IP, Genetic Resources & Associated TK",
            "section": "Article 3 (Mandatory Disclosure)",
            "authority": "World Intellectual Property Organization (WIPO)",
            "authority_level": 1,
            "jurisdiction": "International",
            "portal_url": "https://www.wipo.int/tk/en/"
        }
    },
    {
        "id": "patents-act-10-4",
        "title": "The Patents Act, 1970 — Section 10(4)(d)(ii) (Mandatory Biological Origin Disclosure)",
        "content": (
            "Section 10(4)(d)(ii) of The Patents Act, 1970 mandates that if an applicant mentions any biological material in the specification "
            "which is obtained from India, the application must disclose the source and geographical origin of the biological material. "
            "Furthermore, mandatory declaration on Form 1 must state whether prior approval of the National Biodiversity Authority (NBA) "
            "has been obtained or applied for under Section 6 of the Biological Diversity Act, 2002."
        ),
        "metadata": {
            "source_name": "The Patents Act, 1970 (Disclosure of Biological Origin)",
            "statute": "The Patents Act, 1970",
            "section": "Section 10(4)(d)(ii)",
            "authority": "Office of Controller General of Patents, Designs & Trade Marks (CGPDTM)",
            "authority_level": 1,
            "jurisdiction": "India",
            "portal_url": "https://www.indiacode.nic.in/handle/123456789/1392"
        }
    },
    {
        "id": "patents-act-25-opposition",
        "title": "The Patents Act, 1970 — Section 25 (Pre-Grant and Post-Grant Patent Opposition)",
        "content": (
            "Under Section 25(1) (pre-grant opposition) and Section 25(2) (post-grant opposition) of The Patents Act, 1970, "
            "any person or third party may oppose a patent application on grounds that the complete specification does not disclose "
            "or wrongly mentions the source or geographical origin of biological material used for the invention, or that the invention "
            "claimed was anticipated having regard to the knowledge, oral or otherwise, available within any local or indigenous community in India or elsewhere."
        ),
        "metadata": {
            "source_name": "The Patents Act, 1970 (TK Oppositions)",
            "statute": "The Patents Act, 1970",
            "section": "Section 25",
            "authority": "Office of Controller General of Patents, Designs & Trade Marks (CGPDTM)",
            "authority_level": 1,
            "jurisdiction": "India",
            "portal_url": "https://ipindia.gov.in"
        }
    },
    {
        "id": "bd-act-sec-40-ntc",
        "title": "The Biological Diversity Act, 2002 — Section 40 (Normally Traded Commodities Exemption)",
        "content": (
            "Section 40 of the Biological Diversity Act empowers the Central Government to exempt certain biological resources normally traded as commodities "
            "from the provisions of the Act. The Ministry of Environment, Forest and Climate Change has notified 421+ biological species "
            "(including Black Pepper, Ginger, Turmeric, Clove, Cinnamon, Cumin, Fenugreek) as Normally Traded Commodities (NTC). "
            "NTC exemption applies ONLY when the biological resource is traded strictly as an agricultural/horticultural commodity, and does NOT apply "
            "when it is accessed for research, patenting, or biotechnology applications."
        ),
        "metadata": {
            "source_name": "National Biodiversity Authority — Section 40 NTC List",
            "statute": "The Biological Diversity Act, 2002",
            "section": "Section 40 (NTC Exemption)",
            "authority": "National Biodiversity Authority (NBA)",
            "authority_level": 1,
            "jurisdiction": "India",
            "portal_url": "https://nbaindia.org"
        }
    },
    {
        "id": "dc-act-schedule-e1",
        "title": "Drugs and Cosmetics Rules, 1945 — Schedule E(1) (Poisonous Ingredients & Shodhana)",
        "content": (
            "Schedule E(1) to the Drugs and Cosmetics Rules, 1945 lists poisonous substances of plant, mineral, and animal origin used in Ayurvedic medicines, "
            "such as Aconitum (Vatsanabha), Semecarpus anacardium (Bhallataka), Strychnos nux-vomica (Kupilu), Datura, and Mercury compounds (Parada). "
            "Medicines containing Schedule E(1) ingredients require mandatory detoxification (Shodhana) as per classical methods, "
            "clear cautionary warning labels ('Caution: To be taken under medical supervision'), and strict batch testing."
        ),
        "metadata": {
            "source_name": "Drugs and Cosmetics Rules — Schedule E(1)",
            "statute": "Drugs and Cosmetics Rules, 1945",
            "section": "Schedule E(1)",
            "authority": "Ministry of Ayush",
            "authority_level": 1,
            "jurisdiction": "India",
            "portal_url": "https://www.indiacode.nic.in"
        }
    },
    {
        "id": "tkdl-user-access",
        "title": "Traditional Knowledge Digital Library — Innovator & MSME User Access",
        "content": (
            "Under the August 2022 Union Cabinet decision, TKDL database access was democratized and opened to Indian users, researchers, "
            "educational institutions, and MSMEs. Innovators can register on tkdl.res.in for defensive prior art search before filing patent "
            "or trademark applications to avoid Section 3(p) objections and reduce unnecessary IP filing expenses."
        ),
        "metadata": {
            "source_name": "Traditional Knowledge Digital Library (Innovator Access)",
            "statute": "CSIR & Ministry of Ayush Prior Art Repository",
            "section": "Cabinet Access Resolution",
            "authority": "CSIR & Ministry of Ayush",
            "authority_level": 2,
            "jurisdiction": "India",
            "portal_url": "https://www.tkdl.res.in"
        }
    },
    {
        "id": "ipindia-tk-guidelines",
        "title": "IP India Guidelines for Examination of TK Patent Applications",
        "content": (
            "The Office of CGPDTM's Guidelines for Examination of Patent Applications relating to Traditional Knowledge and Biological Material "
            "mandate patent examiners to verify that claims involving herbal compositions are checked against TKDL and InPASS prior art records. "
            "If a polyherbal composition combines known herbs, the examiner must issue a Section 3(e) objection unless experimental comparative data "
            "clearly establishes synergy. The applicant must also complete NBA Form 1 declaration regarding source of biological resource."
        ),
        "metadata": {
            "source_name": "Office of CGPDTM Examination Guidelines",
            "statute": "Guidelines for Patent Examination of TK",
            "section": "Examination Guidelines 2020",
            "authority": "Office of the Controller General of Patents, Designs & Trade Marks (CGPDTM)",
            "authority_level": 1,
            "jurisdiction": "India",
            "portal_url": "https://ipindia.gov.in"
        }
    },
    {
        "id": "nba-abs-regulations-2014",
        "title": "NBA Access and Benefit-Sharing (ABS) Regulations, 2014 & Form III",
        "content": (
            "Under the Guidelines on Access to Biological Resources and Associated Knowledge and Benefits Sharing Regulations, 2014, "
            "commercial users accessing biological resources from India must execute an ABS agreement with the NBA. "
            "Benefit sharing ranges between 0.1% to 0.5% of ex-factory gross sales for commercial utilization, or 3.0% to 5.0% "
            "of the purchase price of the biological resource. Applicants filing patents must submit Form III on nbaindia.org "
            "and pay the statutory fee of Rs. 10,000 before patent grant."
        ),
        "metadata": {
            "source_name": "National Biodiversity Authority (ABS Regulations 2014)",
            "statute": "Guidelines on Access and Benefit Sharing Regulations, 2014",
            "section": "ABS Regulations 2014",
            "authority": "National Biodiversity Authority (NBA)",
            "authority_level": 1,
            "jurisdiction": "India",
            "portal_url": "https://nbaindia.org"
        }
    }
]
