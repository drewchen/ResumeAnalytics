## Cosine Similarity Between Documents

This analysis entails determining how similar documents are to a target document.  The original problem was determining how relevant 'technical' resumes are to positions in different technical fields such as IT, Analyst, and Software Developer.  To solve this problem, resumes of employees who already fill a position are combined to create a target document.  Then a set of candidate resumes is compared for similarity to the target document.  The end result does not assess how well a candidate may perform at a particular position but should associate people with relevant resumes to a particular position.

### Python Environment
Using Conda, Anaconda Python 3.5.1 :: Continuum Analytics, Inc. with requirements listed in [requirements.yml]()

Create environment via:
``` bash
conda env create
```

### Data Preparation

The resumes come in pdf form. Conversion to raw text is performed using the `pdftotext` utility.  Instructions for installation on OSX can be found [here](http://macappstore.org/pdftotext/).

### Analysis

An example analysis is shown in this [notebook](https://github.com/blakeboswell/nlp-resume/blob/master/newsgroup_test.ipynb)
