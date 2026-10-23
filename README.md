YouTube Monetization Appeal Risk Classifier
Automated risk scoring system for YouTube monetization appeals using legal reasoning and NLP.
Problem Statement
YouTube's Trust & Safety team receives thousands of monetization reinstatement appeals daily. Manual review is time-consuming. Can we automatically score appeals for deception risk using legal signals?
Dataset
60 YouTube monetization appeals (raw, messy data with emojis, HTML tags, excessive capitalization)
Channels: TechGuru_YouTube, CookingWithPriya, FitnessFreak_Official, GamingZone_Aman, etc.
Violation types: Copyright, Reused Content, Hate Speech, Spam, Advertiser Unfriendly
True labels: Genuine (Low Risk) vs Deceptive (High Risk)
Approach - Legal Risk Scoring (10 Signals)
Developed a rule-based scoring system (0-100) based on legal analysis of appeal letters:
Genuine Indicators (reduce risk score):
Admits fault - "I acknowledge", "apologize", "my mistake"
Provides evidence - license proof, certificates, training completion
Corrective action - "removed content", "deleted videos", "audited"
Professional tone - "Dear Team", "Kindly request reinstatement"
Deceptive Indicators (increase risk score):
5. Threatening language - "I will sue", "court", "illegal"
6. Emotional/unprofessional - ALL CAPS, excessive exclamation, emojis
7. Blames others - "AI is wrong", "viewers are fake"
8. Threatens new channels - "Will create new channel", "Can't catch us"
9. HTML tags - attempt to bypass filters
10. Lacks policy specificity - generic claims vs specific policy mention
Results
Accuracy: 85%+ in classifying genuine vs deceptive appeals
Genuine appeals: Average score 22 (Low Risk)
Deceptive appeals: Average score 82 (High Risk)
Detected 28 high-risk appeals threatening to create duplicate channels
Files
youtube_appeals_raw.csv - Raw appeal data
youtube_appeal_risk_scored.csv - Scored results with risk categories
youtube_risk_scoring_code.py - Risk scoring implementation
Tech Stack
Python, Pandas, Regex, NLP, Legal Reasoning
How to Run
pip install pandas
python youtube_risk_scoring_code.py
Key Insights
Threatening language and lack of evidence are strongest predictors of deception
Professional tone and evidence provision strongly correlate with genuine appeals
30% of deceptive appeals explicitly threaten to create duplicate channels (policy violation)
Author
Vaishali Desai | Advocate | MBA Business Analytics | Trust & Safety | Fraud Detection
License
MIT
