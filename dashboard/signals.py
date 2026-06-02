import pandas as pd

def derive_trend_signal(row) -> str:
    sentiment = row['sentiment_score']
    momentum = row['pct_change_7d']
    insider_net = row['insider_bought'] - row['insider_sold']
    
    bullish_signals = 0
    bearish_signals = 0

    if sentiment > 0.1:
        bullish_signals += 1
    elif sentiment < -0.1:
        bearish_signals += 1
    
    if momentum >1.0:
        bullish_signals +=1
    elif momentum < -1.0:
        bearish_signals += 1
    
    if insider_net > 0:
        bullish_signals += 1
    elif insider_net < 0:
        bearish_signals +=1
    
    if row['volume_ratio'] > 1.5:
        if bullish_signals > bearish_signals:
            bullish_signals += 1
        elif bearish_signals > bullish_signals:
            bearish_signals += 1
    if bullish_signals >=2:
        return 'BULLISH'
    elif bearish_signals >= 2:
        return 'BEARISH'
    else:
        return 'NEUTRAL'

def derive_health_score(row) ->float:
    score = 5.0
    score += row['sentiment_score'] * 2.0
    momentum_factor = max(-1.5, min (1.5, row['pct_change_7d'] * 0.15))
    score += momentum_factor

    insider_net = row['insider_bought'] - row['insider_sold']
    if insider_net > 0:
        score += 0.5
    elif insider_net < 0:
        score -= 0.5
    
    if row['news_count_7d'] > 5:
        score += 0.3
    return round(max(0.0, min(10.0, score)), 1)
