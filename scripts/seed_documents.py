"""Seed authoritative statutory documents and chunks into the database.

Populates authentic legal documents and statutory provisions from:
- India Code (The Patents Act, Biological Diversity Act, Drugs and Cosmetics Act, Trade Marks Act)
- IP India Public Databases (Examination Guidelines, InPASS, Trade Marks Manual)
- National Biodiversity Authority (ABS Regulations, Form I-IV, Section 40 NTC)
- Traditional Knowledge Digital Library (TKDL Defensive Repository & TKRC)
- FSSAI (Ayurveda Aahara Regulations 2022)
"""

import asyncio
import os
import sys
import uuid
import hashlib
from datetime import datetime, date
from sqlalchemy import select

backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend'))
sys.path.append(backend_path)

from app.database import init_db, async_session_maker
from app.models.source import Source
from app.models.document import Document, DocumentVersion, DocumentChunk, LegalProvision

DOCUMENTS_DATA = [
    {
        "source_match": "The Patents Act",
        "title": "The Patents Act, 1970 (Statutory Exclusions & Origin Disclosure)",
        "document_type": "legislation",
        "statute": "The Patents Act, 1970",
        "jurisdiction": "India",
        "country": "IN",
        "language": "en",
        "topics": ["patents", "traditional_knowledge", "synergy", "biological_resources", "prior_art"],
        "chunks": [
            {
                "chunk_id": "patents-act-3p",
                "section": "Section 3(p)",
                "content": (
                    "Section 3(p) of The Patents Act, 1970 provides that an invention which in effect is traditional knowledge "
                    "or which is an aggregation or duplication of known properties of traditionally known component or components "
                    "is not an invention within the meaning of this Act. Classical Ayurvedic formulations described in authoritative "
                    "treatises listed in the First Schedule to the Drugs and Cosmetics Act, 1940 (such as Charaka Samhita, Sushruta Samhita, "
                    "Ashtanga Hridaya, and Ayurvedic Formulary of India) are codified traditional knowledge documented in the Traditional "
                    "Knowledge Digital Library (TKDL, tkdl.res.in). Any claim directed to a classical recipe or obvious herbal property "
                    "is barred from patentability and publicly searchable on InPASS (ipindia.gov.in)."
                ),
                "metadata": {
                    "source_title": "The Patents Act, 1970 (India Code)",
                    "statute": "The Patents Act, 1970",
                    "section": "Section 3(p)",
                    "authority": "Office of Controller General of Patents, Designs & Trade Marks (CGPDTM)",
                    "authority_level": 1,
                    "jurisdiction": "India",
                    "portal_url": "https://www.indiacode.nic.in/handle/123456789/1392"
                }
            },
            {
                "chunk_id": "patents-act-3e",
                "section": "Section 3(e)",
                "content": (
                    "Section 3(e) of The Patents Act, 1970 excludes from patentability a substance obtained by a mere admixture "
                    "resulting only in the aggregation of the properties of the components thereof or a process for producing such substance. "
                    "For polyherbal Ayurvedic compositions, patent applicants must demonstrate unexpected synergistic therapeutic effect "
                    "with empirical quantitative laboratory data (such as Combination Index CI < 1.0, isobolographic analysis, or significant "
                    "bioavailability enhancement) to overcome Section 3(e) objections during InPASS patent examination (ipindia.gov.in)."
                ),
                "metadata": {
                    "source_title": "The Patents Act, 1970 (IP India Public Database)",
                    "statute": "The Patents Act, 1970",
                    "section": "Section 3(e)",
                    "authority": "Office of Controller General of Patents, Designs & Trade Marks (CGPDTM)",
                    "authority_level": 1,
                    "jurisdiction": "India",
                    "portal_url": "https://ipindia.gov.in"
                }
            },
            {
                "chunk_id": "patents-act-3d",
                "section": "Section 3(d)",
                "content": (
                    "Section 3(d) of The Patents Act, 1970 bars the mere discovery of a new form of a known substance which does not result "
                    "in the enhancement of the known efficacy of that substance. In the context of Ayurvedic phytopharmaceuticals, standardized fractions, "
                    "or isolated herbal extracts, the applicant must establish proof of enhanced therapeutic efficacy (Novartis AG v. Union of India standard) "
                    "over conventional crude herbal extracts or known compounds."
                ),
                "metadata": {
                    "source_title": "The Patents Act, 1970 (India Code)",
                    "statute": "The Patents Act, 1970",
                    "section": "Section 3(d)",
                    "authority": "Office of Controller General of Patents, Designs & Trade Marks (CGPDTM)",
                    "authority_level": 1,
                    "jurisdiction": "India",
                    "portal_url": "https://www.indiacode.nic.in/handle/123456789/1392"
                }
            },
            {
                "chunk_id": "patents-act-10-4",
                "section": "Section 10(4)(d)(ii)",
                "content": (
                    "Section 10(4)(d)(ii) of The Patents Act, 1970 mandates that if an applicant mentions any biological material in the specification "
                    "which is obtained from India, the application must disclose the source and geographical origin of the biological material. "
                    "Furthermore, mandatory declaration on Form 1 must state whether prior approval of the National Biodiversity Authority (NBA) "
                    "has been obtained or applied for under Section 6 of the Biological Diversity Act, 2002."
                ),
                "metadata": {
                    "source_title": "The Patents Act, 1970 (Disclosure of Biological Origin)",
                    "statute": "The Patents Act, 1970",
                    "section": "Section 10(4)(d)(ii)",
                    "authority": "Office of Controller General of Patents, Designs & Trade Marks (CGPDTM)",
                    "authority_level": 1,
                    "jurisdiction": "India",
                    "portal_url": "https://www.indiacode.nic.in/handle/123456789/1392"
                }
            },
            {
                "chunk_id": "patents-act-25-opposition",
                "section": "Section 25",
                "content": (
                    "Under Section 25(1) (pre-grant opposition) and Section 25(2) (post-grant opposition) of The Patents Act, 1970, "
                    "any person or third party may oppose a patent application on grounds that the complete specification does not disclose "
                    "or wrongly mentions the source or geographical origin of biological material used for the invention, or that the invention "
                    "claimed was anticipated having regard to the knowledge, oral or otherwise, available within any local or indigenous community in India or elsewhere."
                ),
                "metadata": {
                    "source_title": "The Patents Act, 1970 (TK Oppositions)",
                    "statute": "The Patents Act, 1970",
                    "section": "Section 25",
                    "authority": "Office of Controller General of Patents, Designs & Trade Marks (CGPDTM)",
                    "authority_level": 1,
                    "jurisdiction": "India",
                    "portal_url": "https://ipindia.gov.in"
                }
            }
        ]
    },
    {
        "source_match": "The Biological Diversity Act",
        "title": "The Biological Diversity Act, 2002 & 2023 Amendment (ABS Framework)",
        "document_type": "legislation",
        "statute": "The Biological Diversity Act, 2002",
        "jurisdiction": "India",
        "country": "IN",
        "language": "en",
        "topics": ["abs", "biodiversity", "nba", "sbb", "cultivated_plants"],
        "chunks": [
            {
                "chunk_id": "bd-act-sec-6",
                "section": "Section 6 (Mandatory NBA Approval for IPR)",
                "content": (
                    "Section 6(1) of the Biological Diversity Act, 2002 mandates that no person shall apply for any intellectual property right, "
                    "by whatever name called, in or outside India for any invention based on any research or information on a biological resource "
                    "obtained from India without obtaining the previous approval of the National Biodiversity Authority (NBA, nbaindia.org) prior to applying for such right. "
                    "Mandatory application must be filed on NBA Form III (Form I for foreign entities) accessible on nbaindia.org. "
                    "Approval must be granted before the patent is sealed by the patent office."
                ),
                "metadata": {
                    "source_title": "National Biodiversity Authority / ABS Portal",
                    "statute": "The Biological Diversity Act, 2002",
                    "section": "Section 6 (IPR Prior Approval)",
                    "authority": "National Biodiversity Authority (NBA)",
                    "authority_level": 1,
                    "jurisdiction": "India",
                    "portal_url": "https://nbaindia.org"
                }
            },
            {
                "chunk_id": "bd-act-sec-7-2023",
                "section": "Section 7 (Codified TK & Cultivated Plants Exemption)",
                "content": (
                    "Under the Biological Diversity (Amendment) Act, 2023, Section 7 was amended to provide that users of codified traditional knowledge, "
                    "cultivated medicinal plants, and registered AYUSH practitioners (Vaidyas and Hakims) are exempt from giving prior intimation to the "
                    "State Biodiversity Board (SBB) for accessing biological resources for commercial utilization or manufacturing of classical Ayurvedic products. "
                    "Commercial utilization of wild-harvested biological resources by Indian companies still requires prior intimation to the relevant SBB."
                ),
                "metadata": {
                    "source_title": "India Code — Biological Diversity (Amendment) Act, 2023",
                    "statute": "Biological Diversity Act, 2002 (amended 2023)",
                    "section": "Section 7 (Codified TK Exemption)",
                    "authority": "National Biodiversity Authority (NBA)",
                    "authority_level": 1,
                    "jurisdiction": "India",
                    "portal_url": "https://www.indiacode.nic.in"
                }
            },
            {
                "chunk_id": "bd-act-sec-40-ntc",
                "section": "Section 40 (Normally Traded Commodities)",
                "content": (
                    "Section 40 of the Biological Diversity Act empowers the Central Government to exempt certain biological resources normally traded as commodities "
                    "from the provisions of the Act. The Ministry of Environment, Forest and Climate Change has notified 421+ biological species "
                    "(including Black Pepper, Ginger, Turmeric, Clove, Cinnamon, Cumin, Fenugreek) as Normally Traded Commodities (NTC). "
                    "NTC exemption applies ONLY when the biological resource is traded strictly as an agricultural/horticultural commodity, and does NOT apply "
                    "when it is accessed for research, patenting, or biotechnology applications."
                ),
                "metadata": {
                    "source_title": "National Biodiversity Authority — Section 40 NTC List",
                    "statute": "The Biological Diversity Act, 2002",
                    "section": "Section 40 (NTC Exemption)",
                    "authority": "National Biodiversity Authority (NBA)",
                    "authority_level": 1,
                    "jurisdiction": "India",
                    "portal_url": "https://nbaindia.org"
                }
            }
        ]
    },
    {
        "source_match": "The Drugs and Cosmetics Act",
        "title": "The Drugs and Cosmetics Act, 1940 & Rules (ASU Drug Regulations)",
        "document_type": "legislation",
        "statute": "The Drugs and Cosmetics Act, 1940",
        "jurisdiction": "India",
        "country": "IN",
        "language": "en",
        "topics": ["asu_drugs", "classical_medicine", "proprietary_medicine", "gmp", "schedule_t"],
        "chunks": [
            {
                "chunk_id": "dc-act-classical-3a",
                "section": "Section 3(a) & Schedule T (GMP)",
                "content": (
                    "Section 3(a) of the Drugs and Cosmetics Act, 1940 (available on indiacode.nic.in) defines Ayurvedic, Siddha or Unani (ASU) drugs "
                    "manufactured exclusively in accordance with the formulae described in authoritative books specified in the First Schedule. "
                    "Classical formulations require manufacturing license on Form 25-D from State Licensing Authority (AYUSH) "
                    "and mandatory compliance with Schedule T Good Manufacturing Practices (GMP) for infrastructure, batch records, quality control, and hygiene."
                ),
                "metadata": {
                    "source_title": "The Drugs and Cosmetics Act, 1940 (India Code)",
                    "statute": "Drugs and Cosmetics Act, 1940",
                    "section": "Section 3(a) & Schedule T",
                    "authority": "Ministry of Ayush / State Licensing Authorities",
                    "authority_level": 1,
                    "jurisdiction": "India",
                    "portal_url": "https://www.indiacode.nic.in"
                }
            },
            {
                "chunk_id": "dc-act-prop-3h",
                "section": "Section 3(h) & Rule 158-B (Patent or Proprietary Medicine)",
                "content": (
                    "Section 3(h) of Drugs and Cosmetics Act defines Patent or Proprietary (P&P) Ayurvedic Medicine containing ingredients "
                    "from First Schedule treatises but not manufactured verbatim to classical recipes. Rule 158-B of the Drugs and Cosmetics Rules, 1945 "
                    "governs licensing, requiring textual citations, pilot safety studies, and published scientific literature. Proof of safety (acute and chronic "
                    "toxicity) and proof of efficacy must be submitted to the State Licensing Authority on Form 25-D."
                ),
                "metadata": {
                    "source_title": "Drugs and Cosmetics Rules, 1945 (India Code)",
                    "statute": "Drugs and Cosmetics Rules, 1945",
                    "section": "Rule 158-B & Section 3(h)",
                    "authority": "Ministry of Ayush",
                    "authority_level": 1,
                    "jurisdiction": "India",
                    "portal_url": "https://www.indiacode.nic.in"
                }
            },
            {
                "chunk_id": "dc-act-schedule-e1",
                "section": "Schedule E(1) (Poisonous Substances)",
                "content": (
                    "Schedule E(1) to the Drugs and Cosmetics Rules, 1945 lists poisonous substances of plant, mineral, and animal origin used in Ayurvedic medicines, "
                    "such as Aconitum (Vatsanabha), Semecarpus anacardium (Bhallataka), Strychnos nux-vomica (Kupilu), Datura, and Mercury compounds (Parada). "
                    "Medicines containing Schedule E(1) ingredients require mandatory detoxification (Shodhana) as per classical methods, "
                    "clear cautionary warning labels ('Caution: To be taken under medical supervision'), and strict batch testing."
                ),
                "metadata": {
                    "source_title": "Drugs and Cosmetics Rules — Schedule E(1)",
                    "statute": "Drugs and Cosmetics Rules, 1945",
                    "section": "Schedule E(1)",
                    "authority": "Ministry of Ayush",
                    "authority_level": 1,
                    "jurisdiction": "India",
                    "portal_url": "https://www.indiacode.nic.in"
                }
            }
        ]
    },
    {
        "source_match": "Traditional Knowledge Digital Library",
        "title": "Traditional Knowledge Digital Library (TKDL) Prior Art Database",
        "document_type": "guideline",
        "statute": "CSIR & Ayush TKDL Repository",
        "jurisdiction": "India",
        "country": "IN",
        "language": "en",
        "topics": ["tkdl", "prior_art", "tkrc", "biopiracy", "classical_treatises"],
        "chunks": [
            {
                "chunk_id": "tkdl-prior-art",
                "section": "TKRC Classification & Treatises",
                "content": (
                    "The Traditional Knowledge Digital Library (TKDL, tkdl.res.in) is a pioneer database created by CSIR and the Ministry of Ayush "
                    "containing over 4.5 lakh formulations from classical Ayurvedic treatises (Charaka Samhita, Sushruta Samhita, Astanga Hridaya, "
                    "Sharangadhara Samhita, and Bhaishajya Ratnavali) translated into five international languages (English, French, German, Japanese, Spanish) "
                    "structured in Traditional Knowledge Resource Classification (TKRC) mapped to the International Patent Classification (IPC). "
                    "TKDL has successfully prevented over 1,500 wrongful patent grants internationally across USPTO, EPO, and JPO."
                ),
                "metadata": {
                    "source_title": "Traditional Knowledge Digital Library (TKDL)",
                    "statute": "CSIR & Ministry of Ayush Prior Art Repository",
                    "section": "TKRC Classification",
                    "authority": "CSIR & Ministry of Ayush",
                    "authority_level": 2,
                    "jurisdiction": "India",
                    "portal_url": "https://www.tkdl.res.in"
                }
            },
            {
                "chunk_id": "tkdl-user-access",
                "section": "Cabinet Decision on User Access for Innovators",
                "content": (
                    "Under the August 2022 Union Cabinet decision, TKDL database access was democratized and opened to Indian users, researchers, "
                    "educational institutions, and MSMEs. Innovators can register on tkdl.res.in for defensive prior art search before filing patent "
                    "or trademark applications to avoid Section 3(p) objections and reduce unnecessary IP filing expenses."
                ),
                "metadata": {
                    "source_title": "Traditional Knowledge Digital Library (Innovator Access)",
                    "statute": "CSIR & Ministry of Ayush Prior Art Repository",
                    "section": "Cabinet Access Resolution",
                    "authority": "CSIR & Ministry of Ayush",
                    "authority_level": 2,
                    "jurisdiction": "India",
                    "portal_url": "https://www.tkdl.res.in"
                }
            }
        ]
    },
    {
        "source_match": "The Trade Marks Act",
        "title": "The Trade Marks Act, 1999 (Herbal Brands & Generic Name Standards)",
        "document_type": "legislation",
        "statute": "The Trade Marks Act, 1999",
        "jurisdiction": "India",
        "country": "IN",
        "language": "en",
        "topics": ["trademarks", "brand_names", "publici_juris", "cadila_standard"],
        "chunks": [
            {
                "chunk_id": "trademarks-ayurveda-names",
                "section": "Section 9 & Section 11 (Publici Juris Classical Names)",
                "content": (
                    "Under Section 9 of the Trade Marks Act, 1999 (indiacode.nic.in & ipindia.gov.in), descriptive and generic terms lack distinctiveness. "
                    "Names of classical Ayurvedic medicines (e.g., Triphala, Chyawanprash, Dashamularishta, Ashwagandharishta) are publici juris "
                    "and cannot be registered as an exclusive monopoly trademark. Trademark public search on ipindia.gov.in applies the Supreme Court's "
                    "Cadila Healthcare standard (Cadila Health Care v. Cadila Pharmaceuticals, 2001) which establishes a strict threshold against confusingly "
                    "similar medicinal brand names to protect public health."
                ),
                "metadata": {
                    "source_title": "IP India Public Databases — Trade Marks Registry",
                    "statute": "Trade Marks Act, 1999",
                    "section": "Section 9 & Section 11",
                    "authority": "Trade Marks Registry / CGPDTM",
                    "authority_level": 1,
                    "jurisdiction": "India",
                    "portal_url": "https://ipindia.gov.in"
                }
            }
        ]
    },
    {
        "source_match": "Ayurveda Aahara",
        "title": "Food Safety and Standards (Ayurveda Aahara) Regulations, 2022",
        "document_type": "regulation",
        "statute": "Food Safety and Standards Act, 2006",
        "jurisdiction": "India",
        "country": "IN",
        "language": "en",
        "topics": ["ayurveda_aahara", "fssai", "food_safety", "labelling", "claims"],
        "chunks": [
            {
                "chunk_id": "fssai-ayurveda-aahara",
                "section": "Ayurveda Aahara Regulations, 2022",
                "content": (
                    "Under the Food Safety and Standards (Ayurveda Aahara) Regulations, 2022 (fssai.gov.in), foods prepared in accordance with "
                    "authoritative Ayurvedic treatises listed in Schedule A are classified as 'Ayurveda Aahara'. Such products must carry the mandatory "
                    "Ayurveda Aahara logo and clear front-of-pack advisory ('Not for medicinal use'). Such products are strictly prohibited from making "
                    "claims to prevent, treat, or cure human diseases."
                ),
                "metadata": {
                    "source_title": "Food Safety and Standards Authority of India (FSSAI)",
                    "statute": "Food Safety and Standards Act, 2006",
                    "section": "Ayurveda Aahara Regulations, 2022",
                    "authority": "Food Safety and Standards Authority of India (FSSAI)",
                    "authority_level": 2,
                    "jurisdiction": "India",
                    "portal_url": "https://fssai.gov.in"
                }
            }
        ]
    },
    {
        "source_match": "IP India Public Databases",
        "title": "IP India Examination Guidelines for Traditional Knowledge & Biodiversity",
        "document_type": "guideline",
        "statute": "Patent Office Examination Guidelines",
        "jurisdiction": "India",
        "country": "IN",
        "language": "en",
        "topics": ["patent_examination", "inpass", "synergy_testing", "biological_scrutiny"],
        "chunks": [
            {
                "chunk_id": "ipindia-tk-guidelines",
                "section": "Guidelines for Examination of TK Patent Applications",
                "content": (
                    "The Office of CGPDTM's Guidelines for Examination of Patent Applications relating to Traditional Knowledge and Biological Material "
                    "mandate patent examiners to verify that claims involving herbal compositions are checked against TKDL and InPASS prior art records. "
                    "If a polyherbal composition combines known herbs, the examiner must issue a Section 3(e) objection unless experimental comparative data "
                    "clearly establishes synergy. The applicant must also complete NBA Form 1 declaration regarding source of biological resource."
                ),
                "metadata": {
                    "source_title": "Office of CGPDTM Examination Guidelines",
                    "statute": "Guidelines for Patent Examination of TK",
                    "section": "Examination Guidelines 2020",
                    "authority": "Office of the Controller General of Patents, Designs & Trade Marks (CGPDTM)",
                    "authority_level": 1,
                    "jurisdiction": "India",
                    "portal_url": "https://ipindia.gov.in"
                }
            }
        ]
    },
    {
        "source_match": "National Biodiversity Authority (NBA",
        "title": "NBA Access and Benefit-Sharing (ABS) Regulations & Forms Guide",
        "document_type": "regulation",
        "statute": "The Biological Diversity Act, 2002",
        "jurisdiction": "India",
        "country": "IN",
        "language": "en",
        "topics": ["abs_regulations", "benefit_sharing", "form_iii", "form_i"],
        "chunks": [
            {
                "chunk_id": "nba-abs-regulations-2014",
                "section": "ABS Regulations 2014 & Benefit-Sharing Formula",
                "content": (
                    "Under the Guidelines on Access to Biological Resources and Associated Knowledge and Benefits Sharing Regulations, 2014, "
                    "commercial users accessing biological resources from India must execute an ABS agreement with the NBA. "
                    "Benefit sharing ranges between 0.1% to 0.5% of ex-factory gross sales for commercial utilization, or 3.0% to 5.0% "
                    "of the purchase price of the biological resource. Applicants filing patents must submit Form III on nbaindia.org "
                    "and pay the statutory fee of Rs. 10,000 before patent grant."
                ),
                "metadata": {
                    "source_title": "National Biodiversity Authority (ABS Regulations 2014)",
                    "statute": "Guidelines on Access and Benefit Sharing Regulations, 2014",
                    "section": "ABS Regulations 2014",
                    "authority": "National Biodiversity Authority (NBA)",
                    "authority_level": 1,
                    "jurisdiction": "India",
                    "portal_url": "https://nbaindia.org"
                }
            }
        ]
    },
    {
        "source_match": "WIPO Treaty",
        "title": "WIPO Treaty on Intellectual Property, Genetic Resources and Associated Traditional Knowledge (2024)",
        "document_type": "treaty",
        "statute": "WIPO GRATK Treaty (Adopted May 2024)",
        "jurisdiction": "International",
        "country": "GLOBAL",
        "language": "en",
        "topics": ["wipo", "gratk", "international_disclosure", "genetic_resources"],
        "chunks": [
            {
                "chunk_id": "wipo-gratk-treaty-2024",
                "section": "Article 3 (Mandatory Disclosure Requirement)",
                "content": (
                    "Adopted at WIPO in Geneva in May 2024, the Treaty on Intellectual Property, Genetic Resources and Associated Traditional Knowledge establishes "
                    "a mandatory international patent disclosure requirement. Patent applicants across contracting member states must disclose the country of origin "
                    "of genetic resources or the indigenous community providing associated traditional knowledge if claimed inventions are based on them."
                ),
                "metadata": {
                    "source_title": "World Intellectual Property Organization (WIPO)",
                    "statute": "WIPO Treaty on IP, Genetic Resources & Associated TK",
                    "section": "Article 3 (Mandatory Disclosure)",
                    "authority": "World Intellectual Property Organization (WIPO)",
                    "authority_level": 1,
                    "jurisdiction": "International",
                    "portal_url": "https://www.wipo.int/tk/en/"
                }
            }
        ]
    }
]

async def seed_documents():
    await init_db()
    async with async_session_maker() as session:
        try:
            sources_res = await session.execute(select(Source))
            sources = sources_res.scalars().all()
            if not sources:
                print("[ERROR] No sources found in database. Run seed_sources.py first!")
                return

            print(f"[INFO] Found {len(sources)} sources in database.")
            total_docs_created = 0
            total_chunks_created = 0

            for doc_data in DOCUMENTS_DATA:
                matched_source = None
                for s in sources:
                    if doc_data["source_match"].lower() in s.name.lower() or doc_data["source_match"].lower() in s.url.lower():
                        matched_source = s
                        break
                if not matched_source:
                    matched_source = sources[0]

                existing_doc_res = await session.execute(
                    select(Document).where(Document.title == doc_data["title"])
                )
                existing_doc = existing_doc_res.scalars().first()

                if existing_doc:
                    doc = existing_doc
                    print(f"  [SKIP] Document '{doc.title}' already exists.")
                else:
                    doc = Document(
                        id=uuid.uuid4(),
                        source_id=matched_source.id,
                        title=doc_data["title"],
                        document_type=doc_data["document_type"],
                        jurisdiction=doc_data["jurisdiction"],
                        country=doc_data["country"],
                        statute=doc_data["statute"],
                        status="current",
                        language=doc_data["language"],
                        topics=doc_data["topics"],
                        metadata_={
                            "portal_url": matched_source.url,
                            "authority": matched_source.authority,
                            "authority_level": matched_source.authority_level
                        }
                    )
                    session.add(doc)
                    await session.flush()
                    total_docs_created += 1
                    print(f"  [CREATED] Document: '{doc.title}'")

                v_res = await session.execute(
                    select(DocumentVersion).where(DocumentVersion.document_id == doc.id)
                )
                existing_v = v_res.scalars().first()
                if not existing_v:
                    combined_content = "\n\n".join([c["content"] for c in doc_data["chunks"]])
                    content_hash = hashlib.sha256(combined_content.encode("utf-8")).hexdigest()
                    version = DocumentVersion(
                        id=uuid.uuid4(),
                        document_id=doc.id,
                        version_number=1,
                        content_hash=content_hash,
                        raw_content=combined_content,
                        source_url=matched_source.url,
                        effective_from=date(2020, 1, 1),
                        version_status="current",
                        fetched_at=datetime.utcnow()
                    )
                    session.add(version)
                    await session.flush()
                else:
                    version = existing_v

                for i, chunk_spec in enumerate(doc_data["chunks"]):
                    c_res = await session.execute(
                        select(DocumentChunk).where(
                            DocumentChunk.document_id == doc.id,
                            DocumentChunk.chunk_index == i
                        )
                    )
                    existing_c = c_res.scalars().first()
                    if not existing_c:
                        chunk_id_str = chunk_spec["chunk_id"]
                        try:
                            cid = uuid.UUID(chunk_id_str)
                        except ValueError:
                            cid = uuid.uuid5(uuid.NAMESPACE_DNS, chunk_id_str)

                        meta = chunk_spec.get("metadata", {})
                        meta["chunk_tag"] = chunk_spec["chunk_id"]

                        db_chunk = DocumentChunk(
                            id=cid,
                            document_version_id=version.id,
                            document_id=doc.id,
                            chunk_index=i,
                            content=chunk_spec["content"],
                            section=chunk_spec.get("section"),
                            rule=chunk_spec.get("rule"),
                            metadata_=meta,
                            embedding_model="statutory-hybrid-384"
                        )
                        session.add(db_chunk)
                        total_chunks_created += 1

                        legal_prov = LegalProvision(
                            id=uuid.uuid4(),
                            document_id=doc.id,
                            act_name=doc.statute or doc.title,
                            section_number=chunk_spec.get("section"),
                            provision_text=chunk_spec["content"],
                            status="current",
                            jurisdiction=doc.jurisdiction,
                            country=doc.country
                        )
                        session.add(legal_prov)

            await session.commit()
            print(f"\n[SUCCESS] Seeded {total_docs_created} documents and {total_chunks_created} statutory chunks into database!")
        except Exception as e:
            print(f"[ERROR] Failed to seed documents: {e}")
            await session.rollback()
            raise

if __name__ == "__main__":
    asyncio.run(seed_documents())

