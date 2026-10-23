"""
YouTube Monetization Appeal Risk Classifier
Project 2 for Google Trust & Safety - Hyderabad
Author: Vaishali Desai - Advocate + Business Analyst

Scores YouTube monetization appeals 0-100 for deception risk
Used by Google YouTube Trust & Safety team in Hyderabad
"""

import pandas as pd
import re

df = pd.read_csv('youtube_appeals_raw.csv')
print(f"Loaded {len(df)} YouTube appeals")

def calculate_youtube_risk_score(text):
    """Scores appeal 0 (Genuine) to 100 (Deceptive) - 10 legal signals"""
    text_lower = str(text).lower()
    text_raw = str(text)
    score = 0
    signals = {}
    
    # 1. Admits fault?
    if any(w in text_lower for w in ['acknowledge', 'admit', 'apologize', 'my fault', 'my mistake', 'responsibility', 'sorry']):
        signals['admits_fault'] = True
        score -= 20
    else:
        signals['admits_fault'] = False
        score += 15
    
    # 2. Has evidence?
    if any(w in text_lower for w in ['license', 'attached', 'proof', 'certificate', 'copyright school', 'audit', 'evidence']):
        signals['has_evidence'] = True
        score -= 20
    else:
        signals['has_evidence'] = False
        score += 20
    
    # 3. Threatening language?
    if any(w in text_lower for w in ['sue', 'court', 'lawyer', 'illegal', 'harassment', 'complain to govt']):
        signals['threatening'] = True
        score += 25
    else:
        signals['threatening'] = False
    
    # 4. Emotional / CAPS / Emojis
    caps = len(re.findall(r'[A-Z]{4,}', text_raw))
    exclaim = text_raw.count('!')
    emoji = len(re.findall(r'[😭😂🔥💥]', text_raw))
    if caps > 2 or exclaim > 3 or emoji > 0:
        signals['emotional'] = True
        score += 15
    else:
        signals['emotional'] = False
    
    # 5. Blames others?
    if any(w in text_lower for w in ['viewers are fake', 'ai is wrong', 'system is flawed', 'jealous']):
        signals['blames'] = True
        score += 20
    else:
        signals['blames'] = False
    
    # 6. Corrective action?
    if any(w in text_lower for w in ['removed', 'deleted', 'audited', 'creator academy', 'copyright school', 'qc checks']):
        signals['corrective'] = True
        score -= 10
    else:
        signals['corrective'] = False
        score += 5
    
    # 7. Threatens new channel?
    if any(w in text_lower for w in ['new channel', 'create new', '2.0 tomorrow', 'cant catch us', '10 new channels']):
        signals['new_channel_threat'] = True
        score += 30
    else:
        signals['new_channel_threat'] = False
    
    # 8. HTML tags?
    if re.search(r'<[^>]+>', text_raw):
        signals['html'] = True
        score += 10
    else:
        signals['html'] = False
    
    # 9. Mentions policy?
    if any(w in text_lower for w in ['policy', 'copyright', 'monetization', 'guideline']):
        signals['policy_mention'] = True
        score -= 5
    
    # 10. Professional tone?
    if any(w in text_lower for w in ['dear youtube team', 'respected team', 'kindly', 'thank you', 'request reinstatement']):
        signals['professional'] = True
        score -= 10
    
    score = max(0, min(100, score + 50))
    return score, signals

results = []
for _, row in df.iterrows():
    score, sig = calculate_youtube_risk_score(row['appeal_text_raw'])
    results.append({
        'appeal_id': row['appeal_id'],
        'channel_name': row['channel_name_clean'],
        'true_label': row['true_label'],
        'risk_score': score,
        'risk_category': 'HIGH RISK - Deceptive' if score >= 60 else 'LOW RISK - Genuine',
        'admits_fault': sig['admits_fault'],
        'has_evidence': sig['has_evidence'],
        'threatening': sig['threatening']
    })

results_df = pd.DataFrame(results)
print(results_df.head(10).to_string(index=False))

correct = sum(1 for _, r in results_df.iterrows() if (r['true_label']=='Deceptive' and r['risk_score']>=60) or (r['true_label']=='Genuine' and r['risk_score']<60))
print(f"\nAccuracy: {correct}/{len(results_df)} = {correct/len(results_df)*100:.1f}%")

results_df.to_csv('youtube_appeal_risk_scored.csv', index=False)
print("\nSaved: youtube_appeal_risk_scored.csv")

# Summary for dashboard
summary = results_df.groupby('risk_category').size()
print("\nSummary:")
print(summary)
print("\nThis is exactly what Google Hyderabad YouTube Trust & Safety team does daily!")
