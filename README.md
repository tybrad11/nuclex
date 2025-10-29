# NucLex: The Nuclear Medicine Lexicon

**NucLex is a formal, community-driven ontology for the domain of nuclear medicine.**

NucLex was initiated by the SNMMI AI Task Force, and is currently being developed and maintained by the NucLex Committee, led by Dr. Tyler Bradshaw (Director) and Dr. Babak Saboury (Co-Director). 

This repository contains the official Web Ontology Language (OWL) files for NucLex. The goal of this project is to create a standardized, computable vocabulary for nuclear medicine concepts, including procedures, radiopharmaceuticals, imaging equipment, dosimetry, and quantitative analysis. 

This standardized vocabulary is intended to support data annotation, integration, and analysis in both clinical practice and research, enabling more robust, interoperable, and AI-driven applications.

## ⚠️ Project Status: Beta

NucLex is currently in **active, early-stage development**. The structure, terms, and hierarchies are subject to change based on community feedback. We are actively seeking collaborators, reviewers, and contributors.

## Key Scope & Design

NucLex aims to model the key entities and relationships in the nuclear medicine domain. The example classes include:

* `Radiopharmaceutical`: A detailed hierarchy of diagnostic and therapeutic agents, categorized by isotope (e.g., `18F`, `177Lu`), target (e.g., `prostate-specific membrane antigen`), and purpose.
* `Treatment`: Describes radiopharmaceutical therapies (e.g., `peptide receptor radionuclide therapy`).
* `Imaging Observation`: Defines quantitative and qualitative measurements derived from images (e.g., `standardized uptake value measurement`, `Deauville five-point scale`).
* `Medical Device`: Includes nuclear medicine scanners (e.g., `positron emission tomography/computed tomography scanner`), detectors, and phantoms.
* `Medical Device Property`: Captures the attributes and performance characteristics of devices (e.g., `spatial resolution`, `collimator energy rating`).
etc.

## 🚀 How to Use NucLex

### Browsing the Ontology
The easiest way to view and explore the NucLex ontology is with a free, open-source ontology editor like [Protégé](https://protege.stanford.edu/):

1.  Download and install [Protégé Desktop](https://protege.stanford.edu/products.php#desktop-protege).
2.  Clone this repository or download the `nuclex.owl` file.
3.  Open `nuclex.owl` in Protégé.

(note: NucLex is not easily viewable in WebProtégé because the class names are stored in AnnotationProperty PreferredName -- an unfortunate bug of the online software)

Scripts: 
Several scripts are provided that were used to identify terms from nuclear medicine literature. Scripts are also provided that were used to convert between a csv-formatted ontology to an OWL ontology. 
