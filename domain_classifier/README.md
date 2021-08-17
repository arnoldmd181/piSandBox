# Domain Classifier

The domain classifier is an ensemble of classification models designed to measure domain suspiciousness using features extracted from the FQDN.

## Model Structure

![model diagram](https://confluence-connect.gliffy.net/embed/image/63147d8e-bbdd-4487-b780-d0feabf28489.png?utm_medium=live&utm_source=custom)

## Training

You must have aws-okta set up with EDTR credentials in order to execute the following steps.

Load, clean, and save data:
```bash
[iron-predict-models]> aws-okta exec [YOUR-OKTA-PROFILE] -- python3 domain_classifier/scripts/gen_data.py
```

Use the data to build a vocabulary used for feature generation:
```bash
[iron-predict-models]> python3 domain_classifier/scripts/gen_vocab.py --upload-data
```

Generate features (this step is optional, since features are generated automatically upon training if they don't yet exist in the data):
```bash
[iron-predict-models]> python3 domain_classifier/scripts/enrich_data.py --upload-data
```

Train:
```bash
[iron-predict-models]> python3 domain_classifier/scripts/train.py
```

Model artifacts are nominally written to the `domain_classifier/saved_models/latest/`inside the model directory, but this is configurable.

Test model performance on independent data:
```bash
[iron-predict-models]> python3 domain_classifier/scripts/evaluate_model.py
```

Plots of model performance will nominally be saved to the `domain_classifier/plots` directory.

## Data Sources

Raw data for model building is extracted from both the ETDR database and from the `phishing-model-data/domain-classifier` S3 bucket on the DataScience AWS account.

The raw data in these locations is heavily curated before it is used for model building. This curation is handled by the `scripts/gen_data.py` and `scripts/gen_vocab.py` scripts. The process is summarized in the following sections.

### Labeled Domains

- **Benign** candidates:
 - A *static* BNYM sample is loaded from s3: `domain-classifier/sni-set-201901-01.csv`
 - A *static* Merck sample is loaded from s3: `domain-classifier/sni-set-201901-02.csv.bz2`
 - A *static* list of domains extracted by a majestic "prefetch" crawler (using `<link src`) is loaded from s3: `domain-classifier/majestic_crawlers/prefetch.csv`
 - A *static* list of domains extracted by a majestic "link" crawler (using `<a href`) is loaded from s3: `domain-classifier/majestic_crawlers/links.csv`
 - A *dynamic* umbrella sample is loaded from `http://s3-us-west-1.amazonaws.com/umbrella-static/top-1m.csv.zip`. Only the top 2K domains are used.
- **Malicious** candidates:
 - A *dynamic* list of domains from phishing feeds is loaded from DRT: `data.phish_urls`

In addition to these sources above, a *static* sample of mixed benign and malicious  domains is loaded from s3: `domain-classifier/phishing-sbx-201906.csv.bz2`. This list includes data that was originally used in a previous iteration of the classifier. It has overlap with samples above, but it also includes domains from Cerebro, simulated malicious domains, `IronDefense` finds, etc.

Lots of work is done in `scripts/gen_data.py` to prune mislabeled examples and  remove duplication. The cleaned lists are split into train, test, and validation datasets.

In addition, SLDs that show up repeatedly with the same label are saved to a local CSV file.

### Vocabulary

Dictionaries of brands, phishy words, popular embedded TLDs, popular domain tokens, etc, are constructed by passing various static and dynamic word lists through algorithms in `scripts/gen_vocab.py`. The following data sources are used:

- A *static* list of phishy words is loaded from s3: `domain-classifier/vocabulary/phishy_words.txt`
- A *static* list of whitelist words is loaded from s3: `domain-classifier/vocabulary/whitelist_words.txt`
- A *static* list of brands is loaded from s3: `domain-classifier/vocabulary/brands.txt`
- A *static* list of popular embedded public suffixes is loaded from s3: `domain-classifier/vocabulary/embedded_tlds.txt`
- A *static* list of common public suffix tokens is loaded from s3: `domain-classifier/vocabulary/public_suffix_tokens.txt`
- A *static* list of popular english edit distance matches that show up in malicious domains is loaded from s3: `domain-classifier/vocabulary/malicious_english_edist_matches.txt`. These are words that were identified when searching for popular edit distance spoofs. In general, english words are exluded from the list of popular edit distance spoofs, but occasionally a popular spoof word will be found in the english dictionary and still be phishy. When new candidates for this list are found by `scripts/gen_vocab.py` they are printed to logs, and then it is up to the user to expand the list.
- A *static* list of customer-owned SLDs taken from enterprise classification rules is loaded from s3: `domain-classifier/vocabulary/customer_slds.txt`. This should be updated on occasion.
- A *static* reduced list of *resolving* customer-owned SLDs is loaded from s3: `domain-classifier/vocabulary/resolving_customer_slds.txt`. This should be updated on occasion.
- A *static* list of large banks (from wikipedia) is loaded from s3: `domain-classifier/vocabulary/largest_banks.txt`. This should be updated on occasion.
- A *static* list of global banks (from wikipedia) is loaded from s3: `domain-classifier/vocabulary/global_banks.txt`. This should be updated on occasion.
- A *static* list of S&P 500 brands (from wikipedia) is loaded from s3: `domain-classifier/vocabulary/sp500.txt`. This should be updated on occasion.
- A *static* list of trusted brands (from wikipedia) is loaded from s3: `domain-classifier/vocabulary/trusted.txt`. This should be updated on occasion.
- A *static* list of unlabeled common domain words are loaded from s3: `domain-classifier/vocabulary/mixed.txt`. Brands, phishy words, and generic tokens are auto-magically extracted from this list.
- The *dynamic*  list of popular SLDs are loaded from the locally saved CSV. Brands, phishy words, and generic tokens are auto-magically extracted from this list.

The word lists above are curated automatically by `scripts/gen_vocab.py`.

Furthermore, the training data is used along with the curated vocabulary to identify popular misspellings and spoof words that show up in data.

The final dictionary of all keywords and their labels is saved locally to a CSV file, so it can be loaded and used by model components.
