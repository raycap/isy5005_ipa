# isy5005_ipa


### Installment

using pip
```
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

using anaconda
```
conda create -n isy5005_ipa python=3.7.1
conda activate isy5005_ipa
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### Usage

```
python main.py --slack_url your_slack_bot_url
```