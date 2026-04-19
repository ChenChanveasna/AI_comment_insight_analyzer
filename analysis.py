from collections import Counter
import re


STOPWORDS = {
    "a", "about", "after", "again", "all", "also", "am", "and", "any", "are", "as", "at", "be", "because",
    "been", "before", "being", "but", "by", "can", "could", "do", "does", "doing", "down", "during", "each",
    "for", "from", "further", "had", "has", "have", "having", "he", "her", "here", "hers", "herself", "him",
    "himself", "his", "how", "i", "if", "in", "into", "is", "it", "its", "itself", "just", "me", "more",
    "most", "my", "myself", "no", "not", "of", "off", "on", "once", "only", "or", "other", "our", "ours",
    "ourselves", "out", "over", "own", "same", "she", "should", "so", "some", "such", "than", "that", "the",
    "their", "theirs", "them", "themselves", "then", "there", "these", "they", "this", "those", "through", "to",
    "too", "under", "until", "up", "very", "was", "we", "were", "what", "when", "where", "which", "while",
    "who", "whom", "why", "with", "would", "you", "your", "yours", "yourself", "yourselves",
}

POSITIVE_WORDS = {
    "amazing", "awesome", "best", "brilliant", "clean", "cool", "enjoy", "excellent", "fantastic", "good", "great",
    "helpful", "incredible", "love", "lovely", "nice", "perfect", "smart", "super", "useful", "well", "wow", "liked",
    "like", "favourite", "favorite", "thanks", "thank",
}

NEGATIVE_WORDS = {
    "annoying", "bad", "boring", "broken", "confusing", "disappointing", "dreadful", "error", "hate", "horrible",
    "ignore", "lag", "laggy", "lame", "mess", "nonsense", "poor", "problem", "sad", "slow", "stupid", "terrible",
    "ugly", "waste", "weak", "worst", "bug", "bugs", "crash", "crashes", "useless",
}


def split_comment_entry(entry):
    if ": " in entry:
        user, text = entry.split(": ", 1)
    elif ":" in entry:
        user, text = entry.split(":", 1)
    else:
        user, text = "Unknown", entry

    return user.strip() or "Unknown", text.strip()


def tokenize(text):
    return re.findall(r"[a-z']+", text.lower())


def classify_comment(text):
    tokens = tokenize(text)
    positive_hits = sum(token in POSITIVE_WORDS for token in tokens)
    negative_hits = sum(token in NEGATIVE_WORDS for token in tokens)

    if positive_hits > negative_hits:
        label = "positive"
    elif negative_hits > positive_hits:
        label = "negative"
    else:
        label = "neutral"

    total_hits = positive_hits + negative_hits
    confidence = 0.5 if total_hits == 0 else round(0.5 + (abs(positive_hits - negative_hits) / total_hits) * 0.5, 3)

    return {
        "label": label,
        "confidence": confidence,
        "positive_hits": positive_hits,
        "negative_hits": negative_hits,
        "tokens": tokens,
    }


def analyze_comments(comment_entries):
    records = []

    for entry in comment_entries:
        user, text = split_comment_entry(entry)
        if not text:
            continue

        classification = classify_comment(text)
        score = classification["positive_hits"] - classification["negative_hits"]
        records.append(
            {
                "user": user,
                "text": text,
                "label": classification["label"],
                "confidence": classification["confidence"],
                "score": score,
                "word_count": len(classification["tokens"]),
                "tokens": classification["tokens"],
            }
        )

    total_comments = len(records)
    sentiment_counts = Counter(record["label"] for record in records)

    all_tokens = [
        token
        for record in records
        for token in record["tokens"]
        if token not in STOPWORDS and len(token) > 2 and not token.isdigit()
    ]

    word_counts = Counter(all_tokens)

    positive_terms = Counter(
        token
        for record in records
        if record["label"] == "positive"
        for token in record["tokens"]
        if token not in STOPWORDS and len(token) > 2
    )

    negative_terms = Counter(
        token
        for record in records
        if record["label"] == "negative"
        for token in record["tokens"]
        if token not in STOPWORDS and len(token) > 2
    )

    unique_commenters = len({record["user"].lower() for record in records if record["user"] != "Unknown"})
    average_words = round(sum(record["word_count"] for record in records) / total_comments, 1) if total_comments else 0.0

    positive_examples = sorted(records, key=lambda record: (record["score"], record["confidence"]), reverse=True)[:3]
    negative_examples = sorted(records, key=lambda record: (record["score"], record["confidence"]))[:3]

    positive_count = sentiment_counts.get("positive", 0)
    negative_count = sentiment_counts.get("negative", 0)
    if positive_count > negative_count:
        reaction_label = "positive"
    elif negative_count > positive_count:
        reaction_label = "negative"
    else:
        reaction_label = "neutral"

    summary = build_summary(
        total_comments=total_comments,
        sentiment_counts=sentiment_counts,
        reaction_label=reaction_label,
        word_counts=word_counts,
        average_words=average_words,
        unique_commenters=unique_commenters,
    )

    return {
        "total_comments": total_comments,
        "unique_commenters": unique_commenters,
        "average_words": average_words,
        "sentiment_counts": {
            "positive": sentiment_counts.get("positive", 0),
            "negative": sentiment_counts.get("negative", 0),
            "neutral": sentiment_counts.get("neutral", 0),
        },
        "top_words": word_counts.most_common(10),
        "top_positive_terms": positive_terms.most_common(6),
        "top_negative_terms": negative_terms.most_common(6),
        "positive_examples": positive_examples,
        "negative_examples": negative_examples,
        "records": records,
        "summary": summary,
        "reaction_label": reaction_label,
    }


def build_summary(total_comments, sentiment_counts, reaction_label, word_counts, average_words, unique_commenters):
    if total_comments == 0:
        return "No comments were found for this video. Try another link or check whether comments are disabled."

    tone_map = {
        "positive": "more positive than negative",
        "negative": "more negative than positive",
        "neutral": "balanced between positive and negative",
    }
    tone = tone_map.get(reaction_label, "balanced between positive and negative")
    top_terms = [word for word, _ in word_counts.most_common(4)]
    top_term_text = ", ".join(top_terms) if top_terms else "no clear recurring terms"

    return (
        f"Analyzed {total_comments} comments from {unique_commenters} unique commenters. "
        f"The discussion reads as {tone}, with {sentiment_counts.get('positive', 0)} positive, "
        f"{sentiment_counts.get('neutral', 0)} neutral, and {sentiment_counts.get('negative', 0)} negative comments. "
        f"Average comment length is {average_words} words. Repeated topics include {top_term_text}."
    )
